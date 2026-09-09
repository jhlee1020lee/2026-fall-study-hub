---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 63
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
MyTree: use Iter, ListIF, provide Iterable, TreeIF
enum MyTree[+A]:
 case Leaf
 case Node(value: A, left: MyTree[A], right: MyTree[A])
import MyTree._

// behaves like MyTree[A] <: Iterable[A], but clumsy in OOP
given treeIterable[L[_]](using LL: Listlike[L], _ITR: Iter[L]): Iterable[MyTree]
with
  type Itr[A] = L[A]
  def ITR = _ITR
  extension [A](t: MyTree[A])
    def iter: L[A] = t match {
      case Leaf => !()
      case Node(v, lt, rt) => v :: (lt.iter ++ rt.iter)
    }
