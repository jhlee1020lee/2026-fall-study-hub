---
course: "computer_programming"
source_pdf: "7.inheritance.2.pdf"
pdf_page: 41
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf"
generated_at: "2026-09-29T23:41:41Z"
---
Comparable<T> Example: Strings
 public int compareTo(String anotherString) {
    int len1 = value.length;
    int len2 = anotherString.value.length;
    int lim = Math.min(len1, len2);
    char v1[] = value;
    char v2[] = anotherString.value;
    int k = 0;
    while (k < lim) {
        char c1 = v1[k];
        char c2 = v2[k];
        if (c1 != c2) {
             return c1 - c2;
        }
        k++;
    }
    return len1 - len2;
 }

                                          Jaemin Yoo (SNU)   41
