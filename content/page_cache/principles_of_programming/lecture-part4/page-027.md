---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 27
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
General lifetime annotation
 fn foo1<'a>(s1: &'a mut String, s2: &'a String) -> &'a str {
   …
 }
 fn foo2<'a,'b>(s1: &'a String, s2: &'b String) -> &'a str {
   …
 }
 fn foo3<'a,'b,'c>(s1: &'a String, s2: &'b String) -> &'c str {
   …
 }
 fn foo4<'a,'b,'c, 'd, 'e>(s1: &'a String, s2: &'b String, s3: &'c String)
    -> (&'d str, &'e str) where 'a: 'd, 'b:'d, 'b:'e, 'c:'e {

     …

 }
