---
title: "System Programming과 C 프로그램의 구성·빌드"
description: "C의 기본 제어 흐름, build 단계, local·remote 작업의 차이를 복습한다."
course: "system_programming"
unit_id: "systems-c-build"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["01.CProgrammingExamples.pptx", "00.Introduction.pptx", "lab 0 setup.pdf", "assign2_README.md", "10.RE.Life.Cycle.of.a.Program.pptx", "11.RE.Linking.and.Loading.pptx"]
private_source_assets: ["lab 0 setup.pdf", "assign2_README.md"]
source_lectures: ["courses/system_programming/lectures/2026-09-02-lecture-01", "courses/system_programming/lectures/2026-09-07-lecture-02", "courses/system_programming/lectures/2026-09-09-lecture-03", "courses/system_programming/lectures/2026-09-23-lecture-06"]
---

OS 서비스를 사용하는 C 프로그램을 상태 변화부터 실행 파일까지 연결해 보자. 작은 코드의 계산과 build·remote 환경의 역할을 구분하며 읽으면 오류가 생긴 단계를 찾기 쉬워진다.

## System Programming과 OS 서비스

파일에서 데이터를 읽어 계산하는 프로그램을 생각해 보자. 어떤 데이터를 읽고 어떤 알고리즘을 적용할지는 프로그램이 정하지만, 저장장치 접근과 권한 판정은 OS가 관리한다. System Programming(시스템 프로그래밍)은 이 경계를 이해하고 OS의 API를 사용하여 파일·메모리·프로세스 서비스를 조합하는 작업이다. [[courses/system_programming/transcripts/2026-09-02|2026-09-02 STT]] 43:28에서도 이미 존재하는 OS와 상호작용하는 관점을 설명한다.

C는 주소와 낮은 수준의 I/O를 직접 표현하면서도 assembly보다 큰 단위인 type, expression, function으로 계산을 조직할 수 있다. Linux는 공개된 구현과 Unix 계열 도구 환경을 제공한다. 이 선택은 C가 모든 작업에서 더 빠르다는 뜻이 아니다. Machine에 가까운 제어를 사용하는 만큼 type 크기, compiler, library, OS가 달라질 때 portability(이식성)를 확인해야 한다. Process, exception, shell, network, concurrency의 전체 구현은 이 도입에서 모두 배운 내용으로 취급하지 않는다. 이 관점의 강의 설명은 [[courses/system_programming/lectures/2026-09-02-lecture-01|2026-09-02 System Programming 강의]]와 연결된다.

### CPU에서 datacenter까지

CPU는 instruction을 실행하고 memory는 실행 중인 데이터를 보유하며 network는 다른 machine과 데이터를 주고받는다. [system_programming:M004 slide 36](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx)의 mainboard 사진에서는 CPU socket과 그 옆의 길쭉한 memory slots를 구분해서 보면 된다. 하나의 chip에 여러 core를 두는 multicore 구성과 memory 연결은 서로 다른 역할이다. Core가 두 배여도 작업을 나누기 어렵거나 memory가 병목이면 프로그램이 두 배 빨라지지 않는다.

강의의 laptop 4·8 cores, server 16개 이상, slide의 4–60 cores, PC의 약 1 Gbit/s와 datacenter의 10–100 Gbit/s는 당시 구성의 예다. ENIAC(1946), mainframe, Apollo 11(1969), smartphone의 대비도 계산 장치가 작아지고 널리 사용되는 흐름을 설명한다. 자동차·시계·speaker 등으로 확장되는 ubiquitous computing(편재형 컴퓨팅)은 프로그램이 다룰 대상이 PC보다 넓다는 뜻이다. 세대 간 ‘수백만 배’ 표현을 같은 작업에 대한 측정된 speedup으로 읽지는 않는다.

Cloud server는 여러 client의 저장·메시지·계산 요청을 처리한다. Rack에 여러 server를 수용하고 이를 연결한 datacenter는 규모를 키우지만, 요청과 데이터를 어디로 보낼지라는 문제도 만든다. CDN(Content Distribution Network)은 여러 지역에 콘텐츠 사본을 두어 먼 원 서버에만 의존하지 않게 한다. 2026-09-02 STT 11:07의 동영상 배포 예가 여기에 해당한다. ‘가까운 서버’는 전달 경로를 줄이는 개념 설명이며 browser가 항상 물리적 최단거리를 직접 계산한다는 뜻은 아니다.

