---
course: "computer_programming"
source_pdf: "5.encapsulation.pdf"
pdf_page: 23
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/5.encapsulation.pdf"
generated_at: "2026-09-15T04:46:52Z"
---
Trace Accesses to Private Variables

  ChangableVar var1 = new ChangableVar();
  System.out.print("First Read: " + var1.getValue());
  System.out.println(", read History: " + var1.getReadHistory());
  for (int i = 0; i < 2; i++) {
     System.out.print("< Set " + (i + 1) + " > :");
     var1.setValue(52 + i);
  }
  System.out.print("Second Read: "+ var1.getValue());
  System.out.println(", read History: "+ var1.getReadHistory());

  First Read: 0, read History: 1
  < Set 1 > :This is change #1
  < Set 2 > :This is change #2
  Second Read: 53, read History: 2


                                      Jaemin Yoo (SNU)              23
