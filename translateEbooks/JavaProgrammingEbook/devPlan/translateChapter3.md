> [!NOTE]
> Trạng thái: **ĐÃ HOÀN THÀNH**
> Toàn bộ nội dung của chương này đã được dịch, ghép nối, sửa lỗi và biên dịch thành công vào main.pdf.

# Kế hoạch tự động dịch Chương 3 (Chủ đề Chương 3)

Dựa trên yêu cầu và phương pháp đã áp dụng, tôi sẽ tự động trích xuất văn bản từ `Chapter_03.pdf` và tiến hành dịch theo từng phần (chunk) để đảm bảo chất lượng, giữ nguyên cấu trúc, hình ảnh, code và công thức toán học. Đích đến cuối cùng là xuất ra sách LaTeX và biên dịch thành PDF tương tự như project `ML_new1_2026`.

Với Chương 3, khối lượng văn bản khá lớn và chứa nhiều mã nguồn Java, hình ảnh minh họa cũng như bài tập. Việc chia nhỏ tài liệu một cách logic là rất cần thiết để quá trình dịch tự động hoạt động mượt mà.

## Phân chia tài liệu (Tree of Thought)
Văn bản PDF Chương 3 sẽ được tự động phân chia thành các phần logic dựa trên độ dài và cấu trúc tiêu đề trong quá trình trích xuất để đảm bảo không làm quá tải AI:

- **Phần 1**: 3.1 Parameters
- **Phần 2**: 3.2 Methods That Return Values
- **Phần 3**: 3.3 Using Objects
- **Phần 4**: 3.4 Case Study: Projectile Trajectory
- **Phần 5**: Self-Check Problems
- **Phần 6**: Exercises & Programming Projects

*(Việc phân tách sẽ tự động bắt theo các tiêu đề Section và số trang thực tế khi chạy script `extract_pdf.py`)*

## Quy tắc Dịch thuật (Translation Rules)
1. **Ngôn ngữ**: Dịch sang tiếng Việt, bám sát nghĩa gốc, văn phong tự nhiên, phù hợp với sách giáo trình khoa học máy tính.
2. **Mã nguồn (Code)**: Giữ nguyên hoàn toàn code Java. Không dịch tên biến, tên hàm, hay các từ khóa của ngôn ngữ lập trình. 
3. **Từ khóa (Keywords)**: Các thuật ngữ chuyên ngành cần được giữ nguyên tiếng Anh hoặc để tiếng Anh trong ngoặc ở lần xuất hiện đầu tiên.
4. **Hình ảnh (Images)**: Dùng công cụ `pymupdf` để trích xuất hình ảnh từ PDF gốc và lưu vào thư mục `images/chapter_03/`. Đảm bảo các link hình ảnh trong file markdown trỏ đúng đường dẫn.
5. **Công thức toán học (Math)**: Giữ nguyên các định dạng công thức toán học (`$...$` hoặc `$$...$$`).

## Quy trình xuất bản (Publishing Pipeline)
1. **Trích xuất & Dịch**: Sử dụng tập lệnh Python trích xuất text và ảnh theo từng khoảng trang cụ thể. AI sẽ dịch thô và lưu kết quả ra file Markdown `chapters/chapter_03_partY.md`.
2. **Tiền xử lý (Preprocessing)**: Chạy `build_latex.py` để:
   - Gom các phần markdown lại thành `chapter_03_all.md`.
   - Lọc bỏ ảnh rác `< 10KB`.
   - Bọc các hình ảnh vào môi trường `\begin{center}` ... `\end{center}` để chống tràn lề.
   - Chép ảnh hợp lệ vào `Ebooks_output/JavaProgramming/Figures`.
3. **Chuyển đổi LaTeX & Biên dịch**: 
   - Dùng Pandoc sinh `chapter_03.tex`.
   - Tự động include vào `main.tex`.
   - Biên dịch bằng `xelatex` ra thành phẩm PDF.

## User Review Required
> [!IMPORTANT]
> Quá trình dịch sẽ được tiến hành tự động. Ở mỗi bước, hệ thống sẽ trích xuất, chia part, dịch và tạo file tổng hợp.
> Nếu bạn đồng ý với kế hoạch của Chương 3, tôi sẽ kích hoạt pipeline để máy chạy ngay lập tức.

## Verification Plan
- Rà soát file Markdown kết quả để đảm bảo định dạng code blocks Java không bị phá vỡ, đường dẫn hình ảnh hợp lệ.
- Thử nghiệm pipeline biên dịch LaTeX cho chương này để chắc chắn tiếng Việt hiển thị tốt và hình ảnh căn lề chuẩn xác.
