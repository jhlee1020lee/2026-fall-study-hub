---
course: "computer_programming"
source_pdf: "Lab04.v4.pdf"
pdf_page: 13
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab04.v4.pdf"
generated_at: "2026-10-01T16:19:03Z"
---
Packages

   package instrument;
                                                                 Class Definition
   public class Keyboard {
      private int id;
      private String name;

       public Keyboard(int id, String name) {
           this.id = id;
           this.name = name;
       }

       public void printCompanyInfo() {
           if (this.id % 10 == 1) {
               System.out.println(name + ": Samick's device");
           } else if (this.id % 10 == 2) {
               System.out.println(name + ": Yamaha's device");
           } else {
               System.out.println(name + ": Gipson's device");
           }
       }
   }



                                                                                    13
