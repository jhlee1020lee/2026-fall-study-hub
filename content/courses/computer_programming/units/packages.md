---
title: "Packages·이름 공간·Java API 활용"
description: "이름 공간, 버전별 분기, import와 API 문서 읽기를 연결한다."
course: "computer_programming"
unit_id: "packages"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["5 encapsulation.pdf", "Lab04 v2.pdf", "Lab04 v4.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_programming/lectures/2026-09-15-lecture-05"]
---

완전한 type 이름으로 어느 class를 사용하는지 먼저 확인한다. 그다음 import·접근 권한·API 계약을 따로 점검하면 이름이 같아도 혼동을 줄일 수 있다.

## Package: 같은 이름을 서로 다른 공간에 두기

여러 사람이 만든 class(클래스)를 한 프로그램으로 합치면 같은 이름을 서로 다른 뜻으로 사용하는 문제가 생긴다. Package(패키지)는 관련 class와 interface를 묶어 namespace(이름 공간)와 접근 경계를 제공한다. [M012 PDF p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-026)의 그림에서는 File I/O와 UI 쪽에 각각 `Tools.class`가 있다. 단순히 합친 오른쪽 영역에서 두 `Tools.class`가 충돌한다. 이어지는 p.27은 `FileIO`, `Graphic`, `UI`를 분리하고 `Project/FileIO/Tools.class`와 `Project/UI/Tools.class`라는 다른 경로로 같은 끝 이름을 식별한다. 읽어야 할 핵심은 파일 이름을 모두 외우는 것이 아니라 **이름에 소속을 더하면 구별할 수 있다**는 점이다.

이 부분은 Lab04 자료와 M012의 package 부분을 연결한 자료 기반 학습이다. [[courses/computer_programming/lectures/2026-09-15-lecture-05|2026-09-15 강의 노트 · 접근 제어와 다음 범위]]의 녹음은 M012 p.23까지의 Encapsulation을 다루고, [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 STT 01:30:43]]에서 Packages를 다음으로 미뤘다. 여기의 상세 내용에 새 강의 날짜를 부여하지 않는다.

### 두 `Keyboard`는 같은 type이 아니다

Lab04의 예에서 `computer`에는 `Keyboard`, `Monitor`, `Mouse`가, `instrument`에는 `Drum`, `Guitar`, `Keyboard`가 있다. `Mart`는 package 선언 없이 `main()`을 가진다. 이때 두 keyboard의 완전한 이름은 `computer.Keyboard`와 `instrument.Keyboard`다. 이름의 끝부분만 같고 서로 다른 type(자료형)이므로 어느 하나의 이름을 억지로 바꾸지 않아도 된다. [Computer Programming NM003 PDF pp.11–14; NM002 PDF pp.9–12]

`package computer;`는 소속을 정하는 선언이며 이 프로젝트의 `computer` 소스 디렉터리에 대응한다. 화면의 “Default”는 `package default;`를 쓰라는 뜻이 아니라 선언을 생략한 unnamed package를 가리킨다. 또한 subpackage(하위 패키지)가 디렉터리상 아래에 있다고 해서 같은 package가 되는 것은 아니다. 이름의 접두어를 공유하는 두 package가 package-private 접근 권한까지 공유하지는 않는다. 이는 [Encapsulation](encapsulation.md)의 “같은 package”를 정확하게 적용하기 위한 구별이다.

## 완전한 이름과 객체별 분기 추적

두 `Keyboard` class는 각각 private `id`, `name`을 constructor(생성자)로 저장하고 `printCompanyInfo()`를 제공한다. 같은 method 이름을 갖는다고 상속 관계가 선언된 것은 아니다. 각 class가 자기 code에 따라 `id % 10`을 계산하고 자기 branch를 선택한다.

| `id % 10` | Lab04의 `computer.Keyboard` | `instrument.Keyboard` |
|---|---|---|
| `1` | `Corsair` | `Samick` |
| `2` | `Razor` | `Yamaha` |
| 그 밖 | `Realforce` | `Gipson` |

