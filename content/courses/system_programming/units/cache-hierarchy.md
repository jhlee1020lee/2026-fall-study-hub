---
title: "Memory hierarchy·locality와 cache 교체"
description: "Locality와 block 이동에서 conflict·LRU·clock까지 cache의 판단 과정을 복습한다."
course: "system_programming"
unit_id: "cache-hierarchy"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["07.MM.Virtual.Memory.Recap.pptx", "07.MM.Virtual.Memory.Recap_2ffc3cf7.pptx"]
private_source_assets: []
source_lectures: ["courses/system_programming/lectures/2026-09-28-lecture-07"]
---

Memory hierarchy는 자주 쓰는 데이터를 작고 빠른 공간에 두어 비용과 속도를 절충한다. Locality, placement, replacement를 구분하며 hit·miss와 교체 과정을 직접 추적해 보자.

## Memory hierarchy가 필요한 이유

큰 memory를 모두 register처럼 빠르게 만들 수 있다면 편리하겠지만 용량, 속도, byte당 비용은 함께 고려해야 한다. Memory hierarchy(메모리 계층)는 작고 빠른 storage와 크고 상대적으로 저렴한 storage를 결합한다. [Memory layout](memory-layout.md)이 process 안에서 object의 역할을 나눴다면, 여기서는 그 데이터에 접근하는 비용을 줄이는 방법을 다룬다.

[[courses/system_programming/lectures/2026-09-28-lecture-07|2026-09-28 memory hierarchy 강의]]와 [[courses/system_programming/transcripts/2026-09-28|같은 날짜 STT]] 19:55–25:38은 registers, SRAM CPU caches, DRAM main memory, local storage, remote storage를 대비한다. Registers와 cache의 cycle 수준 접근, DRAM 약 100 cycles 또는 수십 ns, SSD의 microsecond, HDD의 millisecond는 강의의 규모 비교이지 현재 모든 장치의 측정값이 아니다. HDD에는 seek와 rotational delay 같은 기계적 지연이 있고 SSD에는 그 기계 부품이 없다. 자료의 hierarchy level 이름과 CPU의 L1/L2/L3 cache 이름도 동일한 번호 체계로 혼동하지 않는다.

### Remote storage가 항상 가장 느린 것은 아니다

Disaggregation(자원 분리)의 예에서는 compute node가 CPU와 memory를 제공하고 disk storage를 network 너머에 모아 둔다. OS에는 disk처럼 보이지만 I/O는 network를 통과한다. Storage 교체·유지보수와 규모 조정을 한곳에서 수행할 수 있는 것이 동기다. STT 22:55–25:38은 빠른 network를 이용한 remote 접근이 local disk보다 빠를 수도 있다고 설명하므로 ‘local은 언제나 remote보다 빠르다’는 절대 순서는 성립하지 않는다.

이 문맥의 “400/800 gigabits per minute”와 remote swap 관련 구절은 불확실한 STT로 남아 있다. 이를 per-second 단위나 특정 구현으로 복원하지 않는다. Tape 보급 정도에 관한 불명확한 말도 계층의 존재를 이해하는 데 필요한 확정 사양으로 사용하지 않는다.

## Locality가 작은 cache를 유용하게 만든다

Cache는 더 크고 느린 storage의 데이터 일부를 잠시 보관하는 작고 빠른 storage다. 전체를 보유하지 않아도 자주 쓰는 subset을 보유하면 많은 접근을 빠르게 처리할 수 있다. 이를 설명하는 locality(지역성)는 두 종류다. Temporal locality는 최근 사용한 항목을 가까운 미래에 다시 쓰는 경향이고, spatial locality는 인접 주소의 항목을 시간적으로 가깝게 쓰는 경향이다.

[system_programming:RM001 slide 18](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/07.MM.Virtual.Memory.Recap.pptx)와 같은 내용을 담은 NM003의 array-sum fragment를 보자. 유효한 array와 범위, 합의 type 범위가 확보된 조건의 개념 예다.

```c
sum = 0;
for (i = 0; i < n; i++)
    sum += a[i];
```

`sum`은 매 반복 사용되므로 temporal locality를 보인다. 각 `a[i]`를 한 번만 읽어도 곧 `a[i+1]`을 읽으므로 array 접근은 spatial locality를 보인다. Loop instruction은 반복되므로 temporal, branch 없는 구간의 연속 instruction 접근은 spatial locality다. STT 26:35–29:32는 data와 instruction 양쪽의 예를 구분한다. 모든 프로그램이 항상 같은 locality를 보인다는 뜻은 아니다.

