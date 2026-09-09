---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 92
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Interface using Traits
// abstract class Dict[K,V] {
// def add(k: K, v: V): Dict[K,V]
// def find(k: K): Option[V] }

trait Dict[K,V] {
  def add(k: K, v: V): Dict[K,V]
  def find(k: K): Option[V]
}
