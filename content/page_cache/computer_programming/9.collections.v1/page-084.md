---
course: "computer_programming"
source_pdf: "9.collections.v1.pdf"
pdf_page: 84
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/9.collections.v1.pdf"
generated_at: "2026-10-19T23:44:17Z"
---
Utilities Example: Min & Max

class AlphabeticComparator implements Comparator<String> {
   @Override
   public int compare(String o1, String o2) {
      return o1.toLowerCase().compareTo(o2.toLowerCase());
   }
}

List list = Arrays.asList("one Two three Four five six one".split(" "));
System.out.println("max: " + Collections.max(list));                   // three
System.out.println("min: " + Collections.min(list));                   // Four

AlphabeticComparator comp = new AlphabeticComparator();
System.out.println("max w/ comp: " + Collections.max(list, comp));     // Two
System.out.println("min w/ comp: " + Collections.min(list, comp));     // five


                                       Jaemin Yoo (SNU)                           84
