# Kế Hoạch Thực Thi: Tích hợp AI Dịch Thuật Thật (Real AI Translation)

Bạn đã sẵn sàng để hệ thống tiến hành dịch thật sự thay vì dùng dữ liệu giả (Mock data). Do cuốn sách dài đến 161 trang, để đảm bảo độ chính xác và tránh bị cắt ngang (timeout / limit output tokens), chúng ta sẽ giữ nguyên cơ chế chia nhỏ (Chunking) 16 phần như hiện tại. Mỗi phần dịch 10 trang.

## User Review Required

> [!WARNING]
> Việc dịch thật sự 161 trang sách có thể mất khá nhiều thời gian (khoảng 30 giây đến 1 phút cho mỗi 10 trang). Do đó, tổng thời gian có thể lên tới 10-15 phút nếu bạn chọn dịch toàn bộ 16 phần cùng lúc.
> API Key của bạn cần có đủ hạn mức (Quota) của Google AI Studio (miễn phí thường là 15 request/phút, hoàn toàn đủ cho tiến độ này).

## Proposed Changes

### Backend (FastAPI)

#### [MODIFY] [main.py](file:///D:/MY_CODE/Antigravity_SDK1/antigravity-sdk-python-main/translateEbooks/WebApp/backend/main.py)
- **Tích hợp `PyPDF2`**: Đọc file `Chapter_05.pdf` từ thư mục gốc.
- **Tích hợp `google.generativeai`**: Khởi tạo Gemini 1.5 Pro với `api_key` nhận được từ Frontend.
- **Xử lý Chunking**:
  - Với mỗi Phần (Part $i$), dùng `PyMuPDF` (`fitz`) trích xuất text và hình ảnh từ trang $(i-1)*10$ đến trang $i*10$.
  - Lưu các hình ảnh hợp lệ vào `Pictures/`.
  - Truyền chuỗi text kết hợp với danh sách hình ảnh (nếu có) vào Prompt của Gemini. Yêu cầu: "Dịch sang tiếng Việt, chèn `\includegraphics{Pictures/tên_ảnh}` nếu có ảnh, giữ nguyên code Java, trả về 100% LaTeX thuần túy".
  - Nối (Append) kết quả LaTeX trả về từ Gemini vào file `chapter_05.tex`.
- Vẫn giữ nguyên logic sinh PDF độc lập (Phần 17) bằng XeLaTeX.

## Verification Plan

### Manual Verification
- Bạn sẽ chọn lại Phần 1 (hoặc các phần nhỏ) trên giao diện Web, nhấn **Start Translation**.
- Kiểm tra Log Terminal trên Web để xem AI đang đọc text và dịch thực tế.
- Bấm **View PDF** sau khi hoàn tất để xem nội dung dịch thuật thật sự.
  - Hình ảnh (nếu có) có được dàn trang đúng không.