`Gipson`과 `Razor`는 자료에 인쇄된 철자다. 이 표는 브랜드에 대한 외부 사실이 아니라 코드의 문자열 분기다. `Mart`의 두 생성문은 다음과 같다. [NM003 PDF pp.12–14]

```java
computer.Keyboard keyboardComputer =
    new computer.Keyboard(15523, "H Gaming keyboard");
instrument.Keyboard keyboardMusic =
    new instrument.Keyboard(131511, "Black and white keyboard");
```

첫 객체는 `15523 % 10 = 3`이므로 `else`를 선택한다. 따라서 Lab04 코드의 출력 문자열은 `H Gaming keyboard: Realforce's device`다. 둘째는 `131511 % 10 = 1`이므로 `Black and white keyboard: Samick's device`다. 생성문에서 어느 class를 골랐는지와 그 class 내부의 branch를 차례대로 확인해야 한다.

그런데 [NM003 PDF p.15의 출력 상자](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-015)는 첫 결과를 `Razor`로 인쇄한다. NM002 v2 p.13에도 같은 불일치가 있다. 이는 **코드와 출력 예시의 자료 내부 충돌**이다. 나머지 `3`을 `2`로 바꾸거나 screenshot을 실제 실행 검증으로 취급하지 않는다. 위의 `Realforce`는 코드에서 직접 도출한 설명이다.

더 오래된 M012 pp.29–34에서는 컴퓨터 쪽 분기가 `Samsung`/`LG`/`Apple`이다. 같은 ID `15523`에서 그 버전의 결과는 `Apple`이고 p.34의 출력과도 일치한다. Lab04의 결과와 섞으면 안 된다. 서로 다른 source version을 구별한 뒤에야 수치 trace가 의미를 갖는다.

## `import`: 이름을 줄여 쓰되 접근 권한은 유지하기

매번 완전한 이름을 쓰는 대신 `import`로 단순 이름을 사용할 수 있다. 다음 세 방식은 같은 접근 가능한 class를 지칭하는 서로 다른 표기다. [M012 PDF pp.35–37]

| 방법 | 선언 또는 사용 | 효과 |
|---|---|---|
| 완전한 이름 | `computer.Keyboard` | 어느 package의 class인지 직접 표시한다. |
| 단일 type import | `import computer.Keyboard;` | 그 class를 `Keyboard`로 부를 수 있게 한다. |
| wildcard import | `import computer.*;` | 그 package의 접근 가능한 type을 단순 이름으로 찾도록 한다. |

`import`는 객체를 생성하지 않는다. 생성은 `new`가 담당한다. 또한 private 접근을 풀어 주지도 않는다. 두 package의 `Keyboard`를 동시에 모호한 단순 이름으로 사용하지 말고 필요한 곳에서 완전한 이름을 쓰면 된다. Wildcard `*`는 하위 package까지 재귀적으로 가져오는 기호가 아니다.

Top-level `public class`는 다른 package에서도 사용할 수 있고, 자료의 소스 파일 구성에서는 class와 같은 이름의 `.java` 파일에 둔다. Modifier가 없는 top-level class는 같은 package 안에서 사용하는 helper가 될 수 있다. Member의 `private`/`protected`를 이 top-level 선언에 그대로 적용하지 않는다. M012 p.36의 `new computer.Keyboard()`는 이름 표기를 설명하는 축약 예다. 앞서 나온 constructor는 `int`, `String` 두 인자를 요구하므로 그 축약을 실제 제공된 no-argument constructor로 받아들이면 안 된다.

### Built-in package를 찾는 기준

`java.lang`의 `String`, `System`, `Math`는 이 자료의 예에서 별도의 import 없이 사용한다. `java.util`에는 `Arrays`, `Calendar`, `Date`, `Random`, `StringTokenizer` 같은 type이 있으며 `java.io`는 I/O용 class와 interface를 제공한다. Lab04는 단일 type을 가져오는 `import java.util.Scanner;`와 package의 type을 찾는 `import java.time.*;`를 비교한다. [M012 PDF p.46; NM003 PDF p.18]

