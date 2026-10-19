---
course: "computer_programming"
source_pdf: "10.io.pdf"
pdf_page: 8
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/10.io.pdf"
generated_at: "2026-10-19T23:44:09Z"
---
InputStream Abstract Class
• InputStream is the abstract superclass of all input streams.
  • int read();
      • Reads one byte as an int, or returns -1 at end of stream.
  • int read(byte[] b);
      • Reads up to b.length bytes into b. Returns the count, or -1 at end of stream.
  • int read(byte[] b, int off, int len);
      • Reads up to len bytes into b at index off. Returns the count, or -1.
  • void close();
      • Closes the stream and releases its system resources.
  • ...


                                        Jaemin Yoo (SNU)                                8
