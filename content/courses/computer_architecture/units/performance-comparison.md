---
title: "Workload·평균·성능 비교"
description: "Workload와 weight에 맞춰 runtime·normalized ratio·aggregate IPC를 집계한다."
course: "computer_architecture"
unit_id: "performance-comparison"
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

여러 실행 결과를 합칠 때 총량·비율·처리율 중 무엇을 구하는지 먼저 정한다. Weight의 의미와 비율의 방향을 쓰면 같은 숫자라도 AM·GM·HM이 서로 다른 질문에 답한다는 점을 확인할 수 있다.

## Workload가 성능 비교의 뜻을 정한다

[CPU execution time과 speedup](performance-model.md)을 계산할 수 있어도, 그 결과가 어떤 사용 상황을 대표하는지는 별도 질문이다. Workload(작업 부하)는 비교할 application과 실행량의 조합이다. Computer X가 application A에서 빠르더라도 B에서 같은 비율로 빠르다는 보장은 없고 C에서는 Y가 더 빠를 수 있다. Game, AI, 다른 연구 작업의 비중이 달라지면 같은 두 machine의 사용자 관점 비교도 달라진다. [[page_cache/computer_architecture/lec.04/page-013|CA M006 p.13]] [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 31:13–33:15]]

여러 결과를 하나의 수치로 요약할 때는 먼저 무엇을 합하는지 정해야 한다. 실행시간이라는 amount(양)를 더하는지, 기준 machine 대비 ratio(비율)를 비교하는지, 단위 시간·cycle당 rate(처리율)를 합치는지에 따라 식이 달라진다. 평균 이름을 먼저 고르고 숫자를 넣기보다 총량과 분모를 먼저 쓰는 편이 안전하다.

## Arithmetic mean과 실행 횟수 Weight

Arithmetic mean(산술평균, AM)은 `n`개 runtime의 합을 `n`으로 나눈다.

$$
AM(T)=\frac{1}{n}\sum_{i=1}^{n}T_i.
$$

같은 application 집합을 같은 횟수씩 실행한다면 AM의 비교는 total runtime의 비교와 같다. 두 machine에 같은 workload를 적용했을 때 `AM_X/AM_Y`는 Y의 X 대비 speedup이다. 긴 application이 합에 더 많이 기여하는 것은 전체 시간을 더한다는 의미에서 자연스럽다. 실제 사용에서는 짧은 application을 훨씬 자주 실행한다면 **같은 횟수**라는 가정이 workload를 대표하지 못하는 것이 문제다. [[page_cache/computer_architecture/lec.04/page-014|CA M006 p.14]]

실행 횟수의 비중을 `w_i`, 그 합을 1로 놓으면 weighted arithmetic mean(가중 산술평균, WAM)은:

$$
WAM(T)=\sum_i w_iT_i,\qquad \sum_iw_i=1.
$$

설명용으로 1초짜리 application을 아홉 번, 10초짜리를 한 번 실행하면 total은 `9×1+1×10=19 s`, 평균은 `19/10=1.9 s/run`이다. 같은 계산을 `0.9×1+0.1×10=1.9`로 할 수 있다. Application 종류 두 개를 동일 가중으로 평균한 5.5초는 이 실행 패턴을 나타내지 않는다. [[page_cache/computer_architecture/lec.04/page-015|CA M006 p.15]]

Weight는 큰 값을 임의로 약하게 만드는 장치가 아니다. 이 runtime 식에서는 **전체 실행 횟수 중 각 종류의 비중**이다. 두 machine의 WAM을 비교할 때도 같은 weight를 사용해야 같은 workload의 비교가 된다.

### 평균 CPI의 Weight는 Instruction count

CPI는 총 cycle 수를 총 instruction 수로 나눈 값이다. 종류 `i`의 instruction 수를 `I_i`, CPI를 `c_i`라 하면:

$$
CPI_{\mathrm{all}}=
\frac{\sum_i I_ic_i}{\sum_i I_i}
=\sum_i\left(\frac{I_i}{\sum_jI_j}\right)c_i.
$$

