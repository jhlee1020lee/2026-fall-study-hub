---
title: "입력 검증·Board 판정·객체 상호작용 실습"
description: "입력 검증·board 규칙·Player/Fight/Main 계약을 제한된 trace와 사례로 확인한다."
course: "computer_programming"
unit_id: "lab-applications"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["Lab02 v4.pdf", "Lab02 official assignment metadata", "Lab03 v2.pdf", "Lab03 skeleton.zip"]
private_source_assets: ["Lab02 official assignment metadata", "Lab03 skeleton.zip"]
source_lectures: ["courses/computer_programming/lectures/2026-09-10-lecture-04", "courses/computer_programming/lectures/2026-09-17-lecture-06"]
---

실습 명세를 입력·검사 순서·상태 변경·출력의 계약으로 나누어 읽는다. Board 판정과 객체 상호작용을 손으로 추적하며 구현 전에 확인할 사례를 고른다.

## 한 줄 입력과 exit sentinel의 계약

실습을 설계할 때는 먼저 입력 단위와 각 입력의 처리 결과를 정해야 한다. [[courses/computer_programming/units/types-expressions|Scanner와 String]] 및 [[courses/computer_programming/units/control-flow|분기·반복]]을 사용하는 Lab02의 첫 단계는 한 줄을 읽어 그대로 출력하는 일을 반복하는 것이다. `exit`는 일반 데이터가 아니라 반복을 끝내는 sentinel(종료 신호)이다.

[Computer Programming M008, Lab02 PDF pp.16–17](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab02.v4.pdf)의 Input/Output 표시는 다음과 같이 읽는다.

| 입력 한 줄 | 요구되는 반응 |
| --- | --- |
| `abc` | `abc`를 출력하고 계속 읽는다. |
| `Computer Programming` | 공백을 포함한 전체 줄을 출력한다. |
| `2018-12345` | 그 줄을 출력한다. |
| `exit` | 종료한다. 원본 예에는 exit의 echo 출력이 없다. |

원본 그림의 마지막 exit에는 Input 표시만 있고 이어지는 Output이 없다. 따라서 무조건 먼저 echo한 다음 종료를 판단하면 예제와 달라진다. [[courses/computer_programming/transcripts/2026-09-10|2026-09-10 STT]] 09:38의 설명과 함께, 입력 읽기·일반 처리·종료를 별개의 경로로 생각하면 된다. `Scanner(System.in)`은 입력 준비의 hint이며, 한 줄 안의 공백은 종료 신호가 아니다.

## Ordered validation과 첫 실패의 우선순위

Student ID Validator의 다음 단계는 `XXXX-XXXXX` 형태의 문자열을 검사한다. 이 숫자 문자열들은 과제 자료의 예시이지 특정 학생의 신원 정보가 아니다. M008 PDF p.18(인쇄 slide 19)은 다음 **순서**를 요구한다.

| 순서 | 검사 | 실패 또는 성공의 의미 |
| --- | --- | --- |
| 1 | 길이가 10인가 | 아니면 `The input length should be 10.` |
| 2 | 다섯 번째 문자, index 4가 `'-'`인가 | 아니면 구분자 오류 메시지 |
| 3 | Index 4를 제외한 모든 문자가 digit인가 | 아니면 `Contains an invalid digit.` |
| 4 | 앞의 검사를 모두 통과했는가 | 입력 뒤에 ` is valid.`를 붙인다. |

여러 조건에 동시에 어긋나도 먼저 실패한 검사에 대응하는 메시지가 우선한다. 길이를 먼저 확인하면 너무 짧은 문자열에서 `charAt(4)`를 성급히 읽는 문제도 막는다. 따라서 validation(유효성 검사)은 조건 집합뿐 아니라 안전한 평가 순서와 보고 순서의 계약이다. [[courses/computer_programming/transcripts/2026-09-10|2026-09-10 STT]] 15:25

`charAt(index)`는 한 문자를 반환한다. 자료의 첫 번째 AND 조건은 양끝 문자 `'0'`과 `'9'`를 포함하는 digit 구간을 판정하고, 두 번째 OR 조건은 De Morgan 법칙에 따라 첫 번째 조건을 부정하여 그 여집합인 범위 밖을 판정한다.

