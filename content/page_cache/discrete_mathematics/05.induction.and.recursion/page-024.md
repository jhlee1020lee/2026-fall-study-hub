---
course: "discrete_mathematics"
source_pdf: "05.Induction.and.Recursion.pdf"
pdf_page: 24
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/05.Induction.and.Recursion.pdf"
generated_at: "2026-09-28T00:49:45Z"
---
Recursive Merge Sort
          procedure mergesort(L = a1, a2,…,an )
               if n > 1 then
                    m := ⌊n/2⌋
                    L1 := a1, a2,…,am
                    L2 := am+1, am+2,…,an
                    L := merge(mergesort(L1), mergesort(L2 ))

  procedure merge(L1, L2 :sorted lists)
       L := empty list
       while L1 and L2 are both nonempty
             remove smaller of first elements of L1 and L2 from its list;
             put at the right end of L
             if this removal makes one list empty
                    then remove all elements from the other list and append them to L
       return L
