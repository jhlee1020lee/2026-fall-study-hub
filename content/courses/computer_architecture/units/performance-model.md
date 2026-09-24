---
title: "실행시간과 Performance 모형"
description: "Latency·CPU time·speedup과 Amdahl의 한계로 성능 주장을 계산한다."
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
source_lectures: ["courses/computer_architecture/lectures/2026-09-15-lecture-05"]
---

동일한 올바른 작업을 어떤 시간·처리량으로 비교하는지 먼저 정한다. IC·CPI·clock의 단위를 맞추고 개선되지 않는 시간을 따로 계산하면 빠르다는 주장과 부분 최적화 목표를 검증할 수 있다.

## Functional correctness와 Latency·Throughput

Processor가 빠르기 전에 충족해야 할 조건은 instruction을 명세대로 실행하는 functional correctness(기능적 정확성)다. Performance(성능)는 그 올바른 작업을 얼마나 효율적으로 수행하는지 평가한다. [ISA와 구현의 구분](architecture-contract.md)을 바탕으로, 같은 기능을 구현한 machine 사이에서도 어떤 성능 지표를 비교하는지 정해야 한다. [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 02:08]]

Latency(지연시간)는 한 task의 시작부터 완료까지의 시간이다. Game에서 입력에 반응하기까지의 시간이나 server의 한 요청 처리시간이 예다. Throughput(처리량)은 단위 시간에 완료한 task 수이며 batch 작업이나 여러 server connection을 함께 처리할 때 중요하다. Bus와 race car의 비유도 한 번 이동하는 시간과 운반하는 승객 수를 나누어 보게 한다. [[page_cache/computer_architecture/lec.04/page-003|CA M006 p.3]]

Concurrency(동시성)가 있으면 throughput을 단순히 `1/latency`로 놓을 수 없다. 설명용으로 독립적인 두 처리기가 각각 한 작업에 1초를 쓰고 계속 작업을 공급받는다면, 한 작업의 service latency는 1초이고 전체 throughput은 초당 2개다. 여러 core를 늘리는 것이 한 작업의 실행시간까지 같은 비율로 줄인다는 결론은 나오지 않는다. 그렇다고 두 지표가 완전히 무관하지도 않다. 병목 구성요소를 개선하면 전체 완료시간도 달라질 수 있다. [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 05:26]] 08:19의 latency 증가·감소 방향은 불명확하므로 위 정의를 그 발화의 복원으로 제시하지 않는다.

## Elapsed time과 CPU time

동일한 일을 수행하는 시간을 비교할 때 `Performance=1/Time`으로 두면 시간이 짧을수록 성능이 크다. 그러나 먼저 **어느 시간인지** 정해야 한다. Unix `time` 예제는 세 값을 구분한다.

| 지표 | 측정하는 시간 | 자료의 값 |
|---|---|---|
| Elapsed 또는 wall-clock time | 시작부터 종료까지 실제 경과 | 1.260 s |
| User CPU time | Program code를 실행한 CPU 시간 | 0.002 s |
| System CPU time | 해당 program을 위해 system code를 실행한 CPU 시간 | 0.013 s |

[[page_cache/computer_architecture/lec.04/page-005|CA M006 p.5]]의 terminal 출력에서 CPU time은 `0.002+0.013=0.015 s`다. Elapsed와의 차이는 `1.260−0.015=1.245 s`다. 강의는 반복 terminal 출력에 필요한 I/O 때문에 실제 경과 시간이 CPU 시간보다 훨씬 긴 예라고 설명했다. [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 13:07]]

이 세 숫자만으로 차이의 모든 원인을 정확히 분해할 수는 없다. 적어도 1.260초 전부를 CPU가 계산한 시간으로 해석하면 틀린다는 것을 알 수 있다. 측정에는 대상·환경을 함께 밝혀야 하며 자료는 다른 부하가 없는 환경에서 wall-clock time을 측정하도록 안내한다.

## IC·CPI·Clock으로 CPU execution time 구성하기

