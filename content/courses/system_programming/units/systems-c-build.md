---
title: "System Programming과 C 프로그램의 구성·빌드"
description: "C의 실행 흐름, 개발 환경과 build 단계를 함께 복습한다."
course: "system_programming"
unit_id: "systems-c-build"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["01.CProgrammingExamples.pptx", "00.Introduction.pptx", "lab 0 setup.pdf", "assign2_README.md"]
private_source_assets: ["lab 0 setup.pdf", "assign2_README.md"]
source_lectures: ["courses/system_programming/lectures/2026-09-02-lecture-01", "courses/system_programming/lectures/2026-09-07-lecture-02", "courses/system_programming/lectures/2026-09-09-lecture-03", "courses/system_programming/lectures/2026-09-23-lecture-06"]
---

C 프로그램의 상태 변화와 executable 생성 과정을 연결한다. 환경·도구·OS의 역할을 나눠 실패한 단계를 설명해 보자.

## System Programming(시스템 프로그래밍): OS와 협력하는 프로그램

파일을 읽는 프로그램은 저장장치를 직접 움직이는 대신 OS(운영체제)에 서비스를 요청한다. 프로그램은 어떤 데이터를 어떻게 처리할지 정하고, kernel(커널)은 접근 권한과 장치를 관리한다. 이 경계에서 파일·메모리·프로세스를 정확하게 사용하는 것이 System Programming의 출발점이다. [[courses/system_programming/transcripts/2026-09-02|2026-09-02 STT 43:28]]에서도 이미 존재하는 OS와 상호작용하는 관점으로 설명했다.

C는 주소와 byte 단위 데이터를 다루면서도 assembly(어셈블리)의 개별 instruction보다 큰 단위로 계산을 표현한다. Linux는 공개된 구현과 Unix 계열의 도구 환경을 제공한다. 그래서 C와 Linux를 함께 배우면 프로그램의 의도가 machine의 작업으로 바뀌는 경로를 살펴보기 좋다. 다만 C라는 이유만으로 항상 빠르거나 다른 언어가 부적절한 것은 아니다. 낮은 수준의 제어를 얻을수록 object의 수명, 잘못된 주소, OS별 API 차이를 직접 확인할 책임도 커진다. Process, exception, shell, network, concurrency는 이 관점에서 이어질 주제다. [Introduction slides 27–31](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx)

### CPU·memory·network가 함께 정하는 실행 비용

CPU는 계산하고, memory는 계산할 데이터와 instruction을 보관하며, network는 다른 machine과 데이터를 교환한다. Multicore(다중 코어)는 한 CPU chip 안에 여러 실행 core를 두는 구성이다. 독립 작업을 나눌 수 있어야 여러 core가 도움이 되므로 core 수가 두 배라는 사실만으로 모든 프로그램이 두 배 빨라지지는 않는다.

Introduction slide 36의 mainboard 사진에서는 CPU socket과 길쭉한 memory slot을 구분해 보면 된다. 오른쪽의 4–60 cores, 10–100-Gigabit Ethernet은 강의의 hardware 구성 예시다. [[courses/system_programming/transcripts/2026-09-02|2026-09-02 STT 47:03]]의 잠정적인 부품 식별을 GPU 확정 정보로 읽지는 않는다. Laptop의 4·8 cores, server의 16개 이상, PC의 약 1 Gbit/s 같은 강의 수치도 당시 환경을 설명한다.

Slides 37–38은 ENIAC(1946), mainframe과 Apollo 11(1969), smartphone으로 이어지는 소형화의 흐름과 자동차·시계의 변화를 보여 준다. 사진에서 볼 핵심은 장치의 크기와 사용 장소의 변화다. “수백만 배”라는 문구는 같은 작업을 측정한 benchmark 결과가 아니다. Ubiquitous computing(편재형 컴퓨팅)은 자동차, 시계, speaker, 반려동물용 기기까지 계산 기능이 들어가면서 software의 대상이 넓어진다는 뜻이다. [Introduction slides 36–38](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx)

