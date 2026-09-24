---
title: "Process memory·alignment·호출의 실제 표현"
description: "Memory section, padding·stride와 parameter passing을 byte 단위로 검토한다."
course: "system_programming"
unit_id: "memory-layout"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["06.MM.Variable.and.Memory.Recap.pptx"]
private_source_assets: []
source_lectures: ["courses/system_programming/lectures/2026-09-23-lecture-06"]
---

C type과 lifetime을 process memory의 배치·보호·호출에 연결한다. Alignment와 주소 계산을 명시하면 diagram을 실제 byte 관계로 검산할 수 있다.

## Virtual address와 process별 memory

[[courses/system_programming/units/objects-pointers|Object와 pointer]]에서는 주소가 object를 찾는 값이라는 점을 배웠다. 이제 그 주소를 해석하는 범위를 더해야 한다. Virtual address(가상 주소)는 process의 address space(주소 공간) 안에서 의미를 가진다. 서로 다른 두 process가 같은 숫자 주소를 출력해도, 그곳에서 읽고 쓰는 storage가 같다는 결론은 나오지 않는다.

[Variable and Memory Recap slides 5–7](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)의 `layout.c` 예는 function, global variable, local variable, heap object, shared object의 주소와 process ID를 함께 보여 준다. Address Space Layout Randomization(ASLR, 주소 공간 배치 무작위화)이 없는 실행 예에서는 대응하는 주소가 같고, 활성화된 예에서는 실행마다 일부 배치 주소가 달라진다. ASLR은 공격자가 사용할 주소를 예측하기 어렵게 하는 완화 기법이다. 주소가 달라졌다는 관찰만으로 프로그램에 취약점이 없거나 모든 공격이 차단되었다고 말할 수는 없다.

더 중요한 비교는 두 process의 **값 변화**다. 자료의 PID 16074와 16075는 각각 `global_int`를 증가시킨다. 같은 numeric virtual address를 사용해도 각 process의 값은 자기 순서대로 0, 1, …을 따른다. 반면 명시적으로 공유한 `shared_int`는 두 process에 걸쳐 0부터 7까지 이어지는 출력 예를 만든다. Private state(독립 상태)와 shared state(공유 상태)의 차이는 주소의 인쇄 모양이 아니라 mapping과 접근 대상에 있다.

이 예에는 shared memory와 semaphore가 등장하지만, 여기서 배울 수 있는 것은 출력으로 드러나는 분리와 공유의 관계다. [[courses/system_programming/transcripts/2026-09-23|9월 23일 STT 13:08]]에서는 전체 `layout.c` source 설명을 다음 강의로 미뤘고, 42:29–43:27에서는 page-table translation도 뒤로 미뤘다. 지금의 설명을 이해하려고 아직 제공되지 않은 동기화 구현이나 주소 변환 algorithm을 가정할 필요는 없다.

## Memory section과 접근 권한

### Executable의 bytes에서 runtime storage로

[Slide 11](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)의 process memory 그림은 낮은 주소에서 높은 주소로 영역의 역할을 구분한다. 아래쪽 unused 영역 위에 executable에서 온 read-only segment가 있고, 이어 read/write segment, runtime heap, shared library 등의 mapped region, user stack, kernel virtual-memory 영역이 배치되어 있다. 그림의 핵심은 절대 주소를 외우는 데 있지 않다. **어떤 bytes를 담고, 언제 생기고, 어떤 접근을 허용하는가**를 구별하는 데 있다.

