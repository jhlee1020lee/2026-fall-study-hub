---
title: "문자 처리와 DFA·Decommenter의 경계조건"
description: "DFA transition과 세 출력 관측값으로 문자 처리의 경계를 검토한다."
course: "system_programming"
unit_id: "state-machines"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["01.CProgrammingExamples.pptx", "00.Introduction.pptx", "lab-1-decommenter.pdf"]
private_source_assets: ["lab-1-decommenter.pdf"]
source_lectures: ["courses/system_programming/lectures/2026-09-02-lecture-01", "courses/system_programming/lectures/2026-09-07-lecture-02", "courses/system_programming/lectures/2026-09-09-lecture-03"]
---

문자 하나를 읽을 때 무엇을 기억해야 하는지 state로 표현한다. Word 경계와 comment·literal·EOF를 분리해 출력과 오류 계약을 검증한다.

## Character stream(문자 스트림): byte와 EOF를 구분하기

문자를 하나씩 읽는 프로그램은 큰 입력을 한꺼번에 저장하지 않고도 처리할 수 있다. 필요한 것은 현재 character와 다음 판단에 필요한 작은 상태다. [[courses/system_programming/units/systems-c-build|Expression과 loop]] 및 [[courses/system_programming/units/objects-pointers|C의 type과 string]]을 바탕으로 입력값, 종료 신호, 기억할 상태를 나누어 보자.

ASCII에서 `'0'`–`'9'`는 48–57, `'A'`–`'Z'`는 65–90, `'a'`–`'z'`는 97–122다. 따라서 자료의 `97`, `'a'+3`, `122`를 character로 출력하면 `a d z`가 된다. `'C'+'a'-'A'`는 `c`, `'c'-('a'-'A')`는 `C`다. 이 계산은 ASCII의 배치에 의존한다. 숫자 97보다 `'a'`가 의도를 잘 드러내지만 alphabet의 연속 범위를 손으로 검사하는 것도 character-set 가정을 남긴다. [C examples slides 3–10](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/01.CProgrammingExamples.pptx)

`isalpha`, `isdigit`, `isspace`는 library의 분류 규칙을 사용한다. 이 규칙은 locale의 영향도 받는다. `getchar`의 결과를 `int`에 저장하면 유효한 character 값과 별도 상태인 `EOF`를 구분할 수 있다. 먼저 `char`로 줄여 버리면 그 구분을 잃을 수 있다. `EOF`는 입력에 들어 있는 보통 byte 하나가 아니며 자료의 -1 표현을 모든 환경의 유일한 값으로 일반화하지 않는다.

```c
int c;
int alphaCount = 0, digitCount = 0, othersCount = 0;

while ((c = getchar()) != EOF) {
    if (isalpha(c))
        alphaCount++;
    else if (isdigit(c))
        digitCount++;
    else
        othersCount++;
}
```

이는 `<stdio.h>`와 `<ctype.h>`를 사용하는 자료의 분류 부분이다. 한 입력값마다 정확히 한 분기만 증가한다. 일반적인 `char` 변수를 `ctype` 함수에 넘길 때에는 `unsigned char`로 표현 가능한 범위 또는 `EOF`라는 인자 조건도 지켜야 한다. 위에서는 `getchar`의 반환값을 유지한 뒤 `EOF`를 제외했다.

제공된 `count.c` 입력의 출력 253 alphabets, 4 digits, 289 others는 그 파일의 결과다. Program의 이름이 같다고 편집한 source나 임의 입력에서도 그 수가 유지되지는 않는다.

## Word counting과 state transition(상태 전이)

단어 수를 세려면 character의 종류뿐 아니라 바로 앞까지 단어 안에 있었는지를 기억해야 한다. 이 예의 word는 사전적 단어가 아니라 연속된 non-whitespace character다. [[courses/system_programming/transcripts/2026-09-07|2026-09-07 STT 14:04]]도 이 정의를 명시하며 space, tab, newline 등을 `isspace`로 처리한다.

처음에는 OUT이다. 아래 표의 action은 현재 입력을 읽을 때 수행한다.

| 현재 state | 입력 | 다음 state | Action |
|---|---|---|---|
| OUT | whitespace | OUT | 없음 |
| OUT | non-whitespace | IN | word 수 1 증가 |
| IN | non-whitespace | IN | 없음 |
| IN | whitespace | OUT | 없음 |