```java
ch >= '0' && ch <= '9'  // within the required digit range
ch < '0' || ch > '9'    // outside that range
```

두 줄은 `char ch`의 값을 분류하는 expression 예이며 완성 validator가 아니다. `'0'`은 숫자 0 자체가 아니라 문자다. 이 조건은 ASCII digit 구간에 해당하며, 모든 숫자 모양 Unicode 문자를 허용하지 않는다. 같은 자료는 소문자 `'a'`…`'z'`, 대문자 `'A'`…`'Z'`도 별도 연속 범위로 소개한다.

원본 사례를 순서대로 적용하면 `2018-1234`는 길이, `2018_12345`는 구분자, `e018-12345`는 digit에서 실패한다. `2018-12345`는 통과하여 `2018-12345 is valid.`를 출력한다. Digit 실패 예는 먼저 길이와 구분자를 통과해야 세 번째 검사에 도달한다.

구분자 메시지는 PDF p.18에서 `Fifth character should be` 뒤 hyphen을 backticks로 감싸고 p.20(인쇄 slide 21)에서는 곡선 인용부호로 감싼다. 두 페이지의 차이는 남아 있으므로 어느 표기를 새로운 공식 채점 문자열로 확정하지 않는다.

## 3×3 board의 저장과 판정

다음 실습은 아홉 정수를 [[courses/computer_programming/units/arrays|2D array]]에 저장한다. 입력은 0 또는 1이며 각각 Player 0·Player 1의 표식이다. **0은 빈칸이 아니다.** M008 PDF p.23(인쇄 slide 25)의 입력 순서는 다음 board를 만든다.

```text
input: 0 1 0 1 0 0 1 1 1

0 1 0
1 0 0
1 1 1
```

한 행을 채운 뒤 다음 행으로 이동한다. `printBoard`는 판정 전에 이 배치가 맞는지 관찰하는 수단이다. 잘못 저장한 board에서 판정 조건만 고쳐도 문제의 원인은 사라지지 않는다.

### Winning line과 invalid 상태를 함께 보기

가로·세로·대각선 한 줄 전체가 같은 player의 표식이면 winning line(승리 줄)이다. 하지만 한 줄을 발견했다고 즉시 최종 winner를 선언할 수는 없다. 두 player가 모두 winning line을 갖거나, 표식 개수 차이가 1보다 크면 `Invalid game.`이다. 유효한 board에서 한 player만 이기면 `Player 0 win.` 또는 `Player 1 win.`, 누구도 이기지 않으면 `Tie.`다. [[courses/computer_programming/transcripts/2026-09-10|2026-09-10 STT]] 38:21 및 M008 PDF pp.24–25

PDF p.25의 다섯 board를 행 단위로 나누어 읽으면 다음과 같다. `/`는 행 구분이며 실제 입력 기호가 아니다.

| Board의 세 행 | 확인할 근거 | 판정 |
| --- | --- | --- |
| `010 / 100 / 111` | 마지막 행 전체가 1 | `Player 1 win.` |
| `011 / 100 / 110` | 주대각선 전체가 0 | `Player 0 win.` |
| `010 / 100 / 101` | 어느 player도 완성 줄이 없고 개수 차이는 1 | `Tie.` |
| `000 / 000 / 001` | 0이 8개, 1이 1개 | `Invalid game.` |
| `011 / 011 / 001` | 첫 열은 모두 0, 마지막 열은 모두 1 | `Invalid game.` |

첫 board의 개수는 0이 4개, 1이 5개다. 세 번째는 0이 5개, 1이 4개이고, 각 행·열·두 대각선을 확인해도 완성 줄이 없다. 마지막은 표식 수 차이만 보면 1이지만 **양쪽 승리**라는 별도 무효 조건에 걸린다. 두 검사를 하나로 뭉치면 이런 차이를 놓친다.

자료가 제시한 것은 이 board 판정 계약이다. 누가 선공인지, 중간에 승리가 났는데 계속 두었는지 등 모든 실제 게임 이력의 적법성을 검증하는 추가 규칙까지 임의로 넣지는 않는다.

### N×N으로 일반화할 때 바뀌는 것

