---
course: "computer_programming"
source_pdf: "10.io.pdf"
pdf_page: 29
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/10.io.pdf"
generated_at: "2026-10-19T23:44:09Z"
---
Scanner Example

static void readFile() {
    File testFile = new File("data/say_hello.txt");
    try {
        Scanner input = new Scanner(testFile);
        while (input.hasNext()) {
            System.out.println(input.nextLine());
        }
    } catch (Exception e) {
        e.printStackTrace();
    }
}

                               Jaemin Yoo (SNU)       29