`I am a boy`는 OUT→IN을 네 번 지나므로 4 words다. 두 space 다음 `ab`, tab, newline, `c`, EOF를 읽는 경우도 따라갈 수 있다. 처음 두 space는 OUT을 유지하고 `a`에서 첫 word를 센다. `b`는 IN을 유지하며 tab에서 OUT으로 돌아온다. Newline도 OUT을 유지하고 `c`에서 둘째 word를 센다. 결과는 2다. 마지막 word 뒤에 whitespace가 없어도 시작할 때 이미 셌으므로 EOF에서 다시 증가시키지 않는다.

이 작은 예는 기억해야 할 상태가 왜 필요한지 보여 준다. Whitespace 개수를 세는 방법은 연속 공백을 여러 word 경계로 오인하지만 state transition은 word에 진입하는 순간만 센다. [C examples slides 11–12](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/01.CProgrammingExamples.pptx)

## DFA(결정적 유한 상태 기계)로 필요한 기억을 표현하기

DFA(Deterministic Finite State Automata)는 유한한 state와 입력에 따른 transition을 갖는다. 교육용 diagram에는 transition action을 함께 적을 수 있다. 바깥에서 들어오는 화살표는 초기 state, 이중 원은 accepting state(수용 상태)를 나타낸다. Word counter의 IN/OUT은 과거 입력 전체 대신 다음 판단에 필요한 정보만 남긴 예다.

### Prefix를 기억하는 SNUCSE와 integer 인식

C examples slide 13의 `SNUCSE` diagram에서는 초기 state S에서 문자 `S,N,U,C,S,E`를 차례로 읽으며 `S→1→2→3→4→5→F`로 진행한다. State 번호는 지금까지 맞춘 prefix(접두사)의 길이를 기억한다고 이해하면 된다. 실패했다고 항상 모든 진행을 버리지는 않는다. State 5에서 `N`을 읽으면 겹치는 prefix를 보존하여 2로 가고, 자료는 state 1·2·3·5에서 `S`를 읽으면 1로 가는 전이를 보충한다. 그림에는 모든 실패 전이가 표시되어 있지 않다.

같은 page의 integer 언어는 `0` 또는 `[+-]?[1-9][0-9]*`다. 그림에서 볼 것은 0의 별도 수용 경로와 nonzero 첫 digit 이후의 반복 경로다. 입력 전체를 하나의 수로 판단하면 `0`은 accept, `+0`은 reject, `+12`는 accept다. `+12`에서는 sign을 읽고, 첫 nonzero digit `1`로 수용 상태에 도달한 뒤 `2`로 그 상태를 반복한다. 이 언어의 `?`는 앞 항목 0회 또는 1회를 뜻한다. 뒤의 [[courses/system_programming/units/dirtree|Dirtree pattern]]에서 사용하는 “임의 문자 하나”와 다르다. [C examples slide 13](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/01.CProgrammingExamples.pptx)

### Named constant와 invariant(불변 조건)

State를 0, 1로 적기보다 IN, OUT으로 쓰면 전이의 의미를 직접 읽을 수 있다. 자료는 세 방법을 소개한다.

```c
enum DFAState { IN, OUT };
```

`enum`의 IN과 OUT은 정수 상수이고 여기서는 0, 1이다. `#define IN 0`은 preprocessing token 치환이며, `const int IN = 0;`은 수정이 제한된 object를 선언한다. 같은 숫자를 담는다고 모든 C99 문맥에서 서로 바꿔 쓸 수 있는 것은 아니다. 특히 [[courses/system_programming/transcripts/2026-09-07|2026-09-07 STT 31:14–33:09]]의 `const int`와 `case` label 질문은 강의에서 결론을 내리지 않았다. C99의 integer constant expression 조건과 object 선언을 구분해야 한다.

`switch`의 `default`에서 `assert(0)`을 사용하는 예는 “state는 IN 또는 OUT”이라는 내부 invariant 위반을 드러낸다. `assert`는 잘못된 내부 상태를 빨리 찾는 도구이며 모든 build에서 외부 입력 오류를 처리하는 계약을 대신하지 않는다. 함수 앞의 comment 역시 character 처리 절차를 나열하기보다 “stdin에서 word 수를 세어 출력한다”는 caller 관점의 동작을 설명하는 편이 유용하다. [C examples slides 14–19](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/01.CProgrammingExamples.pptx)

