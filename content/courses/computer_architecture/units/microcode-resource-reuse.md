---
title: "Microcode·자원 공유·Pipelining과 Hazard"
description: "Microcode의 자원 공유부터 pipeline의 시간 계산, data·control hazard와 분기 정책까지 확인하는 문제와 해설입니다."
course: "computer_architecture"
unit_id: "microcode-resource-reuse"
lang: "ko"
note_layout: "textbook_unit_v1"
reader_layout: "content_first"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook", "plain-document"]
source_assets: ["lec 06.pdf", "lec 07.pdf", "lec 08.pdf", "lec 09.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_architecture/lectures/2026-09-29-lecture-05"]
---

## Microprogram과 다음 control state

명령어가 여러 cycle에 걸쳐 실행되면 datapath에 무엇을 시킬지뿐 아니라 다음 cycle에 어떤 control state로 갈지도 정해야 한다. Opcode와 현재 state를 한꺼번에 큰 ROM의 주소로 쓰면, opcode와 무관하게 다음 state로 가는 부분까지 반복 저장할 수 있다. **Microprogram(마이크로프로그램)**은 control의 진행 순서를 별도의 작은 프로그램으로 표현한다. **μPC(microprogram counter)**는 실행할 microinstruction의 주소이고, μprogram ROM은 그 주소의 control word를 내보낸다. 사용자 프로그램의 명령어 주소인 PC와 μPC는 서로 다른 state이다.

[computer_architecture:NM002 p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-015)의 그림에서는 μPC가 μprogram ROM의 주소 입력으로 들어간다. ROM의 출력은 datapath control과 다음 μPC를 고르는 `AddrCtl`을 포함한다. 다음 주소 후보를 만드는 incrementer와 dispatch ROM을 구분해서 보면 그림의 연결이 읽힌다.

| AddrCtl | 다음 μPC의 선택 | 의미 |
|---|---|---|
| 0 | 0 | 공통 시작 state로 복귀 |
| 1 | Dispatch ROM 1의 출력 | Opcode에 따른 첫 분기 |
| 2 | Dispatch ROM 2의 출력 | 이후 단계의 opcode별 분기 |
| 3 | μPC + 1 | 연속된 microinstruction으로 진행 |

이 그림의 Dispatch ROM 1에서 R-format의 opcode `000000`은 주소 `0110`, `jmp`의 `000010`은 `1001`, `beq`의 `000100`은 `1000`으로 간다. `lw`와 `sw`의 opcode `100011`, `101011`은 모두 `0010`으로 가지만, Dispatch ROM 2에서는 각각 `0011`, `0101`로 갈라진다. 주소 계산처럼 공유할 수 있는 과정은 함께 수행하고, load와 store의 서로 다른 후속 동작에서 갈라지는 구조다.

예를 들어 μPC가 5이고 `AddrCtl=3`이면 다음 μPC는 6이다. R-format을 dispatch해서 이 그림의 주소 6에 도착하는 것과 숫자는 같아도, 다른 FSM의 state 6까지 같은 동작이라는 뜻은 아니다. 이 표는 6-bit opcode를 쓰는 기존 ISA 예제이며 RISC-V의 7-bit opcode 표로 바꾸어 읽으면 안 된다. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 강의 (computer_architecture:NT001)]] 39:27은 incrementer를 설명하고, 43:18·44:26은 비교 중인 FSM들이 서로 다른 예제임을 짚는다. 앞선 multi-cycle control의 흐름은 [[courses/computer_architecture/lectures/2026-09-29-lecture-05|2026-09-29 Computer Architecture 강의 노트]]와 연결된다. Microprogram을 쓴다는 사실만으로 면적이나 실행 속도의 개선량이 정해지는 것은 아니다.

## ALU의 시간 공유와 Instruction Register

### 같은 회로에 다른 일을 맡기는 시간

Single-cycle datapath에서 명령어 연산과 다음 순차 PC 계산이 같은 cycle에 필요하면, ALU 외에 PC용 adder를 두는 구성이 자연스럽다. Multi-cycle에서는 두 작업의 시간을 나눌 수 있다. IF에서는 ALU에 PC와 4를 넣고, EX에서는 register operand나 immediate를 넣는다. **Multiplexer(mux)**는 필요한 입력을 선택하고, control은 어느 cycle에 어느 입력과 operation을 사용할지 정한다. 같은 ALU가 한 순간에 두 독립적인 덧셈을 모두 수행하는 것은 아니다. [computer_architecture:NM002 p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-020); [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 강의 (computer_architecture:NT001)]] 45:27·47:25.

시간 공유를 풀어 쓴 교육용 예를 보자. 4-byte instruction을 사용하는 모델에서 PC가 `0x3000`이고 그곳의 명령어 K가 두 값 10과 12를 더한다고 하자. IF의 ALU 계산은 `0x3000 + 4 = 0x3004`이고, 이후 EX의 ALU 계산은 `10 + 12 = 22`다. 두 결과의 의미도 다르고 보존해야 할 위치도 다르다. 앞의 결과는 다음 instruction 주소이고 뒤의 결과는 K의 연산 결과다. PC+4는 여기서 사용한 instruction 길이 가정에 따른 것이며 모든 RISC-V instruction 길이를 4 bytes로 단정하는 규칙이 아니다.

L06·L07의 기존 datapath 그림에 있는 16→32-bit sign extension 역시 그 예제의 폭이다. RV64의 32-bit instruction word와 64-bit register data를 설명하는 폭으로 가져오지 않는다.

Adder를 공유하면 중복 arithmetic hardware를 줄일 수 있지만 입력 mux, control, 중간값 저장이 필요하다. Cycle 수가 늘거나 mux가 경로를 길게 만들 수도 있다. 따라서 “회로 하나를 줄였다”와 “프로그램이 더 빨라졌다”는 별도로 판단해야 한다.

### PC가 바뀌어도 현재 instruction을 지키기

Instruction memory가 combinational하게 주소를 따라 출력한다고 하자. PC를 일찍 `0x3004`로 갱신하면 memory의 출력도 다음 instruction으로 바뀔 수 있다. 그런데 K의 decode와 register read가 아직 그 출력에 직접 의존한다면, 실행 중인 명령어의 근거가 중간에 사라진다.

**Instruction Register(IR)**는 fetch한 instruction bits를 저장하여 이 경계를 만든다. [computer_architecture:NM002 p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-022)에서 확인할 것은 memory 출력 뒤의 IR이다. Fetch 단계에서 K를 포착한 뒤 IR이 K를 유지하면 PC가 바뀌어도 decode는 같은 K를 본다. 위 예에서 IR이 저장하는 것은 주소 `0x3000` 자체가 아니라 그 주소에서 읽은 K의 비트열이다. Capture할 때와 hold할 때를 구분해야 하는 이유이며, 그림만으로 특정 latch의 active level이나 setup time까지 정할 수는 없다.

[[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 강의 (computer_architecture:NT001)]] 48:04는 PC 변경으로 instruction 출력이 달라지는 문제를 설명한다. 49:03·49:43의 PC와 instruction을 섞은 표현은 이 IR의 저장 내용을 엄밀하게 규정하는 말로 사용하지 않는다. 여기서 instruction bits라고 구분한 것은 자료의 연결에 따른 설명이다.

## Shared memory와 중간값의 수명

ALU를 공유하듯 instruction fetch와 data access도 시간을 나누어 memory를 공유할 수 있다. [computer_architecture:NM002 p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-023)의 multi-cycle 그림에서는 memory 주소로 PC 또는 계산한 data address를 선택한다. 이때 여러 cycle을 건너야 하는 값마다 저장 장소가 필요하다.

| 내부 저장소 | 보존하는 값 | 필요한 이유 |
|---|---|---|
| IR | Fetch한 instruction bits | PC와 memory 출력이 변해도 decode의 대상을 유지 |
| MDR | Memory에서 읽은 data | Memory read 이후 writeback까지 값을 유지 |
| A, B | Register file에서 읽은 operand | 나중 cycle의 ALU 연산이나 store에 사용 |
| ALUOut | ALU가 만든 중간 결과 또는 address | 이후 memory access나 writeback에 사용 |

Load에서는 effective address를 계산한 뒤 memory access까지 지켜야 하고, 읽은 data는 register writeback까지 지켜야 한다. Store에서는 쓸 위치와 쓸 값을 모두 해당 memory 동작 때까지 보존해야 한다. Address와 data가 모두 bit vector라는 이유로 서로 대체할 수는 없다. 이 저장소들은 programmer-visible general-purpose register와 구별되는 microarchitectural state이다.

이 그림의 resource reuse는 한 instruction의 여러 cycle을 이용한 시간 공유다. Pipeline에서는 다른 instruction들의 IF와 MEM이 같은 cycle에 겹칠 수 있다. Single-port memory 하나로 두 접근을 동시에 요구한다면 resource conflict를 해결해야 한다. 순차적인 multi-cycle 그림에서 가능한 공유가 pipeline에서도 그대로 가능하다고 결론내릴 수 없는 이유다. 2026-09-29 강의 51:38의 idle stage를 겹쳐 쓰자는 설명은 이 다음 주제의 동기이며, 52:36의 공유 memory 언급만으로 구체적인 arbitration이나 모든 enable 신호의 순서가 정해지지는 않는다.

## Datapath와 microcontroller 사이의 복잡성

복잡한 instruction을 구현하는 방법은 한 가지가 아니다. Datapath에 전용 기능을 많이 넣으면 microprogram이 적은 단계로 그 기능을 호출할 수 있다. 반대로 단순한 datapath의 기본 연산을 여러 번 조합하면 microprogram이 더 길어지고 sequencing도 복잡해진다. 반복을 microprogram으로 구현하려면 반복 횟수 같은 내부 상태도 필요하다. 이를 위한 loop counter나 내부 μISA의 state를 프로그램의 일반 register와 혼동해서는 안 된다. [computer_architecture:NM002 p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-024); [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 강의 (computer_architecture:NT001)]] 53:36–54:28.

자료는 complex datapath/simple microcode, simple datapath/complex microcode, 그리고 RISC의 simple datapath/simple control이라는 대비로 설계 선택을 설명한다. 비교할 항목은 hardware 면적과 delay, microinstruction 수, control memory와 내부 state다. 이것은 복잡성을 어디에 둘지 생각하는 틀이며 모든 RISC/CISC 구현의 우열이나 현대의 특정 processor 구조를 판정하는 표는 아니다.

## Pipeline의 latency와 throughput

### 겹쳐 처리해도 한 작업의 순서는 남는다

**Pipeline(파이프라인)**은 한 작업을 stage로 나누고 서로 다른 작업을 겹쳐 처리한다. 세탁·건조·접기·보관에 각각 30분이 걸리면 한 묶음의 **latency(완료까지 걸리는 시간)**는 120분이다. 각 stage에 별도 자원이 있으면 처음 묶음이 끝난 뒤 30분마다 다음 묶음이 끝난다. 이때 **throughput(단위 시간당 완료량)**은 순차 처리의 4배이지만 첫 묶음의 latency는 줄지 않는다.