Instruction count(IC, 실행 명령어 수)는 실제로 실행한 instruction 수다. CPI(cycles per instruction, 명령어당 사이클 수)는 한 instruction에 사용한 평균 cycle 수이고, IPC(instructions per cycle, 사이클당 명령어 수)는 그 같은 집계의 역수다. Clock frequency(클록 주파수)는 초당 cycle 수다.

$$
T_{\mathrm{CPU}}=IC\times CPI\times t_{\mathrm{cycle}}
=\frac{IC\times CPI}{f_{\mathrm{clock}}}.
$$

단위를 곱하면 식의 뜻이 드러난다.

$$
\frac{\mathrm{instructions}}{\mathrm{program}}
\times\frac{\mathrm{cycles}}{\mathrm{instruction}}
\times\frac{\mathrm{seconds}}{\mathrm{cycle}}
=\frac{\mathrm{seconds}}{\mathrm{program}}.
$$

설명용으로 `10^9` instructions, CPI=2, frequency=2 GHz라면 `10^9×2/(2×10^9)=1 s`다. 이는 CPU execution time 모형의 결과이며 I/O 대기까지 자동으로 포함한 elapsed time은 아니다.

GHz는 `10^9 cycles/s`, MIPS는 `10^6 instructions/s`다. 따라서 `g GHz`의 cycle time은 `1/(g×10^9) s`이고, `m MIPS`의 평균 instruction time은 `1/(m×10^6) s`다. [[page_cache/computer_architecture/lec.04/page-006|CA M006 p.6]]의 `1/GHz`와 `1/MIPS` 표기는 이 배율을 생략한 약식이며 초 단위 계산에서는 반드시 복원해야 한다.

| 시간식의 인자 | 자료가 연결하는 영향 |
|---|---|
| Frequency | Semiconductor technology, microarchitecture |
| CPI | Microarchitecture, ISA |
| IC | ISA, compiler |

Arithmetic, memory, branch의 비용은 다를 수 있으므로 instruction mix(명령어 구성비)가 평균 CPI에 영향을 준다. 같은 source도 compiler가 다른 IC를 만들 수 있고, 같은 sequence도 다른 구현에서 다른 CPI를 가질 수 있다. 그래서 GHz 하나나 source 줄 수로 실행시간을 결정할 수 없다. [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 16:05–18:54]] 17:56의 나쁜 설계에서 CPI가 “smaller”라는 불명확한 표현은 식의 방향과 충돌한다. 같은 IC·frequency에서 CPI가 작아지면 시간이 줄어든다는 설명은 위 식으로 확인한 정정이다.

복기 Q11(a–b)처럼 시간을 알고 요구 CPI를 구할 때도 새 공식을 외울 필요가 없다. `CPI=T×f_clock/IC`로 정리하고 단위가 cycles/instruction인지 확인하면 된다. 인쇄된 수를 익숙한 규모로 임의 수정하지 않는 것도 계산의 일부다. 이 복기 자료는 공식 원문·답안으로 확인된 것은 아니다. [EX:ca_2025_2_midterm_q11 p.3]

## Time·Energy·Power의 서로 다른 비교

짧은 실행시간만으로 모든 면에서 더 좋은 processor라고 말할 수는 없다. 더 많은 energy(에너지)를 사용해 빨리 끝낼 수도 있고, 느리게 실행하여 energy를 줄일 수도 있다. 평균 power(전력)는 다음과 같다.

$$
P_{\mathrm{avg}}=\frac{E}{T}.
$$

설명용으로 같은 60 J를 10초에 쓰면 평균 6 W, 5초에 쓰면 12 W다. 시간은 절반이지만 total energy는 같고 평균 power는 두 배다. 서로 다른 세 수치를 하나로 섞지 않아야 한다. 자료는 energy와 time을 함께 고려하는 평가, implementation cost, reliability, security도 소개한다. [[page_cache/computer_architecture/lec.04/page-007|CA M006 p.7]]

이는 비교 기준을 넓히는 자료 기반 배경이다. 강의의 주된 분석은 time과 throughput이며 세부 energy model을 전개한 것은 아니다. [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 19:47]]

## Speedup과 “50% faster”의 방향