## Decommenter: 같은 문자라도 문맥에 따라 의미가 달라진다

Decommenter는 C source에서 comment를 제거하는 변환기다. `/`와 `*`만 찾으면 될 것 같지만 string 안의 `/*`까지 지우면 프로그램의 데이터가 변한다. 필요한 state는 지금 문자를 읽는 문맥에서 나온다. [[courses/system_programming/transcripts/2026-09-09|2026-09-09 STT 01:09:39]]에서 이 변환의 목적을 소개한다.

입력은 `stdin`, 변환한 source는 `stdout`, 진단은 `stderr`로 나눈다. Lab 1 PDF p.3의 command를 익명 파일명으로 정리하면 다음과 같다.

```sh
./decomment < input.c > output 2> errors
```

Shell은 `input.c`를 stdin(fd 0), `output`을 stdout(fd 1), `errors`를 stderr(fd 2)에 연결한다. 이 연결을 위해 프로그램 안에 별도의 filename parser가 필요한 것은 아니다. 진단을 stdout에 쓰면 변환 결과에 섞이므로 stream 구분은 결과의 일부다.

### Comment를 space 하나로 바꾸고 newline을 보존하는 이유

Lab 1의 계약은 `/* ... */`와 `// ...` comment를 space 하나로 대체하되 원래 newline은 보존하는 것이다. `abc/*def*/ghi`는 `abc ghi`가 된다. 빈 문자열로 지우면 `abcghi`라는 다른 token을 만들 수 있다. Block comment 안의 newline도 남겨야 뒤 code의 원래 줄 번호가 유지된다.

Block comment는 nested하지 않는다. 따라서 `abc/*def/*ghi*/jkl*/mno`는 첫 `/*`부터 그 뒤 처음 만나는 `*/`까지만 comment로 보아 `abc jkl*/mno`가 된다. 뒤에 남은 `*/`를 또 다른 comment 종료라고 임의 처리하면 계약이 달라진다.

아래 각 줄은 끝에 실제 newline이 있다고 가정한다. 표시된 `s`나 `n`을 출력하는 문제가 아니다.

| 입력 | 출력 |
|---|---|
| `abc/*def*/ghi` | `abc ghi` |
| `abc//def` | `abc ` 뒤 원래 newline |
| `abc"def/*ghi*/jkl"mno` | 입력 그대로 |

자료 PDF pp.4–7의 표에서 아래첨자 `s`와 `n`은 space와 newline을 눈에 보이게 표시한 기호다.

### Quote와 escape를 하나의 문맥으로 읽기

String과 character literal 안에서는 comment 표시자를 보존한다. 또 literal 안의 backslash와 바로 다음 character를 함께 처리하여 escaped quote를 종료 quote로 오인하지 않아야 한다. PDF p.8의 입력은 다음과 같다.

```text
abc"def\"ghi"jkl
```

`\"`의 quote는 string을 닫지 않는다. 따라서 backslash와 quote를 모두 그대로 출력하고 뒤의 unescaped quote에서 literal을 끝낸다. Character literal의 `\'`에도 같은 구분이 필요하다.

두 규칙을 합친 설명용 예 `abc"def\"/*ghi*/jkl"mno`도 끝의 newline까지 그대로 남는다. Escaped quote 뒤에도 아직 string 안이므로 `/*ghi*/`는 comment가 아니다. 이 결합 예는 자료의 규칙을 적용한 계산이며 강의에서 그대로 실행한 결과라는 뜻은 아니다.

## EOF에서 구분해야 하는 종료 상태

문자 처리를 끝내는 EOF가 모든 state에서 같은 의미는 아니다. Lab 1 PDF pp.9–12는 literal 안의 newline이나 종료되지 않은 string·character literal에 warning이나 error를 만들지 않도록 한다. 이 과제는 C compiler 전체의 문법 검사기가 아니다. Multi-character character constant를 모든 C 구현에서 무조건 문법 오류라고 일반화할 필요도 없다.