| 영역 | 자료에서 설명하는 역할 | 혼동하기 쉬운 점 |
| --- | --- | --- |
| `.text` | 실행할 machine instruction | 함수 이름 자체가 별도의 data object라는 뜻은 아니다. |
| `.rodata` | 이 영역에 배치되는 constant data와 string literal | 모든 `const` object가 모든 compiler에서 반드시 이 영역에 놓인다는 규칙은 아니다. |
| `.data` | 초기값을 가진 global data 등의 writable static storage | 초기값이 존재하는 것과 실행 중 수정할 수 있는 것은 다른 속성이다. |
| `.bss` | zero-initialized static storage | 초기값을 생략한 global이 임의의 쓰레기 값을 가진다는 뜻이 아니다. |
| Heap | `malloc` 등으로 요청하는 runtime storage | 모든 allocation이 하나의 연속된 `brk` 영역에서 온다고 보장하지 않는다. |
| Mapped region | shared library 등을 위한 mapping | mapping을 사용한다는 사실만으로 모든 bytes가 다른 process와 공유되는 것은 아니다. |
| Stack | 호출과 관련된 storage의 대표 영역 | 모든 local variable과 parameter가 반드시 memory상의 stack slot에 놓이지는 않는다. |

`.bss`는 executable에 zero byte를 하나씩 모두 저장하지 않고도 loader가 zero-initialized storage를 마련하게 하는 표현과 연결된다. 반면 초기화하지 않은 automatic local variable에는 같은 zero 보장이 없다. [[courses/system_programming/units/objects-pointers|Storage duration과 초기화]]에서 구분한 언어 규칙을 실제 배치에 연결해야 한다.

그림에서 전통적인 heap 경계는 `brk`로 표시되고 heap의 확장 방향은 위쪽이다. 큰 allocation은 별도 mapped region을 이용할 수 있다. User stack은 반대로 높은 주소에서 낮은 주소로 자라는 target 예다. [[courses/system_programming/transcripts/2026-09-23|9월 23일 STT 21:47]]도 Intel CPU에서 이 방향을 설명한다. 이는 x86-64 Linux를 이해하기 위한 개념도이며 모든 platform의 고정 배치도가 아니다.

### 쓰기 가능한 DRAM과 read-only mapping

Read-only 영역을 별도의 “물리적으로 쓸 수 없는 RAM”으로 생각하면 memory protection(메모리 보호)을 이해하기 어렵다. [[courses/system_programming/transcripts/2026-09-23|9월 23일 STT 17:04–18:01]]은 read-only 영역과 read/write 영역 모두 같은 종류의 쓰기 가능한 DRAM에 놓일 수 있다고 설명한다. 물리적 저장장치가 bytes를 바꿀 수 있는 능력과 **이 process에 그 write를 허용하는가**는 별개다.

OS는 CPU의 도움을 받아 접근 권한을 강제한다. 금지된 write를 감지하면 process를 종료할 수 있다. 그러므로 프로그램은 “RAM이니 쓸 수 있다”라는 이유로 string literal이나 instruction을 수정해서는 안 된다.

여기에는 설명 수준의 구별이 하나 더 필요하다. C에서 string literal을 수정하는 것은 undefined behavior(정의되지 않은 동작)다. 특정 실행 환경의 read-only 보호가 그런 write를 잡아낼 수 있다는 사실은 모든 C 구현에서 반드시 같은 crash가 난다는 보장이 아니다. 언어의 허용 여부와 한 OS에서 관찰되는 보호 동작을 같은 규칙으로 합치지 않아야 한다.

## Size와 alignment가 결정하는 배치

### 같은 크기라도 시작 주소 조건은 다르다

Machine은 1·2·4·8-byte integer와 주소, 여러 크기의 floating-point data, vector data를 처리한다. C의 array나 structure 자체를 하나의 특별한 machine object로 이해하는 것은 아니다. Compiler가 이들을 연속된 bytes와 offset 계산으로 표현한다. 이 연결을 정하는 규약이 Application Binary Interface(ABI, 프로그램의 binary 수준 연결 규약)의 일부다.

Size는 object가 차지하는 byte 수이고, alignment(정렬 조건)는 시작 주소에 대한 조건이다. K-byte alignment는 주소가 K로 나누어떨어진다는 뜻이다. 4-byte alignment를 만족하는 주소는 0, 4, 8, 12, …이며 1, 2, 3은 아니다. **Size가 8이라는 사실만으로 모든 ABI에서 alignment도 8이라고 추론할 수는 없다.**

