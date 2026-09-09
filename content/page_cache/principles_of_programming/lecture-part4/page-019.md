---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 19
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
An example with ownership and borrowing

 An example showing how ownership and borrowing work.

 // arg owns a string, say ARG
 fn gee(arg: String) -> String {
    let mut x = String::from("abc"); // x owns the string "abc"
    {
       let y = x + &arg; // y owns the string "abc"+ARG, x not accessible
       x = y + &arg; // x owns the string "abc"+ARG+ARG, y not accessible
    } // y is deallocated
    let z = x; // z owns the string "abc"+ARG+ARG, x not accessible
    return z; // the string "abc"+ARG+ARG is returned, z not accessible
 } // arg, x, z are dallocated, the string ARG in arg is deallocated
