---
course: "computer_programming"
source_pdf: "2.java.basics.1.pdf"
pdf_page: 36
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf"
generated_at: "2026-09-01T06:30:14Z"
---
Widening Casting
• Variable with a smaller scope can be automatically converted into
  a variable with a larger scope.


  byte testByte = 0b1;
  short testShort = testByte;
  int testInt = testShort;
  long testLong = testInt;
  float testFloat = testLong;
  double testDouble = testFloat;

                             Jaemin Yoo (SNU)                     36