반면 block comment가 EOF까지 닫히지 않으면 comment가 **시작한 줄**을 진단하고 `EXIT_FAILURE`로 종료한다. PDF p.11에서 둘째 줄에 시작한 comment의 stderr는 다음 한 줄이며 끝에 newline이 붙는다.

```text
Error: line 2: unterminated comment
```

나머지 경우의 종료 상태는 `EXIT_SUCCESS`다. 현재 줄 번호만 기억하면 comment 시작 위치를 잃을 수 있으므로 “현재 위치”와 “열린 comment의 시작 위치”는 구별되는 정보다.

입력 줄 길이는 임의로 길 수 있다. 짧은 고정 line buffer에 전체 줄이 들어간다고 가정하면 안 된다. 명세는 마지막 줄에 newline이 있고 backslash-newline sequence는 없다고 가정하므로 이 범위에서는 physical line과 logical line이 일치한다. 이는 일반적인 C preprocessing 전체에 대한 가정은 아니다.

## State 경계로 변환기의 동작을 검증하기

State-transition diagram을 먼저 만들면 comment 시작·종료, quote, escape, newline, EOF에서 무엇을 기억해야 하는지 분리할 수 있다. Lab 1은 diagram 설계 후 source 수정, `make` build, reference와 비교하는 흐름을 제시한다.

같은 입력을 reference와 자신의 프로그램에 주고 stdout과 stderr를 각각 비교해야 한다. [[courses/system_programming/transcripts/2026-09-09|2026-09-09 STT 01:20:03]]의 `diff` 설명은 파일 내용 비교다. 출력이 같아도 exit status까지 같다는 뜻은 아니므로 성공·실패 상태도 별도로 확인해야 한다. 특히 unterminated comment는 변환 결과뿐 아니라 오류가 stderr에 있는지, 시작 줄이 맞는지, 실패로 끝나는지가 모두 중요하다. 제공된 여섯 test는 시작점이며 모든 경계를 포함한다는 증거는 아니다.

명확한 이름, caller 관점 function comment, 여러 작은 함수, 72-character line 안내는 이 경계를 유지하기 쉽게 만든다. 제공 Makefile, 실제 compilation history, 단일 `decomment.c`와 확장자 없는 `readme`를 보존하는 당시 제출 구조 역시 build와 작업 과정을 재현하려는 계약이다. Diagram의 정확한 제출 위치는 제공 directory 목록만으로 확정하지 않는다. 이런 분리는 [[courses/system_programming/units/dirtree|directory traversal과 pattern 처리]]에서도 입력의 문법, 선택 조건, 출력 계약을 섞지 않는 설계로 이어진다.

## 핵심 정리

- State는 이미 읽은 prefix가 다음 문자 해석에 주는 정보를 보존한다.
- Word 진입 시 count하면 EOF에서 중복하지 않는다.
- Comment 제거는 token·newline·literal을 동시에 보존해야 한다.
- Stream 분리는 [[courses/system_programming/units/io-streams|I/O와 buffering]]에서도 중요하다.

## 확인·연습문제

### 개념 확인과 추론

#### 확인 Q01 · 문자와 EOF

ASCII에서 97, `'a'+3`, 122와 대소문자 차이 계산은? getchar 결과를 int에 두는 이유, 분류와 ctype의 주의점은?

<details><summary>해설 보기</summary>

97은 a, a+3은 d, 122는 z다. 문자 code 차이 a−A를 C에 더하면 c, c에서 빼면 C다. `getchar`는 모든 byte 값과 별도 EOF를 구별하도록 int로 받는다. Alphabet·digit·other 중 하나만 증가시키면 한 문자를 중복 집계하지 않는다. Ctype에는 EOF 또는 unsigned char로 표현 가능한 값을 주어야 하고 locale 영향도 있다. 253/4/289는 특정 입력의 결과다.

**채점·확인:** a/d/z·case gap·EOF 보존·한 번 집계를 확인한다.

</details>

#### 확인 Q02 · Word 경계

두 space, ab, tab, newline, c, EOF 입력을 OUT/IN으로 추적하고 count가 증가하는 순간을 표시하라.

<details><summary>해설 보기</summary>

처음 OUT에서 두 space는 유지한다. a에서 OUT→IN으로 count=1, b는 IN 유지다. Tab에서 OUT, newline도 OUT이다. c에서 OUT→IN으로 count=2이며 EOF에 추가하지 않는다. Word는 non-whitespace의 연속이므로 마지막 whitespace가 없어도 이미 센 상태다.

