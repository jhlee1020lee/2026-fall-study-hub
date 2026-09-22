---
course: "computer_programming"
source_pdf: "6.inheritance.1.pdf"
pdf_page: 5
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf"
generated_at: "2026-09-22T23:40:42Z"
---
Code with Inheritance

  class Lecture {
     boolean hasTA = true;
     boolean hasExams = true;
     boolean hasAssignments = false;
  }
  class CSLecture extends Lecture {
     boolean isHard = true;
  }
  class CPLecture extends CSLecture {
     boolean hasAssignments = true;
     boolean isExciting = true;
  }


                                 Jaemin Yoo (SNU)   5
