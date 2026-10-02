---
title: "입력 검증·Board 판정·객체 상호작용과 게임 Platform 실습"
description: "입력 검증, board 판정, Player/Fight 계약과 Lab04 게임의 경계를 복습한다."
course: "computer_programming"
unit_id: "lab-applications"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["Lab02 v4.pdf", "Lab02 official assignment metadata", "Lab03 v2.pdf", "Lab03 skeleton.zip", "Lab04 v2.pdf", "Lab04 v4.pdf"]
private_source_assets: ["Lab02 official assignment metadata", "Lab03 skeleton.zip"]
source_lectures: ["courses/computer_programming/lectures/2026-09-10-lecture-04", "courses/computer_programming/lectures/2026-09-17-lecture-06"]
---

입력 단위·판정 순서·객체 책임을 명세에서 찾아 결과와 상태를 추적한다. Lab02–04의 경계 사례를 비교하며 출력·반환·실제 round 수를 구분해 보자.

## Input validation: 값보다 먼저 입력의 계약 읽기

프로그램이 무엇을 입력받고 어느 순서로 판단해야 하는지 명확하지 않으면, 문법이 맞는 코드도 다른 동작을 하게 된다. Input validation(입력 검증)은 허용할 값과 실패 경로를 정하는 일이다. Lab02는 한 줄 입력, 판정 순서, 배열에 저장한 board(보드)의 결과를 통해 이 책임을 나눈다. 기존 설명은 [[courses/computer_programming/lectures/2026-09-10-lecture-04|2026-09-10 강의 노트 · Lab02]]와 연결된다.

### 한 줄과 `exit` sentinel

첫 단계는 String 한 줄을 읽고 그대로 출력하는 일을 반복한다. `Computer Programming`처럼 공백이 있는 입력도 한 줄 전체가 단위다. 토큰 하나만 읽어서 `Computer`만 돌려주면 입력 계약을 바꾼 것이다. `Scanner(System.in)`은 입력 준비에 관한 hint이며, 한 줄을 어떻게 다룰지와 반복을 언제 끝낼지는 별도 판단이다. [Computer Programming M008 PDF pp.16–17]

Sentinel(종료 표식)인 `exit`는 일반 데이터와 다른 경로로 간다. [p.17의 console 예](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-017)는 `abc`, `Computer Programming`, `2018-12345`를 각각 되풀이해 출력하지만 마지막 `exit` 뒤에는 echo가 없다. 입력 행과 출력 행을 구별해서 읽어야 한다. [[courses/computer_programming/transcripts/2026-09-10|2026-09-10 STT 09:38]]도 한 줄을 읽고 `exit`에서 종료하는 흐름을 설명한다.

### 길이 → 구분자 → digit의 순서

다음 단계의 `XXXX-XXXXX` 형식은 세 조건을 순서대로 검사한다. 모두 틀린 조건을 한꺼번에 출력하는 것이 아니라 **첫 실패**를 보고한다. [[courses/computer_programming/transcripts/2026-09-10|2026-09-10 STT 15:25–18:22]]는 순서가 오류 메시지를 결정하며, 뒤의 검사 예시는 앞 조건을 통과해야 한다고 강조한다.

| 단계 | 검사 | 자료의 사례 | 판정 |
|---|---|---|---|
| 1 | 전체 길이가 `10`인가? | `2018-1234` | `The input length should be 10.` |
| 2 | 다섯 번째 문자, index `4`가 `'-'`인가? | `2018_12345` | `Fifth character should be` 뒤에 `'-'`를 표시하는 오류 |
| 3 | index 4를 제외한 문자가 모두 digit인가? | `e018-12345` | `Contains an invalid digit.` |
| 통과 | 세 조건 모두 만족 | `2018-12345` | `2018-12345 is valid.` |

길이를 먼저 검사하면 너무 짧은 문자열에서 `charAt(4)`를 성급하게 호출하는 문제도 피한다. 구분자 오류 메시지의 hyphen 주변 인용부호는 M008 PDF pp.18·20에서 다르게 인쇄되어 있으므로 여기서 하나를 새로운 공식 채점 문자열로 결정하지 않는다. 물리 PDF p.18은 인쇄된 slide 번호 19라는 점도 구별한다.

M008 p.19의 문자 범위는 다음과 같다. 이는 완성 validator가 아니라 한 문자에 대한 원본 조건이다.

```java
ch >= '0' && ch <= '9'  // digit
ch < '0' || ch > '9'    // outside the digit range
ch >= 'a' && ch <= 'z'  // lowercase English letters
ch >= 'A' && ch <= 'Z'  // uppercase English letters
```

문자 `'0'`은 정수 `0`과 다르다. 이 조건은 연속된 문자 코드 범위를 검사하며, 숫자처럼 보이는 모든 Unicode 문자를 허용하는 규칙은 아니다. Digit 범위의 안쪽은 두 경계를 모두 만족해야 하므로 `&&`, 바깥쪽은 어느 한 경계를 벗어나면 되므로 `||`다. 길이, 위치, 문자 범위를 분리하면 어느 단계에서 실패했는지 이유까지 설명할 수 있다.

## Board evaluation: 저장된 표식과 판정 우선순위

Lab02의 TicTacToe는 입력으로 받은 board를 판단한다. 아홉 정수는 `3×3` int array에 행 순서로 저장한다. 여기서 `0`, `1`은 각각 Player 0과 Player 1의 표식이며 **0은 빈칸이 아니다**. `0 1 0 1 0 0 1 1 1`을 저장하면 세 행은 `[0,1,0]`, `[1,0,0]`, `[1,1,1]`이다. 자료의 `printBoard`는 이 저장 배치를 확인하도록 돕는다. [M008 PDF pp.22–23]

