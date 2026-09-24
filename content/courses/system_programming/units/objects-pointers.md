---
title: "C object·type·주소와 pointer"
description: "Type·주소·lifetime으로 pointer 코드와 memory 크기를 검산한다."
course: "system_programming"
unit_id: "objects-pointers"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["00.Introduction.pptx", "02.CPointers_24a7628c.pptx", "06.MM.Variable.and.Memory.Recap.pptx"]
private_source_assets: []
source_lectures: ["courses/system_programming/lectures/2026-09-02-lecture-01", "courses/system_programming/lectures/2026-09-07-lecture-02", "courses/system_programming/lectures/2026-09-09-lecture-03", "courses/system_programming/lectures/2026-09-23-lecture-06"]
---

값을 담은 object와 그 주소를 담은 pointer를 분리해서 읽는다. Type과 lifetime을 먼저 적으면 복잡한 선언·간접 대입·크기 계산을 추적할 수 있다.

## C object(객체)와 type(자료형): 같은 bytes를 어떻게 읽는가

`int n = 5;`를 이해하려면 이름 `n`, 저장된 값 5, 그 값을 담는 object를 구분해야 한다. C의 object는 값을 저장하는 공간이고 variable(변수)의 이름은 그 공간을 지칭하는 수단이다. Type은 필요한 크기와 저장값을 해석하는 방법을 정한다. [[courses/system_programming/units/systems-c-build|C의 상태 변화와 build]]에서 본 대입은 이 object의 값을 바꾼다.

이 단원의 수치는 강의의 x86-64 Linux target을 따른다.

| Type | 크기(bytes) |
|---|---:|
| `char` | 1 |
| `short` | 2 |
| `int` | 4 |
| `long` | 8 |
| `float` | 4 |
| `double` | 8 |
| Object pointer | 8 |

다른 ABI(Application Binary Interface, 프로그램의 이진 인터페이스 규칙)에서는 크기가 달라질 수 있다. 특히 “64-bit OS이면 `long`은 항상 8”을 모든 환경의 C 규칙으로 만들면 안 된다. [Introduction slides 51–54](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx)

Floating-point(부동소수점)는 sign(부호), exponent(지수), significand 또는 mantissa(유효숫자)를 이용해 수를 표현한다. 유한한 bit 수로 모든 실수를 정확하게 나타낼 수 없으므로 반올림이 생긴다. [[courses/system_programming/transcripts/2026-09-02|2026-09-02 STT 01:15:55]]은 IEEE 754를 소개하지만 상세 encoding 계산까지 확정된 범위는 아니다. `long double`의 16-byte 저장공간을 128-bit 유효 정밀도와 동일시해서도 안 된다.

## Address(주소), pointer(포인터), pointee(가리키는 대상)

Byte-addressed memory에서는 각 byte에 주소가 있고 여러 byte를 차지하는 object의 주소는 첫 byte의 주소다. Pointer는 주소값을 저장하는 별도의 object다. `int *ap`의 `*`는 선언에서 pointer type을 구성하고, 식 `*ap`의 `*`는 dereference(간접 참조)를 뜻한다. `&a`는 `a`의 주소를 구한다.

Memory recap slide 15의 도식은 다음 관계를 보여 준다. 숫자는 관계를 설명하는 도식 주소이며 실제 8-byte pointer 배치를 그대로 축소한 memory map은 아니다.

| Object | object 자체의 도식 주소 | 저장된 값 |
|---|---:|---:|
| `a` | 16 | 5 |
| `ap` | 28 | 16 |
| `app` | 4 | 28 |

```c
int a = 5;
int *ap = &a;
int **app = &ap;
```

따라서 `ap`와 `&a`는 같은 주소값 16, `&ap`는 28이다. `app`를 한 번 따라간 `*app`는 pointer object `ap`를 지칭하여 값 16을 읽고, 두 번 따라간 `**app`는 `a`의 값 5를 읽는다. `*app`에 대입하면 `ap`의 대상이 바뀌고 `**app`에 대입하면 현재 그 경로가 도달하는 `int`가 바뀐다. [Memory recap slide 15](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)

[[courses/system_programming/transcripts/2026-09-07|2026-09-07 STT 54:41]]은 주소 출력의 `%p`와 정수 값 출력의 `%d`를 구분한다. 유효하게 초기화한 위 선언에서 다음처럼 쓸 수 있다.

```c
printf("%p\n", (void *)ap);
printf("%p\n", (void *)&ap);
printf("%d\n", *ap);
```

