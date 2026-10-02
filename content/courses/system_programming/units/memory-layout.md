---
title: "Process memory·alignment·호출의 실제 표현"
description: "Process storage, padding, union, 값 전달과 IA-32 frame을 복습한다."
course: "system_programming"
unit_id: "memory-layout"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["06.MM.Variable.and.Memory.Recap.pptx", "EE209 AssemblyFunctions.pptx"]
private_source_assets: []
source_lectures: ["courses/system_programming/lectures/2026-09-23-lecture-06"]
---

주소 숫자보다 먼저 어느 process의 어떤 object인지 확인하자. Size·alignment·호출 규약을 분리하면 memory 그림을 계산과 code trace로 읽을 수 있다.

## Process address space와 실제 저장공간

같은 주소 숫자가 출력되어도 두 process가 같은 object를 공유하는 것은 아니다. [Pointer](objects-pointers.md)는 process의 address space 안에서 해석되며, 서로 다른 공간에는 같은 숫자의 주소가 있을 수 있다. [[courses/system_programming/lectures/2026-09-23-lecture-06|2026-09-23 memory layout 강의]]의 `layout.c`는 function, global, local, heap, shared object의 주소와 PID를 출력하여 이 관계를 관찰한다.

자료에서 PID 16074와 16075의 `global_int`는 같은 numeric virtual address에 있어도 각각 0, 1, …로 독립 증가한다. 반면 `shared_int`는 두 process의 작업을 합쳐 0부터 7까지 이어진다. 따라서 주소 비교만으로 공유를 판정하지 말고 mapping과 object의 역할을 확인해야 한다. [[courses/system_programming/transcripts/2026-09-23|2026-09-23 STT]] 09:18–12:08의 demonstration은 이 차이를 보여 준다. 그날 semaphore의 상세 설명은 미뤄졌으며, 뒤의 [Virtual Memory](virtual-memory.md)에서 9월 28일의 실제 `mmap`·`fork` 설명과 연결한다.

ASLR(Address Space Layout Randomization)은 실행마다 배치 주소를 바꾸어 예측을 어렵게 하는 완화 기법이다. 자료의 ASLR 없는 실행과 활성화된 실행의 주소 비교는 그 효과를 관찰하는 예이며 완전한 보안 보증이 아니다. 여기의 출력 숫자는 제공 예제의 결과다.

### Executable 영역, heap, stack

M016 slide 11의 target address-space model은 낮은 쪽 executable 영역에서 runtime storage로 이어진다.

| 영역 | 자료에서의 역할 |
|---|---|
| Read-only `.init`, `.text`, `.rodata` | 초기화·instruction code, 배치된 constant data와 literal |
| Read/write `.data`, `.bss` | 초기값을 가진 global data와 zero-initialized static storage |
| Heap | Runtime allocation; 전통적인 `brk` 경계는 하나의 model |
| Mapped region | Shared library 등의 mapping, 일부 allocation |
| User stack | 호출 관련 storage; target에서는 높은 주소에서 낮은 주소로 성장 |
| Kernel virtual-memory 영역 | User 공간과 구분된 OS 영역 |

초기값을 쓰지 않은 global은 임의 값이 아니라 zero-initialization 대상이다. `.bss`는 그 zero bytes 전부를 executable에 저장할 필요가 없다는 표현과 연결된다. Automatic local의 미초기화 값에는 같은 보장이 없다. 큰 allocation이 mapped region을 사용할 수 있으므로 모든 `malloc` 결과가 하나의 `brk` heap 안에 있다고 단정하지 않는다. 모든 local과 parameter가 stack에 있다는 보장도 없다. 뒤의 assembly 예는 parameter register를 직접 사용한다.

STT 17:04–18:01은 memory protection(메모리 보호)을 물리 저장 능력과 구분한다. Read-only와 read/write 영역이 같은 종류의 쓰기 가능한 DRAM에 놓여도 process에 허용된 접근은 다를 수 있다. OS가 CPU의 도움을 받아 금지된 write를 감지할 수 있기 때문이다. ‘Read-only’는 반드시 별도의 물리 ROM이라는 뜻이 아니다. 한편 string literal 수정은 C의 undefined behavior이므로 특정 OS의 보호 사례를 근거로 모든 구현에서 같은 crash가 난다고 예측해서는 안 된다.

