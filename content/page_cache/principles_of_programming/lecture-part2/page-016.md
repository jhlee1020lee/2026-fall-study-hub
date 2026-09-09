---
course: "principles_of_programming"
source_pdf: "lecture-part2.pdf"
pdf_page: 16
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/principles_of_programming/lecture-part2.pdf"
generated_at: "2026-09-09T01:13:03Z"
---
Class: Parameterized Record
import reflect.Selectable.reflectiveSelectable

type gee_type = {val name:String; val age: Int; def getPP(): String}
def gee_fun(_name: String, _age: Int) : gee_type = {
  if (!(_age >= 0 && _age < 200)) throw new Exception("Out of range")
  object tmp {
    val name : String = _name
    val age : Int = _age
    def getPP() : String = name + " of age " + age.toString() }
  tmp }
val gee : gee_type = gee_fun("David Jones",25)

gee.getPP()