건조가 60분이면 가장 느린 stage가 처리 간격을 60분으로 제한한다. 건조기를 두 대 두고 교대로 새 묶음을 받게 하면 다시 30분마다 한 묶음을 받을 수 있지만, 자원을 추가한 결과다. 한 묶음 안의 세탁과 건조 순서를 무시한 것이 아니다. 이 절부터의 pipeline 기본 설명과 data hazard는 L07·L08 자료 복습이며 특정 결석일의 발언을 복원한 내용이 아니다. [computer_architecture:NM005 p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-006); [computer_architecture:NM005 p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-007); [computer_architecture:NM005 p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-008).

전체 combinational delay를 T, stage 경계의 latch overhead를 S, 균등하게 나눈 stage 수를 k라고 하자. 균등 분할과 충분한 독립 작업을 가정하면 다음과 같다.

| 양 | Pipeline 없음 | k-stage pipeline |
|---|---|---|
| Clock period | T + S | T/k + S |
| 정상 상태 throughput | 1/(T + S) | 1/(T/k + S) |
| 한 작업 latency | T + S | T + kS |
| Logic cost G, 경계 저장 cost L인 모델 | G + L | G + kL |

S가 양수이면 k를 늘려도 throughput은 1/S보다 커지지 않는 한계를 가진다. Latency와 저장소 cost는 오히려 늘어난다. 실제 stage가 불균형하면 T/k 대신 가장 느린 stage의 delay가 clock을 정한다. [computer_architecture:NM005 p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-011); [computer_architecture:NM005 p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-012).

### 800ps 모델의 계산과 fill/drain

L07의 IF·ID·EX·MEM·WB delay는 각각 200·100·200·200·100ps, 합계 800ps다. L06의 별도 multi-cycle 예제는 200·50·100·200·50ps, 합계 600ps다. 두 예제의 register file과 ALU delay를 섞으면 어느 모델도 아닌 계산이 된다. L07 그림의 register file은 같은 clock의 절반씩을 write와 read에 사용하는 가정을 포함한다. 뒤의 no-forwarding hazard 모델에서 쓰는 다른 RF 가정도 이 값에 덧붙이지 않는다. [computer_architecture:NM005 p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-015); [computer_architecture:NM002 p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-005).

L07에서 latch overhead와 hazard를 무시하면 pipeline clock은 200ps다. 한 instruction이 5단계를 통과하는 latency는 1000ps로, single-cycle의 800ps보다 길다. 대신 충분히 채워진 뒤에는 200ps마다 한 instruction이 완료된다. 장기 throughput 개선은 800/200 = 4배이며 단순히 “5단계이므로 5배”가 아니다.

빈 pipeline에 N개의 instruction을 연속으로 넣고 마지막 WB까지 세면 필요한 cycle은 N+4다. 첫 완료까지 5 cycle이 들고 이후 N−1개가 하나씩 완료되기 때문이다. N=3이면 pipeline 시간은 7×200=1400ps, sequential single-cycle 시간은 3×800=2400ps이므로 speedup은 12/7, 약 1.714다. Fill/drain을 포함한 짧은 실행과 정상 상태의 4배는 다른 측정이다. [computer_architecture:NM005 p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-016).

Multi-cycle은 instruction별 cycle 수를 줄일 가능성과 짧은 clock을 함께 따져야 한다. 평균 CPI가 c이고 clock이 t라면 시간은 instruction당 ct이며, clock만 짧다고 throughput이 반드시 좋아지지는 않는다. Pipeline 또한 latency와 throughput을 분리해서 비교해야 한다. 이 구분은 복원 시험의 성능 판단 항목이 요구하는 추론과 연결되지만 현재 시험 범위를 정하지는 않는다. [EX:ca_2025_2_midterm_q08 p.2] [EX:ca_2025_2_midterm_q09 p.2]

같은 기준으로 비교하려면 microcoded multi-cycle의 instruction i latency를 cᵢtₘ, 정상 처리 간격을 평균 c̄tₘ으로 놓고, 5-stage pipeline의 hazard 없는 latency를 5tₚ, 정상 처리 간격을 tₚ로 놓는다. Multi-cycle은 instruction별 필요한 단계와 자원 재사용을 조절하고, pipeline은 instruction 사이의 겹침으로 처리 간격을 줄인다. 실제 pipeline에서는 처리 간격이 CPI×tₚ가 된다. Microcode ROM·dispatch나 hardwired control이라는 구현 방식만으로 tₘ, tₚ, c̄의 값을 알 수 없으므로 latency·clock speed·throughput의 보편적인 우열은 정해지지 않는다. [EX:ca_2025_2_midterm_q16 p.8]

## Instruction에 붙어서 이동하는 data와 control

### Destination도 pipeline을 통과해야 한다

Stage 사이의 IF/ID, ID/EX, EX/MEM, MEM/WB register는 한 instruction의 중간값을 다음 stage까지 운반한다. Instruction bits나 필요한 fields, PC 관련 값, operand와 immediate, ALU result, store data, load data, destination register 번호가 각각 필요한 경계까지 살아 있어야 한다. 모든 값이 모든 stage에서 새로 사용되는 것은 아니지만 나중에 쓸 값은 그때까지 보존해야 한다.

L07의 기존 ISA 예제 `lw $10, 20($1)` 다음에 `sub $11, $2, $3`가 오는 흐름을 시간표로 읽어 보자. 이 표의 register 표기는 해당 자료의 것이며 RV64 register 이름으로 바꾼 code가 아니다.

| Cycle | lw | sub |
|---|---|---|
| 1 | IF | — |
| 2 | ID | IF |
| 3 | EX: address 계산 | ID: operand 읽기 |
| 4 | MEM: load data 읽기 | EX: 뺄셈 |
| 5 | WB: $10에 쓰기 | MEM stage 통과 |
| 6 | — | WB: $11에 쓰기 |

`sub`의 MEM stage 통과가 memory write를 의미하지는 않는다. Cycle 5에서 load data를 쓸 destination은 여전히 `$10`이다. 현재 앞부분에서 decode하는 다른 instruction의 destination을 사용하면 data는 load의 것인데 register 번호는 다른 instruction의 것이 되는 오류가 생긴다. [computer_architecture:NM005 p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-030)의 cycle 3 그림에서는 왼쪽의 `sub` decode와 오른쪽의 `lw` execution이 동시에 보인다. 이처럼 한 instruction을 가로로 따라가는 operation view와 한 cycle의 여러 stage를 보는 resource view는 같은 실행을 다른 방향에서 읽은 것이다. [computer_architecture:NM005 p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-027).

### Control도 같은 instruction의 수명을 따른다

ID에서 만든 현재 instruction의 control로 MEM의 오래된 instruction을 직접 제어하면 같은 문제가 생긴다. 한 방법은 ID에서 한 번 decode하고 EX용, MEM용, WB용 control을 나누어 data와 함께 전달하는 것이다. EX에서 쓰고 끝나는 control은 거기서 소비하고, memory와 writeback에 필요한 control은 EX/MEM으로, WB용은 다시 MEM/WB로 전달한다. `RegWrite`나 writeback result select는 자신이 제어할 result와 destination에 맞춰 움직여야 한다. [computer_architecture:NM005 p.52](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-052).

다른 방법은 instruction의 필요한 fields를 운반하고 각 stage에서 local decode하는 것이다. 어느 방법이든 data와 control의 instruction 소속을 지켜야 한다. Decode-once는 control 배선을 전달하고, local decode는 필요한 instruction 정보와 stage별 decoder를 둔다. 그림만으로 어느 쪽이 모든 설계에서 더 작고 빠르다고 정할 수는 없다.

현실의 pipeline에서는 instruction들이 모두 같은 일을 하지 않고, 서로 의존하며, stage delay도 균등하지 않다. 따라서 multifunction stage와 선택 control, dependence 처리, stage 재분할이나 자원 증설을 각각 검토한다. 같은 memory port를 동시에 요구하는 **structural hazard**와 아직 준비되지 않은 값을 요구하는 **data hazard**는 원인이 다르다. RF처럼 cycle 안의 read/write 시점을 나누어 공유하는 자원도 있으므로 “한 stage에는 반드시 한 전용 자원”이라는 도식만으로 판단하지 않는다.

## Dependence가 hazard가 되는 조건

**RAW(read after write)**는 앞 instruction의 결과를 뒤 instruction이 읽어야 하는 true dependence다. 예를 들어 먼저 r3을 계산하고 뒤에서 r3으로 r5를 계산하면 뒤 계산에는 새 r3이 필요하다. **WAR(write after read)**는 앞 instruction이 읽어야 할 옛 값을 뒤 instruction이 너무 일찍 덮으면 안 된다는 제약이고, **WAW(write after write)**는 같은 destination에 쓰는 두 write의 최종 순서를 지켜야 한다는 제약이다. 같은 instruction 쌍에 여러 종류의 dependence가 함께 있을 수도 있다.

Dependence는 프로그램이 요구하는 순서이고 hazard는 특정 구현의 timing이 그 순서를 위협하는 상황이다. 모든 register read를 ID에서, 모든 write를 WB에서 수행하며 순서대로 진행하는 고정 5-stage 모델에서는 뒤 instruction의 write가 앞 instruction의 read나 write를 추월하지 않는다. 따라서 이 모델의 WAR·WAW dependence가 곧 WAR·WAW stall을 뜻하지는 않는다. 이 시간 순서를 설명하는 것이 복원 시험의 WAR 항목에 필요한 깊이다. [EX:ca_2025_2_midterm_q10 p.2]

Forwarding이 없고 ID에서 새 값을 읽으려면 producer의 WB가 먼저 끝나야 하는 L08 모델을 보자. Adjacent instruction의 distance를 1, 하나가 사이에 있으면 2로 정의한다. 이 모델에서는 같은 cycle의 WB 값을 ID가 즉시 읽지 못하므로 distance 1·2·3인 RAW가 문제가 되고 distance 4에서는 안전하다. 반대로 WB가 cycle 앞부분에 쓰고 ID가 뒷부분에 읽을 수 있는 RF에서는 경계가 달라진다. L07의 half-clock RF와 L08의 이 stall 계산을 섞어서는 안 된다. [computer_architecture:NM006 p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-013).

검사는 instruction bit field가 같다는 것만으로 끝나지 않는다. Producer가 실제로 register를 쓰는지, consumer가 그 field를 실제 source로 사용하는지, destination이 `x0`인지도 확인한다. 이 모델에서 R/I 연산, `lw`, `jal`, `jalr`는 register result를 만들 수 있다. `sw`와 branch는 GPR result를 만들지 않는다. R/I 연산, load의 base, store의 base와 data, branch operand, `jalr`의 base는 source 사용이지만 `jal`에는 GPR source가 없다. Opcode가 다른데 같은 bit 위치를 무조건 register source로 해석하면 거짓 hazard가 생긴다.

## Stall은 기다릴 instruction만 붙잡는다

값이 아직 RF에 없다면 consumer를 기다리게 해야 한다. **Stall(대기)**은 PC와 앞쪽 pipeline register를 hold하여 consumer와 그 뒤 instruction이 진행하지 않게 한다. 동시에 consumer가 EX로 들어갈 자리는 **bubble(유효한 일을 하지 않는 슬롯)**로 만든다. Bubble의 `RegWrite`와 `MemWrite`는 꺼져 있어야 한다. Producer를 포함한 뒤쪽 stage는 계속 진행해야 값을 완성할 수 있다. 모든 stage를 함께 멈추면 기다리는 값도 영원히 도착하지 않는다.