## Size와 alignment는 별개의 조건

Machine은 integer, address, floating data, vector data를 처리하고 compiler는 array와 struct를 연속 bytes로 구성한다. 자료는 1·2·4·8-byte integer와 4·8·10·16-byte floating 표현을 소개한다. 이 숫자는 storage·표현·ABI를 구분해서 읽어야 한다.

Alignment(정렬) K는 시작 주소가 K로 나누어떨어져야 한다는 배치 조건이다. 4-byte alignment의 주소는 0, 4, 8, 12, …다. Size는 object가 차지하는 양이고 alignment는 시작할 수 있는 위치의 조건이다.

| Type | x86-64 Linux size/alignment 예 | IA32 Linux size/alignment 예 |
|---|---:|---:|
| `long` | 8 / 8 | 4 / 4 |
| `double` | 8 / 8 | 8 / 4 |
| `long double` | 16 / 16 | 12 / 4 |
| `void *` | 8 / 8 | 4 / 4 |

이 표는 M016의 측정 예이며 모든 platform의 규칙이 아니다. 특히 size 8인 `double`도 IA32 예에서는 alignment 4다. M016의 Windows 열에 적힌 `long` 8을 모든 Windows ABI의 사실로 확대하지 않는다. Historical `long double`의 표현 정밀도와 storage도 다르다.

경계를 가로지르는 접근은 추가 memory transaction이나 page-boundary 처리를 요구할 수 있다. Architecture에 따라 허용 여부, 비용, atomicity가 다르므로 ‘unaligned이면 항상 실패한다’나 ‘aligned이면 모든 폭에서 atomic하다’는 결론은 성립하지 않는다. Compiler는 target ABI의 조건을 맞추기 위해 padding을 삽입한다.

### Dummy byte로 alignment 관찰하기

M016 slide 28의 `SIZE(t)`는 `sizeof(t)`를 사용한다. `INFO(t)`는 `char dummy` 뒤에 `t data`를 둔 임시 struct를 만들고 `#t`로 type 이름을 문자열화한다. `OFS`는 `data` 주소에서 struct 시작 주소를 빼 offset을 구한다. 첫 byte가 dummy이므로 offset이 8이면 padding은 8이 아니라 `8 - 1 = 7` bytes다.

앞 표의 두 번째 숫자는 이 배치에서 관찰한 offset으로 alignment를 드러낸다. 자료의 `gcc -m32`/`-m64` 출력은 target별 차이를 보이지만 여기서 다시 실행한 결과는 아니다. Integer로 pointer를 변환하는 원본 macro와 생략된 선언을 모든 구현에 이식 가능한 완성 측정 도구로 읽지는 않는다. STT 50:07의 size/alignment 혼동 대신 두 양의 정의를 분리한다.

## Padding을 계산하여 array stride 구하기

주어진 주소들에서 gap은 `현재 주소 - 이전 주소 - 이전 object size`다. M016 slide 32의 끝자리로 계산하면 `int`가 `0x40..0x43`, `char`가 `0x44`, `short`가 `0x46`에 있어 gap은 1이다. `long long`이 `0x48`, `char` 둘이 `0x50`, `0x51`, `float`가 `0x54`이면 gap은 2다. `char` `0x58` 뒤 `double` `0x60` 앞에는 7, 그 8-byte double 뒤 `long double` `0x70` 앞에는 8 bytes가 남는다. 이는 자료에서 관찰한 global 배치이지 선언 순서가 모든 compiler의 global 주소 순서를 보장한다는 뜻은 아니다.

Struct에서는 member가 선언 순서를 유지하며 겹치지 않고 배치되고, 필요한 internal padding과 tail padding을 갖는다. [system_programming:M016 slide 37](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)의 예를 계산해 보자.

```c
struct S2 {
    double v;
    int i[2];
    char c;
};
```

| Member | 시작 offset | Size |
|---|---:|---:|
| `v` | 0 | 8 |
| `i[0]` | 8 | 4 |
| `i[1]` | 12 | 4 |
| `c` | 16 | 1 |
| Tail padding | 17 | 7 |

