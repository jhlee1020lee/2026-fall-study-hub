---
title: "Programming의 목적과 Java 실행·개발 환경"
description: "Programming 검증과 Java source부터 IDE 실행까지의 흐름을 복습한다."
course: "computer_programming"
unit_id: "java-runtime"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["Lecture 1 Introduction.pdf", "Lecture 2 Java Basics 1.pdf", "Lab01.pdf", "Lab02 v4.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_programming/lectures/2026-09-01-lecture-01", "courses/computer_programming/lectures/2026-09-03-lecture-02", "courses/computer_programming/lectures/2026-09-08-lecture-03", "courses/computer_programming/lectures/2026-09-10-lecture-04", "courses/computer_programming/lectures/2026-09-15-lecture-05"]
---

Programming의 목표를 검증 가능한 조건으로 바꾸고 Java의 compile·실행 단계를 구별한다. 실행 실패를 도구 경로, 파일명, 실행 대상별로 진단해 보자.

## Programming과 검증 가능한 동작

Programming(프로그래밍)은 원하는 결과를 실행 가능한 작업으로 바꾸고, 그 결과가 목적에 맞는지 확인하는 과정이다. 먼저 입력과 출력, 지켜야 할 조건을 정의한다. 다음에는 작업을 나누어 코드로 표현하고, 실행 결과를 요구사항과 비교한다. 코드가 종료되었다거나 한 입력에서 답을 맞혔다는 사실만으로 reliable computational behavior(신뢰할 수 있는 계산 동작)가 확보되지는 않는다. 경계 입력에서도 맞는지, 정해진 시간 안에 끝나는지, memory와 CPU를 적절히 사용하는지까지 확인해야 한다.

이 구분은 [[courses/computer_programming/transcripts/2026-09-01|2026-09-01 STT]] 12:22–13:03의 설명과 연결된다. 강의자는 구현을 다른 사람이나 AI가 도와주어도 목표 충족 여부를 검증하는 일이 남는다고 강조했다. 직접 설명하지 못하는 코드는 수정하기도 어렵다. 작은 기능이나 전체 구조를 구체적으로 질문하는 것과, 돌아온 코드를 읽어 타당성을 판단하는 것은 함께 필요하다.

Maintenance(유지보수성)는 이후의 수정이 얼마나 쉬운가, efficiency(효율성)는 시간과 자원을 어떻게 쓰는가, readability(가독성)는 읽는 사람이 의도를 얼마나 쉽게 파악하는가에 관한 기준이다. 의미 있는 이름과 적절한 작업 분리는 세 기준을 함께 돕는다. [[courses/computer_programming/transcripts/2026-09-08|2026-09-08 STT]] 53:25에서 강조한 memory·CPU·compiler의 이해도 같은 목적을 가진다. 코드의 표면을 읽는 데서 그치지 않고, 각 문장이 실행되면 무엇이 바뀌는지 설명하는 것이다.

## Java source에서 JVM 실행까지

사람이 작성한 Java source(소스 코드)와 컴퓨터가 실행하는 표현은 다르다. `.java` 파일을 compiler(컴파일러)인 `javac`에 주면 Java bytecode(바이트코드)가 들어 있는 `.class` 파일을 만든다. JVM(Java Virtual Machine)은 이 bytecode를 실행한다. 따라서 다음 두 단계는 서로 다른 일을 한다.

```text
javac HelloWorld.java
java HelloWorld
```

첫 줄은 source를 compile하고, 둘째 줄은 `HelloWorld`라는 class의 실행을 요청한다. 여기서 `.class`는 운영체제가 곧바로 실행하는 native executable이 아니다. 플랫폼별 JVM이 실행 환경의 차이를 담당하므로 같은 bytecode를 여러 플랫폼에서 실행하는 모델을 얻는다. Lab01의 “executable file”이라는 입문 표현도 이 범위에서 읽어야 한다. [Java Basics 1, PDF pp.7–9](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf)

JVM·JRE·JDK를 구별하면 설치 도구의 역할도 분명해진다.

| 구성 요소 | 수업에서 설명한 역할 |
| --- | --- |
| JVM | Bytecode 실행 |
| JRE(Java Runtime Environment) | JVM과 Java package classes를 포함하는 실행 환경 |
| JDK(Java Development Kit) | 실행 환경과 개발 도구를 포함하는 개발 환경 |

