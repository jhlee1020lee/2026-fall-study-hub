---
course: "computer_programming"
source_pdf: "Lab03.v2.pdf"
pdf_page: 9
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab03.v2.pdf"
generated_at: "2026-09-19T10:20:37Z"
---
“this” Keyword
 ● A special keyword used to indicate the “self-object”
   ● Can be used to indicate attributes of the class
   ● Can be used to indicate methods of the class
   ● Can be used to call a constructor of the object
class Car {                                   void printColor() {
    int speed = 100;                              System.out.println(this.color); //Attribute
    String color = "red";                     }
    void printSpeed() {
        System.out.println(this.speed);       void printCarInfo() {
    }                                             this.printSpeed(); //Method
    Car(int speed, String color) {            }
        this.speed = speed;
        this.color = color;                   Car() {
    }                                             this(55, "blue"); //Constructor
                                              }
                                          }

                                                                                                9