[Slides 23–29](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)의 Linux 예는 다음과 같다. 각 칸은 size/alignment를 byte 단위로 적었다.

| C type | x86-64 Linux | IA32 Linux |
| --- | ---: | ---: |
| `char` | 1/1 | 1/1 |
| `short` | 2/2 | 2/2 |
| `int` | 4/4 | 4/4 |
| `long` | 8/8 | 4/4 |
| `long long` | 8/8 | 8/4 |
| `float` | 4/4 | 4/4 |
| `double` | 8/8 | 8/4 |
| `long double` | 16/16 | 12/4 |
| `void *` | 8/8 | 4/4 |

`long double`의 표는 저장 크기와 alignment를 나타낸다. 강의의 역사적 extended format은 10-byte, 즉 80-bit 표현과 연결되며, storage가 16 bytes라는 이유로 곧바로 binary128 precision이라고 읽으면 안 된다. 일부 type에 표시된 취소선이나 역사적 언급도 alignment라는 주제 전체를 생략하라는 뜻은 아니다. 이 단원의 계산은 자료의 Linux target을 따른다. 다른 platform, 특히 자료 표의 Windows `long` 열까지 같은 값으로 일반화하지 않는다.

Unaligned access(정렬되지 않은 접근)가 문제 되는 이유는 단순한 형식 취향이 아니다. 하나의 datum이 memory access 경계나 page 경계를 가로지르면 추가 transaction이나 처리가 필요할 수 있다. 어떤 architecture는 허용하고 어떤 경우는 제약을 둔다. 성능과 atomicity도 조건에 따라 달라진다. 따라서 “unaligned이면 항상 실패한다”와 “aligned이면 어떤 크기든 항상 atomic하다”는 두 주장 모두 이 설명에서 나오지 않는다.

### Dummy member로 관찰하는 offset

[Slide 28](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)의 `INFO(t)` macro는 다음 모양의 temporary structure를 만들어 type의 배치를 관찰한다.

```c
struct {
    char dummy;
    double data;
} s;
```

위 코드는 `INFO(double)`이 만드는 structure 부분만 뽑은 것이다. 원래 macro에서 `SIZE(t)`는 `sizeof(t)`이고, `#t`는 type token을 문자열로 바꿔 출력 label로 쓴다. `OFS(s)`는 `s.data`의 주소에서 `s` 시작 주소를 빼어 member offset을 구한다. 자료에서는 pointer를 `unsigned long`으로 변환해 뺀다. 이는 제시된 target을 관찰하는 교육용 방식이며, 그 변환이나 원문의 `main` 선언까지 portable한 완성 도구로 받아들여서는 안 된다.

`dummy`는 1 byte다. x86-64 예에서 `data`의 offset이 8이면, 그 8 bytes에는 **dummy 1 byte와 padding 7 bytes**가 함께 들어 있다. Offset 8 전체를 padding이라고 부르면 1 byte를 중복 계산하게 된다. IA32 예의 `double`은 size가 8이지만 offset은 4여서 dummy 뒤 padding은 3 bytes다.

자료의 `gcc -m32`와 `gcc -m64` 출력은 앞 표의 차이를 관찰한 예다. 새 machine에서 실행한 측정값으로 제시하는 것은 아니다. [[courses/system_programming/transcripts/2026-09-23|9월 23일 STT 50:07]]의 size·alignment 관련 불명확한 표현은 이 계산에서 자료의 주소 차이와 type 크기로 구분한다.

## Padding과 composite object의 크기

### Global address 사이의 빈 bytes 계산

[Slide 32](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)는 global variable의 주소를 출력하고 이전 object와의 gap을 계산한다. 다음 표의 주소는 공통 prefix `0x56183b8ac0` 뒤 두 자리이며, **hexadecimal**이다. 예를 들어 `40`은 전체 주소 `0x56183b8ac040`을 뜻한다.

