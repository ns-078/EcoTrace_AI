
import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class QueryAgent:

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")

        self.client = Groq(api_key=api_key)

    def understand_query(self, query):

        prompt = f"""
You are EcoTrace AI's Query Understanding Agent.

Your job is to understand what the user entered.

The user may enter:
- Company name
- Product name
- Brand name
- Service name
- Initiative

Identify:

1. type
2. company
3. product

Rules:

- If only a company is entered, type = Company.
- If a product is entered, identify its parent company.
- If a brand is entered, identify its owner company.
- If unsure, make the best possible inference.
- Return ONLY valid JSON.
- Do not return markdown.
- Do not explain.

Example 1

Input:
Tesla

Output:
{{
"type":"Company",
"company":"Tesla",
"product":null
}}

Example 2

Input:
Tesla Cybertruck

Output:
{{
"type":"Product",
"company":"Tesla",
"product":"Cybertruck"
}}

Example 3

Input:
Maggi

Output:
{{
"type":"Product",
"company":"Nestlé",
"product":"Maggi"
}}

Example 4

Input:
Apple Vision Pro

Output:
{{
"type":"Product",
"company":"Apple",
"product":"Vision Pro"
}}

User Query:

{query}
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        answer = response.choices[0].message.content.strip()

        answer = re.sub(r"```json", "", answer)
        answer = re.sub(r"```", "", answer)
        answer = answer.strip()

        try:

            result = json.loads(answer)

            result["query"] = query

            return result

        except Exception:

            return {
                "query": query,
                "type": "Unknown",
                "company": query,
                "product": None
            }


if __name__ == "__main__":

    agent = QueryAgent()

    while True:

        q = input("\nEnter Company / Product : ")

        result = agent.understand_query(q)

        print("\nResult:\n")

        print(json.dumps(result, indent=4))