앞의 두 줄은 대상의 주소와 pointer 자체의 주소를, 마지막 줄은 5를 출력한다. Object pointer를 `%p`의 `void *` 인자에 맞춘 것은 이식성을 위한 문법 한정이다. 실제 주소 숫자는 실행마다 달라질 수 있다.

`sizeof(ap)`는 8, `sizeof(*ap)`는 `int`의 크기인 4다. `void *k` 자체도 8 bytes이지만 `void`는 완전한 object type이 아니므로 표준 C의 `sizeof(*k)`로 대상 크기를 얻을 수 없다. Cast는 해석할 type을 바꿀 뿐 유효한 storage, lifetime(수명), alignment(정렬)를 새로 만들어 주지 않는다. 초기화되지 않은 pointer를 출력하거나 dereference하는 것을 안전하다고 받아들이면 안 된다. 우연히 crash가 없었다고 유효한 접근이 되는 것도 아니다.

## Pointer 대입과 대상 값의 대입

두 대입은 왼쪽에서 바꾸는 object부터 다르다.

```c
int i = 1, j = 2;
int *p = &i, *q = &j;
*q = *p;
q = p;
```

`*q = *p`는 `i`의 값 1을 `j`에 복사한다. 이때 `p→i`, `q→j` 관계는 그대로다. 이어 `q = p`는 `q`에 주소값을 복사하므로 둘 다 `i`를 가리킨다. 이 상태에서 `*p=1; *q=2;`를 실행하면 두 대입 모두 `i`를 바꾸어 마지막 값은 2다. [Pointers slides 13–15](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx)

`scanf("%d", ...)`도 값이 아니라 저장할 `int`의 주소를 요구한다. `int i;`에는 `&i`, `int *p=&i;`에는 `p`를 전달한다. `&p`의 type은 `int **`이므로 같은 계약이 아니다. “`scanf`에는 무조건 `&`를 붙인다” 대신 “이 format이 요구하는 대상 object의 주소인가”로 판단해야 한다.

`int a[10]`은 원소 열 개의 storage를 확보한다. `int *a`는 주소 하나를 보관할 object만 확보한다. 두 번째 선언 뒤 곧바로 `*a=0`을 해도 쓸 수 있는 원소가 자동으로 생기지 않는다.

## Array(배열)와 string(문자열)의 저장공간

Array는 같은 type의 원소가 연속된 object다. 전체 크기는 `N * sizeof(T)`이므로 `char c[10]`은 10 bytes, `double pi[5][2]`는 이 target에서 `5*2*8=80` bytes다. `int a[10]`은 40-byte array이며 8-byte pointer object가 아니다.

다만 많은 expression에서 array는 첫 원소의 pointer로 변환된다. 그래서 `a+i`와 `&a[i]`, `*(a+i)`와 `a[i]`가 대응한다. Byte 주소 계산은 `base + i*sizeof(T)`이지만 typed pointer 식 `a+i`에는 원소 크기만큼의 이동이 이미 포함된다. 여기서 `sizeof(T)`를 다시 곱하면 두 번 확대한다. `sizeof(a)`와 `&a` 같은 문맥은 이 변환과 구분한다. `a++`로 array의 시작을 바꿀 수 없으므로 순회에는 별도 pointer를 사용한다. NUL을 찾으며 이동할 때도 종료 문자가 실제 array 안에 있어야 한다. [Pointers slides 18–25](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx)

### Literal의 주소와 writable array

C string은 NUL byte, 즉 `'\0'`로 끝나는 character sequence다. 다음 두 선언은 다른 저장 방식을 만든다.

```c
char *s = "hello world\n";
char text[20] = "SNU CSE00800";
```

`s`는 literal의 첫 문자 주소를 저장한다. `text`는 별도의 20-byte array에 문자를 담는다. `SNU` 3자, space 1자, `CSE` 3자, `00800` 5자로 length는 12이고 첫 NUL은 `text[12]`이다. 남은 원소도 0으로 초기화된다. Capacity 20, string length 12, 종료 NUL의 1 byte는 서로 다른 수치다.

