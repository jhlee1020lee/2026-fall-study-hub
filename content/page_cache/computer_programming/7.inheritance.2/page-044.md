---
course: "computer_programming"
source_pdf: "7.inheritance.2.pdf"
pdf_page: 44
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf"
generated_at: "2026-09-29T23:41:41Z"
---
Comparable<T> Example: Sorting

 class Student implements Comparable<Student> {
    double gpa;
    Student(double gpa) { this.gpa = gpa; }
    public int compareTo(Student anotherStudent) {
        double diff = gpa - anotherStudent.gpa;
        return diff > 0 ? 1 : diff < 0 ? -1 : 0;
    }
    @Override
    public String toString() { // for convenience
        return Double.toString(gpa);
    }
 }


                                  Jaemin Yoo (SNU)   44