따라서 이 식의 weight는 instruction-count 비중이다. 9월 15일 37:12의 arithmetic 90%와 movement 10% 예에서는 “of the time”이라는 표현을 사용했다. 그 발화를 instruction-count 비중으로 바꾸어 인용하지 않는다. 시간 비중을 줬다면 위 식에 바로 넣을 수 없고 각 종류의 비용과 그 비중이 무엇을 측정했는지부터 확인해야 한다. [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 37:12]]

## Geometric mean과 Normalized time ratio

Benchmark마다 실행시간의 규모가 다르면 기준 machine에 대한 상대 비율을 먼저 만들 수 있다. `r_i=T_Xi/T_Yi`로 정의하면 geometric mean(기하평균, GM)은:

$$
G=\left(\prod_{i=1}^{n}r_i\right)^{1/n}.
$$

이는 양의 비율들의 곱셈적 변화를 요약한다. 설명용 비율 0.5와 2의 GM은 `sqrt(0.5×2)=1`이다. 한 benchmark에서 절반 시간이고 다른 하나에서는 두 배 시간이 걸리는 대칭을 나타낸다. 그러나 **총 실행시간이 같다**는 뜻은 아니다. 예를 들어 Y의 두 시간이 2초와 100초, X의 시간이 1초와 200초라면 비율은 그대로지만 합은 각각 102초와 201초다.

[[page_cache/computer_architecture/lec.04/page-016|CA M006 p.16]]의 실제 분수는 `Time_X/Time_Y`다. 그러므로 `G<1`이면 X의 시간이 상대적으로 짧다. 같은 slide의 “relative speedup” 문구는 앞에서 정의한 X의 speedup `Time_Y/Time_X`와 방향이 반대다. 여기서는 **시간 비율 G와 speedup 방향 1/G를 구분해 정정**한다. 예를 들어 `G=0.8`이면 대응하는 speedup의 GM은 `1/0.8=1.25`다. [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 39:09]]

GM은 다음 성질을 갖는다.

$$
\frac{GM(X_i)}{GM(Y_i)}=GM\left(\frac{X_i}{Y_i}\right).
$$

같은 benchmark 집합을 공통 reference `Z_i`로 정규화해도 `GM(X_i/Z_i)/GM(Y_i/Z_i)=GM(X_i/Y_i)`가 되어 기준이 소거된다. 이것은 같은 비교 집합과 일관된 방향을 쓴 결과다. Workload의 실행 횟수를 무시해도 된다는 허가나 어떤 machine이 모든 작업에서 우세하다는 뜻은 아니다.

## Harmonic mean은 총 작업량을 총시간으로 나눈다

Rate의 평균은 먼저 **총 작업량/총시간**으로 구성한다. 자료처럼 처음 10 km는 30 km/h, 다음 10 km는 90 km/h로 이동하면:

$$
v_{\mathrm{avg}}=
\frac{20}{10/30+10/90}
=\frac{20}{4/9}
=45\ \mathrm{km/h}.
$$

두 구간의 시간은 각각 1/3시간과 1/9시간이다. 같은 거리를 느리게 가는 구간에서 세 배 오래 머물기 때문에 단순 산술평균 60 km/h와 다르다. [[page_cache/computer_architecture/lec.04/page-017|CA M006 p.17]]

같은 양 `W`의 작업을 양의 rate `r_i`로 수행하면 각 시간은 `W/r_i`다. `nW`를 이 시간의 합으로 나누어 harmonic mean(조화평균, HM)을 얻는다. 작업량 비중 `w_i`가 합계 1이면 weighted harmonic mean(가중 조화평균, WHM)으로 일반화된다.

$$
HM(r)=\frac{n}{\sum_i1/r_i},
\qquad
WHM(r)=\frac{1}{\sum_iw_i/r_i}.
$$

이 weight는 시간 비중이나 막연한 중요도가 아니라 **합치는 작업량의 비중**이다. “Rate에는 언제나 HM”이라고 외우면 조건을 잃는다. 예를 들어 같은 시간 동안 30과 90 km/h로 달렸다면 거리 합을 시간 합으로 나누었을 때 60 km/h가 된다. 어떤 양을 동일하게 고정했는지가 식을 결정한다.

