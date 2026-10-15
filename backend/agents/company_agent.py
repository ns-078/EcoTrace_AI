from query_agent import QueryAgent
import requests
from ddgs import DDGS



class CompanyAgent:

    def __init__(self):
        pass

    def search_company(self, company):

        query = f"{company} official company sustainability"

        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))

        if not results:
            return None

        first = results[0]

        return {
            "company": company,
            "title": first["title"],
            "url": first["href"],
            "description": first["body"]
        }

    def search_sustainability_report(self, company):

        query = f"{company} sustainability report pdf"

        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=10))

        for result in results:

            url = result["href"]

            if ".pdf" in url.lower():
                return {
                    "title": result["title"],
                    "url": url
                }

        return None

    def search_news(self, company):

        query = f"{company} environment pollution climate"

        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=10))

        news = []

        for r in results:

            news.append({
                "title": r["title"],
                "url": r["href"],
                "description": r["body"]
            })

        return news


if __name__ == "__main__":

    query = input("Enter Company / Product : ")

    query_agent = QueryAgent()

    result = query_agent.understand_query(query)

    print("\nQuery Result")
    print(result)

    company = result["company"]

    print(f"\nSearching for company: {company}\n")

    agent = CompanyAgent()

    print("Searching Company...\n")
    print(agent.search_company(company))

    print("\nSearching Sustainability Report...\n")
    print(agent.search_sustainability_report(company))

    print("\nSearching News...\n")

    news = agent.search_news(company)

    for item in news:
        print(item)