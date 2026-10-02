---
title: "C object·type·주소와 pointer"
description: "Type, pointer 대입, array 변환, 동적 storage의 크기와 수명을 확인한다."
course: "system_programming"
unit_id: "objects-pointers"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["00.Introduction.pptx", "02.CPointers_24a7628c.pptx", "06.MM.Variable.and.Memory.Recap.pptx", "08.MM.Dynamic.Memory.Allocation.I.pptx", "09.MM.Dynamic.Memory.Allocation.II.pptx"]
private_source_assets: []
source_lectures: ["courses/system_programming/lectures/2026-09-02-lecture-01", "courses/system_programming/lectures/2026-09-07-lecture-02", "courses/system_programming/lectures/2026-09-09-lecture-03", "courses/system_programming/lectures/2026-09-23-lecture-06"]
---

Pointer 식을 읽을 때 주소를 담은 object와 그 주소가 가리키는 object를 따로 그려 보자. Type·범위·lifetime을 먼저 정하면 크기 계산과 복잡한 대입을 같은 방법으로 풀 수 있다.

## Object, type, address의 세 가지 질문

프로그램이 값을 바꾸려면 저장할 공간과 그 값을 해석하는 규칙이 필요하다. Object(객체)는 값을 보유하는 저장공간이고, variable은 여기에 붙인 이름으로 이해할 수 있다. Type(자료형)은 해석과 필요한 크기를 결정한다. [C 프로그램의 상태](systems-c-build.md)에서 한 단계 내려오면 ‘무슨 값인가’, ‘어디에 있는가’, ‘어떤 type으로 접근하는가’를 따로 물어야 한다.

이 단원의 수치 예는 자료의 x86-64 Linux target을 따른다. `char`, `short`, `int`, `long`은 각각 1, 2, 4, 8 bytes, `float`, `double`은 4, 8 bytes, object pointer는 8 bytes다. 다른 ABI까지 고정하는 C 규칙이 아니다. Floating-point(부동소수점)는 sign, exponent, significand로 수를 표현하며 유한한 bit 수 때문에 많은 실수를 반올림한다. `double`이 8 bytes라는 사실은 모든 실수를 정확히 표현한다는 뜻이 아니다. `long double`의 16-byte storage도 128-bit 유효 정밀도를 뜻하지 않는다. [[courses/system_programming/lectures/2026-09-02-lecture-01|2026-09-02 type·array 강의]]와 [[courses/system_programming/transcripts/2026-09-02|같은 날짜 STT]] 01:15:55는 이 표현의 차이를 도입하며 상세 IEEE 754 encoding까지 다루지는 않는다.

### Pointer가 저장하는 값과 pointer 자신의 주소

Byte-addressed memory에서는 byte마다 주소가 있고 여러 byte object의 주소는 시작 byte를 가리킨다. 아래 숫자는 주소 관계를 위한 자료의 추상 예다. 실제 8-byte pointer들이 이 간격으로 배치된다는 뜻은 아니다.

| Object | 자신의 주소 | 저장한 값 | Type |
|---|---:|---:|---|
| `a` | 16 | 5 | `int` |
| `ap` | 28 | 16, 즉 `&a` | `int *` |
| `app` | 4 | 28, 즉 `&ap` | `int **` |

`*app`는 `ap`를 지정하므로 그 값은 16이고, `**app`는 `a`를 지정하므로 값은 5다. 선언의 `*`는 pointer type을 만들고 expression의 `*`는 dereference(간접 참조), `&`는 주소 연산이다. `*app = ...`는 pointer object `ap`를 바꿀 수 있지만 `**app = 9`는 `a`에 9를 쓴다.

[[courses/system_programming/transcripts/2026-09-07|2026-09-07 STT]] 54:41의 주소 출력 설명을 유효하게 초기화한 object에 적용하면 다음과 같다.

```c
int a = 5;
int *ap = &a;
printf("%p\n", (void *)ap);
printf("%p\n", (void *)&ap);
printf("%d\n", *ap);
```

첫 두 줄은 각각 대상 주소와 pointer object 자신의 주소, 마지막 줄은 5를 출력한다. Header는 `stdio.h`가 필요하다. `%p`에 `void *`를 맞추는 것은 이식성을 위한 설명상의 한정이다. 실제 주소값과 출력 모양은 고정되지 않는다. 55:31의 미초기화 pointer 출력 제안을 안전한 관찰 방법으로 채택해서는 안 된다. M004의 `x = 102`, 주소 2인 그림과 불확실한 숫자 발화도 구분한다.

`sizeof(ap)`는 8, `sizeof(*ap)`는 4다. `void *k`의 pointer 저장공간은 8이지만 `void`는 완전한 object type이 아니므로 표준 C의 `sizeof(*k)`로 대상 크기를 얻을 수 없다. Cast는 해석할 type을 바꿀 뿐 유효한 storage, lifetime, alignment를 새로 만들지 않는다.

## Array와 string이 실제로 보유하는 공간

Array(배열)는 같은 type의 object가 연속된 저장공간이다. `T a[N]`의 크기는 `N * sizeof(T)`다. 이 target에서 `char c[10]`은 10 bytes, `double pi[5][2]`는 `5 * 2 * 8 = 80` bytes다. `int a[10]`은 40-byte array object이고 `int *p = a`의 `p`는 8-byte pointer object다.