Payload는 17 bytes지만 다음 struct의 `double`도 8-byte aligned여야 한다. 따라서 `sizeof(struct S2) = 24`이고 array의 `a[1]`, `a[2]`는 시작점에서 각각 24, 48 bytes 뒤다. 원본 그림에서는 array의 각 element 폭이 24이고 확대된 element 끝에 7-byte 영역이 있다는 점을 보면 된다. Tail padding은 다음 element의 alignment를 유지하는 데 필요하다.

[EX:sp_2025_1_midterm_q01 p.2] Q1(b)와 이어지는 [EX:sp_2025_1_midterm_q01 p.3]의 적용 요구도 member offset, 전체 struct 크기, typed pointer의 이동 단위를 분리하는 것이다. 각 member를 정렬한 뒤 전체 크기를 struct alignment의 배수로 올리고, 마지막에 array 개수를 곱한다. Private 문항의 숫자 답을 복제하지 않아도 이 순서로 낯선 선언을 분석할 수 있다.

### Union은 합계가 아니라 겹치는 storage

Struct가 별도 member 영역을 두는 반면 union의 모든 member는 offset 0에서 시작한다. Member 주소는 union 시작점과 같고, 필요한 alignment는 가장 강한 member 요구를 충족해야 한다. 따라서 size를 member 크기의 합으로 계산하지 않는다. M016의 `max(member size)`는 출발점이며 일반적으로는 그 크기를 union alignment에 맞게 반올림하는 padding도 고려한다. 같은 bytes를 겹쳐 쓴다는 사실은 여러 member의 독립 값을 동시에 보유한다는 뜻이 아니다. 상세 type-punning 규칙은 여기서 추가하지 않는다.

## C의 값 전달이 machine 동작으로 보이는 방식

Caller에 `x = 5`, `y = 6`이 있을 때 `foo(int a, int b)`가 `a`를 두 배로 하고 `a + b`를 반환하면 local `a = 10`, 결과 16이지만 caller `x = 5`는 유지된다. `foo(int *a, int b)`에 `&x`를 넘겨 `*a`를 두 배로 하면 `x = 10`, 결과 16이다. 두 경우 모두 C는 값을 복사한다. 두 번째에서는 복사된 값이 주소다.

M016 slide 44의 target assembly에서 `mov (%rdi), %eax`는 그 주소의 5를 load하고, 덧셈으로 10을 만든 뒤 `mov %eax, (%rdi)`가 caller memory에 store한다. 이후 `%esi`의 6을 더해 반환한다. Pointer register RDI 자체를 10으로 바꾸는 것이 아니다.

Array `x = {0,1,…,9}`를 넘겨 `a[2] = 5`를 수행하면 세 번째 원소가 바뀐다. Slide 46의 핵심 instruction은 다음과 같다.

```asm
movl $0x5, 0x8(%rdi)
```

Four-byte int의 index 2이므로 displacement는 `2 * 4 = 8` bytes다. Array 전체를 복사하지 않고 caller storage에 5를 쓴다. 이는 제공 target convention이며 모든 architecture가 같은 register를 쓰는 것은 아니다. 원본의 `int` function에 return이 생략된 점도 완성 API의 모범으로 삼지 않는다.

Command-line의 `argc`는 argument 수, `argv`는 `char *`들의 array다. 자료의 정상 호출에서 `argv[0]`은 program name이다. 이 예를 가능한 모든 C 실행환경의 무조건적 보장으로 확대하지 않는다.

Q1(c)의 memory-section 분석([EX:sp_2025_1_midterm_q01 p.3], [EX:sp_2025_1_midterm_q01 p.4])에서는 pointer object와 literal, local `const` object를 분리해야 한다. Writable 영역에서 관찰됐다는 이유로 원래 `const` object를 cast 후 수정해도 된다는 결론은 나오지 않는다. OS의 보호 결과와 C의 유효성은 별도 판정이다.

## IA-32 call과 stack frame의 자료 기반 복습

