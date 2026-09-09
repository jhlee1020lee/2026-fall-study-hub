---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 47
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
Modifying Traits
def StackOverridePut[S,A](newPut: (S,A)=>S)(implicit STK: Stack[S,A])
: Stack[S,A] = new {
  extension (u: Unit)
   def empty = STK.empty(u)
  extension (s: S)
   def get = STK.get(s)
   def put(a: A) = newPut(s,a)
}

def Doubling[S](implicit STK: Stack[S,Int]) : Stack[S,Int] =
 StackOverridePut((s,a) => s.put(2 * a))

def Incrementing[S](implicit STK: Stack[S,Int]) : Stack[S,Int] =
 StackOverridePut((s,a) => s.put(a + 1))

def Filtering[S](implicit STK: Stack[S,Int]) : Stack[S,Int] =
 StackOverridePut((s,a) => if (a >= 0) s.put(a) else s)
