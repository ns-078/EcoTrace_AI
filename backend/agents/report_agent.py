import os
import requests

from company_agent import CompanyAgent
from pdf_agent import PDFAgent


class ReportAgent:

    def __init__(self):

        self.company_agent = CompanyAgent()
        self.pdf_agent = PDFAgent()

        self.save_folder = os.path.join(
            os.path.dirname(__file__),
            "..",
            "reports"
        )

        os.makedirs(self.save_folder, exist_ok=True)

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "Accept": "application/pdf,application/octet-stream,*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive"
        }

    def get_report(self, company):

        print(f"\n🔍 Searching Sustainability Report for {company}...\n")

        report = self.company_agent.search_sustainability_report(company)

        if report is None:

            print("❌ Sustainability Report Not Found")

            return None

        pdf_url = report["url"]

        print("📄 Report Found")
        print(pdf_url)

        pdf_path = self.download_report(company, pdf_url)

        if pdf_path is None:
            return None

        print("\n📖 Extracting Report...\n")

        text_path = self.pdf_agent.extract_text(pdf_path)

        print("\n✅ Pipeline Completed Successfully")

        return {
            "company": company,
            "pdf_path": pdf_path,
            "text_path": text_path
        }

    def download_report(self, company, pdf_url):

        try:

            print("\n⬇ Downloading Report...\n")

            response = requests.get(
                pdf_url,
                headers=self.headers,
                stream=True,
                timeout=180,
                allow_redirects=True
            )

            print("Status Code :", response.status_code)

            if response.status_code != 200:

                print("❌ Download Failed")

                return None

            filename = company.replace(" ", "_") + "_Report.pdf"

            filepath = os.path.join(
                self.save_folder,
                filename
            )

            with open(filepath, "wb") as file:

                for chunk in response.iter_content(chunk_size=8192):

                    if chunk:

                        file.write(chunk)

            print("✅ Report Downloaded Successfully")

            print(filepath)

            return filepath

        except Exception as e:

            print("\n❌ Error Downloading PDF")

            print(e)

            return None


if __name__ == "__main__":

    company = input("Enter Company : ")

    agent = ReportAgent()

    result = agent.get_report(company)

    print("\n================ RESULT ================\n")

    print(result)
    