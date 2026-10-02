---
title: "프로그램 번역·Linking·Loading"
description: "Symbol 연결에서 실행 중 register·memory 변화까지 추적한다."
course: "computer_architecture"
unit_id: "program-translation-loading"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["lec 02.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_architecture/lectures/2026-09-03-lecture-02", "courses/computer_architecture/lectures/2026-09-08-lecture-03"]
---

파일별 번역이 끝나도 이름과 주소를 연결하는 일이 남는다. Linking·loading·실행을 나누어 값이 언제 바뀌는지 추적한다.

## Separate compilation과 symbol의 연결

여러 source file로 나눈 프로그램도 실행할 때는 하나의 일관된 주소 공간에서 서로의 함수와 데이터를 찾아야 한다. Separate compilation(분리 컴파일)은 각 파일을 따로 번역하게 해 주지만, 다른 파일에서 정의한 이름의 최종 위치까지 그 단계에서 모두 알 수 있는 것은 아니다. 이 차이를 해결하는 과정이 linking이다. 아래 내용은 [[courses/computer_architecture/lectures/2026-09-03-lecture-02|2026-09-03 강의 노트 · 자료 기반]]와 같은 instructor 자료를 읽는 복습이며, 녹음으로 확인된 그날의 구두 진도는 아니다.

[CA M008 PDF p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-019)의 예제에서 `main.c`는 `int buf[2] = {1, 2};`를 정의하고 `main`에서 `swap()`을 호출한다. 다음은 함께 제시된 `swap.c`이다.

```c
extern int buf[];
int *bufp0 = &buf[0];
static int *bufp1;

void swap()
{
    int temp;
    bufp1 = &buf[1];
    temp = *bufp0;
    *bufp0 = *bufp1;
    *bufp1 = temp;
}
```

Pointer(포인터)는 대상의 주소를 담고, `*bufp0`는 그 주소에 있는 값을 읽거나 쓸 때 사용한다. `bufp0`가 첫 원소를, `bufp1`가 두 번째 원소를 가리키게 한 뒤 다음 순서로 값을 바꾼다.

| 실행한 문장 | `temp` | `buf[0]` | `buf[1]` |
|---|---:|---:|---:|
| `temp = *bufp0;` | 1 | 1 | 2 |
| `*bufp0 = *bufp1;` | 1 | 2 | 2 |
| `*bufp1 = temp;` | 1 | 2 | 1 |

두 번째 문장에서 첫 값을 덮어쓰므로, 그 전에 `temp`에 보존해야 한다. 최종 배열은 `{2, 1}`이다. 이것은 instructor의 작은 예제를 추적한 결과이며 과제 프로그램이나 새 실행 실험은 아니다.

### Global symbol, external reference, local symbol

Symbol(심벌)은 linking 과정에서 정의와 참조를 연결하는 이름이다. [CA M008 PDF p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-020)의 빨간 표시는 C의 지역변수라는 표현과 linker의 local symbol이 같은 뜻이 아님을 보여 준다.

| 예제 요소 | Linker 관점의 역할 |
|---|---|
| `main.c`의 `main`, `buf` 정의 | 다른 파일과 연결할 수 있는 global symbol |
| `main.c`의 `swap` 사용 | 다른 파일의 정의를 요구하는 external reference |
| `swap.c`의 `swap`, `bufp0` 정의 | Global symbol |
| `swap.c`의 `extern int buf[]`와 `buf` 사용 | 다른 파일에서 정의된 배열 참조 |
| File-scope `static int *bufp1` | 해당 파일에 한정된 linker-local symbol |
| 함수 안의 automatic `temp` | 이 예제에서 파일 간 symbol resolution의 대상이 아닌 실행 중 지역변수 |

특히 `bufp0`는 그 자체로 이 파일에 정의된 pointer이면서 초기화할 주소는 다른 파일의 `buf`에 의존한다. “이름을 정의한다”와 “그 정의 안에서 다른 symbol을 참조한다”는 동시에 성립할 수 있다. `static bufp1`과 automatic `temp`를 모두 그냥 “local”이라고 묶으면 linking에 필요한 구분이 사라진다.

## Translation에서 executable까지

