---
course: "computer_programming"
source_pdf: "2.java.basics.1.pdf"
pdf_page: 47
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf"
generated_at: "2026-09-01T06:30:14Z"
---
String Literal vs. String Object


                                                 "Apple”
    String appleOne = "Apple";
                                                 String Pool
    String appleTwo = "Apple";

                                                "Apple”        "Apple”
                                                                 Heap Memory


    String appleObjOne = new String("Apple");
    String appleObjTwo = new String("Apple");

                             Jaemin Yoo (SNU)                                  47
