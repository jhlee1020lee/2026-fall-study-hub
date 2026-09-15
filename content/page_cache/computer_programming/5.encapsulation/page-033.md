---
course: "computer_programming"
source_pdf: "5.encapsulation.pdf"
pdf_page: 33
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/5.encapsulation.pdf"
generated_at: "2026-09-15T04:46:52Z"
---
Using a Class in a Default Package
• main() Method in the Mart class under the default package.

  System.out.println("Welcome to SNU Mart\n");

  computer.Keyboard keyboardComputer =
          new computer.Keyboard(15523,"H Gaming keyboard");
  instrument.Keyboard keyboardMusic =
          new instrument.Keyboard(131511, "Black and white keyboard");

  System.out.println("<new product of computer keyboard company info>");
  keyboardComputer.printCompanyInfo();
  System.out.println("<new product of instrument keyboard company info>");
  keyboardMusic.printCompanyInfo();

                                  Jaemin Yoo (SNU)                           33
