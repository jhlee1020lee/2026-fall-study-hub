---
course: "computer_programming"
source_pdf: "3.java.basics.2.pdf"
pdf_page: 52
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/3.java.basics.2.pdf"
generated_at: "2026-09-09T01:12:15Z"
---
Function Calls
• Simply write the function name and () to run a function.
   • Along with parameters (if needed).

  class Main {
     static float interpolate(float x1, float x2, float r1, float r2) {
         return (r2 * x1 + r1 * x2) / (r1 + r2);
     }

      public static void main(String[] args) {
          float intrp = interpolate(0f, 3f, 1.5f, 2.5f);
          System.out.println(intrp); // 1.125
      }
  }

                                    Jaemin Yoo (SNU)                      52
