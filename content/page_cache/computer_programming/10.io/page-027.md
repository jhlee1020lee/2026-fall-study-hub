---
course: "computer_programming"
source_pdf: "10.io.pdf"
pdf_page: 27
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/10.io.pdf"
generated_at: "2026-10-19T23:44:09Z"
---
FileReader Example

static void readFile() {
    File testFile = new File("data/say_hello.txt");
    try {
        FileReader testFileReader = new FileReader(testFile);
        int c = testFileReader.read();         // character
        while (c != -1) {
            System.out.print((char) c);
            c = testFileReader.read();         // when there is no data, returns -1
        }
    } catch (Exception e) {
        e.printStackTrace();
    }
}


                                       Jaemin Yoo (SNU)                               27
