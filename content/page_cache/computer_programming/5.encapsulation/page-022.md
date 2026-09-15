---
course: "computer_programming"
source_pdf: "5.encapsulation.pdf"
pdf_page: 22
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/5.encapsulation.pdf"
generated_at: "2026-09-15T04:46:52Z"
---
Trace Accesses to Private Variables
 class ChangableVar {
    private int valueToBeWatched ;
    private int countOfChange = 0;    // trace # of changes
    private int readHistory = 0;      // trace # of reads

     public void setValue(int newval) {
         valueToBeWatched = newval;
         countOfChange++;
         System.out.println("This is change #"+ countOfChange);
     }
     public int getValue() {
         readHistory++;
         return valueToBeWatched;
     }
 }

                                      Jaemin Yoo (SNU)            22
