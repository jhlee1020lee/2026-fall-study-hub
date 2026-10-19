---
course: "computer_programming"
source_pdf: "10.io.pdf"
pdf_page: 12
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/10.io.pdf"
generated_at: "2026-10-19T23:44:09Z"
---
Questions on Streams
• Q1. Why does read() return int instead of char?
  • read() returns a byte value (0 - 255) or -1 for end of stream.
  • char is unsigned and cannot represent -1; check for -1 before casting.
• Q2. Why does Java require checking I/O exceptions?
  • File access can fail even when the code is correct, e.g., a missing file.
  • The caller can respond, for example by asking for another file.
  • Java requires an explicit choice: catch the failure or declare throws.
     • This helps prevent forgotten error handling.




                                       Jaemin Yoo (SNU)                         12
