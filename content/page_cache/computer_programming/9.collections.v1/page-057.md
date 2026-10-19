---
course: "computer_programming"
source_pdf: "9.collections.v1.pdf"
pdf_page: 57
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/9.collections.v1.pdf"
generated_at: "2026-10-19T23:44:17Z"
---
Comparator Example: Main

 public static void main(String[] args) {
     List<Player> squidGame = new ArrayList<Player>();
     squidGame.add(new Player("Gihun", 456));
     squidGame.add(new Player("Sangwoo", 218));
     squidGame.add(new Player("Ilnam", 1));
     squidGame.add(new Player("Saebyuk", 67));
     squidGame.add(new Player("Ali", 199));

     TreeSet<Player> sortbyName = new TreeSet<Player>(new NameComp());
     sortbyName.addAll(squidGame); System.out.println(sortbyName);

     TreeSet<Player> sortbyId = new TreeSet<Player>(new IdComp());
     sortbyId.addAll(squidGame); System.out.println(sortbyId);
 }


                                     Jaemin Yoo (SNU)                    57
