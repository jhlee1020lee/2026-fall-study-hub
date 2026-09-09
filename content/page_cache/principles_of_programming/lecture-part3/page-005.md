---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 5
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
Further example: Ordered Bag
class Bag[U <: Ord[U]] protected (val toList: List[U]) {
  def this() = this(Nil)
  def add(x: U) : Bag[U] = {
    def go(elmts: List[U]): List[U] =
      elmts match {
        case Nil => x :: Nil
        case e :: _ if (x < e) => x :: elmts
        case e :: _ if (x === e) => elmts
        case e :: rest => e :: go(rest)
      }
    new Bag(go(toList))
  }
}
val emp = new Bag[OInt]()
val b = emp.add(new OInt(3)).add(new OInt(2)).
            add(new OInt(10)).add(new OInt(2))
b.toList.map((x)=>x.value)
