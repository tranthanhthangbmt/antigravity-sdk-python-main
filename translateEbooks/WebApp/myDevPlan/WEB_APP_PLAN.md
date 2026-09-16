# Kế Hoạch Phát Triển Web App: Tự Động Hóa Dịch Sách Với Antigravity SDK

## 1. Tổng Quan Kiến Trúc (Architecture Overview)

Dự án này là một Web Application quản lý quá trình dịch tự động giáo trình (PDF sang Tiếng Việt/LaTeX) bằng AI (Antigravity SDK). Hệ thống tuân theo mô hình Client-Server với giao tiếp thời gian thực.

- **Backend**: Python + FastAPI
  - Xử lý logic đọc file kế hoạch (`translateChapterX.md`) và file PDF gốc.
  - Sử dụng Antigravity SDK (`google.antigravity.Agent`) để gọi AI dịch thuật, xử lý ảnh và code.
  - Cung cấp REST APIs và WebSockets.
- **Frontend**: React + Vite
  - Giao diện người dùng đồ họa hiện đại (Dashboard).
  - Kết nối WebSocket để cập nhật tiến trình chi tiết của từng Agent đang chạy ở Backend.

---

## 2. Thiết Kế Giao Diện Trạng Thái & Tiến Độ (Progress & Status Design)

Dựa trên cấu trúc file `translateChapterX.md`, một chương sách PDF được chia thành nhiều phần (chunks/parts) và đi qua nhiều pipeline xuất bản. Giao diện Web (Frontend) sẽ phản ánh chi tiết toàn bộ chu trình này.

### Cấu trúc dữ liệu hiển thị (UI State)
Mỗi thẻ (Chapter Card) trên UI không chỉ hiển thị một thanh Progress chung, mà khi mở rộng (Expand), sẽ hiển thị cấu trúc cây (Tree of Thought) bao gồm:

1. **Giai đoạn 1: Trích xuất & Dịch thuật (Extraction & Translation)**
   - Phân giải kế hoạch (Parsing `translateChapterX.md`).
   - Danh sách các phần nhỏ (Ví dụ: *Phần 1: Mở đầu chương & 1.1 Basic Computing Concepts*, *Phần 2: 1.2 And Now—Java*, v.v.).
   - Trạng thái từng phần (Pending -> Extracting -> Translating -> Reviewing -> Done).
   - *Hiển thị chi tiết (Live Log)*: Có một cửa sổ Terminal ảo nhỏ bên cạnh hiển thị suy nghĩ (thoughts) của Agent khi đang xử lý phần đó (ví dụ: đang giữ nguyên block code Java nào, đang lưu ảnh vào đâu).

2. **Giai đoạn 2: Xử lý Hình Ảnh (Image Processing) [Đã triển khai]**
   - Trích xuất ảnh bằng `PyMuPDF` (`fitz`).
   - Tự động bỏ qua các ảnh nhiễu kích thước siêu nhỏ.
   - Sao chép ảnh hợp lệ vào thư mục đích (`Ebooks_output/JavaProgramming/Figures`).
   - Nhúng siêu dữ liệu về ảnh (tên ảnh) vào Prompt để Gemini 1.5 tự động đặt `\includegraphics` vào đúng ngữ cảnh.

3. **Giai đoạn 3: Biên dịch LaTeX (LaTeX Compilation)**
   - Chạy kịch bản ghép các phần Markdown (`chapter_01_all.md`).
   - Chuyển đổi qua Pandoc (`pandoc --no-highlight`).
   - Chạy engine `xelatex` sinh file PDF cuối cùng.
   - Bắt và hiển thị lỗi LaTeX (nếu Overfull hbox hoặc lỗi cú pháp) về Web.

### Công nghệ trực quan
- **Màu sắc / Nhãn (Badges)**: 
  - 🔵 `Đang phân tích` (Analyzing)
  - 🟡 `Đang dịch` (Translating: Part X/Y)
  - 🟣 `Đang biên dịch PDF` (Compiling LaTeX)
  - 🟢 `Hoàn thành` (Completed)
  - 🔴 `Lỗi` (Error - kèm nút Retry cho phần bị lỗi).
- Giao diện có thể dùng thư viện như `framer-motion` (nếu dùng React) để tạo animation mượt mà khi các dòng trạng thái được cập nhật qua WebSocket.

---

## 3. Cấu Trúc Thư Mục Phát Triển (Directory Structure)

```text
D:\MY_CODE\Antigravity_SDK1\antigravity-sdk-python-main\translateEbooks\WebApp\
├── myDevPlan\
│   └── WEB_APP_PLAN.md               # File tài liệu quản lý kiến trúc này
├── backend\                          # FastAPI Server
│   ├── main.py                       # Điểm vào của server, khai báo API & WebSocket
│   ├── agent_runner.py               # Logic gọi Antigravity SDK
│   ├── chapter_parser.py             # Script parse translateChapterX.md để lấy tiến độ
│   ├── requirements.txt
│   └── ...
└── frontend\                         # React/Vite App
    ├── package.json
    ├── src\
    │   ├── App.jsx                   # Layout chính
    │   ├── components\
    │   │   ├── ChapterList.jsx       # Danh sách các chương
    │   │   ├── ChapterCard.jsx       # Thẻ chi tiết tiến trình của 1 chương
    │   │   ├── DetailedProgress.jsx  # Hiển thị list các Phần (Parts) đang dịch
    │   │   └── TerminalLog.jsx       # Cửa sổ đen hiện log realtime từ SDK
    │   └── index.css                 # Style hiện đại, màu sắc, glassmorphism
```

---

## 4. Các Bước Thực Hiện (Execution Workflow)

1. **Khởi tạo dự án**: 
   - Dùng `npx create-vite` tạo Frontend React.
   - Cài đặt FastAPI và `google.antigravity` cho Backend.
2. **Xây dựng API cơ bản & Trình Phân Tích (Parser)**: 
   - Viết hàm Python đọc file `translateChapterX.md` (từ `devPlan/`) để nhận diện được có bao nhiêu "Phần" cần dịch.
3. **Phát triển luồng WebSocket**: 
   - Mở kênh giao tiếp hai chiều. Gửi toàn bộ cấu trúc các "Phần" từ Backend xuống Frontend để vẽ UI.
4. **Xây dựng Frontend UI**: 
   - Thiết kế các Component với CSS đẹp mắt.
5. **Tích hợp SDK Antigravity**: 
   - Gắn `Agent` vào luồng, khi chạy tới "Phần" nào thì gửi JSON báo cáo trạng thái `{"chapter": 1, "part": 2, "status": "translating"}` qua Socket.
6. **Kiểm thử (Verification)**: 
   - Chạy thử nghiệm với `translateChapter1.md` và kiểm tra UI cập nhật mượt mà.