`text`의 원소는 바꿀 수 있지만 string literal을 수정하는 것은 undefined behavior(정의되지 않은 동작)다. 특정 crash를 반드시 보장한다는 뜻은 아니다. 반대로 pointer가 가리킨다는 이유만으로 모든 대상이 read-only인 것도 아니다. `struct student { int id; char *name; };`의 `name`은 문자 전체가 아니라 주소를 담으므로 구조체 복사만으로 string의 독립 사본이나 수명이 생기지 않는다. [[courses/system_programming/transcripts/2026-09-02|2026-09-02 STT 01:29:10–01:34:38]], [Introduction slide 54](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx)

### 함수 이름과 structure pointer

`void foo(void)`가 있을 때 `void (*fp)(void)=foo`와 `void (*fp)(void)=&foo`는 같은 함수를 지정한다. Function designator(함수 지시자) `foo`가 pointer로 변환되는 것이지 함수 자체가 pointer 변수인 것은 아니다. `sizeof(foo)`로 기계어 길이를 구할 수도 없다. Function pointer와 object pointer는 별도 범주라서 함수 주소를 `void *`로 바꾸어 `%p`로 출력하는 방법을 모든 C 환경에 일반화하지 않는다.

Memory recap의 `shared`는 `struct __shared`를 가리키는 pointer다. `sizeof(shared)`는 8이지만 `sizeof(*shared)`는 `sem_t m`, `int shared_int`와 padding을 포함한 전체 구조체 크기다. `sem_t`의 구체적 크기가 없으므로 숫자를 추정할 수 없다. `&shared->shared_int`는 유효한 대상 안의 member 주소, `&shared`는 pointer object 자체의 주소다. [[courses/system_programming/transcripts/2026-09-23|2026-09-23 STT 05:36–06:37]], [Memory recap slide 4](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)

## Pointer arithmetic과 object의 lifetime

Pointer 이동은 byte 수가 아니라 원소 수로 읽는다. Slides 21–24의 세 예는 **각각 초기 상태를 다시 설정**한다.

| 초기화 | 연산 | 결과 |
|---|---|---|
| `p=&a[2]` | `q=p+3; p+=6;` | `q=&a[5]`, `p=&a[8]` |
| `p=&a[8]` | `q=p-3; p-=6;` | `q=&a[5]`, `p=&a[2]` |
| `p=&a[5]; q=&a[1];` | `p-q`, `q-p` | 4, -4 |
| 같은 세 번째 초기화 | `p<=q`, `p>=q` | 0, 1 |

마지막 두 줄에 두 번째 예의 `p=&a[2]` 상태를 이어 붙이면 답이 달라진다. 같은 array의 위치 차이는 원소 단위다. Array의 마지막 원소 바로 뒤인 one-past pointer는 만들 수 있지만 그 위치의 원소를 읽을 수는 없다. 이 array 범위의 순서 비교 설명을 임의의 서로 다른 object 주소에 적용하지 않는다. [Pointers slides 21–24](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx)

Pointer를 반환할 때는 숫자보다 대상의 lifetime이 중요하다. 자료의 `max(int *a,int *b)`가 큰 값을 가진 caller object의 주소를 반환하면 그 object가 살아 있는 동안 사용할 수 있다. 반대로 `max(int a,int b)`가 `&a`나 `&b`를 반환하면 함수 종료와 함께 local parameter의 lifetime이 끝난다. 저장했던 주소값이 남아 있어도 그 object를 계속 읽을 권리가 남는 것은 아니다.

`find_middle(a,n)`의 `&a[n/2]`도 `n>0`이고 해당 원소가 존재하며 caller array가 살아 있다는 전제를 가진다. [Pointers slides 16–18](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx)

## Array parameter와 double pointer

함수 parameter의 `int a[]`는 `int *a`로 조정된다. Array 전체 대신 주소값을 복사하므로 전달 자체는 원소 수 `N`에 비례하지 않는다. 그렇다고 모든 원소를 조사하는 `find_largest`의 실행도 일정 시간이 되는 것은 아니다. 그 scan은 `N`에 비례한다.

`find_largest(&b[5],10)`에서는 callee의 `a[0]`이 caller의 `b[5]`, `a[9]`가 `b[14]`다. 이 열 원소가 존재해야 하며 `a[0]`을 초기 최대값으로 사용하는 구현은 빈 입력을 받지 못한다. `const int a[]`는 그 접근 경로를 통한 원소 변경을 막는다. Callee가 `a[i]`를 바꾸면 caller의 원소가 바뀌지만 local pointer `a`를 다른 주소로 대입하는 것만으로 caller의 pointer 변수까지 바뀌지는 않는다. Array member가 든 `struct` 전체를 값으로 전달할 때는 구조체와 그 안의 array 값이 복사되는 다른 경우다. [[courses/system_programming/transcripts/2026-09-09|2026-09-09 STT 03:08–10:32]], [Pointers slides 26–30](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx)

