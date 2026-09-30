---
course: "computer_programming"
source_pdf: "Lab04.v2.pdf"
pdf_page: 8
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab04.v2.pdf"
generated_at: "2026-09-30T14:34:15Z"
---
Getter and Setter
● Access validation with Getter/Setter

        class Book {
           private String title;
           public void setTitle(String title) {
               if (title == null || title.equals("")) {
                   System.out.println(
                           "Title cannot be null or empty");
               } else {
                   this.title = title;
               }
           }
           public String getTitle() {
               return title;
               }
        }


                                                               8