```java
import java.util.Scanner;
import java.time.*;
```

이 선언만으로 입력을 읽거나 시간을 계산한 것은 아니다. 필요한 이름을 해석할 수 있게 된 다음, 해당 constructor나 method의 parameter와 반환값을 이해해서 호출해야 한다. 그 계약을 찾는 도구가 API 문서다.

## API 문서에서 필요한 member의 계약 읽기

API(Application Programming Interface)는 다른 코드가 제공하는 기능을 사용하는 약속이다. 모든 기능을 직접 만드는 대신 `Scanner`로 입력을 다루고 `Math.random()` 같은 기능을 사용할 수 있다. 그러나 이름을 안다는 것과 올바르게 호출할 수 있다는 것은 다르다. 같은 이름의 method도 parameter 목록이 다르면 사용법이 달라질 수 있다.

Lab04 v4의 Java 11 문서 화면은 다음 탐색 순서를 보여 준다. 이는 **공급된 화면을 읽는 방법**이며 현재 문서 UI나 소프트웨어 상태에 대한 주장은 아니다. [NM003 PDF pp.19–24]

| 단계 | 화면에서 찾을 것 | 다음에 답할 질문 |
|---|---|---|
| Module 목록, p.21 | `java.base` 같은 module 이름 | 찾는 기능이 어느 큰 묶음에 있는가? |
| Package 목록, p.22 | `java.base` 안의 package들 | 필요한 type은 어느 package에 있는가? |
| Class 목록, p.23 | `java.math`의 class 목록 | 사용하려는 class는 무엇인가? |
| Member summary, p.24 | `Modifier and Type`, `Method`, `Description` | 반환 type, 인자 형태, 설명이 원하는 기능과 맞는가? |

[p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-024)의 표에서는 method 이름 하나만 읽지 말고 왼쪽 type과 오른쪽 설명을 같은 행에서 연결해야 한다. 같은 이름이 반복되면 parameter가 어떻게 다른지도 살핀다. 화면에 `BigDecimal` 등 여러 항목이 보인다는 사실이 그 API 전체를 학습했다는 뜻은 아니다.

이 탐색 흐름은 v2 pp.17–22에도 이미 있다. V4는 앞쪽에 Encapsulation 정의와 Package 정의 설명을 보탰지만 API 탐색을 처음 도입한 버전은 아니다. Inner class와 `Calculator`가 나오는 M012 pp.38–45는 여기서 필요한 package 학습의 범위에 포함하지 않는다. 이름을 정확히 찾고 접근 가능한 동작의 계약을 읽는 능력은 [Lab applications](lab-applications.md)의 `Platform.Platform`과 `Platform.Games`를 구별하는 데 그대로 쓰인다.

## 핵심 정리

- Package는 이름 공간과 접근 경계다. `computer.Keyboard`와 `instrument.Keyboard`는 서로 다른 type이다.
- `import`는 이름을 줄이며 객체 생성이나 권한 부여를 하지 않는다. Subpackage도 별도의 package다.
- Lab04의 ID 15523은 코드상 `Realforce`인데 출력 상자는 `Razor`다. 이전 M012의 `Apple` 분기와도 섞지 않는다.
- API 문서는 module→package→class→member 순서로 찾아 입력·반환·설명을 함께 읽는다.

## 확인·연습문제

### 이름과 계약

#### 확인 Q01 · 완전한 이름과 package 경계

`Tools` 충돌 그림과 두 `Keyboard` 예에서 package는 무엇을 해결하는가? `Mart`의 Default 표시와 subpackage의 접근 권한도 설명하라.

<details><summary>해설 보기</summary>

File I/O와 UI의 `Tools.class`를 단순 합치면 이름이 충돌하지만 `FileIO`와 `UI` 소속을 더하면 구별된다. Lab04도 `computer.Keyboard`와 `instrument.Keyboard`가 다른 type이라 같은 끝 이름을 유지할 수 있다. Package는 관련 class/interface의 묶음이자 접근 경계다. `Mart`의 Default는 package 선언 생략이지 `package default;`가 아니다. `package computer;`는 예제의 computer 소스 디렉터리와 대응한다. Subpackage는 별개라 상위 이름을 공유해도 package-private 권한을 공유하지 않는다.