## Aggregate IPC와 CPI의 역수 관계

Aggregate IPC(전체 집계 IPC)는 전체 instruction 수를 전체 cycle 수로 나눈다. 실행 `i`가 `I_i` instructions를 `CPI_i`로 처리하면:

$$
IPC_{\mathrm{all}}=
\frac{\sum_i I_i}{\sum_i I_iCPI_i}.
$$

모든 실행의 instruction 수가 같은 `I`일 때:

$$
IPC_{\mathrm{all}}=
\frac{nI}{\sum_i ICPI_i}
=\frac{1}{AM(CPI)}
=HM(IPC).
$$

[[page_cache/computer_architecture/lec.04/page-018|CA M006 p.18]]은 같은 frequency와 같은 instruction count를 전제로 이 관계를 설명한다. 그 위의 “Avg. Time = Avg. CPI”는 공통 `I/f_clock`를 생략한 비례 관계다. 초와 cycles/instruction이 단위까지 같은 항등식이라는 뜻은 아니다. 강의 42:11의 불명확한 구두 유도는 위의 총량 계산과 구분한다. [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 42:11]]

예를 들어 같은 instruction 수를 IPC 1과 2로 처리하면 전체 IPC는 `2/(1+1/2)=4/3`이지 1.5가 아니다. 다른 설명용 계산으로 각각 100 instructions를 CPI 1과 3으로 처리하면 cycle은 100과 300, 전체 IPC는 `200/400=0.5`다. 개별 IPC 1과 1/3을 산술평균한 2/3은 그 전체 처리율과 다르다.

Instruction 수가 다르면 `w_i=I_i/ΣI_i`를 사용하여 `IPC_all=1/Σ(w_i CPI_i)=1/Σ(w_i/IPC_i)`로 계산한다. 복기 Q5에서 IPC라는 이름만 보고 GM이나 HM을 고르는 대신, **실제 전체 처리율을 묻는지, 정규화한 benchmark 비율을 요약하는지** 확인해야 하는 이유다. [EX:ca_2025_2_midterm_q05 p.2]

| 집계 대상 | 먼저 정할 조건 | 그 조건에 맞는 식 |
|---|---|---|
| Runtime | 각 application의 실행 횟수 | AM 또는 실행 횟수 WAM |
| Normalized ratio | 같은 benchmark 집합, 기준과 비율 방향 | GM |
| Rate | 같은 작업량 또는 알려진 작업량 비중 | HM 또는 WHM |

표의 이름보다 분자·분모와 weight가 먼저다. Rate를 정규화한 비율을 GM으로 요약하는 것과, 실제 완료한 작업 전체의 rate를 구하는 것은 서로 다른 통계량이다.

## Standard benchmark와 대표성 있는 측정

관심 application이 모두 다르므로 standard benchmark(표준 벤치마크)는 공통 workload와 비교 규칙을 제공한다. 강의는 SPEC benchmark 집합을 소개하고 systems·architecture 연구에서 공통 평가 기준으로 쓰인다고 설명했다. 자료는 여러 산업의 위원회가 고른 application, 기술과 용도 변화에 따른 갱신, 불완전하지만 유용한 공통 기준이라는 배경을 제시한다. [[page_cache/computer_architecture/lec.04/page-020|CA M006 p.20]] [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 44:10–45:07]]

M006 p.21의 integer·floating-point suite 목록은 program·language·용도를 보여 주지만 개별 program 동작을 배웠다는 근거는 아니다. 이 소개에서 필요한 것은 이름 암기보다 **공통 benchmark도 내 workload를 완전히 대표하지 않을 수 있다**는 판단이다. 자료의 배포 관련 표현도 현재의 모든 개별 benchmark license를 보증하지 않는다.

성능을 보고할 때는 측정 목적, 실제 workload와 실행량, 시간의 종류, 환경과 방법, 요약의 방향과 weight를 밝혀야 한다. 한 application에서의 2배를 컴퓨터 전체가 항상 2배라는 주장으로 옮기면 대표성을 잃는다. 하나의 숫자로 요약할 근거가 약하면 개별 결과를 함께 제시하고 raw data(원자료)를 확인할 수 있게 한다. [[page_cache/computer_architecture/lec.04/page-022|CA M006 p.22]] [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT 46:06–48:47]] 독자가 그 수치를 다른 workload에 적용할 수 있는지 판단하려면 결과뿐 아니라 **그 결과가 무엇을 측정했는지**도 알아야 한다.