당시 강의는 Meta 수십만 대, Microsoft 약 400만 대(2021), Google 약 250만 대(2016)를 규모의 사례로 들었다. 50:58의 2026년 hyperscaler 지출 600 billion dollars 초과는 미래형 전망이며 확정 지출 실적이 아니다. 1 billion dollars를 약 1.4조 원으로 환산한 것도 당시 설명이다. 이런 숫자의 역할은 규모를 감 잡게 하는 데 있다.

AI training·inference는 계산기에 데이터를 빨리 공급할 HBM(High-Bandwidth Memory)을 요구한다(53:45). 필요한 memory를 여러 GPU나 machine에 나누면 총 용량은 늘릴 수 있지만 중간 결과를 network로 교환해야 한다. 따라서 memory bandwidth뿐 아니라 network bandwidth와 latency도 전체 계산 시간에 영향을 준다. 한 machine의 1 PB HBM 구성이 어렵다는 발언은 당시 비용·구성의 맥락이며 영구적인 물리적 한계가 아니다. Software 요구가 반도체·SoC·차량 hardware의 설계와 만나는 이유가 여기에 있다.

## C의 abstraction과 프로그램 상태

자료는 BCPL → B → C의 흐름을 Unix 발전과 함께 설명한다. B의 word 중심 표현에 비해 C의 type과 byte 수준 접근은 낮은 수준의 작업을 더 명료하게 적는 수단이다. Multics에서 Unix로 이어지는 이야기는 강의의 간략한 역사 설명으로 읽는다. K&R C 뒤의 ANSI C89와 ISO C90은 관련 표준 이름이며, 이 과목의 compiler option은 C99를 선택한다. 강의의 C23 언급이 C99 바로 다음 표준이라는 뜻은 아니다.

Structured programming(구조적 프로그래밍)은 큰 작업을 subroutine으로 나누고 호출 관계로 조직한다. Object-oriented programming(객체 지향 프로그래밍)은 상태와 그 상태를 다루는 interface/member function을 함께 묶는다. 예를 들어 계산 단계별 함수 분해와 상태를 가진 object의 interface 설계는 복잡도를 다루는 서로 다른 관점이다. 초기 Unix와 큰 Linux codebase의 규모 대비는 이런 abstraction이 필요한 이유를 보여 준다. Assembly에 subroutine이 없다는 뜻은 아니다.

### Expression과 side effect

프로그램 상태는 object에 저장된 값들로 생각할 수 있다. Expression(표현식)은 평가되는 구문이다. `2 + 3`은 5를 계산하고, `i = 10`은 `i`를 바꾸는 side effect(부수 효과)를 일으키면서 값 10도 갖는다. 뒤에 `;`를 붙인 `i = 10;`은 expression statement다. `i = j = 0`은 `i = (j = 0)`으로 결합하여 두 object에 0을 저장한다. 오른쪽 결합은 임의의 operand가 평가되는 시간 순서를 보장하는 규칙과는 다르다.

| Operator 종류 | 표기와 의미 |
|---|---|
| Arithmetic | `+`, `-`, `*`, `/`, `%`, unary `-`; `%`는 정수 나눗셈의 나머지 |
| Relational/equality | `<`, `>`, `<=`, `>=`, `==`, `!=`; `=` 대입과 구분 |
| Logical | `&&`, `\|\|`, `!`; 조건의 결합과 부정 |
| Bitwise | `<<`, `>>`, `&`, `\|`, `^`; bit 단위 연산 |
| Compound assignment | `+=`, `*=` 등; 기존 object 값을 갱신 |

2026-09-02 STT 01:39:14–01:42:07의 일반 설명에는 문법상 한정이 필요하다. `void` function의 호출도 expression이지만 값을 공급하지 않는다. 따라서 `f`가 `void`를 반환하면 `f();`는 가능해도 `int n = f();`처럼 정수 초기값을 받을 수 없다. 이것은 발화를 복원한 인용이 아니라 C 문법에 맞춘 설명상의 한정이다.

### Branch, loop, function의 실행 순서

`if (i < 0)`은 `i = -1`에서 참이고 `0`, `1`, `2`에서는 거짓이다. 반면 자료의 별도 `switch (i)` 예에서는 `1`이 `case 1`, `2`가 `case 2`, `-1`과 `0`은 `default`로 간다. 두 예제에서 같은 이름의 statement가 등장해도 실행 조건은 다르다. `switch`의 `break`를 생략하면 다음 case로 흐를 수 있다.