Assembly code(어셈블리 코드)는 machine instruction을 사람이 읽는 표기이고, assembler(어셈블러)는 이를 binary machine code로 옮긴다. Pseudo-instruction은 여러 machine instruction으로 확장될 수 있으므로 assembly source 줄 수와 실제 instruction 수를 같다고 가정하지 않는다. [CA M008 PDF p.28](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-028)

[CA M008 PDF p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-021)은 `main.c`와 `swap.c`가 각각 translators `cpp`, `cc1`, `as`를 지나 `main.o`, `swap.o`가 되는 흐름을 보여 준다. 이 object file들은 separately compiled이면서 relocatable하다. Compiler driver는 이 여러 도구의 호출을 묶어 표현할 수 있고, linker `ld`가 object들을 실행 파일 `p`로 연결한다. 자료 속 driver 명령은 이 흐름의 예이지 여기서 실행한 명령이 아니다.

이미 binary instruction이 생겼어도 아직 linking이 필요한 이유는 두 가지이다. **Symbol resolution**은 이름이 어느 정의를 가리키는지 정한다. **Relocation**은 최종 code/data 배치에 맞추어 주소 참조를 조정한다. 어떤 이름을 뜻하는지와 그 대상이 최종적으로 어느 주소에 놓이는지는 서로 다른 질문이다.

[CA M008 PDF p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-022)를 왼쪽 object별 구역에서 오른쪽 executable 구역으로 읽으면 다음 관계가 보인다.

| 내용 | Object에서의 위치 | 연결 뒤 의미 |
|---|---|---|
| `main`, `swap`의 코드 | 각 object의 `.text` | 실행 파일의 code 배치에 포함 |
| 초기값이 있는 `buf`, `bufp0` | `.data` | Data 배치와 참조 주소를 정함 |
| File-scope `bufp1` | `.bss` | 해당 저장공간을 배치 |
| Headers, `.symtab`, `.debug` | 형식·심벌·debug 정보 | 모두를 실행 중 일반 data와 동일시할 수 없음 |

따라서 object file을 단순히 이어 붙인다는 설명만으로는 부족하다. 다른 object를 향하던 참조까지 최종 배치와 일치해야 실행 가능한 전체가 된다. 세부 relocation 종류나 dynamic linker 구현은 이 그림이 설명하는 범위를 넘는다.

## Loading과 instruction의 상태 변화

Loader(로더)는 executable의 내용을 실행 가능한 memory image로 준비한다. [CA M008 PDF p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-023)은 ELF 파일의 section과 runtime memory layout을 나란히 둔다. `.init`, `.text`, `.rodata`는 read-only segment 쪽으로, `.data`, `.bss`는 read/write segment 쪽으로 연결된다. Runtime에는 heap, shared-library mapping 영역, user stack 등이 함께 있고 위쪽에는 kernel 영역이 표시된다. 이 그림의 주소는 특정 32-bit 주소 공간의 예시이므로 모든 RV64 프로그램의 고정 주소로 사용하면 안 된다.

File 안의 정보와 runtime 공간도 일대일로 같은 것은 아니다. 예를 들어 symbol/debug 정보를 담는 항목은 일반 변수들의 data segment와 구분해야 한다. Loading은 이런 실행 환경을 준비하고, ISA는 준비된 instruction이 상태를 어떻게 바꾸는지 정한다.

### 세 instruction에서 값과 주소를 따로 추적하기

[CA M008 PDF p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-024)의 시작 상태는 `PC = 0x1000`, `GPR[x10] = 0x2000`, `MEM[0x2000] = 41`이다. 여기서 `GPR[x10]`은 register 안의 값, `MEM[a]`는 주소 `a`에 있는 memory 값을 뜻한다.

```asm
lw   x5, 0(x10)
addi x5, x5, 1
sw   x5, 0(x10)
```

| Instruction 주소 | 동작 | 실행 후 `x5` | 실행 후 `MEM[0x2000]` | 다음 PC |
|---|---|---:|---:|---|
| `0x1000` | Base `0x2000` + offset 0에서 word를 읽음 | 41 | 41 | `0x1004` |
| `0x1004` | Register의 값에 immediate 1을 더함 | 42 | 41 | `0x1008` |
| `0x1008` | Register의 word를 같은 주소에 저장 | 42 | 42 | `0x100C` |

