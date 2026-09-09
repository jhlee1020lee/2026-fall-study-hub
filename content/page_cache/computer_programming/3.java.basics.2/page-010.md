---
course: "computer_programming"
source_pdf: "3.java.basics.2.pdf"
pdf_page: 10
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/3.java.basics.2.pdf"
generated_at: "2026-09-09T01:12:15Z"
---
Loop Through an Array
• You can loop through the array elements with the for loop.
   • Use the length property to specify how many times the loop should run.

 String[] cars = {"Volvo", "BMW", "Ford", "Mazda"};

 // Outputs all elements in the cars array:
 for (int i = 0; i < cars.length; i++) {
     // System.out.print doesn’t break output line
     System.out.println(cars[i]);
 }

                                  Jaemin Yoo (SNU)                            10
