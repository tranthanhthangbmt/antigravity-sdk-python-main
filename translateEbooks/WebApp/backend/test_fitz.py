import fitz

pdf_path = r"D:\MY_CODE\Antigravity_SDK1\antigravity-sdk-python-main\translateEbooks\JavaProgrammingEbook\JavaProgramming_chaptersPDF\Chapter_05.pdf"
doc = fitz.open(pdf_path)
page = doc[3] # Trang thứ 4 (chứa Figure 5.1 theo screenshot)
blocks = page.get_text("dict")["blocks"]

for b in blocks:
    if b['type'] == 0:
        # Text block
        text = "".join([l['spans'][0]['text'] for l in b['lines']])
        print(f"TEXT: {text[:50]}...")
    elif b['type'] == 1:
        # Image block
        print(f"IMAGE: format {b.get('ext')}, size {len(b.get('image', b''))} bytes")