`lw`가 읽는 41은 주소 `0x2000`과 다르다. `addi`가 register를 42로 바꾸어도 memory는 아직 41이다. 마지막 `sw`가 있어야 memory까지 42가 된다. 여기서는 각 instruction이 32 bits, 즉 4 bytes인 순차 예제이므로 PC가 4씩 증가한다. 이런 상태 추적은 [[courses/computer_architecture/lectures/2026-09-08-lecture-03|2026-09-08 강의 노트]]의 register·load-store 설명으로 이어지며, translation이 만드는 instruction과 실행이 바꾸는 상태를 연결해 준다.

## 핵심 정리

- Symbol resolution은 정의를 고르고 relocation은 최종 주소 참조를 맞춘다.
- File-scope `static`과 함수의 automatic 지역변수는 linker 관점에서 다르다.
- Loader가 memory image를 준비한 뒤 instruction의 의미에 따라 상태가 바뀐다.

## 확인·연습문제

### 개념 확인

#### 확인 Q01 · Swap의 값 추적

`buf={1,2}`, `bufp0=&buf[0]`, `bufp1=&buf[1]`에서 `temp=*bufp0; *bufp0=*bufp1; *bufp1=temp;` 뒤의 배열을 각 단계마다 써라. `temp`를 생략하면 왜 안 되는가?

<details><summary>해설 보기</summary>

첫 단계는 `temp=1`, 배열 `{1,2}`이다. 둘째는 `{2,2}`, 셋째는 `{2,1}`이다. Pointer 자체는 주소를 담고 `*`는 그곳의 값을 접근한다. 첫 원소를 덮기 전에 원래 값 1을 `temp`로 보존하지 않으면 마지막에 복구할 값이 사라진다.

**채점·확인:** 주소와 값, 각 대입 후 배열, 보존 이유를 확인한다.

</details>

#### 확인 Q02 · Symbol의 세 역할

`main.c`의 `main`, `buf`, `swap` 사용과 `swap.c`의 `swap`, `bufp0`, `extern int buf[]`, file-scope `static bufp1`, automatic `temp`를 분류하라.

<details><summary>해설 보기</summary>

`main`·`buf`의 정의와 `swap.c`의 `swap`·`bufp0` 정의는 global symbol이다. `main.c`의 `swap` 사용과 `swap.c`의 `buf` 참조는 다른 파일의 정의를 요구한다. `bufp0`를 정의하면서 그 초기화에 외부 `buf` 주소를 사용할 수 있다. File-scope `static bufp1`은 linker-local symbol이고 automatic `temp`는 함수 실행 중 지역변수여서 이 예의 파일 간 symbol resolution 대상이 아니다.

**채점·확인:** `bufp0`의 정의와 외부 참조가 동시에 성립함을 포함한다.

</details>

#### 확인 Q03 · Object에서 executable로

`cpp`·`cc1`·`as`·`ld` 흐름, symbol resolution과 relocation, `.text`·`.data`·`.bss`·`.symtab`·`.debug`를 연결하라. 이미 machine code가 있는데 linking이 필요한 이유와 pseudo-instruction의 주의점은 무엇인가?

<details><summary>해설 보기</summary>

각 C 파일이 preprocessing·compilation·assembly를 거쳐 별도 relocatable `.o`가 되고 `ld`가 executable을 만든다. Driver는 이 도구 호출을 묶을 수 있다. Resolution은 이름의 정의를, relocation은 최종 배치에 맞는 참조 주소를 정하므로 단순 파일 연결만으로 부족하다. `main`·`swap` 코드는 `.text`, 초기화된 `buf`·`bufp0`는 `.data`, `bufp1`은 `.bss`에 해당한다. Header·symbol·debug 정보는 일반 변수 data와 구분한다. Pseudo-instruction이 여러 machine instruction으로 확장될 수 있어 줄 수와 IC는 다르다.

**채점·확인:** 이름 연결과 주소 조정을 나누고 모든 section 예를 분류한다.

</details>

#### 확인 Q04 · 적재와 주소 공간