`for`는 초기화 → 조건 검사 → body → 증가식 → 재검사의 순서다. Body가 `i`를 바꾸지 않고 조기 종료하지 않는 `for (int i = 0; i < 10; i++)`는 `i = 0`부터 `9`까지 body를 열 번 실행한다. 조건은 마지막 `i = 10`의 실패까지 열한 번 검사한다. `while`은 먼저 검사하므로 처음부터 거짓이면 body를 실행하지 않는다. `do-while`은 body를 먼저 실행하므로 적어도 한 번 실행한다.

`break`는 현재 loop 또는 `switch`에서 빠져나오고 `continue`는 현재 loop의 다음 반복으로 진행한다. 특히 `for`의 `continue`는 증가식을 거친다. `{ }`는 여러 statement를 하나의 compound statement로 묶는다. `goto`는 label로 이동한다. STT 01:42:07은 여러 실패 경로를 한 error label의 공통 처리로 모으는 동기를 설명한다. 각 경로에서 실제 확보한 자원이 다를 수 있으므로 정리할 대상도 구분해야 한다.

다음은 자료의 함수 의미를 정돈한 작은 예다.

```c
int add(int x, int y)
{
    return x + y;
}
```

`add(3, 5)`는 parameter 값으로 계산하여 8을 반환한다. 함수 정의와 그 함수를 호출하는 expression은 다른 역할이며, `/* ... */`와 `//`의 comment는 실행 command가 아니다.

## Temperature loop로 계산과 이름을 함께 읽기

좋은 이름은 object의 역할과 단위를 드러낸다. [system_programming:M004 slides 62–63](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx)의 온도 표를 C99 문법으로 정돈하면 다음과 같다.

```c
#include <stdio.h>

int main(void)
{
    int lower = 0, upper = 300, step = 20;
    for (int fahr = lower; fahr <= upper; fahr += step) {
        double celsius = (5.0 / 9.0) * (fahr - 32.0);
        printf("%3d %6.1f\n", fahr, celsius);
    }
    return 0;
}
```

`fahr`, `celsius`, `lower`, `upper`, `step`은 `a`, `b`, `c`, `d`, `e`보다 계산의 의도를 보여 준다. `5.0 / 9.0`은 비율을 유지하지만 정수끼리의 `5 / 9`는 0이다. 실제 loop는 `0, 20, …, 300`을 사용하므로 행 수는 `(300 - 0) / 20 + 1 = 16`이다. 300을 출력한 뒤 `fahr`가 320이 되어 종료한다. 별도 식 점검으로 32°F를 넣으면 0°C이지만, 32는 이 loop가 출력하는 입력에 없다.

Function-level comment는 매 줄을 번역하기보다 caller에게 함수의 목적과 계약을 설명하는 편이 유용하다. 작은 역할별 함수, compiler 진단, 재현 가능한 입력·증상·기대 결과를 함께 사용하면 debugging의 추측을 줄일 수 있다. 강의의 주당 7–10시간은 당시 학습 계획 조언이며 개인별 필요 시간을 고정하는 규칙은 아니다.

## Source에서 executable까지의 build

`#include <stdio.h>`를 적었다고 `printf` 구현이 현재 파일에 모두 들어온 것은 아니다. Header의 declaration(선언)은 compiler가 호출을 해석하는 데 필요하고, definition(정의)의 machine code와 연결하는 일은 뒤 단계다. [[courses/system_programming/lectures/2026-09-07-lecture-02|2026-09-07 C build 강의]] 및 [[courses/system_programming/transcripts/2026-09-07|같은 날짜 STT]] 34:43의 흐름을 네 단계로 읽을 수 있다.

| 단계 | 결과 예 | 하는 일 |
|---|---|---|
| Preprocessing | `hello.i` | Include와 macro 처리, comment 제거 |
| Compilation | `hello.s` | Target architecture의 assembly 생성 |
| Assembly | `hello.o` | Machine code와 연결에 필요한 정보를 가진 object 생성 |
| Linking | `hello` | 다른 object/library의 definition과 reference를 연결하여 executable 구성 |

자료의 command는 이 중간 결과를 관찰하는 방법이다.

```sh
gcc800 -E hello.c > hello.i
gcc800 -S hello.i
gcc800 -c hello.s
gcc800 hello.o -lc -o hello
gcc800 hello.c -o hello
```

마지막 줄은 전체 흐름의 shortcut이다. `-o`를 생략한 자료 예의 기본 이름은 `a.out`이다. M003의 `libc.a` 그림은 단계 관계를 설명하며 모든 실제 build가 static linking을 한다는 증거는 아니다. GCC는 이 단계들을 호출하는 compiler driver다.

