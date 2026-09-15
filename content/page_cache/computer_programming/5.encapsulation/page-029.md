---
course: "computer_programming"
source_pdf: "5.encapsulation.pdf"
pdf_page: 29
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/5.encapsulation.pdf"
generated_at: "2026-09-15T04:46:52Z"
---
Putting a Class in a Package
  package computer;         // package instrument;

  public class Keyboard {
     private int id;
     private String name;

      public Keyboard(int id, String name) {
          this.id = id;
          this.name = name;
      }

      ...
  }

                                   Jaemin Yoo (SNU)   29