[system_programming:NM004](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/EE209.AssemblyFunctions.pptx)는 선택적 IA-32 자료 복습이다. 앞의 x86-64 parameter-register 예와 혼합하지 않는다. 고정된 한 지점으로 jump했다가 돌아오는 방식은 여러 caller에 대응하기 어렵다. Return address 하나만 EAX에 보관해도 `P → Q → R`에서 Q의 다음 호출이 이전 return address를 덮는다. 호출은 마지막에 시작한 것이 먼저 끝나므로 LIFO stack이 자연스럽다.

이 자료의 `pushl`은 ESP를 4 낮춘 뒤 저장하고 `popl`은 읽은 뒤 ESP를 4 높인다. `call`은 다음 instruction의 주소를 암묵적으로 저장하고 이동하며 `ret`는 그 저장 주소로 돌아간다. 표의 `pushl %eip`/`pop %eip`는 이 효과를 나타낸 의사 연산이지 EIP를 그렇게 직접 조작하는 실제 instruction 예가 아니다.

`add3(3,4,5)`의 caller는 5, 4, 3 순서로 push한 뒤 call한다. Callee 진입 직후 첫 인자는 `ESP+4`다. Prolog가 old EBP를 push하고 `EBP=ESP`로 고정하면 세 인자는 `EBP+8`, `+12`, `+16`에서 찾는다. ESP는 local 확보와 추가 call로 움직일 수 있으므로 EBP가 고정 기준을 제공한다. Local `d`만 확보하면 `EBP-4`이지만, full trace처럼 EBX·ESI·EDI를 각각 4 bytes 저장하고 `d` 4 bytes를 확보하면 `d`는 `EBP-16`이다. 이 offset은 push 순서의 계산이며 전체 frame 그림의 화살표를 새로 해석한 주장은 아니다.

자료의 caller-save는 EAX·ECX·EDX, callee-save는 EBX·ESI·EDI다. 호출 전 값을 나중에 사용할 때 해당 책임 주체가 저장·복원한다. `add3`가 후자의 register를 바꾸지 않으면 그 저장은 불필요할 수도 있다. Callee는 필요한 register와 ESP/EBP를 복원하여 return하고 caller는 세 인자의 12 bytes를 치운다. 반환값 `3+4+5=12`는 EAX에 있으므로 old EAX를 복원하기 전에 필요한 곳에 보존해야 한다.

NM004 slides 52–53의 EBX·ESI·EDI 저장 주석은 ‘caller-save’라 적혀 있으나 slides 40·51의 callee-save 설명과 충돌한다. 또한 slides 59–61의 `addl %12,%esp`는 잘못된 immediate 표기이며 slides 26·58의 `$12`와 구분한다. 각 active invocation의 frame이라는 개념을 이해하되, 모든 최적화된 함수가 EBP frame이나 stack local을 반드시 갖는다고 일반화하지 않는다. Floating-point·aggregate 반환의 상세 ABI는 이 복습 범위 밖이다.

## 핵심 정리

- 같은 virtual address라도 process가 다르면 private object는 독립일 수 있다.
- Read-only는 접근 권한이며 물리 ROM이나 특정 C crash 보증이 아니다.
- Size는 공간의 양, alignment는 시작 주소 조건이며 tail padding은 다음 array element를 정렬한다.
- C는 주소도 값으로 전달하므로 pointer 복사와 caller memory 쓰기는 양립한다.
- IA-32 stack 인자와 x86-64 register 인자를 섞지 않고 각 push·store를 추적한다.

## 확인·연습문제

### 개념 확인과 설명

#### 확인 Q01 · 같은 주소, 다른 상태

두 process의 `global_int` 주소는 같은데 각각 0,1,…이고 `shared_int`는 합쳐 0..7이다. 무엇이 공유 여부를 결정하는가? ASLR이 바꾸는 것과 보장하지 않는 것은?

<details><summary>해설 보기</summary>

주소는 process address space 안에서 해석된다. Private global은 같은 숫자라도 다른 storage이고 shared mapping은 같은 object에 연결될 수 있다. Source 출력에서 global의 독립 sequence와 shared의 연결된 sequence가 이를 보여 준다. ASLR은 실행별 배치를 바꾸어 예측을 어렵게 하지만 완전한 보안을 보증하지 않는다. 9월23일 semaphore 상세는 미뤄졌고 뒤 날짜의 mapping 설명과 구분한다.