M008 PDF p.26은 먼저 `N`을 읽고, 이어 `N × N`개의 표식을 읽으며 `N >= 3`을 가정한다. Winning line의 길이는 3에서 N으로, 행·열의 수와 index bounds도 N에 맞게 바뀐다. Player 표식의 의미, 양쪽 승리 충돌, 표식 개수 차이에 관한 조건은 유지된다.

PDF p.27에는 서로 다른 크기의 세 사례가 있다.

| 자료의 사례 | 계산·판정 근거 | 결과 |
| --- | --- | --- |
| 첫 4×4 | 세 번째 행이 `1 1 1 1` | `Player 1 win.` |
| 5×5 | 첫 행은 모두 0, 둘째 행은 모두 1 | `Invalid game.` |
| 마지막 4×4 | 0이 7개, 1이 9개라 차이가 2 | `Invalid game.` |

N=5에서 세 칸만 연속으로 같아도 된다고 보면 이전 3×3 규칙을 잘못 옮긴 것이다. 전체 길이 5의 줄이 필요하다. [[courses/computer_programming/transcripts/2026-09-10|2026-09-10 STT]] 50:11 주변에서 세 예를 모두 4×4라고 부르는 표현과 손상된 N 하한 발화는 자료의 실제 4·5·4 크기 및 `N >= 3`과 구별한다. 일반화는 코드 안의 숫자 3을 모두 바꾸는 작업보다, 입력량·검사할 줄·각 index의 의미를 다시 맞추는 일이다.

## Player·Fight·Main의 책임 분리

Lab03 Fighting Game Simulation은 [[courses/computer_programming/units/objects-references|Object 상태와 reference 전달]], [[courses/computer_programming/units/methods|Method 계약]], [[courses/computer_programming/units/encapsulation|Encapsulation]]을 하나의 상호작용에 연결한다. Player는 개별 ID·health와 행동, Fight는 두 players의 interaction과 rounds, Main은 입력과 전체 진행을 맡는다. 한 class에 모든 책임을 몰아넣지 않아야 변경 대상과 호출 관계를 추적하기 쉽다.

[[courses/computer_programming/transcripts/2026-09-17|2026-09-17 STT]] 14:47–17:39에는 Player 설명의 일부가 남아 있으며 17:39에서 character 반환 설명 도중 끝난다. 아래의 정확한 fields·수치·Fight·Main 계약은 **9월 19일 확보된 공식 Lab03 자료에 근거한 보충**이다. 녹음의 없는 후반부를 복원한 내용은 아니다. [M014, Lab03 PDF pp.18–28](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab03.v2.pdf)

### Player의 초기 상태와 constructor

Player는 `private String userId`, `private int health = 50`, 접근 modifier를 생략한 `Random random`을 가진다. Health는 0≤health≤50을 유지해야 하고 0이면 패배 상태다. Constructor의 parameter 목록은 `Player(String userId, int randomSeed)`다. PDF p.22는 ID 대입과 `new Random(randomSeed)` 초기화를 보여 준다. 다만 제공 skeleton의 Player constructor body는 아직 미구현이며, field declaration의 health=50만 이미 들어 있다. PDF의 초기화 예가 skeleton에도 완성되어 있다는 뜻은 아니다.

녹음의 “health attribute should be and”라는 끊긴 표현에서 `int`라는 발화를 복구하지 않는다. `int`는 자료에서 확인한 type이다. PDF p.19의 설명 표기 `userID`·`attach()`도 실제 declaration인 `userId`·`attack(Player opponent)`와 구별한다. 필요한 정보를 읽기 위한 추가 methods는 허용되지만 특정 getter 이름과 개수가 요구된 것은 아니다.

### Action·helper·predicate·tactic의 다른 계약

| Method | 대상과 효과 | 범위 또는 반환 |
| --- | --- | --- |
| `public void attack(Player opponent)` | 상대 health에 random damage를 적용 | 정수 1–5 inclusive, 최종 health는 음수 금지 |
| `private void getDamaged(int damage)` | 자기 health에 지정된 피해를 적용하는 helper | Health의 하한을 지키는 행동 |
| `public void heal()` | 자기 health를 random amount만큼 회복 | 정수 1–3 inclusive, 최종 health≤50 |
| `isAlive()` | 현재 생존 여부를 질의하는 predicate | health>0이면 true, 아니면 false |
| `public char getTactic()` | 다음 행동을 고른다 | Attack 70%는 `'a'`, heal 30%는 `'h'` |

