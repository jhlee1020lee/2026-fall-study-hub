---
title: "String pool"
tags:
  - concept
  - computer_programming
review_status: approved
---

# String pool

## 정의

동일한 literal은 String pool의 같은 immutable String을 참조할 수 있다. `new String("Apple")`은 명시적으로 새 String object를 만든다. `appleTwo = "Pear"`는 기존 "Apple" object의 문자를 바꾸는 것이 아니라 `appleTwo` reference가 "Pear"를 가리키도록 바꾸는 것이다. String의 value와 variable이 담은 reference를 분리해서 생각해야 한다. **String pool**은 literal 중복을 줄이는 메커니즘이다. [STT 01:11:45-01:15:24] [M02 p.43-49]

## 관련 강의

- [[courses/computer_programming/lectures/2026-09-01-lecture-01|Computer Programming · 2026-09-01 · 1강]]

## 연결 개념

관련 강의가 누적되면서 확장됩니다.