다음은 L08의 no-forwarding·동일 cycle RF read/write 불가 조건을 producer의 IF를 t0로 놓아 다시 쓴 시간표다. Adjacent consumer가 producer의 result를 읽는다.

| Cycle | Producer | Consumer |
|---|---|---|
| t0 | IF | — |
| t1 | ID | IF |
| t2 | EX | ID에서 대기 |
| t3 | MEM | ID에서 대기 |
| t4 | WB | ID에서 대기 |
| t5 | 완료 | ID: 새 값 읽기 |
| t6 | — | EX |
| t7 | — | MEM |
| t8 | — | WB |

세 번의 대기 동안 consumer 자체를 버리지 않는다. [computer_architecture:NM006 p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-018)의 원래 그림은 앞 instruction도 함께 그려 time origin이 다르므로, 숫자 label보다 producer의 WB와 consumer의 정상 ID 사이의 관계를 읽는 것이 중요하다. Hazard detector는 ID의 실제 두 source를 EX·MEM·WB의 유효한 destination과 비교한 여섯 match를 OR하는 방식으로 이해할 수 있다. 각 match에는 write enable과 `x0` 제외 조건이 붙는다.

정상 상태에서 유효 instruction N개에 stall cycle S개가 추가된다면 CPI=(N+S)/N=1+S/N, IPC=N/(N+S)다. 교육용 계산으로 N=100, S=25이면 CPI=1.25, IPC=0.8이다. 빈 5-stage pipeline의 시작부터 마지막 WB까지라면 fill/drain 4 cycle을 포함하여 129 cycle, IPC=100/129가 된다. 한 번의 stall이 여러 dependence를 동시에 해소할 수 있으므로 dependence마다 penalty를 따로 더해서는 안 된다.

## Forwarding과 load-use의 시간 경계

**Forwarding(우회 전달)**은 결과가 이미 계산되었지만 RF에는 아직 쓰이지 않았을 때 그 값을 consumer로 직접 보낸다. 기다리는 이유가 “WB까지 전달 경로가 없어서”였다면 도움이 되지만, 아직 계산되지 않은 값을 미리 만들지는 못한다.

같은 source register와 여러 in-flight destination이 일치하면 프로그램 순서상 가장 가까운 앞선 writer, 즉 youngest older producer의 값이 필요하다. L08의 검사 순서에서는 가까운 EX match가 더 오래된 MEM·WB match보다 우선한다. 가까운 writer가 load이고 결과가 아직 없다면, 더 오래된 writer의 준비된 값을 대신 쓰는 것은 오류다. 올바른 값이 준비될 때까지 기다려야 한다. [computer_architecture:NM006 p.42](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-042).

[computer_architecture:NM006 p.43](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-043)의 stage 표는 값을 **언제 사용하고 언제 생산하는지**를 구분한다.

| Instruction 종류 | Operand를 실제 사용하는 stage | Result가 나오는 stage |
|---|---|---|
| R/I arithmetic·logic | EX | EX |
| Load | EX에서 base/address 계산 | MEM |
| Store | EX에서 address 계산, MEM에서 store data 사용 | GPR result 없음 |
| Conditional branch | EX | GPR result 없음 |
| jal | GPR source 없음 | EX의 link result |
| jalr | EX | EX의 link result |

ALU producer가 t2의 EX 끝에서 값을 만들면 다음 consumer의 t3 EX로 전달할 수 있다. Load가 t2 EX에서 address를 만들고 t3 MEM 끝에서 data를 얻는다면, 바로 뒤 consumer의 t3 EX 시작에는 값이 없다. Consumer의 EX를 t4로 미루는 한 bubble이 필요한 이유다. 이를 **load-use hazard**라고 한다. ID에서 match를 검출하는 시점과 operand가 EX에서 필요한 시점도 구분해야 한다.

기본 검출식은 EX의 load가 읽는 destination과 ID consumer의 실제 source가 일치하는지, 그리고 `MemRead_EX`가 켜져 있는지를 확인한다. 그러나 source의 필요 시점을 생략하면 store를 잘못 다룬다. Store address의 base는 EX에서 필요하지만 store data는 MEM에서 필요하다. MEM까지의 store-data forwarding 경로가 있다면 같은 register dependence라도 EX operand와 stall 수가 다를 수 있다. “Load 뒤에서 그 register를 쓰면 언제나 한 stall”이라는 규칙은 충분하지 않다.

Trace를 작성할 때는 instruction마다 source·destination을 먼저 적고, 생산 stage와 소비 stage를 맞춘 뒤, 사용할 수 있는 bypass와 RF timing을 적용한다. 마지막 instruction의 WB까지 표를 늘려야 하며 인쇄된 표가 끝났다고 실행이 끝난 것은 아니다. 복원 시험의 dependence 식별·forwarding trace·stall 논의는 이 순서로 읽는다. 제공된 cycle 1–8 grid보다 뒤의 완료가 필요할 수 있고, 같은-cycle RF와 store-data bypass 조건이 명확하지 않은 경우 가정을 적어야 한다. [EX:ca_2025_2_midterm_q15 p.7]

## Static scheduling과 더 깊은 pipeline

### Loop의 operand 관계 읽기

L08의 MIPS-style 교육용 loop는 `j=i-1`로 시작하여 `j>=0`와 `v[j]>v[j+1]`를 검사한다. 아래 NM006 p.33의 명령열에서 `$s0`는 i, `$s1`은 j, `$a0`는 배열의 base address를 나타낸다. 점으로 표시된 loop body는 제공되지 않았으며, 이 명령열을 RISC-V program으로 바꾸어 읽으면 안 된다.

```asm
addi $s1, $s0, -1
for2tst: slti $t0, $s1, 0
bne $t0, $zero, exit2
sll $t1, $s1, 2
add $t2, $a0, $t1
lw $t3, 0($t2)
lw $t4, 4($t2)
slt $t0, $t4, $t3
beq $t0, $zero, exit2
.........
addi $s1, $s1, -1
j for2tst
exit2:
```

첫 `addi $s1, $s0, -1`은 i를 담은 `$s0`에서 1을 빼 `$s1`에 j=i−1을 만든다. 이 초기화는 `for2tst` 앞에 있으므로 반복할 때마다 i−1로 되돌리는 동작이 아니다. `for2tst`의 `slti $t0, $s1, 0`은 j<0이면 `$t0=1`, 그렇지 않으면 0을 만든다. 이어 `bne $t0, $zero, exit2`는 이 flag가 0이 아닐 때 종료한다. 따라서 j가 음수이면 뒤의 배열 조건으로 진행하지 않고, j가 0 이상일 때만 다음 비교로 진행하는 guard이다.

`sll $t1, $s1, 2`는 j를 두 bit 왼쪽으로 옮겨 4-byte word 원소의 byte offset 4j를 만든다. 이어 `add $t2, $a0, $t1`이 배열의 base address인 `$a0`에 그 offset을 더하므로 `$t2=base+4j`가 v[j]의 주소다. 두 `lw`는 같은 base register `$t2`를 사용하되 offset 0과 4로 이웃한 두 word에 접근한다.

첫 load는 v[j], 둘째는 v[j+1]을 읽는다. 마지막 비교는 `$t4 < $t3`, 즉 v[j+1]<v[j]이므로 원래 조건과 맞는다. 피연산자 순서를 바꾸면 조건이 달라진다. [computer_architecture:NM006 p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-033).

`slt $t0, $t4, $t3`가 1을 만들 때에만 v[j]>v[j+1]이 참이다. 다음 `beq $t0, $zero, exit2`는 비교 결과가 0이면, 즉 v[j]≤v[j+1]이면 종료한다. 두 guard를 모두 통과해야 점으로 생략된 body에 도달한다. 이 점들은 swap instruction을 확인한 근거가 아니다. 생략된 body 뒤의 `addi $s1, $s1, -1`은 j를 1 줄이고, `j for2tst`는 음수 검사부터 guard를 다시 수행하게 한다. 이로써 초기화→guard→주소와 값 비교→body→decrement→guard의 반복을 읽을 수 있지만, body의 실제 동작은 이 자료만으로 알 수 없다.

Forwarding 없는 자료의 표시에서는 `addi→slti`, `slti→bne`, `sll→add`, `add→첫 lw`, `둘째 lw→slt`, `slt→beq`의 여섯 인접 RAW마다 세 stall이 붙는다. 이것은 해당 표시 지점의 설명이지, 생략된 loop body와 branch outcome까지 포함한 전체 실행 cycle 수가 아니다. [computer_architecture:NM006 p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-034).

**Static scheduling**은 compiler가 program 의미를 유지하면서 독립 instruction을 기다리는 구간에 배치하는 방법이다. **Interlock**은 hardware가 실행 중 hazard를 검출하고 기다리게 하는 장치다. Stall·flush·forwarding 같은 실행 중 처리는 정적으로 instruction 순서를 바꾸는 것과 구별된다.

자료의 MIPS R2000 **load delay slot**에서는 load 바로 다음 instruction이 그 결과를 사용하지 않도록 해야 한다. 필요한 최소 distance는 2이며, 자료는 둘째 load와 `slt` 사이에 `nop`을 넣는다. 안전하게 옮길 독립 instruction이 있으면 유용한 일을 할 수 있지만, 없으면 `nop`이 순서를 보장한다. 이 조건은 load result의 도착 시점에 관한 것이며 뒤에서 다룰 branch delay slot과 다르다. [computer_architecture:NM006 p.47](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-047).

p.47에서도 초기화, 두 guard와 주소 계산, 생략된 body 뒤의 j 감소와 `j for2tst`는 같은 역할이다. 추가된 `nop`은 둘째 `lw`와 그 결과를 쓰는 `slt` 사이의 load-use slot을 채운다. 점으로 남은 body나 별도의 branch delay-slot instruction을 이 그림에서 복원할 수는 없다.

### Clock을 줄여도 dependence의 간격은 남는다

**Superpipelining**은 stage를 더 잘게 나누는 선택이다. 자료의 32-bit adder 예에서는 EX1에서 아래 16 bits와 carry를 계산하고 EX2에서 위 16 bits와 전달된 carry를 처리한다. 먼저 계산한 하위 결과와 나중에 계산한 상위 결과가 같은 연산에 속하도록 저장·정렬해야 완전한 32-bit 결과가 된다. [computer_architecture:NM006 p.49](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-049).

짧은 stage는 clock을 줄일 수 있지만 다음 dependent instruction이 완전한 결과를 기다려야 하는 cycle 수는 늘어날 수 있다. Stage register overhead와 branch penalty도 함께 보아야 한다. ISA가 정한 순차적 결과를 유지하는 범위에서 내부 실행을 겹칠 수 있다는 사실과, 서로 의존하는 연산의 순서를 무시할 수 있다는 주장은 다르다. Pipeline의 장점과 한계를 비교할 때 throughput만이 아니라 latency, 자원·제어 비용, hazard 처리까지 연결하는 것이 복원 시험의 비교 항목과 맞닿는다. [EX:ca_2025_2_midterm_q16 p.8]

## PC dependence와 다음 fetch

Control flow에서도 consumer와 producer를 찾을 수 있다. 모든 instruction fetch는 PC를 소비하며, 앞 instruction은 다음 PC를 결정한다. 따라서 **control dependence**는 다음 instruction 주소에 대한 data dependence로 볼 수 있다. [[courses/computer_architecture/transcripts/undated-control-hazards-tskkzbwcgg2lavgo|날짜 미확인 강의 (computer_architecture:NT002)]] 05:10은 PC도 register라는 관점으로 이를 설명한다. 이 절부터의 L09 내용은 course study에 속하지만 현재 중간고사 cutoff인 L08+Lab1을 넘는다.

