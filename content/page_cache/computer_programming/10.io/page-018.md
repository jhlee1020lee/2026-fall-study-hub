---
course: "computer_programming"
source_pdf: "10.io.pdf"
pdf_page: 18
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/10.io.pdf"
generated_at: "2026-10-19T23:44:09Z"
---
BufferedOutputStream Class
• Buffers output bytes in memory before sending them onward.
  • Wraps another output stream, such as FileOutputStream.
  • Combines small writes into larger writes, reducing I/O overhead.
  • flush() sends pending bytes to its wrapped stream.
     • Does nothing for plain FileOutputStream and ByteArrayOutputStream.




                                    Jaemin Yoo (SNU)                        18
