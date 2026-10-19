---
course: "computer_programming"
source_pdf: "10.io.pdf"
pdf_page: 24
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/10.io.pdf"
generated_at: "2026-10-19T23:44:09Z"
---
FileWriter Example

public static void writeLines(String fName, List<String> l) {
  try {
      FileWriter fileWriter = new FileWriter(fName);
      for (String string : l) {
          fileWriter.write(string);
      }
      fileWriter.close();
  } catch (IOException e) {
      e.printStackTrace();
  }
}

                               Jaemin Yoo (SNU)                 24
