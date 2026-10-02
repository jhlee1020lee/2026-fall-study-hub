---
title: "Virtual Memory·page translation·공유와 보호"
description: "Page 변환·fault·공유 mapping과 역사적 TLB/data-cache 주소 경로를 복습한다."
course: "system_programming"
unit_id: "virtual-memory"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["07.MM.Virtual.Memory.Recap.pptx", "07.MM.Virtual.Memory.Recap_2ffc3cf7.pptx", "06.MM.Variable.and.Memory.Recap.pptx"]
private_source_assets: []
source_lectures: ["courses/system_programming/lectures/2026-09-23-lecture-06", "courses/system_programming/lectures/2026-09-28-lecture-07"]
---

Virtual Memory는 프로그램의 주소와 실제 저장 위치 사이에 mapping을 두어 분리와 공유를 함께 제공한다. 주소 분할, residency, permission, translation cache와 data cache를 차례로 구분하며 접근 경로를 따라가자.

## Virtual address와 physical location을 분리하기

Memory를 byte마다 주소가 붙은 큰 array로 보면 load는 memory에서 register로, store는 register에서 memory로 데이터를 옮기는 동작이다. 자료의 `ld`/`sd`는 이 역할의 예이며 모든 architecture의 instruction 문법은 아니다. 64-bit byte address가 나타낼 수 있는 공간은 `2^64 bytes = 16 EiB`다. 이는 pointer의 표현 범위이지 machine에 그만큼의 DRAM이 장착되었다는 뜻이 아니다.

Process마다 instruction의 text, global data, heap, stack이 있다. [Memory layout](memory-layout.md)의 이 영역들을 하나의 physical memory에서 어떻게 관리할지가 문제다. 다른 process의 데이터에 임의로 접근하지 못하게 하는 isolation/protection과, 협업하는 process가 지정 데이터를 함께 사용하는 sharing이 동시에 필요하다. [[courses/system_programming/lectures/2026-09-28-lecture-07|2026-09-28 Virtual Memory 강의]]와 [[courses/system_programming/transcripts/2026-09-28|같은 날짜 STT]] 01:07–09:46이 이 동기를 연결한다.

Indirection(간접화)은 프로그램이 사용하는 주소와 실제 위치 사이에 mapping을 넣는다. Virtual Memory는 physical memory의 abstraction이고 Virtual Address(VA)는 Physical Address(PA)와 분리된 process의 주소다. Process에는 자기 memory world가 보이지만 접근은 뒤에서 translation을 거친다. 기본적으로 private 공간을 갖되 필요한 shared region을 만들 수 있다.

강의의 비유는 서로 다른 addressing scheme을 쓰는 LAN 위에 IP layer를 두는 것이다. NIC의 48-bit MAC address와 상위 IP address를 구분하면 공통된 상위 주소와 구체적인 하위 주소를 나누는 취지를 이해할 수 있다. 하나의 physical machine 위에 logical machine을 구성한다는 virtual machine 비유도 ‘실제 장치와 같은 기능을 제공하는 개념적 구성’을 설명한다. 이 비유들이 전체 network protocol이나 virtualization 구현을 추가하는 것은 아니다. 불완전한 load/store 문장, “64 different bytes”, 불명확한 LAN 표현은 특정 instruction이나 수치로 복원하지 않는다.

## Page 단위로 주소를 변환하기

모든 byte를 따로 mapping하면 관리량이 지나치게 커진다. Page(페이지)는 mapping의 고정 크기 단위이며 강의의 일반 예는 4 KiB, 큰 page는 2 MiB와 1 GiB다. 단순한 page table은 Virtual Page Number(VPN)를 index로 사용하여 Physical Page Number(PPN)를 얻는다. 표의 한 entry가 PTE다. VPN 0→PPN 2, VPN 1→PPN 1, VPN 2→PPN 5라는 source mapping은 virtual 순서와 physical 배치가 같을 필요가 없음을 보여 준다(STT 10:25–11:52).

### `0x233`을 변환하는 계산

RM001/NM003 slides 14–15의 작은 예는 위의 일반 page 크기와 달리 `PS = 0x100 = 256 bytes`다. 계산을 세 부분으로 나눈다.

1. `VPN = floor(0x233 / 0x100) = 2`
2. `offset = 0x233 % 0x100 = 0x33`
3. `PPN = PT[2] = 5`이므로 `PA = 5 * 0x100 + 0x33 = 0x533`

