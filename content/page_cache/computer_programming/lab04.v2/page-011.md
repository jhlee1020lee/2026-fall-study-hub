---
course: "computer_programming"
source_pdf: "Lab04.v2.pdf"
pdf_page: 11
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab04.v2.pdf"
generated_at: "2026-09-30T14:34:15Z"
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



                                                                                    11
