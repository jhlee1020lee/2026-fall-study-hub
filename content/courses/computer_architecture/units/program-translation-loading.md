---
title: "프로그램 번역·Linking·Loading"
description: "Separate compilation부터 linking·loading과 세 instruction의 상태 변화까지 추적한다."
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
source_lectures: ["courses/computer_architecture/lectures/2026-09-03-lecture-02"]
---

파일을 따로 번역한 결과가 실행 가능한 프로그램이 되는 과정을 따라간다. Symbol 연결·주소 조정·memory image 준비를 나누어 보면 machine code가 있어도 곧바로 실행할 수 없는 이유가 드러난다.

## Separate compilation과 파일 사이의 Symbol

프로그램을 여러 파일로 나누면 각 파일을 독립적으로 번역할 수 있다. 하지만 한 파일이 다른 파일의 함수나 변수를 사용한다면, 나중에 그 이름이 정확히 어느 정의를 가리키는지 연결해야 한다. [ISA와 architectural state](architecture-contract.md)가 실행의 의미를 정한다면, translation(번역)·linking(연결)·loading(적재)은 실행할 프로그램을 준비하는 과정이다. 여기서는 C 함수·배열·pointer의 기초를 전제로, 녹음이 없는 9월 3일 자료의 예제를 따라간다.

[[page_cache/computer_architecture/lec.02/page-019|CA M008 p.19]]의 `main.c`는 `int buf[2] = {1, 2};`를 정의하고 `main`에서 `swap`을 호출한다. 다른 파일 `swap.c`에는 다음 코드가 있다.

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

`extern int buf[];`는 배열의 정의가 다른 곳에서 제공됨을 알린다. `bufp0`는 첫 원소를 가리키며 함수 안에서 `bufp1`은 둘째 원소를 가리키게 된다. 먼저 `temp`에 1을 보관하고, 첫 원소에 2를 쓴 다음, 둘째 원소에 보관해 둔 1을 쓴다. 결과는 `{2, 1}`이다. 첫 값을 보관하지 않고 먼저 덮어쓰면 마지막 대입에 필요한 원래 값이 사라진다.

Symbol(심볼)은 이 연결 과정에서 함수나 객체를 식별하는 이름이다. [[page_cache/computer_architecture/lec.02/page-020|CA M008 p.20]]의 화살표는 다음 차이를 보여 준다.

| 이름 또는 사용 | Linker 관점의 역할 |
|---|---|
| `main.c`의 `main`, `buf` 정의 | 다른 파일에서 참조할 수 있는 global symbol |
| `swap.c`의 `swap`, `bufp0` 정의 | Global symbol |
| `main.c`의 `swap` 사용, `swap.c`의 `buf` 사용 | 다른 파일의 정의가 필요한 external reference |
| 파일 범위의 `static bufp1` | 이 파일에 한정되는 local symbol |
| 함수 안의 `temp` | 실행 중 사용하는 automatic local variable |

`bufp1`과 `temp`는 모두 일상적으로 “지역적”이라고 부를 수 있지만 이유가 다르다. `bufp1`의 `static`은 파일 사이 이름 연결을 제한하고 그 저장공간은 함수 호출마다 새로 생기는 automatic 변수와 다르다. `temp`는 한 번의 `swap` 실행에 필요한 값이다. 그림의 “Linker knows nothing of temp”는 이 변수가 파일 간 symbol resolution(심볼 해결)의 대상이 아니라는 뜻이지, 실행할 때 값이 필요 없다는 뜻이 아니다.

## Translation과 Relocatable object file

Assembly code(어셈블리 코드)는 instruction의 사람이 읽을 수 있는 표기이고, assembler(어셈블러)는 이를 binary machine code(이진 기계어)로 옮긴다. Compiler는 고수준 연산을 instruction으로 바꾸는 역할을 한다. Pseudo-instruction(의사 명령어)은 여러 실제 machine instruction으로 확장될 수 있으므로 assembly source의 줄 수와 실행 instruction 수를 같다고 세면 안 된다. [[page_cache/computer_architecture/lec.02/page-028|CA M008 p.28]]

[[page_cache/computer_architecture/lec.02/page-021|CA M008 p.21]]의 흐름에서는 `main.c`와 `swap.c`가 각각 translators인 `cpp`, `cc1`, `as`를 지나 `main.o`와 `swap.o`가 된다. 전처리, compilation, assembly를 거친 결과가 각각 따로 만들어지는 것이다. Compiler driver는 이러한 단계를 묶어서 호출할 수 있다.

