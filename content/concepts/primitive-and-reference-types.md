---
title: "primitive vs reference"
tags:
  - concept
  - computer_programming
review_status: approved
---

# primitive vs reference

## 정의

Primitive type(기본 자료형)의 variable(변수)은 해당 값을 직접 담고, reference type(참조 자료형)의 variable은 object(객체)를 가리키는 reference(참조)를 담는다. Java의 primitive type은 `byte`, `short`, `int`, `long`, `float`, `double`, `char`, `boolean`의 여덟 가지다. String, array(배열), class(클래스), interface(인터페이스)는 non-primitive type(비기본 자료형)의 예이며 reference type이라고 부른다. Reference는 `null`일 수도 있다. [STT 56:24-59:47, 01:19:22] [M02 p.26-32, p.49]

Assignment(대입)에서도 이 차이가 유지된다. Primitive assignment는 값을 복사하고 reference assignment는 reference를 복사하므로, 두 variable이 같은 object를 가리킬 수 있다. [[concepts/object-oriented-programming|OOP(Object-oriented programming, 객체 지향 프로그래밍)]]에서 object를 추적하려면 variable과 object를 분리해 생각해야 한다. [[concepts/string-pool|String pool(문자열 풀)]]의 예시에서는 `appleTwo = "Pear"`가 variable의 reference를 바꾸며 기존 String object의 내용은 바꾸지 않는다. [STT 01:11:45-01:15:24] [M02 p.47-49]

## 관련 강의

- [[courses/computer_programming/lectures/2026-09-01-lecture-01|Computer Programming · 2026-09-01 · 1강]]

## 연결 개념

관련 강의가 누적되면서 확장됩니다.