승리 후보는 같은 플레이어의 표식이 가로·세로·대각선 한 줄 전체를 채운 경우다. 그러나 승리한 줄 하나를 발견했다고 바로 유효한 승리로 결정해서는 안 된다. 두 플레이어가 모두 승리하거나 표식 수 차이가 1보다 크면 `Invalid game.`이다. 유효한 board에서 한 명만 승리하면 해당 `Player 0 win.` 또는 `Player 1 win.`, 아무도 승리하지 않으면 `Tie.`다. [M008 PDF p.24] [[courses/computer_programming/transcripts/2026-09-10|2026-09-10 STT 38:21–39:19]]

### 다섯 board가 보여 주는 다른 이유

[M008 PDF p.25](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-025)의 예를 행별로 읽으면 다음과 같다. `/`는 표 안에서 행을 나누는 설명 표기다.

| 세 행 | 판정 | 결정적인 근거 |
|---|---|---|
| `0 1 0 / 1 0 0 / 1 1 1` | Player 1 승리 | 마지막 가로줄 전체가 `1`이다. |
| `0 1 1 / 1 0 0 / 1 1 0` | Player 0 승리 | 왼쪽 위부터 오른쪽 아래까지 `0`이다. |
| `0 1 0 / 1 0 0 / 1 0 1` | Tie | 완성된 승리 줄이 없다. |
| `0 0 0 / 0 0 0 / 0 0 1` | Invalid | 표식 수가 8 대 1이다. |
| `0 1 1 / 0 1 1 / 0 0 1` | Invalid | 첫 열의 `0`과 마지막 열의 `1`이 모두 완성된다. |

그림에서 첫 두 board의 표시된 행·대각선과 마지막 board의 두 세로줄을 구분해 보면, “같은 표식이 많다”와 “한 줄이 완성되었다”가 다른 조건임을 알 수 있다. STT의 불명확한 `role` 표현을 새로운 규칙으로 해석하지 않고 줄의 의미는 PDF로 확인한다. 어느 플레이어가 선공인지, 과거의 모든 수 순서가 실제로 가능한지까지 검사하는 규칙은 주어지지 않았다. 이 과제의 입력 가정과 판정 조건을 넘어서는 게임 이력을 추가하지 않는다.

### `N×N`에서 바뀌는 경계

확장은 먼저 `N`을 읽고 이어 `N²`개의 표식을 받는다. M008 p.26의 가정은 `N >= 3`이다. 승리 줄의 길이가 N, 행·열의 수가 N으로 바뀌므로 입력량, loop bounds, index 범위를 함께 바꿔 읽어야 한다. 단순히 모든 숫자 3을 무작정 바꾸는 작업이 아니다. Player 표식의 의미, 양쪽 승리의 충돌, 표식 수 차이 조건은 유지된다.

P.27의 첫 예는 `N = 4`이고 세 번째 행 `1 1 1 1`로 Player 1이 이긴다. 둘째는 **`N = 5`**이며 첫 행이 전부 0, 다음 행이 전부 1이어서 무효다. 마지막은 `N = 4`로 0이 7개, 1이 9개여서 차이 2로 무효다. [[courses/computer_programming/transcripts/2026-09-10|2026-09-10 STT 50:11–51:05]]의 하한 표현은 손상되어 있고 세 예를 모두 “four by four”라고 부르므로, `N >= 3`과 실제 `4/5/4` 크기는 PDF 근거로 명시한다. 손상된 발화를 복원한 것이 아니다.

## Player의 state와 동작을 분리하는 객체 설계

Lab03의 Fighting Game Simulation은 앞의 조건·반복·입력 개념을 객체들의 책임으로 나눈다. `Player`는 개별 ID·health와 행동, `Fight`는 두 플레이어의 상호작용과 round, `Main`은 입력과 전체 진행을 담당한다. [[courses/computer_programming/lectures/2026-09-17-lecture-06|2026-09-17 강의 노트 · Lab03]]의 녹음은 Player 설명 도중인 마지막 `17:39` 구간에서 끝난다. 아래의 정확한 선언과 후반 Fight/Main 요구는 **9월 19일 후취득한 공식 M014·M015로 확인한 자료 보충**을 포함한다. 녹음의 뒷부분을 새로 들었다는 뜻이 아니다.

### 초기 상태와 constructor의 역할

M014 pp.20–22는 private `String userId`, private `int health = 50`, modifier 없는 `Random random`을 제시한다. `userId`와 `health`를 외부에서 임의로 바꾸는 구조로 읽지 않는다. 초기값과 유지해야 할 범위는 다음처럼 다르다.

\[
h_{\text{initial}}=50,\qquad 0\le h\le50.
\]

`0`은 유효 상태 범위의 하한이면서 패배의 경계다. [[courses/computer_programming/transcripts/2026-09-17|2026-09-17 STT 15:41]]의 “health attribute should be and”는 type 부분이 잘린 표현이다. `int`는 후취득 자료로 확인하며 그 단어를 복원된 발화로 넣지 않는다. P.19의 설명 표기 `userID`와 실제 field `userId`, 오타 `attach()`와 선언 `attack(Player opponent)`도 구분한다.

`Player(String userId, int randomSeed)`는 ID와 seed를 받는다. PDF p.22의 예는 입력 ID를 field에 넣고 `new Random(randomSeed)`로 난수 객체를 초기화한다. 그러나 private skeleton의 Player constructor와 다섯 method bodies는 미구현이다. PDF의 초기화 예가 그 ZIP에 이미 완성되어 있다고 읽으면 안 된다. 추가 조회 methods를 만들 수 있지만 특정 getter 이름이나 개수는 지정되어 있지 않다.

Seed는 초기 health나 round 수가 아니라 난수 생성기의 시작 상태를 정하는 입력이다. 각 Player의 `random` reference를 하나의 class-wide static 상태와 혼동하지 않는다. 같은 seed만 외워 결과를 예측할 수도 없다. 사용하는 generator, method와 인자, 호출 순서가 같아야 난수열을 같은 방식으로 비교할 수 있다. 여기서는 특정 seed의 출력을 만들거나 현재 과제의 구현을 완성하지 않는다.

### 다섯 method의 변경 대상과 반환값