| Object | 시작 주소의 끝 두 자리 | Size | 이전 object 뒤 gap |
| --- | --- | ---: | ---: |
| `int i` | `40` | 4 | 첫 항목 |
| `char c` | `44` | 1 | 0 |
| `short s` | `46` | 2 | 1 |
| `long long ll` | `48` | 8 | 0 |
| `char c2` | `50` | 1 | 0 |
| `char c3` | `51` | 1 | 0 |
| `float f` | `54` | 4 | 2 |
| `char c4` | `58` | 1 | 0 |
| `double d` | `60` | 8 | 7 |
| `long double ld` | `70` | 16 | 8 |
| `long l` | `80` | 8 | 0 |

계산식은 `현재 주소 − 이전 주소 − 이전 size`다. `char c`는 `0x44`의 한 byte를 쓰므로 `short s`가 `0x46`에서 시작할 때 `0x45` 한 byte가 비어 있다. `char c3` 뒤 `float f`까지는 `0x54 - 0x51 - 1 = 2`다. `char c4` 뒤 `double d`까지는 `0x60 - 0x58 - 1 = 7`이고, 그 `double` 뒤 `long double`까지는 `0x70 - 0x60 - 8 = 8`이다. Hexadecimal 주소 차이를 decimal처럼 빼면 틀린다.

이것은 특정 실행에서 관찰한 global 배치다. 모든 compiler가 global을 선언 순서대로 배치한다는 규칙은 아니다. 반면 structure의 member 순서와 alignment를 이용한 다음 계산은 해당 target ABI의 구조적 규칙을 이용한다.

### Structure의 끝에도 padding이 필요한 이유

[Slides 35–37](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)의 예를 보자.

```c
struct S2 {
    double v;
    int i[2];
    char c;
} a[10];
```

x86-64 Linux 예에서 `v`는 offset 0부터 8 bytes, `i[0]`은 offset 8부터 4 bytes, `i[1]`은 offset 12부터 4 bytes, `c`는 offset 16의 1 byte를 쓴다. Member payload를 합하면 17 bytes다.

하지만 array의 모든 element 안에서 `double v`가 8-byte alignment를 만족해야 한다. 첫 element가 정렬되어 있어도 다음 element를 17 bytes 뒤에 놓으면 그 조건이 깨진다. 따라서 tail padding(끝부분의 빈 bytes) 7개를 더해 `sizeof(struct S2)`를 24로 만든다. 그림에서 확인해야 할 것은 `c` 뒤의 7-byte 공간과 array element가 0, 24, 48, 72, … byte 간격으로 반복되는 점이다. 그림의 `a+24` 같은 label은 **byte offset 설명**이며, C 식 `a + 24`의 typed pointer arithmetic과 혼동하면 안 된다.

Array stride(인접 element의 시작 주소 간격)는 element의 `sizeof`다. 따라서 `&a[1]`은 시작점보다 24 bytes, `&a[2]`는 48 bytes 뒤이며 전체 `a`는 240 bytes다. 일반적으로 각 member 앞에서 필요한 alignment를 맞추고, 마지막 크기도 member 중 가장 강한 alignment의 배수로 올려 다음 element를 준비한다.

이 사고방식은 structure layout을 묻는 [EX:sp_2025_1_midterm_q01 p.2]의 Q1(b)에도 적용된다. 먼저 target의 size·alignment를 고정한 뒤 member offset, tail padding, typed stride를 분리해서 계산한다. 위 `S2` 계산은 강의 예이며 해당 기출의 private structure나 답안을 재현한 것이 아니다.

### Union은 member들을 같은 시작점에 놓는다

Structure는 member를 순서대로 겹치지 않게 배치한다. Union(공용체)은 모든 member를 offset 0에서 시작시켜 같은 storage를 겹쳐 쓴다. [Slide 38](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)에서는 각 member를 나타내는 가로 구간의 시작선이 같은 위치에 맞춰져 있다. 구간을 옆으로 이어 붙이는 그림이 아니다.