**채점·확인:** 두 transition과 EOF에서 증가하지 않는 이유를 확인한다.

</details>

#### 확인 Q03 · DFA와 state 이름

SNUCSE 경로와 겹치는 prefix를 설명하고 정수 언어에서 0, +0, +12를 판정하라. initial/accept 표시와 macro·const·enum, assert의 역할은?

<details><summary>해설 보기</summary>

Initial arrow와 double-circle accept를 구별한다. SNUCSE는 S→1→2→3→4→5→F다. State5의 N은 prefix SN에 해당하는 2로, 1·2·3·5의 S는 1로 간다. 모든 실패 transition이 그림에 그려진 것은 아니다. 언어 `0|[+-]?[1-9][0-9]*`는 0·+12를 accept, +0을 reject한다. 여기 ?는 optional이다. `#define IN 0`은 token 치환, `const int`는 object, `enum {IN,OUT}`는 0·1 정수 상수여서 모든 C99 문맥에서 동일하지 않다. 이름은 의미·caller 의도를 드러내고 default assert는 정상 state 밖의 invariant 오류를 찾는다. 모든 external error 처리나 모든 build의 검사를 대체하지 않는다.

**채점·확인:** Overlap·정수 판정·세 선언 방식·assert 한계를 모두 확인한다.

</details>

#### 확인 Q04 · Comment와 literal 보존

`./decomment < input.c > output 2> errors`의 세 stream을 설명하라. `abc/*x*/def`와 nested처럼 보이는 comment, escaped quote를 포함한 literal은 어떻게 처리하는가?

<details><summary>해설 보기</summary>

stdin(0)은 input.c, stdout(1)은 output, stderr(2)는 errors다. Comment는 한 space로 바꿔 `abc def`가 되며 내부 newline은 보존해 줄 번호를 유지한다. Block comment는 중첩하지 않아 `abc/*def/*ghi*/jkl*/mno`는 `abc jkl*/mno`다. Line comment도 정해진 경계에서 지운다. `abc"def\"ghi"jkl` 뒤 newline과 `abc"def\"/*ghi*/jkl"mno` 뒤 newline은 각각 그대로 출력한다. Backslash·escaped quote·literal 내부 /*...*/는 모두 문자다. 이 두 성공 입력의 stderr는 비어 있고 종료는 success다. Character literal도 quote 종류와 escape 상태를 구별한다.

**채점·확인:** Token 분리·newline·비중첩·두 literal의 정확한 보존과 stream을 확인한다.

</details>

#### 확인 Q05 · EOF 계약

Line2에서 block comment를 열고 닫지 않은 채 EOF면 stderr·종료값은? 닫히지 않은 string/char literal이나 literal 안 newline도 같은 오류인가?

<details><summary>해설 보기</summary>

정확히 `Error: line 2: unterminated comment`와 newline을 stderr에 쓰고 `EXIT_FAILURE`다. 현재 마지막 줄이 아니라 opening line을 기억한다. 이 과제는 닫히지 않은 string·character literal이나 literal newline에 별도 warning을 내지 않고 다른 block-comment 오류가 없으면 success다. 임의 길이 입력을 처리하며 마지막 newline과 backslash-newline 없음이라는 주어진 가정을 보존한다. 일반 C compiler의 전체 문법 검사와 다르다.

**채점·확인:** 진단 문구·opening line·status와 비오류 조건을 구별한다.

</details>

#### 확인 Q06 · 검증의 세 결과

설계부터 reference 비교까지 순서를 설명하라. stdout이 같기만 하면 통과인가? 기존 Makefile·history와 여섯 예제는 어떻게 다루는가?

<details><summary>해설 보기</summary>

State diagram·transition을 먼저 정하고 구현·make 후 같은 입력의 stdout, stderr, exit status를 각각 비교한다. stdout만 같아도 실패 status나 누락 diagnostic이면 계약 위반이다. 여섯 예제는 경계 확인의 시작이며 모든 입력 증명이 아니다. 함수·이름·comment와 72-column 지침으로 의도를 드러내고 supplied Makefile/history를 보존한다. decomment.c·readme 제출 지침은 당시 자료의 범위이며 diagram 제출 여부는 불명확하다. 여기서는 실제 reference 실행 성공을 주장하지 않는다.

