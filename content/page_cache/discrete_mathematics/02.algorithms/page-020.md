---
course: "discrete_mathematics"
source_pdf: "02.Algorithms.pdf"
pdf_page: 20
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf"
generated_at: "2026-09-09T01:12:41Z"
---
 Greedy Algorithms: Making Change
• Example: Design a greedy algorithm for making change (in U.S. money) of n cents with the
  following coins: quarters (25 cents), dimes (10 cents), nickels (5 cents), and pennies (1 cent) , using
  the least total number of coins.


• Idea: At each step choose the coin with the largest possible value that does not exceed the
  amount of change left.
  1. If n = 67 cents, first choose a quarter leaving 67−25 = 42 cents. Then choose another quarter
     leaving 42 −25 = 17 cents
  2. Then choose 1 dime, leaving 17 − 10 = 7 cents.
  3. Choose 1 nickel, leaving 7 – 5 = 2 cents.
  4. Choose a penny, leaving one cent. Choose another penny leaving 0 cents.


• Thm: The greedy change-making algorithm for U.S. coins produces change using the fewest coins
  possible.
