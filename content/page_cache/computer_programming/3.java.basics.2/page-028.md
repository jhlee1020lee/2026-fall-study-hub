---
course: "computer_programming"
source_pdf: "3.java.basics.2.pdf"
pdf_page: 28
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/3.java.basics.2.pdf"
generated_at: "2026-09-09T01:12:15Z"
---
Switch vs. If/Else
                                                Same logic!

 String string = "something";
 switch (string) {
                                                   String string = "something";
     case "x":
                                                   if (string.equals("x")) {
         System.out.println("x");
                                                       System.out.println("x");
         break;
                                                   } else if (string.equals("y")) {
     case "y":
                                                       System.out.println("y");
         System.out.println("y");
                                                   } else {
         break;
                                                       System.out.println("end");
     default:
                                                   }
         System.out.println("end");
 }

                                      Jaemin Yoo (SNU)                                28
