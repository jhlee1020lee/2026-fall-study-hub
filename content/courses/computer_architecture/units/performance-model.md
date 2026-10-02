---
title: "실행시간과 Performance 모형"
description: "Latency·CPU time·speedup·Amdahl의 상한을 계산한다."
course: "computer_architecture"
unit_id: "performance-model"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["lec 04.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_architecture/lectures/2026-09-15-lecture-05", "courses/computer_architecture/lectures/2026-09-29-lecture-05"]
---

성능을 비교하기 전에 작업량과 시간의 종류부터 정하자. 단위를 붙여 CPU 시간을 계산하고 바뀌지 않는 작업으로 개선의 한계를 점검한다.

## Latency와 throughput이 측정하는 것

Functional correctness(기능적 정확성)는 instruction을 specification대로 실행하는가의 문제이고, performance(성능)는 그 올바른 일을 얼마나 효율적으로 수행하는가의 문제이다. 둘을 구분한 뒤 어떤 작업을 어떤 지표로 측정할지 정해야 한다. [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 02:08]] [[courses/computer_architecture/lectures/2026-09-15-lecture-05|2026-09-15 강의 노트]]

Latency(지연시간)는 한 task가 시작해서 끝날 때까지 걸리는 시간이다. Network server의 한 요청 처리나 game의 keystroke 반응이 예이다. Throughput(처리량)은 단위 시간에 완료하는 task 수로, batch 처리와 여러 connection의 완료율에 중요하다. Bus와 race car의 비유도 한 번 이동하는 시간과 여러 승객을 운반하는 양을 구분한다. [CA M006 PDF p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-003) [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 05:26]]

설명용으로 한 요청이 1초 걸리는 processor 두 개가 서로 독립인 요청을 계속 처리한다고 하자. 각 요청의 latency는 여전히 1초지만 총 throughput은 초당 2요청이 될 수 있다. 이처럼 동시 실행이 있으면 일반적으로 throughput을 $1/latency$와 같다고 할 수 없다. Multicore가 한 작업의 latency를 자동으로 core 수만큼 나누지도 않는다. 반대로 병목 자원의 처리량 개선이 전체 작업의 시간에 영향을 줄 수 있으므로 두 지표가 완전히 무관한 것도 아니다. 9월 15일 08:19의 latency 증가·감소 방향은 불명확하며 여기서는 정의로 관계를 설명한다. [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 08:19]]

## Elapsed time과 CPU time

같은 작업량에서 $Performance=1/Time$으로 놓으면 짧은 시간이 높은 성능을 뜻한다. 하지만 먼저 어느 time인지 정해야 한다. Throughput으로 비교할 때도 작업량과 workload 조건을 맞춘다. [CA M006 PDF p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-004)

| 시간 항목 | 측정 의미 |
|---|---|
| Elapsed 또는 wall-clock time | 시작부터 종료까지 실제 경과 시간 |
| User CPU time | Program code를 실행한 CPU 시간 |
| System CPU time | 해당 program을 대신해 system code를 실행한 CPU 시간 |

[CA M006 PDF p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-005)의 terminal 화면은 같은 문자열을 계속 출력하는 `time yes hello` 예를 제시한다. 화면의 값은 Real 1.260 s, User 0.002 s, Sys 0.013 s이다. 따라서 CPU time은 $0.002+0.013=0.015$ s이고, elapsed와의 차이는 $1.260-0.015=1.245$ s이다.

9월 15일 13:07은 반복 terminal 출력의 I/O를 오래 걸리는 이유로 설명한다. 이 세 숫자만으로 1.245초의 모든 원인을 세부 분해한 것은 아니다. 또한 자료의 기존 출력을 읽은 것이며 이 명령을 새로 실행해 측정한 결과가 아니다. [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 13:07]] 측정값을 보고할 때는 CPU time인지 wall-clock time인지 밝히고, 자료가 권하는 unloaded system 같은 측정 조건도 함께 고려한다.

## Instruction count, CPI, clock period의 곱

Cycle은 processor의 clock 기준 간격이다. CPI는 cycles per instruction, IPC는 instructions per cycle, MIPS는 million instructions per second이다. 같은 실행에 대한 전체 수로 계산하면 CPI와 IPC는 서로 역수이다. GHz는 $10^9$ cycles/s이므로 그 자체가 instructions/s를 뜻하지 않는다.

CPU execution time의 식은 다음과 같다. [CA M006 PDF p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-006)

$$
T_{CPU}=IC\times CPI_{avg}\times T_{clk}
=\frac{IC\times CPI_{avg}}{f_{clk}}.
$$

단위를 소거하면 의미가 분명해진다.