### Cloud와 CDN에서 커지는 데이터 이동의 중요성

Cloud server(클라우드 서버)는 여러 client의 저장·메시지·계산 요청을 처리한다. Rack은 server 여러 대를 수용하는 구조이고 datacenter는 이들을 대규모로 연결한다. CDN(Content Distribution Network, 콘텐츠 분산 네트워크)은 콘텐츠 사본을 여러 지역에 배치한다. 멀리 있는 원 서버에서 매번 가져오는 부담을 줄이는 방식이며, 모든 browser가 물리적 최단거리만 계산해서 서버를 고른다는 뜻은 아니다. [[courses/system_programming/transcripts/2026-09-02|2026-09-02 STT 11:07]]

강의의 Meta 수십만 대, Microsoft 약 400만 대(2021), Google 약 250만 대(2016)는 규모를 이해하기 위한 날짜가 붙은 사례다. 2026년 hyperscaler 지출 600 billion dollars 초과는 [[courses/system_programming/transcripts/2026-09-02|2026-09-02 STT 50:58]]에서 전망으로 말했으며, 확정 지출 실적으로 바꾸어 읽으면 안 된다. 1 billion dollars를 약 1.4조 원으로 설명한 환산도 그때의 설명이다.

AI training과 inference는 HBM(High-Bandwidth Memory, 고대역폭 메모리)에 대한 수요를 만든다. 필요한 데이터를 한 GPU에 모두 두기 어려워 여러 machine에 나누면 이제 계산 중간 결과가 network를 건너야 한다. 총 memory 용량을 늘려도 bandwidth(전송 용량)와 latency(전달 지연)가 새 병목이 될 수 있다. [[courses/system_programming/transcripts/2026-09-02|2026-09-02 STT 53:45]]의 요지는 software 요구가 memory·반도체·SoC와 network 구성에 영향을 준다는 것이다. 한 machine의 HBM 용량에 관한 당시의 비용 설명을 영구적인 물리 한계로 일반화하지 않는다.

## C의 추상화와 프로그램의 상태 변화

BCPL→B→C의 계보와 Unix의 발전은 낮은 수준의 제어를 더 표현력 있게 쓰려는 흐름을 보여 준다. B의 word 중심 표현에 비해 C는 type과 byte 수준 접근을 표현한다. 강의는 Multics에서 Unix로 이어지는 역사, K&R C, ANSI C89/ISO C90, C99를 소개한다. 이 과목의 build option은 C99를 선택한다. C23의 언급이 C99 바로 다음에 나온 표준이라는 뜻은 아니다. [Introduction slides 45–50](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx)

Structured programming(구조적 프로그래밍)은 작업을 작은 함수와 호출 관계로 분해한다. Object-oriented programming(객체 지향 프로그래밍)은 함께 유지할 상태와 그것을 다루는 interface를 object로 묶는다. 둘은 복잡도를 줄이는 조직 방식이며 완전히 배타적이지 않다. Assembly에도 subroutine을 만들 수 있다. 여기서 중요한 차이는 높은 수준의 언어가 큰 프로그램의 구조를 표현하기 쉽게 해 준다는 점이다.

### Expression과 statement는 무엇을 바꾸는가

프로그램을 현재 상태와 그 상태를 바꾸는 동작으로 생각해 보자. Expression(표현식)은 평가되는 구문이다. `2 + 3`의 값은 5이고 literal `2`의 값은 2다. `i = 10`은 `i`의 저장값을 바꾸는 side effect(부수 효과)를 갖는 동시에 값 10을 갖는다. 뒤에 `;`를 붙인 `i = 10;`은 expression statement가 된다. [[courses/system_programming/transcripts/2026-09-02|2026-09-02 STT 01:39:14]]