**채점·점검 기준:** 주소값과 mapping을 분리하고 source 관찰·ASLR 한정을 유지한다.

</details>

#### 확인 Q02 · 영역·초기값·접근 권한

`.text/.rodata/.data/.bss`, heap, mapped region, stack의 역할을 나누라. 초기값 없는 global과 automatic local은 같은가? Writable DRAM 위 read-only 영역과 literal/const 수정의 C 규칙은 어떻게 다른가?

<details><summary>해설 보기</summary>

Text는 instruction, rodata는 배치된 constant/literal, data는 초기값 있는 global, bss는 zero-initialized static storage다. Heap은 runtime allocation, mapping은 library·공유 영역·일부 allocation, stack은 target의 호출 관련 storage다. Global은 zero-initialized지만 automatic local에는 같은 보장이 없다. 모든 malloc이 brk heap, 모든 parameter가 stack인 것도 아니다. OS·CPU는 물리적으로 쓸 수 있는 DRAM에도 process write를 제한할 수 있다. Literal 또는 원래 const object를 cast 후 수정하는 C 유효성은 별도이며 writable 위치 관찰이나 crash 부재가 허용을 뜻하지 않는다.

**채점·점검 기준:** 네 section·runtime 영역, global/local 차이, OS 보호와 C 규칙을 구분한다.

</details>

#### 확인 Q03 · Size와 alignment

K-byte aligned의 식과 4-byte alignment 주소 예를 쓰라. 자료의 x86-64/IA32 Linux에서 long·double·long double·pointer의 size/alignment를 비교하고 unaligned/atomicity 일반화가 왜 위험한지 설명하라.

<details><summary>해설 보기</summary>

주소 mod K=0이며 0,4,8,12가 예다. x86-64는 long 8/8,double 8/8,long double 16/16,pointer 8/8; IA32는 4/4,8/4,12/4,4/4다. 따라서 size 8이 alignment 8을 자동 뜻하지 않는다. 경계 횡단은 추가 transaction 또는 page 처리를 요구할 수 있고 허용·성능·atomicity는 architecture와 폭에 달린다. 모든 unaligned 실패 또는 모든 aligned atomic이라는 결론은 안 된다.

**채점·점검 기준:** 두 model의 네 쌍과 size/alignment 반례를 확인한다.

</details>

#### 확인 Q04 · Dummy byte의 offset

`INFO(t)`가 `char dummy` 다음에 `t data`를 놓을 때 SIZE, OFS, `#t`의 역할은? Data offset이 8 또는 4이면 padding은? 이 macro가 모든 C 구현에서 이식 가능한 측정인가?

<details><summary>해설 보기</summary>

SIZE는 sizeof, OFS는 data 주소−struct 시작 주소, `#t`는 type 이름 문자열화다. Offset에는 dummy 1 byte가 포함되어 padding은 7 또는 3이다. 관찰 offset은 이 배치의 alignment를 드러내며 size와 별개다. 원본의 integer pointer 변환·축약 선언은 이식성 한정이 있고 제공된 `-m32`/`-m64` 관찰값은 해당 target에 한정된다.

**채점·점검 기준:** Offset과 padding을 1 byte 차이로 구분하고 세 macro 역할을 설명한다.

</details>

#### 확인 Q05 · Global gap 계산

관찰 주소에서 char 0x44 뒤 short 0x46, char 0x51 뒤 float 0x54, char 0x58 뒤 double 0x60, 8-byte double 0x60 뒤 long double 0x70의 gap을 계산하라. 왜 일반 global 순서 규칙이 아닌가?

<details><summary>해설 보기</summary>

Gap은 next start−previous start−previous size다. 각각 2−1=1,3−1=2,8−1=7,16−8=8 bytes다. 주소와 size가 주어진 관찰을 계산한 것이며 compiler가 모든 global을 선언 순서대로 놓는다고 보장하지 않는다.

**채점·점검 기준:** 1/2/7/8과 계산식을 함께 적는다.

</details>

#### 확인 Q06 · Struct tail padding과 stride