동일한 작업에 대해 “X가 Y보다 n배 빠르다”는 것은:

$$
\frac{Performance_X}{Performance_Y}
=\frac{T_Y}{T_X}=n.
$$

“m% faster”는 이 성능 비율이 `1+m/100`이라는 뜻이다. 자료처럼 X가 1초 걸리고 Y가 X보다 50% faster이면:

$$
T_Y=\frac{1}{1.5}\ \mathrm{s}\approx0.66667\ \mathrm{s}.
$$

0.5초가 아니다. 0.5초라면 시간은 50% 감소했지만 성능은 2배, 즉 100% 증가한 것이다. [[page_cache/computer_architecture/lec.04/page-010|CA M006 p.10]] [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 27:22]]

개선 전후의 speedup(속도 향상 배수)도 `T_old/T_new`다. 개선되었다면 분모가 더 작아 1보다 크다. 같은 1.5라는 수라도 성능의 배수는 단위가 없고 실행시간은 초 단위다. STT에서 비율과 시간을 혼용한 불명확한 부분을 그대로 수치 규칙으로 채택하면 안 된다.

## Amdahl's Law와 개선되지 않는 시간

전체 프로그램 중 일부만 빨라질 때는 그 부분이 원래 얼마나 오래 걸렸는지가 중요하다. 개선 전 시간 중 해당 부분의 비중을 `f`, 그 부분의 speedup을 `S_f`라 하자.

![개선 전후에 변하지 않는 부분과 짧아지는 부분을 나눈 Amdahl 도표](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/computer_architecture/lec.04/page-012.png)

[[page_cache/computer_architecture/lec.04/page-012|CA M006 p.12]]의 위 막대는 `1−f`와 `f`로 나뉜다. 아래 막대에서 왼쪽 `1−f`는 그대로이고 오른쪽만 `f/S_f`로 줄어든다. 따라서:

$$
T_{\mathrm{new}}=T_{\mathrm{old}}\left((1-f)+\frac{f}{S_f}\right),
\qquad
S_{\mathrm{overall}}=\frac{1}{(1-f)+f/S_f}.
$$

자료의 식을 적용한 설명용 계산으로 `f=0.8`, `S_f=4`이면 남는 시간 비율은 `0.2+0.8/4=0.4`, 전체 speedup은 2.5다. 해당 부분이 무한히 빨라져도 `f<1`이면:

$$
S_{\mathrm{overall}}\le\frac{1}{1-f}
$$

이 예의 상한은 5다. 제거할 수 없는 20%가 남기 때문이다. 반대로 10%만 제거할 수 있으면 상한은 `1/0.9≈1.11`이다. “Make the common case fast”는 전체 시간의 큰 부분을 개선하라는 뜻이지, 작은 `f`에서 `S_f`가 수학적으로 식에서 사라진다는 뜻은 아니다. [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 29:17]] 복기 Q6도 부분 개선과 전체 효과를 구분하도록 요구한다. [EX:ca_2025_2_midterm_q06 p.2]

### Instruction-count 비중을 시간 비중으로 바꾸기

Amdahl의 `f`는 **개선 전 실행시간 비중**이다. 어떤 instruction 종류가 전체 개수의 `q`를 차지하더라도 instruction당 비용이 다르면 시간 비중은 `q`가 아니다. 두 종류의 CPI를 `c_a,c_b`라 하면 같은 clock 아래:

$$
f=\frac{q\,c_a}{q\,c_a+(1-q)c_b}.
$$

또 개선하지 않는 종류만으로 필요한 시간이:

$$
T_{\mathrm{unaffected}}=\frac{IC(1-q)c_b}{f_{\mathrm{clock}}}
$$

이므로, 이 값이 목표 시간보다 크면 다른 종류를 아무리 빨리 해도 목표를 달성할 수 없다. 먼저 하한을 확인하면 존재하지 않는 개선 배수를 찾는 오류를 피한다. 복기 Q11(c)에서 가져오는 추론의 깊이가 이 구분이며, floating-point 연산의 상세 구현을 새 선수범위로 요구하는 것은 아니다. [EX:ca_2025_2_midterm_q11 p.3] Weight가 무엇의 비중인지 따지는 원칙은 [workload와 평균](performance-comparison.md)에서도 그대로 이어진다.

