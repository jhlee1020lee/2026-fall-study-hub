---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 11
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Sub Types for Records
• Permutation
                 =======================
          {…; x: T1; y: T2; …} <: {…; y: T2, x: T1; …}

• Width
                 =======================
                   {…; x: T; …} <: {…; …}

• Depth
                            T <: S
                =======================
                {…; x: T ; …} <: {…; x: S; …}