많은 expression에서 `a`는 첫 원소 주소로 변환된다. 이때 `a + i`는 `&a[i]`, `*(a + i)`는 `a[i]`에 해당한다. 그러나 `sizeof(a)`는 전체 array를 측정하고 `&a`는 전체 array를 가리키는 pointer다. Array 이름에 다른 주소를 대입하거나 `a++`를 수행할 수 없으므로 순회용 pointer는 따로 둔다. `sizeof` 문제에서는 먼저 operand의 type을 결정한다. [EX:sp_2025_1_midterm_q01 p.2] Q1(a)의 요구도 이 구분이다. Non-VLA type의 `sizeof(*p)`는 실제 pointee를 읽는 연산이 아니며, 이것이 미초기화 `p`의 실제 dereference를 허용하지는 않는다. [[exam_questions/sp_2025_1_midterm_q01|기존 공개 question-only preview]]에서도 같은 type 판별 관점을 적용할 수 있다.

### NUL, length, capacity

C string은 NUL byte로 끝나는 character sequence다. 다음 두 선언은 다른 storage를 만든다.

```c
char *p = "hello world\n";
char s[20] = "SNU CSE00800";
```

`p`는 literal의 첫 문자 주소를 저장한다. `s`는 문자들을 담을 20-byte array 자체다. `SNU` 3자, space 1자, `CSE` 3자, `00800` 5자로 length는 12이며 첫 NUL은 `s[12]`다. 부분 초기화된 나머지 `s[12]`부터 `s[19]`까지도 0이다. Length에는 NUL을 세지 않지만 storage에는 NUL이 필요하다.

`s[0]`은 수정할 수 있지만 `p[0]`으로 string literal을 수정하면 undefined behavior(정의되지 않은 동작)다. 모든 pointer 대상이 read-only인 것은 아니며, literal 수정이 항상 특정 crash를 낸다는 보장도 없다. `struct student { int id; char *name; };`은 서로 다른 type을 묶는다. `name`은 문자들을 내부에 보유하는 array가 아니라 주소 member이므로 string의 lifetime을 별도로 관리해야 한다.

### Function designator와 struct pointer

`void foo(void)`의 이름 `foo`는 일반적인 값 사용 문맥에서 function pointer로 변환된다. `void (*fp)(void) = foo;`와 `void (*fp)(void) = &foo;`는 같은 함수를 지정한다. 함수 자체가 pointer variable이라는 뜻도, `sizeof(foo)`로 code 길이를 구한다는 뜻도 아니다. Function pointer를 임의로 `void *`로 바꾸어 `%p`로 출력하는 방법이 모든 C 구현에서 이식 가능한 것도 아니다.

[[courses/system_programming/transcripts/2026-09-23|2026-09-23 STT]] 05:36–06:37의 불완전한 decay 표현은 선언과 구분해 읽는다. 같은 자료의 `shared`는 `struct __shared *`다. `sizeof(shared)`는 8이지만 `sizeof(*shared)`는 `sem_t m`, `int shared_int`, padding을 포함하는 struct 크기다. `sem_t` 크기가 주어지지 않았으므로 총 bytes를 임의로 정할 수 없다. 유효한 `shared`에 대해 `&shared->shared_int`는 member 주소이고 `&shared`는 pointer object 주소다.

## 주소 복사와 값 복사 추적하기

`p = &i`, `q = &j`라면 `q = p`는 `q`의 대상을 `i`로 바꾼다. 반면 `*q = *p`는 현재 대상 `j`에 `i`의 값을 복사한다. [[courses/system_programming/lectures/2026-09-07-lecture-02|2026-09-07 pointer 강의]]의 이 구분을 작은 상태 표로 확인할 수 있다.

```c
int i = 1, j = 7;
int *p = &i, *q = &j;
*q = *p;
q = p;
*p = 1;
*q = 2;
```

첫 대입 뒤 `j = 1`이며 두 pointer의 대상은 그대로다. 다음 `q = p` 뒤 두 pointer가 `i`를 가리킨다. 마지막 두 대입은 같은 object를 바꾸므로 최종 `i = 2`, `j = 1`이다. 이 코드는 source의 주소/값 구분을 정돈한 예다.

`scanf`의 `%d`는 값을 저장할 유효한 `int` object의 주소를 요구한다. 위의 `i`에는 `&i` 또는 `p`를 전달한다. `&p`는 `int **`이므로 다른 계약이다. `int a[10]`은 원소 공간을 확보하지만 `int *a`는 주소를 저장할 공간만 선언한다. 초기화하지 않은 pointer를 dereference하는 오류가 우연히 crash하지 않아도 올바른 C가 되지는 않는다.

### Pointer-to-pointer는 어느 pointer를 바꾸는가

[[courses/system_programming/lectures/2026-09-09-lecture-03|2026-09-09 다중 pointer 강의]]와 M006 slides 31–35의 sequence는 한 단계 더 간다.

```c
int i, j;
int *p = &i, *q = &j;
int **k = &p;
*p = 1;
*q = 2;
*k = q;
k = &q;
*k = &i;
*p = 3;
**k = 4;
```

