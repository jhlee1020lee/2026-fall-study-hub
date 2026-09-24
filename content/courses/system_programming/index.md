---
title: "시스템프로그래밍"
description: "시스템프로그래밍 단원 교과서와 강의 기록"
cssclasses: ["unit-index"]
---

아래 순서로 단원을 읽으세요. 각 단원에서 연결된 원자료·수업 기록과 연습문제를 확인할 수 있습니다.

## 단원 목차

1. **System Programming과 C 프로그램의 구성·빌드** · [[courses/system_programming/units/systems-c-build|한국어]] · [[courses/system_programming/units/en/systems-c-build|English]]

   C의 실행 흐름, 개발 환경과 build 단계를 함께 복습한다.

2. **C object·type·주소와 pointer** · [[courses/system_programming/units/objects-pointers|한국어]] · [[courses/system_programming/units/en/objects-pointers|English]]

   Type·주소·lifetime으로 pointer 코드와 memory 크기를 검산한다.

3. **문자 처리와 DFA·Decommenter의 경계조건** · [[courses/system_programming/units/state-machines|한국어]] · [[courses/system_programming/units/en/state-machines|English]]

   DFA transition과 세 출력 관측값으로 문자 처리의 경계를 검토한다.

4. **Unix file·directory·inode와 metadata** · [[courses/system_programming/units/files-metadata|한국어]] · [[courses/system_programming/units/en/files-metadata|English]]

   File type, link와 mount, stat·directory API의 의미를 연결한다.

5. **Permission·실행 identity·확장 metadata** · [[courses/system_programming/units/permissions|한국어]] · [[courses/system_programming/units/en/permissions|English]]

   Permission bit, effective identity, ACL과 xattr의 역할·한계를 구별한다.

6. **Unix I/O·열린 파일 상태·stdio buffering** · [[courses/system_programming/units/io-streams|한국어]] · [[courses/system_programming/units/en/io-streams|English]]

   Unix I/O와 stdio를 반환 단위·공유 offset·buffering으로 비교한다.

7. **Process memory·alignment·호출의 실제 표현** · [[courses/system_programming/units/memory-layout|한국어]] · [[courses/system_programming/units/en/memory-layout|English]]

   Memory section, padding·stride와 parameter passing을 byte 단위로 검토한다.

8. **Dirtree의 순회·filter·출력 계약과 설계** · [[courses/system_programming/units/dirtree|한국어]] · [[courses/system_programming/units/en/dirtree|English]]

   Dirtree의 출력 계약·depth·filter·memory 책임을 검산한다.

## 원자료와 강의 기록

- [[courses/system_programming/materials|교수 제공 자료 목록과 다운로드]]
- [[courses/system_programming/lectures/index|날짜별 강의노트와 보정 STT]]

[[courses/system_programming/units/index#자료별로-단원-찾기|자료 파일 이름으로 단원 찾기]]

## 개념과 관련 자료 찾아보기

- [[concepts/함수|Function(함수)]]
- [[concepts/반복문|Loop(반복문)]]
- [[concepts/타입|Type(타입)]]
- [[concepts/access-control-list|Access Control List]]
- [[concepts/chmod|chmod]]
- [[concepts/extended-file-attributes|Extended file attributes]]
- [[concepts/file-descriptor|File descriptor]]
- [[concepts/file-offset|Current file position]]
- [[concepts/file-permissions|File permissions]]
- [[concepts/filesystem-hierarchy-standard|Filesystem Hierarchy Standard]]
- [[concepts/hard-link|Hard link]]
- [[concepts/inode|Inode]]
- [[concepts/mount-point|Mount point]]
- [[concepts/real-effective-identity|Real and effective identity]]
- [[concepts/standard-io|Standard I/O]]
- [[concepts/suid-sgid|SUID and SGID]]
- [[concepts/symbolic-link|Symbolic link]]
- [[concepts/system-call|System call]]
- [[concepts/unix-filesystem|Unix filesystem]]
- [[concepts/unix-io|Unix I/O]]
- [[concepts/binary-io|Binary data와 I/O]]
- [[concepts/c-string|C-string interpretation]]
- [[concepts/directory-entry|Directory entry]]
- [[concepts/directory-stream|Directory stream]]
- [[concepts/dup|Descriptor duplication]]
- [[concepts/file-descriptor-passing|descriptor passing]]
- [[concepts/file-metadata|File metadata]]
- [[concepts/fork|inherited descriptors]]
- [[concepts/indirection|indirection]]
- [[concepts/io-redirection|I/O redirection]]
- [[concepts/open-file-table|Open file table]]
- [[concepts/pathname|Pathname]]
- [[concepts/stat-family|fstatat]]
- [[concepts/async-signal-safety|Async-signal safety]]
- [[concepts/buffering|Buffering]]
- [[concepts/file-mode|File mode]]
- [[concepts/file-stream|FILE stream]]
- [[concepts/file-timestamps|File timestamps]]
- [[concepts/flushing|Flushing]]
- [[concepts/formatted-io|Formatted I/O]]
- [[concepts/kernel-space|Kernel space]]
- [[concepts/lseek|lseek]]
- [[concepts/read-ahead|Read-ahead]]
- [[concepts/short-count|Short count]]
- [[concepts/sparse-file|Sparse file]]
- [[concepts/standard-streams|Standard streams]]
- [[concepts/user-space|User space]]
- [[concepts/arrays|Arrays]]
- [[concepts/command-line-arguments|Command line parameters]]
- [[concepts/data-alignment|Data alignment]]
- [[concepts/data-types|Data types]]
- [[concepts/directory-traversal|Directory traversal]]
- [[concepts/dynamic-memory-allocation|Dynamic allocation]]
- [[concepts/memory-abstraction|Memory abstraction]]
- [[concepts/memory-layout|Memory layout]]
- [[concepts/parameter-passing|Parameter passing]]
- [[concepts/pattern-matching|Pattern matching]]
- [[concepts/pointers|Pointers]]
- [[concepts/sizeof|sizeof]]
- [[concepts/struct|Structures]]
- [[concepts/union|Unions]]
- [[concepts/virtual-memory|Virtual memory]]
- [[concepts/abi|ABI]]
- [[concepts/aslr|ASLR]]
- [[concepts/process|Process]]
- [[concepts/virtual-address|virtual address]]