## 핵심 정리

- Functional correctness를 만족한 같은 작업을 같은 지표로 비교한다.
- Elapsed time은 user+system CPU time과 다를 수 있다.
- CPU time=`IC×CPI/frequency`이며 GHz·MIPS의 배율을 복원해야 한다.
- '50% faster'는 시간 50% 감소가 아니라 성능 비율 1.5다.
- Amdahl의 비중은 원래 시간 비중이다. 고정된 나머지 시간이 목표를 넘으면 부분 개선만으로 달성할 수 없다.

## 확인·연습문제

### 개념 확인과 추적

#### 확인 Q01 · 올바른 작업과 두 성능 지표

기능적으로 틀린 결과를 더 빨리 내는 processor를 올바른 작업의 성능 향상이라고 할 수 있는가? 두 독립 처리기가 각각 한 요청에 1초를 쓰고 작업이 계속 공급될 때 latency·throughput을 구하고 서로 역수인지 설명하라.

<details><summary>해설 보기</summary>

먼저 ISA가 정한 결과를 내는 functional correctness가 필요하므로 잘못된 결과는 동일한 올바른 작업의 비교가 아니다. 각 요청의 service latency는 1초, aggregate throughput은 2 requests/s다. 동시 작업 때문에 `1/latency=1/s`와 다르다. Core 추가가 한 작업 시간을 자동으로 줄이지는 않지만 병목 변화가 전체 지연에 영향을 줄 수도 있어 두 지표가 완전히 무관한 것도 아니다.

**채점·확인 기준:** 정확성 전제·1초·2/s와 concurrency 조건을 모두 명시한다.

</details>

#### 확인 Q02 · 측정한 시간의 종류

자료의 Real=1.260 s, User=0.002 s, Sys=0.013 s에서 CPU time과 차이를 구하라. 각 counter의 의미와 차이 전체를 하나의 원인으로 단정할 수 없는 이유를 설명하라.

<details><summary>해설 보기</summary>

CPU time은 `0.002+0.013=0.015 s`, 차이는 `1.260−0.015=1.245 s`다. Real은 경과, User는 program code, Sys는 program을 위한 system code의 CPU 시간이다. 강의의 terminal 출력은 I/O가 큰 예이지만 세 counter가 각 대기 원인을 모두 측정하지는 않는다. 보고할 때 시간 종류·workload·환경을 밝히고 자료의 unloaded 측정 조건도 함께 생각해야 한다.

**채점·확인 기준:** 두 계산·세 정의와 원인 해석 한계를 확인한다.

</details>

#### 확인 Q03 · 단위로 시간식 복원하기

IC=`10^9`, CPI=2, clock=2 GHz의 CPU time·cycle time·IPC를 구하라. 500 MIPS의 평균 instruction time과, 같은 IC·clock에서 목표 0.75초에 필요한 CPI도 계산하라.

<details><summary>해설 보기</summary>

총 cycle은 `2×10^9`, time은 `2×10^9/(2×10^9)=1 s`, cycle time은 `1/(2×10^9)=0.5 ns`, IPC는 `1/2=0.5`다. 500 MIPS는 `500×10^6 instructions/s`여서 2 ns/instruction이다. 목표 CPI=`0.75×2×10^9/10^9=1.5 cycles/instruction`이다. `instructions×cycles/instruction÷cycles/second`가 seconds가 되며 이 CPU 모형이 I/O 대기까지 포함하지는 않는다.

**채점·확인 기준:** GHz/MIPS 배율·역수·역산 단위와 CPU/elapsed 범위를 확인한다.

</details>

#### 확인 Q04 · GHz만으로 비교할 수 없는 이유

CPU time의 세 인자에 compiler·ISA·microarchitecture·반도체 기술이 어떻게 연결되는가? 같은 clock에서 compiler가 IC를 줄이거나 instruction mix가 바뀌는 경우, 작은 CPI의 의미를 설명하라.

