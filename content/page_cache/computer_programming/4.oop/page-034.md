---
course: "computer_programming"
source_pdf: "4.oop.pdf"
pdf_page: 34
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/4.oop.pdf"
generated_at: "2026-09-09T01:12:27Z"
---
How == Works for Objects
• == compares the addresses (not the contents) of the two objects.
  • You should keep in mind how the memory looks like.




  String str1 = new String("hey");                       Memory
  String str2 = new String("hey");
                                                          “hey”
  String str3 = str1;
  System.out.println(str1 == str2);
                                                          “hey”
  System.out.println(str1 == str3);


                                Jaemin Yoo (SNU)                  34