| Method | 책임 | 경계 또는 반환 계약 |
|---|---|---|
| `public void attack(Player opponent)` | 상대에게 피해 | 무작위 정수 1–5, 양 끝 포함; 상대 health는 음수가 되면 안 된다. |
| `private void getDamaged(int damage)` | 받은 지정량을 자기 health에 반영 | 별도 난수 피해를 다시 선택하는 책임이 아니다. |
| `public void heal()` | 자기 health 회복 | 무작위 정수 1–3, 양 끝 포함; health는 50을 넘지 않는다. |
| `isAlive()` | 생존 predicate | `health > 0`이면 `true`, 아니면 `false`다. |
| `public char getTactic()` | 행동 선택을 알림 | 공격 70%는 `'a'`, 회복 30%는 `'h'`를 반환한다. |

이 계약은 M014 p.21에 근거한다. PDF의 `public Boolean isAlive()`와 skeleton의 `public boolean isAlive()`는 type 철자가 다르다. `Boolean`은 wrapper, `boolean`은 primitive다. 생존 조건은 같지만 원본 선언까지 같다고 합치지 않는다.

**계약을 읽는 경계 예시**로, health `2`에서 damage `5`의 단순 차는 `-3`이지만 그 값을 최종 health로 두면 하한을 어긴다. Health `49`에서 회복 선택량 `3`의 합 `52`도 상한을 어긴다. 경계에서 멈추는 처리를 생각하면 각각 `0`, `50`이 되며 실제 변화량과 선택한 수는 다를 수 있다. 이 계산은 범위를 이해하는 설명이며 유일한 내부 구현을 지정하는 것은 아니다. `isAlive()`는 `1`에서 참, `0`에서 거짓이고 전체 게임의 진행이나 종료를 직접 수행하는 동작과도 구분한다.

[[courses/computer_programming/transcripts/2026-09-17|2026-09-17 STT 16:37–17:39]]는 공격·피해·회복·생존과 tactic을 설명하지만 마지막 문자는 미완성이고 공격 확률의 “70”에는 percent가 명시되지 않았다. `70%`, `'a'`/`'h'`는 PDF가 확립하는 상세다. 확률 70%라고 열 번마다 반드시 일곱 번 공격하는 것도 아니며, `'a'`를 반환했다고 상대 health를 이미 바꾼 것도 아니다. `random.nextInt()`와 `random.nextFloat()`는 hint이지 유일하게 허용된 구현 규칙이 아니다.

## Fight: reference 연결과 한 round의 순서

Player가 자기 상태를 관리하면 Fight는 그 동작을 연결한다. 이후 상세는 녹음 종료 뒤 범위에 해당하는 M014 pp.23–26의 자료 설명이다. `int timeLimit = 100`은 **최대 round 수**이며 초나 분이 아니다. `int currRound = 0`은 시작 전 상태이며 첫 출력 round는 1이다. `Player p1`, `Player p2`와 `Fight(Player p1, Player p2)`에는 modifier가 없다.

제공 constructor는 두 입력 references를 `this.p1`, `this.p2`에 저장한다. 내부에서 새로운 Player를 만들거나 복제하는 것이 아니다. Player constructor의 미구현 상태와 달리 이 reference 연결은 skeleton에 제공되어 있지만, 그것만으로 게임 진행 전체가 완성되지는 않는다. [M014 PDF p.26; M015의 private 구조 대조]

### 순차 행동에서 중간 상태가 중요한 이유

`public void proceed()`의 한 round는 먼저 `Round <Round_Number>`를 출력하고 p1의 tactic에 따른 행동을 진행한다. 그 뒤 p2가 살아 있으면 p2의 tactic에 따른 행동을 진행한다. 두 행동은 동시가 아니다. p1의 공격으로 p2의 health가 0이 되었다면 p2는 공격뿐 아니라 회복도 하지 않는다. 같은 round에서 회복해 되살아나도록 해석하면 명세가 달라진다. 마지막에 두 health를 다음 형식으로 출력한다. 꺾쇠 안은 실제 값이 들어갈 자리다. [M014 PDF p.25]

```text
<Player1_userID> health : <Player1_health>
<Player2_userID> health : <Player2_health>
```

이 순서를 이해하면 `currRound = 0`을 첫 출력 번호로 쓰거나, 행동 전 health를 최종 상태로 출력하는 실수를 피할 수 있다. 어느 getter로 읽을지는 별도 구현 선택이며 새로운 필수 이름을 만들 필요는 없다.

### 종료와 승자는 다른 반환 계약이다

`isFinished()`는 어느 한쪽 health가 0이 되거나 마지막 round가 완료되면 참이다. 두 조건을 동시에 요구하지 않는다. 둘 다 살아 있다면 round 99 완료는 아직 round 제한에 의한 종료가 아니고, round 100 완료는 종료다. Round 100을 건너뛰거나 101까지 진행하는 것은 다른 계약이다. PDF는 `Boolean`, skeleton은 primitive `boolean`으로 표기한다.

`public Player getWinner()`는 더 높은 health의 Player를 반환한다. Health가 같으면 **p2가 승자**다. 자료는 p1이 먼저 행동하는 것을 동점 처리 이유로 든다. 이는 draw나 p1 승리로 바꿀 수 없으며, 반환값은 ID String이나 참·거짓이 아니라 Player reference다. [M014 PDF p.25]

`Main`의 `public static void main(String[] args)`는 Scanner로 두 `int` seeds를 읽고, 자료가 정한 가상 ID `Gryffindor`, `Slytherin`의 Players를 생성해 Fight에 연결한다. 종료할 때까지 진행한 뒤 승자의 ID로 `<userID> is the winner!`를 출력한다. 입력 두 개를 health나 round 수로 해석하지 않는다. M014 p.28의 제목에 Constructor가 있어도 실제 제시한 것은 `main`이므로 별도 Main constructor 요구를 추가하지 않는다. Main의 연결 loop와 과제 bodies는 학습자가 구현할 부분으로 남는다. [M014 PDF pp.27–28]

## Lab04의 package 구조와 공통 게임 호출

