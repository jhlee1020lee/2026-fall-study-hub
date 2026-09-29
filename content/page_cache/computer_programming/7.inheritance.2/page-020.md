---
course: "computer_programming"
source_pdf: "7.inheritance.2.pdf"
pdf_page: 20
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf"
generated_at: "2026-09-29T23:41:41Z"
---
equals() Example

 public boolean equals(Object o) {
    // Two instances are same
    if (this == o) return true;

      // Compare three fields of this and o
      if (o instanceof Shoes) {
        Shoes shoes = (Shoes) o;
        return this.company.equals(shoes.company)
                && this.model.equals(shoes.model)
                && this.size == shoes.size; }

      // o is not even a Shoes class instance
      return false;
  }


                                      Jaemin Yoo (SNU)   20
