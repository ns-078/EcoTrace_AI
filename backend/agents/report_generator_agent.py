
import os
import json


class ReportGenerator:

    def __init__(self):

        self.base_path = os.path.join(
            os.path.dirname(__file__),
            ".."
        )

    ########################################################

    def load_json(self, path):

        if not os.path.exists(path):
            raise Exception(f"File not found : {path}")

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    ########################################################

    def generate_report(self, company):

        print("\nGenerating Final ESG Report...\n")

        analysis_file = os.path.join(

            self.base_path,

            "analysis",

            company.replace(" ", "_") +

            "_analysis.json"

        )

        verification_file = os.path.join(

            self.base_path,

            "verification",

            company.replace(" ", "_") +

            "_verification.json"

        )

        news_file = os.path.join(

            self.base_path,

            "news",

            company.replace(" ", "_") +

            "_news.json"

        )

        analysis = self.load_json(analysis_file)

        verification = self.load_json(verification_file)

        news = self.load_json(news_file)

        ####################################################

        company_name = analysis["company"]

        esg_grade = analysis["esg_grade"]

        verification_score = analysis["verification_score"]

        greenwashing_score = analysis["greenwashing_score"]

        confidence_score = analysis["confidence_score"]

        risk_level = analysis["risk_level"]

        summary = analysis["summary"]

        recommendations = analysis["recommendations"]

        statistics = analysis["statistics"]

        category_analysis = analysis["category_analysis"]

        strongest_category = analysis["strongest_category"]

        ####################################################

        news_summary = news["summary"]

        total_news = news_summary["total_articles"]

        positive_news = news_summary["positive"]

        negative_news = news_summary["negative"]

        neutral_news = news_summary["neutral"]

        overall_news = news_summary["overall_sentiment"]

        ####################################################

        verified_claims = []

        partial_claims = []

        greenwashing_claims = []

        insufficient_claims = []

        for claim in verification["claims"]:

            status = claim["verification"]["status"]

            if status == "Verified":

                verified_claims.append(claim["claim"])

            elif status == "Partially Verified":

                partial_claims.append(claim["claim"])

            elif status == "Potential Greenwashing":

                greenwashing_claims.append(claim["claim"])

            else:

                insufficient_claims.append(claim["claim"])
                ####################################################

        final_report = {

            "company": company_name,

            "esg_grade": esg_grade,

            "verification_score": verification_score,

            "greenwashing_score": greenwashing_score,

            "confidence_score": confidence_score,

            "risk_level": risk_level,

            "summary": summary,

            "news_summary": {

                "overall_sentiment": overall_news,

                "total_articles": total_news,

                "positive": positive_news,

                "negative": negative_news,

                "neutral": neutral_news

            },

            "statistics": statistics,

            "strongest_category": strongest_category,

            "category_analysis": category_analysis,

            "verified_claims": verified_claims,

            "partially_verified_claims": partial_claims,

            "potential_greenwashing_claims": greenwashing_claims,

            "insufficient_evidence_claims": insufficient_claims,

            "recommendations": recommendations

        }

        ####################################################

        save_folder = os.path.join(

            self.base_path,

            "final_reports"

        )

        os.makedirs(

            save_folder,

            exist_ok=True

        )

        save_file = os.path.join(

            save_folder,

            company.replace(" ", "_") +

            "_final_report.json"

        )

        with open(

            save_file,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                final_report,

                f,

                indent=4,

                ensure_ascii=False

            )

        print("\nFinal Report Saved Successfully")

        print(save_file)

        return save_file


############################################################

if __name__ == "__main__":

    company = input("Enter Company : ").strip()

    generator = ReportGenerator()

    result = generator.generate_report(company)

    print("\n==============================")

    print("FINAL REPORT GENERATED")

    print("==============================")

    print(result)