### Double pointer가 바꾸는 것은 어느 object인가

`int **k`는 `int *` object의 주소를 담는다. 자료의 다음 trace에서는 `k`의 대상도 중간에 바뀐다.

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

처음 두 store 뒤 `i=1,j=2`다. `*k=q`는 `k`가 지칭하는 `p`에 `q`의 주소값을 넣어 `p→j`로 만든다. `k=&q`는 `k`의 대상을 `q`로 바꾸고, 이어 `*k=&i`는 `q→i`로 만든다. 이제 `*p=3`은 `j`를, `**k=4`는 `k→q→i`를 따라 `i`를 변경한다. 최종값은 `i=4,j=3`이다. `*`의 개수만 세기보다 매 대입 뒤 화살표를 갱신해야 한다. [Pointers slides 31–35](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx), [[courses/system_programming/transcripts/2026-09-09|2026-09-09 STT 15:26–19:25]]

## 복합 선언을 type으로 읽고 sizeof를 계산하기

Identifier에서 시작해 결합을 바깥으로 읽는다. Postfix `[]`와 function `()`가 `*`보다 먼저 결합하지만 grouping 괄호가 순서를 바꾼다.

| 독립적인 선언 | 뜻 |
|---|---|
| `int *p[10];` | `int *` 열 개의 array |
| `int (*p)[10];` | `int[10]` 하나를 가리키는 pointer |
| `int *(*p)[10];` | `int *` 열 개의 array를 가리키는 pointer |
| `int (*pf)(void);` | 인자 없이 `int`를 반환하는 함수의 pointer |
| `int *pf(void);` | 인자 없이 `int *`를 반환하는 함수 |
| `int (*pf[10])(void);` | 첫 번째 종류의 function pointer 열 개의 array |
| `int pf[](void);` | 함수 자체의 array를 요구하여 허용되지 않음 |

첫 번째 `p`가 변환된 뒤 `p+1`은 pointer 원소 하나, 즉 target에서 8 bytes를 이동한다. 두 번째는 `int[10]` 하나, 즉 40 bytes를 이동한다. [Pointers slide 36](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx)

다음 크기는 모두 같은 target의 non-VLA type을 기준으로 한다.

| 선언 | `sizeof(A)` | `sizeof(*A)` | `sizeof(**A)` |
|---|---:|---:|---:|
| `int A1[3]` | 12 | 4 | type 오류 |
| `int *A2[3]` | 24 | 8 | 4 |
| `int (*A3)[3]` | 8 | 12 | 4 |

`*A3`는 `int[3]`이고, 그것이 원소 pointer로 변환된 뒤 한 번 더 dereference한 `**A3`는 첫 `int`다. Slide 38의 `**A3: A3[0]` 표기는 이 type과 맞지 않으며 정확한 대응은 `A3[0][0]`이다. 또 non-VLA `sizeof(*A3)`는 operand를 실제로 읽지 않으므로 초기화되지 않은 pointer를 실행 중 dereference해도 안전하다는 증거가 아니다.

`A={1,2,3}, B={4,5,6}`, `A3=&A, B3=&B`라면 `*A3=*B3`는 array 전체 대입이어서 허용되지 않는다. `**A3=**B3`는 첫 원소만 복사하므로 `A={4,2,3}`이 된다. `pA=*A3`는 첫 원소의 주소를 저장한다. [Pointers slides 38–39](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx)

기출의 `sizeof` 요구도 먼저 “pointer 자체, 대상 object, array 전체 중 무엇의 type인가”를 구별해야 해결된다. 특히 문자열 literal의 저장 크기는 종료 NUL을 포함하고 string length와 다르다. 이 type 판단을 전수해야 하며 특정 실행에서 crash하지 않았다는 결과를 C의 유효성 판정으로 삼으면 안 된다. [EX:sp_2025_1_midterm_q01 p.2]

## Dynamic allocation(동적 할당)의 크기와 초기화

`malloc`은 요청한 storage의 시작 주소를 돌려준다. Pointer 변수의 주소와 확보한 storage의 주소는 다르다. Memory recap slide 17에서는 `A` 자체의 도식 주소가 `0xffffc1a4`이고, 저장된 heap 시작 주소는 `0x56550004`다. `1024 * sizeof(int)=4096=0x1000` bytes이므로 다음 주소를 얻는다.

