---
course: "computer_programming"
source_pdf: "Lab03.v2.pdf"
pdf_page: 22
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab03.v2.pdf"
generated_at: "2026-09-19T10:20:37Z"
---
15mins
Problem 1-1 : Create the Player Class
● Attributes and Constructor for the Player Class

           import java.util.Random;

           public class Player {
               private String userId;
               private int health = 50;
               Random random;

                Player(String userId, int randomSeed) {
                     this.userId = userId;
                     random = new Random(randomSeed);
                }
                // TODO: problem1
               ...



                                                          22