`i = j = 0`은 `i = (j = 0)`으로 결합한다. `j`에 저장한 0을 `i`에도 저장하므로 두 변수와 전체 식의 값이 모두 0이다. 이것은 assignment의 결합 규칙이지 모든 operand의 실행 순서를 정하는 규칙은 아니다. `=`는 저장하고 `==`는 같은지를 검사한다.

| 연산의 목적 | 연산자 | 읽는 방법 |
|---|---|---|
| Arithmetic(산술) | `+ - * / %`, unary `-` | 값을 계산하며 `%`는 정수 나눗셈의 나머지 |
| Logical(논리) | `&& \|\| !` | 참·거짓 조건을 결합하거나 반전 |
| Relational(관계) | `== != < > <= >=` | 두 값의 관계를 검사 |
| Bitwise(비트 단위) | `<< >> & \| ^` | bit 이동 또는 bit별 연산 |
| Compound assignment(복합 대입) | `+= -= *= /= %= <<= >>= ^= \|=` | 기존 값을 계산해 갱신 |

이 표는 역할을 정리한 것이다. Slide 55의 assignment 목록에는 `=`가 중복되어 있으므로 누락 기호를 원문에 있었다고 가정하지 않는다. 또 “expression은 값을 만든다”에는 한정이 필요하다. `void` 함수의 호출도 expression이지만 값은 없다. `f`가 `void`를 반환할 때 `f();`는 가능하지만 `int n = f();`는 존재하지 않는 결과값을 요구한다.

### Branch·loop·function을 순서대로 따라가기

`if (i < 0)`는 음수 여부로 분기하고 `switch (i)`는 해당 `case`로 진입한다. Slide 56의 두 예를 비교하면 `i=-1`은 `if`의 첫 statement와 `switch`의 `default`로 간다. `i=2`는 `if`의 `else`와 `case 2`로 간다. `switch`의 `break`를 만나면 빠져나오며, 생략하면 다음 case 쪽으로 흐를 수 있다.

`for (int i = 0; i < 10; i++)`의 순서는 초기화 한 번 → 조건 검사 → body → 증가식 → 재검사다. Body가 `i`를 변경하지 않고 조기 탈출하지 않으면 `i=0`부터 9까지 body를 10번 실행하고, `i=10`에서 실패하는 검사까지 조건은 11번 확인한다. `while`은 먼저 검사하므로 처음부터 거짓이면 0번, `do-while`은 body부터 실행하므로 1번이다. 올바른 C 문법은 `do { ... } while (condition);`처럼 마지막 semicolon을 포함한다.

`break`는 가장 가까운 해당 loop 또는 switch를 끝낸다. `continue`는 현재 반복의 나머지를 건너뛰며 `for`에서는 증가식을 거쳐 다음 검사를 한다. `goto label;`은 지정 위치로 이동한다. [[courses/system_programming/transcripts/2026-09-02|2026-09-02 STT 01:42:07]]은 여러 실패 경로를 공통 error label로 모으는 사용을 설명했다. 이때 어느 자원을 이미 확보했는지는 경로마다 확인해야 한다.

함수 정의와 호출도 구분하자. 다음은 slide 60의 계산이다.

```c
int add(int x, int y)
{
    return x + y;
}
/* Inside a calling function: */
int sum = add(3, 5);
```

호출은 인자 3과 5로 계산하여 8을 반환한다. `{ }`는 여러 statement를 묶고 `/* ... */`와 `//`는 독자를 위한 comment이다.

## Fahrenheit–Celsius 계산을 읽기 쉬운 프로그램으로 만들기

온도 변환은 상태·조건·반복을 한 번에 연결한다. 다음은 slide 63의 예를 C의 일반 따옴표와 연산자로 정리한 코드다.

```c
#include <stdio.h>

/* Print a Fahrenheit-Celsius table for 0, 20, ..., 300. */
int main(void)
{
    float fahr, celsius;
    int lower = 0, upper = 300, step = 20;

    for (fahr = lower; fahr <= upper; fahr = fahr + step) {
        celsius = (5.0 / 9.0) * (fahr - 32.0);
        printf("%3.0f %6.1f\n", fahr, celsius);
    }
    return 0;
}
```

