---
course: "computer_programming"
source_pdf: "5.encapsulation.pdf"
pdf_page: 21
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/5.encapsulation.pdf"
generated_at: "2026-09-15T04:46:52Z"
---
Access Validation with Getter/Setter

 class Person {
    private String name;
    public void setName(String name) {
        if (name == null || name.equals("")) {
            System.out.println("Name cannot be null or empty");
        } else {
            this.name = name;
        }
    }
 }

                            Jaemin Yoo (SNU)                      21