Virtual page와 physical page 크기가 같으므로 page 안의 offset은 보존된다. PPN 5는 page **번호**이고 `0x500`은 그 page의 **시작 주소**다. 따라서 PT가 PPN을 반환하는 정의라면 일반식은 다음과 같다.

$$
PA = PT[\lfloor VA/PS\rfloor]\,PS + (VA\bmod PS).
$$

Source slide 14의 `2 (= 0x233 & 0xF00)`는 mask 결과 `0x200`에서 shift를 빠뜨렸다. 이 toy 주소에서 `(0x233 & 0xF00) >> 8`이어야 2다. Slide 15의 `PA = PT[VA/PS] + VA%PS`는 PT가 page base를 반환할 때만 그대로 맞으며, VPN→PPN 표라는 원래 정의에서는 위의 곱셈이 필요하다. 이것은 원본 정의와 예제를 근거로 한 명시적 설명 교정이다. STT 13:47–16:16의 division/remainder 혼란이나 “Inside page 1”을 새 발화로 바꾸는 것은 아니다.

## MMU, page table, TLB의 역할

MMU(Memory Management Unit)는 VA→PA 변환을 수행하는 hardware다. Page table 자체는 main memory의 자료구조다. PTBR(Page-Table Base Register)는 탐색 시작 위치를 주며 Intel 예에서는 CR3라는 register 이름을 사용한다. OS가 관리하는 mapping 자료, 그 시작점을 담는 register, mapping을 이용하는 hardware를 구분해야 한다(STT 17:16–18:05).

매번 page table을 여러 차례 읽어야 하면 데이터 접근 전의 translation 비용이 커진다. TLB(Translation Lookaside Buffer)는 자주 사용하는 translation 정보를 cache하여 그 비용을 줄인다. TLB hit이면 저장된 translation을 활용하고, 없으면 page-table 경로가 필요하다. TLB는 program data bytes를 보유하는 data cache와 다르며 모든 PTE를 담지도 않는다. STT 19:02–19:55의 불명확한 “both times”를 특정 hit 비율이나 “most times”로 복원하지 않는다.

## Process별 mapping으로 isolation과 sharing 구성하기

각 process는 자기 address space와 page table을 가진다. 실행 중인 process의 table을 PTBR가 가리키므로 같은 VPN도 다른 PPN으로 연결될 수 있다. 반대로 두 process의 PTE를 같은 physical page에 연결하면 sharing이 된다.

Source의 sharing 예에서 A의 VPN 1과 B의 VPN 1은 PPN 1을 공유한다. A의 VPN 4와 B의 VPN 6도 PPN 6을 공유한다. 두 번째 경우처럼 공유한다고 VA가 같아야 하는 것은 아니다. 이 표의 상태와 앞의 isolation 예는 별개이므로 mapping 숫자를 섞지 않는다(STT 54:08–55:05).

또 다른 toy 예에서 A/B/C는 각각 virtual pages 일곱 개를 가진다. `PS=0x100`이면 각 공간은 `0x700` bytes, 합은 21 pages=`0x1500` bytes다. Physical memory는 11 pages=`0xB00` bytes다. 모순이 아닌 이유는 virtual 공간 전체를 process별로 같은 크기의 별도 resident DRAM으로 확보하는 모델이 아니기 때문이다. Page table들 자체도 physical memory에 놓이고, 사용 중인 mapping 일부만 나타난다. 모든 virtual page가 동시에 별도 physical page에 상주한다는 주장이 아니다(STT 56:00).

### 주소 공간 규모와 multilevel table의 동기

Full 64-bit byte space를 4-KiB pages로 나누면 가능한 page 수는 `2^64 / 2^12 = 2^52`, 약 `4.5 × 10^15`다. 뒤에서 사용할 역사적 Core i7 모델은 이와 다른 **48-bit VA**다. Offset이 12 bits이므로 VPN은 36 bits, 가능한 VPN은 `2^36`개다. Byte 공간은 `2^48 bytes = 256 TiB`이며 ‘256조 pages’가 아니다. STT 57:02–59:51의 불명확한 “256 terapheases” 표현을 단위가 확정된 숫자로 인용하지 않는다.

작은 `ls`나 `cat`에도 가능한 모든 VPN의 entry를 담는 단순 array를 두면 과도하다. 필요한 mapping에 맞춰 계층적으로 관리하는 multilevel page table의 동기가 여기에 있다. 동시에 여러 process가 libc의 `printf` 같은 공통 page를 중복 보유하지 않도록 공유할 필요도 있다. Source가 소개한 lazy copy와 copy on write(COW)는 중복 절감의 동기와 후속 설명 예고까지다. Write fault에서의 복사 구현을 이번 범위로 추가하거나 `fork`가 항상 모든 physical page를 즉시 복사한다고 단정하지 않는다.