`fahr`는 0에서 300까지 20씩 증가하므로 16행을 출력한다. 예를 들어 첫 행의 섭씨 값은 (5.0/9.0) × (−32) ≈ −17.8이다. 변환식 자체에 32°F를 넣으면 0°C가 되지만 32는 이 표의 20 간격 행에는 없다. `5.0 / 9.0` 대신 정수 식 `5 / 9`를 쓰면 결과가 0이 되어 변환 비율을 잃는다. `%3.0f`는 소수점 아래 없이, `%6.1f`는 한 자리까지 출력한다.

같은 식을 `a,b,c,d,e`로 쓸 수도 있지만 `fahr,celsius,lower,upper,step`은 단위와 역할을 드러낸다. Function comment는 줄마다 코드를 번역하기보다 caller가 기대할 동작을 설명해야 한다. 작은 함수, 명확한 이름, 입력·기대 결과·실제 증상을 정리한 debugging이 서로 연결되는 이유다. 강의의 주당 7–10시간 조언은 계획의 참고이지 사람마다 같은 시간이 필요하다는 법칙은 아니다. [Introduction slides 62–63](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx), [C examples slides 17–19](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/01.CProgrammingExamples.pptx)

## Source code에서 executable까지

`#include <stdio.h>`는 `printf`의 선언 등 header 내용을 처리하게 한다. 선언을 아는 것과 실제 구현을 executable에 연결하는 것은 다르다. 간단한 `hello.c`도 다음 단계를 거친다.

| 단계 | 결과 예 | 해결하는 일 |
|---|---|---|
| Preprocessing(전처리) | `hello.i` | include·macro 처리, comment 제거 |
| Compilation(컴파일) | `hello.s` | C를 target assembly로 변환 |
| Assembly(어셈블) | `hello.o` | machine-code object 생성 |
| Linking(연결) | `hello` | object와 library의 외부 참조를 연결 |

`hello.o`에 `printf` 호출이 있어도 그 구현이 아직 해결되지 않을 수 있다. Slides 21–26의 `libc.a`는 library 구현과 object를 연결하는 관계를 보여 주며 모든 실제 build가 static linking이라는 뜻은 아니다. [[courses/system_programming/transcripts/2026-09-07|2026-09-07 STT 34:43]]

```sh
gcc800 -E hello.c > hello.i
gcc800 -S hello.i
gcc800 -c hello.s
gcc800 hello.o -lc -o hello
gcc800 hello.c -o hello
```

앞 네 줄은 단계를 나누어 관찰하고 마지막 줄은 전체 build를 요청한다. `-o hello`는 출력 이름을 정하며 생략한 예의 기본 이름은 `a.out`이다. [C examples slides 20–27](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/01.CProgrammingExamples.pptx)

이 연결을 더 정확히 설명하려면 외부 이름이 어느 정의를 뜻하는지 찾는 symbol resolution(심볼 해석)과 최종 배치에 맞게 주소 참조를 조정하는 relocation(재배치)을 구분할 수 있다. 기출 Q5(a)가 요구하는 것도 이 두 책임을 구별하는 설명이다. 이는 기본 build 흐름에 덧붙이는 심화 연결이며 archive 탐색 순서나 PLT/GOT 구현까지 이 단원에서 배웠다는 뜻은 아니다. [EX:sp_2025_2_midterm_q05 p.12]

### gcc800의 진단과 shell의 명령 검색

자료의 `gcc800`은 다음 명령을 실행하는 wrapper다.

```sh
gcc -Wall -Werror -pedantic -std=c99 "$@"
```

`-Wall`은 흔한 warning 묶음을 켜고, `-Werror`는 warning을 error로 처리한다. `-pedantic`은 선택 표준에 관한 진단을 요구하며 `-std=c99`는 언어 기준을 C99로 정한다. `-Wall`이 가능한 모든 warning을 뜻하거나 이 옵션들만으로 논리적 정답이 증명되지는 않는다. `"$@"`는 source 파일명과 `-o` 같은 호출 인자를 전달한다.

