# Kế hoạch tự động dịch các Chương còn lại (Java Programming)

Dựa trên thành công của quá trình dịch Chương 1, kế hoạch này nhằm tự động hóa và đồng bộ hóa quy trình trích xuất, dịch thuật, và xuất bản cho toàn bộ các chương còn lại của cuốn sách **Building Java Programs** (từ `Chapter_0_Intro` đến `Chapter_19`, cùng với `Chapter_other.pdf`).

## Danh sách các chương cần dịch
Dựa vào thư mục `EBooks_input\JavaProgramming\`, chúng ta có 20 file PDF còn lại:
- `Chapter_0_Intro.pdf`
- `Chapter_02.pdf` đến `Chapter_19.pdf`
- `Chapter_other.pdf`

## Quy tắc Dịch thuật Đồng bộ (Translation Rules)
Các quy tắc này kế thừa nguyên vẹn từ cấu hình đã chứng minh tính hiệu quả ở Chương 1:
1. **Ngôn ngữ**: Dịch phần chữ (narrative text) sang tiếng Việt với văn phong chuẩn mực của giáo trình Khoa học máy tính.
2. **Mã nguồn (Code)**: Bất khả xâm phạm. Giữ nguyên toàn bộ code Java, bao gồm cả comment (nếu không được yêu cầu dịch rõ ràng), tên biến, tên hàm.
3. **Từ khóa chuyên ngành**: Các từ khóa (như *Loop*, *Array*, *Class*, *Object*, *Inheritance*...) cần được dịch kèm tiếng Anh trong ngoặc ở lần đầu, sau đó có thể giữ nguyên tiếng Anh để tránh gượng ép.
4. **Hình ảnh (Images)**: Dùng `pymupdf` để trích xuất ảnh và lưu vào `images/chapter_XX/`.
5. **Công thức toán học**: Giữ nguyên block LaTeX (`$...$` hoặc `$$...$$`) để Pandoc không làm hỏng cú pháp.

## Quy trình Tự động hóa Toàn diện (Automated Pipeline)

Quá trình làm việc với 20 chương sẽ cần một quy trình tự động hóa mạnh mẽ hơn thay vì làm thủ công từng file:

### Bước 1: Trích xuất Hàng loạt (Batch Extraction)
- Nâng cấp tập lệnh `extract_pdf.py` để duyệt qua toàn bộ thư mục `EBooks_input/JavaProgramming/`.
- Với mỗi `Chapter_XX.pdf`:
  - Trích xuất ảnh vào `images/chapter_XX/`.
  - Tách text theo cơ chế "Chunking" (khoảng 10-15 trang/chunk để AI không bị quá tải) và chia nhỏ ra thành các file thô tạm thời.

### Bước 2: Dịch thuật AI (Translation phase)
- Chạy prompt chuẩn hóa (đã dùng ở Chương 1) lên từng chunk của mỗi chương.
- Kết quả trả về sẽ được lưu dưới định dạng Markdown vào `chapters/chapter_XX_partY.md`.
- File markdown sử dụng đường dẫn ảnh tương đối `![alt](images/chapter_XX/img_...)`.

### Bước 3: Tiền xử lý Markdown & Hình ảnh (Preprocessing)
Tương tự script `build_latex.py` hiện tại, hệ thống sẽ tự động vòng lặp qua từng chương:
1. Nối các phần `partY` thành `chapter_XX_all.md`.
2. **Bảo vệ Layout**:
   - Dò quét và tự động lọc loại bỏ các file ảnh có dung lượng `< 10KB` (watermark, icon rác).
   - Tự động bọc mọi cú pháp ảnh vào môi trường `\begin{center} ... \end{center}` bằng regex khi chuyển sang định dạng LaTeX (nhằm chấm dứt tình trạng *overfull hbox* gây lệch ảnh).
3. Copy toàn bộ ảnh hợp lệ vào `Ebooks_output/JavaProgramming/Figures/`.

### Bước 4: Chuyển đổi LaTeX & Biên dịch (LaTeX Generation & Build)
- Dùng `pandoc --no-highlight` để convert từng `chapter_XX_all.md` thành `chapter_XX.tex` lưu trong `chapters_tex/`.
- Tự động đẩy vĩ lệnh `\pandocbounded` (chứa `\maxwidth`, `\maxheight`) vào đầu mỗi file `.tex` để ràng buộc kích cỡ ảnh tối đa không tràn trang.
- Tập lệnh sẽ tự động chèn các câu lệnh `\include{chapters_tex/chapter_XX}` vào file `main.tex`.
- Chạy `xelatex main.tex` (2 vòng để cập nhật Mục lục/Reference).

## Bảng Theo dõi Tiến độ Tổng thể (Progress Tracker)

Trạng thái: 
- `[x]` Đã hoàn thành 
- `[/]` Đang tiến hành
- `[ ]` Chưa bắt đầu

| Chương (Chapter) | Trích xuất (Extract) | Dịch thuật (Translate) | Sinh LaTeX (Build) | Trạng thái chung | Ghi chú |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Chapter_01 (Intro)** | `[x]` | `[x]` (9/9 parts) | `[x]` | Hoàn thành | Đã xác nhận chuẩn template |
| **Chapter_0_Intro** | `[ ]` | `[ ]` | `[ ]` | Pending | |
| **Chapter_02** | `[x]` | `[x]` | `[x]` | Hoàn thành | |
| **Chapter_03** | `[ ]` | `[ ]` | `[ ]` | Pending | |
| **Chapter_04** | `[ ]` | `[ ]` | `[ ]` | Pending | |
| **Chapter_05** | `[ ]` | `[ ]` | `[ ]` | Pending | |
| **Chapter_06** | `[ ]` | `[ ]` | `[ ]` | Pending | |
| **Chapter_07** | `[ ]` | `[ ]` | `[ ]` | Pending | |
| **Chapter_08** | `[ ]` | `[ ]` | `[ ]` | Pending | |
| **Chapter_09** | `[ ]` | `[ ]` | `[ ]` | Pending | |
| **Chapter_10** | `[ ]` | `[ ]` | `[ ]` | Pending | |
| **Chapter_11** | `[ ]` | `[ ]` | `[ ]` | Pending | |
| **Chapter_12** | `[ ]` | `[ ]` | `[ ]` | Pending | |
| **Chapter_13** | `[ ]` | `[ ]` | `[ ]` | Pending | |
| **Chapter_14** | `[ ]` | `[ ]` | `[ ]` | Pending | |
| **Chapter_15** | `[ ]` | `[ ]` | `[ ]` | Pending | |
| **Chapter_16** | `[ ]` | `[ ]` | `[ ]` | Pending | |
| **Chapter_17** | `[ ]` | `[ ]` | `[ ]` | Pending | |
| **Chapter_18** | `[ ]` | `[ ]` | `[ ]` | Pending | |
| **Chapter_19** | `[ ]` | `[ ]` | `[ ]` | Pending | |
| **Chapter_other** | `[ ]` | `[ ]` | `[ ]` | Pending | Appendices/Index |

---

## Kế hoạch chi tiết từng chương (Detailed Chapter Plans)

*Lưu ý: Số lượng các phần (parts) của mỗi chương sẽ được quyết định tự động trong Bước "Trích xuất" dựa trên độ dài (mỗi part khoảng 10-15 trang).*


## Bài học & Cập nhật Pipeline (Từ thực tế làm Chương 1-4)
Quá trình làm các chương đầu tiên đã giúp hoàn thiện pipeline để áp dụng cho các chương sau (chỉ cần chạy tự động):
1. **Trích xuất (extract_pdf.py)**: Đã sửa biến `start_page` thành `start_index` để trích xuất đúng trang theo offset.
2. **Sắp xếp file (build_latex.py)**: Đã sửa lỗi ghép sai thứ tự file (VD: part10 bị ghép sau part9 do sort string) bằng cách sort theo số học `part(\d+)_(\d+)`.
3. **Đánh số LaTeX (build_latex.py)**:
   - Đã chèn `\chapter{Tiêu đề}` vào đầu mỗi chương trong script để LaTeX reset bộ đếm phần (`section`), nhờ vậy đánh số chương sẽ chuẩn xác (VD: 4.1 thay vì 2.4.1).
   - Đã chèn regex để xóa các con số thủ công trong thẻ `\section{4.2 ...}` thành `\section{...}` để LaTeX tự đánh số chuẩn, tránh bị trùng lặp `2.4.8 4.2`.
4. **Lỗi `\maxwidth`**: LLM và Pandoc hay sinh ra cú pháp lỗi `\maxwidth{0.9\linewidth}` trong Markdown. Cú pháp này gây lỗi trình biên dịch LaTeX. Đã xử lý triệt để bằng regex replace trong pipeline.

*Khi tiến hành dịch Chương 5 trở đi, hãy tiếp tục sử dụng các script đã được cập nhật này! Các lỗi trên đã được khắc phục hoàn toàn trong các script hiện tại, chỉ cần gọi script và yên tâm chạy.*

### Kế hoạch tiếp theo: Chương 5
- **File gốc:** `Chapter_02.pdf`
- **Tình trạng:** `[/]` Đang tiến hành (Part 2/7)
- **Các bước chi tiết:**
  - `[x]` Chạy script trích xuất ảnh và text từ PDF.
  - `[x]` Phân tích mục lục (Tree of Thought) để chia thành các Part (đã xác định 7 Part).
  - `[x]` Dịch Part 1.
  - `[x]` Dịch Part 2 đợt 1 (trang 30-34).
  - `[x]` Dịch Part 2 đợt 2 (trang 35-40).
  - `[x]` Dịch Part 2 đợt 3 (trang 41-46).
  - `[x]` Dịch Part 2 đợt 4 (trang 47-52).
  - `[x]` Dịch Part 2 đợt 5 (trang 53-58).
  - `[x]` Dịch Part 2 đợt 6 (trang 59-64).
  - `[ ]` Dịch Part 3...
  - `[ ]` Chạy `build_latex.py` để gộp, bọc ảnh (`\begin{center}`), loại bỏ icon rác và sinh `chapter_02.tex`.
  - `[ ]` Cập nhật `main.tex` chèn `\include{chapters_tex/chapter_02}`.
  - `[ ]` Chạy `xelatex` kiểm tra lỗi tràn lề, lỗi font.
  - `[ ]` Hoàn tất và check mục Tiến độ Tổng thể ở trên.

*(Quá trình này sẽ lặp lại với Chapter 3, 4, 5... Mỗi khi AI chuyển sang một chương mới, hệ thống sẽ log tiến trình cụ thể vào bảng theo dõi).*

## Tiêu chí hoàn thành (Definition of Done)
- Toàn bộ nội dung chữ tiếng Anh được chuyển thể sang tiếng Việt tự nhiên.
- Code Java format hoàn hảo bằng template *Legrand Orange Book*.
- Không có hình ảnh nào bị tràn lề, cắt xén, lệch lề phải hay xuất hiện các icon/watermark rác.
- Sinh thành công file `main.pdf` hoàn chỉnh chứa > 1000 trang của toàn bộ cuốn sách.

> Kế hoạch này được lưu để đóng vai trò làm tài liệu hướng dẫn (blueprint) và **bảng điều khiển tiến độ** (dashboard) cho các phiên làm việc dịch thuật tiếp theo. Quản trị viên có thể mở file này ra bất cứ lúc nào để xem AI đang dịch tới đâu.
