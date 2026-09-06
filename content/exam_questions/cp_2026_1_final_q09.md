---
title: "2026-1 기말 복기 9번 - overloading·overriding 출력 추적"
cssclasses: [exam-question]
description: 기출 문제 원문 미리보기 · 제공 정답 제외
---

문제 원문 · 제공 정답 제외. 이미지를 아래로 읽으면 전체 문항을 볼 수 있습니다.

<img src="assets/exam_questions/cp_2026_1_final_q09-01.png" width="1425" height="1401" alt="2026-1 기말 복기 9번 - overloading·overriding 출력 추적 문제 원문 1/1 · PDF p.6" loading="eager" decoding="async">

<details>
<summary>텍스트로 읽기 · 복사 / Read as text</summary>

<pre class="exam-question-text">9번

다음 코드의 실행 결과 적기, 각각이 어떻게 resolve 되는지 설명

```java
class A {
    int x = 10;

    void say(int v) { System.out.println(&quot;A.say(int) &quot; + v); }

    void say(double v) { System.out.println(&quot;A.say(double) &quot; + v); }
}

class B extends A {
    int x = 20;

    @Override
    void say(int v) { System.out.println(&quot;B.say(int) &quot; + v); }
}

class Main {
    public static void main(String[] args) {
        A a = new B();
        B b = new B();

        a.say(3);
        a.say(3.0);
        b.say(3);
        b.say(3.0);
        System.out.println(a.x + &quot; &quot; + b.x);
    }
}
```</pre>

</details>

### 출처와 주의사항

<ul>
<li>공식 원본·공식 정답으로 검증되지 않은 복기본. 본문에서 문제 순서와 일부 내용의 부정확 가능성을 직접 고지함.</li>
<li>기말·교수는 파일명 근거; 2026-1은 본문에서도 확인.</li>
</ul>

- Source ID: `cp_2026_1_final_recall` · PDF 페이지: 6
- 사용자 제공 자료의 문제 발췌입니다. 현재 학기 시험 범위·출제 예고를 의미하지 않습니다.