[[courses/computer_programming/transcripts/2026-09-03|2026-09-03 STT]] 02:20은 이 포함 관계를 설명한다. 개발하려면 실행 기능뿐 아니라 compile 도구도 필요하다는 뜻이다. 이는 수업의 개념 모델이며 현재 모든 배포 제품의 패키징이 같다는 주장은 아니다. 소개 자료의 mobile·web application, server, game, database connection은 Java의 활용 예로 읽으면 된다.

## `HelloWorld`의 구조와 실행 진입점

다음은 Java Basics 1의 시작 예제다.

```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, world!");
    }
}
```

`class`는 코드를 담는 class 정의를 시작하고, `HelloWorld`는 그 이름이다. 이 예제의 public class는 `HelloWorld.java`에 저장해야 한다. `Hello.java`에 저장하면 파일명 불일치로 compile error가 발생한다. Class 이름을 PascalCase로 짓는 것은 naming convention(이름 관례)이지만, 이 public class와 파일명의 일치는 도구가 검사하는 규칙이다.

`main`은 이 독립 실행 예제의 entry point(진입점)다. `public`은 접근 허용, `static`은 class 소속, `void`는 반환값 없음, `String[] args`는 문자열 배열 parameter를 나타낸다. 중괄호는 class와 method의 범위를 구분하고, 출력문 끝의 semicolon은 문장을 끝낸다. 모든 class가 각각 `main`을 가져야 한다는 뜻은 아니다. `static`과 object의 상세 관계는 [[courses/computer_programming/units/objects-references|Objects와 reference]]에서 이어진다.

`System.out.println`은 `System`의 `out`을 통해 `println`을 호출하여 글을 출력하고 줄을 바꾼다. 화면에 출력하는 동작과 caller에게 값을 돌려주는 동작은 별개다. 그러므로 `main`이 `void`여도 화면 출력은 가능하다. [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 STT]] 40:13의 재설명도 `void`, method 이름, 문자열 배열 입력을 나누어 읽는다.

Comment(주석)는 실행할 문장과 설명을 분리한다. `//`부터 줄 끝까지는 한 줄 주석이고, `/*`와 `*/` 사이는 여러 줄 주석이다. 이름만으로 드러나지 않는 의도나 제약을 설명하는 데 유용하다. 주석에 쓴 출력 예보다 실제 문자열 literal이 실행 결과를 결정한다. 위 코드는 대소문자와 쉼표까지 포함한 `Hello, world!`를 출력한다.

## JDK와 IDE를 연결하는 실행 환경

실행 원리를 알면 환경 문제를 단계별로 구별할 수 있다. [Lab01](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab01.pdf)은 OS와 CPU architecture에 맞는 JDK 선택, 설치 확인, source 작성, compile, run 순서를 제시한다. `java -version`은 현재 shell에서 실행되는 Java를 확인하는 명령이다. 이것만으로 source 파일과 compile 설정까지 올바르다고 결론 내리지는 않는다.

Windows에서 명령을 찾지 못할 때 자료는 JDK의 `bin` 경로를 `Path`에 추가하고 PowerShell을 다시 여는 절차를 설명한다. Mac에서는 설치 뒤 Terminal에서 버전을 확인한다. 파일 확장자를 표시해 `HelloWorld.java.txt`를 만들지 않도록 하고, source가 있는 directory에서 compile한다. [[courses/computer_programming/transcripts/2026-09-03|2026-09-03 STT]] 08:06의 `javac HelloWorld.java`도 이 흐름에 놓인다. 이는 수업 절차를 읽는 설명이다. 자료가 지정한 11.0.32.1과 Mac 화면의 16.0.2·11.0.16.1은 서로 다른 역사적 버전 표기이므로 동일한 설치 상태로 합치지 않는다.

IDE(Integrated Development Environment, 통합 개발 환경)는 editor, compile 기능, debugger를 한 환경에 모은다. IntelliJ 예제에서는 Java project를 만들고 JDK를 선택한 뒤 `src`에 `HelloWorld` class를 작성한다. Application run configuration의 main class를 올바르게 지정하고 Run 창에서 출력을 확인한다. 설정의 표시 이름을 바꿨다고 실행 대상 class까지 바뀌는 것은 아니다. IDE는 같은 compile·실행 과정을 편리하게 연결한다.

