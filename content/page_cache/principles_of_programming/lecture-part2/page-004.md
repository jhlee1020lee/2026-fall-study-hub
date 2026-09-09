---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 4
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Sub Types to the Rescue!
import reflect.Selectable.reflectiveSelectable

type NameHome = { val name: String; val home: String }
type NameMobile = { val name: String; val mobile: String}
type Name = { val name: String }

NameHome <: Name (NameHome is a sub type of Name)
NameMobile <: Name (NameMobile is a sub type of Name)

def greeting(r: Name) = "Hi " + r.name + ", How are you?"
greeting(tom)
greeting(bob)
