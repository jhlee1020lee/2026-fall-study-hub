---
course: "computer_programming"
source_pdf: "7.inheritance.2.pdf"
pdf_page: 23
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf"
generated_at: "2026-09-29T23:41:41Z"
---
equals() in Collections
 public static int frequency(Collection<?> c, Object o) {
    int result = 0;               // “?” represents “any” class
    if (o == null) {
        for (Object e : c)
             if (e == null)
                 result++;
    } else {
        for (Object e : c)
             if (o.equals(e))
                 result++;
    }
    return result;
 }

                                  Jaemin Yoo (SNU)                23
