---
course: "computer_programming"
source_pdf: "10.io.pdf"
pdf_page: 25
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/10.io.pdf"
generated_at: "2026-10-19T23:44:09Z"
---
FileWriter Example


public static void main(String[] args) {
  String[] lines = {
     "Hello\n",
     "Computer Programming\n",
     "Class!"
  };
  // make sure to have data directory beforehand
  writeLines("data/say_hello.txt", Arrays.asList(lines));
}



                                   Jaemin Yoo (SNU)         25
