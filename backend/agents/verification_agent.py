
import os
import json
from collections import defaultdict


class AnalysisAgent:

    def __init__(self):

        self.base_folder = os.path.join(
            os.path.dirname(__file__),
            ".."
        )

    ############################################################

    def load_verification(self, company):

        file_path = os.path.join(
            self.base_folder,
            "verification",
            company.replace(" ", "_") + "_verification.json"
        )

        if not os.path.exists(file_path):
            raise Exception("Verification file not found.")

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    ############################################################

    def analyze(self, company):

        data = self.load_verification(company)

        claims = data["claims"]

        total_claims = len(claims)

        verified = 0
        partial = 0
        greenwashing = 0
        insufficient = 0

        strengths = []
        needs_verification = []
        red_flags = []

        category_stats = defaultdict(lambda: {
            "total": 0,
            "verified": 0,
            "partial": 0,
            "greenwashing": 0,
            "insufficient": 0
        })

        ########################################################

        for item in claims:

            category = item["category"]

            status = item["verification"]["status"]

            category_stats[category]["total"] += 1

            if status == "Verified":

                verified += 1

                category_stats[category]["verified"] += 1

                strengths.append(item["claim"])

            elif status == "Partially Verified":

                partial += 1

                category_stats[category]["partial"] += 1

                needs_verification.append(item["claim"])

            elif status == "Potential Greenwashing":

                greenwashing += 1

                category_stats[category]["greenwashing"] += 1

                red_flags.append(item["claim"])

            else:

                insufficient += 1

                category_stats[category]["insufficient"] += 1

        ########################################################
        # Verification Score

        verification_grade = round(

            (
                verified +
                (0.5 * partial)
            ) / total_claims * 100,

            2

        )

        ########################################################
        # Greenwashing Score

        greenwashing_score = round(

            (
                greenwashing /
                total_claims
            ) * 100,

            2

        )

        ########################################################
        # Confidence Score

        confidence_score = round(

            (
                verified +
                partial
            ) / total_claims * 100,

            2

        )

        ########################################################
        # ESG Grade

        if verification_grade >= 85:

            grade = "A"

        elif verification_grade >= 70:

            grade = "B"

        elif verification_grade >= 50:

            grade = "C"

        else:

            grade = "D"

        ########################################################
        # Risk Level

        if greenwashing_score >= 40:

            risk = "High"

        elif greenwashing_score >= 15:

            risk = "Medium"

        else:

            risk = "Low"

        ########################################################
        # Strongest Category

        strongest_category = "None"

        strongest_percentage = -1

        category_output = {}

        for category, stats in category_stats.items():

            total = stats["total"]

            percentage = round(

                (
                    stats["verified"] +
                    0.5 * stats["partial"]
                ) / total * 100,

                2

            )

            category_output[category] = {

                "claims": total,

                "verified": stats["verified"],

                "partial": stats["partial"],

                "greenwashing": stats["greenwashing"],

                "insufficient": stats["insufficient"],

                "verification_percentage": percentage

            }

            if percentage > strongest_percentage:

                strongest_percentage = percentage

                strongest_category = category

        ########################################################

        summary = self.generate_summary(

            company,

            verification_grade,

            greenwashing_score,

            verified,

            partial,

            greenwashing,

            insufficient

        )

        recommendations = self.generate_recommendations(

            greenwashing,

            insufficient,

            partial
        )
                ########################################################

        output = {

            "company": company,

            "verification_score": verification_grade,

            "greenwashing_score": greenwashing_score,

            "confidence_score": confidence_score,

            "esg_grade": grade,

            "risk_level": risk,

            "summary": summary,

            "statistics": {

                "total_claims": total_claims,

                "verified": verified,

                "partially_verified": partial,

                "potential_greenwashing": greenwashing,

                "insufficient_evidence": insufficient

            },

            "category_analysis": category_output,

            "strongest_category": strongest_category,

            "strengths": strengths[:5],

            "needs_further_verification": needs_verification[:5],

            "red_flags": red_flags[:5],

            "recommendations": recommendations

        }

        save_folder = os.path.join(

            self.base_folder,

            "analysis"

        )

        os.makedirs(save_folder, exist_ok=True)

        save_file = os.path.join(

            save_folder,

            company.replace(" ", "_") +

            "_analysis.json"

        )

        with open(

            save_file,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                output,

                f,

                indent=4,

                ensure_ascii=False

            )

        return save_file

    ############################################################

    def generate_summary(

        self,

        company,

        verification_grade,

        greenwashing_score,

        verified,

        partial,

        greenwashing,

        insufficient

    ):

        if greenwashing > 0:

            return (

                f"{company} has {greenwashing} claim(s) that may indicate "

                f"potential greenwashing. Independent verification should "

                f"be strengthened before these claims can be fully trusted."

            )

        if verification_score >= 80:

            return (

                f"{company} demonstrates strong sustainability reporting. "

                f"Most ESG claims are supported by independent evidence "

                f"and the overall greenwashing risk is low."

            )

        elif verification_score >= 60:

            return (

                f"{company} demonstrates moderate sustainability "

                f"performance. Several claims are independently supported, "

                f"while some require additional external validation."

            )

        else:

            return (

                f"{company}'s sustainability report contains numerous claims "

                f"that currently lack sufficient independent verification. "

                f"This does not necessarily indicate greenwashing, but "

                f"additional third-party evidence would improve credibility."

            )

    ############################################################

    def generate_recommendations(

        self,

        greenwashing,

        insufficient,

        partial

    ):

        recommendations = []

        if greenwashing > 0:

            recommendations.append(

                "Review environmental claims that are contradicted by independent evidence."

            )

            recommendations.append(

                "Increase transparency for ESG disclosures."

            )

        if insufficient > 0:

            recommendations.append(

                "Publish more independently audited sustainability metrics."

            )

            recommendations.append(

                "Provide third-party ESG assurance wherever possible."

            )

        if partial > 0:

            recommendations.append(

                "Include measurable KPIs for renewable energy, emissions, water and waste."

            )

            recommendations.append(

                "Strengthen evidence supporting partially verified sustainability claims."

            )

        if (

            greenwashing == 0

            and insufficient == 0

            and partial == 0

        ):

            recommendations.append(

                "Maintain current sustainability reporting standards and continue independent assurance."

            )

        return recommendations


############################################################

if __name__ == "__main__":

    company = input("Enter Company : ").strip()

    agent = AnalysisAgent()

    result = agent.analyze(company)

    print("\n===================================")

    print("ANALYSIS COMPLETED")

    print("===================================")

    print(result)

    print("\nOpen the analysis folder to view the generated JSON report.")