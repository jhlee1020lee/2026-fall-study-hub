---
course: "computer_programming"
source_pdf: "Lab.6.Polymorphism.pdf"
pdf_page: 5
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab.6.Polymorphism.pdf"
generated_at: "2026-10-14T23:43:26Z"
---
 Recap: Overloading
P1: To handle the same task on different data types.
    • void move(int dx, int dy)
    • void move(float dx, float dy)
P2: To handle slightly different, but closely related behaviors.
    • static double abs_add(double a, double b)
    • static double abs_add(double[] arr)
P3: Supply additional information to the method.
    • int first = dna.indexof(“CGC”)
    • int second = dna.indexof(“CGC”, first + "CGC".length())
P4: Supply default values for the parameters