Level k가 level k+1 데이터의 일부를 보유한다는 관계는 CPU cache에만 한정되지 않는다. Registers는 아래 memory 계층에서 가져온 값을 보유하고, main memory는 disk 데이터의 cache가 되며, local disk는 remote file의 사본을 보유할 수 있다. 전체 memory를 최고 속도로 만드는 대신 hot subset에 비용을 집중하는 것이다(STT 30:31–31:27). 끝이 끊긴 “K+” 발화는 새 문장으로 복원하지 않는다.

## Block 단위 이동, hit, miss

계층 사이에서 데이터를 block 단위로 복사하면 접근 시작 비용을 여러 byte에 나눌 수 있다. Fixed-size block은 indexing과 관리가 쉽고 hardware cache에 흔하다. Variable-size block은 web image 전체를 보관하는 web cache처럼 데이터 크기에 맞출 수 있지만 관리가 더 어렵다. 자료의 예는 register word 8 bytes, cache line 64 bytes, 일반 page 4 KiB, 큰 page 2 MiB 또는 1 GiB다. Cache line 64 bytes는 전체 cache 용량이 아니며 주소 폭이 모든 block 크기를 정하는 것도 아니다.

STT 32:27–35:28의 source 예에서 level k가 blocks `4,9,10,3`을 보유하면 10 요청은 hit, 13 요청은 miss다. Block 13이 level k+1에 있다면 같은 요청도 계층에 따라 판정이 다르다. Miss에서 아래로부터 가져온 block을 **어디에 놓을지**는 placement, 공간이 찼을 때 **무엇을 내보낼지**는 replacement 또는 eviction 문제다.

### Miss의 세 원인

Cold/compulsory miss는 처음 접근하여 아직 가져온 적이 없기 때문에 생긴다. 첫 code segment 실행이나 첫 array 접근이 예다. Working set은 현재 활동하는 blocks의 집합이다. Capacity miss는 이를 cache에 함께 유지할 수 없을 때 생긴다. Source의 1000-byte cache로 1200-byte array를 오가며 처리하는 예는 용량 부족을 보여 준다. 이 수치의 단위는 bytes이며 blocks 개수로 바꾸지 않는다.

Placement를 제한하는 이유는 lookup에 필요한 비교를 줄이기 위해서다. [[courses/system_programming/transcripts/2026-09-28|2026-09-28 STT]] 38:15–39:15에서 설명하듯, block을 어느 위치에나 둘 수 있으면 찾을 때 여러 위치의 tag를 비교해야 하며 이를 병렬로 수행하는 hardware는 더 비싸고 복잡해진다. 반면 block 번호에서 `i mod 4`라는 index를 정하면 조사할 위치와 tag의 수를 줄여 lookup 회로를 단순하게 만들 수 있다.

Conflict miss는 총 용량보다 **놓을 수 있는 위치의 제한** 때문에 생긴다. Source가 block i를 `i mod 4` 위치에만 놓는다면 0과 8은 모두 위치 0이다. 그 위치에 block 하나만 둘 수 있는 조건에서 `0,8,0,8`은 서로를 계속 축출한다. 첫 접근들은 compulsory이지만 이후 반복 miss는 충돌을 드러낸다. 다른 위치가 비어 있어도 두 block이 그곳을 쓸 수 없기 때문이다.

STT 38:15–40:13은 이 문맥에 넓게 “set associative”를 사용하지만, 이 trace의 한 위치·한 block 조건은 direct-mapped다. 여러 ways가 두 block을 동시에 보유할 수 있는 구성에 같은 miss 결과를 적용하면 안 된다. 이는 source의 조건을 명시한 설명상의 교정이다.

## Replacement는 미래를 추정하는 정책이다

Cache가 찼을 때 새로운 block을 넣으려면 victim을 골라야 한다. Optimal 정책은 다시 쓰이지 않거나 다음 사용이 가장 먼 미래의 block을 내보낸다. 실제 프로그램의 branch와 input을 미리 알기 어려워 미래 전체를 아는 정책을 일반적으로 구현할 수는 없다.

