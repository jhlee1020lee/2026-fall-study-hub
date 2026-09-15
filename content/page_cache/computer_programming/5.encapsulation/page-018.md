---
course: "computer_programming"
source_pdf: "5.encapsulation.pdf"
pdf_page: 18
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/5.encapsulation.pdf"
generated_at: "2026-09-15T04:46:52Z"
---
Getter and Setter
• Public methods to access or modify private attributes.
• Not Java syntax, but a convention to implement encapsulation.

  private int age;
  public int getAge() {
     // Getter format : public type getXXX()
     return age;
  }
  public void setAge(int age) {
     // Setter format : public void setXXX (type xxx)
     this.age = age;
  }

                                   Jaemin Yoo (SNU)               18
