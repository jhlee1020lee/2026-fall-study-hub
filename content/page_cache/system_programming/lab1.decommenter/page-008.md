---
course: "system_programming"
source_pdf: "Lab1.Decommenter.pdf"
pdf_page: 8
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/Lab1.Decommenter.pdf"
generated_at: "2026-10-02T05:08:57Z"
---
Requirements – Handle ‘\’+ following char as ordinary characters (5/9)

                                                                                 Standard
     Case           Standard Input Stream             Standard Output Stream
                                                                               Error Stream

 Part of the
                       abc"def\"ghi"jkln                 abc"def\"ghi"jkln
   string

 Part of the
 character              abc'def\'ghi'jkln                 abc'def\'ghi'jkln
  constant

 ▪   Handle ‘\’+ following char as ordinary characters when
      • Within the string or character constant
 ▪   A C compiler would incur an error (multiple characters in a character constant)
      • But many C preprocessors would not
      • And your program should not either

                                                  8