표는 method body의 완성 코드가 아니라 각 호출이 지켜야 할 약속이다. Attack이 자기 health를 줄이거나 heal이 opponent를 회복시키면 변경 대상을 혼동한 것이다. Health=2에서 damage=5이면 최종값은 −3이 아니라 0으로 제한되어야 하고, health=49에서 heal amount=3이면 52가 아니라 50으로 제한되어야 한다. 이는 명세의 경계값을 풀어 쓴 예다.

PDF p.21은 `public Boolean isAlive()`, 실제 skeleton은 `public boolean isAlive()`로 type 표기가 다르다. 녹음의 “70”에는 percent 단위가 없고 마지막 반환 문장도 끊겼으므로 70% 및 `'a'`·`'h'`는 PDF에서 확인한 정보다. [[courses/computer_programming/transcripts/2026-09-17|2026-09-17 STT]] 16:37–17:39의 알려진 한계를 이 수치로 지우지 않는다.

`Random.nextInt()`·`nextFloat()`는 자료의 hints다. 이를 유일한 구현 방식으로 정하거나, 자료에 없는 seed별 출력과 추가 분포 조건을 확정하지 않는다. Tactic을 선택하는 일과 실제 action을 실행하는 일도 구별해야 한다.

## Fight의 reference 연결과 round 순서

Fight의 `int timeLimit = 100`은 최대 rounds이지 초나 분이 아니다. `int currRound = 0`은 시작 전 상태이고 처음 출력하는 round는 1이다. Modifier 없는 `Player p1`·`Player p2`와 `Fight(Player p1, Player p2)`는 두 players를 연결한다. 제공 constructor는 전달받은 references를 fields에 저장한다. 안에서 새 Player를 만드는 것과 다르므로, Fight가 사용하는 player의 health 변화는 Main이 가진 reference로도 관찰된다.

자료의 `public void proceed()`는 한 round를 진행한다. 먼저 `Round <Round_Number>`를 출력하고, p1의 tactic에 해당하는 행동을 수행한다. 이어 **p2가 살아 있을 때만** p2의 tactic과 행동으로 진행한다. p1의 attack으로 p2의 health가 0이 되었다면 p2는 attack뿐 아니라 heal도 하지 않는다. 두 action은 동시가 아니므로 이 순서와 생존 검사가 결과를 바꾼다.

이후 두 health를 다음 형식으로 출력한다. Angle brackets 안은 실제 값이 들어갈 자리다.

```text
<Player1_userID> health : <Player1_health>
<Player2_userID> health : <Player2_health>
```

이 세부 순서는 M014 PDF pp.23–26의 자료 기반 명세다. 녹음의 Player 설명 이후를 들었다고 가정하지 않는다.

### 종료 predicate와 winner reference

`isFinished()`는 어느 player의 health가 0이 되거나 마지막 round가 끝나면 true다. 기본 설정은 rounds 1–100이며, health 조건을 만족하면 더 일찍 종료한다. 시작 전 currRound=0과 첫 round=1을 섞으면 총 회차가 달라지는 off-by-one 오류가 생긴다. 이 method도 PDF p.25에는 `Boolean`, skeleton에는 `boolean`으로 적혀 있다.

`getWinner()`의 return type은 **Player**다. Health가 더 큰 player를 반환하며 같으면 p2가 이긴다. 자료는 p1이 먼저 행동한다는 것을 동점 처리 이유로 든다. 따라서 마지막 round 후 health가 같다고 draw를 만들거나 p1 승리로 바꾸지 않는다. 반환되는 Player reference와 나중에 출력하는 ID String은 서로 다른 값이다. 종료되었다는 사실은 그 object의 GC가 즉시 실행되었다는 뜻도 아니다.

## Main의 입력·구성과 관찰 가능한 출력

Main의 `public static void main(String[] args)`은 전체 simulation을 연결한다. M014 PDF p.27의 두 int 입력은 각각 random seed이며 초기 health나 round 수가 아니다. IDs가 `Gryffindor`·`Slytherin`인 두 Players를 만들고, 그 references를 연결하는 Fight를 만든 뒤 종료 조건에 이를 때까지 진행한다.

