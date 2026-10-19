---
course: "computer_programming"
source_pdf: "10.io.pdf"
pdf_page: 10
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/10.io.pdf"
generated_at: "2026-10-19T23:44:09Z"
---
ByteArrayInputStream Example
 import java.io.ByteArrayInputStream;
 import java.io.IOException;

 public class Main {
     public static void main(String[] args) throws IOException {
         byte[] buf = { 35, 36 };
         ByteArrayInputStream inputStream = new ByteArrayInputStream(buf);
         int k = 0;
         while ((k = inputStream.read()) != -1) {
             char ch = (char) k;       // Conversion of a byte into character.
             System.out.println("ASCII:" + k + "; Special character: " + ch);
         }                             // k=35 then k=36
         inputStream.close();
     }
 }


                                        Jaemin Yoo (SNU)                         10
