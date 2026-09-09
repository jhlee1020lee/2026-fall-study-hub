---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 60
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Solution 1: Using Lists of Trees
class MyTreeIter[A](val lst: MyList[MyTree[A]]) extends Iter[A] {
 val getValue = lst match {
   case MyCons(Node(v,_,_), _) => Some(v)
   case _ => None
 }
 def getNext = {
   val remainingTrees : MyList[MyTree[A]] = lst match {
     case MyNil() => throw new Exception("...")
     case MyCons(hd,tl) => hd match {
       case Empty() => throw new Exception("...")
       case Node(_,Empty(),Empty()) => tl
       case Node(_,lt,Empty()) => MyCons(lt,tl)
       case Node(_,Empty(),rt) => MyCons(rt,tl)
       case Node(_,lt,rt) => MyCons(lt,MyCons(rt,tl))
     }
   }
   new MyTreeIter(remainingTrees)
 }}