Text wrapper를 저장하는 것, 실행 권한을 갖는 것, shell이 이름으로 찾는 것은 별개다. 자료는 `chmod +x gcc800`과 `PATH`에 포함되는 위치에 두는 과정을 설명한다. 현재 directory가 `PATH`에 없다면 `./gcc800`처럼 경로를 써야 한다. [[courses/system_programming/transcripts/2026-09-07|2026-09-07 STT 44:11]]

## Local 개발 환경과 remote 실행 환경

프로그램은 compiler·header·library·OS의 조합에서 실행된다. Local machine에서 성공해도 평가 환경에서 같은 build와 동작이 보장되지는 않는다. Lab 0은 Ubuntu, Linux VM, WSL을 소개하고 local에서 작성한 뒤 Bacchus 환경에서 검증하도록 안내한다. 이후 Assignment 2의 platform 안내도 ARM Mac에서 작성할 수는 있지만 Linux와의 header·API 차이를 확인하도록 한다. 후자의 안내는 handout 보충이다.

자료의 Windows 절차는 관리자 command prompt에서 `wsl --install`로 설치하고, Ubuntu 또는 `wsl`로 Linux shell을 여는 순서다. `uname -r`은 kernel release, `lsb_release -a`는 distribution 정보를 확인한다. 서로 다른 층의 버전이다. 아래는 계정과 host를 placeholder로 바꾼 강의 명령 예시다.

```sh
ssh -p 2222 USER@HOST
scp -P 2222 -r assignment1/ USER@HOST:~/
scp -P 2222 -r USER@HOST:~/assignment1/ ./
```

SSH(Secure Shell)는 암호화·인증된 remote shell 연결이고 SCP는 파일 복사다. SSH의 port option은 소문자 `-p`, SCP는 대문자 `-P`이며 `-r`은 directory 복사에 쓰인다. 두 SCP 줄은 각각 local→remote, remote→local 방향이다. 22·2222는 당시 lab 안내 값이지 현재 endpoint 검증 결과는 아니다.

Remote SSH로 작업하면 화면은 local에 있어도 열린 파일과 terminal의 build 위치는 remote machine이다. 확장을 설치하고 host·user·port를 설정해 접속한 뒤 원격 파일을 여는 흐름을 [[courses/system_programming/transcripts/2026-09-09|2026-09-09 STT 01:31:06–01:32:03]]에서 설명한다. 반대로 local 파일을 편집했다면 별도로 복사해야 한다.

`man strstr` 같은 manual 조회는 함수 계약을 찾고, compiler는 번역·진단, debugger는 실행 상태 관찰, ctags/cscope는 code 탐색, source management는 변경 기록, trace 도구는 실제 호출 관찰을 돕는다. 환경을 연결했다는 사실과 프로그램이 맞다는 사실은 별개다. 이제 저장된 값과 주소가 어떻게 달라지는지 [[courses/system_programming/units/objects-pointers|C object와 pointer]]에서 구체화할 수 있다.

## 핵심 정리

- Application·compiler·kernel의 책임을 구별한다.
- 이름과 단위로 계산·반복 경계를 검산한다.
- Build 성공과 실행 정답성은 별도로 확인한다.
- 다음은 [[courses/system_programming/units/objects-pointers|object와 pointer]]다.

## 확인·연습문제

### 개념 확인과 추론

#### 확인 Q01 · OS의 역할

파일을 읽는 application과 kernel의 책임, C·Linux를 선택하는 이유를 설명하라.

<details><summary>해설 보기</summary>

Application은 파일·알고리즘을 정해 API를 호출하고 kernel은 권한·장치 서비스를 제공한다. C는 주소와 낮은 수준 I/O를 표현하며 Linux는 공개 구현과 Unix 도구를 제공한다. Kernel 자체 구현이나 C의 보편적 성능 우위를 뜻하지 않는다. 소개된 향후 network·concurrency를 현재 완료 진도로 세지 않는다.

