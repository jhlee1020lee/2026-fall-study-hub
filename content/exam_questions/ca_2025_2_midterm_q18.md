---
title: "2025-2 중간 복기 Q18 - Atomic instruction과 semaphore P operation"
cssclasses: [exam-question]
description: 기출 문제 원문 미리보기 · 제공 정답 제외
---

문제 원문 · 제공 정답 제외. 이미지를 아래로 읽으면 전체 문항을 볼 수 있습니다.

<img src="assets/exam_questions/ca_2025_2_midterm_q18-01.png" width="1425" height="1248" alt="2025-2 중간 복기 Q18 - Atomic instruction과 semaphore P operation 문제 원문 1/1 · PDF p.9" loading="eager" decoding="async">

<details>
<summary>텍스트로 읽기 · 복사 / Read as text</summary>

<pre class="exam-question-text">18. (15 points) In multi-core processors, different threads often need to modify a shared variable, requiring atomic operations to prevent data corruption. RISC-V provides lr.w rd, (rs1) (load-reserved) and sc.w rd, rs2, (rs1) (store-conditional) for this.

- lr.w rd, (rs1): Loads a word from the address in rs1 into rd and places a reservation on that memory address.
- sc.w rd, rs2, (rs1): Attempts to store the word from rs2 to the address in rs1. It succeeds (and writes 0 to rd) only if the reservation is still valid. It fails (and writes a non-zero value to rd) if another core modified the memory location in the meantime.

A “counting semaphore” is a shared integer used to control access to a resource. A thread must perform a P (“wait”) operation on the semaphore before accessing the resource. The P operation is defined as:

1. Atomically check the semaphore’s value.
2. If the value is greater than zero, decrement it by one. The operation is then complete.
3. If the value is zero, the thread must wait (or “spin”) until the value becomes greater than zero before trying again.

Task: Write a RISC-V assembly snippet that correctly implements the P operation. Assume the address of the semaphore is in register x10. You may use x11 and x12 as temporary registers.</pre>

</details>

### 출처와 주의사항

<ul>
<li>실제 시험 기반 복기본이며 공식 원문·정답 정확성 미검증. 교수명은 파일명 근거.</li>
<li>복기본의 reservation 설명은 단순화되어 있으며 실제 ISA의 실패 조건 전체를 보장하지 않음.</li>
<li>일반적인 동기화 correctness에는 memory ordering 가정도 별도로 필요하며, 여기서는 원문에 없는 가정을 추가하지 않았음.</li>
</ul>

- Source ID: `ca_2025_2_midterm_recall` · PDF 페이지: 9
- 사용자 제공 자료의 문제 발췌입니다. 현재 학기 시험 범위·출제 예고를 의미하지 않습니다.
