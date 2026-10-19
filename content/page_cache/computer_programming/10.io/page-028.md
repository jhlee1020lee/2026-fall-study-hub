---
course: "computer_programming"
source_pdf: "10.io.pdf"
pdf_page: 28
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/10.io.pdf"
generated_at: "2026-10-19T23:44:09Z"
---
Scanner: Alternative to Read Files
• FileReader: reads characters from a file.
   • read() returns a UTF-16 code unit as int, or -1 at end of file.
   • read(char[]) reads a block of characters without parsing numbers.
• Scanner: reads and interprets text
   • next() reads a token. nextInt() converts a token to an integer.
   • nextLine() returns a String. Use hasNextLine() for line loops.
• Example: "123 45"
   • FileReader with read(): 49 ('1'), 50 ('2'), 51 ('3'), ...
   • Scanner with nextInt(): 123, then 45.


                                      Jaemin Yoo (SNU)                   28
