---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 29
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Use of instanceof
• Overriding can be imitated by using the instanceof operator.
public class HumanResources {
  public static int getSalary(Employee e) {       System.out.println("Executive: " +
    if(e instanceof Executive) {                     HumanResources.getSalary(
      return 960;                                      new Executive()
    }                                                ) + ", Manager: " +
    else if(e instanceof Manager) {                  HumanResources.getSalary(
      return 250;                                      new Manager()
    }                                                )
    else {                                        );
      return 180;
    }
  }                                                // Executive: 960, Manager: 250
}

                                       Jaemin Yoo (SNU)                                29