Union의 alignment는 모든 member를 수용해야 하므로 가장 강한 member alignment를 만족해야 한다. 크기의 기본 출발점은 가장 큰 member의 size이며, 필요한 경우 union alignment에 맞는 tail padding까지 고려한다. Structure처럼 member size를 모두 합하면 안 된다. 예를 들어 이 target의 `int`와 `double`을 담는 단순한 union은 4+8 bytes가 아니라 8-byte storage와 8-byte alignment로 두 member를 수용할 수 있다. 이는 source의 일반 규칙을 적용한 설명용 계산이다.

같은 bytes를 쓴다는 말은 두 member의 독립적인 값이 동시에 보존된다는 뜻도 아니다. 한 member에 쓰면 다른 member가 겹쳐 보는 bytes가 달라진다. 여기서는 이 storage 관계까지만 다루며, 다른 member로 읽는 type-punning의 상세 허용 조건은 별도 주제다.

## Argument의 복사와 caller memory의 변경

### Scalar 값과 주소값을 복사하는 두 호출

Caller(호출하는 함수)와 callee(호출되는 함수)를 구분하면 “함수가 인자를 바꾼다”라는 말의 모호함이 줄어든다. [Slides 41–44](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)의 첫 함수는 scalar 값을 받는다.

```c
int foo(int a, int b)
{
    a = 2 * a;
    return a + b;
}
```

Caller에서 `x = 5`, `y = 6`으로 `foo(x, y)`를 호출하면 callee의 `a`는 5를 복사받아 10이 되고, 반환값은 16이다. Caller의 `x`는 여전히 5다. `a`와 `x`를 같은 storage로 취급하면 이 결과를 설명할 수 없다.

다음은 자료의 pointer를 받는 별도 함수다.

```c
int foo2(int *a, int b)
{
    *a = 2 * *a;
    return *a + b;
}
```

`foo2(&x, y)`에서는 `a`가 `x`의 주소값을 복사받는다. `*a`를 두 배로 하면 그 주소의 object, 즉 caller의 `x`가 10이 되고 반환값은 다시 16이다. 두 경우 모두 C는 값을 복사한다. 두 번째 값이 주소여서 caller storage에 접근할 수 있을 뿐이다. 자료의 “pass by reference”는 이 효과를 설명하는 표현으로 읽어야 하며 C에 별도의 reference parameter mechanism이 생긴다는 뜻은 아니다.

### Register와 memory operand가 드러내는 차이

Slide 44의 x86-64 assembly는 이 관계를 더 선명하게 보여 준다. 다음은 자료의 instruction을 spacing만 정리한 것이다.

```asm
mov (%rdi),%eax
add %eax,%eax
mov %eax,(%rdi)
add %esi,%eax
ret
```

이 호출에서 `%rdi`는 `x`의 주소를, `%esi`는 두 번째 argument 6을 가진다. 첫 instruction은 `(%rdi)`가 가리키는 memory의 5를 `%eax`로 읽는다. 다음 instruction이 10을 만들고, 세 번째가 그 10을 같은 caller memory에 저장한다. 네 번째가 6을 더해 반환값 16을 만든다.

`%rdi` 자체가 10으로 바뀌는 것은 아니다. 괄호 없는 register와 `(%rdi)`라는 memory operand의 차이가 “주소를 보관하는 값”과 “그 주소의 내용”의 차이다. 또한 parameter가 register로 전달되는 이 예는 모든 parameter가 반드시 stack에 있다고 외우면 안 되는 이유를 보여 준다.

### Array element와 command-line string

[Slides 45–46](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)에서는 `int x[10] = {0,1,2,3,4,5,6,7,8,9};`를 받은 함수가 `a[2] = 5;`를 수행한다. Array 전체가 별도로 복사되는 것이 아니라 element를 가리키는 pointer가 전달되어 caller의 `x[2]`가 2에서 5로 바뀐다. 이 target에서 `int`가 4 bytes이므로 필요한 byte offset은 `2 * 4 = 8`이다.

```asm
movl $0x5,0x8(%rdi)
ret
```

`0x8(%rdi)`는 base address보다 8 bytes 뒤에 쓰라는 뜻이다. Source의 C fragment는 `int` 반환형에 return이 없는 형태이므로 그대로 완성 함수의 모범으로 옮기기보다, 여기서는 이 store와 주소 계산만 읽는다.