| 원소 | 시작 주소 |
|---|---|
| `A[0]` | `0x56550004` |
| `A[1]` | `0x56550008` |
| `A[2]` | `0x5655000c` |
| `A[1023]` | `0x56550004 + 1023*4 = 0x56551000` |

One-past 주소는 `0x56551004`다. [[courses/system_programming/transcripts/2026-09-23|2026-09-23 STT 24:43]]에는 byte 수와 주소의 혼동이 남아 있어 이 계산은 slide의 식과 도식에 따른다. [Memory recap slides 16–20](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)

`char buf[512]={'A','B','C'}`는 나머지 원소를 0으로 초기화한다. 반면 `malloc(512)` 뒤 첫 세 byte만 대입해도 나머지가 0이라는 보장은 없다. `calloc`은 확보 영역의 bytes를 0으로 초기화한다. STT 26:45–28:44의 불명확한 표현에서 `malloc`의 zero 보장이나 신뢰할 수 있는 난수성을 끌어내면 안 된다.

할당 실패를 확인하고, 필요한 동안만 사용하며, 사용이 끝나면 `free`해야 한다. Process 종료 때 OS가 자원을 회수해도 오래 실행되는 프로그램에서 누적되는 leak이 정당화되지는 않는다.

마지막으로 `sizeof`는 allocation 기록을 조회하지 않는다. 실제 array `char buf[512]`의 `sizeof(buf)`는 512지만 `char *buf`의 값이 512-byte 영역을 가리켜도 `sizeof(buf)`는 8이다. 따라서 `read(fd,buf,sizeof(buf))`는 pointer인 경우 8 bytes만 요청한다. `BUFSIZE` 같은 실제 capacity를 별도로 보관해야 한다. `char` 한 개를 읽을 때는 저장값이 아니라 `&buf`를 전달한다. 이 구분은 [[courses/system_programming/units/io-streams|I/O의 요청 길이와 반환 길이]]를 이해하는 바탕이다.

## 핵심 정리

- Pointer 값, pointer 자신의 주소, pointed-to 값은 별개다.
- Array capacity와 string length는 pointer sizeof에서 나오지 않는다.
- 간접 대입마다 바뀌는 object를 표시하고 reset을 보존한다.
- 배치 계산은 [[courses/system_programming/units/memory-layout|alignment와 memory layout]]으로 이어진다.

## 확인·연습문제

### 개념 확인과 추론

#### 확인 Q01 · 크기와 정밀도

강의 target에서 char·short·int·long·float·double·pointer 크기는? double 8 bytes와 long double 16 bytes가 뜻하지 않는 것은?

<details><summary>해설 보기</summary>

각각 1, 2, 4, 8, 4, 8, 8 bytes다. 다른 ABI의 보편값은 아니다. Floating point는 sign·exponent·significand로 유한한 값을 나타내므로 모든 실수를 정확히 표현하지 못한다. Storage 크기 16 bytes가 128-bit precision을 뜻하지 않는다.

**채점·확인:** 크기·ABI·표현 정밀도를 구별한다.

</details>

#### 확인 Q02 · 주소를 저장한 object

`a=5`, `ap=&a`, `app=&ap`이고 schematic 주소가 a=16, ap=28, app=4다. ap·&ap·*ap·*app·**app와 두 간접 대입을 설명하고 printf 형식을 정하라.

<details><summary>해설 보기</summary>

`ap`는 16, `&ap`는 28, `*ap`는 5다. `*app`는 ap object를 가리키는 lvalue이고 값은 16, `**app`는 a의 5다. `*app=&b`는 ap를 b로 돌리고 이후 `**app=9`는 b를 바꾼다. `app` 자체는 그대로다. 주소는 `%p`에 `(void *)ap`·`(void *)&ap`, int는 `%d`에 `*ap`를 준다. Pointer 8 bytes와 int 4 bytes는 다르다. `void *`도 8 bytes지만 표준 C의 `sizeof(void)`는 없다. Cast는 lifetime·alignment·유효 대상을 만들지 않으며 uninitialized pointer의 비충돌은 안전 증거가 아니다. 숫자 4·16·28은 실제 8-byte 배치가 아닌 도식이다.

**채점·확인:** 주소·주소 object·값과 두 단계 대입 대상을 구분한다.

</details>

#### 확인 Q03 · Array·function·struct pointer

