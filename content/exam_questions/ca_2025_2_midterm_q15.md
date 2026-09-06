---
title: "2025-2 중간 복기 Q15 - Pipeline trace와 RAW hazard"
cssclasses: [exam-question]
description: 기출 문제 원문 미리보기 · 제공 정답 제외
---

문제 원문 · 제공 정답 제외. 이미지를 아래로 읽으면 전체 문항을 볼 수 있습니다.

<img src="assets/exam_questions/ca_2025_2_midterm_q15-01.png" width="1482" height="1473" alt="2025-2 중간 복기 Q15 - Pipeline trace와 RAW hazard 문제 원문 1/1 · PDF p.7" loading="eager" decoding="async">

<details>
<summary>텍스트로 읽기 · 복사 / Read as text</summary>

<pre class="exam-question-text">15. (15 points) Consider the following sequence of RISC-V instructions:

```riscv
I1: ld x5, 0(x10)
I2: addi x6, x5, 4
I3: sub x7, x6, x5
I4: sd x7, 8(x10)
```

(a) (5 pts) Identify all RAW (Read-After-Write) data hazards. For each, specify the two instructions and the register involved.

(b) (5 pts) Complete the following pipeline execution diagram for this code running on a 5-stage pipeline with full forwarding. If a stall is necessary, write “stall” in the corresponding cell.

| Clock Cycle | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | |
|---|---|---|---|---|---|---|---|---|---|
| I1: ld | IF | ID | EX | MEM | WB | | | | |
| I2: addi | | | | | | | | | |
| I3: sub | | | | | | | | | |
| I4: sd | | | | | | | | | |

(c) (5 pts) If the pipeline had no forwarding, how many total stall cycles would be required to resolve all hazards in this specific code sequence?</pre>

</details>

### 출처와 주의사항

<ul>
<li>실제 시험 기반 복기본이며 공식 원문·정답 정확성 미검증. 교수명은 파일명 근거.</li>
<li>I1 행의 IF·ID·EX·MEM·WB는 원문에 주어진 문제 데이터이며 제공 풀이를 추가한 것이 아님. 나머지 행은 원문대로 비워 둠.</li>
<li>원문 표는 cycle 1-8을 표시하고 오른쪽에 번호 없는 빈 공간이 더 있음. 번호 9나 후속 단계를 만들어 넣지 않았음.</li>
<li>동일 cycle WB와 ID 읽기 순서, store-data forwarding 경로 등 원문에 명시되지 않은 가정을 추가하지 않았음.</li>
</ul>

- Source ID: `ca_2025_2_midterm_recall` · PDF 페이지: 7
- 사용자 제공 자료의 문제 발췌입니다. 현재 학기 시험 범위·출제 예고를 의미하지 않습니다.
