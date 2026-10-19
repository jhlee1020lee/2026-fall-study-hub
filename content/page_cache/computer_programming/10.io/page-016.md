---
course: "computer_programming"
source_pdf: "10.io.pdf"
pdf_page: 16
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/10.io.pdf"
generated_at: "2026-10-19T23:44:09Z"
---
ByteArrayOutputStream Example

static void writeMemory() {
    try {
        // An internal buffer is created along with the stream
        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
        byteArrayOutputStream.write(65);
        byteArrayOutputStream.write(75);               // Stored in an internal buffer

        byte[] x = byteArrayOutputStream.toByteArray();       // Copy the buffer
        System.out.println(x[0]);                             // 65 is printed
        byteArrayOutputStream.close();
    } catch (IOException e) {
         e.printStackTrace();
    }
}


                                       Jaemin Yoo (SNU)                                  16