[Slide 47](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)의 `main(int argc, char *argv[])`도 같은 연결을 이용한다. `argc`는 argument 수이고 `argv`는 string을 가리키는 `char *`들의 배열을 통해 전달된다. 자료의 정상적인 command-line 호출에서는 `argv[0]`이 program name이고 이후 element가 사용자가 준 argument다. 각 `argv[i]`는 문자를 담은 배열 그 자체를 value로 복사한 것이 아니라 string의 시작을 가리킨다.

자료의 반복문 `for (i = 0; i < argc; i++)`가 하는 일은 유효한 argument index를 차례로 방문하는 것이다. 정상 호출 예의 `argc >= 1`을 모든 가능한 C 환경의 무조건적인 보장으로 확대하지 않는다. 이 pointer와 storage 구분을 이해하면 [[courses/system_programming/units/dirtree|Dirtree의 option과 root 처리]]에서도 option 문자열, entry 이름의 사본, recursive 호출이 쓰는 memory의 소유권을 따로 생각할 수 있다.

## 핵심 정리

- 같은 virtual address만으로 공유를 판단하지 않는다.
- Size·alignment·precision은 다른 수량이다.
- Tail padding은 array의 다음 원소 alignment까지 유지한다.
- Pointer 기초가 흔들리면 [[courses/system_programming/units/objects-pointers|object와 pointer]]로 돌아간다.

## 확인·연습문제

### 개념 확인과 추론

#### 확인 Q01 · Virtual address와 공유

두 process의 같은 virtual address가 같은 object를 뜻하는가? Global counter와 shared counter 예, ASLR과 다음 강의 범위를 설명하라.

<details><summary>해설 보기</summary>

각 process의 address space가 별도이므로 같은 숫자만으로 공유가 성립하지 않는다. 독립 global counter는 각자0, 1로 진행하지만 실제 공유한 counter 예는 공동0..7로 진행한다. ASLR은 배치를 변화시켜 예측을 어렵게 하는 완화책이지 완전한 보안이 아니다. 9월23일13:08·42:29–43:27은 현재 recap과 이후 논의를 구별하며 page-table/TLB 계산을 이미 배웠다고 만들지 않는다.

**채점·확인:** 주소 숫자/공유 object·두 counter·ASLR 한계를 구별한다.

</details>

#### 확인 Q02 · Section과 보호

Text·rodata·data·bss·heap·stack을 분류하라. Writable DRAM인데 read-only인 이유, bss와 uninitialized auto, malloc/brk, literal 변경의 한계는?

<details><summary>해설 보기</summary>

Text는 instruction, rodata는 literal·읽기 전용 data, data는 초기화된 writable static storage, bss는 zero-initialized static storage다. Bss가 executable에 모든 zero bytes로 저장된다는 뜻은 아니며 uninitialized automatic object는 자동 zero가 아니다. Heap은 동적 allocation으로 brk뿐 아니라 mapping도 쓰며 stack은 이 target에서 아래 주소로 자라지만 인자는 register에도 있을 수 있다. DRAM 자체의 쓰기 능력과 CPU·OS가 적용하는 논리적 protection은 다르다. Literal/const 변경은 C에서 허용되지 않으며 실제 crash 유무가 합법성을 결정하지 않는다. Page translation 구현은 여기서 설명하지 않는다.

**채점·확인:** 여섯 영역·static/auto·물리/논리 protection을 확인한다.

</details>

#### 확인 Q03 · Size와 alignment 표

Size와 K-byte alignment를 구별하고 x86-64 Linux와 IA32 Linux의 주요 type size/alignment를 비교하라. Long double과 unaligned access의 주의점은?

<details><summary>해설 보기</summary>

Alignment K는 시작 주소가 K의 배수라는 제약이다.

|Type|x86-64 size/align|IA32 size/align|
|---|---|---|
|char|1/1|1/1|
|short|2/2|2/2|
|int, float|4/4|4/4|
|long, pointer|8/8|4/4|
|long long, double|8/8|8/4|
|long double|16/16|12/4|

