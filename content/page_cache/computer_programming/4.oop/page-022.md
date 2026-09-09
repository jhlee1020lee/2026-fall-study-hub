---
course: "computer_programming"
source_pdf: "4.oop.pdf"
pdf_page: 22
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/4.oop.pdf"
generated_at: "2026-09-09T01:12:27Z"
---
Constructor Parameters

 public class Car {
    int weight;
                                        new Car(1500, "red").printInfo();
    String color = "unknown";
                                        new Car(2000).printInfo();
    Car(int w) { weight = w; }
    Car(int w, String c) {
        weight = w;
        color = c;
    }
    void printInfo() {
        System.out.println(weight + " kg, " + color);
    }
 }


                                  Jaemin Yoo (SNU)                          22