이 날짜 미확인 전사는 원음 검증 없이 자료와 대조한 텍스트이며 완전한 축어 복원이 아니다. 빠진 발화, 실제 수업 날짜와 화자 신원은 복원되지 않았다.

L09의 보수적 모델에서는 일반 R/I·load·store의 next PC를 ID에서, conditional branch·`jal`·`jalr`의 next PC를 EX에서 알게 된다고 둔다. Fetch는 IF에서 그 주소를 필요로 한다. [computer_architecture:NM007 p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-005). 예측 없이 확정된 next PC만 기다리면 non-branch h가 t0 IF, t1 ID를 수행한 뒤 다음 instruction i는 t2에야 IF로 들어온다. 같은 조건이 반복되면 j는 t4, k는 t6에 fetch된다. Branch가 아니어도 fetch 사이에 빈 cycle이 생긴다. 이 “어느 stage에서 알게 되는가”는 ISA 자체의 불변 규칙이 아니라 이 datapath의 가정이다.

Sequential PC를 미리 선택하면 이 기다림을 줄일 수 있다. **Speculation(추측 실행)**은 아직 확정되지 않은 선택을 따라 먼저 일을 진행하는 것이다. 여기서는 4-byte instruction 모델의 PC+4를 예측한다. 예측이 맞으면 결과를 그대로 사용할 수 있지만, 틀리면 잘못된 경로의 instruction이 architectural state를 바꾸지 못하게 해야 한다.

## Branch resolution, redirect와 flush

ID에서 branch임을 알아도 그 branch의 taken 여부와 target이 모두 확정된 것은 아니다. 날짜 미확인 강의 computer_architecture:NT002 17:37은 이 구분을 강조한다. 아래 표는 branch h가 EX 끝에서 taken으로 판명되고 올바른 target instruction이 k인 L09 모델이다. i와 j는 순차 경로에서 잘못 fetch한 instruction이다.

| Cycle | h | i | j | k |
|---|---|---|---|---|
| t0 | IF | — | — | — |
| t1 | ID | IF | — | — |
| t2 | EX: 끝에서 taken 확정 | ID | IF | — |
| t3 | MEM | EX 자리의 bubble | ID 자리의 bubble | IF |
| t4 | WB | MEM 자리의 bubble | EX 자리의 bubble | ID |
| t5 | 완료 | WB 자리의 bubble | MEM 자리의 bubble | EX |
| t6 | — | — | WB 자리의 bubble | MEM |
| t7 | — | — | — | WB |

**Redirect**는 fetch PC를 k로 바꾸는 일이고, **flush**는 i·j의 유효성을 없애는 일이다. t3에 k가 IF로 들어가도 잘못 들어온 i·j의 자리가 즉시 유효한 일로 채워지지는 않는다. Bubble이 뒤로 진행하며 memory/register write 같은 side effect를 만들지 않는다. Branch h와 그보다 오래된 올바른 instruction을 함께 지우는 것도 아니다. [computer_architecture:NM007 p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-022); [[courses/computer_architecture/transcripts/undated-control-hazards-tskkzbwcgg2lavgo|날짜 미확인 강의 (computer_architecture:NT002)]] 23:27.

Stall은 나중에 계속 실행할 instruction을 보존하고, flush는 실행하면 안 되는 instruction을 무효화한다. 이 모델의 두 bubble은 잘못된 fetch 두 개에 대응하는 2-cycle penalty다. 모든 processor의 branch penalty가 2라는 뜻은 아니다. 예측이 맞을 때 penalty가 없다는 설명도 다른 data/resource hazard가 없다는 조건 아래의 말이다.

## Misprediction 확률과 CPI·IPC

L09의 program profile은 control-flow instruction 비율 20%, forward branch taken 비율 50%, backward branch taken 비율 90%, 전체 control-flow의 taken 비율 70%를 제시한다. Forward/backward는 target 주소의 방향이며 실행 시간의 앞뒤가 아니다. 두 방향의 개수 비중을 모르면 50%와 90%만으로 전체 70%를 계산할 수 없으므로, 여기서는 전체 70%를 별도로 주어진 값으로 사용한다. [computer_architecture:NM007 p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-012). [computer_architecture:NM007 p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-030); [computer_architecture:NM007 p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-031).

Predict-not-taken에서 non-control-flow 80%는 순차 PC 선택이 맞고, control-flow 중 30%도 not taken이다. 따라서

- Correct-guess probability = 0.8 + 0.2×0.3 = 0.86.
- Wrong-guess probability = 0.2×0.7 = 0.14.
- 이상적 CPI=1, 추가 data hazard 없음, misprediction당 2 cycle이면 CPI = 1 + 0.14×2 = 1.28.
- IPC = 1/1.28 = 0.78125, 약 0.78.

같은 비율을 100개의 유효 instruction에 적용하면 86개는 맞고 14개는 틀린다. 틀린 14개가 28 cycle을 추가하므로 정상 상태 기준 128 cycle이다. 이 계산에는 fill/drain이 들어 있지 않다. `0.28`은 instruction당 추가 cycle이고, IPC 감소량은 1−0.78125=0.21875다. 같은 instruction 수와 clock을 비교할 때 실행 시간은 28% 늘고 처리율은 21.875% 줄므로 두 백분율을 같은 양으로 쓰지 않는다.

날짜 미확인 강의의 14:56·26:58·27:42·28:41에는 이 확률·IPC·penalty와 일치하지 않거나 양이 모호한 숫자 표현이 남아 있다. 위 계산은 자료의 20%·70%와 2-cycle 모델을 이용한 명시적 수학 설명이며, 그 발화를 정확한 공식처럼 고쳐 인용한 것이 아니다. 또한 “data hazard를 제외한다”는 계산 가정은 프로그램에 data dependence가 없다고 선언하는 말이 아니다.

성능 개선은 세 요소를 나누어 생각한다. Control-flow 빈도는 program의 성질이고, 그중 얼마나 틀리는가는 prediction accuracy이며, 한 번 틀릴 때 잃는 cycle은 resolution·redirect 시점 등 구현의 성질이다. 더 정확한 prediction은 틀리는 횟수를 줄이고, 더 이른 resolution은 한 번의 손실을 줄일 수 있다. 강의 27:42의 구현별 차이는 이 구분과 연결된다. 자세한 predictor algorithm은 여기서 주어진 근거를 넘는다. 조건이 compile time에 알려졌다는 이유로 branch를 단순화하려면 실제 조건 값과 관련 side effect 보존까지 확인해야 하며, 불분명한 강의 변수값만으로 “항상 참인 branch”를 만들 수는 없다.

## Branch delay slot의 architectural 의미

자료의 MIPS R2000 **branch delay slot**은 branch 바로 뒤 PC+4 instruction을 taken 여부와 관계없이 실행하는 architectural 규칙이다. 그 다음 instruction 주소, 즉 두 번째 successor는 taken이면 target, not taken이면 PC+8이다. 이는 잘못 예측한 순차 instruction을 flush하는 앞의 모델과 다른 계약이다. [computer_architecture:NM007 p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-032)의 그림에서 볼 것은 branch 직후 instruction의 자리가 유지되고, 이른 branch 결정이 그 다음 fetch를 선택한다는 점이다.

Compiler가 slot에 instruction을 옮기려면 taken과 not-taken 양쪽에서 그 실행이 program 의미를 보존하는지 확인해야 한다. 한쪽 경로에서만 필요한 store나 아직 준비되지 않은 operand를 쓰는 연산을 무심코 옮길 수는 없다. 적절한 instruction이 없으면 `nop`으로 채운다. 자료의 약 80% 채움 언급은 해당 역사적 설명의 수치이며 모든 program에 대한 보장이나 현재 compiler 성능이 아니다. Slot을 유용한 일로 채우고 다른 hazard가 없다면 이상적인 IPC=1에 접근할 수 있지만, `nop`까지 “유용한 instruction”으로 세어 성능을 부풀려서는 안 된다.

Load delay slot은 load result의 사용 간격에 관한 것이고 branch delay slot은 branch 다음 instruction의 실행 의미에 관한 것이다. 둘 다 compiler에 제약을 보이지만 같은 규칙이 아니다. 복원 시험의 관련 항목은 ISA에 노출된 이 의미와 hardware bubble을 구분하는 데 활용할 수 있다. L09를 현재 중간고사 범위로 추가하는 근거는 아니다. [EX:ca_2025_2_midterm_q17 p.8]

## Speculation의 architectural effect와 cache state

잘못된 경로의 instruction을 flush하면 architectural register나 memory의 잘못된 갱신을 막아야 한다. 그러나 그런 갱신을 막았다는 사실만으로 실행의 모든 흔적이 사라지는 것은 아니다. Cache에 어떤 data가 들어왔는지 같은 **microarchitectural effect**가 남으면 이후 접근 시간이 달라질 수 있다. Functional correctness를 위한 state 복구와 관찰 가능한 내부 효과를 없애는 문제는 구분해야 한다.

[computer_architecture:NM007 p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-033)의 권한 조건 예는 조건 뒤의 접근을 추측 실행할 때 어떤 흔적이 남을 수 있는지 생각하게 한다. [[courses/computer_architecture/transcripts/undated-control-hazards-tskkzbwcgg2lavgo|날짜 미확인 강의 (computer_architecture:NT002)]] 35:17–35:35도 cache state로 설명을 이어간다. 이 수준에서 말할 수 있는 것은 “architectural 결과를 취소해도 cache 같은 내부 상태는 별도로 검토해야 한다”는 원리다. Cache hit/miss와 timing 관찰의 구체적인 mechanism은 이후 cache 학습과 연결된다.

이 조건문만으로 실제 machine code의 branch 방향, 권한 검사 우회 방식, 공격자가 읽을 수 있는 범위까지 결정되지는 않는다. 강의에 등장하는 Spectre와 Meltdown이라는 이름도 서로 다른 mechanism을 하나로 합치는 근거가 아니다. 여기의 pipeline 예시는 모든 processor가 같은 취약성을 갖는다는 주장이나 현재 제품의 보안 상태 판정이 아니다.

## 확인·연습문제

### 복습 순서

Q01–Q05에서 자원과 저장값을 말로 설명한 뒤 Q06–Q09와 P01로 유한 실행시간을 계산하세요. Q10–Q18과 P02는 producer→consumer 표와 cycle trace를 먼저 쓰고 해설로 대조하세요. Q19–Q24와 P03–P04는 시험 범위 밖의 보충으로, PC 결정·flush·확률 단위를 차례로 확인하세요.

### Microcode와 자원 공유

#### 확인 Q01 · μPC와 dispatch

μPC, μprogram ROM, incrementer, dispatch ROM과 `AddrCtl`의 역할을 연결하라. μPC=5일 때 `AddrCtl=0`과 `3`의 다음 주소, `1`에서 R-format의 주소를 구하고, `lw`·`sw`가 두 dispatch에서 어떻게 갈라지는지 설명하라.

<details><summary>해설 보기</summary>

