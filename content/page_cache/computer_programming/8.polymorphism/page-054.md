---
course: "computer_programming"
source_pdf: "8.polymorphism.pdf"
pdf_page: 54
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/8.polymorphism.pdf"
generated_at: "2026-10-07T01:00:37Z"
---
Generic Class: Example
 class Pair<T, S> {
    T first; S second;
    Pair(T a, S b) {
        this.first = a;
        this.second = b;
    }
    public String toString() {
        return "(" + first.toString() + ", " + second.toString() + ")";
    }
 }

 System.out.println(new Pair<Integer, String>(6, "Six"));     // (6, Six)
 System.out.println(new Pair<Boolean, String>(true, "True")); // (true, True)

                                 Jaemin Yoo (SNU)                               54