## Resident page, page fault, protection fault

많은 active program이 DRAM을 요구하면 일부 page를 disk로 내보내고 physical memory를 cache처럼 사용할 수 있다. 이 paging 예제의 VA `0x233`은 앞서 PPN 5로 정상 변환하던 상태와 다르다. 여기서는 VPN 2가 paged-out 상태와 disk 위치를 나타낸다.

필요한 page가 없으면 page fault가 발생하여 해당 실행이 잠시 중단된다. OS는 필요하다면 [clock 같은 replacement](cache-hierarchy.md)로 공간을 확보하고, disk에서 page를 읽고, PTE를 갱신한다. 그 후 faulting instruction을 다시 실행하면 접근할 수 있다(STT 01:00:47–01:05:06). 이는 복구 가능한 nonresident-page 사례이며 모든 fault가 종료를 뜻하지 않는다. 모든 fault에 disk I/O가 필요하다는 뜻도 아니다.

### Victim 선택과 보존할 데이터는 다른 문제

Victim을 골랐다고 항상 disk write가 필요한 것은 아니다. File-backed page가 원본 file을 읽은 뒤 수정되지 않았다면 현재 memory 사본을 버리고 나중에 다시 읽을 수 있다. 이미 disk에 같은 내용이 있는 clean page도 같은 원리다. 반대로 변경된 내용은 버리기 전에 보존해야 한다. STT 01:05:06–01:05:59는 이 차이가 I/O 비용을 바꾼다고 설명한다. 후속 PTE D-bit layout 전체를 도입하지 않아도 clean과 modified data의 차이는 이해할 수 있다.

### Mapping이 있어도 write가 허용되지는 않는다

PTE는 PPN뿐 아니라 접근 permission도 나타낸다. Read-only, readable/writable, executable 같은 성질이 page마다 다를 수 있다. Source의 별도 protection 예에서는 VPN 2가 PPN 7에 mapping되어 있지만 permission은 R뿐이다. RDX가 가리키는 그 memory에 RAX 값을 store하려 하면 CPU가 금지된 write를 발견하여 exception을 일으키고 OS가 처리한다. 강의는 이 예를 process 종료로 설명한다(STT 01:06:53–01:08:38).

이는 앞의 정상 page-in 뒤 retry와 다르다. 주소를 찾을 수 있는가, 현재 resident인가, 요청한 접근이 허용되는가는 각각 다른 판정이다. Stack 실행을 피하려는 동기는 있지만 불명확한 발화에서 상세 공격 기법을 만들지는 않는다.

## Private pointer가 shared object를 가리키는 예

STT 01:08:38–01:18:04는 이전의 `layout.c`를 실제 mapping으로 설명한다. Source는 `sizeof(struct __shared)` 크기의 영역을 `mmap`으로 만들며 `PROT_READ|PROT_WRITE`, `MAP_ANONYMOUS|MAP_SHARED`를 사용한다. Struct에는 semaphore `m`과 `shared_int`가 있다. `sem_init(&shared->m, 1, 1)`은 process-shared 사용과 초기값 1을 지정하고 `shared_int`는 0으로 시작한다. 이 설명에서는 semaphore를 우선 lock처럼 이해한다. 원본에는 `MAP_FAILED` 검사, delay, sleep도 있지만 모든 행을 강의에서 낭독했다고 볼 수는 없다.

뒤의 `fork` loop는 `nproc=2`이면 추가 process 하나를 만든다. 두 process는 별도의 address space를 갖는다. `global_int`와 pointer variable `shared` 자체가 있는 VPN 2는 A에서 PPN 1, B에서 PPN 7이다. 반면 `shared`가 가리키는 struct의 VPN 3은 둘 다 PPN 2다. **Pointer를 저장하는 공간은 private이면서 pointee는 shared**일 수 있다. 같은 variable 이름과 같은 VA가 같은 physical storage를 뜻하지 않는다.

각 process가 자기 `global_int`를 증가시키는 일은 독립적이다. `shared_int` 증가 구간은 shared region 안의 semaphore에 대한 `sem_wait`와 `sem_post` 사이에 있어 동시에 수행되지 않도록 한다. 그래서 private counter들은 따로 증가하고 shared counter는 두 process의 작업을 합친다. 특정 출력 interleaving은 보장되지 않는다. STT의 “So, the result is different.”가 pointer 저장 위치와 값 중 무엇을 가리키는지 불명확하므로 pointer 값이 반드시 서로 다르다고 결론내리지 않는다. 복사 설명은 논리적 private semantics이며 즉시 physical 전체 복제를 보장하지 않는다.