**채점·확인:** 요청·서비스·선택 이유와 한계를 구별한다.

</details>

#### 확인 Q02 · 구성요소와 병목

CPU socket·memory slot·network의 역할과 core 증가의 한계를 설명하라. 역사·생활 속 computing 사례는 무엇을 보여 주는가?

<details><summary>해설 보기</summary>

Socket의 CPU는 명령을 실행하고 slot의 memory는 작업 데이터를 보유하며 network는 machine 간 데이터를 옮긴다. 병렬 작업이 적거나 memory·통신 대기가 크면 core나 bandwidth가 두 배여도 전체가 두 배 빨라지지 않는다. ENIAC(1946), Apollo·mainframe(1969), smartphone과 자동차·시계 사례는 computing의 확산이다. 당시 수치는 현재 사양이 아니며 불명확한 GPU 발언은 확정하지 않는다.

**채점·확인:** 세 역할과 speedup 반례를 제시한다.

</details>

#### 확인 Q03 · Cloud와 HBM

Server·rack·datacenter·CDN을 연결하고, HBM 용량을 여러 machine으로 나눌 때 생기는 비용을 설명하라.

<details><summary>해설 보기</summary>

Server는 rack·datacenter로 조직된다. CDN은 content 사본을 여러 위치에 두지만 browser가 항상 물리적으로 가장 가까운 서버를 직접 선택한다는 규칙은 아니다. AI의 bandwidth 요구는 HBM 수요와 연결된다. 분산하면 총용량뿐 아니라 데이터 교환 bandwidth·latency·작업 배치가 중요하다. 강의의 server 수와 2026년 600 billion dollar 지출은 당시 수치·전망이지 확정 실적이 아니다.

**채점·확인:** 용량과 통신 비용, 전망과 실적을 구별한다.

</details>

#### 확인 Q04 · C와 abstraction

BCPL·B·C, K&R, C89·C90·C99의 관계와 함수/객체 중심 조직의 차이는?

<details><summary>해설 보기</summary>

C는 BCPL·B의 계보에서 발전했고 K&R은 초기 기술이다. ANSI C89·ISO C90은 표준화 흐름이고 도구는 C99를 선택한다. C23을 C99의 바로 다음 판이라고 해석하지 않는다. 함수는 작업·호출을, object는 함께 유지되는 상태·interface를 중심으로 조직한다. 둘은 병용할 수 있고 assembly에도 subroutine이 있다.

**채점·확인:** 역사·선택 표준·두 조직 관점을 구분한다.

</details>

#### 확인 Q05 · Local과 remote

WSL 설치·진입·정보 명령, SSH/SCP와 port option, 양방향 복사, Remote SSH 저장 위치를 설명하라. 왜 lab에서 재검증하며 어떤 도구를 쓰는가?

<details><summary>해설 보기</summary>

`wsl --install`은 설치, Ubuntu/`wsl`은 진입, `uname -r`은 kernel, `lsb_release -a`는 distribution 정보다. SSH는 인증·암호화된 shell이며 `-p`, SCP는 복사이며 `-P`·재귀 `-r`을 쓴다. `scp -P 2222 -r assignment1/ USER@HOST:~/`는 local→remote이고 source/destination을 뒤집으면 반대다. 당시 예시이며 현재 endpoint 검증은 아니다. Remote SSH extension에서 host 설정·접속·폴더 열기 후 저장하면 remote 파일이 바뀐다. Local 편집은 복사가 필요하다. OS·compiler·header·library 차이 때문에 lab에서 build·실행한다. `man strstr`은 API, debugger는 실행 상태, ctags/cscope는 탐색, source management는 이력, trace는 실행 상호작용을 확인한다.

**채점·확인:** 명령 역할·대소문자 option·저장 위치·환경 차이를 확인한다.

</details>

#### 확인 Q06 · Build 단계