LRU(Least Recently Used)는 과거의 recency를 이용한다. 가장 오래 사용하지 않은 block이 가까운 미래에도 덜 쓰일 것이라고 추정하여 victim으로 고른다. 이 가정은 틀릴 수 있다. 강의는 보통 프로그램에서 유용한 경향으로 설명하며 미래 예측 보장으로 설명하지 않는다(STT 41:06–42:45).

STT 44:10–46:30의 명확한 후속 설명은 최근 사용한 항목을 queue의 tail로 옮기고 오래된 head 쪽을 내보내는 것이다. 새로 적은 설명용 상태 추적에서 head→tail이 `[A,B,C]`일 때 A에 hit하면 `[B,C,A]`가 된다. 이어 D를 넣어야 하면 B가 victim이다. Hit에서 순서를 바꾸지 않는 FIFO와 차이가 여기서 드러난다. Head/tail 방향을 반대로 정할 수는 있지만 갱신과 축출 규칙이 일관되어야 한다. 불명확한 학생 응답과 중간 “D cubed.” 구절을 특정 deque 구현이나 pointer 조작으로 복원하지 않는다.

## Page, page table, PTE, MMU로 clock 준비하기

Main memory를 disk의 cache로 관리할 때의 교체를 이해하려면 page에 대한 최소한의 정의가 먼저 필요하다. Process가 사용하는 virtual address는 실제 physical 위치와 다르다. Page는 그 mapping을 수행하는 고정 크기 단위다. Virtual Page Number(VPN)를 Physical Page Number(PPN)에 연결한 자료구조가 page table이고, 표의 한 항목이 Page-Table Entry(PTE)다. Page table은 main memory에 있는 자료구조이며, MMU(Memory Management Unit)는 그 mapping을 이용하여 주소를 변환하는 hardware다. 이 구분은 STT 10:25–19:55와 RM001/NM003 slides 10–16에 근거한다.

이제 ‘page에 접근했다’는 상태를 그 PTE의 reference/access bit에 기록한다는 말을 이해할 수 있다. 여기서는 bitfield 전체나 상세 주소 계산을 요구하지 않으며 그것은 뒤의 [Virtual Memory](virtual-memory.md)로 이어진다.

### Exact LRU 비용과 second chance

작은 read/write마다 exact LRU queue를 갱신하면 관리 비용이 원래 접근보다 비싸질 수도 있다. Page 단위로 관리해도 그 page 안의 데이터가 사용될 때마다 순서를 유지해야 한다. Clock, 또는 second chance는 전체 순서 대신 저렴한 최근 사용 흔적을 이용한다(STT 47:17–51:15).

Hardware는 page 접근 때 PTE의 reference bit를 1로 만든다. Memory pressure에서 OS가 pages를 차례로 살펴본다. Bit가 0이면 victim으로 선택하고, 1이면 0으로 지우며 이번에는 살려 두고 다음 page로 간다. 이후 접근되면 hardware가 다시 1로 만든다. 예를 들어 scan 대상 세 page의 bits가 `[1,0,1]`이고 첫 page에서 시작하면 첫 bit를 0으로 바꾸어 second chance를 주고, 다음 page의 0을 만나 victim으로 선택한다. 이는 새로 적은 짧은 정책 예이며 exact recency 순서를 복원하지 않는다. Clock은 LRU 근사지 exact LRU가 아니다.

### 계층마다 관리 주체가 다르다

Compiler의 register allocation은 code analysis를 통해 어떤 값을 register에 보유할지 정한다. CPU L1/L2/L3 cache는 hardware가 관리하며 빠른 lookup을 위해 정해진 placement 구조를 사용한다. Main memory의 paging과 replacement는 OS가 관리한다. Disk I/O가 매우 비싸므로 OS는 더 복잡한 LRU-like 정책이나 second chance의 관리 비용을 들일 여지가 있다(STT 51:15–54:08). 정해진 lookup 구조라는 말이 모든 hit/miss의 실제 latency가 같다는 뜻은 아니다.

## Cache lookup 문제에서 조건을 옮기지 않기

[EX:sp_2025_1_midterm_q04 p.13] Q4(e)와 [EX:sp_2025_1_midterm_q04 p.14] Q4(f)는 별도 cache의 주소 field와 hit 판정을 요구한다. 접근 방법은 block 크기에서 offset 폭, 전체 lines와 ways에서 set 수, set 수에서 index 폭을 구하고 나머지를 tag로 읽는 것이다. 선택된 set의 각 way에서 **valid와 tag를 함께** 확인한 뒤에야 line 안의 byte를 선택한다.