**채점·확인:** 세 관측값·경계 테스트·자료 한계를 확인한다.

</details>

### 응용 연습

#### 연습 P01 · 서로 다른 실패를 잡는 테스트

**강의 기반 일반 연습.** 세 buggy 설계가 있다: A는 comment를 빈 문자열로 지운다; B는 literal 안 /*를 comment로 본다; C는 EOF의 모든 열린 state를 error로 본다. 각 설계를 구별할 최소 입력과 stdout·stderr·status 기대값을 제시하라.

강의·Lab 1 요구사항 기반 새 일반 연습이다. 전체 후보 색인에 이 word-DFA·decommenter의 literal/newline/EOF 계약을 직접 뒷받침하는 문항이 없다. 다른 wildcard 문법을 기출 style로 전용하지 않는다. 선행: Q02·Q04–Q06.

<details><summary>해설 보기</summary>

A에는 `a/*x*/b`+newline: stdout `a b`+newline, stderr empty, success다. B에는 `"/*x*/"`+newline: stdout은 원문 그대로, stderr empty, success다. C에는 닫히지 않은 `"abc`+newline 후 EOF: literal 내용을 그대로 보존하고 stderr empty, success다. 대비용 실제 block-comment 입력 `a\n/*x\n`은 stdout `a\n \n`, stderr `Error: line 2: unterminated comment`+newline, failure다. 이 네 결과가 token·literal·EOF 분류를 각각 점검한다.

**채점·확인:** 각 입력에 세 관측값을 모두 적고 잡는 bug를 연결한다.

</details>

### 복습 계획

Q02·Q03의 state 경로를 먼저 그린다. Q04·Q05는 stdout/stderr/status 세 칸에 답하고 P01로 경계마다 별도 테스트를 설계한다.

## 출처

### 날짜별 강의 노트

- [[courses/system_programming/lectures/2026-09-02-lecture-01|2026-09-02 강의 노트]]
- [[courses/system_programming/lectures/2026-09-07-lecture-02|2026-09-07 강의 노트]]
- [[courses/system_programming/lectures/2026-09-09-lecture-03|2026-09-09 강의 노트]]

### 수업자료와 강의 구간

- [C examples slides 3–10](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/01.CProgrammingExamples.pptx)
- [C examples slides 11–12](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/01.CProgrammingExamples.pptx)
- [C examples slide 13](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/01.CProgrammingExamples.pptx)
- [C examples slides 14–19](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/01.CProgrammingExamples.pptx)
- [[courses/system_programming/transcripts/2026-09-07|2026-09-07 STT 14:04]]
- [[courses/system_programming/transcripts/2026-09-07|2026-09-07 STT 31:14–33:09]]
- [[courses/system_programming/transcripts/2026-09-09|2026-09-09 STT 01:09:39]]
- [[courses/system_programming/transcripts/2026-09-09|2026-09-09 STT 01:20:03]]
- Lab 1 decommenter handout: 공개 URL이 없는 제공 PDF의 stream·EOF 요구사항을 참고한다.

연결된 공개 자료는 slide deck이며, 이 자료들의 PDF 페이지 보기 링크는 제공되지 않았다. 녹취 시각은 일반 텍스트로 표시한다.

- [00.Introduction.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx)

### 자료 범위와 한계

- 9월 2일 항목은 연결된 자료 범위도 포함하며 이후 날짜의 설명을 그날 발화로 소급하지 않는다.
- 정수 DFA의 ?는 optional이고 Dirtree의 ?와 다르다. 생략된 transition과 불명확한 발화는 임의로 복구하지 않는다.
- 제출·환경 지침은 당시 자료 기준이다. Diagram 제출 여부는 미확정이며 여섯 예제로 전체 검증이나 실제 실행 성공을 주장하지 않는다.
- 직접 대응하는 indexed 기출 근거가 없어 P01은 일반 연습이다.


---

[[courses/system_programming/units/objects-pointers|← 이전: C object·type·주소와 pointer]] · [[courses/system_programming/units/index|단원 목차]] · [[courses/system_programming/units/files-metadata|다음: Unix file·directory·inode와 metadata →]]