Long double의 storage16은128-bit precision이 아니며 자료의 extended 값은80-bit 표현과 구별한다. Unaligned access는 boundary를 넘어 추가 처리가 필요할 수 있지만 모든 target에서 실패하거나 atomicity가 보장된다고 하지 않는다.

**채점·확인:** Size/align 두 열과 IA32 예외·precision 한계를 확인한다.

</details>

#### 확인 Q04 · Alignment를 관찰하는 macro

INFO(double)가 char dummy 뒤 data를 둔 struct를 만들 때 SIZE, #t, OFS는 무엇을 계산하는가? x86-64와 IA32의 offset·padding을 구하라.

<details><summary>해설 보기</summary>

SIZE는 sizeof(type), #t는 macro 인자 이름의 stringification, OFS는 data 주소−struct 시작 주소다. X86-64에서 dummy1 뒤 data offset 8이므로 padding7, IA32 Linux에서는 offset 4·padding3이고 double size는 여전히8이다. Offset·size를 섞으면 alignment를 잘못 읽는다. 원문의 unsigned long 주소 cast와 예제 main 표기는 target 의존 측정 code의 한계이며 여기서 실행한 결과가 아니다.

**채점·확인:** 8/7과4/3·double8·stringification을 확인한다.

</details>

#### 확인 Q05 · Padding과 array stride

Global 주소 tail 44(char1)→46(short), 51(char1)→54(float), 58(char1)→60(double), 60(double8)→70(long double)의 gap을 hex로 구하라. S2={double v; int i[2]; char c; }의 offset·tail padding과 S2 원소 10개인 array의 크기는?

<details><summary>해설 보기</summary>

Gap=현재 주소−이전 주소−이전 size이므로1, 2, 7, 8 bytes다. Global의 이 배치 순서가 C의 일반 보장은 아니다. S2는 v offset 0, i[0]8, i[1]12, c16이고 사용17 bytes 뒤 tail padding7을 더해 size 24, alignment 8이다. Array10개는240 bytes, index 1은byte 24, index 2는byte 48이다. Tail padding이 다음 원소의 double alignment도 지킨다. 그림의 a+24는 byte 위치이지 typed pointer에24를 더하라는 뜻이 아니다.

**채점·확인:** 네 gap·member offsets·tail 7·stride24를 확인한다.

</details>

#### 확인 Q06 · Union의 겹침

int와 double을 담은 union과 struct의 배치 원리는 어떻게 다른가? Union size·alignment와 동시에 보유 가능한 값의 의미를 설명하라.

<details><summary>해설 보기</summary>

Struct는 member가 순서대로 비중첩하게 놓이고 padding을 포함한다. Union은 모든 member offset 0에 겹치며 최대 member 크기를 최대 alignment의 배수로 올린 storage를 쓴다. 이 target의 int/double union은size 8, alignment 8이지4+8=12가 아니다. 같은 storage라 두 값이 독립적으로 동시에 유지되는 구조가 아니며 임의 type-punning 기법을 새로 정당화하지 않는다.

**채점·확인:** Offset 0·max+rounding·동시 독립 값 불가를 확인한다.

</details>

#### 확인 Q07 · 값 복사와 주소를 통한 변경

x=5, y=6에서 scalar foo와 pointer foo2의 x·return을 비교하라. mov/add/store assembly, a[2]=5의 byte offset, argc/argv의 parameter type도 설명하라.

<details><summary>해설 보기</summary>

Scalar foo는 local a만10으로 만들고16을 반환해 caller x=5다. `foo2`는 복사된 &x로 x를10으로 바꾸고16을 반환한다. 둘 다 C의 value passing이다. Assembly는 (%rdi)에서5 load→eax 두 배10→(%rdi)에 store→esi의6을 더해16 return이며 rdi 자체를10으로 바꾸지 않는다. 4-byte int의 a[2]는byte 8이라 `movl $0x5,0x8(%rdi)`가 caller 원소를 바꾼다. 원문 int 함수의 return 누락은 임의 결과값으로 보충하지 않는다. Argc는 인자 수, parameter `char *argv[]`는 char**로 조정되며 각 원소는 string pointer다. 보통 argv[0]는 프로그램 이름이고 i<argc로 순회하지만 모든 C 환경의 argc>=1을 보장하지 않는다.