`gcc800` wrapper의 핵심은 다음과 같다.

```sh
gcc -Wall -Werror -pedantic -std=c99 "$@"
```

`-Wall`은 유용한 warning 묶음, `-Werror`는 warning을 error로 처리하는 정책, `-pedantic`은 선택 표준 관련 진단, `-std=c99`는 language mode다. `-Wall`이 가능한 모든 warning을 뜻하거나 진단 통과가 논리적 정답성을 보증하지는 않는다. `"$@"`는 호출자가 준 filename과 option들의 인자 경계를 보존하여 전달한다.

STT 44:11과 M003 slide 27의 준비 순서는 text wrapper 작성, `chmod +x gcc800`으로 실행 권한 부여, `PATH`에서 찾는 directory에 배치하는 것이다. 자료에는 `/usr/bin/gcc800` 예가 있다. 저장된 파일, 실행 가능한 파일, 이름만으로 검색되는 command는 다른 조건이다. 현재 directory가 `PATH`에 없으면 `./gcc800`처럼 경로를 지정한다. Lab이 이미 설정되었다는 말은 당시 환경 안내다.

### Separate compilation과 linker의 두 책임

RM004 slides 6–15, 17과 RM005 slides 5–8의 선택적 자료 복습은 build를 조금 더 분해한다. `main.c`와 `swap.c`를 각각 compile하면 한 파일만 수정했을 때 그 파일을 다시 compile하고 relink할 수 있다. `main.o`의 `main`, `buf`는 definition이지만 `printf`, `swap`은 `UND`일 수 있다. `swap.o`에는 `swap`, `bufp0`, module 내부의 `static bufp1`이 있고 외부 `buf`를 참조한다. 여기서 local linker symbol은 function의 automatic local variable과 같은 말이 아니다.

Symbol resolution은 reference에 대응하는 definition을 찾는다. Relocation은 합쳐진 section의 실제 위치를 반영하여 주소 의존 reference를 조정한다. Object `.o`, executable, shared object `.so`는 그 결과와 역할이 다르다. 이 두 책임을 설명하는 요구가 [EX:sp_2025_2_midterm_q05 p.12] Q5(a)와 연결된다. ‘파일을 합친다’에서 멈추지 않고 이름을 연결하는 문제와 배치된 주소를 반영하는 문제를 분리하면 된다. 상세 ELF, PC-relative byte 계산, PLT/GOT는 이 자료 복습의 범위를 넘는다. 오래된 implicit-declaration 예도 prototype을 생략하라는 권장은 아니다.

## Local 개발과 remote 검증의 경계

동일한 source라도 compiler, header, library, OS가 다르면 build와 실행 결과가 달라질 수 있다. Ubuntu, WSL, Linux VM은 이 차이를 관리할 환경 선택지다. Private Lab0 자료의 일반 절차는 Windows의 관리자 command prompt에서 `wsl --install`로 설치한 뒤 Ubuntu 또는 `wsl`로 Linux shell을 여는 것이다. `uname -r`은 kernel release, `lsb_release -a`는 distribution 정보를 보여 준다. 이것은 설치·접속 성공 기록이 아니다.

SSH는 인증·암호화된 remote shell, SCP는 파일 복사를 제공한다. 아래는 개인 계정과 host를 제거한 역할 예다. 제공 당시의 교내 22·교외 2222 안내를 현재 endpoint 보증으로 읽지 않는다.

```sh
ssh -p 2222 USER@HOST
scp -P 2222 -r assignment1/ USER@HOST:~/
scp -P 2222 -r USER@HOST:~/assignment1/ ./
```

SSH의 port는 소문자 `-p`, SCP는 대문자 `-P`다. SCP의 첫 인자는 source, 둘째는 destination이며 `-r`은 directory 복사다. 마지막 줄은 source/destination 규칙을 반대로 적용한 설명용 예다. 원자료의 hostname 표기가 서로 달라 실제 접속 대상은 이 예로 확정할 수 없다.

[[courses/system_programming/transcripts/2026-09-09|2026-09-09 STT]] 01:03:10, 01:31:06–01:32:03과 [[courses/system_programming/lectures/2026-09-09-lecture-03|2026-09-09 환경 설정 강의]]는 Remote SSH 연결 뒤 원격 `src/decomment.c`를 여는 흐름을 설명한다. 확장 설치 → host/user/port 설정 → 연결 → 원격 파일 편집의 순서다. 창이 local에 있어도 저장 대상과 그 terminal의 build 위치는 remote VM이다. Local 파일을 편집한 경우에는 복사 후 remote에서 파일과 build를 확인하는 별도 흐름이 필요하다.

