---
course: "computer_programming"
source_pdf: "7.inheritance.2.pdf"
pdf_page: 56
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf"
generated_at: "2026-09-29T23:41:41Z"
---
Think About... (Optional)
• What is the role of the List<T> interface?
• What is the role of the AbstractList<T> abstract class?
• Why it extends AbstractList<T>, not implementing List<T>?



  public abstract class AbstractList<E> implements List<E> {...}

  public class ArrayList<E> extends AbstractList<E>


                             Jaemin Yoo (SNU)                      56