`*k = q`는 `p`에 `q`의 값을 넣어 `p → j`를 만든다. `k = &q` 뒤 `*k = &i`는 `q → i`를 만든다. 그러므로 `*p = 3`은 `j`, `**k = 4`는 `i`를 바꾼다. 최종 관계는 `p → j`, `q → i`, `k → q`, 값은 `i = 4`, `j = 3`이다. 별표 수만 세지 말고 statement마다 대상 object를 갱신해야 한다. 같은 추적 능력을 요구하는 [EX:sp_2025_2_midterm_q01 p.3] Q1(b)에서도 pointer 이동과 원소 수정을 별도 상태로 기록하는 것이 핵심이다. 문제의 private 출력값을 외우는 것보다 각 대입의 왼쪽이 어느 object인지 확인하는 방법이 전이된다.

## Pointer arithmetic과 lifetime

Typed pointer의 이동 단위는 byte가 아니라 원소다. 허용되는 범위 안에서 `p + k`의 byte displacement는 `k * sizeof(*p)`다. 이미 scaling이 적용되므로 `int *p`의 `p += sizeof(int)`는 다음 int가 아니라, 여기서는 네 int를 건너뛴다.

| 각각 새로 시작하는 source 예 | 결과 |
|---|---|
| `p = &a[2]; q = p + 3; p += 6;` | `q = &a[5]`, `p = &a[8]` |
| `p = &a[8]; q = p - 3; p -= 6;` | `q = &a[5]`, `p = &a[2]` |
| `p = &a[5]; q = &a[1];` | `p-q = 4`, `q-p = -4`, `p<=q`는 0, `p>=q`는 1 |

감산·순서 비교의 이 예는 같은 array의 유효한 원소들을 전제로 한다. 앞 행의 마지막 상태를 다음 행에 이어 붙이면 안 된다. One-past pointer는 경계로 만들 수 있지만 추가 원소처럼 dereference할 수 없다. Equality와 relational ordering의 규칙을 모두 같은 문장으로 일반화하지 않는다.

주소 반환에서도 숫자보다 lifetime이 중요하다. `max(int *a, int *b)`가 caller의 살아 있는 object를 가리키는 `a` 또는 `b`를 반환하면 그 lifetime 동안 사용할 수 있다. `max(int a, int b)`가 자기 parameter의 `&a`나 `&b`를 반환하면 함수 종료 뒤 object가 사라진다. 이전 bytes가 남아 있어도 유효한 접근이 아니다. 자료의 `find_middle(a, n)`이 `&a[n/2]`를 반환하는 경우는 `n > 0`, 충분한 array 범위, caller array의 생존이 필요하다.

### Array parameter도 값으로 전달된다

Parameter의 `int a[]`는 `int *a`로 조정된다. 주소값 하나를 전달하는 비용과 N개 원소를 조사하는 알고리즘 비용은 다르다. `find_largest`가 모든 원소를 검사하면 작업은 N에 따라 늘지만 호출 때 array 전체를 복사하는 것은 아니다. `find_largest(&b[5], 10)`의 local `a[0]`은 `b[5]`, `a[9]`는 `b[14]`이므로 그 열 원소가 존재해야 한다. 첫 원소를 초기 최대값으로 쓰면 `n > 0`도 필요하다.

C는 pointer parameter도 값으로 전달한다. `a[i]` 수정은 caller 원소에 영향을 주지만 local pointer `a`를 다른 주소로 바꿔도 caller의 pointer variable은 바뀌지 않는다. `const int a[]`는 이 접근 경로를 통한 수정을 제한하며 다른 alias의 변경까지 없애지는 않는다. Array member를 가진 struct 전체를 값으로 넘기면 그 array를 포함한 struct 값이 복사되는 별도 경우다.

## Declarator에서 크기와 접근 단위 읽기

Identifier에서 출발하여 grouping 괄호, `[]`, function `()`, `*`의 결합을 따라간다. `[]`와 function `()`는 `*`보다 먼저 결합한다.

| 선언 | 의미 |
|---|---|
| `int *p[10]` | `int *` 열 개의 array |
| `int (*p)[10]` | `int[10]`을 가리키는 pointer |
| `int *(*p)[10]` | `int *[10]`을 가리키는 pointer |
| `int (*pf)(void)` | 인자 없이 `int`를 반환하는 function pointer |
| `int *pf(void)` | 인자 없이 `int *`를 반환하는 function |
| `int (*pf[10])(void)` | 위 function pointer 열 개의 array |
| `int pf[](void)` | 허용되지 않는 function 자체의 array |

`int (*p)[10]`의 `p + 1`은 target에서 40 bytes를 이동한다. Pointer array가 expression에서 변환되었을 때의 원소 단위는 pointer 하나이므로 8 bytes다. M006 slides 38–39의 크기 비교도 먼저 type을 읽으면 계산된다.

| 선언 | `sizeof(A)` | `sizeof(*A)` | `sizeof(**A)` |
|---|---:|---:|---:|
| `int A1[3]` | 12 | 4 | 잘못된 expression |
| `int *A2[3]` | 24 | 8 | 4 |
| `int (*A3)[3]` | 8 | 12 | 4 |

여기서 `A`는 각 행의 identifier를 뜻한다. 자료 slide 38의 `**A3: A3[0]` 표기는 type과 맞지 않아 `**A3`는 `A3[0][0]`이라고 명시적으로 바로잡는다. `A = {1,2,3}`, `B = {4,5,6}`, `A3 = &A`, `B3 = &B`인 source 예에서 `*A3 = *B3`는 array 대입이어서 불가하다. `**A3 = **B3`는 첫 int만 복사하여 `A = {4,2,3}`을 만든다. `pA = *A3`는 첫 원소 주소를 저장한다. 표의 non-VLA `sizeof` 계산과 실제 미초기화 pointer 접근의 안전성을 혼동하지 않는다.