`man strstr`은 함수 계약 확인, compiler는 번역·진단, debugger는 실행 상태 관찰, ctags/cscope는 source 탐색, source management는 변경 관리, trace tools는 실행 상호작용 관찰에 사용한다. 후에 제공된 M018의 ARM Mac 안내도 header/API 차이를 고려하여 평가 환경에서 검증하라는 자료상 보충이다. 특정 함수 parameter 차이에 관한 불명확한 발화를 확인된 API 차이로 단정하지 않는다. 다음 [object와 pointer 설명](objects-pointers.md)에서는 이런 프로그램이 실제로 어떤 저장공간을 읽고 쓰는지 구분한다.

## 핵심 정리

- 프로그램은 처리 목적을 정하고 OS는 권한·장치 접근 같은 서비스를 제공한다.
- Core·memory·network는 서로 다른 병목을 만들며 강의의 규모 수치는 날짜가 붙은 사례다.
- Declaration, definition, symbol resolution, relocation을 구분해야 build 오류를 설명할 수 있다.
- 식의 값과 side effect, loop의 body 횟수와 검사 횟수를 따로 추적한다.
- Remote 창의 위치와 편집·실행되는 파일의 위치는 다를 수 있다.

## 확인·연습문제

### 개념 확인과 설명

#### 확인 Q01 · 프로그램과 OS

파일을 읽어 합계를 계산할 때 프로그램과 OS의 역할을 나누고 C·Linux를 쓰는 이유와 한계를 설명하라.

<details><summary>해설 보기</summary>

프로그램은 파일·알고리즘을 정하고 API를 호출한다. OS는 권한과 장치 접근을 관리한다. C는 주소·낮은 수준 I/O를 type과 함수로 표현하고 Linux는 공개 구현과 Unix 도구를 제공한다. 이는 kernel을 직접 구현한다는 뜻도, 모든 작업에서 C가 가장 빠르다는 뜻도 아니다. Machine·OS 차이에 따른 이식성 확인이 필요하다.

**채점·점검 기준:** 역할 두 가지, 선택 이유, 성능·이식성 한정을 모두 설명한다.

</details>

#### 확인 Q02 · Hardware와 성능 비교

CPU socket·memory slot·network의 역할과 multicore의 의미를 설명하라. Core 수를 두 배로 하면 모든 작업이 두 배 빨라지는가? ENIAC부터 smartphone·차량으로 이어지는 사례는 무엇을 보여 주는가?

<details><summary>해설 보기</summary>

CPU는 instruction을 실행하고 memory는 작업 데이터를 보유하며 network는 machine 간 데이터를 옮긴다. Multicore는 한 chip에 여러 core가 있는 구성이다. 병렬화되지 않는 작업이나 memory·통신 병목 때문에 속도가 같은 비율로 늘지 않는다. 역사 사례는 장치의 소형화와 computing의 확산을 보여 준다. 강의의 core 수·bandwidth·세대 간 배수는 당시 사례이지 같은 workload의 검증된 speedup이 아니다.

**채점·점검 기준:** 부품 역할과 병목을 연결하고 역사 수치를 현재 사양으로 바꾸지 않는다.

</details>

#### 확인 Q03 · 분산 용량과 통신 비용

Cloud server·rack·datacenter·CDN의 역할을 연결하라. GPU memory를 여러 machine으로 나누면 무엇을 얻고 어떤 비용을 고려해야 하는가? 2026 지출 전망은 어떻게 읽어야 하는가?

<details><summary>해설 보기</summary>

Server는 client의 저장·메시지·계산 요청을 처리하고 rack과 datacenter는 이를 수용·연결한다. CDN은 지역별 콘텐츠 사본으로 먼 origin 의존을 줄인다. 분산 memory는 총 용량을 늘리지만 중간 결과 교환 때문에 network bandwidth·latency·작업 배치가 중요해진다. HBM은 계산에 데이터를 빠르게 공급한다. 지출 수치는 미래형 전망이며 확정 실적이 아니고, 한 machine의 1 PB HBM이 어렵다는 말도 당시 비용·구성의 맥락이다.

**채점·점검 기준:** 용량 증가만 쓰지 말고 통신 비용·CDN 배치·전망의 한정을 포함한다.

</details>