<details><summary>해설 보기</summary>

자료는 IC에 ISA·compiler, CPI에 microarchitecture·ISA, frequency에 기술·microarchitecture를 연결한다. Compiler는 다른 sequence를 만들어 IC와 mix를 바꿀 수 있고, 비용이 다른 instruction 비중이 변하면 평균 CPI도 달라진다. 같은 IC·frequency에서 작은 CPI는 시간을 줄이지만 세 인자가 함께 바뀌면 곱과 나눗셈 전체를 계산해야 한다. Source 줄 수와 GHz 하나는 그 정보를 주지 않는다.

**채점·확인 기준:** 세 인자의 영향과 '나머지 고정' 조건을 명확히 쓴다.

</details>

#### 확인 Q05 · Energy와 Power

두 실행이 모두 60 J를 쓰고 각각 10초와 5초 걸린다. 평균 power·total energy·time을 비교하고 더 짧은 time만으로 모든 평가 기준에서 우세하다고 할 수 있는지 설명하라.

<details><summary>해설 보기</summary>

평균은 각각 `60/10=6 W`, `60/5=12 W`다. Time은 절반, energy는 같고 power는 두 배이므로 세 지표가 다르다. 더 적은 energy를 위해 느리게 실행할 수도 있고 cost·reliability·security도 기준이다. 여기의 식은 평균 관계이며 세부 energy model이나 모든 우열을 정하지 않는다.

**채점·확인 기준:** J·s·W 단위와 세 비교 결과를 확인한다.

</details>

#### 확인 Q06 · Faster와 시간 감소

1초 작업에 대해 50% faster의 새 시간과, 새 시간이 0.5초일 때 speedup·성능 증가율·시간 감소율을 비교하라.

<details><summary>해설 보기</summary>

50% faster는 성능 비율 1.5이므로 `Tnew=1/1.5=2/3 s`다. 0.5초라면 speedup=`1/0.5=2`, 성능 증가율 `(2−1)×100=100%`, 시간 감소율 `(1−0.5)/1=50%`다. 성능 비율은 무차원이고 시간은 초이며, 같은 일을 비교해야 역시간 관계를 쓸 수 있다.

**채점·확인 기준:** 분모 방향·2/3초·2배·100%·50%를 구분한다.

</details>

#### 확인 Q07 · Amdahl의 남는 시간

원래 time의 80%를 4배 개선하면 남는 time 비율과 overall speedup은? 그 부분을 무한히 빠르게 한 상한과, 원래 10%만 개선할 수 있을 때 상한도 설명하라.

<details><summary>해설 보기</summary>

`Tnew/Told=(1−0.8)+0.8/4=0.4`, speedup은 2.5다. 아무리 빨라도 20%가 남아 상한은 5이며 유한 개선으로 그 한계를 넘을 수 없다. 10%만 제거할 수 있다면 90%가 남아 상한 `1/0.9≈1.111`이다. 개선 가능한 비중 f는 원래 시간이고, 작은 f가 부분 speedup을 식에서 없애는 것은 아니다.

**채점·확인 기준:** 고정 부분과 줄어드는 부분을 따로 쓰고 세 배수를 검산한다.

</details>

#### 확인 Q08 · Instruction 비중과 Time 비중

100 instructions 중 A는 20개/CPI 4, B는 80개/CPI 1이고 공통 clock이다. A의 instruction 비중·time 비중과 전체 CPI를 계산하고 A만 빨라질 때 남는 cycle 하한을 말하라.

<details><summary>해설 보기</summary>

A cycle은 80, B도 80, 합 160이므로 전체 CPI=1.6이다. A의 count 비중은 0.2지만 time 비중은 `80/160=0.5`다. A의 시간을 0으로 보내도 B의 80 cycles가 남는다. Amdahl에 count 0.2를 그대로 넣으면 class별 비용 차이를 무시하게 된다.

**채점·확인 기준:** 20%/50%를 구분하고 160 cycles·CPI 1.6·80-cycle 하한을 확인한다.

</details>

### 적용과 오류 진단