**채점·확인:** x5/x10·return 16·rdi 주소 유지·offset 8·argv 조정을 확인한다.

</details>

### 응용 연습

#### 연습 P01 · Member 순서와 전체 크기

**새로 만든 합성 연습.** X86-64 Linux에서 struct A {char tag; double value; char ready; }; struct B {double value; char tag; char ready; }; 의 offsets, size, 두 원소 array 크기를 구하라. 두 char를 union으로 바꾸면 두 flag를 독립 보관할 수 있는가?

[EX:sp_2025_1_midterm_q01 p.2] Q1(b)의 alignment·stride 계산을 두 배치 비교와 설계 판단으로 옮긴 새 연습이다. 선행: Q03·Q05·Q06. 원문의 구조체·주소 차 식과 crash 문항은 재현하지 않는다. [[exam_questions/sp_2025_1_midterm_q01|허용된 관련 문항 미리보기]]

<details><summary>해설 보기</summary>

A는 offsets 0, 8, 16이며 마지막 byte 뒤17을8의 배수24로 올린다. B는0, 8, 9로10을16으로 올린다. Array2는48과32 bytes다. 순서 변경은 internal/tail padding을 바꾸지만 alignment 8은 같다. Union의 두 char는 offset 0을 공유하므로 두 독립 flag의 대체가 아니다.

**채점·확인:** Offsets·tail rounding·48/32·union 설계 한계를 확인한다.

</details>

### 복습 계획

Q01–Q02로 address space와 영역을 그린 뒤 Q03–Q06에서 size/align/offset을 다른 열에 적는다. P01을 가리고 계산하고 Q07에서 어떤 object가 실제 바뀌는지 확인한다.

## 출처

### 날짜별 강의 노트

- [[courses/system_programming/lectures/2026-09-23-lecture-06|2026-09-23 강의 노트]]

### 수업자료와 강의 구간

- [Variable and Memory Recap slides 5–7](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)
- [Slide 11](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)
- [Slides 23–29](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)
- [Slide 28](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)
- [Slide 32](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)
- [Slides 35–37](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)
- [Slide 38](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)
- [Slides 41–44](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)
- [Slides 45–46](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)
- [Slide 47](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)
- [[courses/system_programming/transcripts/2026-09-23|9월 23일 STT 13:08]]
- [[courses/system_programming/transcripts/2026-09-23|9월 23일 STT 21:47]]
- [[courses/system_programming/transcripts/2026-09-23|9월 23일 STT 17:04–18:01]]
- [[courses/system_programming/transcripts/2026-09-23|9월 23일 STT 50:07]]

연결된 공개 자료는 slide deck이며, 이 자료들의 PDF 페이지 보기 링크는 제공되지 않았다. 녹취 시각은 일반 텍스트로 표시한다.

### 자료 범위와 한계

- 9월 23일 memory recap 범위다. 이후 page table·TLB·translation 계산을 이미 확인된 진도로 주장하지 않는다.
- 자료의 주소·global 배치·assembly·ABI 수치는 예시 target에 한정하며 현 PC에서 실행한 관측이 아니다.
- Assembly/C 예의 누락 return과 unsigned long cast 등의 이식성 한계를 유지한다.
- 제공된 exam crash 답은 C 유효성의 기준이 아니다. Q1(b)의 제한된 alignment reasoning만 사용한다.


---

[[courses/system_programming/units/io-streams|← 이전: Unix I/O·열린 파일 상태·stdio buffering]] · [[courses/system_programming/units/index|단원 목차]] · [[courses/system_programming/units/dirtree|다음: Dirtree의 순회·filter·출력 계약과 설계 →]]
