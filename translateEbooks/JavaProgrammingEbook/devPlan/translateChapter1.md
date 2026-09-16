> [!NOTE]
> Trạng thái: **ĐÃ HOÀN THÀNH**
> Toàn bộ nội dung của chương này đã được dịch, ghép nối, sửa lỗi và biên dịch thành công vào main.pdf.

# Kế hoạch tự động dịch Chương 1 (Introduction to Java Programming)

Dựa trên yêu cầu và phương pháp đã áp dụng, tôi sẽ tự động trích xuất văn bản từ `Chapter_01.pdf` và tiến hành dịch theo từng phần (chunk) để đảm bảo chất lượng, giữ nguyên cấu trúc, hình ảnh, code và công thức toán học. Đích đến cuối cùng là xuất ra sách LaTeX và biên dịch thành PDF tương tự như project `ML_new1_2026`.

Với Chương 1 (dài 135 trang), khối lượng văn bản khá lớn và chứa nhiều mã nguồn Java, hình ảnh minh họa cũng như bài tập. Việc chia nhỏ tài liệu một cách logic là rất cần thiết để quá trình dịch tự động hoạt động mượt mà.

## Phân chia tài liệu (Tree of Thought)
Văn bản PDF Chương 1 sẽ được chia thành các phần logic sau để đảm bảo chất lượng dịch thuật và không làm quá tải AI:

- **Phần 1**: Mở đầu chương & 1.1 Basic Computing Concepts 
- **Phần 2**: 1.2 And Now—Java (Phần đầu đến Escape Sequences)
- **Phần 3**: 1.2 And Now—Java (Phần còn lại về định danh, biến...)
- **Phần 4**: 1.3 Program Errors (Syntax Errors, Logic Errors/Bugs)
- **Phần 5**: 1.4 Procedural Decomposition (Phần đầu đến Flow of Control)
- **Phần 6**: 1.4 Procedural Decomposition (Phần còn lại, gọi hàm lồng nhau)
- **Phần 7**: 1.5 Case Study: DrawFigures & Chapter Summary
- **Phần 8**: Self-Check Problems 
- **Phần 9**: Exercises & Programming Projects

*(Việc phân tách sẽ tự động bắt theo các tiêu đề Section và trang thực tế khi trích xuất PDF)*

## Quy tắc Dịch thuật (Translation Rules)
1. **Ngôn ngữ**: Dịch sang tiếng Việt, bám sát nghĩa gốc, văn phong tự nhiên, phù hợp với sách giáo trình khoa học máy tính.
2. **Mã nguồn (Code)**: Giữ nguyên hoàn toàn code Java. Không dịch tên biến, tên hàm, hay các từ khóa của ngôn ngữ lập trình. 
3. **Từ khóa (Keywords)**: Các thuật ngữ chuyên ngành (như *Compiler*, *Interpreter*, *Bytecode*, *Object-oriented*, *Method*, *Identifier*...) cần được giữ nguyên tiếng Anh hoặc để tiếng Anh trong ngoặc ở lần xuất hiện đầu tiên (VD: *Trình biên dịch (Compiler)*).
4. **Hình ảnh (Images)**: Dùng công cụ (như `pymupdf` - fitz) để trích xuất hình ảnh từ PDF gốc và lưu vào thư mục `images/chapter_01/`. Đảm bảo các link hình ảnh trong file markdown trỏ đúng đường dẫn tương đối.
5. **Công thức toán học (Math)**: Giữ nguyên các định dạng công thức toán học (nếu có) dưới dạng chuẩn LaTeX (`$...$` hoặc `$$...$$`) để tương thích trơn tru với hệ thống build LaTeX sau này.