**확인 기준:** 두 완전한 이름, unnamed package, 별도 접근 경계를 확인한다.

</details>

#### 확인 Q02 · 버전별 branch

두 Keyboard가 private `id`·`name`을 constructor로 저장한 뒤 `id%10`으로 회사를 고른다. Lab04의 각 분기를 나열하고 컴퓨터 ID 15523, 악기 ID 131511의 결과를 추적하라. 출력 상자 및 M012와의 차이는?

<details><summary>해설 보기</summary>

컴퓨터 쪽은 나머지 1→`Corsair`, 2→`Razor`, 그 밖→`Realforce`; 악기 쪽은 1→`Samick`, 2→`Yamaha`, 그 밖→원문 철자 `Gipson`이다. 15523의 나머지 3은 Realforce, 131511의 나머지 1은 Samick이다. V2 p.13/v4 p.15의 Razor 출력은 코드와 충돌한다. M012의 컴퓨터 분기는 Samsung/LG/Apple이므로 같은 15523에서 Apple이다. 같은 method 이름이 상속 관계를 만들지 않으며 각 생성 type의 코드 버전을 따라야 한다.

**확인 기준:** 나머지 계산, 여섯 branch, 버전 충돌을 구별한다.

</details>

#### 확인 Q03 · import와 접근

완전한 이름·단일 import·wildcard를 비교하라. 두 `Keyboard`의 모호함, top-level class 접근, 기본 제공 package, 축약 constructor 호출에서 주의할 점은?

<details><summary>해설 보기</summary>

`computer.Keyboard`, `import computer.Keyboard;` 뒤 `Keyboard`, `import computer.*;` 뒤 접근 가능한 `Keyboard`는 이름 사용 방식의 차이다. 둘을 모호한 단순명으로 쓰지 말고 필요한 type을 완전히 적는다. Wildcard는 하위 package를 재귀적으로 가져오지 않으며 private도 열지 않는다. Top-level은 public 또는 modifier 생략을 구별하고 private/protected를 붙이지 않는다. 자료의 public class는 동명 .java 파일을 쓴다. `java.lang`의 String/System/Math는 별도 import 없이 사용하고 java.util은 Scanner/Arrays/Random, java.io는 I/O, java.time.*는 해당 package의 type 검색을 돕는다. Import가 객체를 만들지는 않는다. M012의 인자 없는 축약은 실제 두 인자 Keyboard constructor를 대체하지 않는다.

**확인 기준:** 이름 해석·접근·객체 생성의 세 판단을 분리한다.

</details>

#### 확인 Q04 · API 계약 찾기

Lab04의 Java 11 문서 화면을 따라 특정 method를 찾는 네 단계를 적고 마지막 표에서 확인할 정보를 설명하라. 같은 이름만 일치하면 호출을 결정해도 되는가?

<details><summary>해설 보기</summary>

Module 목록→package 목록→class 목록→member summary다. 화면은 java.base에서 package를 찾고 java.math의 class 목록으로 간다. 마지막에는 Modifier and Type, Method, Description을 연결해 반환 type·parameter 목록·기능 설명을 읽는다. 같은 이름도 parameter가 다를 수 있으므로 이름만으로 선택하지 않는다. API는 기존 기능을 사용하는 계약이고 import는 그 이름을 줄이는 수단이다. 이 탐색은 v2에도 있으며 v4 최초 도입이나 화면 속 수치 API 전체 학습을 뜻하지 않는다.

**확인 기준:** 네 단계와 입력·반환·설명 확인을 포함한다.

</details>

### 적용 연습

#### 연습 P01 · 이름을 찾은 뒤에도 남는 일

