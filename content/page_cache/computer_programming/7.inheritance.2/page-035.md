---
course: "computer_programming"
source_pdf: "7.inheritance.2.pdf"
pdf_page: 35
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/7.inheritance.2.pdf"
generated_at: "2026-09-29T23:41:41Z"
---
List<E> Interface

 List<Integer> list = new ArrayList<>();
                                                        Any of these declaration
 // List<Integer> list = new LinkedList<>();
 // List<Integer> list = new MyFavoriteList<>();
                                                        will not have any problem
 // List<Integer> list = new MyOwnList<>();             running the code below.

 list.add(10);        User-defined list classes implement the List interface.
 list.add(20);
 list.add(30);

 list.get(2);
 list.remove(1);
 list.size();


                                     Jaemin Yoo (SNU)                               35
