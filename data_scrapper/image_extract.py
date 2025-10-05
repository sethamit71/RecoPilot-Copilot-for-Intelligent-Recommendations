import fitz  # from PyMuPDF
import os
import re
import io
from PIL import Image
import pandas as pd

# ----------------------------
# CONFIG
# ----------------------------
pdf_path = "12594102_Labels_Decals.pdf"   # your catalog
output_dir = "output_images"
os.makedirs(output_dir, exist_ok=True)

# Regex for REF IDs
ref_pattern = re.compile(r"(REF\s+[0-9A-Z]+)")

# Open PDF
doc = fitz.open(pdf_path)

results = []

# ----------------------------
# Process all pages
# ----------------------------
for page_num, page in enumerate(doc, start=1):
    # Extract words with positions
    if page_num>=18 and page_num<=284:

        words = page.get_text("words")
        
        word_df = pd.DataFrame(
            words,
            columns=["x0","y0","x1","y1","word","block","line","word_no"]
        )
        
        print(word_df.shape)
        print(word_df[word_df["word"]=="REF"].reset_index().shape)
        
        mask = (word_df["word"].str.len() == 9) & (word_df["word"].shift(1) == "REF")
        idx = word_df[mask].index

        # keep both the matched row and the previous REF row
        filtered_df = word_df.loc[idx.union(idx - 1)]
        #print(filtered_df[filtered_df["word"]=="REF"].reset_index().shape)
        word_df=filtered_df[filtered_df["word"]!="REF"].reset_index().copy()
        
        print(word_df)
        # Group into lines
        file_name=[]
        lines = {}
        for _, row in word_df.iterrows():
            line_key = (row["block"], row["line"])
            lines.setdefault(line_key, []).append(row)
            file_name.append(str(row["word"]))
        
        # Collect REF lines + positions
        line_texts = []
        for line_words in lines.values():
            sorted_words = sorted(line_words, key=lambda r: r["x0"])
            text = " ".join([w["word"] for w in sorted_words])
            bbox = (min([w["x0"] for w in sorted_words]), min([w["y0"] for w in sorted_words]),
                    max([w["x1"] for w in sorted_words]), max([w["y1"] for w in sorted_words]))
            if ref_pattern.search(text):
                line_texts.append({"text": text, "bbox": bbox})

        # Extract images from page
        images=[]
        for i, img in enumerate(page.get_images(full=True), start=1):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image = Image.open(io.BytesIO(image_bytes))
            
            # Get image position
            bbox = page.get_image_bbox(img)
            img_y = (bbox.y0 + bbox.y1) / 2
            images.append({"xref": xref, "image": image, "ext": image_ext, "bbox": bbox})### collect imag
            # 2. Sort images top-to-bottom, then left-to-right
            images = sorted(images, key=lambda im: (round(im["bbox"].y0, -1), im["bbox"].x0))
            ########search below centr
            # Instead of center, take slightly below image
            img_x = (bbox.x0 + bbox.x1) / 2
            img_y = bbox.y1 + 10   # 10 units below bottom edge
            # Find nearest REF text
            nearest_ref = None
            min_dist = float("inf")
            for _, ref in word_df.iterrows():
                ref_x = (ref["x0"] + ref["x1"]) / 2
                ref_y = (ref["y0"] + ref["y1"]) / 2
                dist = (ref_x - img_x)**2 + (ref_y - img_y)**2
                if dist < min_dist:
                    min_dist = dist
                    nearest_ref = ref["word"]

            # Save image with REF ID
            out_name = f"{nearest_ref}_page{page_num-2}_img{i}.{image_ext}"
            out_path = os.path.join(output_dir, out_name)
            image.save(out_path)
            
            
        # # 3. Assign ref IDs from file_name[] after sorting
        # for i, img_info in enumerate(images, start=1):
        #     ref_id = file_name[i-1] if i-1 < len(file_name) else "NotFound"
        #     out_name = f"{ref_id}_page{page_num}_img{i}.{img_info['ext']}"
        #     img_info["image"].save(os.path.join(output_dir, out_name))
        # results.append({
        #         "page": page_num,
        #         "ref_id": "nearest_ref",
        #         "file": "out_path"
        #     })

# ----------------------------
# Summary
# ----------------------------
print("✅ Extraction complete!")
print(f"Images saved in: {output_dir}")
print("Sample results:")
for r in results[:5]:
    print(r)