마지막으로 winner Player의 ID를 사용하여 `<userID> is the winner!` 형식으로 출력한다. Seed가 random generator의 동작과 관련된다는 사실과 자료가 특정 seed의 정확한 전체 실행 결과를 제공한다는 주장은 다르다. Random 호출 순서도 관련되므로 여기서 임의의 승자나 출력 trace를 만들어 확정하지 않는다.

PDF p.28 제목에는 Constructor라는 말이 들어 있지만 실제 제시된 것은 main이며 추가 Main constructor 요구가 아니다. Skeleton의 Main은 main signature와 미구현 표시만 있고, Fight의 constructor 외 진행·종료·승자 methods도 미구현이다. 반환값이 필요한 methods까지 비어 있으므로 skeleton은 완성 실행 프로그램이 아니다. 학습자가 채워야 할 것은 이 책임과 계약을 만족하는 구현이며, 여기의 설명은 전체 제출용 class bodies를 대신하지 않는다.

## 핵심 정리

- Sentinel은 일반 입력과 다른 경로다. Validation은 조건뿐 아니라 첫 실패 순서도 정한다.
- Board의0은 Player0 표식이며 invalid 검사를 winner보다 먼저 반영한다.
- N×N 일반화는 입력량·line 길이·index 경계를 함께 바꾼다.
- Player는 자기 상태·행동, Fight는 순서·round, Main은 입력·구성을 맡는다.
- Tactic 선택·action 실행·종료 predicate·winner Player 반환을 서로 구별한다.

## 확인·연습문제

### 개념과 실행을 확인하기

#### 확인 Q01 · 한 줄과 sentinel

입력이 abc, Computer Programming, exit 순서로 들어온다. Lab02 echo 단계의 출력과 종료 위치는? 공백이나 exit를 먼저 출력해도 되는가?

<details><summary>해설 보기</summary>

출력은 abc와 공백을 보존한 Computer Programming이다. `exit`는 자료의 입력 label만 있고 다음 output이 없어 echo 없이 종료한다. Scanner로 한 줄을 읽은 뒤 sentinel인지 분기하고 일반 데이터일 때만 그대로 출력한다. 공백은 종료 신호가 아니므로 뒷부분을 버리면 계약과 다르다.

**확인 기준:** 두 출력·공백·sentinel 전용 종료 경로를 확인한다.

</details>

#### 확인 Q02 · 첫 실패의 우선순위

Length10→index4의hyphen→나머지digit 순으로 검사한다. `2018-1234`, `2018_12345`, `e018-12345`, `2018-12345`의 결과와 이 순서가 안전성·보고에 미치는 효과를 설명하라.

<details><summary>해설 보기</summary>

첫째는 `The input length should be 10.`, 둘째는 separator 오류, 셋째는 `Contains an invalid digit.`, 넷째는 `2018-12345 is valid.`다. 첫 실패만 보고하므로 digit 오류를 관찰할 입력은 length·separator를 먼저 통과해야 한다. Length를 먼저 보면 짧은 문자열의 charAt(4) 접근도 막는다. Separator 메시지의 인용부호는 두 원본 페이지가 달라 한쪽을 새 채점 정답으로 지정하지 않는다.

**확인 기준:** 네 분류와 우선순위·safe access를 연결한다.

</details>

#### 확인 Q03 · ASCII digit의 경계

`charAt`의 반환과 ASCII digit 조건·반대 조건을 적어라. `'0'`, `'9'`, `'A'`, 숫자 모양이지만 ASCII0…9 밖인 문자를 비교하고 alphabet 범위도 설명하라.

<details><summary>해설 보기</summary>

`charAt`은 char를 반환한다. `'0'<=ch && ch<='9'`가 허용 조건, `ch<'0'||ch>'9'`가 그 밖이다. 0·9 경계 문자는 통과하고 A나 해당 범위 밖 문자는 실패한다. 문자'0'은 정수0 자체가 아니다. Lowercase는'a'…'z', uppercase는'A'…'Z'의 별도 범위다. 일반 Unicode 숫자 전부를 허용하는 검사로 확대하지 않는다.

**확인 기준:** 양끝 포함·AND/OR·char와int·ASCII 한정을 설명한다.

</details>

#### 확인 Q04 · Board 저장과 다섯 판정

