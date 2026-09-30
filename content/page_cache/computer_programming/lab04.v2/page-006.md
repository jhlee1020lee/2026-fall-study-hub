---
course: "computer_programming"
source_pdf: "Lab04.v2.pdf"
pdf_page: 6
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab04.v2.pdf"
generated_at: "2026-09-30T14:34:15Z"
---
Getter and Setter
● Public methods to access or modify private attributes
● Getters and setters are not the Java syntax, but a convention to
   implement encapsulation


      private int income;
      public int getIncome() {
         // Getter format : public type getXXX()
         return income;
      }
      public void setIncome(int income) {
         // Setter format : public void setXXX (type xxx)
         this.income = income;
      }


                                                                     6