Target double 8/8, int 4/4, char 1/1에서 `struct S2 {double v; int i[2]; char c;};`의 member offset, payload, tail padding, sizeof, array a[1]·a[2]의 offset을 구하라.

<details><summary>해설 보기</summary>

v=0,i[0]=8,i[1]=12,c=16이다. Payload 17 bytes를 alignment 8의 다음 배수 24로 올려 tail 7을 둔다. Array stride는 24여서 a[1]=base+24,a[2]=base+48이다. Tail이 없으면 다음 element의 double 시작이 17이라 alignment를 깨므로 member 합만으로 sizeof를 구하면 안 된다.

**채점·점검 기준:** 네 offset, 17+7=24, 24/48 stride를 검산한다.

</details>

#### 확인 Q07 · Union의 겹치는 storage

Size/alignment가 int 4/4, double 8/8인 union과 struct를 비교하라. Union member 주소·size·alignment와 두 값을 동시에 유지할 수 있는지 설명하라.

<details><summary>해설 보기</summary>

Union member는 모두 offset 0에서 겹치고 가장 강한 alignment 8을 만족한다. 최대 member size 8을 8의 배수로 맞추므로 이 조건에서는 sizeof 8이다. Struct처럼 두 member size를 더하지 않는다. 같은 bytes를 바꾸므로 두 독립 값을 동시에 저장하지 못한다. 일반적으로 최대 size를 alignment에 올려야 할 수도 있으며 상세 type-punning 규칙은 여기서 판단하지 않는다.

**채점·점검 기준:** Offset 0, size/alignment 8, 겹침과 독립 값 부재를 설명한다.

</details>

#### 확인 Q08 · 값 전달과 caller memory store

x=5,y=6에서 value parameter a를 두 배로 한 반환과 pointer parameter *a를 두 배로 한 반환을 비교하라. `mov (%rdi),%eax`·store의 의미와 `movl $0x5,0x8(%rdi)`가 배열의 무엇을 바꾸는지, argc/argv도 설명하라.

<details><summary>해설 보기</summary>

두 반환은 16이지만 value 경우 x는 5, pointer 경우 x는 10이다. 둘 다 값 복사이며 후자는 주소를 복사한다. Load는 RDI의 주소에서 5를 읽고 10을 계산하여 그 주소에 store하므로 RDI 자체를 10으로 바꾸지 않는다. Array base가 RDI이고 int=4이면 8-byte offset은 index 2여서 x[2]=5다. argc는 인자 수, argv는 char pointer들의 array이며 정상 호출 예의 argv[0]은 program name이다.

**채점·점검 기준:** 두 caller 값, 공통 반환 16, memory/register 구분, 2×4 offset을 확인한다.

</details>

#### 확인 Q09 · Nested call과 return address

P→Q→R 호출에서 return address 하나만 EAX에 보관하면 왜 실패하는가? 자료의 pushl/popl/call/ret 효과와 `pushl %eip`의 지위를 설명하라.

<details><summary>해설 보기</summary>

Q가 R을 부를 때 이전 복귀 주소가 덮인다. 가장 최근 호출부터 돌아가므로 각각의 return address를 LIFO stack에 둔다. IA-32 예의 pushl은 ESP−4 뒤 저장, popl은 읽은 뒤 ESP+4다. Call은 다음 instruction 주소를 암묵 저장하고 이동하며 ret는 저장 주소로 복귀한다. `pushl %eip`/`pop %eip`는 효과의 의사 표현이지 직접 실행할 instruction 예가 아니다.

**채점·점검 기준:** 덮어쓰기 원인, LIFO, 네 instruction 효과와 의사 표현 한정을 확인한다.

</details>

#### 확인 Q10 · Frame offset과 register 책임

IA-32 add3(3,4,5)의 push 순서, callee entry·EBP prolog 뒤 인자 위치, local d만 있을 때와 EBX/ESI/EDI 저장 뒤 d의 위치를 계산하라. Caller/callee-save, 복구·인자 정리와 EAX 반환 보존도 설명하라.

<details><summary>해설 보기</summary>