## Dynamic allocation의 크기와 수명

[[courses/system_programming/lectures/2026-09-23-lecture-06|2026-09-23 dynamic array 설명]]의 [system_programming:M016 slide 17](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)은 pointer `A` 자신의 위치 `0xffffc1a4`와 저장한 heap 시작 주소 `0x56550004`를 분리한다. 그림에서 확인할 것은 pointer box와 1024개 원소 영역이 다른 storage라는 점이다. Four-byte int 1024개는 `4096 = 0x1000` bytes다. 따라서 `A[1]`은 `0x56550008`, `A[2]`는 `0x5655000c`, 마지막 `A[1023]`은 `base + 4092 = 0x56551000`이다. 이 계산은 slide에 근거하며 STT 24:43의 불명확한 수치를 복원한 것이 아니다.

`char buf[512] = {'A','B','C'};`는 나머지도 0으로 초기화한다. 그러나 `malloc` 뒤 첫 세 byte만 쓰면 나머지는 0으로 보장되지 않는다. `calloc`은 zero-initialization을 제공한다. 할당 실패 확인, 사용 후 `free`, 해제 뒤 접근 금지는 각각 별개 책임이다. 미초기화 memory는 신뢰할 수 있는 난수원도 아니다.

I/O 길이에도 같은 구분이 적용된다. 위 array의 `sizeof(buf)`는 512이지만 heap buffer를 가리키는 pointer의 `sizeof(buf)`는 8이다. Heap buffer는 확보한 길이를 별도로 보유하고 전달해야 한다. 한 `char`에 읽을 때는 그 값이 아니라 `&buf`를 목적지로 전달한다. OS가 process 종료 시 자원을 회수한다는 사실은 오래 실행되는 프로그램의 leak을 정당화하지 않는다.

### 크기 변경과 서로 독립적인 allocation

RM002 slides 5–27과 RM003의 오류 예는 선택적 자료 기반 복습이다. 이 전체 allocation deck이 9월 28일에 강의되었다는 뜻은 아니다. `malloc`/`free`는 libc의 요청이며 libc는 `brk`/`sbrk` 또는 `mmap` 등을 통해 OS와 상호작용할 수 있다. 모든 allocation이 하나의 연속된 `brk` heap에 놓이는 것은 아니다. 자료는 `alloca`와 `sbrk(0)`도 소개하지만 여기서는 대안의 존재와 역할만 구분한다.

`realloc`의 양수 크기 요청이 실패하면 NULL을 반환하고 기존 allocation은 유지된다. 결과를 기존 pointer에 바로 덮어쓰는 source 예는 실패 때 원래 block을 가리킬 수단을 잃을 수 있다. 성공 뒤에는 반환한 pointer를 사용하고 old base나 내부 alias를 재사용하지 않는다. 이동 여부와 무관하게 이전 allocation을 계속 유효하다고 추정해서는 안 된다. 기존 내용은 새 크기에 들어가는 범위에서 유지되고 확장 부분은 자동 초기화되지 않는다. Zero-size 요청은 표준·구현 조건을 생략한 보편 규칙으로 다루지 않는다.

Source의 256개 int를 512개로 늘리는 예는 1024 → 2048 bytes다. 처음 `0..255`를 저장한 뒤 새 원소 `256..511`도 별도로 초기화한다. 이것과 RM002 slides 15–25의 **독립 allocation 수명** 예는 다른 sequence다. 모든 요청 성공을 가정하면 다음과 같다.

| 호출까지 진행한 상태 | 살아 있는 allocation |
|---|---|
| `p1 = malloc(3); p2 = malloc(1); p3 = malloc(4);` | `p1`, `p2`, `p3` |
| `free(p2);` | `p1`, `p3` |
| `p4 = malloc(6);` | `p1`, `p3`, `p4` |
| `free(p3);` | `p1`, `p4` |
| `p5 = malloc(2);` | `p1`, `p4`, `p5` |
| `free(p1); free(p4); free(p5);` | 없음 |

할당 순서와 해제 순서는 같을 필요가 없다. 해제된 공간은 재사용될 수 있지만 `p5`가 이전 `p2`와 같은 주소를 받는다는 API 보장은 없다. 이 표는 호출 순서의 분석이며 원본 그림의 세부 위치를 주장하지 않는다.

### Memory error를 원인으로 분류하기

RM003 slides 33–45는 pointer 지식을 오류 진단으로 연결한다. 초기화하지 않은 `y[i]`에 `+=`를 하면 0부터 누적하는 계산이 아니다. `int **p`의 N개 pointer slot에 `N * sizeof(int)`만 할당하면 pointer와 int 크기가 다른 target에서 부족하다. `char s[8]`에 제한 없이 아홉 문자를 읽으면 NUL까지 포함하여 넘친다. `*size--`는 `(*size)--`가 아니라 `*(size--)`로 결합하여 pointed-to count 대신 pointer를 이동시킨다.

Local 주소 반환, use-after-free, double free, 마지막 소유 pointer를 잃는 leak은 서로 다른 수명 오류다. 연결 구조의 head만 `free`해도 별도로 할당한 next node가 자동 해제되지 않는다. Debugger, `mtrace`/`muntrace`, Valgrind는 관찰 도구이며 도구 이름만으로 오류가 검증된 것은 아니다. Allocator의 list·coalescing·binning 구현은 후속 범위다. 여기서 다룬 object 크기와 lifetime은 [memory layout과 호출](memory-layout.md)을 이해하는 기반이 된다.