Lab04는 [Packages](packages.md)와 [Encapsulation](encapsulation.md)을 게임 실행에 적용한다. **V4인 NM003이 최신 공급본**이며 live 확인이나 새 녹음에 근거한 순서는 아니다. V2인 NM002와 공통 요구는 유지하고 차이는 분리한다.

소스 구조는 `Platform` package 안의 `Platform` class와, 별도 package `Platform.Games` 안의 `Dice`, `ChamChamCham`이다. 따라서 `Platform.Platform`의 앞 단어는 package이고 뒤 단어는 class다. 게임 class의 package 선언은 정확히 다음과 같다.

```java
package Platform.Games;
```

NM003 pp.27–32의 화면 흐름은 `src`에서 New → Package로 `Platform`을 만든 다음 그 안에 class `Platform`, 하위 package `Platform.Games`, 두 게임 class를 만드는 순서다. `Platform`과 `Platform.Games`는 서로 다른 package이므로 접근 가능한 public class/method와 import 또는 완전한 이름이 필요하다. 대문자 `Platform`, `Games`와 `ChamChamCham` 철자를 임의의 스타일로 바꾸지 않는다.

| Class의 완전한 이름 | 제공해야 할 호출 |
|---|---|
| `Platform.Games.Dice` | `public int playGame()` |
| `Platform.Games.ChamChamCham` | `public int playGame()` |
| `Platform.Platform` | `public double run()`, `public void setRounds()` |

P.33의 `return -1`과 `return -0.0`은 배치용 임시 body다. 모든 게임이 패배하도록 이미 구현되었다는 뜻이 아니다. V2 p.24는 `Lab04_skeleton.zip`, v4 p.26은 `Lab04.zip`을 지칭하지만 **어느 Lab04 ZIP도 여기에는 공급되지 않았다**. 테스트 이름은 확인할 수 있어도 그 내부 비교나 seed 규칙은 확인되지 않는다. 앞의 M015는 Lab03 ZIP이므로 이를 Lab04의 구현으로 대체하지 않는다.

### Dice의 값·출력·반환을 분리하기

Dice는 보통의 여섯 면 주사위와 달리 **0–99의 정수**를 사용자와 상대가 한 번씩 얻는다. 반환 전에 사용자 값, 상대 값 순서로 공백 하나를 사이에 두고 출력한다. 더 큰 사용자 값은 `1`, 더 작은 값은 `-1`, 같은 값은 draw `0`을 반환한다. [NM003 PDF pp.34–35; NM002 PDF pp.32–33]

| 출력하는 두 값 | 비교 | 반환값 |
|---|---|---|
| 자료의 `47 11` | 사용자 승리 | `1` |
| 자료의 `40 42` | 사용자 패배 | `-1` |
| 같은 두 값 | 명세의 draw 조건 | `0` |

출력된 두 수와 caller가 받는 `int` outcome은 서로 다른 정보다. `Math.random()` hint의 범위를 이해하려면 `0 ≤ r < 1`을 100칸으로 대응할 때 정수 결과가 `0`부터 `99`까지 총 100개라는 경계를 확인하면 된다. 이는 자료 hint의 수학적 설명이며 제출용 `playGame()`을 완성한 것이 아니다. V4의 `10mins`는 실습 시간 안내이지 난수 규칙이나 프로그램 실행 제한이 아니다.

### ChamChamCham의 case-sensitive 입력

ChamChamCham도 같은 `public int playGame()` 형태를 제공하지만 규칙은 다르다. 사용자는 정확한 소문자 `up`, `down`, `left`, `right` 중 하나를 입력하고 상대는 무작위 pose(방향)를 정한다. 유효한 두 pose가 같으면 승리 `1`, 다르면 패배 `-1`이다. `Up`처럼 다른 문자열은 유효한 입력이 아니므로 패배 `-1`이다. 자동으로 소문자로 고치면 자료의 case-sensitive 요구를 바꾼다. [NM003 PDF pp.36–37; NM002 PDF pp.34–35]

유효한 입력일 때는 반환 전에 사용자 pose와 상대 pose를 공백으로 구분해 출력한다. 자료의 `up right`는 `-1`, `left left`는 `1`이다. Dice와 달리 **같은 값이 draw가 아니라 승리**이고 별도의 draw 반환 규칙이 없다. Invalid 입력에 대한 추가 오류 문구나 재입력 loop는 명시되지 않았다. “Similar interface”는 같은 호출 형태라는 뜻이지 골격에 Java `interface`와 `implements` 선언이 있다는 뜻은 아니다.

## Platform의 한 번만 가능한 설정과 승률

`setRounds()`는 단순히 원하는 값을 매번 덮어쓰는 setter가 아니다. 초기 round 수는 `1`이고, **첫 호출만 5–10 inclusive에서 무작위로 설정**한다. 이후 호출은 그 값을 다시 바꾸지 못한다. 예를 들어 첫 호출이 6을 정했다면 두 번째 호출 뒤에도 6이어야 한다. 처음부터 5–10으로 초기화되어 있다고 읽거나 매 호출마다 다시 뽑는 것은 다른 상태 계약이다. [NM003 PDF p.39; NM002 PDF p.37]

`run()`은 먼저 console에서 정수 `0` 또는 `1`을 읽는다. `0`이면 Dice, `1`이면 ChamChamCham을 설정된 round 수만큼 실행하고 `double` 승률을 반환한다. 설정과 실행은 서로 다른 책임이다.

\[
\text{win rate}=\frac{\text{사용자가 이긴 round 수}}{\text{전체 수행 round 수}}.
\]

Dice의 draw는 승리는 아니지만 수행한 round이므로 분모에 포함된다. 예를 들어 **설명용 outcome trace**에서 네 round가 승리·패배·draw·승리이면 승률은 `2/4 = 0.5`다. Draw를 제외해 `2/3`으로 계산하면 다른 비율이다. 또 두 정수로 먼저 나누면 `4/6`이 `0`으로 잘릴 수 있으므로 `double` 비율 계산과 integer division을 구별해야 한다.

