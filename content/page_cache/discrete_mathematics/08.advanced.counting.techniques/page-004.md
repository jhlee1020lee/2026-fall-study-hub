---
course: "discrete_mathematics"
source_pdf: "08.Advanced.Counting.Techniques.pdf"
pdf_page: 4
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/discrete_mathematics/08.Advanced.Counting.Techniques.pdf"
generated_at: "2026-10-18T23:43:34Z"
---
 The Tower of Hanoi
• In the late nineteenth century, the French mathematician Édouard Lucas invented a
  puzzle consisting of three pegs on a board with disks of different sizes. Initially all of the
  disks are on the first peg in order of size, with the largest on the bottom.
  – Rules: You are allowed to move the disks one at a time from one peg to another as long as a larger
   disk is never placed on a smaller.
  – Goal: Using allowable moves, end up with all the disks on the second peg in order of size with
   largest on the bottom.
  – Solution: Let Hn denote the number of moves needed to solve the Tower of Hanoi Puzzle with n
   disks. We can transfer the top n −1 disks, following the rules of the puzzle, to peg 3 using Hn−1
   moves. Then, we use 1 move to transfer the largest disk to the second peg. Finally, we transfer the
   n −1 disks from peg 3 to peg 2 using Hn−1 additional moves. This can not be done in fewer steps.
  – Hence, 𝐻𝑛 = 2𝐻𝑛−1 + 1 and the initial condition is 𝐻1 = 1.
