---
title: "2025-2 중간 Q1 - Mastering C Programming"
cssclasses: [exam-question]
description: 기출 문제 원문 미리보기 · 제공 정답 제외
---

문제 원문 · 제공 정답 제외. 이미지를 아래로 읽으면 전체 문항을 볼 수 있습니다.

<img src="assets/exam_questions/sp_2025_2_midterm_q01-01.png" width="1170" height="1261" alt="2025-2 중간 Q1 - Mastering C Programming 문제 원문 1/4 · PDF p.2" loading="eager" decoding="async">

<img src="assets/exam_questions/sp_2025_2_midterm_q01-02.png" width="1128" height="883" alt="2025-2 중간 Q1 - Mastering C Programming 문제 원문 2/4 · PDF p.3" loading="eager" decoding="async">

<img src="assets/exam_questions/sp_2025_2_midterm_q01-03.png" width="1128" height="440" alt="2025-2 중간 Q1 - Mastering C Programming 문제 원문 3/4 · PDF p.3" loading="eager" decoding="async">

<img src="assets/exam_questions/sp_2025_2_midterm_q01-04.png" width="1128" height="98" alt="2025-2 중간 Q1 - Mastering C Programming 문제 원문 4/4 · PDF p.4" loading="eager" decoding="async">

<details>
<summary>텍스트로 읽기 · 복사 / Read as text</summary>

<pre class="exam-question-text">Common assumptions: assume that the execution environment for all the code in the exam is 
sp01.snucse.org (64-bit OS with Intel CPU). Also, assume all header files are properly 
included for standard C library functions (e,g. printf(), etc.) 
 
1. (20 points) Mastering C Programming 
 
(a) (5 points) Let’s say the code below prints out “b=0x7ffd1819cca0” among other 
things. 
 
 
struct { 
 
int a; 
 
long b; 
 
int c; 
} x = { 1, 2, 3}; 
 
 
printf(“1=%ld\n”, sizeof(x)); 
printf(“2=%ld\n”, sizeof(&amp;x.a)); 
printf(“b=%p\n”, &amp;x.a); 
printf(“3=%p\n”, &amp;x.b); 
printf(“4=%d\n”, (int)*(char *)(&amp;x.a + 2)); 
*((char *)&amp;x + 17) = 1; 
printf(“5=%d\n”, x.c); 
 
What else does the code print out? Fill in the blanks. 
 
1=_____ 
 
2=_____ 
 
3=_____ 
 
4=_____ 
 
5=_____

(b) (5 points) What’s the output of this code snippet?  
 
int a[5] = {10, 20, 30, 40, 50}; 
int *p = a; 
int **q = &amp;p; 
 
p += 2; 
**q += 5; 
 
(*q)++; 
**q = **q + a[0]; 
 
int *r = a + 4; 
*(r - 1) = *p + **q; 
 
printf(&quot;%d %d %d %d %d\n&quot;, a[0], a[1], a[2], a[3], a[4]);

(c) (5 points) A stack grows downward on Intel CPUs, but it grows upward on other 
platforms (e.g., HP PA-RISC). The following function returns 1 if the stack grows 
downward when called as stack_grows_downward(NULL). Otherwise it 
returns 0. Fill in the blank.  
 
int stack_grows_downward(int *prev_addr)  
{ 
int current_var;  
if (prev_addr == NULL)   
return stack_grows_downward(&amp;current_var);   
return (____A____) ? 1: 0; 
}

(d) (5 point) List at least one advantage of alloca() over malloc() (3 point). List at least 
one limitation of it over malloc().</pre>

</details>

### 출처와 주의사항

<ul>
<li>제공된 정답 포함 자료에서 문제 영역만 분리했습니다. 공식 배포 여부와 정답 정확성은 검증하지 않았습니다.</li>
<li>원문은 64-bit Intel 실행 환경을 전제로 합니다. 메모리 배치·stack 방향을 모든 C 구현의 보장으로 일반화하지 마세요.</li>
</ul>

- Source ID: `sp_2025_2_midterm_answers` · PDF 페이지: 2, 3, 4
- 사용자 제공 자료의 문제 발췌입니다. 현재 학기 시험 범위·출제 예고를 의미하지 않습니다.