$$
\frac{instructions}{program}
\times\frac{cycles}{instruction}
\times\frac{seconds}{cycle}
=\frac{seconds}{program}.
$$

설명용으로 $10^9$ instructions를 평균 CPI 2, clock 2 GHz에서 실행하면 $10^9\times2/(2\times10^9)=1$초이다. I/O 대기까지 이 식이 자동으로 계산하는 것은 아니다. $g$ GHz의 cycle time은 $1/(g\times10^9)$초이고, $m$ MIPS의 평균 instruction time은 $1/(m\times10^6)$초이다. 자료의 간략한 “1/GHz”, “1/MIPS” 표기에서는 이 배율을 복원해서 계산해야 한다.

### 세 항은 서로 다른 설계 선택의 영향을 받는다

Arithmetic, memory, branch instruction의 비용이 다르면 instruction mix에 따라 평균 CPI도 달라진다. 9월 15일 16:05는 register 중심 연산과 memory 접근 비용을 이 동기로 비교한다. 이를 모든 상황에서의 절대적인 속도 순위로 받아들일 필요는 없다. [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 16:05]]

| 식의 항 | 자료가 연결한 영향 |
|---|---|
| Clock frequency | Semiconductor technology, microarchitecture |
| CPI | Microarchitecture, ISA |
| IC | ISA, compiler |

같은 C source라도 compiler가 instruction 수와 memory 접근을 바꿀 수 있다. 같은 instruction sequence도 구현에 따라 CPI가 달라질 수 있다. 그러므로 GHz 하나나 source 줄 수만으로 실행시간을 판단하면 안 된다. 17:56의 “poor design”에서 CPI가 작아진다는 말은 식의 방향과 충돌한다. **같은 IC와 frequency에서 CPI 감소는 시간을 줄인다**는 것이 식으로 확인되는 설명이며 불확실한 말을 고친 STT 인용은 아니다. [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 17:56]]

복기 Q11(a–b)의 reasoning도 같은 식을 거꾸로 읽는 것이다. 시간과 주파수에서 총 cycle 수 $T f_{clk}$를 구하고 IC로 나누면 CPI이다. 목표 시간에 필요한 CPI는 $T_{target}f_{new}/IC$로 구한다. [EX:ca_2025_2_midterm_q11 p.3] 그 문서의 instruction count는 실제로 “200 billion”으로 인쇄되어 있으므로 그 규모를 임의로 고쳐 답을 맞추면 안 된다. 이 시험은 2025-2 복기본이며 공식 원문·정답은 독립 확인되지 않았다.

## Speedup과 시간 감소율

“X is $n$ times faster than Y”는 같은 일을 기준으로

$$
\frac{Performance_X}{Performance_Y}
=\frac{Time_Y}{Time_X}=n
$$

이라는 뜻이다. “$m\%$ faster”라면 성능 비율은 $1+m/100$이다. 분자와 분모를 먼저 정하면 시간이 얼마나 줄었는지와 성능이 얼마나 늘었는지를 구분할 수 있다. [CA M006 PDF p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-010)

자료 예에서 X가 1초 걸리고 Y가 X보다 50% faster이면 Y의 시간은 $1/1.5=2/3\approx0.66667$초이다. 0.5초는 시간이 50% 감소한 경우로 speedup은 2, 성능 증가는 100%이다. 9월 15일 27:22의 times에서 percent로 바꾼 설명은 이 구분과 연결되며 1.5라는 성능 비율에 seconds 단위를 붙이지 않는다. [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 27:22]]

Enhancement(개선)의 speedup도 $T_{old}/T_{new}$이다. 더 빨라진 version의 짧은 시간을 분모에 놓으므로 효과적인 개선은 1보다 큰 비율을 준다. 두 version이 하는 작업이 달라지면 이 비율만으로 같은 일을 얼마나 빨리 끝내는지 판단할 수 없다. [CA M006 PDF p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-011)

## Amdahl's Law와 바뀌지 않는 실행시간

전체 프로그램 중 일부만 개선하면 바뀌지 않는 부분이 남는다. 개선 **전** 실행시간에서 개선할 부분의 비중을 $f$, 그 부분의 speedup을 $S_f$라고 두자. [CA M006 PDF p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-012)의 위 막대는 $1-f$와 $f$로 나뉘고, 아래 막대에서는 $1-f$는 그대로이며 $f$만 $f/S_f$로 줄어든다.

$$
T_{new}=T_{old}\left((1-f)+\frac{f}{S_f}\right),
\qquad
S_{overall}=\frac{1}{(1-f)+f/S_f}.
$$