## 핵심 정리

- `sizeof`의 대상은 type이며 pointer가 확보 영역의 길이를 기억하지 않는다.
- 주소 복사, pointee 값 복사, pointer-to-pointer를 통한 pointer 변경을 구분한다.
- Array는 object이고 많은 식에서 첫 원소 주소로 변환될 뿐 pointer variable과 같지 않다.
- 유효한 주소 계산에는 원소 단위, array 범위, 살아 있는 object가 모두 필요하다.
- Allocation·초기화·크기 변경·해제는 각각 다른 책임이다.

## 확인·연습문제

### 개념 확인과 설명

#### 확인 Q01 · 크기와 정밀도

본문 target의 `char/short/int/long/float/double` 크기를 쓰고 type·object·variable을 구분하라. 8-byte `double`과 16-byte `long double`이 모든 실수 또는 128-bit 정밀도를 보장하는가?

<details><summary>해설 보기</summary>

크기는 1/2/4/8/4/8 bytes다. Object는 저장공간, variable은 이름, type은 해석과 크기 규칙이다. Floating-point는 sign·exponent·significand를 쓰며 표현 가능한 상태가 유한하여 반올림한다. Storage 크기와 유효 정밀도는 다르다. 이 크기는 x86-64 Linux 자료 조건이며 모든 ABI의 C 규칙이 아니다.

**채점·점검 기준:** 여섯 크기와 storage/precision 구별, target 한정을 확인한다.

</details>

#### 확인 Q02 · Pointer box와 대상

추상 도식에서 `a=5`는 주소 16, `ap=&a`는 주소 28, `app=&ap`는 주소 4에 있다. `ap/&ap/*app/**app` 및 `*app=...`·`**app=9`의 대상을 설명하라. 주소·int 출력 형식과 `sizeof(ap)`, `sizeof(*ap)`, `void *k`의 `sizeof(*k)`는?

<details><summary>해설 보기</summary>

값은 16/28/16/5다. `*app` 대입은 ap의 주소값, `**app` 대입은 현재 대상 int를 바꾼다. 주소는 `(void *)ap`, `(void *)&ap`를 `%p`, 대상 int는 `*ap`를 `%d`로 출력한다. 크기는 8/4이고 void는 완전한 object type이 아니므로 표준 C의 `sizeof(*k)`는 불가하다. Cast는 유효 storage·alignment·lifetime을 만들지 않으며 미초기화 pointer 출력도 안전한 관찰이 아니다. 도식 간격은 실제 pointer 배치를 뜻하지 않는다.

**채점·점검 기준:** 네 값, 두 대입 대상, 출력 인자 type, void 한정을 확인한다.

</details>

#### 확인 Q03 · Array의 크기와 변환

`int a[10]; int *p=a; double pi[5][2];`에서 `sizeof(a/p/pi)`와 `a+2`의 byte 이동을 구하라. `a++`, `&a`, `sizeof(a)`는 일반 decay와 어떻게 다른가?

<details><summary>해설 보기</summary>

40/8/80 bytes이며 `a+2`는 8 bytes 뒤 세 번째 int다. Typed pointer 산술에는 scaling이 이미 포함된다. `a`는 많은 식에서 첫 원소 주소로 변환되지만 `sizeof(a)`는 전체 array, `&a`는 전체 array를 가리킨다. Array 이름을 갱신하는 `a++`는 불가하며 별도 pointer를 사용한다. Pointer 값에 원소 개수 10이 함께 저장되는 것은 아니다.

**채점·점검 기준:** 40/8/80, 8-byte 이동, 두 decay 예외를 설명한다.

</details>

#### 확인 Q04 · Function과 struct pointer

`void foo(void)`에서 `foo`와 `&foo`를 function pointer에 넣는 차이는? `sizeof(foo)`는 code 길이인가? `struct __shared {sem_t m; int shared_int;} *shared;`의 두 sizeof와 두 주소 `&shared`, `&shared->shared_int`를 구별하라.

<details><summary>해설 보기</summary>

두 초기화는 같은 function을 지정하지만 function 자체가 pointer variable인 것은 아니다. 표준 C에서는 function type에 `sizeof(foo)`를 적용할 수 없어 code 길이를 구할 수 없고 function pointer의 `%p`/`void *` 출력도 일반 이식성 규칙이 아니다. `sizeof(shared)=8`, `sizeof(*shared)`는 member와 padding을 포함하며 `sem_t` 크기 없이는 수치를 모른다. 첫 주소는 pointer object, 둘째는 유효 struct의 int member 주소다.

**채점·점검 기준:** Function 변환과 struct 크기를 분리하고 모르는 크기를 발명하지 않는다.

</details>

#### 확인 Q05 · 문자열 길이·공간·수명

`char *p="abc"; char s[20]="SNU CSE00800";`의 storage를 비교하고 s의 length·첫 NUL·capacity·남은 초기값을 구하라. `p[0]`·`s[0]` 수정과 `struct student`의 `char *name` member 수명은?

<details><summary>해설 보기</summary>

