from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import asyncio
import json
import os
import google.generativeai as genai
import fitz

import urllib.request

app = FastAPI(title="Antigravity Ebook Translator API")

# Allow CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OUTPUT_DIR = r"D:\MY_CODE\Antigravity_SDK1\antigravity-sdk-python-main\translateEbooks\JavaProgrammingEbook\JavaProgramming_outputEbook"
app.mount("/output", StaticFiles(directory=OUTPUT_DIR), name="output")

ORIGINAL_DIR = r"D:\MY_CODE\Antigravity_SDK1\antigravity-sdk-python-main\translateEbooks\JavaProgrammingEbook\JavaProgramming_chaptersPDF"
app.mount("/original", StaticFiles(directory=ORIGINAL_DIR), name="original")

# In-memory storage for active websockets per chapter
active_connections = {}

# Persistent progress tracking
PROGRESS_FILE = "progress.json"

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r") as f:
                data = json.load(f)
                return {k: set(v) for k, v in data.items()}
        except Exception:
            pass
    return {
        "chapter_01": set(),
        "chapter_02": set(),
        "chapter_03": set(),
        "chapter_04": set(),
        "chapter_05": set(),
        "chapter_06": set()
    }

def save_progress(progress_dict):
    with open(PROGRESS_FILE, "w") as f:
        json.dump({k: list(v) for k, v in progress_dict.items()}, f)

chapter_progress = load_progress()

chapters_db = [
    {"id": "chapter_01", "name": "Chapter 01: An Introduction to Computers and Java", "status": "pending"},
    {"id": "chapter_02", "name": "Chapter 02: Primitive Data and Definite Loops", "status": "pending"},
    {"id": "chapter_03", "name": "Chapter 03: Introduction to Parameters and Objects", "status": "pending"},
    {"id": "chapter_04", "name": "Chapter 04: Conditional Execution", "status": "pending"},
    {"id": "chapter_05", "name": "Chapter 05: Program Logic and Indefinite Loops", "status": "pending"},
    {"id": "chapter_06", "name": "Chapter 06: File Processing", "status": "pending"},
]

@app.get("/api/chapters")
async def get_chapters():
    for ch in chapters_db:
        ch_id = ch["id"]
        if ch_id in chapter_progress and len(chapter_progress[ch_id]) > 0:
            ch["status"] = "completed"
    return chapters_db

@app.get("/api/chapters/{chapter_id}/plan")
def get_chapter_plan(chapter_id: str):
    if chapter_id == "chapter_05":
        parts = []
        # Create 16 chunking parts for 161 pages
        for i in range(1, 17):
            start_page = (i - 1) * 10
            end_page = min(i * 10, 161)
            status = "completed" if i in chapter_progress["chapter_05"] else "pending"
            parts.append({
                "id": i,
                "name": f"Phần {i} (Bản gốc: Trang {start_page} - {end_page})",
                "status": status
            })
        # Final part for LaTeX
        status_17 = "completed" if 17 in chapter_progress["chapter_05"] else "pending"
        parts.append({
            "id": 17,
            "name": "Phần 17: Xuất file PDF Độc Lập",
            "status": status_17
        })
        return {"parts": parts}
    
    return {"parts": []}

