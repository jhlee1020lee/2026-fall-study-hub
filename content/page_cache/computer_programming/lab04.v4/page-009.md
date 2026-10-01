---
course: "computer_programming"
source_pdf: "Lab04.v4.pdf"
pdf_page: 9
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab04.v4.pdf"
generated_at: "2026-10-01T16:19:03Z"
---
Getter and Setter
● Example of access validation with Getter/Setter

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


                                                               9