## 역사적 Core i7 모델의 두 cache 계층

이제 translation 정보와 실제 data가 각각 어디에 cache되는지 분리할 수 있다. RM001/NM003 slide 39와 STT 01:18:04–01:21:26은 약 2009년의 네-core Core i7 모델을 사용한다. 현재 모든 Core i7의 사양이 아니다.

| 구조 | 제공 모델의 용량·associativity | 범위 |
|---|---|---|
| L1 instruction / data cache | 각각 32 KiB, 8-way | Core별 분리 |
| L2 unified cache | 256 KiB, 8-way | Core별 |
| L3 unified cache | 8 MiB, 16-way | Cores 공유 |
| L1 DTLB / ITLB | 64 / 128 entries, 각각 4-way | Data / instruction translation |
| L2 unified TLB | 512 entries, 4-way | Translation |

Branch 없는 instruction 접근은 순차적이어서 data 접근보다 예측하기 쉽다는 설명도 이 모델에 연결된다. Source는 DDR3 memory controller 총 32 GB/s, QPI를 통한 다른 cores·I/O bridge 연결을 제시한다. 이들은 역사적 구성의 맥락이며 모든 세부 숫자가 발화되었다는 뜻은 아니다.

### VA에서 TLB set와 tag 구하기

제공 모델의 주소 분할은 `48 = 36 + 12`, 즉 VPN 36 bits와 VPO 12 bits다. VPN은 다시 TLBT 32 bits와 TLBI 4 bits로 나뉜다. TLBI가 `2^4=16` sets 중 하나를 고르고, 그 set 안의 4 ways에서 valid translation의 tag를 비교한다. 총 용량은 `16×4=64 entries`이며 같은 set에 최대 네 translation을 보관한다. STT 01:22:13–01:23:55의 “at least four”는 곧 “up to four”로 정정된다. “32 bits is now divided…”라는 발화는 36-bit VPN 도식과 맞지 않아 분할식의 근거로 쓰지 않는다.

TLB hit이면 40-bit PPN을 얻는다. Miss이면 36-bit VPN을 9 bits씩 네 부분으로 나누어 page-table walk를 수행한다. CR3가 시작 위치를 주고 각 단계의 선택을 거쳐 마지막 PTE의 PPN을 얻으며, 얻은 translation을 TLB에 보관해 다음 접근에 재사용한다(STT 01:24:41–01:25:41). TLB에 없다는 사실은 page가 DRAM에 없다는 뜻이 아니다. Resident page는 table walk로 해결할 수 있다. 네 단계와 9-bit 분할은 실제 설명된 범위지만 후속 directory별 영역 크기와 모든 PTE flags까지 포함하지 않는다.

[EX:sp_2025_1_midterm_q04 p.11] Q4(a)의 field 구분, [EX:sp_2025_1_midterm_q04 p.12] Q4(b–c)의 PA·주어진 VA 분석, [EX:sp_2025_1_midterm_q04 p.13] Q4(d)의 TLB/page-table 판정은 이 구분의 선택적 적용이다. 먼저 **그 문항의** page size와 주소 폭에서 offset·VPN·PPN 폭을 다시 구하고, set 안의 valid/tag를 확인하고, miss이면 유효한 page-table mapping을 조사한다. PTE를 확인하기 전에 PA를 확정하지 않는다. 문제의 작은 주소 모델과 이 Core i7 모델의 bit 수를 섞지 않으며, private 표와 답을 본문에 복제하지 않는다.

### PA에서 data cache의 byte까지

40-bit PPN에 보존된 12-bit PPO를 붙이면 이 모델의 PA는 52 bits다. L1 data cache는 이를 CT 40 bits, CI 6 bits, CO 6 bits로 읽는다. CI는 `2^6=64` sets 중 하나, CT는 그 안의 8 ways에서 비교할 physical tag, CO는 64-byte line 내부의 byte 위치다. 용량은 `64×8×64 = 32768 bytes = 32 KiB`다.

이 계산에서 TLB의 64 **entries**와 data cache의 64 **sets**는 다른 수다. Translation hit는 주소 정보를 주고 data-cache hit는 내용 bytes를 준다. 한 `char`만 요청하면 program이 필요한 것은 line 전체가 아니라 해당 byte일 수 있다. L1 miss는 L2, L3, main memory 쪽으로 이어진다(STT 01:26:40–01:29:55).

