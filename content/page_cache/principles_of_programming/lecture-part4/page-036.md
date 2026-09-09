---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 36
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Caveat: subtle immutability in let (seems a design bug)
 • “let x : T” only guarantees its owned parts are unchanged
 • “&x” guarantees that all data reachable from x are unchanged
 struct Foo<'a> {
    x: i64,
    s: &'a mut String
 }
 fn main() {
    let mut str = "abc".to_string();
    let foo = Foo {x: 42, s: &mut str};
    println!("{} {}", foo.x, foo.s);
    foo.s.push_str("def");
    // (&foo).s.push_str("def");
    // foo.x = 37;
    println!("{} {}", foo.x, foo.s);
 }
