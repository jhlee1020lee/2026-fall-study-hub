---
course: "computer_architecture"
source_pdf: "lec.08.pdf"
pdf_page: 35
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.08.pdf"
generated_at: "2026-10-08T14:12:23Z"
---
Data Forwarding (= Register Bypassing)

What does “ADD rx ry rz” mean?

  ➟ Get values from RF[ry] and RF[rz] respectively and put result in RF[rx]
But, RF is just a part of an abstraction

  ➟ A way to connect dataflow between instructions
  ➟ “inputs to ADD are resulting values of the last instructions to assign to
   RF[ry] and RF[rz]
  ➟ RF doesn’t have to exist as a literal object
If only dataflow matters, no need to wait for WB




                                                                                35 / 51
