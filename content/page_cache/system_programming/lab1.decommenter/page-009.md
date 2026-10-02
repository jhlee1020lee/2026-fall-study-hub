---
course: "system_programming"
source_pdf: "Lab1.Decommenter.pdf"
pdf_page: 9
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/Lab1.Decommenter.pdf"
generated_at: "2026-10-02T05:08:57Z"
---
Requirements – Newline Characters in Str or Char Const (6/9)
                                                                           Standard
     Case        Standard Input Stream          Standard Output Stream
                                                                         Error Stream

 Part of the
                     abc"defnghi"jkln              abc"defnghi"jkln
   string

 Part of the
 character           abc'defnghi'jkln               abc'defnghi'jkln
  constant

 ▪ Handle the newline character in str or chat const without generating errors or
   warnings
 ▪ A C compiler would incur an error (newline character in a string constant)
     • But many C preprocessors would not
     • And your program should not either

                                            9
