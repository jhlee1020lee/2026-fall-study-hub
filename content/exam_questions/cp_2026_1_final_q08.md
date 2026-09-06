---
title: "2026-1 기말 복기 8번 - ambiguous call"
cssclasses: [exam-question]
description: 기출 문제 원문 미리보기 · 제공 정답 제외
---

문제 원문 · 제공 정답 제외. 이미지를 아래로 읽으면 전체 문항을 볼 수 있습니다.

<img src="assets/exam_questions/cp_2026_1_final_q08-01.png" width="1425" height="801" alt="2026-1 기말 복기 8번 - ambiguous call 문제 원문 1/1 · PDF p.5" loading="eager" decoding="async">

<details>
<summary>텍스트로 읽기 · 복사 / Read as text</summary>

<pre class="exam-question-text">8번

다음 중 ambiguous call이어서 컴파일 실패하는 것

```java
class Overload {
    static String f(Object o) { return &quot;Object&quot;; }

    static String f(String o) { return &quot;String&quot;;}

    static String f(Integer o) { return &quot;Integer&quot;; }
}
```

A. Overload.f(“a”)

B. Overload.f((Object) null)

C. Overload.f((String) null)

D. Overload.f(null)</pre>

</details>

### 출처와 주의사항

<ul>
<li>공식 원본·공식 정답으로 검증되지 않은 복기본. 본문에서 문제 순서와 일부 내용의 부정확 가능성을 직접 고지함.</li>
<li>기말·교수는 파일명 근거; 2026-1은 본문에서도 확인.</li>
<li>보기 A의 문자열 따옴표는 원문에서 “a”로 인쇄되어 있어 그대로 보존함.</li>
</ul>

- Source ID: `cp_2026_1_final_recall` · PDF 페이지: 5
- 사용자 제공 자료의 문제 발췌입니다. 현재 학기 시험 범위·출제 예고를 의미하지 않습니다.
