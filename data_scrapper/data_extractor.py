import pdfplumber
import re
import pandas as pd

pdf_path = "12594102_Labels_Decals.pdf"

def extract_ref_and_desc(line):
    match = re.match(r"^([A-Z0-9\-]+)\s+(.*)", line)
    if match:
        ref = match.group(1)
        desc = match.group(2)
        if len(ref) > 2 and len(desc) > 3:
            return ref, desc
    return None, None

products = []
current_category = None

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if text:
            lines = text.split("\n")
            for line in lines:
                line = line.strip()
                if not line:
                    continue

                if not any(char.isdigit() for char in line) and len(line.split()) <= 3 and line.isalpha():
                    current_category = line

                ref, desc = extract_ref_and_desc(line)
                if ref and desc:
                    products.append([i+1, current_category, ref, desc])

df = pd.DataFrame(products, columns=["page", "category", "reference", "description"])
df.to_csv("labels_decals_clean.csv", index=False)
print("Saved to labels_decals_clean.csv")
