import google.generativeai as genai
from PIL import Image
import os, glob
import time
genai.configure(api_key="AIzaSyDLxvBSLXe2FX4EBBC4mU70zC-06PoKTjY")
model = genai.GenerativeModel("gemini-1.5-flash")
import pandas as pd
#df=pd.read_csv("./tvh_final/tvh_captioned_product.csv").head(2)
#######################################
import google.generativeai as genai
import pandas as pd
from PIL import Image
import os



def refine_caption_gemini(image_path, category, fg, bg, subcategory):
    """
    Generate a refined catalog-style description from an image + metadata.
    """
    img = Image.open(image_path)

    prompt = f"""
You are creating factual product descriptions for a lables and decals and safety label catalog of TVH company.

Input:
- product image : use given product image
- Metadata: Category={category}, Sub-category={subcategory}, Foreground={fg}, Background={bg}.

Task:
Rewrite the caption into a **concise, catalog-style product description**.
Rules:
- Always mention the sign type (safety label, dashboard arrow, warning sign, etc.).
- Always include Foreground and Background colors.
- If the caption suggests a specific symbol/text, include it (e.g., "deadman switch", "LPG warning").
- Do not add creative, marketing, or mystical language.
- Keep it short (less than 2 sentence).
- Example style: "Black on yellow safety warning label: LPG gas hazard".
- Use correct shapes (circle vs triangle) and avoid repeating "symbol" twice in a row.
- Add a short "Purpose: this field require because , user should be able to describe what they want, or even describe the scenario for which they want it and he should be able to point them to the right  product. 

Output:
Return only the final factual product description, nothing else.
"""

    response = model.generate_content([prompt, img])
    return response.text.strip()

input_csv="./tvh_final/tvh_product.csv"
output_csv="./tvh_final/tvh_captioned_gemini.csv"
def process_csv(input_csv, output_csv):
    df = pd.read_csv(input_csv)

    # If resuming, load existing output
    if os.path.exists(output_csv):
        df_out = pd.read_csv(output_csv)
    else:
        df_out = df.copy()
        df_out["description_gemini"] = ""

    for idx, row in df_out.iterrows():
        if pd.isna(row["description_gemini"]) or row["description_gemini"] == "":
            try:
                desc = refine_caption_gemini(
                    row["image_path"],
                
                    row.get("category", ""),
                    row.get("foreground", ""),
                    row.get("background", ""),
                    row.get("sub-category", "")
                )
                df_out.at[idx, "description_gemini"] = desc
                # Save only after success
                df_out.to_csv(output_csv, index=False)
                print("💾 Saved description for:", row["ref_id"])
            except Exception as e:
                df_out.at[idx, "description_gemini"] = f"Error: {e}"
                print(f"[{idx}] ❌ Error: {e}")
                time.sleep(60) 
            # Save after each row → prevents losing progress
            # df_out.to_csv(output_csv, index=False)
            #print("saved description for:",row["ref_id"])
            

    print(f"\n✅ Processing complete. Results saved to {output_csv}")

process_csv(input_csv, output_csv)