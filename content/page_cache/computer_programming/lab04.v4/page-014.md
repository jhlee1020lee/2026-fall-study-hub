---
course: "computer_programming"
source_pdf: "Lab04.v4.pdf"
pdf_page: 14
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab04.v4.pdf"
generated_at: "2026-10-01T16:19:03Z"
---
Packages
● Using classes in different packages
  ● The main method in the Mart class under the default package

 System.out.println("Welcome to SNU Mart\n");

 computer.Keyboard keyboardComputer =
         new computer.Keyboard(15523,"H Gaming keyboard");
 instrument.Keyboard keyboardMusic =
         new instrument.Keyboard(131511, "Black and white keyboard");

 System.out.println("<new product of computer keyboard company info>");
 keyboardComputer.printCompanyInfo();

 System.out.println("<new product of instrument keyboard company info>");
 keyboardMusic.printCompanyInfo();


                                                                            14
