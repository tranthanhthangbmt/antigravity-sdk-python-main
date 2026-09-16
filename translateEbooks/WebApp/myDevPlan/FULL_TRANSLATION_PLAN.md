# Kế Hoạch Thực Thi: Dịch Toàn Bộ Chương 5 & Xuất PDF Độc Lập

## 1. Cơ Chế Phân Mảnh (Dynamic Chunking)
Hệ thống sẽ chia 161 trang thành 16 phần (mỗi phần 10 trang). 
Phần cuối cùng (Part 17) sẽ đảm nhiệm tác vụ Biên dịch LaTeX.
Giao diện Web App sẽ sinh ra 17 phần chi tiết trên thanh tiến độ để theo dõi.

## 2. Thực Thi Dịch & Streaming
Trong WebSocket (`/ws/translate/chapter_05`), hệ thống sẽ sử dụng vòng lặp duyệt qua 16 phần để gọi quá trình dịch. Trạng thái Extracting, Translating, và Completed của từng phần sẽ được stream trực tiếp xuống giao diện React bằng giao thức WSS.

## 3. Xuất File PDF Độc Lập (Standalone PDF)
Tạo ra `chapter_05_standalone.tex` (bằng cách copy `main.tex` và chỉ giữ lại `chapter_05` trong `\includeonly`).
Chạy ngầm lệnh `xelatex chapter_05_standalone.tex` bên trong tiến trình của Backend, sau đó gửi thông báo hoàn tất về Frontend để người dùng bấm nút tải PDF độc lập.

## 4. Tính Năng Selective Translation (Chọn phần để dịch)
- **Frontend**: Thay vì hiển thị loading bar cố định, UI sẽ biến thành bảng danh sách các Checkbox. Người dùng có thể tick chọn phần muốn dịch. Phần nào đã hoàn thành sẽ chuyển sang màu xanh lá cây đậm (✓).
- **Backend State**: Khởi tạo biến `chapter_progress = {}` lưu trạng thái những phần đã được dịch xong vào RAM. 
- **WebSocket Logic**: URL nhận tham số `&parts=1,2,17` để quyết định chỉ nhảy vào vòng lặp của các phần được đánh dấu. Giúp tối ưu Token API trong quá trình kiểm thử phần mềm.