설명용 $f=0.8$, $S_f=4$를 넣으면 남는 시간 비율은 $0.2+0.8/4=0.4$, 전체 speedup은 2.5이다. 해당 부분을 무한히 빠르게 해도 나머지 0.2가 남으므로 상한은 5이다. 일반적으로 $f<1$일 때 상한은 $1/(1-f)$이다. 작은 부분만 개선하면 전체 효과가 제한된다는 뜻이지 $S_f$가 식에서 사라진다는 뜻은 아니다. [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 29:17]]

과거 Q6 및 Q11(c)와 연결되는 방법은 개선되지 않는 작업부터 계산하는 것이다. [EX:ca_2025_2_midterm_q06 p.2] [EX:ca_2025_2_midterm_q11 p.3] Instruction **개수 비중** $p$를 곧바로 실행시간 비중 $f$로 쓰면 안 된다. 개선하지 않는 instruction의 CPI가 $C_u$라면 그 부분만의 최소 CPU 시간은

$$
T_{unaffected}=\frac{IC(1-p)C_u}{f_{clk}}.
$$

목표가 이 값보다 짧다면 개선할 부분을 제거해도 달성할 수 없다. 그렇지 않은 경우에도 개선 대상의 기존 비용과 실현 가능한 개선 정도가 더 필요하다. 이 식은 CPU-time 관계에서 도출한 해설이며 비공개 시험의 완성 답안을 옮긴 것이 아니다.

9월 15일 30:18의 pipeline 언급과 9월 29일 51:38의 비어 있는 stage 활용 설명은 후속 설계의 동기이다. Pipeline이 개별 memory access의 latency를 반드시 줄인다는 법칙이나 세부 hazard 처리까지 배웠다는 뜻은 아니다. [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 30:18]] [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 51:38]]

## Energy와 power를 함께 읽기

실행시간이 짧다는 사실만으로 모든 평가 기준에서 좋은 processor가 되는 것은 아니다. 빨리 끝내기 위해 더 많은 energy를 쓰거나, 더 느리게 실행해 energy를 줄이는 trade-off가 있을 수 있다.

$$
Power_{avg}=\frac{Energy}{Time}.
$$

설명용으로 두 실행이 모두 10 J를 쓰되 하나는 1초, 다른 하나는 2초 걸리면 평균 power는 각각 10 W와 5 W이다. 더 낮은 power가 곧 더 적은 total energy라는 뜻은 아니다. Energy와 time의 함수를 평가 기준으로 삼거나 implementation cost, reliability, security를 함께 고려할 수 있다. [CA M006 PDF p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-007)

9월 15일 19:47은 무거운 workload에서 energy의 중요성을 동기로 들면서 이번 성능 분석의 중심을 time과 throughput에 두었다. 세부 energy model은 자료 수준의 소개이며 특정 브랜드의 일화를 검증된 효율 비교로 옮기지 않는다. [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 19:47]]

## 핵심 정리

- Throughput은 동시 실행에서 단순히 1/latency가 아니다.
- CPU time=IC×CPI/frequency이며 elapsed time과 구별한다.
- '50% faster'는 시간을 1/1.5로 줄이는 것이고 50% 시간 감소와 다르다.
- Amdahl의 f는 원래 시간의 비중이며 개선하지 않는 시간이 하한을 만든다.

## 확인·연습문제

### 개념 확인

#### 확인 Q01 · Correctness·latency·throughput

올바른 결과를 내지만 느린 processor는 어떤 기준을 만족하는가? 각 요청이 1초인 처리기 두 개가 독립 요청을 계속 받으면 latency와 throughput은 무엇이며 interactive/batch 작업에는 무엇이 중요한가?

<details><summary>해설 보기</summary>

Specification대로 실행하면 functional correctness는 만족한다. 각 요청 latency는 1초, 이상적인 총 throughput은 2 requests/s이다. Interactive 반응은 개별 latency, batch 처리량은 완료율이 중요하다. 동시 실행 때문에 throughput≠1/latency일 수 있고 추가 core가 한 작업을 자동으로 나누지 않는다. 다만 병목 component의 처리율이 바뀌면 전체 latency도 영향을 받을 수 있어 두 지표가 완전히 무관하지는 않다.

**채점·확인:** 요청 한 개와 전체 완료율의 단위를 구별한다.

</details>

#### 확인 Q02 · 실제 경과와 CPU 사용

자료의 `time yes hello` 출력 Real=1.260 s, User=0.002 s, Sys=0.013 s에서 CPU time과 차이를 구하라. 이를 무엇까지 해석할 수 있으며 성능 비교 전에 어떤 조건을 맞춰야 하는가?