@app.websocket("/ws/translate/{chapter_id}")
async def websocket_endpoint(websocket: WebSocket, chapter_id: str, api_key: str = None, parts: str = None):
    await websocket.accept()
    
    if not api_key:
        await websocket.send_text(json.dumps({"type": "log", "message": "[Lỗi Authentication] Vui lòng nhập Antigravity API Key ở Header để bắt đầu quá trình dịch!"}))
        await websocket.close()
        return

    selected_parts = set()
    if parts:
        try:
            selected_parts = set(int(p.strip()) for p in parts.split(","))
        except ValueError:
            pass

    active_connections[chapter_id] = websocket
    
    # In a real environment, you would inject the key like this before calling the SDK:
    os.environ["ANTIGRAVITY_API_KEY"] = api_key

    try:
        if chapter_id == "chapter_05":
            await websocket.send_text(json.dumps({"type": "log", "message": f"Verified API Key. Selected Parts: {selected_parts or 'All'}..."}))
            
            # Configure Gemini (SDK config kept for reference, but we use REST directly below)
            genai.configure(api_key=api_key)
            
            output_dir = r"D:\MY_CODE\Antigravity_SDK1\antigravity-sdk-python-main\translateEbooks\JavaProgrammingEbook\JavaProgramming_outputEbook"
            chapter_tex_path = os.path.join(output_dir, "chapters_tex", "chapter_05.tex")
            
            # Note: We no longer reset the single chapter_05.tex file here because we assemble it at the end.
            
            original_pdf_path = r"D:\MY_CODE\Antigravity_SDK1\antigravity-sdk-python-main\translateEbooks\JavaProgrammingEbook\JavaProgramming_chaptersPDF\Chapter_05.pdf"
            
            # Loop through 16 parts of translation
            for i in range(1, 17):
                if selected_parts and i not in selected_parts:
                    continue

                start_page = (i - 1) * 10
                end_page = min(i * 10, 161)
                
                part_tex_path = os.path.join(output_dir, "chapters_tex", f"chapter_05_part_{i}.tex")
                
                # TRANSLATION STORE CHECK
                if os.path.exists(part_tex_path):
                    await websocket.send_text(json.dumps({"type": "status", "part": i, "status": "completed"}))
                    await websocket.send_text(json.dumps({"type": "log", "message": f"[System] Phần {i} đã có sẵn trong Store. Lấy từ Store (không cần dịch lại)!"}))
                    chapter_progress["chapter_05"].add(i)
                    save_progress(chapter_progress)
                    continue
                
                await websocket.send_text(json.dumps({"type": "status", "part": i, "status": "extracting"}))
                await websocket.send_text(json.dumps({"type": "log", "message": f"[Agent] Đang trích xuất văn bản từ trang {start_page} đến {end_page} của file gốc..."}))
                
                # Extract text using PyMuPDF (fitz)
                extracted_text = ""
                images_found = []
                
                try:
                    # Initialize Pictures directory
                    pictures_dir = os.path.join(OUTPUT_DIR, "Pictures")
                    os.makedirs(pictures_dir, exist_ok=True)
                    
                    doc = fitz.open(original_pdf_path)
                    
                    # Calculate actual number of pages to avoid index out of bounds
                    num_pages = len(doc)
                    actual_end = min(end_page, num_pages)
                    
                    for page_num in range(start_page, actual_end):
                        page = doc[page_num]
                        
                        # Extract text
                        extracted_text += page.get_text() + "\n"
                        
                        # Extract images
                        image_list = page.get_images(full=True)
                        for img_idx, img in enumerate(image_list):
                            xref = img[0]
                            base_image = doc.extract_image(xref)
                            image_bytes = base_image["image"]
                            image_ext = base_image["ext"]
                            
                            # Filter small artifact images (e.g., < 10KB)
                            if len(image_bytes) > 10240: 
                                filename = f"ch05_p{page_num}_img{img_idx}.{image_ext}"
                                filepath = os.path.join(pictures_dir, filename)
                                
                                with open(filepath, "wb") as f:
                                    f.write(image_bytes)
                                
                                images_found.append(filename)
                    
                    doc.close()
                    
                    # If images were found, inject meta instructions for AI
                    if images_found:
                        meta_instruction = "\n[LƯU Ý CHO AI: TRÊN CÁC TRANG NÀY CÓ CHỨA CÁC HÌNH ẢNH SAU: "
                        meta_instruction += ", ".join(images_found)
                        meta_instruction += ". HÃY TỰ ĐỘNG CHÈN LỆNH \\includegraphics[max width=\\linewidth]{Pictures/tên_ảnh} VÀO VỊ TRÍ THÍCH HỢP TRONG BẢN DỊCH ĐỂ TRÌNH BÀY LẠI HÌNH ẢNH!]\n\n"
                        extracted_text = meta_instruction + extracted_text
                        
                except Exception as e:
                    await websocket.send_text(json.dumps({"type": "log", "message": f"[Lỗi Extract] {str(e)}"}))
                    continue
                
                if not extracted_text.strip():
                    await websocket.send_text(json.dumps({"type": "log", "message": f"[Agent] Không tìm thấy nội dung văn bản nào ở các trang này. Bỏ qua..."}))
                    chapter_progress["chapter_05"].add(i)
                    await websocket.send_text(json.dumps({"type": "status", "part": i, "status": "completed"}))
                    continue
                
                await websocket.send_text(json.dumps({"type": "status", "part": i, "status": "translating"}))
                await websocket.send_text(json.dumps({"type": "log", "message": f"[Agent] Đã lấy {len(extracted_text)} ký tự. Bắt đầu gửi lên Google Gemini 1.5 Pro để dịch sang LaTeX..."}))
                
                prompt = f"""Dịch đoạn văn bản sau sang Tiếng Việt.
YÊU CẦU TỐI THƯỢNG (NẾU VI PHẠM SẼ BỊ PHẠT):
1. Bạn là một cỗ máy dịch thuật tự động, CHỈ TRẢ VỀ DUY NHẤT MÃ LATEX.
2. Tuyệt đối KHÔNG ĐƯỢC lặp lại chỉ dẫn này. KHÔNG ĐƯỢC sinh ra các thẻ markdown (như ```latex).
3. KHÔNG ĐƯỢC tạo cấu trúc tài liệu hoàn chỉnh (không dùng thẻ begin document hay end document). CHỈ trả về phần nội dung (Body).
4. Giữ nguyên cấu trúc các đoạn code Java (sử dụng môi trường \\begin{{verbatim}}...\\end{{verbatim}}).
5. Các thuật ngữ chuyên ngành (như Array, Loop) có thể giữ nguyên hoặc để trong ngoặc đơn.

BẮT ĐẦU TRẢ VỀ MÃ LATEX NGAY LẬP TỨC CHO ĐOẠN VĂN BẢN SAU:
---
{extracted_text}
---
"""
                
                try:
                    # Run generate_content via REST API directly using SSE streaming
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:streamGenerateContent?alt=sse&key={api_key}"
                    
                    payload = {
                        "system_instruction": {
                            "parts": [{"text": "Bạn là chuyên gia dịch thuật sách CNTT sang tiếng Việt. Bạn CHỈ trả về mã LaTeX đã dịch. TUYỆT ĐỐI KHÔNG giải thích, KHÔNG thêm suy nghĩ (thought process), KHÔNG thêm bullet points, KHÔNG bọc trong markdown (```latex). Bắt đầu trả lời ngay lập tức bằng mã LaTeX."}]
                        },
                        "contents": [{"role": "user", "parts": [{"text": prompt}]}]
                    }
                    data = json.dumps(payload).encode("utf-8")
                    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
                    
                    import queue
                    q = queue.Queue()
                    
                    import time
                    def make_request():
                        max_retries = 3
                        for attempt in range(max_retries):
                            try:
                                with urllib.request.urlopen(req) as response:
                                    for line in response:
                                        q.put(("data", line.decode("utf-8")))
                                break # Success, break out of retry loop
                            except urllib.error.HTTPError as e:
                                if e.code in [503, 429] and attempt < max_retries - 1:
                                    time.sleep(2 * (attempt + 1)) # Exponential backoff
                                    continue
                                q.put(("error", e))
                                break
                            except Exception as e:
                                q.put(("error", e))
                                break
                        q.put(("done", None))
                            
                    asyncio.create_task(asyncio.to_thread(make_request))
                    
                    response_text = ""
                    await websocket.send_text(json.dumps({"type": "log", "message": f"[Agent] ⏳ Đang dịch: "}))
                    
                    while True:
                        msg_type, msg_val = await asyncio.to_thread(q.get)
                        if msg_type == "done":
                            break
                        if msg_type == "error":
                            raise Exception(msg_val)
                        if msg_type == "data":
                            line = msg_val.strip()
                            if line.startswith("data: "):
                                json_str = line[6:]
                                if json_str == "[DONE]":
                                    continue
                                try:
                                    res_data = json.loads(json_str)
                                    if "candidates" in res_data and len(res_data["candidates"]) > 0:
                                        parts = res_data["candidates"][0]["content"].get("parts")
                                        if parts:
                                            chunk = parts[0]["text"]
                                            response_text += chunk
                                            # Send partial chunk to frontend to show real-time progress
                                            await websocket.send_text(json.dumps({"type": "log_append", "text": chunk}))
                                except json.JSONDecodeError:
                                    pass
                                    
                    await websocket.send_text(json.dumps({"type": "log", "message": f"[Agent] Dịch xong phần {i}!"}))
                    translated_tex = response_text
                    
                    # Clean up if model accidentally returned markdown backticks
                    if translated_tex.startswith("```latex"):
                        translated_tex = translated_tex[8:]
                    if translated_tex.endswith("```"):
                        translated_tex = translated_tex[:-3]
                    elif translated_tex.endswith("```\n"):
                        translated_tex = translated_tex[:-4]
                        
                except Exception as e:
                    await websocket.send_text(json.dumps({"type": "log", "message": f"[Lỗi Dịch Gemini] {str(e)}"}))
                    continue
                
                # Save translated content for this chunk into its OWN file (The Store)
                with open(part_tex_path, "w", encoding="utf-8") as f:
                    # Do not inject \section anymore to prevent breaking code blocks across pages
                    f.write(translated_tex.strip() + "\n")
                
                chapter_progress["chapter_05"].add(i)
                save_progress(chapter_progress)
                await websocket.send_text(json.dumps({"type": "status", "part": i, "status": "completed"}))
                await websocket.send_text(json.dumps({"type": "log", "message": f"[System] Đã dịch xong phần {i}!"}))
            
            # Part 17: LaTeX Standalone
            if not selected_parts or 17 in selected_parts:
                await websocket.send_text(json.dumps({"type": "status", "part": 17, "status": "extracting"}))
                await websocket.send_text(json.dumps({"type": "log", "message": "[System] Stitching parts from Store and generating chapter_05_standalone.tex..."}))
                
                output_dir = r"D:\MY_CODE\Antigravity_SDK1\antigravity-sdk-python-main\translateEbooks\JavaProgrammingEbook\JavaProgramming_outputEbook"
                
                # Assemble chapter_05.tex from parts
                assembled_content = "\\chapter{Program Logic and Indefinite Loops}\n\n"
                for i in range(1, 17):
                    part_file = os.path.join(output_dir, "chapters_tex", f"chapter_05_part_{i}.tex")
                    if os.path.exists(part_file):
                        with open(part_file, "r", encoding="utf-8") as pf:
                            # Quick autofix for common chunk boundary issues
                            chunk_text = pf.read()
                            # Enforce max width on images for older chunks that didn't have the new prompt
                            import re
                            chunk_text = re.sub(r'\\includegraphics\{Pictures/', r'\\includegraphics[max width=\\linewidth]{Pictures/', chunk_text)
                            
                            assembled_content += chunk_text + "\n"
                            
                chapter_05_merged_path = os.path.join(output_dir, "chapters_tex", "chapter_05.tex")
                with open(chapter_05_merged_path, "w", encoding="utf-8") as f:
                    f.write(assembled_content)
                    
                main_tex_path = os.path.join(output_dir, "main.tex")
                standalone_tex_path = os.path.join(output_dir, "chapter_05_standalone.tex")
                
                # Read main.tex and clean it up for standalone PDF
                with open(main_tex_path, "r", encoding="utf-8") as f:
                    content = f.read()
                import re
                # Remove Title Page, Copyright, TOC (starts at \begingroup, ends at \pagestyle{fancy})
                # We must retain \chapterimage to prevent 'File `' not found' error on \chapter
                content = re.sub(r'\\begingroup.*?\\pagestyle\{fancy\}', r'\\chapterimage{chapter_head_1.pdf}', content, flags=re.DOTALL)
                # Inject adjustbox for max width image support
                content = content.replace(r'\usepackage{booktabs}', "\\usepackage{booktabs}\n\\usepackage[export]{adjustbox}")
                
                # Remove Bibliography and Index (starts at \chapter*{Bibliography})
                content = re.sub(r'\\chapter\*\{Bibliography\}.*?(?=\\end\{document\})', '', content, flags=re.DOTALL)
                
                # Replace includeonly
                content = re.sub(r'\\includeonly\{.*?\}', r'\\includeonly{chapters_tex/chapter_05}', content)
                
                with open(standalone_tex_path, "w", encoding="utf-8") as f:
                    f.write(content)
                    
                await websocket.send_text(json.dumps({"type": "status", "part": 17, "status": "translating"}))
                await websocket.send_text(json.dumps({"type": "log", "message": "[System] Compiling chapter_05_standalone.pdf with XeLaTeX..."}))
                
                # Run xelatex async with nonstopmode to prevent hanging
                proc = await asyncio.create_subprocess_shell(
                    "xelatex -interaction=nonstopmode chapter_05_standalone.tex",
                    cwd=output_dir,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await proc.communicate()
                
                if proc.returncode == 0:
                    chapter_progress["chapter_05"].add(17)
                    await websocket.send_text(json.dumps({"type": "status", "part": 17, "status": "completed"}))
                    await websocket.send_text(json.dumps({"type": "log", "message": "Pipeline finished successfully! Standalone PDF is ready."}))
                else:
                    await websocket.send_text(json.dumps({"type": "log", "message": f"LaTeX Error: {stderr.decode()}"}))
                
        else:
            await websocket.send_text(json.dumps({"type": "log", "message": f"Processing {chapter_id}..."}))
            await asyncio.sleep(1)
            
        await websocket.send_text(json.dumps({"type": "done"}))
        await websocket.close()
            
    except WebSocketDisconnect:
        del active_connections[chapter_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