0/1 이외 입력의 처리, 특정 seed, 정확한 private field 이름·getter 개수는 자료가 지정하지 않았다. Generalization(일반화)의 필요성을 후속 inheritance와 연결한다는 NM003 p.38의 설명도 새 상속 구조를 과제 필수조건으로 만들지는 않는다.

### 두 console 예에서 실제 round 세기

[NM003 PDF p.40](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-040)과 NM002 p.38은 같은 두 실행을 보여 준다.

| Round | Dice 출력 쌍 | 사용자 결과 | ChamChamCham 출력 쌍 | 사용자 결과 |
|---|---|---|---|---|
| 1 | `73 38` | 승리 | `up left` | 패배 |
| 2 | `58 10` | 승리 | `left up` | 패배 |
| 3 | `95 26` | 승리 | `down right` | 패배 |
| 4 | `69 39` | 승리 | `down down` | 승리 |
| 5 | `2 65` | 패배 | `up right` | 패배 |
| 6 | `38 77` | 패배 | `down up` | 패배 |

첫 실행은 `4/6 = 2/3`이고 화면의 `0.6666667`은 그 근사 표시다. 둘째는 같은 pose가 네 번째 하나뿐이어서 `1/6`, 화면에는 `0.16666666666666666`이 보인다. 오른쪽 console의 단독 `down` 입력 행과 다음 `down down` 출력 행을 두 round로 세면 안 된다. 둘은 한 번의 입력과 그 결과다.

두 예가 모두 여섯 round라는 사실은 허용 범위를 6으로 고정하지 않는다. 또한 서로 다른 소수 자릿수를 보고 특정 출력 formatter를 새 필수조건으로 만들지 않는다. 요구는 `double` 승률 반환이며, 예시 출력의 표시와 반환 계약을 분리해 읽어야 한다.

## 핵심 정리

- 첫 실패만 보고하는 validator에서는 검사 순서도 계약이다. Board에서는 승리 후보보다 invalid 조건을 먼저 확정한다.
- Player는 자기 상태·행동, Fight는 순차 round, Main은 입력과 전체 흐름을 담당한다.
- 확률적 행동 선택은 실제 행동 수행이나 열 번 중 정확한 횟수 보장이 아니다.
- Dice의 같은 수는 draw지만 ChamChamCham의 같은 유효 pose는 승리다. 입력 대소문자도 명세다.
- `setRounds()`는 첫 호출만 설정하고 `run()`은 승리/전체 round를 double로 돌려준다. Draw도 분모에 포함한다.

## 확인·연습문제

### 입력과 board

#### 확인 Q01 · 한 줄과 종료 신호

`Computer Programming`과 `exit`를 입력할 때 echo 단계가 어떻게 다른가? Scanner를 준비했다는 사실만으로 한 줄 계약을 충족하는가?

<details><summary>해설 보기</summary>

첫 문자열은 공백까지 포함한 한 줄 전체를 그대로 출력하고 반복한다. `exit`는 종료 신호라 자료 예에서 다시 echo하지 않는다. 토큰 하나만 읽어 Computer만 출력하면 계약이 달라진다. Scanner(System.in)은 입력 준비 hint이며 읽는 단위·종료 조건·echo 순서를 별도로 맞춰야 한다.

**확인 기준:** 공백 보존과 exit 비echo를 확인한다.

</details>

#### 확인 Q02 · 첫 실패와 문자 범위

길이·구분자·digit의 검사 순서를 적고 원본 `2018-1234`, `2018_12345`, `e018-12345`, `2018-12345`를 분류하라. Digit 안/밖 및 영문 소문자·대문자 조건을 설명하라.

<details><summary>해설 보기</summary>

길이 10→index 4의 '-'→나머지 모두 digit 순서다. 네 입력은 길이 오류, 구분자 오류, digit 오류, 성공이다. 길이 오류는 `The input length should be 10.`, digit 오류는 `Contains an invalid digit.`, 성공은 입력 뒤 `is valid.`를 붙인다. 첫 실패만 보고하므로 digit 검사를 시험할 입력은 앞 둘을 통과해야 한다. 길이 선검사는 짧은 문자열의 charAt(4)도 피한다. Digit는 `ch>='0' && ch<='9'`, 밖은 `ch<'0' || ch>'9'`; 소문자/대문자는 각각 'a'–'z'/'A'–'Z'의 두 경계를 모두 만족한다. 문자 '0'은 정수 0이 아니며 모든 Unicode 숫자가 아니다. 구분자 메시지의 인용부호 충돌은 그대로 남긴다.

**확인 기준:** 순서·첫 오류·&&/||의 논리와 문자 상수를 확인한다.

</details>

#### 확인 Q03 · 다섯 board의 판정

0/1 표식과 행 우선 저장을 설명하라. 다음 boards를 순서대로 판정하고 이유를 적어라: `010/100/111`, `011/100/110`, `010/100/101`, `000/000/001`, `011/011/001`.

<details><summary>해설 보기</summary>

0과 1은 두 플레이어 표식이며 0은 빈칸이 아니다. 아홉 입력을 3개씩 행으로 저장하고 `printBoard`로 배치를 확인한다.

| Board | 판정 | 이유 |
|---|---|---|
| `010/100/111` | Player 1 win | 마지막 행 111; count 4/5 |
| `011/100/110` | Player 0 win | 주대각선 000; count 4/5 |
| `010/100/101` | Tie | 완성 줄 없음; count 5/4 |
| `000/000/001` | Invalid | count 8/1로 차이 7 |
| `011/011/001` | Invalid | 첫 열 000과 마지막 열 111이 모두 승리 |

승리에는 가로·세로·대각선 전체가 같아야 한다. 양쪽 승리 또는 count 차이>1이면 무효가 우선하므로 한 줄을 찾자마자 승리를 확정하지 않는다. 선공·전체 수 이력 규칙은 추가하지 않는다.

**확인 기준:** 저장·다섯 판정·서로 다른 무효 원인을 확인한다.

</details>

#### 확인 Q04 · N에 따른 경계

