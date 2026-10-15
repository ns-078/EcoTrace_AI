
import os
import json
from collections import Counter


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

        category_counter = Counter()

        strengths = []
        weaknesses = []
        red_flags = []

        for item in claims:

            category = item["category"]

            category_counter[category] += 1

            status = item["verification"]["status"]

            if status == "Verified":

                verified += 1

                strengths.append(item["claim"])

            elif status == "Partially Verified":

                partial += 1

                weaknesses.append(item["claim"])

            elif status == "Potential Greenwashing":

                greenwashing += 1

                red_flags.append(item["claim"])

            else:

                insufficient += 1

        ########################################################

        score = (
            verified * 10
            + partial * 5
            - greenwashing * 20
        )

        if total_claims > 0:

            score = round(
                (score / (total_claims * 10)) * 100
            )

        score = max(0, min(100, score))

        ########################################################

        if score >= 80:

            risk = "Low"

        elif score >= 60:

            risk = "Medium"

        else:

            risk = "High"

        ########################################################

        if strengths:

            top_strengths = strengths[:5]

        else:

            top_strengths = []

        if weaknesses:

            top_weaknesses = weaknesses[:5]

        else:

            top_weaknesses = []

        if red_flags:

            top_red_flags = red_flags[:5]

        else:

            top_red_flags = []

        ########################################################

        if len(category_counter) > 0:

            strongest_category = category_counter.most_common(1)[0][0]

        else:

            strongest_category = "None"

        ########################################################

        summary = self.generate_summary(

            company,

            score,

            verified,

            partial,

            greenwashing,

            insufficient

        )
                ########################################################

        recommendations = self.generate_recommendations(

            greenwashing,

            insufficient,

            partial

        )

        ########################################################

        output = {

            "company": company,

            "overall_score": score,

            "risk_level": risk,

            "summary": summary,

            "statistics": {

                "total_claims": total_claims,

                "verified": verified,

                "partially_verified": partial,

                "potential_greenwashing": greenwashing,

                "insufficient_evidence": insufficient

            },

            "category_distribution": dict(category_counter),

            "strongest_category": strongest_category,

            "strengths": top_strengths,

            "weaknesses": top_weaknesses,

            "red_flags": top_red_flags,

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

        score,

        verified,

        partial,

        greenwashing,

        insufficient

    ):

        if score >= 80:

            return (

                f"{company} demonstrates strong ESG disclosure. "

                f"Most sustainability claims are independently supported. "

                f"No major greenwashing concerns were identified."

            )

        elif score >= 60:

            return (

                f"{company} shows moderate ESG performance. "

                f"Several claims are supported, but additional "

                f"independent evidence would improve credibility."

            )

        else:

            return (

                f"{company} presents limited independently verified "

                f"sustainability evidence. Several claims require "

                f"additional external validation."

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

                "Improve transparency and avoid unsupported environmental claims."

            )

        if insufficient > 0:

            recommendations.append(

                "Provide more third-party verified ESG disclosures."

            )

        if partial > 0:

            recommendations.append(

                "Strengthen sustainability reporting with measurable evidence."

            )

        if (

            greenwashing == 0

            and insufficient == 0

            and partial == 0

        ):

            recommendations.append(

                "Maintain current sustainability reporting standards."

            )

        return recommendations


############################################################


if __name__ == "__main__":

    company = input("Enter Company : ").strip()

    agent = AnalysisAgent()

    result = agent.analyze(company)

    print("\n====================================")

    print("ANALYSIS COMPLETED")

    print("====================================")

    print(result)

    print("\nOpen the analysis folder to view the JSON report.")