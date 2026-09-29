---
course: "computer_programming"
source_pdf: "7.inheritance.2.pdf"
pdf_page: 15
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf"
generated_at: "2026-09-29T23:41:41Z"
---
toString() Example

 class Student {
    String fName;
    String lName;
    int id;
    Student(String fName, String lName, int id) {
        this.fName = fName;
        this.lName = lName;
        this.id = id;
    }
    @Override
    public String toString() {
        return String.format("%s %s (%d)", fName, lName, id);
    }
 }


                                     Jaemin Yoo (SNU)           15
