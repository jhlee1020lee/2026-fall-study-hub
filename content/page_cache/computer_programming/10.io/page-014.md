---
course: "computer_programming"
source_pdf: "10.io.pdf"
pdf_page: 14
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/10.io.pdf"
generated_at: "2026-10-19T23:44:09Z"
---
OutputStream Abstract Class
• OutputStream is the abstract superclass of all output streams.
  • void write(int i);
     • Writes one byte using the lowest 8 bits of i.
  • void write(byte buf[], int index, int size);
     • Writes size bytes from buf, starting at index.
  • void flush();
     • Sends any buffered bytes to the destination.
  • void close();
     • Closes the stream and releases its system resources.




                                        Jaemin Yoo (SNU)           14