#### 확인 Q04 · C와 abstraction

BCPL→B→C 흐름에서 C의 type·byte 접근이 의미하는 바를 설명하고 structured programming과 OOP를 비교하라. C89/C90·C99·C23 언급을 어떻게 구분하는가?

<details><summary>해설 보기</summary>

강의의 단순화된 역사에서 B의 word 중심 표현에 비해 C는 type과 byte 접근으로 낮은 수준 제어를 더 명확히 표현한다. Structured programming은 작업을 함수와 호출 관계로 나누고 OOP는 상태와 이를 다루는 interface를 묶는다. 둘 다 복잡도를 줄이는 abstraction이며 assembly에도 subroutine이 있다. ANSI C89와 ISO C90은 관련 표준 이름이고 wrapper는 C99를 선택한다. C23의 언급은 C99 바로 다음 표준이라는 주장이 아니다.

**채점·점검 기준:** 작업 분해와 상태·interface 결합을 구분하고 C99 설정을 식별한다.

</details>

#### 확인 Q05 · 설치·접속·복사의 역할

`wsl --install`, `wsl`, `uname -r`, `lsb_release -a`의 역할을 설명하라. `scp -P 2222 -r assignment1/ USER@HOST:~/`의 방향과 각 option은? SSH와 SCP는 어떻게 다른가?

<details><summary>해설 보기</summary>

설치, Linux shell 진입, kernel release 확인, distribution 정보 확인이다. 제시된 SCP는 local directory를 remote home으로 보내며 첫 operand가 source, 둘째가 destination이다. `-P`는 port, `-r`은 directory 재귀 복사다. Remote 경로를 첫 operand로 바꾸면 내려받는 방향이 된다. SSH는 인증·암호화된 remote shell이고 port option은 `-p`다. `USER`·`HOST`는 역할 placeholder이며 접속 성공이나 현재 endpoint를 뜻하지 않는다.

**채점·점검 기준:** 명령별 역할, 대소문자 option, source/destination을 정확히 구분한다.

</details>

#### 확인 Q06 · 어느 파일을 편집하는가

Remote SSH 확장으로 원격 파일을 여는 순서를 설명하라. Local 파일을 고친 경우와 무엇이 다른가? 평가 환경 재검증과 `man`·debugger·source 탐색 도구의 역할도 설명하라.

<details><summary>해설 보기</summary>

확장 설치→host/user/port 설정→접속→원격 파일 열기·편집 순서다. Local 창에 보여도 remote 파일과 remote terminal의 build가 바뀐다. Local 사본만 고쳤다면 복사 후 remote의 실제 파일·build를 확인해야 한다. OS·compiler·header·library 차이 때문에 local 성공이 평가 환경 성공을 보장하지 않는다. `man`은 계약, compiler는 번역·진단, debugger는 실행 상태, ctags/cscope는 source 탐색, source management는 변경 이력, trace 도구는 실행 상호작용을 돕는다.

**채점·점검 기준:** 창 위치와 파일 위치를 구분하고 재검증 이유를 구체적으로 든다.

</details>

#### 확인 Q07 · Build 단계와 wrapper

`hello.c`에서 executable까지 네 단계·결과와 `-E/-S/-c/-o`를 연결하라. Header가 있는데 link가 필요한 이유, wrapper의 네 진단 option·`"$@"`, 실행 권한·`PATH`의 차이는?

<details><summary>해설 보기</summary>

Preprocessing은 include·macro·comment를 처리해 `.i`, compilation은 assembly `.s`, assembly는 machine-code object `.o`, linking은 외부 definition을 연결한 executable을 만든다. `-E`는 전처리까지, `-S`는 assembly text까지, `-c`는 object까지, `-o`는 결과 이름 지정이다. Header declaration은 구현 기계어가 아니다. `-Wall`은 warning 묶음, `-Werror`는 warning을 error로, `-pedantic`은 표준 관련 진단, `-std=c99`는 언어 선택이며 `"$@"`는 인자 경계를 보존해 전달한다. 저장→`chmod +x`→`PATH` 검색 위치 배치는 별개 조건이다. 현재 directory가 `PATH`에 없으면 `./gcc800`처럼 경로가 필요하다. 진단 통과도 논리적 정답 보증은 아니다.

**채점·점검 기준:** 네 단계·option 전체와 declaration/definition, 실행 권한/검색 경로의 차이를 포함한다.

</details>

#### 확인 Q08 · 이름과 주소의 연결