<details><summary>해설 보기</summary>

CPU time=0.002+0.013=0.015 s, 차이는 1.245 s이다. User는 program code, system은 해당 program을 대신하는 system code, elapsed는 실제 시작→종료 시간이다. 강의는 반복 출력 I/O를 이유로 설명하지만 세 수치만으로 차이의 모든 원인을 분해하지 못한다. 동일 작업·workload와 측정 종류를 명시하고 자료의 unloaded-system 조건도 고려해야 Performance=1/Time 비교가 의미 있다. 이 값은 기존 출력이며 새 실행 결과가 아니다.

**채점·확인:** 차이를 전부 특정 대기 원인으로 단정하지 않는다.

</details>

#### 확인 Q03 · IC·CPI·clock 계산

IC=10^9, CPI=2, clock=2 GHz의 CPU time·cycle period·IPC·MIPS를 구하라. Compiler·ISA·microarchitecture·기술이 식의 어떤 항에 영향을 주는가?

<details><summary>해설 보기</summary>

T=10^9×2/(2×10^9)=1 s, period=0.5 ns, IPC=1/2=0.5, rate=10^9 instructions/s=1000 MIPS이다. Instructions×cycles/instruction×seconds/cycle에서 cycles가 소거된다. Frequency는 기술·microarchitecture, CPI는 microarchitecture·ISA, IC는 ISA·compiler 영향을 받는다. Instruction mix도 CPI를 바꾼다. GHz는 cycles/s이며 instructions/s가 아니다. 같은 IC·frequency에서 낮은 CPI가 더 짧은 시간을 주고 I/O 대기는 이 CPU 식에 자동 포함되지 않는다.

**채점·확인:** 10^9·10^6 배율과 CPI/IPC의 같은 실행 조건을 확인한다.

</details>

#### 확인 Q04 · Energy와 power

동일한 일을 하는 두 실행이 각각 10 J를 쓰고 1초·2초 걸린다. 평균 power를 구하고 낮은 power·짧은 time만으로 우열을 정할 수 없는 이유를 설명하라.

<details><summary>해설 보기</summary>

P=E/T로 10 W와 5 W이다. 두 번째는 power가 낮지만 energy가 같고 latency는 길다. 더 많은 energy로 시간을 줄이거나 반대로 시간을 양보하는 trade-off가 가능하다. 목적에 따라 energy와 time의 함수, implementation cost·reliability·security도 평가한다. 여기서 세부 energy 모델이나 브랜드별 효율을 측정한 것은 아니다.

**채점·확인:** J와 W를 구별하고 동일 energy가 동일 power는 아님을 보인다.

</details>

#### 확인 Q05 · Faster와 시간 감소

기준 실행 1초에 대해 50% faster인 실행과 50% 시간 감소인 실행을 비교하라. 각 time·speedup·성능 증가율을 구하라.

<details><summary>해설 보기</summary>

50% faster는 성능 비율 1.5이므로 time=1/1.5=2/3 s, speedup=1.5, 시간 감소 약 33.33%이다. 시간 50% 감소는 0.5 s, speedup=1/0.5=2, 성능 증가 100%이다. Speedup은 같은 작업의 old/new time이며 비율 1.5에 seconds를 붙이지 않는다.

**채점·확인:** 분자·분모와 서로 다른 두 백분율을 확인한다.

</details>

#### 확인 Q06 · Amdahl 식과 상한

원래 시간의 f를 S_f배 빠르게 할 때 전체 speedup을 유도하라. f=0.8, S_f=4와 f=0.1의 무한 개선 상한을 계산하라.

<details><summary>해설 보기</summary>

원래 시간을 1로 두면 안 바뀌는 1−f와 줄어든 f/S_f가 남아 S=1/((1−f)+f/S_f)이다. 첫 경우 1/(0.2+0.8/4)=2.5이고 해당 f의 상한은 1/0.2=5이다. f=0.1이면 상한은 1/0.9≈1.111이다. f는 개선 전 시간 비중이며 작은 부분의 효과가 제한된다는 말이 S_f를 식에서 지운다는 뜻은 아니다.

**채점·확인:** 개선 전 비중, unchanged 항, 무한 개선의 극한을 포함한다.

</details>

#### 확인 Q07 · 개수 비중과 시간 비중

Instruction의 20%가 개선 대상이라는 정보만으로 Amdahl의 f=0.2라 할 수 있는가? 총 IC, 미개선 CPI=C_u, 대상 개수 비중 p, clock f_clk로 미개선 시간 하한과 목표 CPI를 써라.

<details><summary>해설 보기</summary>