p는 별도 literal의 주소만 저장한다. s는 20-byte writable array이며 3+1+3+5=12 characters, 첫 NUL은 index 12, index 12–19는 모두 0이다. Literal은 3 characters+NUL의 별도 공간이다. `s[0]` 수정은 가능하지만 literal을 바꾸는 `p[0]` 수정은 undefined behavior이며 특정 crash 보장은 없다. `name`도 문자 사본이 아니라 주소이므로 대상 string의 수명을 따로 보장해야 한다.

**채점·점검 기준:** 12/12/20과 pointer/literal/array storage를 모두 구분한다.

</details>

#### 확인 Q06 · 주소 대입과 값 대입

`i=1,j=7,p=&i,q=&j`에서 `*q=*p; q=p; *p=1; *q=2;`를 추적하라. `%d` scanf에 `&i`, `p`, `&p` 중 무엇이 맞는가? `int *a` 선언만으로 입력 공간이 생기는가?

<details><summary>해설 보기</summary>

첫 문장에서 j=1, 다음에 q가 i를 가리키며 마지막 두 문장이 i를 차례로 1,2로 바꾼다. 최종 i=2,j=1,p와 q는 i를 가리킨다. `&i`와 p는 유효한 `int *`, `&p`는 `int **`여서 틀리다. Pointer 선언은 pointer object만 만들며 유효 int 대상을 자동 확보하지 않는다.

**채점·점검 기준:** 값 2/1, alias 관계, scanf type을 확인한다.

</details>

#### 확인 Q07 · Pointer 산술과 반환 수명

충분한 array에서 각각 새로 시작한다: (a) `p=&a[2];q=p+3;p+=6;` (b) `p=&a[8];q=p-3;p-=6;` (c) `p=&a[5];q=&a[1];` 뒤 `p-q,q-p,p<=q,p>=q`. 결과와 one-past 규칙을 쓰고 local parameter 주소 반환과 `&a[n/2]` 반환의 수명 조건을 비교하라.

<details><summary>해설 보기</summary>

(a) p→a[8],q→a[5]; (b) p→a[2],q→a[5]; (c) 4,-4,0,1이다. 감산은 같은 array의 원소 거리이며 행 사이 상태를 이어 쓰지 않는다. One-past는 경계로 만들 수 있으나 dereference할 수 없다. 지역 value parameter의 주소는 반환 후 수명이 끝나지만 caller object를 가리키는 pointer 반환은 caller object가 살아 있으면 가능하다. `&a[n/2]`는 n>0, 실제 범위와 caller array 수명 유지가 필요하다.

**채점·점검 기준:** 세 독립 초기화, 네 비교값, caller/local lifetime 차이를 모두 확인한다.

</details>

#### 확인 Q08 · Array parameter와 slice

`find_largest(&b[5],10)`의 local `a[0]`, `a[9]`는 어디인가? 전달 비용과 검색 비용, 원소 수정과 local a 재대입, `const int a[]`와 array member를 가진 struct 값 전달을 비교하라.

<details><summary>해설 보기</summary>

b[5]와 b[14]다. Parameter는 `int *`로 조정되어 주소값 하나를 복사하지만 전체 검색은 10개 원소를 읽는다. 첫 원소로 최대값을 초기화하면 n>0과 전체 slice 범위가 필요하다. `a[i]`는 caller 원소를 바꾸지만 local a 재대입은 caller pointer를 바꾸지 않는다. const는 이 경로의 쓰기를 제한하며 모든 alias를 막지는 않는다. `struct` 전체 값 전달은 member array도 복사하는 별도 경우다.

**채점·점검 기준:** Slice 끝 index, 값 전달, const 접근 경로, struct 복사 차이를 포함한다.

</details>

#### 확인 Q09 · Double pointer 전체 trace

처음 `p=&i,q=&j,k=&p`다. `*p=1;*q=2;*k=q;k=&q;*k=&i;*p=3;**k=4;`에서 각 대입의 대상과 최종 관계를 구하라.

<details><summary>해설 보기</summary>

대상은 i,j,p,k,q,j,i 순이다. 먼저 i=1,j=2가 되고 `*k=q`는 p→j, `k=&q`는 k→q, `*k=&i`는 q→i를 만든다. 따라서 최종 p→j,q→i,k→q이며 i=4,j=3이다. 마지막 문장은 k가 더 이상 p를 가리키지 않으므로 j를 바꾸지 않는다.

**채점·점검 기준:** 최종 값만 아니라 p/k/q가 바뀌는 세 단계를 보인다.

</details>

#### 확인 Q10 · 일곱 declarator 읽기

독립 선언 `int *p[10]`, `int (*p)[10]`, `int *(*p)[10]`, `int (*pf)(void)`, `int *pf(void)`, `int (*pf[10])(void)`, `int pf[](void)`를 해석하라. 첫 두 경우 p가 한 단위 전진할 때 byte 차이는?

<details><summary>해설 보기</summary>

순서대로 int pointer 10개 array, int[10] pointer, int pointer 10개 array의 pointer, 무인자 int 반환 함수 pointer, 무인자 int pointer 반환 함수, 첫 함수 pointer 10개 array, 불가한 function 자체의 array다. Identifier에서 []·()를 먼저 읽되 괄호가 결합을 바꾼다. 첫 array의 element pointer로 순회하면 8 bytes, 둘째 p는 int[10] 하나여서 40 bytes다. Array 이름 자체의 증가는 불가하다.

**채점·점검 기준:** 일곱 해석과 8/40-byte 단위를 모두 확인한다.

</details>

#### 확인 Q11 · Type별 sizeof와 array 대입

