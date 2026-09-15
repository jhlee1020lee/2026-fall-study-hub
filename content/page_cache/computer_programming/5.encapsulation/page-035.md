---
course: "computer_programming"
source_pdf: "5.encapsulation.pdf"
pdf_page: 35
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/5.encapsulation.pdf"
generated_at: "2026-09-15T04:46:52Z"
---
import package.classname;

import computer.Keyboard;

public class Mart {
   public static void main (String arg[]){
       System.out.println("Welcome to SNU Mart");
       Keyboard keyboardComputer = new Keyboard(15523,"H Gaming keyboard");
       System.out.println("<new product of computer keyboard company info>");
       keyboardComputer.printCompanyInfo();
   }
}



                                  Jaemin Yoo (SNU)                              35
