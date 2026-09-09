---
course: "computer_programming"
source_pdf: "4.oop.pdf"
pdf_page: 41
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/4.oop.pdf"
generated_at: "2026-09-09T01:12:27Z"
---
Method Call: Call-by-Reference

 class Test {
    static void swap(IntHolder a, IntHolder b) {
        int temp = a.value;
        a.value = b.value;
        b.value = temp;
    }
    public static void main(String[] args) {
        IntHolder a = new IntHolder(2), b = new IntHolder(3);
        swap(a, b);
        System.out.println(a.value + " " + b.value);          // it works!
    }
 }


                                 Jaemin Yoo (SNU)                            41