`main.o`가 `UND swap`을 표시하고 다른 object가 `swap`을 정의한다. Symbol resolution과 relocation을 구별하고 separate compilation의 이점 및 local linker symbol의 뜻을 설명하라.

<details><summary>해설 보기</summary>

`UND`는 현재 object에 definition이 없다는 뜻이다. Resolution은 reference와 definition을 연결하고 relocation은 최종 section 배치에 맞게 주소 의존 reference를 조정한다. 한 source만 바뀌면 그 object를 다시 만들고 relink할 수 있다. `.o`는 연결 입력, executable은 실행용 결과, `.so`는 shared object다. Module의 `static` symbol은 그 module에 한정된 linker symbol이며 function automatic local variable과 같은 개념이 아니다.

**채점·점검 기준:** Resolution과 relocation을 각각 설명하고 `UND`를 compile 실패로 단정하지 않는다.

</details>

#### 확인 Q09 · 온도 표의 정확한 trace

Fahrenheit를 0부터 300까지 20씩 바꾸는 표의 식·행 수·종료 상태를 계산하라. 32°F가 출력되는가? `5/9` 오류와 좋은 이름·comment·재현 정보의 효과를 설명하라.

<details><summary>해설 보기</summary>

식은 `(5.0/9.0)*(fahr-32.0)`이다. `0,20,…,300`은 16행이고 마지막 출력 뒤 320에서 조건이 거짓이다. 32°F→0°C는 별도 식 점검이며 실제 loop에 32는 없다. 정수 `5/9`는 0이므로 비율을 잃는다. `fahr/celsius/lower/upper/step`은 단위·범위·증가량을 드러내며 comment는 caller의 목적·계약을 설명한다. Debugging에는 입력, 증상, 기대 결과와 compiler 진단을 함께 기록한다.

**채점·점검 기준:** 16행·320·32 미포함과 정수 나눗셈 원인을 모두 확인한다.

</details>

#### 확인 Q10 · 값·부수 효과·operator

`i=j=0`의 저장값과 식의 값을 설명하고 `=`/`==`, `%`, `&&`/`&`, `+=`를 구분하고 나머지 주요 operator 종류도 분류하라. `void f(void)`일 때 `f()`는 expression인가, `int n=f();`는 가능한가?

<details><summary>해설 보기</summary>

오른쪽 결합으로 두 변수와 식의 값은 모두 0이다. 결합 방향이 임의 operand 평가 순서를 뜻하지는 않는다. `=`는 대입·상태 변경, `==`는 같음 검사, `%`는 정수 나머지, `&&`는 논리 결합, `&`는 bit 연산, `+=`는 기존 값 갱신이다. 그 밖에 산술 `+`, `-`, `*`, `/`, unary `-`; 논리 `||`, `!`; 비교 `!=`, `<`, `>`, `<=`, `>=`; bitwise `<<`, `>>`, `|`, `^`; compound `*=`가 있다. `f()`는 값 없는 void expression이므로 `f();`는 statement로 가능하지만 정수 초기값을 요구하는 `int n=f();`는 불가능하다.

**채점·점검 기준:** 값·상태 변화·void의 값 없음과 operator 종류를 분리한다.

</details>

#### 확인 Q11 · 분기·반복·함수

본문의 `if (i<0)`와 `switch`의 `case 1`, `case 2`, `default`를 `i=-1`·`i=2`로 추적하라. `for (int i=0;i<10;i++)`의 body·검사 횟수, `while`/`do-while`, `break`/`continue`, 공통 error label, `add(3,5)`의 의미도 설명하라.

<details><summary>해설 보기</summary>

`-1`은 if의 참 분기, switch의 default이고 `2`는 if의 거짓 분기, switch의 case 2다. 각 case의 `break`가 없으면 fall-through할 수 있다. Body가 i를 바꾸거나 탈출하지 않으면 초기화 한 번→검사→body→증가→재검사로 body 10회·검사 11회이며 마지막 검사는 i=10이다. 처음 거짓인 `while`은 0회, `do-while`은 1회다. `break`는 해당 loop/switch를 끝내고 `continue`는 다음 반복으로 가며 for의 증가식을 거친다. 공통 error label은 여러 실패 경로의 처리를 모으되 확보한 자원을 구분해야 한다. `return x+y`인 add의 호출 결과는 8이고 정의와 호출은 다르다. Braces는 statement를 묶고 comment는 실행되지 않는다.

**채점·점검 기준:** 분기 두 경우, 10/11회, for의 continue 증가식, 함수 결과를 확인한다.

</details>

