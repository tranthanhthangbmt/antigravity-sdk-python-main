import fitz

pdf_path = r"D:\MY_CODE\Antigravity_SDK1\antigravity-sdk-python-main\translateEbooks\JavaProgrammingEbook\JavaProgramming_chaptersPDF\Chapter_05.pdf"
doc = fitz.open(pdf_path)
page = doc[3] 

drawings = page.get_drawings()
if drawings:
    rect = fitz.Rect()
    for d in drawings:
        rect.include_rect(d["rect"])
    
    print(f"Found drawings with bounding box: {rect}")
    # Render just this rect
    pix = page.get_pixmap(clip=rect, dpi=150)
    pix.save("test_drawing.png")
    print("Saved test_drawing.png")
else:
    print("No drawings found")