| 관찰된 문제 | 먼저 구별할 단계 |
| --- | --- |
| `java`를 찾지 못함 | 도구 설치와 shell의 경로 탐색 |
| 파일이 `.java.txt`임 | Source 파일명과 확장자 |
| public class와 파일명이 다름 | Compile 시 이름 검사 |
| 다른 main class가 실행됨 | IDE의 실행 대상 설정 |
| 출력이 보이지 않음 | 실행 성공 여부와 Run 출력 창 |

Lab02에는 재설치 없이 license를 활성화하는 보완 절차도 있다. 자료의 메뉴 순서는 Help → Manage Subscriptions… → Log in to JetBrains Account → Activate → 재시작이다. 계정 등록, software 설치, license 활성화는 서로 다른 확인 항목이다. [Lab02, PDF pp.3–5](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab02.v4.pdf)

## 핵심 정리

- 한 번 맞은 출력만으로 입력 경계·자원·오류 조건까지 검증되지는 않는다.
- `javac`는 bytecode를 만들고 플랫폼별 JVM이 실행한다.
- `void`와 출력, naming convention과 파일명 규칙을 구별한다.
- IDE도 JDK·source·main class를 연결해 compile하고 실행한다.

## 확인·연습문제

### 개념과 실행을 확인하기

#### 확인 Q01 · 정답 한 번과 검증

AI 코드가 예시 입력에서 정답을 냈다. Programming의 세 단계와 추가 검증을 설명하고 readability·maintenance·efficiency를 연결하라.

<details><summary>해설 보기</summary>

입력·출력·제약을 정의하고 작업을 나누어 구현한 뒤 실제 동작을 요구와 대조한다. 다른 입력과 경계값, 시간·memory·CPU 제한, 오류와 의도하지 않은 동작도 확인해야 한다. Readability는 상태 변화를 읽어 설명하게 하고 maintenance는 이후 수정을 쉽게 하며 efficiency는 자원 사용을 다룬다. AI 작성 여부는 이런 검증을 없애지 않는다.

**확인 기준:** 세 단계와 입력·자원 조건, 세 품질 기준을 구별한다.

</details>

#### 확인 Q02 · Compiler와 JVM

`HelloWorld.java`의 compile·run 명령과 결과를 설명하고 JVM·JRE·JDK 및 `.class`와 native executable을 구별하라.

<details><summary>해설 보기</summary>

`javac HelloWorld.java`는 `.class` bytecode를 만들고 `java HelloWorld`는 대상 JVM에서 그 class를 실행하도록 요청한다. `.class`는 OS native executable이 아니다. 수업 모델에서 JRE는 JVM과 Java package classes, JDK는 여기에 compile 등의 개발 도구를 더한다. 플랫폼별 JVM이 실행 차이를 담당하며 이 그림이 현재 모든 제품의 포장 방식을 정하지는 않는다.

**확인 기준:** 명령의 단계와 도구 역할을 각각 설명한다.

</details>

#### 확인 Q03 · `main`과 출력 읽기

`public class HelloWorld`를 `Hello.java`에 저장하면? `public static void main(String[] args)`와 `System.out.println("Hello, world!");`의 요소, 주석·중괄호, 관례와 규칙을 설명하라.

<details><summary>해설 보기</summary>

`public` class와 파일명 불일치로 compile error가 난다. `HelloWorld.java`가 이 예의 파일명이며 PascalCase는 별도 관례다. `public`은 접근, `static`은 class 소속, `void`는 반환값 없음, `main`은 이 예의 진입점, `String[] args`는 문자열 배열 parameter다. 중괄호는 class·method 범위, semicolon은 출력문 끝이다. `//`는 줄 끝, `/* ... */`는 그 사이를 주석으로 만든다. `System.out`의 `println`은 `Hello, world!`와 줄바꿈을 출력한다. 출력은 반환과 별개라 void여도 가능하며 모든 class에 main이 필요한 것은 아니다.

**확인 기준:** 대소문자·쉼표와 출력/반환 구별을 보존한다.

</details>

#### 확인 Q04 · 환경 오류 분류

`java`를 못 찾음, `.java.txt` 파일, 다른 main class 실행, license 미활성화를 구별하라. IDE는 수동 실행을 어떻게 연결하는가?

<details><summary>해설 보기</summary>

