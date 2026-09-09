---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 13
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Stack memory with static size and static lifetime

 Stack memory consists of variables of sized types (ie, static header sizes)
 with scopes (ie, static lifetime).
 A stack variable of a type T stores a header of the type T.

 // variable arg of type i64 (8-byte header) with Scope 1
 fn foo(arg: i64) -> i64 {
    let mut x = 10; // variable x of type i64 with Scope 1
    {
       let y = arg + x; // variable y of type i64 with Scope 2
       x = x + y;
    } // Scope 2
    let x2 = x; // variable x2 of type i64 with Scope 1
    let z = arg + x2; // variable z of type i64 with Scope 1
    return z;
 } // Scope 1