입력 `0 1 0 1 0 0 1 1 1`을3×3으로 저장하라. 이어 별도 boards `010/100/111`, `011/100/110`, `010/100/101`, `000/000/001`, `011/011/001`의 결과와 근거를 적어라. Slash는 row 구분이다.

<details><summary>해설 보기</summary>

입력은 첫 board의 세 rows010,100,111이 된다. 0도 Player0의 표식으로 빈칸이 아니다.

| Board | 근거 | 판정 |
| --- | --- | --- |
| 010/100/111 | 0이4개,1이5개; 마지막 row1승리 | Player 1 win. |
| 011/100/110 | 0이4개,1이5개; 주대각선0승리 | Player 0 win. |
| 010/100/101 | 0이5개,1이4개; 행·열·두 대각선에 승리 없음 | Tie. |
| 000/000/001 | 개수8대1 | Invalid game. |
| 011/011/001 | 개수4대5지만 첫 열0·마지막 열1 동시 승리 | Invalid game. |

한 줄을 찾자마자 winner를 출력하면 개수 차이>1 또는 양쪽 승리를 놓친다. `printBoard`는 저장 순서를 확인하며 추가 선공·게임 이력 규칙은 이 명세에 없다.

**확인 기준:** 입력 배치와 다섯 결과·독립 invalid 두 조건을 검산한다.

</details>

#### 확인 Q05 · N에 따라 바뀌는 경계

N×N 확장에서 입력량·최소 N·승리 줄 길이·유지 규칙을 말하라. 다음 완성 boards를 각각 판정하라. Slash는 row 구분이다.

- 4×4: `0100/1001/1111/1000`
- 5×5: `00000/11111/00011/11100/10100`
- 4×4: `0101/1010/0101/1011`

<details><summary>해설 보기</summary>

N을 먼저 읽고 N²개 표식을 읽으며 N ≥ 3이다. 행·열 수와 indices, winning line의 길이는 N을 따른다. 0/1 의미, 양쪽 승리와 개수 차이 > 1의 invalid 규칙은 유지된다.

첫 board는 0과 1이 각각 8개이고 셋째 row만 1의 winning line을 만들어 `Player 1 win.`이다. 둘째는 개수가 13/12로 허용 범위지만 첫 row의 0과 둘째 row의 1이 모두 이겨 `Invalid game.`이다. 셋째는 개수가 7/9여서 차이 2만으로 `Invalid game.`이다. N = 5이면 전체 다섯 칸이 같아야 하며 세 칸만으로는 승리하지 않는다. 원래 발화가 셋을 모두 4×4라고 해도 PDF의 크기 4·5·4를 구별한다.

**확인 기준:** 바뀌는 bounds와 유지 규칙, 서로 다른 invalid 원인을 설명한다.

</details>

#### 확인 Q06 · Player 초기화와 책임

Player·Fight·Main의 책임, Player fields와 constructor parameters·health 범위를 설명하라. PDF의 초기화 예와 skeleton의 완료 상태, userID/attach 표기는 어떻게 읽어야 하는가?

<details><summary>해설 보기</summary>

Player는 ID·health·행동, Fight는 interaction·round, Main은 입력·전체 구성을 맡는다. Fields는 private String userId, private int health=50, modifier 없는 Random random이다. Constructor는 Player(String userId,int randomSeed), health범위0…50이며0이면 패배다. PDF는 ID와 seeded Random 초기화를 보이지만 skeleton constructor는 미구현이고 field health50만 이미 있다. Descriptive userID·attach와 실제 userId·attack 선언을 구별하고 특정 getter 이름·개수를 새로 요구하지 않는다. 이 정확한 정보는9월19일 자료 보충이다.

**확인 기준:** 세 책임·fields·seed·skeleton 미구현과 자료 범위를 설명한다.

</details>

#### 확인 Q07 · 다섯 method의 다른 계약

`attack`·getDamaged·heal·isAlive·getTactic의 접근·대상·범위·반환을 정리하라. Health2/damage5,health49/heal3의 결과, Boolean/boolean과 녹음의70·character 한계도 설명하라.

<details><summary>해설 보기</summary>

