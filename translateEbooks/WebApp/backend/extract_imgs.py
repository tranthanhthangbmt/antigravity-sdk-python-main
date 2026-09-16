import fitz
import os

pdf_path = r"D:\MY_CODE\Antigravity_SDK1\antigravity-sdk-python-main\translateEbooks\JavaProgrammingEbook\JavaProgramming_chaptersPDF\Chapter_05.pdf"
doc = fitz.open(pdf_path)
page = doc[4] 

image_list = page.get_images(full=True)
print(f"Found {len(image_list)} images on page 5")

for i, img in enumerate(image_list):
    xref = img[0]
    base_image = doc.extract_image(xref)
    image_bytes = base_image["image"]
    image_ext = base_image["ext"]
    
    with open(f"test_image_page5_{i}.{image_ext}", "wb") as f:
        f.write(image_bytes)
    print(f"Saved test_image_page5_{i}.{image_ext} size: {len(image_bytes)}")