강의는 PA를 얻고 cache를 찾는 논리적 순서로 설명하지만, 변하지 않는 page-offset bits로 index 일부를 미리 사용할 수 있는 동시 lookup도 언급한다. Physical tag를 쓴다고 모든 index 작업이 translation 완료 뒤에만 시작되는 것은 아니다. 불명확한 “six step order”를 정식 6단계 알고리즘으로 복원하지 않고, translation의 역할과 data 선택의 역할을 나누어 주소 경로를 이해한다.

## 핵심 정리

- 주소 표현 범위는 설치된 DRAM 용량과 다르며 공유에 같은 VA가 필요한 것은 아니다.
- VPN→PPN 변환은 page 안 offset을 보존하고 page 번호와 base 주소를 구분한다.
- MMU는 hardware, page table은 memory 자료구조, TLB는 translation cache다.
- TLB miss, nonresident page fault, 금지된 write는 서로 다른 사건이다.
- Private pointer object가 shared pointee를 가리킬 수 있다.
- 역사적 48-bit VA·52-bit PA와 다른 toy model의 수치를 섞지 않는다.

## 확인·연습문제

### 개념 확인과 설명

#### 확인 Q01 · 주소 abstraction의 목적

Load/store, 64-bit byte address 규모와 실제 DRAM을 구분하라. Process의 영역·protection·sharing에 indirection이 필요한 이유와 LAN/IP·virtual machine 비유의 공통점은?

<details><summary>해설 보기</summary>

Load는 memory→register, store는 register→memory다. 표현 공간은 2^64 bytes=16 EiB이지 그만큼 설치된 RAM이 아니다. Process의 text/data/heap/stack을 physical memory에 배치하면서 임의 타 process 접근은 막고 지정 데이터는 공유해야 한다. Mapping이 process VA와 physical 위치를 분리한다. IP/MAC과 logical/physical machine 비유도 위의 통일된 인터페이스와 아래 구체 구현의 분리다. Private 공간은 명시 shared region을 금지하지 않으며 비유가 전체 network/virtualization 구현을 뜻하지 않는다.

**채점·점검 기준:** 16 EiB의 의미와 두 요구·두 주소의 분리를 설명한다.

</details>

#### 확인 Q02 · Page 번호·offset·base

Mapping 단위와 VPN/PTE/PPN을 설명하고 PS=0x100,PT[2]=5일 때 VA0x233을 계산하라. Source의 `0x233 & 0xF00`과 `PT[VA/PS]+VA%PS`에는 어떤 한정·교정이 필요한가?

<details><summary>해설 보기</summary>

Page는 고정 mapping 단위, VPN은 입력 page 번호, PTE는 한 entry, PPN은 출력 번호다. VPN=floor(0x233/0x100)=2, offset=0x33, base=5×0x100=0x500, PA=0x533이다. Mask 결과는 2가 아니라0x200이므로 >>8이 필요하다. PT가 PPN을 반환하면 `PT[VPN]*PS+offset`, base를 반환할 때만 인쇄 덧셈식이 맞다. 같은 page 크기에서 offset은 유지한다. 일반 4 KiB·큰 2 MiB/1 GiB와 이 toy 256 bytes를 섞지 않는다.

**채점·점검 기준:** 2/0x33/0x500/0x533와 두 인쇄식의 문제를 모두 확인한다.

</details>

#### 확인 Q03 · MMU·table·register·TLB

MMU, main-memory page table, PTBR/CR3, TLB가 각각 보유·수행하는 것은? TLB hit가 줄이는 작업과 data cache와의 차이를 설명하라.

<details><summary>해설 보기</summary>

OS가 관리하는 table은 main memory의 mapping 자료다. PTBR/CR3는 시작 위치, MMU는 이를 사용하는 변환 hardware다. TLB는 자주 쓰는 일부 translation 정보를 보유해 반복 table 탐색 비용을 줄인다. 모든 PTE를 register 안에 담거나 실제 program bytes를 cache하는 것이 아니다. TLB hit는 translation 정보, data-cache hit는 내용을 얻는 사건이다.

**채점·점검 기준:** 네 역할과 translation/content 차이를 명확히 구분한다.

</details>

#### 확인 Q04 · 공유 VA와 virtual 용량