새로 만든 자료 기반 일반 연습이다. 전체 후보에 namespace와 API 탐색을 직접 함께 평가하는 문항은 없으며 중간 4번의 상속 접근 표는 이 단원의 직접 형식 근거로 쓰지 않는다. 서로 다른 package의 동명 type 두 개를 쓰는 동료가 wildcard 두 개만 적고 객체 생성과 private 접근도 해결되었다고 말한다. 무엇을 순서대로 다시 점검하게 할 것인가?

<details><summary>해설 보기</summary>

먼저 두 type의 완전한 이름으로 의도를 분리한다. 다음 class와 사용할 member가 현재 위치에서 접근 가능한지 확인한다. 필요한 constructor의 parameter·기능은 문서의 member 정보로 확인하고 별도의 `new` 호출이 필요함을 설명한다. Wildcard가 단순 이름의 모호함을 해소하거나 접근 권한을 넓히거나 객체를 생성하지 않는다. Subpackage 이름도 정확히 별도로 확인한다.

**확인 기준:** 완전한 이름→접근→계약→생성 순서를 이유와 함께 제시한다.

</details>

#### 연습 P02 · 출력 상자 검토

새로 만든 자료 기반 일반 연습이다. 이 버전 충돌 검토와 직접 대응하는 기출 근거는 없다. 검토자가 Lab04 출력의 `Razor`를 맞추려고 코드의 else를 Razor로 고치고 M012도 같은 수정이 필요하다고 주장한다. 강의 코드를 수정하지 않고 이 제안을 평가하라.

<details><summary>해설 보기</summary>

출력에 코드를 억지로 맞추면 원문 충돌을 숨긴다. Lab04는 15523%10=3에서 Realforce가 도출되고 Razor 상자를 별도 오류로 남겨야 한다. M012는 별도 Samsung/LG/Apple 분기라 Apple이 코드와 출력에 모두 맞는다. 따라서 공통 수정 근거가 없으며 source version을 구별해 결과를 설명한다.

**확인 기준:** 동일 입력과 서로 다른 분기표를 구별하며 실행 확인을 주장하지 않는다.

</details>

### 짧은 복습 계획

Q02를 각 버전별로 다시 계산한 뒤 Q03을 보지 않고 설명한다. 다음 날 P01의 점검 순서를 사용해 API 화면에서 입력·출력 계약을 찾아본다.

## 출처

이 상세 내용은 자료 기반 복습이다. 9월 15일 녹음은 Encapsulation p.23까지이며 01:30:43에서 packages를 미뤘다. 아래 날짜 링크는 그 경계를 보여 준다. Lab04의 Razor 출력 충돌과 M012의 Apple 버전은 구별하고, API 화면은 공급된 Java 11 문서 예로 읽는다. M012의 inner class/Calculator pp.38–45는 범위 밖이다.

### 날짜별 노트와 녹취

- [[courses/computer_programming/lectures/2026-09-15-lecture-05|2026-09-15 · 강의 노트]]

- [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 · 보정 녹취 · 01:30:43]]

### 자료와 해당 페이지

- [5 encapsulation · PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/5.encapsulation.pdf) — [p.25](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-025), [p.26](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-026), [p.27](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-027), [p.28](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-028), [p.29](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-029), [p.30](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-030), [p.31](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-031), [p.32](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-032), [p.33](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-033), [p.34](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-034), [p.35](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-035), [p.36](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-036), [p.37](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-037), [p.46](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/5.encapsulation/page-046)

- [Lab04 v2 · PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab04.v2.pdf) — [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-008), [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-009), [p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-010), [p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-011), [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-012), [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-013), [p.16](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-016), [p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-017), [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-018), [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-019), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-020), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-021), [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v2/page-022)

- [Lab04 v4 · PDF](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab04.v4.pdf) — [p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-010), [p.11](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-011), [p.12](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-012), [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-013), [p.14](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-014), [p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-015), [p.17](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-017), [p.18](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-018), [p.19](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-019), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-020), [p.21](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-021), [p.22](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-022), [p.23](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-023), [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab04.v4/page-024)

이 단원과 직접 대응하는 기출 형식 근거가 없어 P 문제는 강의·자료 기반 일반 연습으로 제시한다.