μPC는 사용자 PC가 아니라 현재 microinstruction의 주소이고, μprogram ROM은 그 주소의 datapath control과 다음 주소 선택을 낸다. Incrementer는 μPC+1을, dispatch ROM은 opcode별 주소를 만든다. `AddrCtl=0`이면 0, `3`이면 6이다. `1`은 ROM 1, `2`는 ROM 2를 고른다. ROM 1에서 R-format `000000`은 `0110`, `jmp`는 `1001`, `beq`는 `1000`으로 가며 `lw`·`sw`는 모두 `0010`으로 간다. ROM 2에서는 `lw→0011`, `sw→0101`이므로 공통 주소 계산 뒤 후속 동작을 나눌 수 있다. 이 6-bit opcode 예제의 주소 6을 별도 RISC-V FSM의 state 6으로 해석할 수 없다. 인쇄 표의 `0110`과 41:27의 불명확한 0,1,0 발화는 구분한다. 37:51의 lookup-input 표현도 μPC로 주소를 정하는 ROM 설명으로 발화를 복원했다는 뜻은 아니다.

확인 기준: 네 `AddrCtl` 선택, μPC와 PC의 차이, load/store의 공통·분리 경로, 별도 opcode namespace를 모두 확인한다.

근거: [L06 p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-014) · [L06 p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-015)

</details>

#### 확인 Q02 · 같은 ALU의 두 계산

4-byte instruction 모델에서 PC=`0x3000`이고 현재 instruction은 10+12를 계산한다. IF와 EX의 ALU 입력·결과·목적을 적어라. 두 입력을 RF에 고정하면 무엇이 안 되며, 공유의 비용과 bit-width 주의점은 무엇인가?

<details><summary>해설 보기</summary>

IF는 PC와 4로 `0x3004`라는 다음 주소를 만든다. EX는 10과 12로 연산 결과 22를 만든다. 입력을 RF로 고정하면 PC와 상수 4를 선택할 수 없으므로 mux와 단계별 control이 필요하다. 두 결과는 필요한 시점까지 따로 보존해야 하며 같은 ALU가 두 덧셈을 동시에 하지는 않는다. Adder 중복을 줄이는 대신 mux 지연·저장소·control과 cycle 비용을 검토한다. PC+4는 이 4-byte 모델의 조건이다. L06·L07의 16→32-bit immediate 그림을 RV64의 32-bit instruction/64-bit data와 섞지 않는다.

확인 기준: 주소 `0x3004`와 data 22를 구별하고 입력 선택·저장·시간 비용을 설명한다.

근거: [L06 p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-020)

</details>

#### 확인 Q03 · 조기 PC 갱신과 IR

PC=A에서 instruction K를 fetch한 뒤 남은 단계 전에 PC를 A+4로 바꾼다. Combinational instruction memory와 IR의 유무에 따라 decode가 보는 것이 어떻게 달라지는가? IR에 주소 A를 저장하면 해결되는가?

<details><summary>해설 보기</summary>

IR 없이 memory 출력을 바로 decode하면 PC 변경이 memory에 전파되어 다음 instruction의 opcode·operand field를 보게 될 수 있다. IR은 A 자체가 아니라 A에서 읽은 K의 instruction bits를 capture하고, K의 남은 단계 동안 hold해야 한다. 그러면 memory 출력이 달라져도 decode는 K를 유지한다. 그림은 저장 경계의 이유를 설명하지만 특정 latch active level이나 setup time을 정하지 않는다. 전사의 PC/IR 혼용 표현을 정확한 저장 내용의 정의로 사용하지 않는다.

확인 기준: 변화의 전파 경로, instruction bits의 capture/hold, 주소와 비트열의 차이를 확인한다.

근거: [L06 p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-021) · [L06 p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-022)

</details>

#### 확인 Q04 · 중간값의 수명

IR·MDR·A·B·ALUOut에 어떤 값이 남는가? Load와 store에서 주소·data가 살아 있어야 하는 시점을 설명하고, 한 memory의 multi-cycle 공유가 pipeline의 IF/MEM 동시 접근까지 해결하는지 판단하라.

<details><summary>해설 보기</summary>

IR은 instruction bits, MDR은 memory read data, A·B는 RF에서 읽은 operand, ALUOut은 ALU 결과나 유효 주소를 보존한다. Load는 계산한 주소를 memory access까지, 반환 data를 WB까지 유지한다. Store는 주소와 쓸 data를 memory write까지 함께 유지한다. 이들은 내부 실행 상태이며 programmer-visible GPR와 다르다. 한 명령의 서로 다른 cycle에 memory를 쓰는 것은 가능하지만, pipeline에서 서로 다른 명령의 IF와 MEM이 같은 single-port memory를 동시에 요구하면 structural conflict가 남는다. 9월 29일의 예고만으로 전체 pipeline 제어를 배웠다고 할 수 없다.

확인 기준: 다섯 저장소의 의미와 load/store의 수명, 순차 공유와 동시 충돌을 구분한다.

근거: [L06 p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-023)

</details>

#### 확인 Q05 · 복잡성의 위치

복잡한 instruction을 전용 datapath로 처리하는 방법과 단순 datapath의 긴 μprogram으로 처리하는 방법을 비교하라. Loop counter는 왜 필요할 수 있고, 반드시 ISA register가 되는가?

<details><summary>해설 보기</summary>

전용 회로는 많은 일을 하드웨어에 넣어 control sequence를 짧게 할 수 있지만 면적·delay·설계 부담을 가진다. 단순 datapath를 재사용하면 micro-operation 수, control memory, sequencing과 내부 state 비용이 커질 수 있다. μprogram이 반복하면 횟수를 기억할 loop counter가 필요하지만 이는 내부 μISA state이며 자동으로 프로그램의 GPR가 되지는 않는다. 자료의 RISC simple datapath/simple control은 또 하나의 설계 방향이다. 세 방향의 latency·면적·control 비용을 비교해야 하며 microcode라는 이름만으로 우열을 정할 수 없다.

확인 기준: 회로 비용과 sequence 비용을 함께 비교하고 내부 state와 architectural state를 구별한다.

근거: [L06 p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-024)

</details>

### Pipeline의 시간과 상태

#### 확인 Q06 · 처리율·latency·비용

각 30분인 네 세탁 단계의 한 작업 latency와 정상 완료 간격은? 건조가 60분이면 무엇이 바뀌고 두 건조기는 무엇을 회복하는가? 균등 k-stage에서 총 logic delay T, 경계 overhead S>0, logic cost G, 경계 cost L의 clock·latency·cost와 처리율 상한을 써라.

<details><summary>해설 보기</summary>

균등 세탁의 latency는 4×30=120분, 충분히 채운 뒤 완료 간격은 30분이다. 건조가 60분이면 한 작업은 150분이고 병목 때문에 완료 간격은 60분이다. 두 건조기를 교대로 사용하면 새 작업을 30분마다 받아 정상 간격을 30분으로 회복하지만 개별 작업의 건조는 여전히 60분이고 자원이 추가된다. 균등 logic 분할에서는 clock=T/k+S, 한 작업 latency=T+kS, cost=G+kL, rate=1/(T/k+S)이다. 비분할은 T+S, G+L이고, k가 커질 때 rate는 1/S에 접근한다. 불균형이면 clock을 가장 느린 stage가 제한한다.

확인 기준: 첫 완료와 정상 간격, 추가 자원, S에 따른 상한·latency·cost 증가를 모두 확인한다.

근거: [L07 p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-006) · [L07 p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-007) · [L07 p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-008) · [L07 p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-011) · [L07 p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-012)

</details>

#### 확인 Q07 · 빈 pipeline의 계산

L07의 stage delay 200·100·200·200·100ps를 쓰고 overhead와 hazard를 무시하라. 첫 instruction, 독립 instruction 3개, 정상 상태 처리율을 single-cycle과 비교하라. L06의 200·50·100·200·50ps를 섞으면 안 되는 이유도 설명하라.

<details><summary>해설 보기</summary>

L07 single-cycle은 합계 800ps이다. Pipeline clock은 최댓값 200ps, 첫 instruction latency는 5×200=1000ps이다. 빈 5-stage pipeline의 N개 완료는 N+4 cycle이므로 3개는 7×200=1400ps, single-cycle은 2400ps이고 유한 speedup은 12/7≈1.714다. 정상 완료 간격은 200ps여서 장기 throughput은 4배다. 5-stage라는 이유로 latency가 줄거나 5배 빨라지지 않는다. L06의 합계 600ps는 별도 부품 지연 모델이며 두 표를 섞으면 근거 없는 새 모델이 된다. L07의 half-clock RF 가정도 L08 no-forwarding의 같은-cycle 읽기 불가 조건과 구분한다.

확인 기준: 800·200·1000·1400ps와 12/7·4의 서로 다른 의미, N+4의 근거를 확인한다.

근거: [L07 p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-015) · [L07 p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-016) · [L06 p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-005)

</details>

#### 확인 Q08 · Load와 SUB의 소속

본문의 `lw $10, 20($1)` 뒤 `sub $11, $2, $3`가 hazard 없이 실행된다. Cycle 1–6의 stage를 나열하고 cycle 5의 writeback 값·destination 소속을 설명하라. Pipeline register가 data 외에 무엇을 보존해야 하며 operation/resource view는 어떻게 다른가?

<details><summary>해설 보기</summary>

`lw`는 IF1→ID2→EX3→MEM4→WB5, `sub`는 IF2→ID3→EX4→MEM5→WB6이다. Cycle 5의 writeback은 load data와 `$10`을 짝지어야 한다. SUB는 MEM 자리를 통과하면서 자신의 ALU result와 `$11`을 유지할 뿐 memory write를 하지 않는다. IF/ID·ID/EX·EX/MEM·MEM/WB는 필요한 instruction fields, PC 관련 값, operand/immediate, address/result, store/load data와 destination을 소비 시점까지 운반한다. Operation view는 한 instruction의 시간 흐름, resource view는 한 cycle의 동시 점유이다. Cycle 3의 load EX와 SUB ID는 두 관점에서 같은 사건이다.

확인 기준: 여섯 cycle, 올바른 data/destination 짝, MEM 통과와 memory 효과의 차이를 확인한다.

근거: [L07 p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-020) · [L07 p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-027) · [L07 p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-030)

</details>

#### 확인 Q09 · Control도 함께 이동한다

ID의 새 store가 만든 `MemWrite=1`을 현재 MEM에 곧바로 적용하면 왜 위험한가? Decode-once와 local-decode를 비교하고 현실의 pipeline에서 동일 작업·독립 작업·균등 stage라는 이상이 각각 깨지는 이유와 대응을 설명하라.

<details><summary>해설 보기</summary>

현재 MEM의 instruction은 ID의 새 store보다 오래되므로 새 control을 직접 주면 다른 instruction의 memory 효과를 바꾼다. Decode-once는 ID에서 EX/MEM/WB control을 만들고 사용 단계까지 data와 함께 전달한다. EX control은 EX에서 소비하고 MEM/WB를 EX/MEM으로, WB를 MEM/WB로 보낸다. Local decode는 필요한 instruction fields를 전달하고 stage별 decoder를 둔다. 어느 쪽도 보편적 우월성이 없다. 서로 다른 instruction에는 multifunction stage와 선택 control, 의존성과 자원 충돌에는 검출·대기·forwarding 또는 자원 증설, 불균형 delay에는 stage 재분할이 필요하다. Single-port 충돌은 structural이고 미완성 operand 문제는 data hazard다.

