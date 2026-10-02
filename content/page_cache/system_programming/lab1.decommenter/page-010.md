---
course: "system_programming"
source_pdf: "Lab1.Decommenter.pdf"
pdf_page: 10
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/Lab1.Decommenter.pdf"
generated_at: "2026-10-02T05:08:57Z"
---
Requirements – Handle Unterminated Str and Char Const (7/9)
                                                                            Standard
    Case         Standard Input Stream           Standard Output Stream
                                                                          Error Stream

 Part of the
                    abc"def/*ghi*/jkln              abc"def/*ghi*/jkln
   string

 Part of the
 character          abc'def/*ghi*/jkln              abc'def/*ghi*/jkln
  constant

▪   Handle unterminated str and char const w/o generating errors or warnings
▪   A C compiler would incur an error (newline character in a string constant)
     • But many C preprocessors would not
     • And your program should not either

                                            10
