---
title: "Instruction Set Architecture(ISA; 명령어 집합 구조)"
tags:
  - concept
  - computer_architecture
review_status: approved
---

# Instruction Set Architecture(ISA; 명령어 집합 구조)

## 정의

**ISA**는 software가 관찰할 수 있는 processor(프로세서)의 기능적 계약이다. 어떤 instruction(명령어)을 제공하고 어떤 결과를 내야 하는지 규정하며, 그 계약을 실제로 구현하는 [[concepts/microarchitecture|microarchitecture(마이크로아키텍처)]]와 구분한다. [STT 15:25-17:56] [M01 p.11]

```text
program / compiler
        ↓
**ISA** ── 호환성·기능 명세
        ↓ 구현
[[concepts/microarchitecture|microarchitecture]] ── datapath·control·pipeline·cache
        ↓ 구성
logic gates ── NAND 등 boolean function
        ↓ 물리적 구현
transistors ── control로 켜고 끄는 switch
```

## 관련 강의

- [[courses/computer_architecture/lectures/2026-09-01-lecture-01|Computer Architecture · 2026-09-01 · 1강]]

## 연결 개념

관련 강의가 누적되면서 확장됩니다.
