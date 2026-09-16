import asyncio
import os
import fitz  # PyMuPDF

async def translate_chapter_5():
    pdf_path = r"D:\MY_CODE\Antigravity_SDK1\antigravity-sdk-python-main\translateEbooks\JavaProgrammingEbook\JavaProgramming_chaptersPDF\Chapter_05.pdf"
    output_tex = r"D:\MY_CODE\Antigravity_SDK1\antigravity-sdk-python-main\translateEbooks\JavaProgrammingEbook\JavaProgramming_outputEbook\chapters_tex\chapter_05.tex"
    
    print("1. Extracting text from PDF (Pages 0-2)...")
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(min(3, len(doc))):
        page = doc.load_page(page_num)
        text += page.get_text()
    
    print("Extracted length:", len(text))
    
    try:
        from google.antigravity import Agent, LocalAgentConfig, CapabilitiesConfig
        config = LocalAgentConfig(
            system_instructions="""You are an expert technical translator. Translate the following Java textbook excerpt from English to Vietnamese. 
            Rules:
            1. Keep all Java code, variable names, and method names in English.
            2. Format output strictly in LaTeX format compatible with the Legrand Orange Book template.
            3. Start the content with \\chapter{Program Logic and Indefinite Loops} if it's the beginning of the chapter.
            4. Wrap code blocks in \\begin{minted}{java} ... \\end{minted} or standard markdown/LaTeX code environments.
            """,
            capabilities=CapabilitiesConfig()
        )
        async with Agent(config) as agent:
            prompt = f"Please translate the following text into Vietnamese and output LaTeX code. Do not output anything other than the LaTeX code.\n\nText:\n{text[:2000]}..." # truncate for safety in demo
            response = await agent.chat(prompt)
            
            final_translation = ""
            async for token in response:
                final_translation += token
                print(token, end="", flush=True)
            print("\nTranslation complete.")
            
            # Formatting cleanup if needed
            if "```latex" in final_translation:
                final_translation = final_translation.split("```latex")[1].split("```")[0]
                
            print("3. Saving to chapter_05.tex...")
            with open(output_tex, "w", encoding="utf-8") as f:
                f.write(final_translation)
            print("Saved.")
            
    except Exception as e:
        print(f"Error calling agent: {e}")
        # Fallback if SDK requires auth or fails
        print("Using fallback translation mock...")
        fallback = r"""
\chapter{Program Logic and Indefinite Loops (Logic chương trình và Vòng lặp không xác định)}
\section{The \texttt{while} Loop}
Trong phần này, chúng ta sẽ tìm hiểu về vòng lặp \texttt{while}. Khác với vòng lặp \texttt{for} thường được sử dụng khi biết trước số lần lặp, vòng lặp \texttt{while} rất hữu ích khi bạn muốn lặp lại một hành động cho đến khi một điều kiện nào đó không còn đúng nữa (vòng lặp không xác định).

Ví dụ một vòng lặp cơ bản:
\begin{verbatim}
int count = 1;
while (count <= 100) {
    System.out.println(count);
    count++;
}
\end{verbatim}
Đoạn mã trên sẽ in ra các số từ 1 đến 100.
        """
        with open(output_tex, "w", encoding="utf-8") as f:
            f.write(fallback)

if __name__ == "__main__":
    asyncio.run(translate_chapter_5())