Target int=4, pointer=8일 때 `int A1[3]`, `int *A2[3]`, `int (*A3)[3]`의 객체·한 번·두 번 dereference type과 sizeof를 표로 구하라. `A={1,2,3}`, `B={4,5,6}`, `A3=&A`, `B3=&B`에서 `*A3=*B3`, `**A3=**B3`, `pA=*A3`는?

<details><summary>해설 보기</summary>

|선언|객체|한 번 *|두 번 *|
|---|---|---|---|
|A1|int[3],12|int,4|불가|
|A2|int *[3],24|int *,8|int,4|
|A3|int (*)[3],8|int[3],12|int,4|

Non-VLA sizeof는 type을 따르며 실제 미초기화 pointer 읽기 허가가 아니다. 첫 대입은 array 대입이어서 불가, 둘째는 A[0]만 바꿔 `{4,2,3}`, 셋째는 첫 원소 주소를 pA에 넣는다. `**A3`는 `A3[0][0]`이며 slide의 `A3[0]` 표기와 다르다.

**채점·점검 기준:** Type와 크기를 함께 쓰고 잘못된 array 대입·source 표기 오류를 구분한다.

</details>

#### 확인 Q12 · Heap 주소·초기화·I/O 길이

A가 0x56550004에서 시작하는 1024개 int를 가리킨다. 총 bytes와 A[1], A[2], A[1023] 주소는? 512-byte array의 부분 초기화와 malloc 후 세 byte만 쓰기의 차이, 할당된 `char *p`에 대한 `read(fd,p,sizeof(p))`, 한 char 목적지, 실패·free 책임을 설명하라.

<details><summary>해설 보기</summary>

4096=0x1000 bytes, 주소는 0x56550008/0x5655000c/0x56551000이다. A object 자신의 주소와 이 base는 다르다. `char buf[512]={'A','B','C'}`의 나머지는 0이지만 malloc의 나머지는 미초기화이며 calloc이 zero-initialization을 제공한다. Heap pointer p의 sizeof는 8이라 요청은 8 bytes이고 확보 길이는 별도로 보유해야 한다. 별도의 `char c`에는 `read(fd,&c,1)`처럼 주소와 1-byte 길이를 전달한다. Allocation 실패를 확인하고 사용 뒤 free하며 해제 뒤 접근하지 않는다. 종료 시 OS 회수는 장기 실행 leak의 해결책이 아니다.

**채점·점검 기준:** 세 주소·4096 bytes, 초기화 차이, 요청 길이 8을 검산한다.

</details>

#### 확인 Q13 · Reallocation의 성공과 실패

256개 int를 512개로 늘리는 자료 예에서 bytes와 보존·초기화 범위는? 양수 크기 realloc 실패를 기존 pointer에 바로 대입할 때 위험, 성공 뒤 alias, libc/OS 역할을 설명하라.

<details><summary>해설 보기</summary>

1024→2048 bytes이며 기존 0..255 값은 유지할 범위이고 새 256..511은 별도 초기화가 필요하다. 실패하면 NULL이지만 old block은 살아 있어 pointer를 덮으면 접근 수단을 잃을 수 있다. 성공 뒤 반환 pointer를 사용하고 old base·interior alias를 재사용하지 않는다. malloc/free는 libc 요청이며 OS와 brk/sbrk 또는 mmap으로 상호작용할 수 있다. 모든 allocation이 단일 연속 heap인 것은 아니다. Zero-size realloc의 보편 규칙이나 allocator 구현으로 확대하지 않는다.

**채점·점검 기준:** 실패 시 old block 유지, 성공 시 새 pointer 사용, 새 영역 초기화를 구분한다.

</details>

#### 확인 Q14 · 독립 allocation 수명

모든 요청 성공을 가정한다. `p1=malloc(3);p2=malloc(1);p3=malloc(4);free(p2);p4=malloc(6);free(p3);p5=malloc(2);`에서 두 free 직후와 p5 할당 직후 살아 있는 allocation을 쓰라. p5 주소와 마지막 해제 순서는 보장되는가?

<details><summary>해설 보기</summary>

free(p2) 뒤 p1·p3, free(p3) 뒤 p1·p4, p5 뒤 p1·p4·p5다. 이 세 allocation을 각각 해제하면 모두 끝나며 요청 순서와 동일 순서일 필요가 없다. Freed 공간이 재사용될 수 있지만 p5가 옛 p2 주소라는 보장은 없다. 옛 p2/p3 pointer를 dereference할 권한도 생기지 않는다. 이 sequence는 realloc 크기 변경과 별개다.

**채점·점검 기준:** 세 live 집합과 주소 재사용 비보장을 확인한다.

</details>

#### 확인 Q15 · Memory error의 원인 분류

다음을 각각 진단하라: 미초기화 y[i]의 `+=`, N개 `int *` slot에 `N*sizeof(int)` 할당, `char s[8]`에 9문자와 NUL, `p+=sizeof(int)`, `*size--`, local 주소 반환, use-after-free, double free, head만 해제. 어떤 진단 도구가 도움이 되며 crash 여부가 C 유효성을 결정하는가?

<details><summary>해설 보기</summary>

