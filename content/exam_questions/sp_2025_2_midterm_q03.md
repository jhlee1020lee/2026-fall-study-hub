---
title: "2025-2 중간 Q3 - File System, Unix I/O, Standard I/O"
cssclasses: [exam-question]
description: 기출 문제 원문 미리보기 · 제공 정답 제외
---

문제 원문 · 제공 정답 제외. 이미지를 아래로 읽으면 전체 문항을 볼 수 있습니다.

<img src="assets/exam_questions/sp_2025_2_midterm_q03-01.png" width="1170" height="123" alt="2025-2 중간 Q3 - File System, Unix I/O, Standard I/O 문제 원문 1/6 · PDF p.2" loading="eager" decoding="async">

<img src="assets/exam_questions/sp_2025_2_midterm_q03-02.png" width="1173" height="166" alt="2025-2 중간 Q3 - File System, Unix I/O, Standard I/O 문제 원문 2/6 · PDF p.7" loading="eager" decoding="async">

<img src="assets/exam_questions/sp_2025_2_midterm_q03-03.png" width="1131" height="138" alt="2025-2 중간 Q3 - File System, Unix I/O, Standard I/O 문제 원문 3/6 · PDF p.7" loading="eager" decoding="async">

<img src="assets/exam_questions/sp_2025_2_midterm_q03-04.png" width="1131" height="555" alt="2025-2 중간 Q3 - File System, Unix I/O, Standard I/O 문제 원문 4/6 · PDF p.7" loading="eager" decoding="async">

<img src="assets/exam_questions/sp_2025_2_midterm_q03-05.png" width="1131" height="643" alt="2025-2 중간 Q3 - File System, Unix I/O, Standard I/O 문제 원문 5/6 · PDF p.8" loading="eager" decoding="async">

<img src="assets/exam_questions/sp_2025_2_midterm_q03-06.png" width="1131" height="178" alt="2025-2 중간 Q3 - File System, Unix I/O, Standard I/O 문제 원문 6/6 · PDF p.8" loading="eager" decoding="async">

<details>
<summary>텍스트로 읽기 · 복사 / Read as text</summary>

<pre class="exam-question-text">Common assumptions: assume that the execution environment for all the code in the exam is 
sp01.snucse.org (64-bit OS with Intel CPU). Also, assume all header files are properly 
included for standard C library functions (e,g. printf(), etc.)

3. (20 points) File System, UniX I/O, and Standard I/O 
(a) (4 points) An inode has a number of hard links but it does not have a number of soft 
links. Why?

(b) (4 points) Say a directory, X, has empty subdirectories, a, b, c, and no other files. 
When you run ‘ls -ld X’, what’s the number of hard links you would see in the 
output? Explain why.

(c) (4 points) Assume all system calls succeed.  
int fd1 = open(&quot;data.txt&quot;, O_CREAT | O_RDWR | O_TRUNC, 
0644); 
write(fd1, &quot;Exam is hard&quot;, 12); 
int fd2 = dup(fd1); 
lseek(fd2, 1, SEEK_SET); 
close (fd1); 
write(fd2, &quot;easy&quot;, 4); 
close (fd2); 
Explain what the code does. Be specific.

(d) (4points) We build two programs, a from a.c and b from b.c. Say, we have a 10GB 
textfile, 10GF, that is stored on disk.  
a.c
b.c
#include &lt;stdio.h&gt; 
int main() 
{ 
int c; 
while ((c = getchar()) != EOF) 
 
putchar (c); 
 return 0; 
}
#include &lt;stdio.h&gt; 
int main() 
{ 
char c; 
while ((read(0, &amp;c, 1)) &gt; 0) 
write(1, &amp;c, 1); 
return 0; 
}
 
$ time ./a &lt; 10GF 
$ time ./b &lt; 10GF 
Which one would shows a larger execution time? Explain the reason in detail.

(e) (4points) Explain the set-user-id (suid) privilege (1pt). List at least two well-known 
binaries (e.g., cat but cat doesn’t have the suid bit set) on Linux that require suid (2 
pts). Explain why the number of suid bianries should be minimized. Give a concrete 
secuirty risk with it (1pt).</pre>

</details>

### 출처와 주의사항

<ul>
<li>제공된 정답 포함 자료에서 문제 영역만 분리했습니다. 공식 배포 여부와 정답 정확성은 검증하지 않았습니다.</li>
<li>첫 이미지는 PDF 2쪽의 공통 실행 조건입니다. 문제는 PDF 7-8쪽이며 제공 답안은 포함하지 않습니다.</li>
<li>원문 코드·오탈자를 보존했습니다. (d)는 제시된 두 프로그램의 I/O 방식을 비교하는 문제입니다.</li>
</ul>

- Source ID: `sp_2025_2_midterm_answers` · PDF 페이지: 7, 8
- 사용자 제공 자료의 문제 발췌입니다. 현재 학기 시험 범위·출제 예고를 의미하지 않습니다.
