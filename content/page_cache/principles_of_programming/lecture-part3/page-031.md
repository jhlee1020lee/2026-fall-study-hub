---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 31
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
Implement Treelike for MyTree
// behaves like MyTree[A] <: Treelike[A] in OOP
given mytreeTreelike[A] : Treelike[MyTree[A],A] with
  extension (u: Unit)
    def unary_! = Leaf
  extension (a: A)
    def has(l: MyTree[A], r: MyTree[A]) = Node(a,l,r)
  extension (t: MyTree[A])
    def root = t match {
      case Leaf => None
      case Node(v,_,_) => Some(v)
    }
    def left = t match {
      case Leaf => t
      case Node(_,lt,_) => lt
    }
    def right = t match {
      case Leaf => t
      case Node(_,_,rt) => rt }
