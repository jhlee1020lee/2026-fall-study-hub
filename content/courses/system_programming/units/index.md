---
title: "시스템프로그래밍 단원 목차"
description: "시스템프로그래밍 교과서 읽기 순서"
cssclasses: ["unit-index"]
---

개념 설명 → 예제 → 강의에서 덧붙인 설명 → 확인·연습문제 순서로 읽으세요. 출처의 날짜·페이지·시각은 각 단원에서 확인할 수 있습니다.

1. **System Programming과 C 프로그램의 구성·빌드** · [[courses/system_programming/units/systems-c-build|한국어]] · [[courses/system_programming/units/en/systems-c-build|English]]

   C의 기본 제어 흐름, build 단계, local·remote 작업의 차이를 복습한다.

2. **C object·type·주소와 pointer** · [[courses/system_programming/units/objects-pointers|한국어]] · [[courses/system_programming/units/en/objects-pointers|English]]

   Type, pointer 대입, array 변환, 동적 storage의 크기와 수명을 확인한다.

3. **문자 처리와 DFA·Decommenter의 경계조건** · [[courses/system_programming/units/state-machines|한국어]] · [[courses/system_programming/units/en/state-machines|English]]

   DFA transition과 세 출력 관측값으로 문자 처리의 경계를 검토한다.

4. **Unix file·directory·inode와 metadata** · [[courses/system_programming/units/files-metadata|한국어]] · [[courses/system_programming/units/en/files-metadata|English]]

   File type, link와 mount, stat·directory API의 의미를 연결한다.

5. **Permission·실행 identity·확장 metadata** · [[courses/system_programming/units/permissions|한국어]] · [[courses/system_programming/units/en/permissions|English]]

   File·directory 권한, set-ID identity, ACL·xattr의 역할을 구분한다.

6. **Unix I/O·열린 파일 상태·stdio buffering** · [[courses/system_programming/units/io-streams|한국어]] · [[courses/system_programming/units/en/io-streams|English]]

   Unix I/O와 stdio를 반환 단위·공유 offset·buffering으로 비교한다.

7. **Process memory·alignment·호출의 실제 표현** · [[courses/system_programming/units/memory-layout|한국어]] · [[courses/system_programming/units/en/memory-layout|English]]

   Process storage, padding, union, 값 전달과 IA-32 frame을 복습한다.

8. **Dirtree의 순회·filter·출력 계약과 설계** · [[courses/system_programming/units/dirtree|한국어]] · [[courses/system_programming/units/en/dirtree|English]]

   Traversal·출력 폭·통계·pattern 문법을 구분하여 Dirtree 명세를 점검한다.

9. **Memory hierarchy·locality와 cache 교체** · [[courses/system_programming/units/cache-hierarchy|한국어]] · [[courses/system_programming/units/en/cache-hierarchy|English]]

   Locality와 block 이동에서 conflict·LRU·clock까지 cache의 판단 과정을 복습한다.

10. **Virtual Memory·page translation·공유와 보호** · [[courses/system_programming/units/virtual-memory|한국어]] · [[courses/system_programming/units/en/virtual-memory|English]]

   Page 변환·fault·공유 mapping과 역사적 TLB/data-cache 주소 경로를 복습한다.

## 자료별로 단원 찾기

원자료 파일에 연결된 단원입니다. 실제로 다룬 페이지·슬라이드와 자료 버전은 각 단원의 출처에서 확인하세요.