## 핵심 정리

- 어떤 application을 몇 번 실행하는지가 비교의 의미를 정한다.
- Runtime WAM은 실행 횟수, CPI WAM은 instruction count를 weight로 쓴다.
- GM은 양의 정규화 비율을 요약하며 total runtime과 동일하지 않다.
- Rate는 총 작업량/총시간으로 유도한다. 같은 작업량일 때 HM, 알려진 작업량 비중이면 WHM이다.
- 실제 IPC는 총 instructions/총 cycles이며 benchmark 비율의 GM과 다른 통계량이다.
- 공통 benchmark도 실제 사용을 완벽히 대표하지 않으므로 개별 결과와 측정 조건을 함께 본다.

## 확인·연습문제

### 개념 확인과 추적

#### 확인 Q01 · 무엇을 대표하는 수치인가

한 application에서 X의 speedup이 2라고 보고했다. 왜 모든 용도에서 두 배 빠르다고 결론낼 수 없는가? 독자가 재해석할 수 있게 보고해야 할 항목을 제시하라.

<details><summary>해설 보기</summary>

다른 application은 instruction mix·병목·실행량이 다르고 우열이 바뀔 수 있다. 보고에는 측정 목적, 실제 application과 실행 횟수, 시간의 종류, 환경·방법, 비교 기준과 비율 방향, 평균의 식·weight가 필요하다. 요약이 대표성을 잃으면 개별 결과와 원자료도 제시해야 한다. Workload를 밝히는 일은 단일 수치의 적용 범위를 정하는 일이다.

**채점·확인 기준:** 서로 다른 workload의 가능성과 재현·해석에 필요한 구체 항목을 설명한다.

</details>

#### 확인 Q02 · Runtime의 실행 횟수 Weight

A=1초, B=10초를 A 9회·B 1회 실행한다. Total·실행당 평균·종류별 동일 weight 평균을 비교하라. AM/WAM의 비교를 speedup으로 읽는 조건과 방향은?

<details><summary>해설 보기</summary>

Total=19초, 실행당 평균=19/10=1.9초이며 weight는 0.9·0.1이다. 종류에 동일 weight를 주면 `(1+10)/2=5.5`초로 다른 실행 패턴을 나타낸다. 같은 application을 동일 횟수씩 실행할 때 AM 비교는 total 비교와 같고, WAM은 같은 run-count weight를 두 machine에 적용해야 한다. `WAM_X/WAM_Y`는 Y의 X 대비 speedup이다. 긴 실행이 time 합에 많이 기여하는 것 자체는 오류가 아니다.

**채점·확인 기준:** 19·1.9·5.5와 weight의 의미, 동일 workload·speedup 방향을 확인한다.

</details>

#### 확인 Q03 · CPI의 Weight는 무엇인가

Instruction A 90개/CPI 1, B 10개/CPI 5의 전체 CPI를 구하라. A time이 90%라는 정보만 주었을 때도 같은 계산을 해도 되는가?

<details><summary>해설 보기</summary>

Cycle 합은 90+50=140, instruction 합은 100이므로 CPI=1.4다. `0.9×1+0.1×5`의 0.9·0.1은 instruction 수 비중이다. 실제 A time 비중은 공통 clock에서 90/140=9/14로 90%가 아니다. Time 비중만 주면 count와의 관계부터 구해야 하므로 그대로 대입하면 안 된다. 강의의 'of the time' 표현도 임의로 count로 바꾸지 않는다.

**채점·확인 기준:** 140/100 유도와 instruction/time weight 차이를 설명한다.

</details>

#### 확인 Q04 · GM의 방향과 Total의 차이

