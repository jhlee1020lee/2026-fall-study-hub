---
course: "principles_of_programming"
source_pdf: "lecture-part4.pdf"
pdf_page: 37
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part4.pdf"
generated_at: "2026-09-09T01:13:51Z"
---
Hack: achieving proper immutability
 struct Foo<'a> {
    x: i64,
    s: &'a mut String
 }
 fn main() {
    let mut str = "abc".to_string();
    let foo = Foo {x: 42, s: &mut str};
    let _foo_immutable = &foo;
    println!("{} {}", foo.x, foo.s);
    // foo.s.push_str("def");
    println!("{} {}", foo.x, foo.s);
    let _foo_end = _foo_immutable;
 }
