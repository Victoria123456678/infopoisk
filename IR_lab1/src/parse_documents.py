# src/parse_documents.py
import os
from bs4 import BeautifulSoup
import fitz

input_folder = "../data/raw"
output_folder = "../data/processed"

os.makedirs(output_folder, exist_ok=True)

processed_count = 0

for root, dirs, files in os.walk(input_folder):
    for file_name in files:
        file_path = os.path.join(root, file_name)
        clean_text = ""

        try:
            # PDF
            if file_name.lower().endswith(".pdf"):
                doc = fitz.open(file_path)
                for page in doc:
                    clean_text += page.get_text()
                doc.close()

            # HTML / TXT
            elif file_name.lower().endswith((".html", ".htm", ".txt")):
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()

                soup = BeautifulSoup(text, "html.parser")
                clean_text = soup.get_text()

        except Exception as e:
            print(f"Ошибка обработки {file_name}: {e}")
            continue

        # очистка
        clean_text = " ".join(clean_text.split())

        if clean_text:
            base_name = os.path.splitext(file_name)[0]
            out_path = os.path.join(output_folder, base_name + ".txt")

            with open(out_path, "w", encoding="utf-8") as f:
                f.write(clean_text)

            processed_count += 1

print(f"✅ Обработано документов: {processed_count}")