A VPN1/B VPN1→PPN1과 A VPN4/B VPN6→PPN6을 비교하라. 이 공유 비교와 별개의 용량 예에서 세 process A/B/C는 각각 virtual pages 7개를 가지며, PS=0x100이고 physical memory는 11 pages다. 각 process와 전체의 virtual bytes, physical bytes를 계산하고 모순이 아닌 이유를 설명하라.

<details><summary>해설 보기</summary>

첫 공유는 같은 VPN,둘째는 다른 VPN으로 같은 PPN을 가리킨다. 공유의 핵심은 physical mapping이며 VA 일치가 아니다. 각0x700,총21 pages=0x1500 bytes와 physical0xB00이다. 모든 virtual page를 동시에 별도 resident frame으로 예약하지 않고 table 자체도 physical memory를 쓴다. Isolation 표와 sharing 표는 다른 상태여서 mapping 숫자를 섞지 않는다.

**채점·점검 기준:** 두 공유 관계,0x700/0x1500/0xB00, residency 한정을 확인한다.

</details>

#### 확인 Q05 · Table 규모와 중복 절감

4 KiB page에서 full64-bit와 역사적48-bit VA의 page 수,후자의 byte 공간을 구하라. Multilevel table과 libc sharing의 동기는 어떻게 다르며 COW는 어디까지 배운 범위인가?

<details><summary>해설 보기</summary>

Offset12 bits이므로64-bit는2^52 pages,48-bit는 VPN36→2^36 pages이며 byte 공간은2^48=256 TiB다. 256조 pages가 아니다. 작은 프로그램에도 모든 VPN entry를 flat array로 두면 너무 커져 계층적 table이 필요하다. Libc/printf 공통 page sharing은 불필요한 내용 복제를 줄인다. COW/lazy copy는 이름·동기·후속 예고까지만이며 write-fault 복사 구현이나 fork의 무조건 eager copy를 주장하지 않는다.

**채점·점검 기준:** Page 수와 byte 수를 구분하고 table 크기와 내용 중복의 두 문제를 설명한다.

</details>

#### 확인 Q06 · Page-in과 clean eviction

VPN2가 disk에 paged out인 별도 상태에서 VA0x233을 접근하면 retry 전 어떤 일이 필요한가? Clean file-backed victim과 modified victim의 차이,모든 fault에 대한 일반화 한계는?

<details><summary>해설 보기</summary>

Fault로 실행을 잠시 중단하고 필요하면 replacement로 공간 확보→disk page 읽기→PTE 갱신→faulting instruction 재실행이다. 앞의 VPN2→PPN5 성공 상태와 섞지 않는다. 같은 원본이 disk에 있는 clean page는 버린 뒤 재읽기 가능해 새 writeback을 생략할 수 있다. Modified 내용은 버리기 전에 보존해야 한다. 이 예는 복구 가능한 disk-backed fault로 모든 fault가 disk I/O나 종료를 요구하지 않는다.

**채점·점검 기준:** 네 복구 단계와 clean/modified 보존 차이를 명시한다.

</details>

#### 확인 Q07 · Resident여도 금지된 write

VPN2→PPN7이고 permission이 R뿐이다. RDX가 가리키는 주소에 RAX를 store하려 할 때 왜 성공한 mapping만으로 충분하지 않은가? Nonresident fault와 비교하라.

<details><summary>해설 보기</summary>

Page는 찾을 수 있어도 write 허용이 없다. CPU가 금지 접근 exception을 만들고 OS가 처리하며 source는 이 경우 종료로 단순화한다. 적법한 nonresident 접근은 page-in·PTE 갱신 뒤 재시도할 수 있다. Mapping 존재,residency,요청 동작 permission을 따로 판정해야 한다.

**채점·점검 기준:** Write 권한 부재를 원인으로 적고 두 fault 경로를 구분한다.

</details>

#### 확인 Q08 · Shared mapping 준비

layout.c의 mmap 크기·protection·mapping flags,구조체 내용·초기화, nproc=2의 process 수를 설명하라. Semaphore와 code의 어떤 범위까지만 주장하는가?

<details><summary>해설 보기</summary>

Size는 sizeof(struct __shared),PROT_READ|PROT_WRITE와 MAP_ANONYMOUS|MAP_SHARED다. Semaphore m과 shared_int를 두고 `sem_init(&shared->m,1,1)`로 process-shared·초기값1,integer는0으로 시작한다. `fork` loop는 추가1 process로 총2다. Semaphore는 shared increment의 lock처럼 설명된 범위이며 source의 MAP_FAILED 검사·delay·sleep 모든 줄이 발화되었다고 하지 않는다.

**채점·점검 기준:** Flags·두 member·초기값·총2 process와 범위 한정을 확인한다.

