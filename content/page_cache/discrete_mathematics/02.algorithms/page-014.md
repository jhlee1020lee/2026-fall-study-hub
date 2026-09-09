---
course: "discrete_mathematics"
source_pdf: "02.Algorithms.pdf"
pdf_page: 14
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf"
generated_at: "2026-09-09T01:12:41Z"
---
Bubble Sort
• Bubble sort makes multiple passes through a list. Every pair of elements that are found
  to be out of order are interchanged.

           procedure bubblesort (a1,…,an: real numbers with n ≥ 2)
              for (i := 1 to n− 1)
                    for (j := 1 to n − i)
                          if (aj >aj+1) then interchange aj and aj+1

• At the first pass the largest element has been put into the correct position
• In each subsequent pass, an additional element is put in the correct position.