이 `.o` 파일들은 relocatable object file(재배치 가능한 목적 파일)이다. 이미 machine code가 있어도 다른 파일의 symbol이 아직 연결되지 않았거나 최종 주소가 정해지지 않았을 수 있다. 예를 들어 `main.o`에는 `swap` 호출이 있지만 `swap`의 실제 코드가 어디에 놓일지는 두 파일을 연결할 때 정해진다. 따라서 machine code를 만들었다는 것과 완성된 실행 파일을 만들었다는 것은 다른 단계다.

## Symbol resolution과 Relocation

Linker(링커)는 서로 다른 object file의 정의와 참조를 연결하고 최종 code·data 배치를 만든다. Symbol resolution은 “이 이름은 어느 정의인가?”에 답하고, relocation(재배치)은 “최종 배치에서 이 주소 참조를 어떻게 맞출 것인가?”에 답한다.

![Object file의 code와 data가 실행 파일의 section으로 모이는 원자료 도표](https://jhlee1020lee.github.io/2026-fall-study-hub/static/page_cache/computer_architecture/lec.02/page-022.png)

[[page_cache/computer_architecture/lec.02/page-022|CA M008 p.22]]에서 왼쪽 `main.o`와 `swap.o`의 작은 상자가 오른쪽 실행 파일의 큰 상자로 모인다. `main`과 `swap` 코드는 `.text`, 초기값이 있는 `buf`와 `bufp0`는 `.data`, 파일 범위의 `bufp1`은 `.bss`에 표시되어 있다. 함수 안의 `temp`를 이 global/static data 목록에 추가해서는 안 된다.

`bufp0`는 단순한 정수 초기값이 아니라 `buf[0]`의 주소를 갖는 pointer이므로, `buf`의 최종 배치와 주소 참조를 일치시키는 문제가 생긴다. 함수 호출의 target도 같은 이유로 최종 code 위치와 맞아야 한다. 그림에는 headers, `.symtab`, `.debug`도 따로 있다. 이들은 파일의 모든 내용이 실행 instruction이거나 프로그램의 보통 data라는 생각이 틀렸음을 보여 준다. 이 설명은 static linking의 입문 모형이며 모든 relocation 종류나 dynamic linker의 동작을 열거하지는 않는다.

## ELF Loading과 실행 중 Memory layout

Loading은 실행 파일로부터 실행에 필요한 memory image를 준비하는 단계다. [[page_cache/computer_architecture/lec.02/page-023|CA M008 p.23]]의 ELF(실행 파일 형식) 그림은 왼쪽의 file 구성과 오른쪽의 runtime memory 구성을 구분한다. `.init`·`.text`·`.rodata`는 read-only segment, `.data`·`.bss`는 read/write segment로 묶여 있다. 그 위에 runtime heap, shared-library mapping 영역, user stack과 kernel 영역이 표시되어 있다.

이 그림에서 읽어야 할 핵심은 **파일의 section 목록과 실행 중 memory 전체가 같지 않다**는 점이다. File의 symbol/debug 정보 전체를 일반 data segment와 동일시할 수 없고, 실행 중 사용하는 heap과 stack도 구분해야 한다. 그림의 주소는 특정 32-bit 주소 공간의 예시다. 모든 OS나 RV64 프로그램이 그 고정 주소에 적재된다는 뜻은 아니다.

## 적재된 Instruction이 State를 바꾸는 과정

Loader가 실행할 내용을 배치한 다음에는 ISA가 각 instruction의 효과를 정한다. [[page_cache/computer_architecture/lec.02/page-024|CA M008 p.24]]는 처음에 `PC=0x1000`, `GPR[x10]=0x2000`, `MEM[0x2000]=41`인 예를 준다. `GPR[x10]`은 register의 값이며 `MEM[a]`는 주소 `a`의 memory 값이라는 표기다.

```asm
lw   x5, 0(x10)
addi x5, x5, 1
sw   x5, 0(x10)
```

| 실행한 instruction의 주소 | 동작 | 실행 뒤 `x5` | 해당 memory 값 | 다음 PC |
|---|---|---|---|---|
| `0x1000` | `lw`로 주소 `0x2000`에서 읽음 | 41 | 41 | `0x1004` |
| `0x1004` | `addi`로 1을 더함 | 42 | 41 | `0x1008` |
| `0x1008` | `sw`로 결과를 같은 주소에 씀 | 42 | 42 | `0x100C` |

중간 행에서 register가 42가 되어도 memory는 아직 41이다. Arithmetic가 register를 바꾼 뒤 명시적인 store가 있어야 memory의 값도 바뀐다. 이 예는 기본 32-bit instruction을 사용하므로 PC가 매번 4 bytes씩 증가한다. Data를 담는 register의 폭과 instruction 자체의 길이를 같은 것으로 읽으면 안 된다. 이 분리는 [Register와 memory의 데이터 표현](data-register-memory.md)에서 더 자세히 이어진다.

## 핵심 정리

- `static`의 파일 내 linkage와 함수 안 automatic variable의 local 범위는 서로 다르다.
- Object file에 machine code가 있어도 외부 symbol과 최종 주소는 아직 미정일 수 있다.
- Symbol resolution은 정의를 연결하고 relocation은 최종 위치에 주소 참조를 맞춘다.
- ELF의 file section과 실행 중 heap·stack은 같은 목록이 아니다.
- Register 연산의 결과는 store가 실행되어야 memory에 반영된다.

## 확인·연습문제

### 개념 확인과 추적

#### 확인 Q01 · Symbol의 종류와 값 보존

본문의 `swap`에서 `{1,2}`가 바뀌는 순서를 설명하라. `buf`, `swap`, `bufp0`, 파일 범위 `static bufp1`, 함수 안 `temp`를 연결 관점에서 구분하고, `temp`를 linker가 연결하지 않아도 필요한 이유를 말하라.

<details><summary>해설 보기</summary>

`temp`가 첫 값 1을 보관하고 첫 원소에 2를 쓴 뒤 둘째 원소에 보관한 1을 써 `{2,1}`이 된다. `buf`의 정의와 `swap`·`bufp0`의 정의는 global symbol이며 다른 파일에서 사용하는 `buf`·`swap`은 external reference다. `bufp1`은 파일 내부로 linkage가 제한된 static 저장 객체이고 `temp`는 호출 중 쓰는 automatic local variable이다. 파일 간 이름 해결 대상이 아니어도 덮어쓰기 전 값을 보존할 runtime 역할이 있다.

**채점·확인 기준:** 세 대입 순서와 global/external/file-local/automatic 구분을 모두 보인다.

</details>

#### 확인 Q02 · Machine code와 실행 파일

`main.c`와 `swap.c`에서 각각 `.o`가 만들어지고 하나의 실행 파일이 되는 단계를 설명하라. Compiler·assembler·compiler driver의 역할과 pseudo-instruction의 줄 수를 구분하라.

<details><summary>해설 보기</summary>

각 source는 preprocessing·compilation·assembly를 거쳐 따로 번역된 relocatable object가 된다. Compiler는 고수준 연산을 instruction으로, assembler는 assembly를 machine code로 옮기며 driver는 여러 단계를 묶어 호출할 수 있다. Linker는 object를 연결한다. `.o`에 machine code가 있어도 외부 참조와 최종 배치가 미정일 수 있고 pseudo-instruction은 여러 실제 instruction으로 확장될 수 있으므로 source 줄 수도 실행 instruction 수가 아니다.

**채점·확인 기준:** 단계 순서, 도구 역할, object가 아직 relocatable인 이유와 pseudo-instruction의 한계를 설명한다.

</details>

#### 확인 Q03 · 이름 해결과 주소 조정

`main.o`의 `swap` 호출과 `bufp0=&buf[0]`를 이용해 symbol resolution과 relocation의 질문을 구분하라. 예제의 code·초기화 data·`bufp1`·symbol/debug 정보는 어떻게 분류되는가?

<details><summary>해설 보기</summary>

Resolution은 호출의 `swap`이나 참조의 `buf`가 어느 정의인지 정한다. Relocation은 code/data의 최종 위치에 맞게 call target과 pointer의 주소 참조를 조정한다. `main`·`swap` 코드는 `.text`, 초기값이 있는 `buf`·`bufp0`는 `.data`, `bufp1`은 그림의 `.bss`에 놓인다. `.symtab`·`.debug`와 headers는 일반 instruction/data와 구분하며 `temp`를 global/static section 목록에 넣지 않는다.

**채점·확인 기준:** 정의 선택과 위치 조정을 구별하고 pointer 초기값도 주소 참조임을 설명한다.

</details>

#### 확인 Q04 · ELF File과 Runtime memory

ELF file의 section 목록을 runtime memory의 전체 모습과 같다고 보면 무엇을 놓치는가? Read-only/read-write 부분과 heap·shared libraries·stack을 구분하라.

<details><summary>해설 보기</summary>

그림에서 `.init`·`.text`·`.rodata`는 read-only, `.data`·`.bss`는 read/write segment다. 실행 중에는 heap, shared-library mapping, user stack과 kernel 영역도 구분된다. Symbol/debug 정보를 모두 일반 data segment로 읽으면 파일의 도구용 정보와 실행 상태를 혼동한다. Loader가 실행용 memory image를 준비하며 그림의 주소는 특정 32-bit 예시다.

**채점·확인 기준:** 두 segment 분류와 runtime 영역 차이, 주소 예시의 범위를 확인한다.

</details>

#### 확인 Q05 · Register 갱신과 Memory 갱신

처음 `PC=0x1000`, `x10=0x2000`, `MEM[0x2000]=41`이다. 본문의 `lw x5,0(x10)` → `addi x5,x5,1` → `sw x5,0(x10)` 뒤의 `x5`, memory, PC를 각각 추적하고 loader와 ISA의 역할을 분리하라.

<details><summary>해설 보기</summary>

첫 load 뒤 `(x5,memory,PC)=(41,41,0x1004)`, 덧셈 뒤 `(42,41,0x1008)`, store 뒤 `(42,42,0x100C)`다. Memory는 store까지 41이며 register 산술이 memory를 자동 갱신하지 않는다. Loader는 실행 내용을 준비하고 ISA는 각 instruction의 상태 변화를 정한다. PC의 +4는 이 예제의 32-bit instruction 길이에서 나온다.

**채점·확인 기준:** 세 시점 모두를 쓰고 data register 폭과 instruction 길이를 혼동하지 않는다.

</details>

### 적용과 오류 진단

#### 연습 P01 · 설명에서 단계 혼동 찾기

새로 만든 자료 기반 일반 연습이다. 제공된 18문항에는 linking/loading의 직접 유형 근거가 없다. 다음 설명을 각각 고쳐라: (a) “`bufp0`의 주소 초기값은 각 `.o`를 만드는 순간 모든 최종 배치에서 유효하다.” (b) “`temp`가 `.bss`에 없으므로 swap은 첫 값을 보관할 수 없다.” (c) “Loader가 `addi`를 적재하면 memory의 41도 바로 42가 된다.”

<details><summary>해설 보기</summary>

(a) 최종 `buf` 배치에 맞춰 pointer 주소 참조를 조정해야 한다. Relocatable이라는 성질과 충돌하는 주장이다. (b) Automatic `temp`는 실행 중 원래 값을 보관하며 global/static section 분류와 별개다. (c) 적재와 실행이 다르고 `addi` 실행 자체도 register만 바꾼다. 해당 store가 실행된 뒤에야 memory가 42가 된다.

**채점·확인 기준:** 세 오류를 각각 relocation·storage 역할·실행 효과로 설명한다.

</details>

### 복습 순서

Q01–Q03으로 symbol·번역·주소 연결을 설명하고 Q04–Q05의 file/memory 구분과 상태 표를 빈 종이에 다시 쓴다. P01의 잘못된 문장을 고친 뒤 [[courses/computer_architecture/units/data-register-memory|Register와 memory]]에서 주소·값·폭 구분을 강화한다.

## 출처

- [[courses/computer_architecture/lectures/2026-09-03-lecture-02|2026-09-03 · 자료 기반 복습]]

- [lec.02.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/lec.02.pdf): [[page_cache/computer_architecture/lec.02/page-019|p.19]], [[page_cache/computer_architecture/lec.02/page-020|p.20]], [[page_cache/computer_architecture/lec.02/page-028|p.28]], [[page_cache/computer_architecture/lec.02/page-021|p.21]], [[page_cache/computer_architecture/lec.02/page-022|p.22]], [[page_cache/computer_architecture/lec.02/page-023|p.23]], [[page_cache/computer_architecture/lec.02/page-024|p.24]]

- 이 단원 전체는 녹음·STT가 없는 2026-09-03 lec.02 자료 기반 복습이며 정확한 구두 진도를 확인하지 않는다.
- ELF 주소 그림은 32-bit 예시이며 모든 OS·RV64의 고정 배치가 아니다. Linking 설명은 입문 static-linking 모형으로, 모든 relocation 종류나 dynamic linker를 다루지 않는다.
- 코드 추적은 기본 32-bit instruction과 유효한 data 주소를 전제로 한다. Source 명령을 실행한 결과나 과제 구현은 아니다.


---

[[courses/computer_architecture/units/architecture-contract|← 이전: 컴퓨터의 구성과 ISA: 명세에서 구현까지]] · [[courses/computer_architecture/units/index|단원 목차]] · [[courses/computer_architecture/units/data-register-memory|다음: 데이터 표현·Register·Memory →]]
