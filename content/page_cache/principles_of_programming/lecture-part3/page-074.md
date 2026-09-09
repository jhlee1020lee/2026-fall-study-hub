---
course: "principles_of_programming"
source_pdf: "lecture-part3.pdf"
pdf_page: 74
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part3.pdf"
generated_at: "2026-09-09T01:13:30Z"
---
Turning Type Classes into OO Classes
import scala.language.implicitConversions
type curry1[F[_,_],A1] = ([X] =>> F[X,A1])
type curry2[F[_,_,_],A1,A2] = ([X] =>> F[X,A1,A2])
type curry3[F[_,_,_,_],A1,A2,A3] = ([X] =>> F[X,A1,A2,A3])

trait dyn[S[_]]:
  type Data
  val * : Data
  given DI: S[Data]

object dyn {
  implicit // needed for implicit conversion of D into dyn[S]
  def apply[S[_],D](d: D)(implicit i: S[D]): dyn[S] = new {
     type Data = D
     val * = d
     val DI = i
   }
}
