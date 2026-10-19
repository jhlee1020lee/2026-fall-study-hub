---
course: "computer_programming"
source_pdf: "10.io.pdf"
pdf_page: 19
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/10.io.pdf"
generated_at: "2026-10-19T23:44:09Z"
---
BufferedOutputStream Example
static void writeFile() {
    try {
        FileOutputStream fileOutputStream = new FileOutputStream("file.txt");
        BufferedOutputStream bufferedOutputStream =
            new BufferedOutputStream(fileOutputStream);

        String s = "Welcome to Computer Programming";
        bufferedOutputStream.write(s.getBytes());
        bufferedOutputStream.flush();
        bufferedOutputStream.close();
        fileOutputStream.close();
    } catch (IOException e) {
         e.printStackTrace();
    }
}

                                      Jaemin Yoo (SNU)                          19
