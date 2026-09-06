---
title: "2026-1 기말 복기 2번 - static·dynamic resolution"
cssclasses: [exam-question]
description: 기출 문제 원문 미리보기 · 제공 정답 제외
---

문제 원문 · 제공 정답 제외. 이미지를 아래로 읽으면 전체 문항을 볼 수 있습니다.

<img src="assets/exam_questions/cp_2026_1_final_q02-01.png" width="1425" height="1785" alt="2026-1 기말 복기 2번 - static·dynamic resolution 문제 원문 1/1 · PDF p.2" loading="eager" decoding="async">

<details>
<summary>텍스트로 읽기 · 복사 / Read as text</summary>

<pre class="exam-question-text">2번

다음 코드의 실행 결과 적기, statically resolve 되는 것과 dynamically resolve 되는 것 설명

```java
class A {
    int x = 1;

    static String who() {
        return &quot;A&quot;;
    }

    String say() {
        return &quot;A&quot; + x;
    }
}

class B extends A {
    int x = 2;

    static String who() {
        return &quot;B&quot;;
    }

    @Override
    String say() {
        return &quot;B&quot; + x + &quot;/&quot; + super.x;
    }
}

class Main {
    public static void main(String[] args) {
        A a = new B();
        B b = new B();

        System.out.println(a.x + &quot; &quot; + b.x);
        System.out.println(a.who() + &quot; &quot; + b.who());
        System.out.println(a.say() + &quot; &quot; + ((A) b).say());
    }
}
```</pre>

</details>

### 출처와 주의사항

<ul>
<li>공식 원본·공식 정답으로 검증되지 않은 복기본. 본문에서 문제 순서와 일부 내용의 부정확 가능성을 직접 고지함.</li>
<li>기말·교수는 파일명 근거; 2026-1은 본문에서도 확인.</li>
</ul>

- Source ID: `cp_2026_1_final_recall` · PDF 페이지: 2
- 사용자 제공 자료의 문제 발췌입니다. 현재 학기 시험 범위·출제 예고를 의미하지 않습니다.
