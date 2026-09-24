---
title: "컴퓨터구조"
description: "컴퓨터구조 단원 교과서와 강의 기록"
cssclasses: ["unit-index"]
---

아래 순서로 단원을 읽으세요. 각 단원에서 연결된 원자료·수업 기록과 연습문제를 확인할 수 있습니다.

## 단원 목차

1. **컴퓨터의 구성과 ISA: 명세에서 구현까지** · [[courses/computer_architecture/units/architecture-contract|한국어]] · [[courses/computer_architecture/units/en/architecture-contract|English]]

   ISA의 계약, 컴퓨터 구성, RISC의 선택과 multicore의 동기를 연결한다.

2. **프로그램 번역·Linking·Loading** · [[courses/computer_architecture/units/program-translation-loading|한국어]] · [[courses/computer_architecture/units/en/program-translation-loading|English]]

   Separate compilation부터 linking·loading과 세 instruction의 상태 변화까지 추적한다.

3. **데이터 표현·Register·Memory** · [[courses/computer_architecture/units/data-register-memory|한국어]] · [[courses/computer_architecture/units/en/data-register-memory|English]]

   Register 계산, byte 주소, endianness, 정수 표현과 load/store 폭을 함께 확인한다.

4. **Instruction의 비트 표현과 주소 구성** · [[courses/computer_architecture/units/instruction-encoding|한국어]] · [[courses/computer_architecture/units/en/instruction-encoding|English]]

   R/I/S field, PC-relative 변위와 signed immediate를 이용한 큰 상수 구성을 확인한다.

5. **Bitwise operation·분기·Synchronization** · [[courses/computer_architecture/units/control-synchronization|한국어]] · [[courses/computer_architecture/units/en/control-synchronization|English]]

   Mask·분기·array loop·signed 비교와 LR/SC의 두 가지 검사를 연결한다.

6. **Procedure 호출·Calling convention·Stack** · [[courses/computer_architecture/units/procedures-stack|한국어]] · [[courses/computer_architecture/units/en/procedures-stack|English]]

   Calling convention, frame 배치, leaf·factorial·string copy의 보존과 복귀를 추적한다.

7. **실행시간과 Performance 모형** · [[courses/computer_architecture/units/performance-model|한국어]] · [[courses/computer_architecture/units/en/performance-model|English]]

   Latency·CPU time·speedup과 Amdahl의 한계로 성능 주장을 계산한다.

8. **Workload·평균·성능 비교** · [[courses/computer_architecture/units/performance-comparison|한국어]] · [[courses/computer_architecture/units/en/performance-comparison|English]]

   Workload와 weight에 맞춰 runtime·normalized ratio·aggregate IPC를 집계한다.

## 원자료와 강의 기록

- [[courses/computer_architecture/materials|교수 제공 자료 목록과 다운로드]]
- [[courses/computer_architecture/lectures/index|날짜별 강의노트와 보정 STT]]

[[courses/computer_architecture/units/index#자료별로-단원-찾기|자료 파일 이름으로 단원 찾기]]

## 개념과 관련 자료 찾아보기

- [[concepts/von-neumann-architecture|von Neumann architecture(폰 노이만 구조)]]
- [[concepts/moores-law|Moore's Law(무어의 법칙)]]
- [[concepts/microarchitecture|Microarchitecture(마이크로아키텍처)]]
- [[concepts/instruction-set-architecture|Instruction Set Architecture(ISA; 명령어 집합 구조)]]
- [[concepts/dennard-scaling|Dennard scaling(데나드 스케일링)]]
- [[concepts/amdahls-law|Amdahl’s Law]]
- [[concepts/benchmarking|Benchmark]]
- [[concepts/cpi-ipc|CPI와 IPC]]
- [[concepts/cpu-execution-time|CPU execution time]]
- [[concepts/latency-throughput|Latency와 Throughput]]
- [[concepts/arithmetic-mean|arithmetic mean]]
- [[concepts/benchmark|Benchmark]]
- [[concepts/cpi|CPI]]
- [[concepts/geometric-mean|geometric mean]]
- [[concepts/harmonic-mean|harmonic mean]]
- [[concepts/instruction-mix|instruction mix]]
- [[concepts/ipc|IPC]]
- [[concepts/latency|Latency]]
- [[concepts/relative-performance|Relative performance]]
- [[concepts/single-cycle-processor|single-cycle processor]]
- [[concepts/speedup|speedup]]
- [[concepts/throughput|throughput]]
- [[concepts/weighted-arithmetic-mean|weighted arithmetic mean]]
- [[concepts/workload|Workload]]
