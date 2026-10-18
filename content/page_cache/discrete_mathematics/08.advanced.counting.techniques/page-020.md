---
course: "discrete_mathematics"
source_pdf: "08.Advanced.Counting.Techniques.pdf"
pdf_page: 20
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/08.Advanced.Counting.Techniques.pdf"
generated_at: "2026-10-18T23:43:34Z"
---
 Complexity of Merge Sort / Fast Integer Multiplication
• Merge Sort Example: Give a big-O estimate for the number of comparisons used by
  merge sort.
  – Since the number of comparisons used by merge sort to sort a list of n elements is less than
   M(n) where M(n) = 2M(n/2) + n, by the master theorem M(n) is O(n log n).


• Integer Multiplication Example: Give a big-O estimate for the number of bit operations
  used needed to multiply two n-bit integers using the fast multiplication algorithm.
  – We have shown that f(n) = 3f(n/2) + Cn, when n is even, where f(n) is the number of bit
    operations needed to multiply two n-bit integers. Hence by the master theorem with a = 3, b = 2,
    c = C, and d = 0 (so that we have the case where a > bd), it follows that f(n) is O(nlog 3).
  – Note that log 3 ≈ 1.6. Therefore the fast multiplication algorithm is a substantial improvement
    over the conventional algorithm that uses O(n2) bit operations.
