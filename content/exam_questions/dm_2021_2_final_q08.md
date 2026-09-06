---
title: "2021-2 기말 Q8"
cssclasses: [exam-question]
description: 기출 문제 원문 미리보기 · 제공 정답 제외
---

문제 원문 · 제공 정답 제외. 이미지를 아래로 읽으면 전체 문항을 볼 수 있습니다.

<img src="assets/exam_questions/dm_2021_2_final_q08-01.png" width="1170" height="595" alt="2021-2 기말 Q8 문제 원문 1/1 · PDF p.2" loading="eager" decoding="async">

<details>
<summary>텍스트로 읽기 · 복사 / Read as text</summary>

<pre class="exam-question-text">Question 8. (10+15 points) Dynamic programming can be used to develop an algorithm for solving the matrix-chain multiplication problem of determining how the product A₁A₂…A_n can be computed using the fewest integer multiplications, where A₁, A₂, …, A_n are m₁ × m₂, m₂ × m₃, …, m_n × m_{n+1} matrices, respectively, and each matrix has integer entries.

1. Denote by A_{i,j} the product A_i A_{i+1}…A_j, and M(i, j) the minimum number of integer multiplications required to find A_{i,j}, where i ≤ j. Construct a recurrence relation of M(i, j).
[Hint: if the least number of integer multiplications are used to compute A_{i,j} by splitting the product into the product of A_i through A_k and the product of A_{k+1} through A_j, then A_{i,k} and A_{k+1,j} must be parenthesized so that both are computed in the optimal ways.]

2. Use the recurrence relation to devise an efficient algorithm for determining the order the n matrices should be multiplied to use the minimum number of integer multiplications. What is the worse-case complexity of your algorithm in terms of multiplications of integers?
[Hint: store the partial results M(i, j) as you find them so that your algorithm will not have exponential complexity.]</pre>

</details>

### 출처와 주의사항

<ul>
<li>두 Hint는 문제에 인쇄된 출제 지시문이다. 새 풀이를 추가하지 않았다.</li>
<li>원문의 worse-case 표기를 보존했다.</li>
</ul>

- Source ID: `dm_2021_2_final` · PDF 페이지: 2
- 사용자 제공 자료의 문제 발췌입니다. 현재 학기 시험 범위·출제 예고를 의미하지 않습니다.