이 문항의 cache 조건은 앞 소문항의 VM 조건과 주소 폭·block 크기가 다르다. 앞에서 얻은 bit 분할을 그대로 가져오면 안 된다. 이는 cache 개념을 계산에 연결하는 선택적 적용이며 private 표나 제공 답을 복제하는 예가 아니다. Primary의 locality, remote storage, LRU, clock은 이 기출에 직접 대응하지 않더라도 각각 필요한 개념이다.

## 핵심 정리

- Hierarchy는 속도·용량·비용의 절충이며 local/remote 속도 순서는 절대적이지 않다.
- Temporal은 재사용, spatial은 가까운 주소 접근이며 data와 instruction 모두에 적용된다.
- Placement는 허용 위치, replacement는 victim 선택이다.
- 첫 접근·working-set 용량·같은 위치 충돌을 구분해야 miss 원인이 보인다.
- LRU는 과거 순서, optimal은 미래 정보, clock은 reference bit를 사용한다.

## 확인·연습문제

### 개념 확인과 설명

#### 확인 Q01 · 계층과 분리된 storage

Registers→SRAM cache→DRAM→local/remote storage의 용량·비용·latency 경향과 SSD/HDD 차이를 설명하라. Disaggregation에서 OS가 보는 것, 관리상 동기, local보다 remote가 빠를 수 있는 조건은?

<details><summary>해설 보기</summary>

위쪽은 작고 빠르며 byte당 비싸다. 강의 규모는 register/cache cycle 수준, DRAM 수십 ns 또는 약100 cycles, SSD microseconds,HDD milliseconds이며 HDD는 seek·회전 지연이 있다. 빠른 storage만으로 전체 용량을 만들기는 비싸다. Disaggregation은 network를 통한 I/O를 OS에 disk처럼 제공하며 집중 교체·유지보수·규모 조정을 돕는다. 빠른 network와 storage는 느린 local disk보다 빠를 수 있다. 강의의 per-minute bandwidth·remote swap·tape 발화는 불확실하여 고친 사양으로 쓰지 않는다.

**채점·점검 기준:** 세 절충·장치 지연 차이·network I/O와 관리 동기·uncertainty를 포함한다.

</details>

#### 확인 Q02 · Data와 instruction locality

Array-sum loop의 sum·a[i]·loop instruction·branch 없는 연속 instruction을 temporal/spatial로 설명하라. 작은 cache가 효과적인 이유와 CPU 외 계층 관계는?

<details><summary>해설 보기</summary>

`sum` 반복은 temporal, a[i] 뒤 이웃 a[i+1]은 spatial, 반복 instruction은 temporal, 순차 instruction은 spatial이다. Locality로 hot subset에 접근이 몰리면 일부 데이터만 보유해도 빠른 계층에서 많은 요청을 처리한다. Level k가 k+1 일부를 보유하는 관계로 register, main memory의 disk cache 역할, local disk의 remote-file 사본을 설명할 수 있다. 경향이지 모든 프로그램의 보장은 아니다.

**채점·점검 기준:** 네 locality와 hot subset의 이유를 함께 설명한다.

</details>

#### 확인 Q03 · Block·hit·placement

Fixed/variable block tradeoff와 8-byte register·64-byte line·4 KiB/2 MiB/1 GiB page의 역할을 구분하라. Level k에 4,9,10,3, k+1에 13이 있을 때 10·13 요청과 placement/replacement는?

<details><summary>해설 보기</summary>

Fixed는 관리·indexing이 쉽고 variable은 web image처럼 크기에 맞출 수 있지만 복잡하다. Block 전송은 시작 비용을 여러 byte에 나눈다. 제시 크기는 각 전송 단위이며 64는 전체 cache 용량이 아니고 주소 폭이 모든 block 크기를 정하지 않는다. 10은 k hit,13은 k miss·k+1 hit다. 가져온 13의 허용 위치가 placement, 필요 공간을 위해 내보낼 기존 block 선택이 replacement다.

**채점·점검 기준:** 단위·capacity 혼동 없이 두 요청과 두 결정을 구분한다.

</details>

#### 확인 Q04 · Miss의 세 원인

