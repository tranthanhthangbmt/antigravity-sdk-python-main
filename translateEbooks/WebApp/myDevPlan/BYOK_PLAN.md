# Kiến trúc Bring Your Own Key (BYOK) cho Web App trên Cloud

Để ứng dụng sẵn sàng triển khai trên Cloud (AWS, GCP, Vercel) và chạy độc lập với môi trường Antigravity IDE cá nhân, tôi đã tích hợp tính năng BYOK. 

## Chi tiết triển khai

### 1. Frontend (React)
- Cập nhật `App.jsx` để hiển thị thêm thanh nhập liệu **API Key**.
- Sử dụng `localStorage` để tự động lưu Key trên máy người dùng, tiện lợi cho những lần dùng tiếp theo.
- Khóa (API Key) được truyền thẳng xuống Component `ChapterCard` thông qua hệ thống Props.
- Khi người dùng nhấn nút "Start Translation", WebSocket URL sẽ đính kèm Key qua Query Parameter: `?api_key=XYZ`.

### 2. Backend (FastAPI)
- Bổ sung tham số `api_key` vào hàm bắt luồng kết nối `websocket_endpoint`.
- Kiểm tra tính hợp lệ:
  - Nếu `api_key` bị trống, ngay lập tức đóng kết nối và trả thông báo yêu cầu người dùng phải nhập Key.
  - (Khi đấu nối thực tế với SDK) API Key sẽ được gán vào biến môi trường hệ thống của luồng đó (ví dụ: `os.environ['GEMINI_API_KEY'] = api_key`) để Agent biết cách định danh.

## Cảnh báo bảo mật
Vì phương thức truyền tải này qua Query String, để đảm bảo an toàn tuyệt đối, hệ thống Cloud Production **bắt buộc phải có SSL Certificate (HTTPS / WSS)**.