`N=5`에서 행의 앞 세 값만 같은 경우 승리인가? 입력량·index·승리 길이에서 바뀌는 것과 유지되는 규칙, p.27의 4/5/4 예를 설명하라.

<details><summary>해설 보기</summary>

승리는 N개 전체가 같아야 하므로 앞 세 값만으로는 부족하다. N부터 읽고 N² 표식을 저장하며 N행·N열과 각 줄의 N개를 검사한다. 자료는 N>=3이고 표식 0/1, 양쪽 승리, count 차이 규칙은 유지된다. 첫 N=4 예는 세 번째 행 1111로 Player 1 승리, 둘째 N=5는 완성 0행·1행으로 Invalid, 마지막 N=4는 0이 7개/1이 9개라 Invalid다. 모두 4×4라고 한 말과 손상된 하한 대신 크기·N>=3은 PDF에 근거한다.

**확인 기준:** N² 입력·N개 줄·유지 규칙·세 예의 다른 이유를 확인한다.

</details>

### 객체와 round

#### 확인 Q05 · Player 상태와 생성

Player/Fight/Main의 책임, Player fields의 정확한 선언·초기 상태·constructor 입력을 설명하라. PDF의 초기화 예와 ZIP의 완성 상태는 같은가?

<details><summary>해설 보기</summary>

Player는 ID·health·행동, Fight는 상호작용·round, Main은 입력·전체 진행이다. Player는 private String userId, private int health=50, modifier 없는 Random random을 둔다. Health 범위는 0–50이고 0은 패배 경계다. Player(String userId,int randomSeed)는 ID와 난수 초기화 입력을 받는다. PDF는 ID 대입/new Random(randomSeed)를 보여 주지만 ZIP의 constructor와 다섯 body는 미구현이다. 설명 userID/attach와 선언 userId/attack도 구별한다. Getter는 추가 가능하지만 필수 이름·개수는 없다. 끊긴 STT의 health type을 복원한 발화로 만들지 않는다.

**확인 기준:** 책임·field type/access·50과 0의 의미·자료/골격 차이를 확인한다.

</details>

#### 확인 Q06 · 다섯 method의 계약

(a) `attack`·`getDamaged`·`heal`의 변경 대상·범위·반환을 구별하라. (b) Health 2에 피해 5, health 49에 회복 3의 경계와 `isAlive()`를 설명하라. (c) `getTactic()`의 반환과 확률 70%, 자료별 type 차이는?

<details><summary>해설 보기</summary>

(a) `public void` attack(Player opponent)는 상대에 1–5의 선택 피해를 주고 private void getDamaged(int damage)는 지정량을 자기 상태에 적용하며 다시 난수를 뽑는 역할이 아니다. `public void` heal은 자기 health를 1–3만큼 회복시킨다. 

(b) 경계에서 멈추는 해석이면 두 사례는 0과 50으로 제한되며 -3/52는 불가다. `isAlive()`는 health>0, 즉 1에서 참/0에서 거짓인 predicate다. 

(c) PDF Boolean과 skeleton boolean 차이는 남긴다. `public char` getTactic은 70% 'a'/30% 'h' 선택을 반환할 뿐 공격을 수행하지 않는다. 열 번에 꼭 일곱 공격도 아니다. 비율·문자는 PDF로 확립되며 nextInt/nextFloat는 hints다.

**확인 기준:** 대상·범위·경계·predicate·선택 반환을 모두 구별한다.

</details>

#### 확인 Q07 · Reference 연결과 한 round

Fight constructor, timeLimit=100, currRound=0의 뜻은? 첫 round의 출력·행동 순서와 p1 뒤 p2가 죽었을 때를 설명하라.

<details><summary>해설 보기</summary>

Constructor는 전달된 Player references를 저장해 기존 객체에 연결하며 생성·복제하지 않는다. Fields와 constructor에 modifier는 없다. `timeLimit`은 최대 round 수이지 시간이 아니고 currRound=0은 시작 전이라 첫 출력은 Round 1이다. 먼저 round 번호, p1 tactic에 맞는 행동, 그 뒤 살아 있는 p2의 행동, 마지막 두 health를 출력한다. p1이 p2를 0으로 만들면 p2는 공격·회복 모두 하지 않는다. 출력은 `<Player1_userID> health : <Player1_health>` 다음 Player2 형식으로 실제 값을 넣는다. Getter 이름은 명세가 정하지 않는다.

**확인 기준:** Alias 연결, 첫 번호, 중간 생존 검사, 최종 상태 출력 순서를 확인한다.

</details>

#### 확인 Q08 · 종료와 승자 반환

둘 다 살아 있을 때 round 99/100 완료와 한쪽 health 0의 종료를 비교하라. 마지막 동점의 승자·반환 type, PDF/ZIP 차이는?

<details><summary>해설 보기</summary>

종료는 한쪽 health=0 또는 마지막 round 완료 중 하나면 된다. 둘 다 살아 있으면 99 완료는 아직 아니고 100 완료는 종료이며 101까지 진행하지 않는다. Health가 높은 Player가 승자이고 같으면 선행 p1을 고려한 명세에 따라 p2다. `getWinner()`는 Player reference이지 ID나 boolean이 아니다. PDF의 isFinished는 Boolean, skeleton은 boolean이며 의미가 같아도 선언이 동일하지 않다. `isFinished()`의 참/거짓과 getWinner의 객체 반환은 별개다.

**확인 기준:** OR 종료·99/100 경계·p2 동점·Player 반환을 확인한다.

</details>

#### 확인 Q09 · Main과 seed

Main의 두 int 입력에서 승자 메시지까지의 연결을 설명하라. Seed만 같으면 임의 구현의 결과도 같다고 할 수 있는가?

<details><summary>해설 보기</summary>

두 int는 Player별 random seeds다. 자료의 가상 ID Gryffindor/Slytherin으로 Players를 만들고 그 references를 Fight에 전달해 종료까지 진행한 뒤 승자 Player의 ID로 `<userID> is the winner!`를 출력한다. Seed는 health나 round가 아니며 Player별 Random reference를 하나의 static 상태와 혼동하지 않는다. 같은 난수 trace를 비교하려면 generator·호출 methods·인자·순서도 같아야 한다. P.28 Constructor 제목이 별도 Main constructor를 요구하지 않으며 ZIP main body도 미완성이다. 이는 녹음 cutoff 이후 자료 보충이다.

