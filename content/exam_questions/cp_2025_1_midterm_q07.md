---
title: "2025-1 중간 복기 7번 - static 중첩 Class 코드 수정"
cssclasses: [exam-question]
description: 기출 문제 원문 미리보기 · 제공 정답 제외
---

문제 원문 · 제공 정답 제외. 이미지를 아래로 읽으면 전체 문항을 볼 수 있습니다.

<img src="assets/exam_questions/cp_2025_1_midterm_q07-01.png" width="1425" height="1470" alt="2025-1 중간 복기 7번 - static 중첩 Class 코드 수정 문제 원문 1/1 · PDF p.4" loading="eager" decoding="async">

<details>
<summary>텍스트로 읽기 · 복사 / Read as text</summary>

<pre class="exam-question-text">7. 다음 코드는 TestClass 내부의 static 중첩 클래스가 외부 필드 s에 접근하려 할 때 컴파일 오류가 발생한다. testMethod()는 수정할 수 없고, 실행 시 “New Value”가 출력되도록 고치시오.

```java
class TestClass {
    String s = &quot;Hello world&quot;;

    static class InnerClass {
        void testMethod() {
            s = &quot;New Value&quot;;
            System.out.println(s);
        }
    }
}

class Main {
    public static void main(String[] args) {
        TestClass.InnerClass t = new TestClass.InnerClass();
        t.testMethod();
    }
}
```

틀린 이유:

고친 코드:</pre>

</details>

### 출처와 주의사항

<ul>
<li>공식 원본·공식 정답으로 검증되지 않은 복기본. 연도·학기·교수는 파일명 근거.</li>
<li>testMethod() 수정 금지 제약을 보존함. &#x27;틀린 이유&#x27;와 &#x27;고친 코드&#x27;는 원문에 인쇄된 빈 응답란 제목이며 제공 답안이 아님.</li>
</ul>

- Source ID: `cp_2025_1_midterm_recall` · PDF 페이지: 4
- 사용자 제공 자료의 문제 발췌입니다. 현재 학기 시험 범위·출제 예고를 의미하지 않습니다.
