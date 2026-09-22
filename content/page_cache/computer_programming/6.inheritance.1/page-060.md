---
course: "computer_programming"
source_pdf: "6.inheritance.1.pdf"
pdf_page: 60
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf"
generated_at: "2026-09-22T23:40:42Z"
---
Default vs. Protected
 package RealAlgebra;
 import ComplexAlgebra.C;

 public class R extends C {
    public R(double value) { super(value, 0); }

     @Override
     public String toString() {
         return "(" + Double.toString(real) + ")";
     }

     // Supports add() and multiply(), but not angle() and radius()
 }

                                   Jaemin Yoo (SNU)                   60