**확인 기준:** 입력 용도·객체 연결·reference에서 ID·seed 비교 조건을 확인한다.

</details>

### 게임과 Platform

#### 확인 Q10 · Lab04의 정확한 소속

Platform.Platform과 Platform.Games의 구조·생성 순서·methods를 적고 placeholder 및 ZIP 한계를 설명하라.

<details><summary>해설 보기</summary>

`src`에서 package Platform→그 안 class Platform→별도 package Platform.Games→Dice/ChamChamCham 순서다. 완전한 이름은 Platform.Platform, Platform.Games.Dice, Platform.Games.ChamChamCham이고 games 선언은 `package Platform.Games;`다. Games와 Platform은 별도 package라 접근 가능한 public class/method와 import 또는 완전한 이름이 필요하다. 두 게임은 public int playGame(), Platform은 public double run()/public void setRounds()를 제공한다. -1/-0.0 body는 배치 placeholder이지 완성 결과가 아니다. V2의 Lab04_skeleton.zip과 v4의 Lab04.zip 모두 미공급이며 M015는 Lab03다. 보이는 Test 이름으로 내부 검사를 추측하지 않는다.

**확인 기준:** 소속 대소문자·signature·별도 package·미공급 archive를 확인한다.

</details>

#### 확인 Q11 · Dice의 출력과 반환

Dice의 값 범위와 사용자/상대 순서를 설명하고 `47 11`, `40 42`, 같은 수의 반환을 구하라. Math.random hint의 양끝은?

<details><summary>해설 보기</summary>

양쪽은 각각 0–99 정수 한 개를 얻고 반환 전에 사용자 값 먼저, 공백 하나, 상대 값을 출력한다. 세 경우의 반환은 1,-1,0이다. 0은 출력 숫자 자체가 아니라 동점 outcome일 수도 있으므로 역할을 구별한다. 0≤r<1을 100칸에 대응하면 정수 후보는 0부터 99이고 100은 포함하지 않는다. 보통 주사위의 1–6 규칙을 쓰지 않는다. V4 10mins는 실습 시간이며 TestDice의 seed·내부 비교는 제공되지 않았다.

**확인 기준:** 두 경계·출력 순서·세 반환·hint 범위를 확인한다.

</details>

#### 확인 Q12 · Pose의 대소문자와 일치

`Up`, 유효 `up/right`, `left/left`의 결과를 구하고 Dice의 동점과 비교하라. Similar interface가 Java interface 선언을 뜻하는가?

<details><summary>해설 보기</summary>

`Up`은 정확한 소문자 up/down/left/right가 아니므로 -1이다. 유효 up/right도 다르므로 -1, left/left는 같아서 1이다. 상대 pose는 무작위이며 유효 입력에서는 사용자/상대 pose를 공백으로 출력한 뒤 반환한다. 같은 pose는 승리라 Dice의 같은 값 draw 0과 다르며 별도 draw는 없다. 자동 소문자 변환·추가 오류 메시지·재시도를 필수로 만들지 않는다. 공통 public int playGame() 호출 형태라는 뜻이지 공급 골격에 interface/implements가 선언되었다는 뜻은 아니다.

**확인 기준:** Invalid·다름·같음의 세 경로와 추정하지 않을 동작을 확인한다.

</details>

#### 확인 Q13 · 한 번 설정과 비율

최초 round 수, 첫·둘째 setRounds 효과와 run의 0/1 선택을 설명하라. 승리·패배·draw·승리의 비율과 int division 함정은?

<details><summary>해설 보기</summary>

최초는 1, 첫 호출만 5–10 inclusive에서 무작위 설정하고 그 뒤에는 변경하지 않는다. 첫 결과가 6이면 둘째 뒤에도 6이다. `run()`은 0이면 Dice, 1이면 ChamChamCham을 설정 횟수만큼 실행하고 double 승률을 반환한다. 네 결과에서 2승/4회=0.5이며 draw도 분모에 남아 2/3이 아니다. 4/6을 int끼리 먼저 나누면 0으로 절단되어 뒤늦게 double로 바꿔도 복원되지 않는다. 범위 밖 선택 처리·seed·필드명·getter 수는 새로 정하지 않고 상속 구조도 필수화하지 않는다.

**확인 기준:** 일회 설정·게임 선택·draw 분모·나눗셈 type을 확인한다.

</details>

#### 확인 Q14 · Console에서 round 세기

자료의 Dice 쌍 `73/38,58/10,95/26,69/39,2/65,38/77`와 pose 쌍 `up/left,left/up,down/right,down/down,up/right,down/up`의 비율을 구하라. 입력 down과 출력 down down을 어떻게 세는가?

<details><summary>해설 보기</summary>

Dice는 앞 네 승리/전체 여섯=4/6=2/3, pose는 네 번째만 같아 1/6이다. 단독 down과 뒤의 down down은 한 round의 입력과 출력이지 둘이 아니다. 표시 0.6666667과 0.16666666666666666은 비율의 예시 표현이며 특정 반올림 formatter를 필수화하지 않는다. 두 예 모두 6회여도 설정 범위가 6으로 고정되지 않는다. V2 p.38과 v4 p.40의 값은 같으며 새 수치 규칙이 도입된 것은 아니다.

**확인 기준:** 4/6·1/6, 입력/출력 한 쌍, 근삿값과 계약 차이를 확인한다.

</details>

### 적용 연습

#### 연습 P01 · 실패 단계 격리

새로 만든 강의·자료 기반 일반 연습이다. 후보의 날짜 계산 문제는 윤년·날짜 계약이고 파일 입력 문제는 예외·자원 처리가 필요하여 이 실습의 직접 기출 형식으로 삼지 않는다. `x`로 digit 검사를 검증했다는 주장과, N=5 행의 앞 세 표식만 같아서 승리라는 주장을 평가하라. 각 주장의 문제와 이를 드러낼 확인 방법만 제시하라.