확인 기준: 명령별 control 소속, 두 decode 방식, 세 현실 제약과 원인별 대응을 확인한다.

근거: [L07 p.52](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-052) · [L07 p.55](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-055)

</details>

### Data hazard와 우회

#### 확인 Q10 · Dependence와 hazard

A: `r3←r1+r2`, B: `r5←r3+r4`, C: `r3←r6+r7`의 RAW·WAR·WAW를 찾아라. 모든 read=ID, write=WB이고 순서대로 진행하는 고정 5-stage에서 WAR·WAW가 반드시 stall을 일으키는가? 복기 Q10(p.2)과의 연결은 읽기·쓰기 순서가 WAR hazard를 실제로 만들 수 있는지 설명하는 추론이다. [EX:ca_2025_2_midterm_q10 p.2]

<details><summary>해설 보기</summary>

A→B의 r3는 RAW: B가 A의 새 값을 읽어야 한다. B→C의 r3는 WAR: B의 읽기 뒤 C의 overwrite가 와야 한다. A→C의 r3는 WAW: 최종 r3는 C의 값이어야 한다. Dependence는 필요한 프로그램 순서이고 hazard는 실행 timing이 그 순서를 위협하는 경우다. 주어진 고정 in-order 모델에서는 C의 WB가 B의 ID나 A의 WB를 추월하지 않으므로 WAR·WAW가 자동으로 stall을 만들지 않는다. RAW도 값이 필요한 때 준비되었는지 확인해야 한다.

확인 기준: 세 관계의 register와 순서를 쓰고 dependence 존재만으로 hazard를 단정하지 않는다.

근거: [L08 p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-004) · [L08 p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-013)

</details>

#### 확인 Q11 · 실제 source와 거리

No-forwarding이고 WB의 새 값을 같은 cycle ID에서 읽을 수 없다. Producer와 consumer 사이에 독립 instruction이 하나 있으면 RAW hazard인가? 거리 3·4는 어떤가? R/I·load·store·branch·`jal`·`jalr`의 GPR read/write와 `x0` 조건을 포함하여 설명하라.

<details><summary>해설 보기</summary>

인접 거리를 1로 세므로 하나가 끼면 거리 2이고, L08의 distance≤3 조건에 해당한다. 거리 3은 WB와 ID가 같은 cycle이어서 아직 기다려야 하고, 거리 4는 WB 다음 cycle ID이므로 안전하다. R/I 연산·load·`jal`·`jalr`는 GPR writer가 될 수 있고 store·branch는 아니다. R/I operands, load base, store base/data, branch operands, `jalr` base는 실제 source이지만 `jal`에는 GPR source가 없다. Match에는 실제 `RegWrite`, opcode별 source use, `x0` 제외가 필요하다. WB 앞부분 write/ID 뒷부분 read를 허용하면 거리 3의 결론이 바뀐다.

확인 기준: 거리의 정의, equality의 RF 조건, producer/consumer 종류와 `x0`를 모두 확인한다.

근거: [L08 p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-013)

</details>

#### 확인 Q12 · 누구를 멈추고 누구를 진행시키나

Producer가 t0 IF→t4 WB이고 인접 consumer가 t2 ID에 도착한다. No-forwarding·같은-cycle 새 RF 값 읽기 불가 조건에서 consumer의 정상 ID부터 WB까지와 bubble 수를 써라. Hold 대상과 hazard detector의 여섯 비교도 설명하라.

<details><summary>해설 보기</summary>

Consumer는 t2·t3·t4에 기다린 뒤 t5 ID→t6 EX→t7 MEM→t8 WB한다. PC와 upstream instruction 저장소는 hold하고 EX에는 세 bubble을 넣는다. Bubble은 `RegWrite=0`, `MemWrite=0`이어야 한다. Producer가 있는 downstream은 계속 진행해야 t4에 결과를 쓸 수 있다. ID의 실제 두 source 각각을 EX·MEM·WB의 destination과 비교하므로 2×3=6 match를 OR한다. 각 match는 source use, 유효한 writer의 `RegWrite`, non-`x0` 조건을 갖는다. Consumer를 보존하는 stall은 wrong-path instruction을 버리는 flush와 다르다.

확인 기준: t5 재개·t8 완료·세 bubble을 확인하고 producer까지 freeze하는 답은 배제한다.

근거: [L08 p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-018) · [L08 p.29](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-029) · [L08 p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-031)

</details>

#### 확인 Q13 · Stall과 유한 실행의 회계

100개의 유효 instruction에 추가 stall 25 cycle이 관측되었다. 정상 상태 CPI·IPC와 빈 5-stage pipeline에서 마지막 WB까지의 cycle·IPC를 구하라. 두 dependence의 별도 대기 횟수를 언제나 더하면 되는가?

<details><summary>해설 보기</summary>

정상 회계는 100+25=125 cycle이므로 CPI=125/100=1.25, IPC=100/125=0.8이다. 빈 pipeline의 전체 실행은 fill/drain 4 cycle을 더한 129 cycle, IPC=100/129≈0.7752이다. 같은 stall 동안 여러 producer가 진행하여 여러 dependence를 함께 해결할 수 있으므로 dependence별 penalty 합이 실제 S라는 보장은 없다. 실제 schedule에서 추가된 cycle을 세어야 한다.

확인 기준: 유효 instruction 분모/분자와 cycle 단위를 지키고 fill/drain 4를 한 번만 더한다.

근거: [L08 p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-032)

</details>

#### 확인 Q14 · 가장 가까운 writer

한 consumer source와 EX의 load destination, MEM의 오래된 ALU destination이 모두 일치한다. MEM 값은 준비되었지만 load data는 없다. 무엇을 선택해야 하는가? EX→MEM→WB 우선순위는 값이 만들어지는 stage와 같은 말인가?

<details><summary>해설 보기</summary>

Consumer가 필요로 하는 것은 프로그램 순서상 마지막으로 그 register를 쓴 older instruction, 즉 더 가까운 EX load의 결과다. 준비된 MEM 값을 대신 고르면 이전 버전을 읽어 잘못된다. 필요한 만큼 기다린 뒤 load 값을 전달해야 한다. EX→MEM→WB는 matching producer의 나이 우선순위이며 모든 결과가 EX에 준비된다는 뜻은 아니다. ID에서 match를 검출하는 것과 EX/MEM에서 operand를 소비하는 것도 구별한다. 실제 source와 non-`x0` 조건을 적용한다.

확인 기준: 최신 producer를 먼저 정하고 readiness와 경로를 확인하는 순서를 설명한다.

근거: [L08 p.37](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-037) · [L08 p.42](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-042)

</details>

#### 확인 Q15 · 생산 시점과 소비 시점

ALU producer는 t2 EX 끝, load producer는 t3 MEM 끝에 결과를 낸다고 하자. 다음 instruction이 t3 EX 시작에 값을 필요로 하면 각각 어떻게 되는가? Store base와 store data, branch와 `jal`·`jalr`의 사용/생산 stage도 구별하라.

<details><summary>해설 보기</summary>

ALU 결과는 t3 EX로 forward할 수 있다. Load 결과는 t3 EX 시작에 아직 없으므로 한 bubble로 consumer EX를 t4로 늦춘다. ID에서 실제 source가 EX load의 rd와 match하고 `MemRead_EX`가 참인지 검사하되 source의 필요 시점도 확인한다. R/I는 EX에서 operand를 쓰고 결과를 만들며 load는 EX에서 base를 쓰고 MEM에서 data를 만든다. Store base는 EX, store data는 MEM에서 필요하고 GPR result는 없다. MEM으로의 store-data bypass가 있으면 인접 load→store-data는 EX-use와 다르게 처리할 수 있다. Branch는 EX에서 operands를 쓰고 GPR result는 없다. `jal`은 GPR source 없이 EX link result를, `jalr`는 EX source use와 EX link result를 갖는 자료 모델이다.

확인 기준: 한 load-use bubble의 시간 원인, store의 두 소비 시점, instruction별 table을 확인한다.

근거: [L08 p.43](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-043)

</details>

#### 확인 Q16 · Loop의 비교 방향과 RAW

자료 loop의 `slti`, 2-bit `sll`, 두 `lw`, `slt $t0, $t4, $t3`가 각각 무엇을 뜻하는지 설명하라. No-forwarding 표시의 여섯 인접 RAW를 나열하고 그 표시만으로 전체 loop CPI를 정할 수 있는지 판단하라.

초기화와 반복 진입을 구분하여 `bne`·`beq`의 두 종료 조건, `base+4j` 주소, body 뒤 j 감소와 `j for2tst`의 복귀 위치까지 설명하라.

<details><summary>해설 보기</summary>

`j=i-1` 뒤 `slti`는 j<0을 검사하여 종료 판단에 쓰이고, `sll` 2는 4-byte 원소의 offset 4j를 만든다. Base에 더해 v[j] 주소를 얻고 첫 `lw`는 v[j], 다음 `lw`는 v[j+1]을 읽는다. `slt $t0, $t4, $t3`는 v[j+1]<v[j]이므로 원래 v[j]>v[j+1] 조건이다. 비교 operands를 뒤집으면 뜻이 바뀐다. 표시된 RAW는 `addi→slti`, `slti→bne`, `sll→add`, `add→첫 lw`, `둘째 lw→slt`, `slt→beq`이며 해당 no-forwarding 모델에서 각각 세 stall이다. body와 branch outcome이 생략되어 있으므로 18이라는 표시 합을 전체 loop cycle이나 CPI로 바꾸지 않는다.

초기화 `addi $s1, $s0, -1`은 `for2tst` 앞에서 한 번 j=i−1을 만든다. `slti $t0, $s1, 0`의 결과가 1이면 `bne $t0, $zero, exit2`가 음수 j를 종료시켜 배열 접근을 하지 않는다. 그렇지 않으면 shift로 얻은 4j를 `$a0`에 더해 `$t2=base+4j`를 만들고 offset 0·4의 load로 이웃 원소를 읽는다. 비교가 0이면 v[j]≤v[j+1]이므로 `beq $t0, $zero, exit2`가 종료한다. 두 guard를 통과한 경우에만 생략된 body에 도달한다. Body 뒤 `addi $s1, $s1, -1`로 j를 줄이고 `j for2tst`로 음수 검사부터 다시 시작한다. 복귀 지점은 초기화 뒤이므로 j를 매번 i−1로 되돌리지 않는다. 생략된 body가 swap을 수행한다고 추정할 수는 없다.

확인 기준: 음수 검사·4j·비교 방향과 여섯 pair를 모두 설명하고 legacy `$` 표기를 유지한다. 초기화와 복귀 위치, 두 branch의 flag·종료 조건, base+4j와 body 뒤 감소도 확인한다.

근거: [L08 p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-033) · [L08 p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-034)

</details>

#### 확인 Q17 · Load delay slot과 interlock

자료의 둘째 `lw`와 그 결과를 쓰는 `slt` 사이에 있는 `nop`은 무엇을 보장하는가? 독립 instruction으로 대체할 조건, static scheduling과 interlock의 차이를 설명하라.

<details><summary>해설 보기</summary>