순서대로 0부터 누적이 아님; 8-byte pointer에 4-byte int 기준이어서 부족; 10 bytes가 필요해 overflow; 이미 scaling되는 pointer를 네 int 이동; `*(size--)`여서 count가 아니라 pointer 이동이다. Local 주소는 반환 후 수명이 끝나고 free 뒤 접근·같은 block 재해제는 잘못이다. Head의 next가 별도 allocation이면 자동 해제되지 않아 소유 참조를 잃을 수 있다. Debugger는 상태 관찰을, mtrace/muntrace·Valgrind는 allocation이나 접근 오류 조사를 도울 수 있다. 관찰은 결함 위치를 찾는 단서지만 crash가 없다고 undefined behavior가 유효해지지는 않는다.

**채점·점검 기준:** 아홉 원인을 각각 적고 crash 여부와 C 유효성을 동일시하지 않는다.

</details>

### 적용과 점검

#### 연습 P01 · Alias를 바꾼 뒤 무엇을 측정하는가

**새로 만든 합성 연습.** Q1(a)의 type 판별 [EX:sp_2025_1_midterm_q01 p.2]와 Q1(b)의 pointer/원소 추적 [EX:sp_2025_2_midterm_q01 p.3]을 결합한다. 선수는 본문의 array decay·alias·non-VLA sizeof이며 원문 문항이 아니다. Target int=4, pointer=8이다.

```c
int a[3]={2,4,6};
int *p=a, *q=&a[2];
int **r=&p;
*r=q;
**r=a[0]+1;
q=a;
*q=9;
```
최종 a와 p/q/r의 관계, `sizeof(a)`, `sizeof(*r)`, `sizeof(**r)`를 구하라. `*r=q`를 `*p=*q`로 바꾼 독립 실행에서는 무엇이 달라지는가?

<details><summary>해설 보기</summary>

원래는 p→a[2]로 바뀌어 a[2]=3, 이후 q→a[0]가 되어 a[0]=9다. 최종 `{9,4,3}`, p→a[2], q→a[0], r→p이며 sizeof는 12/8/4다. 변경 실행에서는 첫 대입이 a[0]=6을 쓰고 p는 a[0]에 남는다. 다음 문장이 같은 a[0]에 7을 쓰고 마지막에 9가 되어 `{9,4,6}`이다. 두 실행의 sizeof는 type이 같아 변하지 않는다.

**채점·점검 기준:** 각 대입의 왼쪽 object를 추적하고 두 최종 array와 불변 sizeof를 확인한다.

</details>

### 복습 순서

Q02·Q06·Q09는 object별 상자를 그려 다시 풀고 P01 두 실행을 비교하라. Q10–Q11은 type을 먼저 적고, Q12–Q15는 크기·초기화·살아 있는 allocation을 각각 별도 열로 점검하라.

## 출처

[[courses/system_programming/lectures/2026-09-02-lecture-01|2026-09-02 · 강의 노트]]

[[courses/system_programming/lectures/2026-09-07-lecture-02|2026-09-07 · 강의 노트]]

[[courses/system_programming/lectures/2026-09-09-lecture-03|2026-09-09 · 강의 노트]]

[[courses/system_programming/lectures/2026-09-23-lecture-06|2026-09-23 · 강의 노트]]

[00.Introduction.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx) — slide 51; slide 54

[02.CPointers_24a7628c.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx) — slides 3, 9, 15, 17, 23–25, 28–29, 31–36, 38–39

[06.MM.Variable.and.Memory.Recap.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx) — slide 15; slide 34; slide 4; slide 17; slide 20

[[courses/system_programming/transcripts/2026-09-02|2026-09-02 · 보정 STT]] — 01:15:55, 01:21:23, 01:34:38, 01:29:10

[[courses/system_programming/transcripts/2026-09-07|2026-09-07 · 보정 STT]] — 54:41

[[courses/system_programming/transcripts/2026-09-09|2026-09-09 · 보정 STT]] — 01:22–20:26, 21:19

[[courses/system_programming/transcripts/2026-09-23|2026-09-23 · 보정 STT]] — 05:36, 06:37

[08.MM.Dynamic.Memory.Allocation.I.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/08.MM.Dynamic.Memory.Allocation.I.pptx) — slides 5, 7–9, 15–25, 27

[09.MM.Dynamic.Memory.Allocation.II.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/09.MM.Dynamic.Memory.Allocation.II.pptx) — slide35; slide38; slide40; slide44

수치 계산은 x86-64 Linux 자료 조건에 한정한다. 원자료 A3 표기·array 대입 오류와 불완전한 function decay 발화는 그대로 구분하며, non-VLA sizeof가 실제 미초기화 pointer 접근을 허용하지 않는다. Allocation 두 deck은 선택적 자료 기반 복습이고 allocator list·coalescing·binning은 범위 밖이다. 새 deck 전체 그림의 배치 검증이 없으므로 호출 sequence와 명시한 type·크기만 사용한다. 9월 23일의 불명확한 allocation 숫자·초기화 발화는 복원하지 않으며 계산은 자료를 따른다. 과거 시험 제공 crash 목록은 undefined behavior 전체의 정의가 아니다.

아래 과거 시험 연결은 명시한 추론 요구에 한정한다. 제공 답안은 참고자료이며 독립 검증된 정답으로 간주하지 않고, 현재 시험 범위나 출제 빈도를 추정하지 않는다.

[[exam_questions/sp_2025_1_midterm_q01|2025-1 중간 Q1 · C pointer (기존 미리보기)]]

[[exam_questions/sp_2025_2_midterm_q01|2025-2 중간 Q1 · C 프로그래밍 (기존 미리보기)]]
