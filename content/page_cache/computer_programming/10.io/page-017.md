---
course: "computer_programming"
source_pdf: "10.io.pdf"
pdf_page: 17
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/10.io.pdf"
generated_at: "2026-10-19T23:44:09Z"
---
FileOutputStream Example

static void writeFile() {
    try {
        // No internal buffer exists for FileOutputStream
        FileOutputStream fileOutputStream = new FileOutputStream("file.txt");
        fileOutputStream.write(65);
        fileOutputStream.flush();      // Does nothing
        fileOutputStream.close();
    } catch (IOException e) {
          e.printStackTrace();
    }
}



                                      Jaemin Yoo (SNU)                          17