`public void` attack(Player opponent)는 상대에게1…5 damage를 적용하고 private void getDamaged(int damage)는 자기 health를 지정 피해만큼 낮추되0 아래로 두지 않는다. `public void` heal은 자기 health를1…3 회복하되50을 넘지 않는다. 두 경계 결과는0과50이다. `isAlive`는 health>0의 predicate이며 PDF는 Boolean, skeleton은 boolean이다. `public char` getTactic은70% attack에'a',30% heal에'h'를 반환하는 선택이며 그 자체가 action 수행은 아니다. `nextInt()`/`nextFloat()`는 hints다. 녹음의70에는 단위가 없고 character 설명은17:39에 끊겨 정확한 수치·문자는 PDF 근거다.

**확인 기준:** 다섯 책임·target·두 clamp 결과·type/source 차이를 모두 적는다.

</details>

#### 확인 Q08 · Reference 연결과 한 round

Fight constructor가 this.p1=p1,this.p2=p2를 저장한다. 새 Player가 생기는가? `timeLimit = 100`,currRound0의 의미와 proceed의 출력·행동 순서, p1 공격으로 p2가0이 되는 경우를 설명하라.

<details><summary>해설 보기</summary>

들어온 reference 값을 저장해 Main과 같은 Players를 쓰므로 health 변화가 Main에서도 보인다. 100은 최대 rounds이지 시간 단위가 아니며0은 시작 전, 첫 출력은 Round1이다. `proceed`는 `Round <Round_Number>`를 출력하고 p1 tactic/action을 먼저 수행한다. `p2`가 살아 있을 때만 p2 tactic/action을 수행하므로 p1이 p2를0으로 만들면 p2의 attack·heal 모두 생략한다. 뒤에 두 `<userID> health : <health>` 줄을 p1,p2 순서로 출력한다. 동시 행동이 아니며 이 세부는 materials-only 계약이다.

**확인 기준:** 복사된 references·round 단위·순서·사망 후 action 금지를 확인한다.

</details>

#### 확인 Q09 · 종료와 winner의 다른 반환

Health0 또는 마지막 round가 끝난 경우 isFinished는? 기본 round 범위와 getWinner의 return type·동점 규칙·Main 출력 ID의 차이를 설명하라.

<details><summary>해설 보기</summary>

둘 중 하나가 만족하면 true다. 시작 전0에서 rounds1…100을 진행하되 health 조건이면 더 일찍 끝난다. PDF의 Boolean과 skeleton boolean 차이는 유지한다. `getWinner`는 더 높은 health의 Player reference를 반환하며 같으면 p2다. 자료는 p1의 선행 행동을 동점 이유로 든다. 이 값은 ID String도 draw도 아니며 Main이 Player의 ID를 따로 출력한다. Simulation 종료는 즉시 GC 증거가 아니다.

**확인 기준:** Predicate와 Player 반환·동점p2·off-by-one·GC 구별을 설명한다.

</details>

#### 확인 Q10 · Main의 입력과 미구현 범위

Main의 두 int는 어디에 쓰이고 어떤 objects를 연결하는가? 최종 메시지·p28의 Constructor heading·skeleton 상태와 특정 seed 승자를 확정할 수 없는 이유를 설명하라.

<details><summary>해설 보기</summary>

두 int는 Players의 random seeds이며 초기 health나 round 수가 아니다. Gryffindor·Slytherin IDs의 Players를 만들고 두 references로 Fight를 구성해 종료될 때까지 진행한다. Winner Player의 ID로 `<userID> is the winner!`를 출력한다. P28 heading과 달리 코드는 main이지 추가 Main constructor 요구가 아니다. Main과 Player constructor, Fight의 진행·종료·winner 등은 skeleton에서 미구현이므로 return 필요한 빈 bodies도 완성 실행 프로그램이 아니다. Random 호출 순서와 구현이 결과에 관련되고 자료에 특정 seed trace가 없어 승자를 꾸며낼 수 없다.

**확인 기준:** Seed→Players→Fight→winner ID 흐름과 미구현 상태를 구별한다.

</details>

### 적용 연습

#### 연습 P01 · 실패 단계만 드러내는 사례

**새로 작성한 강의 기반 일반 연습; 직접 대응 기출 유형 근거 없음.** Validator를 검사하려 한다. `A`, `1234_56789`, `1234-56A89`, `1234-56789`, `exit`에 대해 최초 검사 결과를 적어라. 왜 `A`만으로 digit 검사가 맞는지 알 수 없는가?

