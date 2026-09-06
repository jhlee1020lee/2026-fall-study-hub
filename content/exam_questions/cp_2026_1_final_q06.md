---
title: "2026-1 기말 복기 6번 - readPositiveInts 구현"
cssclasses: [exam-question]
description: 기출 문제 원문 미리보기 · 제공 정답 제외
---

문제 원문 · 제공 정답 제외. 이미지를 아래로 읽으면 전체 문항을 볼 수 있습니다.

<img src="assets/exam_questions/cp_2026_1_final_q06-01.png" width="1425" height="825" alt="2026-1 기말 복기 6번 - readPositiveInts 구현 문제 원문 1/1 · PDF p.4" loading="eager" decoding="async">

<details>
<summary>텍스트로 읽기 · 복사 / Read as text</summary>

<pre class="exam-question-text">6번

다음 요구사항을 만족시키는 함수

```java
static List&lt;Integer&gt; readPositiveInts(String path) throws IOException
```

을 작성하라

- try-with-resources와 함께 BufferedReader 사용
- line.trim().isEmpty() 가 true면 그 line 무시
- trimmed line에 대해 Integer.parseInt를 수행
- parse된 integer가 0 이하면 그 값을 포함해서 IllegalArgumentException throw
- IOException을 함수 내에서 catch 하지 말 것
- NumberFormatException이 발생하면 catch하지 말고 propagate 되게 놔두기</pre>

</details>

### 출처와 주의사항

<ul>
<li>공식 원본·공식 정답으로 검증되지 않은 복기본. 본문에서 문제 순서와 일부 내용의 부정확 가능성을 직접 고지함.</li>
<li>기말·교수는 파일명 근거; 2026-1은 본문에서도 확인.</li>
</ul>

- Source ID: `cp_2026_1_final_recall` · PDF 페이지: 4
- 사용자 제공 자료의 문제 발췌입니다. 현재 학기 시험 범위·출제 예고를 의미하지 않습니다.
