---
course: "system_programming"
source_pdf: "Lab1.Decommenter.pdf"
pdf_page: 5
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/Lab1.Decommenter.pdf"
generated_at: "2026-10-02T05:08:57Z"
---
Requirements – Support Both Types of Comments (2/9)
                                                      Standard Output
       Case              Standard Input Stream                           Standard Error Stream
                                                          Stream

     Single line
                                 abc//defn                 abcsn
     comment


     Multi-line
                         abc/*defnghi*/jklnmnon        abcsnjklnmnon
     comment


 ▪   2 Types of comments:
        • “//”: Single line comment
        • “/* … */”: Multi-line comment
 ▪   Ensure the program adds blank lines as needed to preserve original line numbering


                                                  5