`int a[10]; int *p=a;`의 sizeof와 a+2, `char[10]`·`double[5][2]` 크기를 구하라. Function name과 &foo, struct pointer와 struct 크기도 비교하라.

<details><summary>해설 보기</summary>

`sizeof(a)=40`, `sizeof(p)=8`, `a+2`는 8 bytes 뒤 세 번째 int다. Char array는 10, double array는 80 bytes다. Array는 보통 첫 원소 pointer로 변환되지만 sizeof·주소 연산에서는 구별되며 `a++`는 불가하다. Typed addition에 다시 sizeof를 곱하지 않는다. `void foo(void)`의 foo와 &foo는 `void (*fp)(void)`에 쓸 수 있지만 function sizeof나 object-pointer 방식의 이식 가능한 함수 주소 출력은 보장되지 않는다. `sizeof(shared)=8`이나 `sizeof(*shared)`는 member와 padding 전체다. `sem_t` 크기 없이 추정하지 않는다. Member 주소와 pointer 변수 자신의 주소도 다르다.

**채점·확인:** 40/8/8-byte 이동·10/80·function pointer·미정 struct 크기를 확인한다.

</details>

#### 확인 Q04 · String의 세 길이

`char s[20]="SNU CSE00800"`의 length·NUL index·capacity는? `char *p="abc"`와 writable array, struct의 name pointer 복사는 어떻게 다른가?

<details><summary>해설 보기</summary>

Length는 12, 첫 NUL은 index 12, capacity는 20이며 s[12]..s[19]는 zero다. `p`는 문자 전체가 아닌 첫 주소를 저장하고 literal은 NUL 포함 4 bytes다. `char a[4]="abc"`의 a[0] 수정은 가능하지만 literal의 p[0] 수정은 undefined behavior이며 반드시 crash한다는 뜻은 아니다. `struct student`의 `char *name`을 복사하면 주소만 복사되어 동일 문자를 참조한다. Deep copy나 lifetime 연장은 생기지 않는다.

**채점·확인:** 12/12/20과 pointer storage·문자 storage·lifetime을 구별한다.

</details>

#### 확인 Q05 · 값 복사와 주소 복사

i=1, p=&i, q=&j에서 `*q=*p; q=p; *p=1; *q=2;`를 추적하라. scanf의 `%d`에 &i·p·&p 중 무엇이 맞는가?

<details><summary>해설 보기</summary>

첫 대입은 j=1로 만들고 주소는 유지한다. q=p 뒤 둘 다 i를 가리키므로 마지막 두 대입은 i를 1, 2로 바꾼다. 최종 i=2, j=1이다. `%d`는 `int *`이므로 &i와 p가 맞고 &p는 `int **`여서 아니다. Pointer 선언만으로 pointed-to int가 만들어지지는 않는다.

**채점·확인:** j 값 유지·q 재지정·scanf type을 확인한다.

</details>

#### 확인 Q06 · Lifetime과 pointer 연산

Local int 주소 반환과 caller array 원소 반환을 비교하라. 같은 충분히 큰 a에서 p=a+2, q=p+3, p+=6; 새 시작 p=a+8, q=p-3, p-=6; 다시 p=a+5, q=a+1의 차이·비교를 구하라.

<details><summary>해설 보기</summary>

Local object는 반환 때 lifetime이 끝나 주소 숫자가 남아도 사용할 수 없다. Caller array 원소는 caller가 유지하고 n>0·범위를 만족하면 반환 가능하다. 첫 예는 q=a+5, p=a+8; 새 예는 q=a+5, p=a+2다. 마지막 재설정에서는 p−q=4, q−p=−4, p<=q=0, p>=q=1이다. 원소 단위 계산이며 앞 예의 상태를 이어 쓰지 않는다. 같은 array의 유효 범위를 전제하고 one-past는 만들 수 있어도 dereference하지 않는다.

**채점·확인:** 세 reset을 분리하고 lifetime·원소 단위를 설명한다.

</details>

#### 확인 Q07 · Array parameter의 실제 전달

`find_largest(&b[5],10)`의 a[0]·a[9], 전달 비용과 탐색 비용은? const, pointer 재대입, array를 포함한 struct 전달은?

<details><summary>해설 보기</summary>