### 적용과 점검

#### 연습 P01 · 두 종류의 build 실패 구별

**새로 만든 합성 연습.** [EX:sp_2025_2_midterm_q05 p.12] Q5(a)의 symbol resolution/relocation 구별을 오류 진단에 적용한다. 선수는 본문의 build·separate compilation·remote 파일 구별이며 PLT/GOT와 재배치 byte 계산은 제외한다.

Local에서 `helper.c`를 수정했지만 remote에는 이전 사본이 있다. Remote `main.o`는 `UND helper`이고 `helper.o` 없이 link하여 unresolved-symbol 오류가 난다. (a) Header를 다시 include하면 해결되는가? (b) Object를 추가해 link가 성공해도 수정 효과가 없을 수 있는 이유는? (c) 각 단계에서 확인할 것을 제시하라.

<details><summary>해설 보기</summary>

(a) 아니다. Declaration은 definition의 machine code를 제공하지 않으므로 올바른 정의를 가진 object/library가 필요하다. (b) Remote의 오래된 source/object를 연결했을 수 있다. Link 성공은 의도한 source version 사용을 보증하지 않는다. (c) Local 수정 내용과 remote 파일 일치→remote 재compile→정의를 가진 object 포함→reference resolution 및 배치에 맞는 relocation→기대한 동작 확인 순으로 점검한다. 주소를 맞추는 relocation만으로 없는 symbol definition을 만들 수 없다.

**채점·점검 기준:** 누락된 definition, stale remote 사본, link 성공과 동작 확인의 차이를 각각 설명한다.

</details>

### 복습 순서

Q07–Q08을 보지 않고 build 흐름으로 그린 뒤 P01의 실패 원인을 단계별로 분류하라. Q09–Q11은 표에 저장값·출력·조건 검사 횟수를 적어 검산하고, Q05–Q06으로 실제 작업 파일의 위치를 말해 보라.

## 출처

[[courses/system_programming/lectures/2026-09-02-lecture-01|2026-09-02 · 강의 노트]]

[[courses/system_programming/lectures/2026-09-07-lecture-02|2026-09-07 · 강의 노트]]

[[courses/system_programming/lectures/2026-09-09-lecture-03|2026-09-09 · 강의 노트]]

[[courses/system_programming/lectures/2026-09-23-lecture-06|2026-09-23 · 강의 노트]]

[01.CProgrammingExamples.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/01.CProgrammingExamples.pptx) — slides 17, 21–27

[00.Introduction.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx) — slide 30; PDF p.35 / slide 35 (section agenda); PDF p.36 / slide 36 (hardware figure and specifications); PDF p.36 / slide 36; PDF p.37 / slide 37; PDF p.38 / slide 38; slide 46; slide 50; slide 15; slide 63; slide 59; slide 60; slide 56; slide 57

[[courses/system_programming/transcripts/2026-09-02|2026-09-02 · 보정 STT]] — 43:28, 47:03, 11:07, 53:45, 50:58, 01:39:14, 01:42:07

[[courses/system_programming/transcripts/2026-09-07|2026-09-07 · 보정 STT]] — 34:43, 44:11

[[courses/system_programming/transcripts/2026-09-09|2026-09-09 · 보정 STT]] — 01:03:10, 01:31:06, 01:32:03

[10.RE.Life.Cycle.of.a.Program.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/10.RE.Life.Cycle.of.a.Program.pptx) — slide6; slide14

[11.RE.Linking.and.Loading.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/11.RE.Linking.and.Loading.pptx) — slide5

Lab0와 공식 Assignment 2 README 원본은 비공개이며 계정·password는 포함하지 않는다. Hostname 표기 충돌과 불확실한 UI·API 발화는 해결된 것으로 보지 않는다. 9월 23일 노트의 ARM Mac 안내 및 Life Cycle/Linking slides는 자료 기반 보충이며 해당 deck 전체의 강의를 뜻하지 않는다. Hardware 수치와 지출 전망은 당시 설명이다. 원자료의 중복 `=`·빠진 do-while semicolon·오래된 implicit declaration 및 2025-2 Q5 뒷부분의 byte 개수·호출 표기 불일치는 수정된 원문으로 간주하지 않는다. STT에는 불확실한 발화와 가림 구간이 남아 있다.

아래 과거 시험 연결은 명시한 추론 요구에 한정한다. 제공 답안은 참고자료이며 독립 검증된 정답으로 간주하지 않고, 현재 시험 범위나 출제 빈도를 추정하지 않는다.