- **01.CProgrammingExamples.pptx** — [[courses/system_programming/units/systems-c-build|System Programming과 C 프로그램의 구성·빌드]] ([[courses/system_programming/units/en/systems-c-build|English]]) · [[courses/system_programming/units/state-machines|문자 처리와 DFA·Decommenter의 경계조건]] ([[courses/system_programming/units/en/state-machines|English]])
- **00.Introduction.pptx** — [[courses/system_programming/units/systems-c-build|System Programming과 C 프로그램의 구성·빌드]] ([[courses/system_programming/units/en/systems-c-build|English]]) · [[courses/system_programming/units/objects-pointers|C object·type·주소와 pointer]] ([[courses/system_programming/units/en/objects-pointers|English]]) · [[courses/system_programming/units/state-machines|문자 처리와 DFA·Decommenter의 경계조건]] ([[courses/system_programming/units/en/state-machines|English]]) · [[courses/system_programming/units/io-streams|Unix I/O·열린 파일 상태·stdio buffering]] ([[courses/system_programming/units/en/io-streams|English]])
- **10.RE.Life.Cycle.of.a.Program.pptx** — [[courses/system_programming/units/systems-c-build|System Programming과 C 프로그램의 구성·빌드]] ([[courses/system_programming/units/en/systems-c-build|English]])
- **11.RE.Linking.and.Loading.pptx** — [[courses/system_programming/units/systems-c-build|System Programming과 C 프로그램의 구성·빌드]] ([[courses/system_programming/units/en/systems-c-build|English]])
- **02.CPointers_24a7628c.pptx** — [[courses/system_programming/units/objects-pointers|C object·type·주소와 pointer]] ([[courses/system_programming/units/en/objects-pointers|English]])
- **06.MM.Variable.and.Memory.Recap.pptx** — [[courses/system_programming/units/objects-pointers|C object·type·주소와 pointer]] ([[courses/system_programming/units/en/objects-pointers|English]]) · [[courses/system_programming/units/memory-layout|Process memory·alignment·호출의 실제 표현]] ([[courses/system_programming/units/en/memory-layout|English]]) · [[courses/system_programming/units/virtual-memory|Virtual Memory·page translation·공유와 보호]] ([[courses/system_programming/units/en/virtual-memory|English]])
- **08.MM.Dynamic.Memory.Allocation.I.pptx** — [[courses/system_programming/units/objects-pointers|C object·type·주소와 pointer]] ([[courses/system_programming/units/en/objects-pointers|English]])
- **09.MM.Dynamic.Memory.Allocation.II.pptx** — [[courses/system_programming/units/objects-pointers|C object·type·주소와 pointer]] ([[courses/system_programming/units/en/objects-pointers|English]])
- **03.IO.Unix.Filesystem.Concepts.pptx** — [[courses/system_programming/units/files-metadata|Unix file·directory·inode와 metadata]] ([[courses/system_programming/units/en/files-metadata|English]]) · [[courses/system_programming/units/permissions|Permission·실행 identity·확장 metadata]] ([[courses/system_programming/units/en/permissions|English]])
- **04.IO.Direct.and.Buffered.IO_8e725857.pptx** — [[courses/system_programming/units/files-metadata|Unix file·directory·inode와 metadata]] ([[courses/system_programming/units/en/files-metadata|English]]) · [[courses/system_programming/units/io-streams|Unix I/O·열린 파일 상태·stdio buffering]] ([[courses/system_programming/units/en/io-streams|English]])
- **05.IO.Files.and.Directories_3d312c60.pptx** — [[courses/system_programming/units/files-metadata|Unix file·directory·inode와 metadata]] ([[courses/system_programming/units/en/files-metadata|English]]) · [[courses/system_programming/units/permissions|Permission·실행 identity·확장 metadata]] ([[courses/system_programming/units/en/permissions|English]]) · [[courses/system_programming/units/io-streams|Unix I/O·열린 파일 상태·stdio buffering]] ([[courses/system_programming/units/en/io-streams|English]])
- **04.IO.Direct.and.Buffered.IO.pptx** — [[courses/system_programming/units/io-streams|Unix I/O·열린 파일 상태·stdio buffering]] ([[courses/system_programming/units/en/io-streams|English]])
- **EE209 AssemblyFunctions.pptx** — [[courses/system_programming/units/memory-layout|Process memory·alignment·호출의 실제 표현]] ([[courses/system_programming/units/en/memory-layout|English]])
- **lab 2 input and output.pptx** — [[courses/system_programming/units/dirtree|Dirtree의 순회·filter·출력 계약과 설계]] ([[courses/system_programming/units/en/dirtree|English]])
- **lab 2 input and output_2b90a395.pptx** — [[courses/system_programming/units/dirtree|Dirtree의 순회·filter·출력 계약과 설계]] ([[courses/system_programming/units/en/dirtree|English]])
- **07.MM.Virtual.Memory.Recap.pptx** — [[courses/system_programming/units/cache-hierarchy|Memory hierarchy·locality와 cache 교체]] ([[courses/system_programming/units/en/cache-hierarchy|English]]) · [[courses/system_programming/units/virtual-memory|Virtual Memory·page translation·공유와 보호]] ([[courses/system_programming/units/en/virtual-memory|English]])
- **07.MM.Virtual.Memory.Recap_2ffc3cf7.pptx** — [[courses/system_programming/units/cache-hierarchy|Memory hierarchy·locality와 cache 교체]] ([[courses/system_programming/units/en/cache-hierarchy|English]]) · [[courses/system_programming/units/virtual-memory|Virtual Memory·page translation·공유와 보호]] ([[courses/system_programming/units/en/virtual-memory|English]])

## 원자료와 강의 기록

- [[courses/system_programming/materials|교수 제공 자료 목록과 다운로드]]
- [[courses/system_programming/lectures/index|날짜별 강의노트와 보정 STT]]
