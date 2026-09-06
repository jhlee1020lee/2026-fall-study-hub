---
title: "2025-1 중간 Q1 - Understanding C Pointers"
cssclasses: [exam-question]
description: 기출 문제 원문 미리보기 · 제공 정답 제외
---

문제 원문 · 제공 정답 제외. 이미지를 아래로 읽으면 전체 문항을 볼 수 있습니다.

<img src="assets/exam_questions/sp_2025_1_midterm_q01-01.png" width="1168" height="593" alt="2025-1 중간 Q1 - Understanding C Pointers 문제 원문 1/5 · PDF p.2" loading="eager" decoding="async">

<img src="assets/exam_questions/sp_2025_1_midterm_q01-02.png" width="1126" height="483" alt="2025-1 중간 Q1 - Understanding C Pointers 문제 원문 2/5 · PDF p.2" loading="eager" decoding="async">

<img src="assets/exam_questions/sp_2025_1_midterm_q01-03.png" width="1128" height="813" alt="2025-1 중간 Q1 - Understanding C Pointers 문제 원문 3/5 · PDF p.3" loading="eager" decoding="async">

<img src="assets/exam_questions/sp_2025_1_midterm_q01-04.png" width="1083" height="166" alt="2025-1 중간 Q1 - Understanding C Pointers 문제 원문 4/5 · PDF p.3" loading="eager" decoding="async">

<img src="assets/exam_questions/sp_2025_1_midterm_q01-05.png" width="631" height="305" alt="2025-1 중간 Q1 - Understanding C Pointers 문제 원문 5/5 · PDF p.4" loading="eager" decoding="async">

<details>
<summary>텍스트로 읽기 · 복사 / Read as text</summary>

<pre class="exam-question-text">Common assumptions: assume that the execution environment for all the code in the exam is 
sp01.snucse.org (64-bit OS with Intel CPU). Also, assume all header files are properly 
included for standard C library functions (e,g. printf(), etc.) 
 
1. (20 points) Understading C Pointers 
 
(a) (5 points) What’s the output of this code snippet? 
 
unsigned char a; 
int b; 
double c; 
char *d; 
 
printf(“1=%ld 2=%ld 3=%ld 4=%ld 5=%ld\n”, 
 
sizeof(a), sizeof(b),sizeof(c), 
 
sizeof(*d), sizeof(“hello”));

(b) (5 points) what’s the output of this code snippet?  
 
typedef struct {char a; long b; char c;} SR; 
 
SR (*k)[10], p[10] = {0}; 
 
printf(“1=%ld 2=%ld 3=%ld 4=%ld 5=%ld\n”,  
 
  sizeof(SR), sizeof(k), sizeof(p),  
 
  &amp;p[0].c – &amp;p[0].a,  
&amp;p[1].c – (char *)(&amp;p[0].b + 1));

(c) (5 points) Say we compile and run the code. 
1: const int a = 100;  
2: int main() { 
3:  
const int b = 200; 
4:    const char *c = “hello”; 
5:    static char *d = “world\n”; 
6:    *(char *)&amp;a = ‘1’; 
7:  
*(char *)&amp;b = ‘2’; 
8:  
*(char *)c = ‘3’; 
9:    *(char *)&amp;c = ‘4’; 
10:   *(char *)d = ‘5’; 
11: return 0; } 
The leftmost two characters of each line are line numbers and not part of the code.  
(1) List all line numbers that would generate memory access violation. In other words, 
which lines should be fixed to avoid any program crash? (5 pt)

(2) When you run the program, various program contents can be located in different 
memory sections such as text, BSS, read-only data section, read-write data section, 
stack, and heap sections. For each subproblem below, write the memory section 
that the content would belong to. (5pt)

Subproblem Progam content  
(a) 
a in line 1 
(b) 
b in line 3 
(c) 
d in line 5 
(d) 
The value, 200, in line 3 
(e) 
‘1’, ‘2’, ‘3’, ‘4’, ‘5’ in line 6-10</pre>

</details>

### 출처와 주의사항

<ul>
<li>제공된 정답 포함 자료에서 문제 영역만 분리했습니다. 공식 배포 여부와 정답 정확성은 검증하지 않았습니다.</li>
<li>(c)(2) 표의 답이 기입된 Memory section 열은 제외했습니다. 남은 각 항목에 해당하는 memory section을 답하는 문제입니다.</li>
<li>원문 코드의 따옴표·대시·배점·오탈자를 보존했습니다. C 표준의 undefined behavior와 특정 실행 환경의 관찰 결과를 구분해야 합니다.</li>
</ul>

- Source ID: `sp_2025_1_midterm_answers` · PDF 페이지: 2, 3, 4
- 사용자 제공 자료의 문제 발췌입니다. 현재 학기 시험 범위·출제 예고를 의미하지 않습니다.