<details><summary>해설 보기</summary>

A는 length 실패로 끝나 index4나 digit 검사에 도달하지 않는다. 두 번째는 length10이나 separator 실패다. 세 번째는 length·hyphen 통과 후 A 때문에 digit 실패다. 네 번째는 통과, exit는 일반 검증/echo 전에 종료 경로다. Digit 검사를 확인하려면 세 번째처럼 앞 조건을 만족한 반례가 필요하다. Exact separator quotes는 원문 차이를 유지하고 이 연습이 새 채점 문자열을 정하지 않는다.

**확인 기준:** 다섯 경로·첫 실패·단계별 test 설계 이유를 설명한다.

</details>

#### 연습 P02 · 지정된 사건으로 한 round 추적

**새로 작성한 강의 기반 일반 연습; 직접 대응 기출 유형 근거 없음.** Seed에서 추정한 결과가 아니라 이번 연습에서 p1의 선택을 attack,damage5로 지정한다. Round 시작 전 currRound0,p1 health4,p2 health3이며 IDs는 Gryffindor/Slytherin이다. 한 round의 health·출력·종료·winner를 구하라. `p2`가 heal을 미리 준비했다고 가정해도 실행할 수 있는가?

<details><summary>해설 보기</summary>

Round1에서 p1이 p2에게5를 적용하면 p2는 하한0, p1은4다. `p2`는 이미0이라 tactic/action 단계로 가지 않고 heal도 못 한다. Health 조건으로 종료하며 winner는 p1 Player이고 Main은 그 ID를 출력한다.

```text
Round 1
Gryffindor health : 4
Slytherin health : 0
Gryffindor is the winner!
```

마지막 줄은 proceed 자체가 아니라 종료 뒤 Main의 출력이다. 미리 준비한 heal도 사망 후 행동 금지 계약을 바꾸지 않는다. 이 결과는 지정한 사건의 trace이며 실제 seed 결과나 전체 구현은 아니다.

**확인 기준:** 하한0·p2 생략·출력 주체·Player/ID 구별과 지정 사건 범위를 설명한다.

</details>

### 복습 순서

Q01–Q03에서 입력·오류별 사례를 직접 만든 뒤 Q04–Q05의 board를 행·열·대각선·개수로 검산한다. Q06–Q10은 책임과 return type을 말하고 P01–P02로 검사 순서와 round 순서를 확인한다.

## 출처

### 날짜별 강의와 녹음

- [[courses/computer_programming/lectures/2026-09-10-lecture-04|2026-09-10 · Computer Programming 강의·원자료]]
- [[courses/computer_programming/lectures/2026-09-17-lecture-06|2026-09-17 · Computer Programming 강의·원자료]]
- [[courses/computer_programming/transcripts/2026-09-10|2026-09-10 보정 녹음문]] — 09:38, 15:25, 38:21, 50:11.
- [[courses/computer_programming/transcripts/2026-09-17|2026-09-17 보정 녹음문]] — 15:41, 16:37.

### 강의자료와 해당 페이지

- [Lab02 v4.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab02.v4.pdf) — [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-016), [p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-017), [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-018), [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-019), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-020), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-023), [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-024), [p.25](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-025), [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-026), [p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-027).
- [Lab03 v2.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab03.v2.pdf) — [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-018), [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-019), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-020), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-021), [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-022), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-023), [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-024), [p.25](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-025), [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-026), [p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-027), [p.28](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab03.v2/page-028).

Lab02의 구분자 메시지는 PDF p18과 p20의 인용부호가 다르며 새로운 채점 문자열로 확정하지 않는다. Board 규칙은 주어진 완성 board 판정만이며 모든 게임 이력의 적법성을 증명하지 않는다. 9월17일 녹음은17:39에 끊긴다. Lab03의 정확한 선언·수치와 Fight/Main 상세는9월19일 확보 자료 보충이다. PDF의 Boolean과 skeleton의 boolean, userID/userId·attach/attack 표기 차이는 유지한다. 제공 skeleton에는 미구현 methods가 남아 있어 전체 실행 결과나 seed별 승자를 주장하지 않는다.


---

[[courses/computer_programming/units/encapsulation|← 이전: Encapsulation과 접근·상태 설계]] · [[courses/computer_programming/units/index|단원 목차]]