MIPS R2000 예의 바로 다음 load delay slot은 load 결과를 요구하면 안 된다. `nop`은 한 자리를 비워 `slt`를 distance 2로 옮긴다. 독립 instruction을 옮길 때도 operand readiness와 원래 program 의미를 보존해야 한다. Static scheduling은 compile time에 순서를 정하는 것이고 interlock은 runtime에 hazard를 검출하여 기다리게 하는 hardware다. 실행 중 stall·flush·forwarding도 static 재배치와 구별한다. Load slot은 결과 사용 간격을 노출하는 규칙이며 branch 다음 instruction을 항상 실행한다는 branch slot 규칙과 다르다.

확인 기준: distance 2, 의미 보존 조건, compile time/runtime, 두 delay slot의 차이를 확인한다.

근거: [L08 p.44](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-044) · [L08 p.47](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-047) · [L08 p.50](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-050)

</details>

#### 확인 Q18 · Split adder의 의존 latency

32-bit adder를 EX1의 low 16-bit 합과 EX2의 high 16-bit 합으로 나누었다. Carry와 앞서 계산한 low result는 어떻게 해야 하며, 전체 결과를 쓰는 바로 뒤 instruction이 항상 더 빨라지는가?

<details><summary>해설 보기</summary>

EX1의 carry를 EX2의 high-bit 계산에 전달하고 low result도 저장하여 같은 instruction의 high result와 정렬해야 한다. Low half만 준비되었다고 전체 32-bit 값이 준비된 것은 아니다. Stage를 쪼개 clock을 줄일 수 있어도 consumer가 완전한 결과를 기다리는 cycle 수는 늘 수 있다. Boundary overhead와 branch penalty도 추가되어 dependent-chain latency나 전체 성능 개선은 보장되지 않는다. ISA의 순차적 결과를 유지해야 내부 overlap이 올바르다.

확인 기준: carry 전달·low/high 소속 보존과 clock period/의존 latency의 차이를 확인한다.

근거: [L08 p.49](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-049) · [L07 p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-011)

</details>

### Control hazard와 분기 정책

#### 확인 Q19 · PC의 producer와 consumer

L09의 예측 없는 모델에서 모든 instruction은 어느 stage에서 PC를 쓰며, R/I·load·store와 branch·`jal`·`jalr`는 언제 next PC를 결정하는가? Non-branch h가 t0 IF이면 i·j·k의 IF를 적고 PC+4 선택이 왜 prediction인지 설명하라.

<details><summary>해설 보기</summary>

Fetch는 IF에서 PC를 소비한다. 이 보수적 모델에서 R/I·load·store의 next PC는 ID, branch·`jal`·`jalr`의 next PC는 EX에서 결정된다. h가 t0 IF, t1 ID이면 i는 t2 IF, j는 t4 IF, k는 t6 IF이다. 비분기에도 확정을 기다리는 빈 cycle이 생긴다. Decode와 결정을 끝내기 전에 다음 주소를 PC+4로 택하면 아직 확인되지 않은 순차 경로를 선택하므로 prediction이다. 생산 stage는 이 구현의 가정이고 PC+4는 4-byte instruction 가정이다. L09는 현재 L08+Lab1 중간고사 범위 밖이다.

확인 기준: 모든 PC use=IF, 두 생산 시점, 교대 fetch와 시험 범위 경계를 확인한다.

근거: [L09 p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-004) · [L09 p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-005)

</details>

#### 확인 Q20 · Taken branch 뒤의 두 bubble

h가 t0 IF, t1 ID, t2 EX 끝에 taken으로 판명되고 target은 k이다. PC+4로 fetch한 i·j는 t2에 어디 있는가? t3 이후 h·i·j·k의 운명을 마지막 k WB까지 추적하고 decode·resolution·redirect·flush를 구분하라.

<details><summary>해설 보기</summary>

t2에는 h EX, i ID, j IF이다. t1 decode는 h가 branch임을 알아도 outcome과 target까지 확정하지 않는다. t2 EX 끝의 resolution 뒤 t3에는 PC를 k로 redirect하여 k IF를 시작하고 i·j를 flush한다. h는 MEM t3, WB t4로 진행한다. i의 bubble은 EX t3→MEM t4→WB t5, j의 bubble은 ID t3→EX t4→MEM t5→WB t6이며 register/memory write를 하지 않는다. k는 IF t3→ID t4→EX t5→MEM t6→WB t7이다. Stall은 나중에 실행할 명령을 보존하지만 flush는 잘못된 명령을 무효화한다. 두 bubble은 이 EX-resolution 모델의 비용이며 다른 hazard는 제외했다.

확인 기준: h를 버리지 않고 i·j만 무효화하는지, t3 redirect와 t7 완료, side effect 차단을 확인한다.

근거: [L09 p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-015) · [L09 p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-017) · [L09 p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-022)

</details>

#### 확인 Q21 · 확률과 cycle의 단위

Control flow 20%, 그중 taken 70%, predict-not-taken, wrong당 2 cycle, 기본 CPI=1, 다른 hazard와 fill/drain 없음이다. 유효 instruction 100개에서 correct/wrong·추가 cycle·CPI·IPC를 구하고 시간 증가율과 처리율 감소율을 비교하라. Forward 50%, backward 90%만으로 70%를 구할 수 있는가?

<details><summary>해설 보기</summary>

Non-control 80개와 not-taken 6개가 맞아 correct=86, wrong=14이다. 추가 28 cycle로 total=128, CPI=1.28, IPC=100/128=0.78125이다. Wrong probability 0.14는 무차원, penalty 2는 cycle/wrong, 곱 0.28은 cycle/instruction이다. 동일 IC·clock에서 시간은 28% 늘지만 IPC는 1−0.78125=0.21875, 즉 21.875% 줄어든다. Forward/backward는 target 주소 방향이고 각각의 비중이 없으면 50%·90%만으로 전체 70%를 정할 수 없다. 계산은 자료의 가정을 적용한 것이며 날짜 미확인 전사의 14:56·26:58·27:42·28:41 숫자 충돌을 정확한 발화로 고친 것은 아니다.

확인 기준: 86/14, 28, 1.28, 0.78125와 각각의 단위, 주어지지 않은 mix weight를 확인한다.

근거: [L09 p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-012) · [L09 p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-030)

</details>

#### 확인 Q22 · 빈도·정확도·손실을 분리하기

Control-flow 빈도, prediction 오류율, wrong당 penalty는 무엇으로 결정되는가? 더 이른 resolution과 더 정확한 prediction의 차이, 항상 참이라는 불명확한 발화만으로 branch를 없앨 수 없는 이유를 설명하라.

<details><summary>해설 보기</summary>

빈도는 프로그램의 instruction mix, 오류율은 선택한 predictor와 실제 control behavior, penalty는 resolution·redirect timing 등 구현에 달려 있다. 더 정확한 prediction은 wrong 횟수를 줄이고 더 이른 resolution은 한 번의 wrong에서 잃는 cycle을 줄일 수 있다. 깊은 pipeline이면 더 많은 younger work가 취소될 수도 있어 2 cycle은 보편 상수가 아니다. Branch 제거는 실제 condition이 확정되고 관련 side effect와 program 의미가 보존될 때만 정당하다. 비교식이 없는 불확실한 변수값으로 항상 참을 판정할 수 없다. 이후 predictor algorithm이나 IPC≈0.9 개선을 보장하지 않는다.

확인 기준: 세 요인의 역할과 두 개선 방향을 구별하고 condition·side effect의 증거를 요구한다.

근거: [L09 p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-031)

</details>

#### 확인 Q23 · Branch delay slot의 계약

MIPS R2000 branch가 taken일 때 PC+4 instruction과 그 다음 fetch는 어떻게 되는가? Not-taken일 때와 비교하고 slot에 옮길 instruction의 조건, `nop`, 자료의 80% 수치와 load delay slot의 차이를 설명하라.

<details><summary>해설 보기</summary>

PC+4의 한 instruction은 두 outcome 모두 실행한다. 그 다음은 taken이면 target, not-taken이면 PC+8이다. 따라서 slot instruction은 예측이 틀리면 지울 wrong path가 아니라 ISA 의미의 일부다. 옮길 instruction은 양쪽 경로에서 필요·안전하고 operands가 준비되어야 하며 branch 판단이나 다른 효과를 바꾸면 안 된다. 적절한 일이 없으면 `nop`을 쓰지만 이를 유용한 완료 작업으로 세면 처리율을 부풀린다. 약 80% 자동 채움은 자료의 역사적 사례이지 보장이 아니다. Load slot은 바로 뒤에서 load 결과를 사용하지 말라는 spacing 규칙이다. L09의 branch slot은 현재 중간고사 cutoff 밖이다.

확인 기준: 두 outcome의 주소 순서, 안전한 이동 조건, 유용한 일과 `nop`, 두 slot 차이를 확인한다.

근거: [L09 p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-032) · [L08 p.44](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-044)

</details>

#### 확인 Q24 · Architectural 복구의 한계

Wrong-path instruction의 register/memory write를 막았다. 그 사실만으로 cache 변화나 관찰 가능한 timing effect도 없다고 할 수 있는가? 자료의 권한 조건 예에서 추가로 확정할 수 없는 것을 세 가지 이상 적어라.

<details><summary>해설 보기</summary>

Architectural state에 틀린 결과를 쓰지 않는 것과 내부 cache 상태를 원래대로 만드는 것은 다른 요구다. 추측 접근이 cache 상태를 바꾸었다면 이후 접근 timing에 영향을 줄 수 있으므로 architectural flush만으로 내부 효과 부재를 증명할 수 없다. 다만 이 예에는 실제 machine code의 branch polarity, 권한 우회 mechanism, 공격자 준비 조건, network 경로나 누출 범위가 없다. Spectre와 Meltdown의 이름을 같은 mechanism으로 합치거나 모든 processor에서 성공한다고 결론내릴 수 없다. 구체적 cache/공격 설명은 후속 범위이며 현재 제품의 보안 판정도 아니다.

확인 기준: 두 state 수준의 차이를 설명하고 추측을 실제 공격 성공·전체 memory 누출로 확대하지 않는다.

근거: [L09 p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-033)

</details>

### 새로 쓴 종합 연습

#### 연습 P01 · 두 설계의 평가 기준

새로 쓴 합성 연습이다. 2025-2 복기 Q8·Q9(p.2), Q16(p.8)의 조건부 성능 비교를 가져와 첫 완료와 유한 stream을 함께 판단한다. 선수 개념은 μprogram·CPI×clock·5-stage fill/drain이다. 복기본은 공식 원문·정답이 인증되지 않았으며 현재 범위를 정하지 않는다. [EX:ca_2025_2_midterm_q08 p.2] [EX:ca_2025_2_midterm_q09 p.2] [EX:ca_2025_2_midterm_q16 p.8]

가상 설계 M은 각 instruction을 200ps의 3 cycle로 순차 실행하고, P는 160ps의 5-stage pipeline이다. Hazard와 overhead는 이미 주어진 clock 외에 없고 각 실행은 빈 상태에서 시작한다. (a) 첫 instruction과 긴 stream의 완료 간격을 비교하라. (b) N=1·2의 전체 시간을 구하고 P가 유리해지는 최소 N을 찾아라. (c) M의 이름이 microcoded, P가 hardwired라는 사실만으로 이 결과를 다른 설계에 일반화할 수 있는가?

<details><summary>해설 보기</summary>

