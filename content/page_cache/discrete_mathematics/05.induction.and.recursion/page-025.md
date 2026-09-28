---
course: "discrete_mathematics"
source_pdf: "05.Induction.and.Recursion.pdf"
pdf_page: 25
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/05.Induction.and.Recursion.pdf"
generated_at: "2026-09-28T00:49:45Z"
---
Complexity of Merge Sort
• Complexity of Merge: Two sorted lists with m elements and n elements can be merged
  into a sorted list using no more than m + n − 1 comparisons.

• Complexity of Merge Sort: The number of comparisons needed to merge a list with n
  elements is O(n log n).
  – For simplicity, assume that n is a power of 2, say 2m.
  – At the end of the splitting process, we have a binary tree with m levels, and 2m lists with one
   element at level m.
  – The merging process begins at level m with the pairs of 2m lists with one element combined into
   2m−1 lists of two elements. Each merger takes two one comparison.
  – The procedure continues , at each level (k = m, m−1, m−1,…,3,2,1), 2k lists with 2m−k elements
   are merged into 2k−1 lists, with 2m−k + 1 elements at level k−1.
  – The total number of comparisons is bounded by n log n – n + 1
  – The fastest comparison-based sorting algorithms have O(n log n) complexity. So, merge sort
   achieves the best possible big-O estimate of time complexity