5,4,3을 push한다. Entry 첫 인자는 ESP+4, old EBP 저장·EBP 고정 뒤 세 인자는 +8/+12/+16이다. d만 있으면 EBP−4, 세 register 12 bytes 뒤라면 EBP−16이다. Caller-save EAX/ECX/EDX, callee-save EBX/ESI/EDI이며 필요한 이전 값을 책임 주체가 보존한다. Callee는 필요한 register와 ESP/EBP를 복구하고 ret, caller는 인자 12 bytes를 정리한다. EAX의 결과 12를 old EAX 복구 전에 보존해야 한다. Source의 caller-save 오기와 `%12` immediate 오기는 `$12` 및 다른 slide의 분류와 구분한다.

**채점·점검 기준:** 모든 offset, 12-byte 정리, 반환값 덮어쓰기 위험, 두 원문 오류를 확인한다.

</details>

### 적용과 점검

#### 연습 P01 · Layout을 바꿔 space 절약하기

**새로 만든 합성 연습.** [EX:sp_2025_1_midterm_q01 p.2] Q1(b)의 alignment→sizeof→array stride 절차를 사용한다. 선수는 본문의 struct·union과 int 4/4,double 8/8,char 1/1이며 private 숫자 답을 옮기지 않는다.

`struct R {char c; double d; int n;};`의 offsets·sizeof와 `R[2]`의 크기를 구하라. Member 순서를 `double d; int n; char c;`로 바꾸면 무엇이 절약되는가? 같은 세 member를 union으로 바꿔도 독립 값 세 개를 유지할 수 있는가?

<details><summary>해설 보기</summary>

원래 offsets는 0,8,16이며 payload 끝은 20, tail 4로 sizeof 24다. 두 원소는 48 bytes다. 재배치하면 0,8,12이고 끝 13을 16으로 올려 sizeof 16, 두 원소 32여서 총 16 bytes 절약한다. Union은 모두 offset 0, size/alignment 8이지만 bytes가 겹쳐 독립 세 값 보존 조건을 만족하지 않는다. 절약량만 보고 union으로 바꾸면 의미가 달라진다.

**채점·점검 기준:** 두 layout의 내부·tail padding, array 총량, union 의미 차이를 각각 설명한다.

</details>

### 복습 순서

Q03–Q07은 offset·size·alignment 세 열로 계산하고 P01을 풀이 없이 다시 배치하라. Q08은 caller 값과 register/address를 분리하고 Q09–Q10은 push마다 ESP 변화와 return address를 적어 확인하라.

## 출처

[[courses/system_programming/lectures/2026-09-23-lecture-06|2026-09-23 · 강의 노트]]

[06.MM.Variable.and.Memory.Recap.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx) — slides 7, 11, 23–24, 27–28, 32, 34, 36–39, 43–46

[[courses/system_programming/transcripts/2026-09-23|2026-09-23 · 보정 STT]] — 09:18–12:08 (private/global과 shared counter 비교), 13:08 (다음 강의의 source code 재방문 예고), 17:04–18:01 (물리 DRAM과 접근 권한), 21:47 (target stack 방향)

[EE209 AssemblyFunctions.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/EE209.AssemblyFunctions.pptx) — slides 10, 26, 29, 40, 51–53, 58–61

자료의 size/alignment는 target 사례이며 Windows long 열·STT size/alignment 혼동을 보편 규칙으로 채택하지 않는다. 9월23일 공유 상태 출력은 source 관찰이고 synchronization 상세는 뒤 날짜 범위다. AssemblyFunctions 자료는 선택적 IA-32 자료 복습으로 x86-64와 별개이며 전체 frame 그림의 화살표를 새로 검증한 것은 아니다. EBX/ESI/EDI의 caller-save 오기와 `addl %12,%esp`의 잘못된 immediate 표기를 보존해 구분한다. 과거 시험 제공 crash 목록은 const 또는 literal 수정의 C 유효성을 정하지 않는다.

아래 과거 시험 연결은 명시한 추론 요구에 한정한다. 제공 답안은 참고자료이며 독립 검증된 정답으로 간주하지 않고, 현재 시험 범위나 출제 빈도를 추정하지 않는다.

[[exam_questions/sp_2025_1_midterm_q01|2025-1 중간 Q1 · C pointer (기존 미리보기)]]