## Quy trình xuất bản (Publishing Pipeline)
1. **Trích xuất & Dịch**: Sử dụng tập lệnh Python (`scratch\extract_pdf.py`) dùng thư viện `pymupdf` (fitz) để trích xuất text (kèm đánh dấu trang) và ảnh (lưu vào `images/chapter_01/`) theo từng khoảng trang cụ thể. AI sẽ nhận text thô và dịch thủ công từng khối theo đúng văn bản gốc. Lưu kết quả ra file Markdown trong thư mục `chapters/` (VD: `chapter_01_part1.md`).
2. **Chuyển đổi sang LaTeX**: Sử dụng Pandoc (hoặc script Python custom) để chuyển file Markdown sang định dạng LaTeX `.tex`. Template LaTeX sẽ được cấu hình tương tự như `Ebooks_output\ML_new1_2026`, hỗ trợ tiếng Việt (dùng `xeCJK`, `babel-vietnamese`, font chữ Unicode), sử dụng package `minted` hoặc `listings` để render code Java đẹp mắt.
3. **Biên dịch PDF**: Biên dịch file LaTeX thành định dạng PDF bằng engine `xelatex`, cho ra thành phẩm sách giáo trình.
4. **Sao chép hình ảnh**: Tự động copy toàn bộ file hình ảnh từ `images/chapter_01/` vào thư mục tài nguyên của project LaTeX đích (`Ebooks_output/JavaProgramming/Figures`) để đảm bảo quá trình biên dịch không bị thiếu file.
5. **Bước 5: Chuyển đổi sang LaTeX và xuất bản PDF (Hoàn thành)**:
   - **Nhiệm vụ:** Gom các phần đã dịch lại và biên dịch ra PDF.
   - **Phương pháp:**
  - Viết kịch bản Python (`build_latex.py`) nối toàn bộ các phần `chapter_01_part1.md` đến `chapter_01_part9.md` thành một file duy nhất `chapter_01_all.md`.
     - Tự động lọc và loại bỏ các ảnh quá nhỏ (chẳng hạn < 10KB) là các icon hoặc watermark không cần thiết trong sách.
     - Tự động bọc các hình ảnh vào môi trường `\begin{center}` để ngăn lỗi tràn lề (overfull hbox) khi hiển thị cùng dòng với văn bản.
     - Sao chép toàn bộ ảnh (.png, .jpg) hợp lệ từ thư mục `images/chapter_01` vào thư mục đích `Ebooks_output/JavaProgramming/Figures`.
     - Dùng `pandoc --no-highlight` để sinh LaTeX thô, kết hợp template *Legrand Orange Book* và thêm định nghĩa vĩ lệnh `\pandocbounded` cũng như `\maxwidth`.
     - Sử dụng engine `xelatex` để biên dịch ra PDF hoàn chỉnh.
   - **Tiêu chí hoàn thành:** File `main.pdf` chứa toàn bộ 56 trang với nội dung, mã nguồn, công thức và hình ảnh được dàn trang thành công.

## User Review Required
> [!IMPORTANT]
> Quá trình dịch sẽ được tiến hành một cách tự động. Ở mỗi bước, tôi sẽ dùng thư viện trích xuất văn bản, xử lý nối dòng, lấy ảnh, sau đó gửi cho AI dịch và lưu thành file tổng hợp.
>
> Do Chương 1 có nhiều mã nguồn Java, AI sẽ được thiết lập nghiêm ngặt: **chỉ dịch văn bản giải thích, giữ nguyên toàn bộ mã nguồn và từ khóa**. Hình ảnh sẽ được trích xuất và chèn vào đúng vị trí.
>
> Nếu bạn đồng ý với kế hoạch chia nhỏ tài liệu, các quy tắc dịch thuật, và quy trình xuất ra bản in PDF như trên, hãy phản hồi để tôi tiến hành bước tiếp theo! Hoặc báo cho tôi nếu bạn muốn điều chỉnh.

## Verification Plan
- Quá trình dịch sẽ lần lượt xử lý qua 9 phần văn bản và lưu lại kết quả.
- Rà soát (verify) file Markdown kết quả để đảm bảo: định dạng code blocks Java không bị phá vỡ, đường dẫn hình ảnh (`![alt](images/...)`) hợp lệ, từ khóa chuyên ngành không bị dịch sai nghĩa.
- Thử nghiệm pipeline biên dịch: chạy `xelatex` cho một đoạn ngắn để chắc chắn tiếng Việt hiển thị tốt, code đẹp, hình ảnh không bị tràn lề trước khi áp dụng cho toàn bộ chương.