</details>

#### 확인 Q09 · Private pointer·shared pointee

VPN2가 A→PPN1,B→PPN7이고 VPN3은 둘 다 PPN2다. Global과 pointer shared가 VPN2,pointee m/shared_int가 VPN3일 때 어떤 상태가 독립·공유이며 increment는 어떻게 보호되는가? Pointer 값과 출력 순서에 무엇을 보장할 수 없는가?

<details><summary>해설 보기</summary>

Global과 pointer object는 별도 physical storage지만 pointer가 가리키는 struct는 같은 PPN2다. 그래서 global_int는 각자 증가하고 shared_int는 공동 증가한다. Semaphore도 공유되어 sem_wait–increment–sem_post 구간의 동시 갱신을 막는다. Private pointer라는 이유로 저장한 VA 값이 반드시 다르지는 않으며 특정 출력 interleaving이나 모든 physical page의 eager copy를 보장하지 않는다.

**채점·점검 기준:** 저장공간과 pointer 값·pointee를 세 가지로 구분하고 semaphore도 공유임을 명시한다.

</details>

#### 확인 Q10 · 역사적 Core i7의 계층

제공 four-core 모델의 L1I/L1D,L2,L3 용량·ways·공유 관계와 DTLB/ITLB/L2 TLB entry·ways를 쓰라. Instruction locality,DDR3/QPI 수치는 어떤 맥락인가?

<details><summary>해설 보기</summary>

L1I와 L1D는 core별 각각32 KiB/8-way,L2는 core별 unified256 KiB/8-way,L3는 shared8 MiB/16-way다. L1 DTLB64,ITLB128,L2 unified TLB512 entries이며 각각4-way다. Branch 없는 instruction 순차 접근은 data보다 예측하기 쉬운 경향을 설명한다. DDR3 총32 GB/s와 QPI 연결은 약2009년 모델의 맥락이며 현재 모든 Core i7 사양이나 모든 그림 label의 발화를 뜻하지 않는다.

**채점·점검 기준:** Data와 translation 용량의 단위를 구분하고 각 공유 범위를 확인한다.

</details>

#### 확인 Q11 · TLB 분할과 table walk

48-bit VA,4 KiB page,64-entry4-way TLB에서 VPO/VPN/TLBI/TLBT 폭과 set 수를 도출하라. Hit의 PPN 폭과 miss의 네 단계·CR3 역할은? 왜 miss가 항상 page fault는 아닌가?

<details><summary>해설 보기</summary>

VPO12,VPN36이다. Sets64/4=16→TLBI4,TLBT36−4=32이며 set에 최대4 translations다. Hit는40-bit PPN,miss는 VPN36을9-bit씩 네 부분으로 나누어 CR3 시작점에서 table walk한다. 최종 PTE를 얻어 translation을 TLB에 저장한다. TLB에 없어도 page가 resident이면 disk page-in 없이 가능하다. Source의 'at least'는 'up to'로 정정되고32-bit VPN 발화는36-bit 도식과 구분한다.

**채점·점검 기준:** 48=36+12,36=32+4,16×4=64,4×9=36과 resident miss를 확인한다.

</details>

#### 확인 Q12 · PA에서 data byte까지

40-bit PPN+12-bit PPO로 만든 PA를 CT40/CI6/CO6으로 나눈다. 각 field 역할,sets·ways·line 크기·전체 용량,TLB64 entries와 차이,L1 miss와 overlap 가능성을 설명하라.

<details><summary>해설 보기</summary>

PA는52 bits이며 CI6은64 sets,CT40은 선택 set의8 ways에서 physical tag 비교,CO6은64-byte line의 byte 선택이다. 64×8×64=32768 bytes=32 KiB다. TLB64는 mapping entry 수이고 여기64는 data set 수다. `char` 요청은 해당1 byte만 필요할 수 있으며 L1 miss는 L2/L3/main memory로 간다. VPO=PPO의 변하지 않는 bits로 일부 index lookup을 translation과 겹칠 수 있어 physical tag가 모든 작업의 순차 대기를 뜻하지 않는다.

**채점·점검 기준:** 52-bit 합·32 KiB 계산·두64의 단위와 overlap 한정을 확인한다.

</details>

### 적용과 점검

#### 연습 P01 · TLB miss를 fault와 구별하기

