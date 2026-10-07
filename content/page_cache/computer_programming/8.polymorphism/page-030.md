---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 30
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Use of getClass()
• getClass() can be also used to mimic overriding.

public class HumanResources {
  public static int getSalary(Employee e) {       System.out.println("Executive: " +
    switch(e.getClass().getName()) {                 HumanResources.getSalary(
      case "personnelpkg.Executive" :                  new Executive()
        return 960;                                  ) + ", Manager: " +
      case "personnelpkg.Manager" :                  HumanResources.getSalary(
        return 250;                                    new Manager()
      default :                                      )
        return 180;                               );
    }
  }                                                // Executive: 960, Manager: 250
}

                                       Jaemin Yoo (SNU)                                30
