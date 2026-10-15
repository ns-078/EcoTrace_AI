import os
import fitz


class PDFAgent:

    def __init__(self):

        self.output_folder = os.path.join(
            os.path.dirname(__file__),
            "..",
            "extracted_text"
        )

        os.makedirs(self.output_folder, exist_ok=True)

    def extract_text(self, pdf_path):

        try:

            print("\n📖 Extracting PDF Content...\n")

            doc = fitz.open(pdf_path)

            text = ""

            for page in doc:
                text += page.get_text()

            doc.close()

            filename = os.path.basename(pdf_path)
            filename = filename.replace(".pdf", ".txt")

            output_path = os.path.join(self.output_folder, filename)

            with open(output_path, "w", encoding="utf-8") as file:
                file.write(text)

            print("✅ Text Extraction Complete")

            print(f"📄 Saved : {output_path}")

            return output_path

        except Exception as e:

            print("❌ PDF Extraction Failed")

            print(e)

            return None