Cold·capacity·conflict를 구분하고 1000-byte cache/1200-byte working array, 단일-way `i mod4`의 `0,8,0,8`을 분석하라. 다른 slot이 비어 있거나 두 way가 있다면? 위치를 제한하면 어떤 lookup 비용을 줄이는가?

<details><summary>해설 보기</summary>

어느 위치에나 block을 둘 수 있으면 여러 위치의 tag를 찾아 비교해야 하고 병렬 비교 hardware가 더 비싸고 복잡해진다. `i mod 4`로 index를 정하면 검사할 위치와 tag의 수를 줄여 lookup 회로를 단순하게 한다.

Cold는 첫 참조로 아직 없음, capacity는 active working set을 함께 담지 못함, conflict는 placement 제한이다. 1000/1200 단위는 bytes다. 0과8은 둘 다 slot0이라 처음 둘은 cold, 뒤 둘은 서로 축출한 conflict miss다. 빈 다른 slot은 허용 위치가 아니므로 못 쓴다. 같은 set에 두 block을 보유할 두 way가 있으면 첫 둘 뒤 hit할 수 있어 이 단일-way trace를 일반 set-associative에 적용하지 않는다.

**채점·점검 기준:** 첫 두 접근과 이후 두 접근의 원인, 두-way 반례와 제한된 index가 비교 hardware의 비용을 줄이는 이유를 설명한다.

</details>

#### 확인 Q05 · Optimal·LRU·FIFO

Optimal과 LRU의 정보 차이 및 LRU 가정의 한계를 쓰라. Head=oldest인 [A,B,C]에서 A hit 뒤 D 삽입의 순서·victim을 구하고 FIFO와 비교하라.

<details><summary>해설 보기</summary>

Optimal은 다시 안 쓰이거나 다음 사용이 가장 먼 block을 미래 정보로 고른다. LRU는 마지막 사용이 가장 오래된 것을 고르며 미래 재사용을 보장하지 않는다. A hit 후 [B,C,A], D 삽입 시 B를 내보내 [C,A,D]다. FIFO는 hit에 순서를 갱신하지 않아 [A,B,C]에 머물고 A를 내보낸다. 명확한 tail 이동 설명만 사용하며 불분명한 deque 발화를 구현으로 복원하지 않는다.

**채점·점검 기준:** 두 정보 종류, A hit 갱신, B와 A의 victim 차이를 확인한다.

</details>

#### 확인 Q06 · Clock 전에 필요한 mapping

Virtual/physical address, page, page table, PTE, MMU를 각각 구분하고 reference bit가 어느 단위의 상태인지 설명하라.

<details><summary>해설 보기</summary>

Virtual address는 process가 쓰는 주소, physical은 실제 memory 위치다. Page는 고정 mapping 단위, page table은 main memory의 VPN→PPN mapping 자료구조, PTE는 그 한 항목, MMU는 변환 hardware다. Reference bit는 해당 page에 접근한 흔적을 PTE와 연결해 기록한다. MMU와 table을 같은 hardware라 부르거나 전체 PTE bitfield를 알아야 clock을 이해한다고 할 필요는 없다.

**채점·점검 기준:** 여섯 개념과 hardware/data structure 차이를 확인한다.

</details>

#### 확인 Q07 · Second chance 추적

왜 exact LRU를 매 memory access에 유지하기 어려운가? 첫 page에서 시작한 bits [1,0,1]의 scan을 추적하고 hardware와 OS의 bit 역할 및 exact LRU와 차이를 설명하라.

<details><summary>해설 보기</summary>

작은 read/write마다 queue를 갱신하면 원래 접근보다 큰 관리 비용이 들 수 있다. Hardware는 접근 때 bit=1, OS scan은 1이면 0으로 지우고 살려 두며 0이면 victim으로 선택한다. 첫 bit를 0으로 만든 뒤 둘째 page가 victim, 셋째는 아직 조사하지 않아 1이다. 다시 접근하면 hardware가 1로 만들 수 있다. 전체 recency 순서를 보유하지 않아 clock은 exact LRU의 근사다.

**채점·점검 기준:** 첫 bit clear·둘째 victim·셋째 유지와 두 주체를 명시한다.

</details>

#### 확인 Q08 · 계층의 관리 주체

Register, CPU L1/L2/L3, main-memory paging을 누가 관리하는가? OS가 더 복잡한 replacement를 고려할 여지가 있는 이유와 fixed lookup의 latency 한정은?

