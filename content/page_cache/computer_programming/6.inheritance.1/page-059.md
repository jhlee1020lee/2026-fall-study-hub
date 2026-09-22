---
course: "computer_programming"
source_pdf: "6.inheritance.1.pdf"
pdf_page: 59
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/6.inheritance.1.pdf"
generated_at: "2026-09-22T23:40:42Z"
---
Default vs. Protected

  package ComplexAlgebra;

  public class C {
    protected double real;
    double imag;
    public C(double real, double imag) { this.real = real; this.imag = imag; }

      protected C add(C op2) { return new C(real + op2.real, imag + op2.imag); }
      protected C multiply(C op2) { ... }
      double angle() { return Math.atan2(imag, real); }
      double radius() { return Math.sqrt(imag * imag + real * real); }
      @Override
      public String toString() { return String.format("(%.1f)+(%.1f)j", real, imag); }
  }


                                        Jaemin Yoo (SNU)                                 59
