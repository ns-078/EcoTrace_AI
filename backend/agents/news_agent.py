
import os
import json
from ddgs import DDGS
from groq import Groq
from dotenv import load_dotenv


class NewsAgent:

    def __init__(self):

        load_dotenv(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                ".env"
            )
        )

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise Exception("GROQ_API_KEY not found")

        self.client = Groq(api_key=api_key)

    ########################################################

    def search_news(self, company):

        queries = [

            f"{company} sustainability",

            f"{company} climate",

            f"{company} pollution",

            f"{company} ESG",

            f"{company} environment"

        ]

        articles = []

        visited = set()

        with DDGS() as ddgs:

            for query in queries:

                results = ddgs.text(

                    query,

                    max_results=8

                )

                for r in results:

                    url = r.get("href", "")

                    if url in visited:
                        continue

                    visited.add(url)

                    articles.append({

                        "title": r.get("title", ""),

                        "description": r.get("body", ""),

                        "url": url

                    })

        return articles

    ########################################################

    def classify_article(

        self,

        company,

        article

    ):

        prompt = f"""
You are an ESG News Analyst.

Company:

{company}

News Title:

{article["title"]}

Description:

{article["description"]}

Your task:

1. Ignore news unrelated to ESG or environment.

2. If unrelated return

IGNORE

3. Otherwise classify the article.

Possible sentiment:

Positive

Negative

Neutral

Possible topic:

Climate

Carbon

Energy

Water

Waste

Plastic

Biodiversity

Pollution

Supply Chain

ESG

Governance

Social

Return ONLY JSON.

Example:

{{
"sentiment":"Positive",
"topic":"Energy",
"reason":"..."
}}
"""

        response = self.client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[

                {

                    "role":"user",

                    "content":prompt

                }

            ],

            temperature=0

        )

        answer = response.choices[0].message.content.strip()

        if answer.upper() == "IGNORE":

            return None

        answer = answer.replace(

            "```json",

            ""

        )

        answer = answer.replace(

            "```",

            ""

        ).strip()

        try:

            result = json.loads(answer)

        except:

            return None

        result["title"] = article["title"]

        result["description"] = article["description"]

        result["url"] = article["url"]

        return result

    ########################################################

    def analyze_company(self, company):

        print("\nSearching ESG News...\n")

        articles = self.search_news(company)

        print(

            "Articles Found :",

            len(articles)

        )

        positive = 0

        negative = 0

        neutral = 0

        news = []

        for i, article in enumerate(articles):

            print(

                f"Analyzing {i+1}/{len(articles)}"

            )

            result = self.classify_article(

                company,

                article

            )

            if result is None:

                continue
            news.append(result)
            sentiment = result["sentiment"].lower()

            if sentiment == "positive":
                positive += 1

            elif sentiment == "negative":
                negative += 1

            else:
                neutral += 1

        ####################################################

        if positive > negative:
            overall = "Positive"

        elif negative > positive:
            overall = "Negative"

        else:
            overall = "Neutral"

        output = {

            "company": company,

            "summary": {

                "total_articles": len(news),

                "positive": positive,

                "negative": negative,

                "neutral": neutral,

                "overall_sentiment": overall

            },

            "news": news

        }

        save_folder = os.path.join(

            os.path.dirname(__file__),

            "..",

            "news"

        )

        os.makedirs(save_folder, exist_ok=True)

        save_file = os.path.join(

            save_folder,

            company.replace(" ", "_") + "_news.json"

        )

        with open(save_file, "w", encoding="utf-8") as f:

            json.dump(
                output,
                f,
                indent=4,
                ensure_ascii=False
            )

        return save_file


if __name__ == "__main__":

    company = input("Enter Company : ").strip()

    agent = NewsAgent()

    result = agent.analyze_company(company)

    print("\n==============================")

    print("NEWS ANALYSIS COMPLETED")

    print("==============================")

    print(result)