#### 연습 P01 · 달성 가능한 목표와 불가능한 목표

새로 만든 synthetic 연습이다. [EX:ca_2025_2_midterm_q11 p.3] (a–c)의 CPI 역산·고정 부분 하한과 [EX:ca_2025_2_midterm_q06 p.2]의 부분 개선 추론을 옮긴다. 선수는 현재 본문의 CPU time과 count→time 비중이다. IC=`2×10^9`, clock=2 GHz이고 A는 count의 25%/CPI 6, B는 75%/CPI 2다. IC·clock·B를 고정하고 A만 개선한다. 원래 time/CPI, 목표 1.8초의 필요한 평균 CPI와 A speedup, 목표 1.2초의 가능성을 구하라. 1.5초를 유한 speedup으로 달성할 수도 있는가?

<details><summary>해설 보기</summary>

원래 평균 CPI=`0.25×6+0.75×2=3`, time=3초다. A·B의 원래 시간은 각각 1.5초이므로 A time 비중은 25%가 아니라 50%다. 1.8초 목표의 평균 CPI=`1.8×2×10^9/(2×10^9)=1.8`이다. `1.5+1.5/S=1.8`에서 S=5, 새 A CPI=6/5=1.2이며 overall speedup=3/1.8=5/3이다. B만 1.5초이므로 1.2초는 불가능하다. 1.5초 자체도 A 시간이 정확히 0이어야 하므로 이 모형에서는 유한 S로 도달하지 않고 극한에서 접근한다.

**채점·확인 기준:** Count/time 구분·역산·부분/전체 speedup·불가능과 극한 도달을 각각 확인한다.

</details>

### 복습 순서

Q01–Q02로 측정 대상을, Q03–Q06으로 단위와 비율 방향을 확인한다. Q07–Q08 및 P01은 개선되지 않는 부분부터 계산한 뒤 [[courses/computer_architecture/units/performance-comparison|Workload와 평균]]에서 weight의 의미를 이어서 점검한다.

## 출처

- [[courses/computer_architecture/lectures/2026-09-15-lecture-05|2026-09-15 · 강의 노트]]

- [lec.04.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.04.pdf): [[page_cache/computer_architecture/lec.04/page-003|p.3]], [[page_cache/computer_architecture/lec.04/page-004|p.4]], [[page_cache/computer_architecture/lec.04/page-005|p.5]], [[page_cache/computer_architecture/lec.04/page-006|p.6]], [[page_cache/computer_architecture/lec.04/page-007|p.7]], [[page_cache/computer_architecture/lec.04/page-010|p.10]], [[page_cache/computer_architecture/lec.04/page-011|p.11]], [[page_cache/computer_architecture/lec.04/page-012|p.12]]

- [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT · 02:08, 05:26, 08:19, 13:07, 16:05–18:54, 19:47, 27:22, 29:17]]

- 9월 15일 08:19의 latency 방향과 17:56의 CPI 표현은 불명확하다. 정의·시간식으로 설명하며 복원된 발화라고 하지 않는다.
- Elapsed−CPU 차이의 모든 원인을 세 counter만으로 분해할 수 없다. Energy·power는 자료 기반 배경이며 세부 energy model을 강의한 것은 아니다.
- 30:18의 pipeline 예고로 개별 memory latency 감소나 datapath 설계를 이미 배웠다고 판단하지 않는다.
- 복기 Q11의 200 billion instruction 수를 임의로 수정하지 않는다. 새 연습의 수치는 별도 조건이고 FP instruction 구현은 전이 범위에 없다.
- 2025-2 문항은 복기본이며 공식 원문·답안 정확성은 확인되지 않았다. 연결은 추론 요구를 뜻하며 출제 예측이 아니다.

- [[exam_questions/ca_2025_2_midterm_q11|기존 문제 미리보기 · Q11]]


---

[[courses/computer_architecture/units/procedures-stack|← 이전: Procedure 호출·Calling convention·Stack]] · [[courses/computer_architecture/units/index|단원 목차]] · [[courses/computer_architecture/units/performance-comparison|다음: Workload·평균·성능 비교 →]]