<details><summary>해설 보기</summary>

`x` 입력은 길이가 1이라 첫 단계에서 끝나 digit 검사를 관찰하지 못한다. 길이 10·index 4 hyphen을 만족하면서 다른 위치에 영문자가 있는 `e018-12345`로 digit 단계만 드러낼 수 있다. N=5에서 앞 세 값만 검사하면 길이 조건을 누락한다. `[0,0,0,1,1]` 행은 첫 셋이 같아도 전체 줄은 아니므로 그 행 자체는 승리 줄이 아니다. 전체 board 판정은 다른 줄·counts까지 따로 확인해야 한다.

**확인 기준:** 도달 조건과 전체 길이를 설명하며 완성 validator나 board 구현으로 확장하지 않는다.

</details>

#### 연습 P02 · 행동 전후의 판정

새로 만든 자료 기반 일반 연습이며 이 round 계약의 직접 기출 근거는 없다. p1 행동 직전 p2 health는 2이고 선택된 공격 피해는 5다. 검토자가 p2의 예정 heal을 먼저 실행하거나, 둘 다 살아 있는 round 99 직후 종료하거나, getWinner에서 ID만 반환하려 한다. 세 변경이 왜 명세와 다른지 설명하라.

<details><summary>해설 보기</summary>

원래 순서는 p1 뒤 p2이며 피해 하한을 적용하면 p2는 0이다. 중간 생존 검사에서 탈락해 heal까지 하지 않으므로 먼저 회복시키면 순서와 생존 조건을 바꾼다. 둘 다 살아 있는 99 완료는 최종 100 완료가 아니므로 제한 종료 조건이 아니다. `getWinner()`는 Player reference를 반환하고 Main이 ID를 읽어 메시지를 만든다. ID만 반환하면 책임과 return type이 달라진다. 선택 피해는 설명 입력이지 seed에서 계산한 결과가 아니다.

**확인 기준:** 순서·중간 상태·100 경계·반환 책임 네 항목을 확인한다.

</details>

#### 연습 P03 · 같은 결과처럼 보이는 다른 계약

새로 만든 자료 기반 일반 연습이다. 이 두 게임과 일회 설정을 함께 다루는 기출 형식 근거는 없다. 첫 setRounds가 5를 정한 뒤 다시 호출했다. Dice의 다섯 outcome이 `1,0,-1,1,0`이라면 횟수·승률은? 같은 두 pose에 draw 0을 반환하거나 입력/출력 줄을 각각 round로 세는 제안도 평가하라.

<details><summary>해설 보기</summary>

둘째 설정은 변경하지 않아 5회이고 승리 둘/전체 다섯=0.4다. 두 draw도 분모에 포함한다. 같은 유효 pose는 ChamChamCham에서 1이지 Dice처럼 0이 아니다. 두 게임의 playGame signature가 같아도 결과 조건까지 같지는 않다. Console 입력과 그 결과 출력은 한 round라 각 줄을 세면 분모가 잘못된다. 완성 게임 body나 미공급 Test의 내부를 정할 필요는 없다.

**확인 기준:** 일회 설정·5회·0.4·게임별 equality 의미·round 단위를 확인한다.

</details>

### 짧은 복습 계획

Q02–Q04를 실패 이유별로 다시 분류한 뒤 Q06–Q09를 상태·반환 표로 회상한다. 다음 날 Q13–Q14와 P03을 계산해 draw·입력 행·둘째 설정 호출을 잘못 세지 않는지 확인한다.

## 출처

Lab02는 9월 10일, Lab03의 일부는 9월 17일 녹음과 연결된다. 9월 17일 녹음은 Player 설명의 17:39 구간에서 끝나며, 정확한 type·확률·문자와 Fight/Main의 후반 요구는 9월 19일 얻은 공식 자료로 보충했다. 끊긴 말은 복원된 발화가 아니다. Lab04 v2/v4는 새 녹음 없는 자료 복습이다. 원본 과제 ZIP과 행정 metadata는 공개 링크를 제공하지 않으며 Lab04 ZIP/Test 내부는 미공급이다. 실습 전체 구현은 다루지 않는다.

### 날짜별 노트와 녹취

- [[courses/computer_programming/lectures/2026-09-10-lecture-04|2026-09-10 · 강의 노트]]

- [[courses/computer_programming/lectures/2026-09-17-lecture-06|2026-09-17 · 강의 노트]]

- [[courses/computer_programming/transcripts/2026-09-10|2026-09-10 · 보정 녹취 · 09:38; 15:25–18:22; 38:21–39:19; 50:11–51:05]]

- [[courses/computer_programming/transcripts/2026-09-17|2026-09-17 · 보정 녹취 · 14:47–17:39 (녹음 마지막 구간)]]

### 자료와 해당 페이지

- [Lab02 v4 · PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab02.v4.pdf) — [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-016), [p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-017), [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-018), [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-019), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-020), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-021), [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-022), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-023), [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-024), [p.25](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-025), [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-026), [p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-027)

- [Lab03 v2 · PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab03.v2.pdf) — [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-018), [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-019), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-020), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-021), [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-022), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-023), [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-024), [p.25](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-025), [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-026), [p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-027), [p.28](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-028)

- [Lab04 v2 · PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab04.v2.pdf) — [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-024), [p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-032), [p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-033), [p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-034), [p.35](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-035), [p.36](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-036), [p.37](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-037), [p.38](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-038)

- [Lab04 v4 · PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab04.v4.pdf) — [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-026), [p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-027), [p.28](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-028), [p.29](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-029), [p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-030), [p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-031), [p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-032), [p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-033), [p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-034), [p.35](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-035), [p.36](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-036), [p.37](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-037), [p.38](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-038), [p.39](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-039), [p.40](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-040)

이 단원과 직접 대응하는 기출 형식 근거가 없어 P 문제는 강의·자료 기반 일반 연습으로 제시한다.
