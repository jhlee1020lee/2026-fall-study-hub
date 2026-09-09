---
course: "discrete_mathematics"
source_pdf: "02.Algorithms.pdf"
pdf_page: 22
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/02.Algorithms.pdf"
generated_at: "2026-09-09T01:12:41Z"
---
Greedy Scheduling
• Example: We have a group of proposed talks with start and end times. Construct a greedy
  algorithm to schedule as many as possible in a lecture hall, under the following assumptions:
  – When a talk starts, it continues till the end.
  – No two talks can occur at the same time.
  – A talk can begin at the same time that another ends.
  – Once we have selected some of the talks, we cannot add a talk which is incompatible with
   those already selected because it overlaps at least one of these previously selected talks.


• How should we make the “best choice” at each step of the algorithm? That is, which talk do
  we pick ?
     ✓ The talk that starts earliest among those compatible with already chosen talks?
     ✓ The talk that is shortest among those already compatible?
     ✓ The talk that ends earliest among those compatible with already chosen talks?