**새로 만든 합성 연습.** [EX:sp_2025_1_midterm_q04 p.11] Q4(a),[EX:sp_2025_1_midterm_q04 p.12] Q4(b–c),[EX:sp_2025_1_midterm_q04 p.13] Q4(d)의 주소 분할과 TLB→PTE 판단을 사용한다. 선수는 본문의 offset·set/tag·resident·permission이며 역사적 Core i7 bit 수와 별개다.

VA12 bits,PA10 bits,page64 bytes,TLB4 entries/2-way이며 모든 TLB entry는 처음 invalid다. VPN0x12는 resident PPN5/RW,VPN0x13은 적법하지만 disk에 paged out,VPN0x14는 resident PPN7/R이다. 다른 접근·mapping 변경은 없고 성공한 walk는 TLB에 채운다.

순서대로 read VA0x4A7,read0x4B2,read0x4E0,write0x501을 판정하라. 마지막 두 fault는 처리하지 않은 상태로 분류만 한다. Field 폭,첫 요청 set/tag/PA,두 번째 hit 이유,뒤 두 실패의 차이를 설명하라.

<details><summary>해설 보기</summary>

Offset6 bits,VPN6,PPN4다. TLB는2 sets→index1,tag5다. 0x4A7/64는 VPN0x12,offset0x27;set0,tag0x9이며 처음 miss라도 PTE가 resident RW여서 PA=5×64+0x27=0x167로 성공하고 translation을 채운다. 0x4B2도 VPN0x12,offset0x32라 TLB hit,PA0x172다. 0x4E0은 VPN0x13,offset0x20이며 paged-out fault라 현재 resident PA를 확정하지 않는다. 0x501은 VPN0x14,offset1이고 resident라도 R-only여서 write protection fault다. Mapping 산술과 허용된 접근을 구분하고 모든 TLB miss를 disk fault로 부르지 않는다.

**채점·점검 기준:** 6/6/4와1/5,0x167/0x172,동일 page 재사용과 두 fault 원인을 검산한다.

</details>

### 복습 순서

Q02·Q04·Q05는 단위를 적고 계산한 뒤 Q06–Q07의 fault를 원인별로 나누라. Q08–Q09는 pointer box와 shared page를 그리고,Q10–Q12는 translation/data 경로를 따로 그린 뒤 P01의 access별 표로 합쳐 보라.

## 출처

[[courses/system_programming/lectures/2026-09-23-lecture-06|2026-09-23 · 강의 노트]]

[[courses/system_programming/lectures/2026-09-28-lecture-07|2026-09-28 · 강의 노트]]

[[courses/system_programming/transcripts/2026-09-28|2026-09-28 · 보정 STT]] — 01:07–19:55 (abstraction·주소 변환), 54:08–01:08:38 (공유·용량·fault), 01:08:38–01:18:04 (shared mapping 예), 01:18:04–01:29:55 (Core i7 경로)

[07.MM.Virtual.Memory.Recap.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/07.MM.Virtual.Memory.Recap.pptx) — slide 4; slide 5; slide 7; slide 8; slide 10; slide 11; slide 16; slide 27; slide 28; slide 29; slide 30; slide 31; slide 32; slide 34; slide 35; slide 37; slide 39; slide 40

[07.MM.Virtual.Memory.Recap_2ffc3cf7.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/07.MM.Virtual.Memory.Recap_2ffc3cf7.pptx) — slide 4; slide 5; slide 7; slide 8; slide 10; slide 11; slide 16; slide 27; slide 28; slide 29; slide 30; slide 31; slide 32; slide 34; slide 35; slide 37; slide 39; slide 40

[06.MM.Variable.and.Memory.Recap.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx) — slide 11; slide 7

9월28일의 불명확한 load/store·LAN·page 단위·TLB hit 빈도·pointer 값·six-step 발화를 복원하지 않는다. VM mask의 shift 누락과 PPN/base 식의 차이는 명시적 설명 교정이며 원문을 바꾼 것이 아니다. Source의 isolation·sharing·paged-out·protection 표는 다른 상태다. Core i7는 역사적 모델이며 전체 vector layout·어두운 이미지 label을 새로 확인한 것으로 주장하지 않는다. COW 구현·후속 PTE flags·allocator·전체 synchronization 이론은 범위 밖이다. 기출의 2024 VPN1F 중복·invalid PA 표기와 2025-2 Q4 배점 불일치는 그대로 남고 제공 답안을 정답으로 복사하지 않는다.

아래 과거 시험 연결은 명시한 추론 요구에 한정한다. 제공 답안은 참고자료이며 독립 검증된 정답으로 간주하지 않고, 현재 시험 범위나 출제 빈도를 추정하지 않는다.