Y의 두 runtime은 2·100초, X는 1·200초다. `T_X/T_Y`의 GM과 total을 비교하라. Time-ratio GM=0.8인 별도 사례의 speedup GM은? 공통 reference Z를 쓰면 GM의 비교가 변하는가?

<details><summary>해설 보기</summary>

비율 0.5·2의 GM은 1이지만 total은 Y=102초, X=201초로 같지 않다. GM은 multiplicative ratio 요약이다. Time-ratio 0.8의 반대 방향 speedup은 1/0.8=1.25다. 같은 양의 benchmark 값으로 `GM(X/Z)/GM(Y/Z)=GM(X/Y)`가 되어 Z가 소거된다. 같은 집합과 방향을 유지해야 하며 이 성질이 실제 실행 횟수나 총시간을 대신하지는 않는다.

**채점·확인 기준:** GM=1과 서로 다른 total, 1.25 방향, 공통 reference 조건을 확인한다.

</details>

#### 확인 Q05 · 같은 거리와 같은 시간

10 km씩 30·90 km/h로 가면 평균은? 같은 시간씩 그 속도로 달리면 왜 달라지는가? 첫 속도로 20 km, 둘째로 10 km일 때 work weight와 WHM도 구하라.

<details><summary>해설 보기</summary>

동일 거리에서는 `20/(10/30+10/90)=45 km/h`다. 느린 구간에 1/3시간, 빠른 구간에 1/9시간을 써 단순 평균 60이 아니다. 같은 시간 t씩이면 거리=(30+90)t, 시간=2t여서 60이다. 20·10 km의 work weight는 2/3·1/3이고 `WHM=1/((2/3)/30+(1/3)/90)=270/7≈38.57 km/h`다. Positive rate와 작업량 비중이라는 조건에서 총량/총시간을 전개한 결과다.

**채점·확인 기준:** 45·60·270/7과 각 case의 동일하게 둔 양을 명시한다.

</details>

#### 확인 Q06 · 전체 IPC를 Totals로 구하기

두 구간이 각각 100 instructions를 CPI 1·3으로 처리할 때 전체 CPI/IPC를 구하라. 둘째 구간만 300 instructions라면? 왜 p.18의 Time=CPI는 단위가 같은 등식이 아니며 normalized ratio의 GM과도 다른가?

<details><summary>해설 보기</summary>

같은 count이면 cycles=100+300=400, CPI=400/200=2, IPC=0.5다. 개별 IPC 1과 1/3의 AM인 2/3은 틀리고 `1/AM(CPI)=HM(IPC)`가 맞다. 둘째 count=300이면 cycles=100+900=1000, instructions=400, CPI=2.5, IPC=0.4다. Weight 1/4·3/4로 CPI를 평균한 뒤 역수를 취한다. Time은 같은 I·frequency 아래 `(I/f)×CPI`로 비례한다. IPC의 totals와 benchmark ratio의 곱셈 요약은 질문 자체가 다르다.

**채점·확인 기준:** 두 count 조건의 totals와 역수, CPI weight·차원·rate/ratio 구별을 확인한다.

</details>

#### 확인 Q07 · 공통 Benchmark의 쓸모와 한계

SPEC 같은 공통 benchmark가 유용하면서도 모든 사용자 workload를 대표하지는 못하는 이유는? 이 단원의 자료에서 suite 이름 암기·현재 license·개별 program 동작까지 결론낼 수 있는가?

<details><summary>해설 보기</summary>

공통 application과 규칙이 있으면 machine·설계를 같은 기준으로 비교할 수 있고, 기술·용도 변화에 맞춰 workload를 갱신할 이유도 생긴다. 하지만 사용자의 실행 비중·bottleneck이 다르면 공통 점수와 실제 체감은 달라진다. 자료의 suite 목록은 이름·용도 소개일 뿐 상세 동작을 학습한 근거가 아니며 현재 license도 증명하지 않는다. 강의가 남긴 목표는 이름 암기가 아니라 benchmark 집합의 존재와 한계를 이해하는 것이다.

**채점·확인 기준:** 공통 비교와 실제 대표성을 분리하고 자료가 확정하지 않는 범위를 유지한다.

</details>

### 적용과 오류 진단

#### 연습 P01 · IPC라는 이름으로 평균 고르지 않기