첫째는 설치·shell 경로 문제로 자료는 JDK bin을 Path에 추가하고 shell을 다시 연다. 둘째는 확장자 문제다. 셋째는 run configuration의 실행 대상 문제이며 표시 이름과 다르다. 넷째는 설치와 별개인 계정·활성화 문제로 Lab02는 활성화 후 재시작을 안내했다. 수동으로 source directory에서 compile한 뒤 class를 실행한다. IDE도 project JDK, src의 class, main class를 연결해 compile/run하고 Run 창에 출력한다. `java -version`만 성공했다고 source·compiler 설정까지 맞는 것은 아니다.

**확인 기준:** 네 오류를 분리하고 IDE에서도 compile/run 단계를 유지한다.

</details>

### 적용 연습

#### 연습 P01 · 점검 순서 설계

**새로 작성한 강의 기반 일반 연습.** 직접 대응 기출은 없다. 버전 확인은 성공하지만 파일은 `HelloWorld.java.txt`이고 IDE는 다른 class를 실행한다. 재설치를 제안한 동료에게 먼저 할 점검과 각 점검의 증거를 설명하라.

<details><summary>해설 보기</summary>

확장자를 표시해 public class와 맞는 `HelloWorld.java`인지 확인한다. Source directory에서 `javac HelloWorld.java` 결과로 compile 성공을, `java HelloWorld` 결과로 해당 class 실행을 확인한다. IDE에서는 project JDK와 main class를 확인한 뒤 Run 출력을 비교한다. 마지막으로 literal과 입력·경계 요구를 대조한다. 버전 확인은 도구 탐색만, compile은 source 번역만 확인하므로 한 단계 성공으로 전체를 판정할 수 없다. 제시된 파일·실행 대상 문제는 재설치만으로 해결된다고 볼 근거가 없다.

**확인 기준:** 두 관찰된 원인과 단계별 제한을 모두 짚는다.

</details>

### 복습 순서

Q01의 검증 기준을 말한 뒤 Q02–Q03을 보지 않고 설명한다. Q04와 P01에서는 관찰마다 어느 단계가 확인되었는지 표시한다.

## 출처

### 날짜별 강의와 녹음

- [[courses/computer_programming/lectures/2026-09-01-lecture-01|2026-09-01 · Computer Programming 강의·원자료]]
- [[courses/computer_programming/lectures/2026-09-03-lecture-02|2026-09-03 · Computer Programming 강의·원자료]]
- [[courses/computer_programming/lectures/2026-09-08-lecture-03|2026-09-08 · Computer Programming 강의·원자료]]
- [[courses/computer_programming/lectures/2026-09-10-lecture-04|2026-09-10 · Computer Programming 강의·원자료]]
- [[courses/computer_programming/lectures/2026-09-15-lecture-05|2026-09-15 · Computer Programming 강의·원자료]]
- [[courses/computer_programming/transcripts/2026-09-01|2026-09-01 보정 녹음문]] — 12:22–13:03.
- [[courses/computer_programming/transcripts/2026-09-03|2026-09-03 보정 녹음문]] — 02:20, 08:06.
- [[courses/computer_programming/transcripts/2026-09-08|2026-09-08 보정 녹음문]] — 53:25.
- [[courses/computer_programming/transcripts/2026-09-10|2026-09-10 보정 녹음문]] — 00:47.
- [[courses/computer_programming/transcripts/2026-09-15|2026-09-15 보정 녹음문]] — 40:13.

### 강의자료와 해당 페이지

- [Lecture 1 Introduction.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/1.intro.pdf) — [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/1.intro/page-004), [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/1.intro/page-008).
- [Lecture 2 Java Basics 1.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/2.java.basics.1.pdf) — [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-009), [p.13](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-013), [p.15](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-015), [p.20](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-020), [p.24](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/2.java.basics.1/page-024).
- [Lab01.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab01.pdf) — [PDF p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab01.pdf#page=8), [PDF p.29](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab01.pdf#page=29), [PDF p.63](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab01.pdf#page=63).
- [Lab02 v4.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab02.v4.pdf) — [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_programming/lab02.v4/page-005).

JDK 지정값 11.0.32.1과 Mac 화면의 16.0.2·11.0.16.1은 서로 다른 역사적 표기다. 설치·계정·license 절차는 당시 자료의 예이며 최신 지침으로 확인한 내용이 아니다. 녹음문의 불확실성도 유지된다.


---

[[courses/computer_programming/units/index|단원 목차]] · [[courses/computer_programming/units/types-expressions|다음: Variables·Types·Operators와 String →]]