Instruction별 비용이 다를 수 있어 개수 비중은 시간 비중이 아니다. 미개선 cycles=IC(1−p)C_u, 시간=IC(1−p)C_u/f_clk이다. 목표 시간이 이보다 짧으면 개선 대상 시간을 0으로 해도 불가능하다. 목표 평균 CPI는 T_target f_clk/IC이다. 하한보다 길다는 것만으로 실현 가능성이 확정되지는 않고 대상의 원래 비용과 가능한 개선이 더 필요하다.

**채점·확인:** 개수에서 cycles를 거쳐 시간으로 계산한다.

</details>

### 적용 연습

#### 연습 P01 · 개선안 선택과 불가능한 목표

새로 만든 합성 연습이다. 같은 8천만 instruction 실행에서 FP가 개수의 25%, CPI 4이고 나머지는 CPI 1이다. Clock은 2 GHz이다. A안은 FP만 4배 빠르게 하고 B안은 CPI·IC 그대로 2.8 GHz로 바꾼다. 기존 시간, 각 안의 시간·speedup을 구하고 FP만 개선해 0.025 s 또는 0.04 s를 달성할 수 있는지 판단하라.

연결: [EX:ca_2025_2_midterm_q11 p.3] (a–c)의 식 역산·미개선 하한과 [EX:ca_2025_2_midterm_q06 p.2]의 부분 개선 한계를 비교 의사결정으로 옮겼다. 선수는 Q03·Q05–Q07이다. 원문에 인쇄된 200 billion은 그대로 두며 이 문제의 수치·설계 선택은 새로 썼다.

<details><summary>해설 보기</summary>

기존 cycles=2천만×4+6천만×1=1억4천만, time=0.07 s이다. FP 시간은 0.04 s여서 시간 비중은 4/7이지 1/4이 아니다. A는 0.04/4+0.03=0.04 s, speedup=1.75; B는 1.4×10^8/(2.8×10^9)=0.05 s, speedup=1.4이다. 이 조건에서는 A가 더 짧다. 미개선 시간 0.03 s가 남으므로 0.025 s는 불가능하다. 그 목표 CPI=0.025×2×10^9/(8×10^7)=0.625인데 미개선 기여만 0.75이다. 0.04 s에는 FP 몫 0.01 s가 허용되어 0.04/0.01=4배가 필요하다. Energy·비용은 주어지지 않았으므로 전체 설계 우열까지 정하지 않는다.

**채점·확인:** Count/time 비중, 두 개선안, 두 목표의 가능성을 각각 검산한다.

</details>

### 짧은 복습 계획

Q02·Q03의 단위와 시간 종류를 먼저 점검한 뒤 Q05–Q07을 풀자. P01에서는 목표 가능성을 먼저 판단하고 필요한 speedup을 계산하는 순서를 다시 연습하자.

## 출처

- [[courses/computer_architecture/lectures/2026-09-15-lecture-05|2026-09-15 강의 노트]]
- [[courses/computer_architecture/lectures/2026-09-29-lecture-05|2026-09-29 강의 노트 · pipeline 동기 예고]]
- [lec 04.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.04.pdf) — [p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-003), [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-004), [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-005), [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-006), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-007), [p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-010), [p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-011), [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.04/page-012)
- [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 보정 STT]] — 02:08, 05:26, 08:19, 13:07, 16:05, 17:56, 19:47, 27:22, 29:17, 30:18 (페이지 안의 시간 표기)
- [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 보정 STT]] — 51:38 (페이지 안의 시간 표기)

주된 근거는 9월 15일 강의와 자료다. 08:19의 latency 방향, 17:56의 CPI 방향, 27:22의 단위 불명확성은 정의·식으로 구별하며 발화를 복원하지 않는다. 9월 29일 연결은 idle-stage 활용의 예고만 보강하고 세부 pipeline이나 개별 memory latency 개선을 입증하지 않는다. Energy는 개요이고 제품 일화는 비교 증거가 아니다.

시험 연결은 2025-2 복기본에 한정되며 공식 원문·정답은 독립 확인되지 않았다. 제공 답안은 검증된 정답으로 채택하지 않았고 과거 채점 규칙·출제 가능성을 현 학기로 옮기지 않는다.
선택한 reasoning 연결: [EX:ca_2025_2_midterm_q06 p.2], [EX:ca_2025_2_midterm_q11 p.3].
- [[exam_questions/ca_2025_2_midterm_q11|2025-2 중간 복기 Q11 · 기존 문제 미리보기]]
복기 Q11의 IC는 원문에 200 billion으로 인쇄되어 있으며 임의로 규모를 바꾸지 않는다.
