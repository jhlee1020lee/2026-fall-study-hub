---
title: "String pool"
tags:
  - concept
  - computer_programming
review_status: approved
---

# String pool

## 정의

String pool(문자열 풀)은 같은 String literal(문자열 리터럴)이 하나의 String object(문자열 객체)를 함께 가리킬 수 있게 하는 공간이다. String은 immutable(불변인) object이므로 생성된 내용이 바뀌지 않는다. `new String("Apple")`은 명시적으로 새 object를 만드는 반면, 동일한 literal을 사용하는 variable(변수)들은 같은 object를 가리킬 수 있다. [STT 01:11:45-01:15:24] [M02 p.43-49]

`appleTwo = "Pear"`는 기존 "Apple" object의 문자를 수정하지 않는다. Variable이 담은 reference(참조)가 "Pear"를 가리키도록 바뀐다. 따라서 String의 내용과 variable의 reference를 분리해서 읽으면 immutability(불변성)와 assignment(대입)를 함께 설명할 수 있다. [STT 01:11:45-01:15:24] [M02 p.43-49]

## 관련 강의

- [[courses/computer_programming/lectures/2026-09-01-lecture-01|Computer Programming · 2026-09-01 · 1강]]

## 연결 개념

관련 강의가 누적되면서 확장됩니다.
