---
course: "computer_programming"
source_pdf: "7.inheritance.2.pdf"
pdf_page: 38
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf"
generated_at: "2026-09-29T23:41:41Z"
---
Comparable<T> Example
 class Seagull implements Comparable<Seagull> {
    int flyingHeight, numFriend;
    Seagull(int flyingHeight, int numFriend) {
        this.flyingHeight = flyingHeight;
        this.numFriend = numFriend;
    }
    @Override
    public int compareTo(Seagull seagull) {
        if (this.flyingHeight > seagull.flyingHeight)
            return 1;
        else if (this.flyingHeight == seagull.flyingHeight)
            return 0;
        else return -1;
    }
 }

                                     Jaemin Yoo (SNU)         38