a[0]=b[5], a[9]=b[14]이며 유효한 10개 원소와 n>0이 필요하다. Array parameter는 pointer로 조정되어 주소 하나의 값이 복사된다: 전달 O(1), 최대값 탐색 O(N)이다. const는 그 접근 경로의 변경을 제한한다. Local a를 재지정해도 caller pointer는 바뀌지 않지만 원소 쓰기는 원본에 닿는다. Array member를 가진 struct를 값으로 넘기면 member도 함께 복사된다.

**채점·확인:** slice 범위·두 비용·주소 복사와 object 복사를 구별한다.

</details>

#### 확인 Q08 · 두 단계 간접 참조

p=&i, q=&j, k=&p로 시작해 `*p=1; *q=2; *k=q; k=&q; *k=&i; *p=3; **k=4;` 전체를 추적하라.

<details><summary>해설 보기</summary>

1: i=1. 2: j=2. 3: k가 p를 가리키므로 p=q=&j. 4: k가 q를 가리킨다. 5: q=&i가 된다. 6: p는 여전히 &j라 j=3. 7: k→q→i라 i=4. 최종 p→j, q→i, k→q, i=4, j=3이다. `*k`가 어떤 pointer object인지 매번 다시 판단해야 한다.

**채점·확인:** 최종 값뿐 아니라 일곱 단계의 변경 대상을 제시한다.

</details>

#### 확인 Q09 · 복합 선언 읽기

서로 독립적인 `int *p[10]`, `int (*p)[10]`, `int *(*p)[10]`, `int (*pf)(void)`, `int *pf(void)`, `int (*pf[10])(void)`, `int pf[](void)`를 분류하라. 첫 둘의 p+1 단위는?

<details><summary>해설 보기</summary>

순서대로 int pointer 10개 array, int 10개 array를 가리키는 pointer, int pointer 10개 array를 가리키는 pointer, 인자 없고 int 반환인 함수 pointer, int pointer 반환 함수, 첫 종류 함수 pointer 10개 array, invalid인 함수 자체 array다. 첫 p가 변환된 뒤 p+1은 pointer 원소 8 bytes, 둘째는 int[10] 40 bytes를 이동한다. Function pointer는 object지만 function 자체는 array 원소가 아니다.

**채점·확인:** 일곱 선언과 8/40 stride를 모두 확인한다.

</details>

#### 확인 Q10 · sizeof와 유효한 대입

`int A1[3], *A2[3], (*A3)[3]`의 변수·한 번/두 번 *의 type과 sizeof를 표로 정리하라. 미초기화 A3의 sizeof와 읽기, A3=&A, B3=&B에서 array/첫 원소 대입도 비교하라.

<details><summary>해설 보기</summary>

|식|type와 bytes|
|---|---|
|A1, *A1, **A1|int[3]:12; int:4; invalid|
|A2, *A2, **A2|int *[3]:24; int *:8; int:4|
|A3, *A3, **A3|int (*)[3]:8; int[3]:12; int:4|

Non-VLA `sizeof(*A3)`는 값을 평가하지 않아 12를 구할 수 있지만 실제 미초기화 pointer 읽기는 안전하지 않다. A={1, 2, 3}, B={4, 5, 6}이면 `*A3=*B3`는 array 대입이라 불가, `**A3=**B3`는 첫 int만 바꿔 A={4, 2, 3}이다. `*A3`는 필요한 문맥에서 첫 int pointer로 변환된다. 원문의 **A3 대응 표기는 `A3[0][0]`로 읽어야 한다.

**채점·확인:** 모든 type·크기와 평가 여부·array 대입 금지를 설명한다.

</details>

#### 확인 Q11 · Allocation과 capacity

4-byte int 1024개가 0x56550004부터라면 A[1]·A[2]·A[1023]·one-past 주소는? 512-byte array와 malloc pointer의 sizeof·초기화·read 크기·수명을 비교하라.

<details><summary>해설 보기</summary>

4096=0x1000 bytes를 확보한다. 주소는 0x56550008, 0x5655000c, 0x56551000, 0x56551004다. `&A`는 pointer 변수의 별도 주소(도식 0xffffc1a4)다. `char a[512]="ABC"`는 나머지를 zero로 하지만 malloc은 초기화하지 않고 calloc은 zeroing한다. Pointer sizeof는 8, array sizeof는 512이므로 `read(fd,p,sizeof(p))`는 8 요청이다. Capacity를 따로 보관·전달하고 한 char에는 `&buf`를 준다. Allocation 실패를 확인하고 마지막 사용 뒤 free하며 dangling 사용을 피한다. 종료 때 OS 정리가 실행 중 leak을 정당화하지 않는다.

