---
course: "computer_programming"
source_pdf: "10.io.pdf"
pdf_page: 11
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/10.io.pdf"
generated_at: "2026-10-19T23:44:09Z"
---
FileInputStream Example
// Exception handling is necessary for FileInputStream.
// - Unhandled Exceptions: java.io.FileNotFoundException
// - Unhandled Exceptions: java.io.IOException
static void readFile() {
    try {
        FileInputStream inputStream = new FileInputStream ("say_hello.txt");
        int c = inputStream.read();
        System.out.print((char) c);
        inputStream.close();
    } catch (Exception e) {
        e.printStackTrace();
    }
}

                                   Jaemin Yoo (SNU)                            11