Source→executable의 단계·파일·옵션, header와 link의 관계, gcc800 옵션·권한·PATH를 설명하라.

<details><summary>해설 보기</summary>

Preprocessing은 include·macro·comment를 처리하여 `.i`(`-E`), compilation은 `.s`(`-S`), assembly는 `.o`(`-c`), linking은 외부 정의와 합쳐 executable을 만든다. `-o`는 출력 이름, 기본 executable은 `a.out`이다. 선언은 구현 code가 아니다. `-Wall`은 흔한 warning, `-Werror`는 warning을 error로, `-pedantic`은 표준 진단, `-std=c99`는 dialect 선택이며 정답성 증명은 아니다. Wrapper의 `"$@"`는 인자 경계를 보존한다. 저장, `chmod +x` 실행 권한, `PATH` 이름 검색은 별개이고 `./gcc800`은 경로를 명시한다. `libc.a` 그림이 모든 실행의 static linking을 뜻하지 않는다.

**채점·확인:** 네 단계와 옵션, 선언/정의, 권한/검색을 확인한다.

</details>

#### 확인 Q07 · 온도 표 검산

Fahrenheit 0..300 step 20의 행 수, 첫 Celsius 값, 32의 변환과 `5/9` 오류를 구하라. 이름·comment는 어떻게 돕는가?

<details><summary>해설 보기</summary>

`300/20+1=16`행이다. `(5.0/9.0)*(0-32)`는 약 −17.8, 32는 0°C지만 이 표의 행은 아니다. 정수 `5/9`는 0이 되어 계산을 망친다. 단위·범위·간격의 이름과 caller 관점 comment가 의도를 드러내므로 입력/예상/실제 비교가 쉬워진다. 강의의 공부 시간 조언은 고정 규정이 아니다.

**채점·확인:** 16, −17.8, 32의 행 부재, integer division을 확인한다.

</details>

#### 확인 Q08 · Expression과 statement

`i=j=0`, `=`/`==`, `void f(void)`의 `f();`/`int n=f();`를 설명하고 operator 범주를 구별하라.

<details><summary>해설 보기</summary>

오른쪽 결합으로 j와 i에 각각 0을 저장하고 전체 값도 0이다. 모든 operand 평가 순서를 정하는 것은 아니다. `=`는 저장, `==`는 비교다. `f()`는 값 없는 expression이므로 `f();`는 가능하지만 `int n=f();`는 invalid다. 산술·`%`, 관계 비교, logical `&& || !`, bitwise `& | ^ << >>`, compound assignment는 역할이 다르다.

**채점·확인:** 상태·값·void expression·operator 차이를 확인한다.

</details>

#### 확인 Q09 · 분기·반복 추적

`if(i<0)`와 case 1·2/default인 switch에 −1, 2를 넣어라. `for(i=0;i<10;i++)` 횟수, while/do-while, break/continue, error label과 `add(3,5)`를 설명하라.

<details><summary>해설 보기</summary>

−1은 if의 statement1·switch의 default statement3, 2는 둘 다 statement2다. 조기 종료·i 변경이 없으면 초기화 1회, body 10회, 검사 11회 후 i=10이다. 처음 거짓인 while은 0회, do-while은 1회이며 뒤 semicolon이 필요하다. `break`는 가장 가까운 loop/switch를 나가고 `continue`는 다음 반복 절차(for의 증가 포함)로 간다. 공통 error label은 cleanup을 모으되 확보한 resource를 구별해야 한다. `add(3,5)`는 인자를 전달해 8을 돌려받는다. Braces는 statement를 묶고 comment는 의도를 설명한다.

**채점·확인:** 분기 결과·10/11·cleanup 조건을 확인한다.

</details>

### 응용 연습

#### 연습 P01 · Link 실패 진단

**새로 만든 합성 연습.** Object A는 외부 함수를 호출하고 B는 정의한다. A만 link하면 정의가 없고 A·B를 합치면 배치 주소가 달라진다. 두 책임을 구별하고 header 재복사가 해결책인지 설명하라.