**채점·확인:** 네 주소·pointer 자체 위치·8/512·초기화·수명을 확인한다.

</details>

### 응용 연습

#### 연습 P01 · API 경계에서 잃는 크기

**새로 만든 합성 연습.** Target int=4, pointer=8이다. `char text[7]="cat"; char *p=text; int a[3]={1,2,3}; int (*whole)[3]=&a;`에서 sizeof(text), sizeof(p), sizeof(*whole), sizeof(**whole), string length를 구하라. Text를 char * parameter로 받은 함수가 sizeof로 7을 복원할 수 있는가?

[EX:sp_2025_1_midterm_q01 p.2] Q1(a)의 type·sizeof·NUL 추론을 array parameter의 정보 손실 진단으로 확장한 새 연습이다. 선행: Q03·Q04·Q10·Q11. Crash 예측은 제외한다. [[exam_questions/sp_2025_1_midterm_q01|허용된 관련 문항 미리보기]]

<details><summary>해설 보기</summary>

각각 7, 8, 12, 4이며 string length는 3이다. Text의 NUL과 남은 zero bytes는 capacity 안에 포함된다. Pointer parameter에는 주소만 전달되므로 sizeof는 8이며 7이나 length 3을 복원하지 못한다. Capacity는 별도 전달해야 한다. Type별 계산과 API 설계 판단이 함께 필요하다.

**채점·확인:** 7/8/12/4/3과 capacity 별도 전달 이유를 확인한다.

</details>

### 복습 계획

Q02·Q05·Q08을 화살표로, Q06은 reset별 별도 그림으로 푼다. Q09·Q10 type 표를 가리고 재작성한 뒤 Q11·P01로 sizeof와 capacity를 구별한다.

## 출처

### 날짜별 강의 노트

- [[courses/system_programming/lectures/2026-09-02-lecture-01|2026-09-02 강의 노트]]
- [[courses/system_programming/lectures/2026-09-07-lecture-02|2026-09-07 강의 노트]]
- [[courses/system_programming/lectures/2026-09-09-lecture-03|2026-09-09 강의 노트]]
- [[courses/system_programming/lectures/2026-09-23-lecture-06|2026-09-23 강의 노트]]

### 수업자료와 강의 구간

- [Introduction slides 51–54](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx)
- [Memory recap slide 15](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)
- [Pointers slides 13–15](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx)
- [Pointers slides 18–25](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx)
- [Introduction slide 54](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx)
- [Memory recap slide 4](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)
- [Pointers slides 21–24](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx)
- [Pointers slides 16–18](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx)
- [Pointers slides 26–30](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx)
- [Pointers slides 31–35](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx)
- [Pointers slide 36](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx)
- [Pointers slides 38–39](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx)
- [Memory recap slides 16–20](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)
- [[courses/system_programming/transcripts/2026-09-02|2026-09-02 STT 01:15:55]]
- [[courses/system_programming/transcripts/2026-09-07|2026-09-07 STT 54:41]]
- [[courses/system_programming/transcripts/2026-09-02|2026-09-02 STT 01:29:10–01:34:38]]
- [[courses/system_programming/transcripts/2026-09-23|2026-09-23 STT 05:36–06:37]]
- [[courses/system_programming/transcripts/2026-09-09|2026-09-09 STT 03:08–10:32]]
- [[courses/system_programming/transcripts/2026-09-09|2026-09-09 STT 15:26–19:25]]
- [[courses/system_programming/transcripts/2026-09-23|2026-09-23 STT 24:43]]

연결된 공개 자료는 slide deck이며, 이 자료들의 PDF 페이지 보기 링크는 제공되지 않았다. 녹취 시각은 일반 텍스트로 표시한다.

### 자료 범위와 한계

- 수치는 강의의 Linux x86-64 target 또는 명시된 도식 주소에 한정한다.
- Unclear 녹취를 복구된 발화로 간주하지 않는다. **A3 표기 오류는 A3[0][0]로 교정하여 해석한다.
- 기출 Q1(a)의 크기 추론만 연결한다. 제공된 crash 답이나 writable 배치가 const/literal 변경을 합법화하지 않는다.


---

[[courses/system_programming/units/systems-c-build|← 이전: System Programming과 C 프로그램의 구성·빌드]] · [[courses/system_programming/units/index|단원 목차]] · [[courses/system_programming/units/state-machines|다음: 문자 처리와 DFA·Decommenter의 경계조건 →]]
