---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 25
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Overriding
• To redefine an inherited instance method of a subclass to change
  or extend the behavior of the parent’s corresponding method.

                          Employee
                                                     The same method
        Inherit           getSalary()
                                                    name “getSalary()”
          or
                                                    could have different
       Override
                                                     behaviors. This is
                                                     why overriding is
                   Manager                …            polymorphic.
                   getSalary()    getSalary()

                                 Jaemin Yoo (SNU)                          25