ELF 그림의 read-only/read-write segment와 heap·shared-library·stack·kernel 영역을 설명하라. Loader가 하는 일과 ISA가 정하는 일은 무엇이며 그림 주소는 모든 RV64 실행에 고정되는가?

<details><summary>해설 보기</summary>

그림은 `.init/.text/.rodata`를 read-only, `.data/.bss`를 read/write로 묶고 runtime heap·shared-library mapping·user stack과 위쪽 kernel 영역을 보인다. Loader는 실행할 memory image를 준비하고 ISA는 적재된 instruction의 상태 전이 의미를 제공한다. `.symtab/.debug` 전체를 변수 data segment로 보지 않는다. 이 그림은 특정 32-bit 주소 공간 예이므로 모든 RV64의 고정 배치가 아니다.

**채점·확인:** File section과 runtime 영역을 구별하고 32-bit 예시 한계를 밝힌다.

</details>

#### 확인 Q05 · Load·계산·store의 시점

`PC=0x1000`, `x10=0x2000`, `MEM[0x2000]=41`에서 `lw x5,0(x10); addi x5,x5,1; sw x5,0(x10)`의 각 단계 뒤 `x5`, memory, PC를 구하라. Instruction은 각각 4 bytes이다.

<details><summary>해설 보기</summary>

`lw` 뒤 `(x5,memory,PC)=(41,41,0x1004)`, `addi` 뒤 `(42,41,0x1008)`, `sw` 뒤 `(42,42,0x100C)`이다. 주소 `0x2000`은 값 41과 다르다. 덧셈은 register만 바꾸고 store가 있어야 memory가 바뀐다. PC는 4-byte instruction 세 개만큼 진행한다.

**채점·확인:** `addi` 직후 memory가 아직 41인지 확인한다.

</details>

### 적용 연습

#### 연습 P01 · 단계별 증거 판별

새로 만든 자료 기반 일반 연습이다. 두 `.o`가 만들어졌으므로 외부 `swap`의 주소도 확정되었고 이미 `buf`가 뒤집혔다는 주장이 있다. 또 `.debug`를 모두 변수 data라고 부른다. 각 주장의 오류와 실행 결과를 확인하려면 필요한 단계를 설명하라.

18개 후보에는 symbol resolution·relocation·ELF loading을 직접 평가하는 문항이 없어 해당 시험 스타일의 근거는 없다.

<details><summary>해설 보기</summary>

Object 생성은 파일별 번역이다. Cross-file symbol resolution과 최종 배치의 relocation은 linking에서 필요하다. Loading은 memory image를 준비할 뿐이고 `swap`의 대입을 실제 실행해야 `{2,1}`이 된다. `.debug`는 debug 정보이며 초기화된 변수들의 `.data`와 다르다. 단계가 성공했다는 주장과 실행 중 값 추적은 별도로 확인해야 한다.

**채점·확인:** Translation→linking→loading→execution 순서와 각 단계의 한계를 답한다.

</details>

### 짧은 복습 계획

Q01–Q03으로 symbol과 section을 분류한 뒤 Q04–Q05를 연결하자. P01에서 어느 단계의 증거인지 말하고, 다음 날 Q05의 register/memory 표를 다시 작성하자.

## 출처

- [[courses/computer_architecture/lectures/2026-09-03-lecture-02|2026-09-03 강의 노트 · 자료 기반]]
- [[courses/computer_architecture/lectures/2026-09-08-lecture-03|2026-09-08 강의 노트 · 관련 선수 개념]]
- [lec 02.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.02.pdf) — [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-019), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-020), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-021), [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-022), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-023), [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-024), [p.28](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lec.02/page-028)

9월 3일 자료 기반 복습이며 녹음으로 확인한 구두 진도가 아니다. 9월 8일 노트는 register·load-store의 관련 설명이다. 자료 속 코드는 읽기 예이고 실행 실험이나 현재 과제의 구현이 아니다.

시험 연결은 2025-2 복기본에 한정되며 공식 원문·정답은 독립 확인되지 않았다. 제공 답안은 검증된 정답으로 채택하지 않았고 과거 채점 규칙·출제 가능성을 현 학기로 옮기지 않는다.
