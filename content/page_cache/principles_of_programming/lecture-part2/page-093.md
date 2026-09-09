---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 93
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Implementing Traits
class ListIterDict[K,V]
      (eq: (K,K)=>Boolean, list: List[(K,V)])
      extends ListIter[(K,V)](list)
         with Dict[K,V]
{
  def add(k:K,v:V): ListIterDict[K,V] =
    new ListIterDict(eq,(k,v)::list)
  def find(k: K) : Option[V] = {
    def go(l: List[(K, V)]): Option[V] = l match {
        case Nil => None
        case (k1, v1) :: tl =>
          if (eq(k, k1)) Some(v1) else go(tl) }
    go(list) }
}
