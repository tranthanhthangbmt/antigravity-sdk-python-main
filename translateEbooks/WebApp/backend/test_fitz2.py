import fitz

pdf_path = r"D:\MY_CODE\Antigravity_SDK1\antigravity-sdk-python-main\translateEbooks\JavaProgrammingEbook\JavaProgramming_chaptersPDF\Chapter_05.pdf"
doc = fitz.open(pdf_path)
page = doc[3] 
blocks = page.get_text("dict")["blocks"]

for b in blocks:
    if b['type'] == 0:
        text = "".join([l['spans'][0]['text'] for l in b['lines']])
        print(f"TEXT: {text[:50]}...")
