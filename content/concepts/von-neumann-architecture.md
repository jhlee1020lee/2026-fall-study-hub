---
title: "von Neumann architecture(폰 노이만 구조)"
tags:
  - concept
  - computer_architecture
review_status: approved
---

# von Neumann architecture(폰 노이만 구조)

## 정의

**von Neumann architecture**는 program과 data를 같은 memory에 저장하는 stored-program computer(프로그램 내장형 컴퓨터) 구조다. 강의에서는 program과 data가 하나의 통로를 공유하는 구조를 Harvard architecture(하버드 구조)의 분리된 저장공간·통로와 비교했다. [STT 21:31-24:09] [M01 p.14-15]

아래는 이 개념이 등장한 회차의 흐름이다.

1. 과목의 목표, 평가, RISC-V·Chisel 실습 구성을 안내했다. Lab 1~2는 single-cycle CPU, Lab 3은 five-stage pipelined CPU, Lab 4는 branch prediction을 다룬다. [STT 01:58-08:38] [M01 p.3-6]
2. Computer Architecture(컴퓨터구조)를 software와 digital circuit(디지털 회로) 사이의 abstraction(추상화)으로 정의했다. [STT 13:36-17:56] [M01 p.9-11]
3. ISA(명령어 집합 구조)와 microarchitecture(마이크로아키텍처)를 구분하고, 같은 ISA에 여러 구현이 존재할 수 있음을 설명했다. [STT 15:25-17:56] [M01 p.11]
4. **von Neumann architecture**와 Harvard architecture, CPU·memory·I/O의 전형적 구성을 살펴봤다. [STT 21:31-26:01] [M01 p.14-15]
5. transistor(트랜지스터)를 switch(스위치)로 보고 NAND 같은 logic gate(논리 게이트)를 구성하는 방향을 짚었다. [STT 28:29-31:30] [M01 p.19-20]
6. Moore's Law(무어의 법칙), Dennard scaling(데나드 스케일링)의 붕괴, multicore(멀티코어) 전환을 통해 현대 CPU 설계의 배경을 설명했다. [STT 32:11-40:38] [M01 p.22-27]
7. 학기 후반에는 GPU 설계 개요와 hardware security(하드웨어 보안)도 다룬다고 예고했다. [STT 41:36-42:53]

## 관련 강의

- [[courses/computer_architecture/lectures/2026-09-01-lecture-01|Computer Architecture · 2026-09-01 · 1강]]

## 연결 개념

관련 강의가 누적되면서 확장됩니다.
