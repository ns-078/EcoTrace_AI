
import os
import json
from groq import Groq
from dotenv import load_dotenv


class ClaimAgent:

    def __init__(self):

        # Load .env from backend folder
        env_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                ".env"
            )
        )

        load_dotenv(env_path)

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise Exception(
                f"GROQ_API_KEY not found!\nExpected .env at:\n{env_path}"
            )

        self.client = Groq(api_key=api_key)

    def extract_claims(self, text_file):

        if not os.path.exists(text_file):
            raise FileNotFoundError(
                f"Text file not found:\n{text_file}"
            )

        print("\nReading Sustainability Report...\n")

        with open(text_file, "r", encoding="utf-8") as file:
            report = file.read()

        # Limit tokens (we'll improve this later with chunking)
        report = report[:15000]

        prompt = f"""
You are an ESG Sustainability Analyst.

Read the sustainability report below.

Extract ONLY important sustainability claims.

Return ONLY valid JSON.

Format:

[
    {{
        "claim":"",
        "category":"",
        "type":"",
        "confidence":""
    }}
]

Categories:

Climate
Carbon
Energy
Water
Waste
Plastic
Net Zero
Governance
Human Rights
Supply Chain
Biodiversity
Social
Other

Types:

Metric
Goal
Achievement
Commitment

Report:

{report}
"""

        print("Sending Report to Llama 3...\n")

        response = self.client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2

        )

        answer = response.choices[0].message.content.strip()

        if answer.startswith("```json"):
            answer = answer.replace("```json", "")

        if answer.endswith("```"):
            answer = answer.replace("```", "")

        answer = answer.strip()

        try:

            claims = json.loads(answer)

        except Exception:

            print("\nJSON Parsing Failed.")
            print("Saving Raw Output Instead.\n")

            claims = {
                "raw_output": answer
            }

        output_folder = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "claims"
            )
        )

        os.makedirs(output_folder, exist_ok=True)

        filename = os.path.basename(text_file).replace(
            ".txt",
            "_claims.json"
        )

        save_path = os.path.join(
            output_folder,
            filename
        )

        with open(save_path, "w", encoding="utf-8") as file:

            json.dump(
                claims,
                file,
                indent=4,
                ensure_ascii=False
            )

        return save_path


if __name__ == "__main__":

    company = input("Enter Company : ").strip()

    text_file = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "extracted_text",
            company.replace(" ", "_") + "_Report.txt"
        )
    )

    print("\nText File:")
    print(text_file)

    agent = ClaimAgent()

    output = agent.extract_claims(text_file)

    print("\n===================================")
    print("✅ CLAIM EXTRACTION COMPLETED")
    print("===================================")
    print(output)