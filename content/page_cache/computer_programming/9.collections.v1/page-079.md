---
course: "computer_programming"
source_pdf: "9.collections.v1.pdf"
pdf_page: 79
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/9.collections.v1.pdf"
generated_at: "2026-10-19T23:44:17Z"
---
TreeMap Example: Function

static TreeMap<String,Integer>frequency(String[] names) {
    Map<String, Integer> frequency = new TreeMap<String, Integer>();
    for(String name : names) {
        Integer currentCount = frequency.get(name);
        if(currentCount == null) {
            currentCount = 0; // auto-boxing
        }
        frequency.put(name, ++currentCount);
    }
    return frequency;
}


                                  Jaemin Yoo (SNU)                     79
