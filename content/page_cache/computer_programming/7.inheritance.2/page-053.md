---
course: "computer_programming"
source_pdf: "7.inheritance.2.pdf"
pdf_page: 53
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf"
generated_at: "2026-09-29T23:41:41Z"
---
Abstract Class Example
 Person goodStudent = new Student("Good", "Student", 25);
 Person busyMan = new BusinessMan("Busy", "Man", 34);

 goodStudent.printName();         // Good Student
 busyMan.printName();             // Busy Man

 goodStudent.ageOneYear();        // Student is now 26 years old.
 busyMan.ageOneYear();            // Man is now 35 years old.

 goodStudent.work();              // Study hard
 busyMan.work();                  // Meeting all day
 goodStudent.play();              // Drink hard
 busyMan.play();                  // Go to the movies

                                  Jaemin Yoo (SNU)                  53