<details><summary>해설 보기</summary>

Compiler register allocation, hardware cache, OS paging/replacement다. Compiler는 code analysis로 값 재사용을 계획하고 hardware는 정해진 placement로 빠르게 lookup한다. OS는 비싼 disk I/O를 줄이는 이득이 있어 LRU-like/second-chance 관리 비용을 들일 여지가 있다. 정해진 lookup 구조가 모든 hit/miss의 동일 latency를 뜻하지 않는다.

**채점·점검 기준:** 세 주체와 disk 대비 비용 논리를 연결한다.

</details>

### 적용과 점검

#### 연습 P01 · 같은 용량에서 placement 바꾸기

**새로 만든 합성 연습.** [EX:sp_2025_1_midterm_q04 p.13] Q4(e)와 [EX:sp_2025_1_midterm_q04 p.14] Q4(f)의 주소 field·valid/tag·offset 추론을 사용한다. 선수는 본문의 block·placement·lookup 설명이며 VM 조건은 쓰지 않는다.

8-bit physical addresses,4-byte lines,총 4 lines인 빈 cache를 (A) direct-mapped,(B) 2-way로 비교한다. 요청은 0x04,0x14,0x05,0x15이며 다른 접근은 없다. 각 구성의 offset/index/tag 폭과 hit/miss를 구하라. Memory block 0x04의 bytes는 31,32,33,34(hex),0x14는 41,42,43,44다. B의 마지막 두 접근은 어떤 byte인가? 이어 0x04 line의 valid만 0으로 바꿨다면 0x05는 hit인가?

<details><summary>해설 보기</summary>

Offset은 log2(4)=2 bits. A는4 sets라 index2/tag4; 두 block 번호1·5가 set1로 충돌하여 M,M,M,M이다. B는2 sets라 index1/tag5; block1·5는 set1이지만 서로 다른 tag0·2로 두 way에 들어가 M,M,H,H다. 마지막 둘은 offset1이므로 0x32와0x42다. Valid=0이면 tag가 남아도 hit가 아니며 0x05는 miss다. 총 용량을 늘리지 않고 허용 배치를 바꾼 것이 차이다.

**채점·점검 기준:** 2/2/4와2/1/5, 두 trace,0x32/0x42, valid 조건을 모두 검산한다.

</details>

### 복습 순서

Q02의 locality를 code에 표시한 뒤 Q04–Q05를 access별 표로 풀어 보라. Q06을 먼저 설명하고 Q07–Q08의 clock 주체를 확인한 다음 P01에서 field 계산과 hit 판정을 별도 열로 검산하라.

## 출처

[[courses/system_programming/lectures/2026-09-28-lecture-07|2026-09-28 · 강의 노트]]

[[courses/system_programming/transcripts/2026-09-28|2026-09-28 · 보정 STT]] — 10:25–19:55 (page와 translation 배경), 19:55–25:38 (계층과 원격 storage), 26:35–40:13 (locality·block·miss), 41:06–54:08 (replacement와 관리 주체)

[07.MM.Virtual.Memory.Recap.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/07.MM.Virtual.Memory.Recap.pptx) — slide 17; slide 18; slide 19; slide 20; slide 21; slide 23; slide 24; slide 25; slide 11

[07.MM.Virtual.Memory.Recap_2ffc3cf7.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/07.MM.Virtual.Memory.Recap_2ffc3cf7.pptx) — slide 17; slide 18; slide 19; slide 20; slide 21; slide 23; slide 24; slide 25; slide 11

9월28일 보정 STT의 bandwidth 단위·remote swap·tape·queue 문답 및 가림 구간은 불확실한 채로 남는다. Source의 i mod4 예는 단일-way 조건으로 한정하며 넓은 set-associative 발화를 모든 구성에 적용하지 않는다. Deck 전체 그림의 세부 layout을 검증한 것은 아니고 block·code·명시 조건을 따른다. 성능 수치는 당시 규모 비교다. 기출 cache와 VM 소문항은 서로 다른 주소 폭·block 조건이며 제공 답안은 독립 정답 보증이 아니다.

아래 과거 시험 연결은 명시한 추론 요구에 한정한다. 제공 답안은 참고자료이며 독립 검증된 정답으로 간주하지 않고, 현재 시험 범위나 출제 빈도를 추정하지 않는다.
