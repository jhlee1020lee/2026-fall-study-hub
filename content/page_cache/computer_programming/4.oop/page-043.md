---
course: "computer_programming"
source_pdf: "4.oop.pdf"
pdf_page: 43
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/4.oop.pdf"
generated_at: "2026-09-09T01:12:27Z"
---
Method Call: Call-by-Reference
                                                                  Memory

                                                                main function
 class Test {
    static void swap(IntHolder a, IntHolder b) {                       a
        int temp = a.value;                                      value     3
        a.value = b.value;                                             b
        b.value = temp;
                                                                 value     2
    }
    public static void main(String[] args) {
        IntHolder a = new IntHolder(2), b = new IntHolder(3);   swap function
        swap(a, b);
                                                                temp       2
        System.out.println(a.value + " " + b.value);
    }
 }


                                 Jaemin Yoo (SNU)                               43