[EX:sp_2025_2_midterm_q05 p.12] Q5(a)의 linker 책임 구분을 실패 진단으로 옮긴 연습이다. 선행: Q06의 object·외부 이름. Archive·PLT/GOT·byte 계산은 제외한다.

<details><summary>해설 보기</summary>

Symbol resolution은 참조와 정의를 연결하고 relocation은 합친 배치에 맞춰 주소 의존 참조를 조정한다. Header는 구현을 공급하지 않으므로 정의 부족을 해결하지 않는다. B를 제공해도 배치 조정은 별도 필요하다.

**채점·확인:** 정의 연결과 주소 조정을 구별한다.

</details>

### 복습 계획

Q01–Q04를 역할·병목으로 설명하고 Q05–Q06을 환경→build 순서로 연결한다. Q07–Q09를 종이로 추적한 뒤 P01로 실패 단계를 분류한다.

## 출처

### 날짜별 강의 노트

- [[courses/system_programming/lectures/2026-09-02-lecture-01|2026-09-02 강의 노트]]
- [[courses/system_programming/lectures/2026-09-07-lecture-02|2026-09-07 강의 노트]]
- [[courses/system_programming/lectures/2026-09-09-lecture-03|2026-09-09 강의 노트]]
- [[courses/system_programming/lectures/2026-09-23-lecture-06|2026-09-23 연계 자료]]

### 수업자료와 강의 구간

- [Introduction slides 27–31](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx)
- [Introduction slides 36–38](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx)
- [Introduction slides 45–50](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx)
- [Introduction slides 62–63](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx)
- [C examples slides 17–19](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/01.CProgrammingExamples.pptx)
- [C examples slides 20–27](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/01.CProgrammingExamples.pptx)
- [[courses/system_programming/transcripts/2026-09-02|2026-09-02 STT 43:28]]
- [[courses/system_programming/transcripts/2026-09-02|2026-09-02 STT 47:03]]
- [[courses/system_programming/transcripts/2026-09-02|2026-09-02 STT 11:07]]
- [[courses/system_programming/transcripts/2026-09-02|2026-09-02 STT 50:58]]
- [[courses/system_programming/transcripts/2026-09-02|2026-09-02 STT 53:45]]
- [[courses/system_programming/transcripts/2026-09-02|2026-09-02 STT 01:39:14]]
- [[courses/system_programming/transcripts/2026-09-02|2026-09-02 STT 01:42:07]]
- [[courses/system_programming/transcripts/2026-09-07|2026-09-07 STT 34:43]]
- [[courses/system_programming/transcripts/2026-09-07|2026-09-07 STT 44:11]]
- [[courses/system_programming/transcripts/2026-09-09|2026-09-09 STT 01:31:06–01:32:03]]
- Lab 0 setup handout: 제공된 PDF에 공개 링크가 없다. ARM Mac 환경 안내는 자료에 근거한다.
- 9월 23일 Assignment 2 handout의 요구사항은 자료 보충으로 다룬다. 비공개 원문과 완성 구현의 공개 링크는 없다.

연결된 공개 자료는 slide deck이며, 이 자료들의 PDF 페이지 보기 링크는 제공되지 않았다. 녹취 시각은 일반 텍스트로 표시한다.

### 자료 범위와 한계

- Hardware·cloud 수치와 지출 전망은 당시 설명이며 현재 실측값이 아니다.
- ARM Mac 안내와 9월 23일 handout 보충은 자료 근거다. Endpoint 상충 표기와 불명확한 녹취는 미해결이다.
- 기출은 Q5(a)에 한정한다. 후속 쪽의 swap 선언/호출 불일치와 8-byte 칸의 9-byte 답안을 채택하지 않았으며 제공 답안을 정답 권위로 삼지 않는다.


---

[[courses/system_programming/units/index|단원 목차]] · [[courses/system_programming/units/objects-pointers|다음: C object·type·주소와 pointer →]]