M의 latency·완료 간격은 모두 3×200=600ps다. P의 첫 latency는 5×160=800ps지만 정상 완료 간격은 160ps다. N=1에서는 M=600, P=800ps로 M이 빠르다. N=2에서는 M=1200, P=6×160=960ps로 P가 빠르다. 일반식 160(N+4)<600N은 N>640/440=16/11이므로 정수 최소 N=2다. 첫 결과를 빨리 얻는 일과 많은 결과를 빨리 처리하는 일이 다른 선택을 준다. 제어 방식 이름은 주어진 clock·cycle 수를 보장하지 않으므로 다른 구현에는 실제 수치와 hazard 비용이 필요하다.

확인 기준: 600/800ps latency, 600/160ps 간격, 유한 N의 부등식과 구현 가정의 한계를 확인한다.

근거: [L06 p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-024) · [L07 p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-016)

</details>

#### 연습 P02 · 의존성·우회·재배치 비교

새로 쓴 합성 연습이다. 복기 Q15(p.7)의 RAW 식별→forwarding trace→stall 비교를 독립 작업의 재배치 판단으로 확장했다. 선수 개념은 실제 source/destination, 결과 준비 시점, ID/WB timing이다. 원문의 1–8 cycle 표에 맞춰 완료를 잘라내지 않는다. [EX:ca_2025_2_midterm_q15 p.7]

```asm
A: lw x8, 0(x20)
B: add x9, x8, x10
C: addi x14, x14, 1
D: sub x11, x9, x8
```

빈 in-order 5-stage에서 A의 IF를 cycle 1로 둔다. ALU 결과는 EX 끝, load data는 MEM 끝에 생긴다. EX로 필요한 forwarding 경로가 있으며 다른 hazard는 없다. (a) RAW와 마지막 WB까지 stage를 적어라. (b) Forwarding을 없애고 같은-cycle WB→ID 읽기도 금지하면 총 stall은? (c) C는 다른 줄과 독립이며 옮겨도 다른 효과가 없다고 보장한다. A,C,B,D로 바꾸면 forwarding 실행은 어떻게 달라지는가?

<details><summary>해설 보기</summary>

RAW는 A→B(x8), A→D(x8), B→D(x9)이다. Forwarding에서는 B가 load-use 한 cycle을 기다린다.

|명령|IF|ID|EX|MEM|WB|
|---|---|---|---|---|---|
|A|1|2|3|4|5|
|B|2|3–4 (대기 포함)|5|6|7|
|C|3–4 (유지)|5|6|7|8|
|D|5|6|7|8|9|

A data는 B EX5에, B result는 D EX7에 전달할 수 있다. 총 4+4+1=9 cycle이다. No-forwarding에서는 A WB5 뒤 B 정상 ID6→EX7→MEM8→WB9이므로 B에 세 stall이 필요하다. C는 ID7→EX8→MEM9→WB10이다. D는 ID8·9에서 기다린 뒤 ID10→EX11→MEM12→WB13이다. 따라서 추가 stall은 3+2=5, total=4+4+5=13이다. A→D를 또 더하지 않는다. A,C,B,D 순서는 C가 load-use 간격을 채워 A EX3/MEM4, C EX4, B EX5, D EX6이고 마지막 WB8로 끝난다. 재배치는 명시한 독립성 조건 아래에서만 안전하다.

확인 기준: 세 RAW, 원래 9 cycle·no-forwarding 13 cycle·재배치 8 cycle을 원인과 함께 확인한다.

근거: [L08 p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-013) · [L08 p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-031) · [L08 p.43](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-043) · [L08 p.50](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-050)

</details>

#### 연습 P03 · 실행해야 하는 slot인가

새로 쓴 합성 연습이다. 복기 Q17(p.8)의 branch delay slot이 단순 pipeline에 주는 이점을, 양쪽 경로의 의미 보존 판단에 적용한다. 선수 개념은 delay-slot 계약과 flush이며 L09의 현재 중간고사 범위 밖 보충이다. [EX:ca_2025_2_midterm_q17 p.8]

Instruction은 4 bytes다. Branch 주소는 `0x400`, target은 `0x500`이다. Slot 후보 A는 양쪽 경로에서 한 번 실행해야 하는 독립 덧셈으로, operands가 준비되었고 branch 조건도 바꾸지 않는다. 후보 B는 taken 경로에서만 필요한 store다. (a) Taken/not-taken에서 branch 뒤 두 실행 주소를 적어라. (b) 안전한 후보와 이유를 고르라. (c) 후보가 없을 때, 그리고 delay slot 대신 본문의 EX-resolution 예측 모델일 때 처리가 어떻게 다른가?

<details><summary>해설 보기</summary>

Delay-slot 모델은 taken에서 `0x404→0x500`, not-taken에서 `0x404→0x408`이다. A는 양쪽에 필요한 독립 작업이므로 주어진 조건에서 옮길 수 있다. B를 옮기면 not-taken에서도 store하여 의미가 바뀐다. 후보가 없으면 `nop`을 넣되 유용한 작업으로 세지 않는다. 예측 모델에서는 PC+4와 PC+8의 younger instruction이 wrong path이면 flush하고 target으로 redirect한다. 그 두 bubble을 architectural delay-slot instruction과 동일시하면 안 된다.

확인 기준: 두 주소 순서, A/B의 양쪽 경로 효과, `nop`과 flush의 차이를 확인한다.

근거: [L09 p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-022) · [L09 p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-032)

</details>

#### 연습 P04 · 두 개선안의 시간 비교

새로 쓴 강의 기반 일반 연습이다. 전체 기출 후보에는 branch 확률·penalty·clock을 함께 비교하는 직접 대응 문항이 없어 기출 유형으로 인증하지 않는다. L09 보충 범위이며 선수 개념은 Q21·Q22와 CPI×clock이다.

기준은 predict-not-taken, control flow 20%, 그중 taken 70%, wrong당 2 cycle, CPI 기본값 1이다. 개선 A는 오류율을 유지하면서 penalty를 1로 줄이지만 clock period가 10% 길어진다. 개선 B는 control flow 중 오류율을 35%로 낮추고 penalty=2·clock은 유지한다. 다른 hazard와 fill/drain은 제외한다. 동일 instruction 수의 실행시간을 기준 clock 단위로 비교하라.

<details><summary>해설 보기</summary>

기준 CPI=1+0.2×0.7×2=1.28이다. A의 CPI는 1+0.2×0.7×1=1.14이지만 시간/instruction은 1.14×1.10=1.254 기준 clock 단위이다. B도 CPI=1+0.2×0.35×2=1.14이지만 clock을 유지하여 시간은 1.14다. 둘 다 기준보다 빠르고 B가 더 빠르다. A는 오류당 손실, B는 오류 빈도를 줄였으며 같은 CPI라도 clock이 달라 시간이 달라진다. 이는 명시된 가상의 수치 비교이지 실제 predictor 성능 보장이 아니다.

확인 기준: 0.14와 0.07의 전체 오류 비율, 1.28·1.254·1.14의 시간 비교를 확인한다.

근거: [L09 p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-030) · [L09 p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-031)

</details>

## 출처

### 강의와 자료

[[courses/computer_architecture/lectures/2026-09-29-lecture-05|2026-09-29 · Microcode·자원 공유·실습 안내]]

- [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 (computer_architecture:NT001)]] 37:51, 39:27, 41:27, 43:18, 44:26, 45:27, 47:25, 48:04, 49:03, 49:43, 51:38, 52:36, 53:36, 54:28 — 당시 강의 전사.

- [[courses/computer_architecture/transcripts/undated-control-hazards-tskkzbwcgg2lavgo|날짜 미확인 강의 (computer_architecture:NT002)]] 03:17, 05:10, 14:56, 17:37, 23:27, 26:58, 27:42, 28:41, 31:19, 33:03, 34:01, 35:17, 35:35, 37:02, 38:23, 39:22 — 강의 날짜 미확인. 불확실한 발화는 자료 설명과 구분합니다. TXT 전사를 자료와 대조했으며 원음은 검증되지 않았습니다. 완전한 축어록이 아니며 빠진 발화·실제 수업 날짜·화자 신원은 복원되지 않았습니다.

- [L06 원문](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.06.pdf): [L06 p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-005), [L06 p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-014), [L06 p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-015), [L06 p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-020), [L06 p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-021), [L06 p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-022), [L06 p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-023), [L06 p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.06/page-024). 9월 29일 전사와 연결되는 L06; legacy opcode·폭·지연값을 별도 모델로 유지.

- [L07 원문](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.07.pdf): [L07 p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-006), [L07 p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-007), [L07 p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-008), [L07 p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-011), [L07 p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-012), [L07 p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-015), [L07 p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-016), [L07 p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-020), [L07 p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-027), [L07 p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-030), [L07 p.52](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-052), [L07 p.55](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.07/page-055). 자료 기반 선수 설명; 별도 강의 날짜·발화 미확인.

- [L08 원문](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.08.pdf): [L08 p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-004), [L08 p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-013), [L08 p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-018), [L08 p.29](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-029), [L08 p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-031), [L08 p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-032), [L08 p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-033), [L08 p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-034), [L08 p.37](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-037), [L08 p.42](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-042), [L08 p.43](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-043), [L08 p.44](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-044), [L08 p.47](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-047), [L08 p.49](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-049), [L08 p.50](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.08/page-050). 자료 기반 선수 설명; 별도 강의 날짜·발화 미확인.

- [L09 원문](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.09.pdf): [L09 p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-004), [L09 p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-005), [L09 p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-012), [L09 p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-015), [L09 p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-017), [L09 p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-022), [L09 p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-030), [L09 p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-031), [L09 p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-032), [L09 p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.09/page-033). 현재 L08+Lab1 중간고사 범위 밖의 수업 내용.

### 복기 문항 연결

2025-2 중간 복기본은 공식 원문과 정답의 정확성이 별도로 확인되지 않았습니다. 아래는 추론 방식의 연결이며 새 문제의 출제 예측이나 실제 기출 표시가 아닙니다. 원문에 제시된 해설도 복기본 작성자의 답안입니다.

Q08·Q09(p.2), Q16(p.8)은 latency·throughput과 구현 가정 비교, Q10(p.2)은 dependence 분류, Q15(p.7)는 RAW와 pipeline trace, Q17(p.8)은 delay-slot 의미에 연결됩니다. Q15의 1–8 cycle 표와 RF/store forwarding의 미명시 조건을 보완해 새 문제의 가정을 명시했습니다. Q17은 현재 시험 범위 밖의 L09 보충에만 연결합니다.

문항만 보는 기존 링크: [[exam_questions/ca_2025_2_midterm_q09|2025-2 중간 복기 Q9]] · [[exam_questions/ca_2025_2_midterm_q15|2025-2 중간 복기 Q15]] · [[exam_questions/ca_2025_2_midterm_q16|2025-2 중간 복기 Q16]].

자료 표기 주의: L07 p.16의 `predicated`, p.27의 `state`는 원문 표기입니다. 여기서 prediction·stage를 설명하는 것은 문맥 해석이며 원문 인용을 고친 것이 아닙니다. 9월 29일 49:03·49:43의 IR/PC 혼동과 날짜 미확인 강의의 숫자·timing 충돌도 자료의 해설과 구분합니다.


---

[[courses/computer_architecture/units/index|단원 목차]] · [[courses/computer_architecture/units/lab-environment-specification|다음: Docker 실습 환경과 CPU 과제 사양 읽기 →]]