새로 만든 synthetic 연습이다. [EX:ca_2025_2_midterm_q05 p.2]의 rate/ratio 구별을 적용하며 선수는 현재 본문의 totals·weight·GM·HM이다. X는 A에서 100 instructions를 IPC 1, B에서 300 instructions를 IPC 2로 처리한다. Reference의 각 benchmark IPC는 1이다. 한 보고서가 normalized IPC ratio의 GM을 구한 뒤 그 값을 X가 완료한 전체 작업의 IPC라고 썼다. 실제 IPC, 적절한 weight, GM을 구하고 보고서의 혼동을 설명하라. Unweighted HM은 여기서 유효한가?

<details><summary>해설 보기</summary>

X의 cycles는 A=100/1=100, B=300/2=150으로 합 250이다. 전체 IPC=400/250=1.6이며 work weight=1/4·3/4로 `1/((1/4)/1+(3/4)/2)=1.6`을 얻는다. Normalized ratio는 1과 2, GM은 `√2≈1.414`로 다른 통계량이다. Unweighted HM=`2/(1+1/2)=4/3`은 동일 instruction 수를 가정하므로 이 workload에 맞지 않는다. GM은 benchmark별 상대 변화의 요약으로 표시하고 실제 totals의 IPC와 따로 보고해야 한다.

**채점·확인 기준:** 400/250·count weight·√2·unweighted HM의 조건 실패를 각각 보인다.

</details>

### 복습 순서

Q01–Q03으로 workload와 weight를 명시하고 Q04–Q06은 평균 이름 대신 분자·분모부터 만든다. P01에서 실제 처리율과 정규화 비율을 분리한 뒤 Q07의 기준으로 자기 성능 보고서를 짧게 점검한다. 식의 단위가 헷갈리면 [[courses/computer_architecture/units/performance-model|실행시간 모형]]의 Q03을 다시 푼다.

## 출처

- [[courses/computer_architecture/lectures/2026-09-15-lecture-05|2026-09-15 · 강의 노트]]

- [lec.04.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.04.pdf): [[page_cache/computer_architecture/lec.04/page-013|p.13]], [[page_cache/computer_architecture/lec.04/page-014|p.14]], [[page_cache/computer_architecture/lec.04/page-015|p.15]], [[page_cache/computer_architecture/lec.04/page-016|p.16]], [[page_cache/computer_architecture/lec.04/page-017|p.17]], [[page_cache/computer_architecture/lec.04/page-018|p.18]], [[page_cache/computer_architecture/lec.04/page-019|p.19]], [[page_cache/computer_architecture/lec.04/page-020|p.20]], [[page_cache/computer_architecture/lec.04/page-022|p.22]]

- [[courses/computer_architecture/transcripts/2026-09-15|2026-09-15 STT · 31:13–33:15, 37:12, 39:09, 42:11, 44:10–45:07, 46:06–48:47]]

- 9월 15일 37:12의 'of the time'은 instruction-count 비중으로 고쳐 인용하지 않는다. CPI 집계에 쓸 weight는 실제 instruction count여야 한다.
- lec.04 p.16은 `Time_X/Time_Y`를 쓰면서 relative speedup으로 부른다. 이 불일치는 time ratio와 역방향 speedup을 나누어 설명한다.
- p.18의 Time=CPI는 같은 I/f를 생략한 비례 관계이며 단위가 같은 등식은 아니다. 42:11의 불명확한 구두 유도는 복원하지 않는다.
- SPEC는 공통 benchmark의 목적을 설명하는 배경이다. 개별 suite 동작·이름 암기·현재 license를 이 자료로 추가 학습 범위나 확정 사실로 삼지 않는다. 비기술적 개인 일화 대신 투명한 측정 원칙만 유지한다.
- 2025-2 문항은 복기본이며 공식 원문·답안 정확성은 확인되지 않았다. 연결은 추론 요구를 뜻하며 출제 예측이 아니다.


---

[[courses/computer_architecture/units/performance-model|← 이전: 실행시간과 Performance 모형]] · [[courses/computer_architecture/units/index|단원 목차]]
