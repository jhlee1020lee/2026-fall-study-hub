---
course: "computer_programming"
source_pdf: "5.encapsulation.pdf"
pdf_page: 43
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/5.encapsulation.pdf"
generated_at: "2026-09-15T04:46:52Z"
---
Inner Class: Example

 Calculator cal1 = new Calculator(3);
 Calculator cal2 = new Calculator(10);

 for(int i = 0; i < 4; i++) {
    System.out.println("< result of " + i + " and " + (i + 1) + " > ");
    System.out.println(cal1.specialOp(i, i + 1) + "\n");
 }

 System.out.println(cal2.specialOp(5, 6));



                              Jaemin Yoo (SNU)                        43
