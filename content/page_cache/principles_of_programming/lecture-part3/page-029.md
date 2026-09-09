---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 29
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
Implement Iterable for MyTree using Listlike,Iter
enum MyTree[+A]:
 case Leaf
 case Node(value: A, left: MyTree[A], right: MyTree[A])
import MyTree._

// behaves like MyTree[A] <: Iterable[A], but clumsy in OOP
given treeIterable[L,A](using LL: Listlike[L,A], _ITR: Iter[L,A])
  : Iterable[MyTree[A], A] with
  type Itr = L
  def ITR = _ITR
  extension (t: MyTree[A])
    def iter: L = t match {
      case Leaf => !()
      case Node(v, lt, rt) => v :: (lt.iter ++ rt.iter)
    }
