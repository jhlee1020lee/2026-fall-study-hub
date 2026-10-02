---
title: "Docker 실습 환경과 CPU 과제 사양 읽기"
description: "Docker 준비와 Lab1 사양·worksheet를 경계에 맞게 읽는다."
course: "computer_architecture"
unit_id: "lab-environment-specification"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["Docker Install.pdf", "Lab 0 1.pdf"]
private_source_assets: []
source_lectures: ["courses/computer_architecture/lectures/2026-09-29-lecture-05"]
---

환경 준비, instruction 구현, 제출 요구를 구분해 읽자. 설치 안내의 단계와 worksheet가 요구하는 정보의 종류를 확인한다.

## Docker container와 실습 환경의 경계

실습 환경을 준비하는 일과 CPU instruction을 구현하는 일은 다르다. Lab0는 도구와 project 환경을 준비하고, Lab1은 주어진 사양에 맞게 instruction 동작을 구현한다. 9월 29일 안내는 모든 lab을 Docker container에서 수행하며 VSCode의 Dev Containers extension을 권장한다. Docker에 익숙하면 CLI 경로도 사용할 수 있지만 그 세부 사항은 `assignment-0.md`를 참조하도록 되어 있다. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 56:40]] [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 57:31]] [CA NM004 PDF p.2](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-002) [CA NM004 PDF p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-003) [[courses/computer_architecture/lectures/2026-09-29-lecture-05|2026-09-29 강의 노트]]

이 구분이 필요한 이유는 파일을 편집기에서 여는 것만으로 container 안의 실습 환경에 연결되었다고 볼 수 없기 때문이다. 자료의 흐름은 Docker 준비 → 제공 archive 압축 해제 → 생성된 folder 열기 → container build·연결이다.

[CA NM004 PDF p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-004)의 archive 이름은 `dinocpu-lab1.tar.gz`이고 압축 해제 예는 다음과 같다. 아래 command들은 instructor 문서를 읽기 위한 예이며 이 본문 작성 중 실행한 기록은 아니다.

```sh
tar -xzf dinocpu-lab1.tar.gz
```

자료는 이 작업으로 `dinocpu/`가 생긴다고 설명한다. [CA NM004 PDF p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-005)의 screenshot에서는 VSCode 오른쪽 아래 **Reopen in Container**를 강조한다. `dinocpu` folder를 연 다음 이 선택으로 VSCode가 container를 build하고 연결하는 흐름이다. Folder를 열었다는 사실, container를 만들었다는 사실, 그 안에 연결되었다는 사실을 구별해야 환경 상태를 이해할 수 있다.

Lab0는 Chisel 소개와 `first-hardware.md` tutorial 링크를 제공한다고 안내한다. Chisel이 익숙하지 않을 때 tutorial을 따라가는 것은 선택적 준비이며 Assignment0에는 제출물이 없다. [CA NM004 PDF p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-006) 제공된 자료에는 archive 내부, `assignment-0.md`, `first-hardware.md`가 없으므로 구체적인 Chisel 문법, build/test command나 실제 설치 성공을 여기서 추가로 확정하지 않는다. STT의 불명확한 이름 대신 archive와 Chisel의 철자는 문서에서 확인한 표기를 쓴다.

## OS별 설치 경로를 따로 읽기

다음 세부 순서는 **Docker Install 자료 기반 복습**이다. 9월 29일에 OS별 command를 모두 구두로 설명했다는 뜻이 아니며 현재 제품 UI·최신 버전이나 사용자의 설치 상태를 새로 확인한 안내도 아니다. 서로 다른 OS의 command를 한 순서로 모두 실행하는 것으로 읽지 않는다.

### Windows에서 WSL과 Ubuntu 경로로 이어지기

[CA NM003 PDF p.1](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-001)–[CA NM003 PDF p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-003)은 Windows 기능 켜기/끄기에서 **Windows Subsystem for Linux**를 활성화하고 재부팅한 뒤 administrator PowerShell에서 다음 두 command를 사용하는 흐름이다.

```powershell
wsl --install
wsl --set-default-version 2
```

첫 command는 WSL 설치, 둘째는 기본 version을 2로 설정하는 역할이다. 이어서 VSCode의 Dev Containers extension Settings에서 **Dev › Containers: Execute In WSL**을 활성화한다. PowerShell의 다음 command로 Ubuntu shell에 들어가 자료의 Ubuntu 절차를 계속한다.

```powershell
wsl
```

이때 이후 command의 실행 문맥은 Ubuntu shell이다. Windows PowerShell에서 시작했다는 이유로 뒤의 Linux command까지 모두 같은 shell 문법이라고 생각하면 안 된다.

### Ubuntu에서 Docker Engine과 실행 확인

[CA NM003 PDF p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-004)에는 Docker Engine 설치 script를 받아 실행하는 예와 현재 사용자를 docker group에 추가하는 예가 나란히 있다.

```sh
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
```

첫 줄은 source 문서에 있는 다운로드·설치 pipeline이고, 둘째는 사용자 group 구성을 바꾸는 command이다. WSL에서는 script가 warning과 약 20초의 대기를 표시할 수 있다고 자료에 적혀 있다. Group 변경 뒤 shell을 닫고 다시 열며, WSL 경로에서는 다시 `wsl`로 들어간 다음 확인하는 순서이다.

```sh
docker run hello-world
```

이 마지막 command는 환경에서 container 실행을 확인하는 단계이다. 여기서는 해당 문서의 절차와 command 역할을 읽었으며 다운로드·설치·실행을 수행하거나 성공했다고 주장하지 않는다.

### Mac의 두 대안과 version 출력

[CA NM003 PDF p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-005)–[CA NM003 PDF p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-006)의 option 1은 Apple chip 또는 Intel chip에 맞는 Docker Desktop을 선택하고, `.dmg`에서 `Docker.app`을 Applications로 옮긴 뒤 실행하는 흐름이다. Menu bar의 whale icon을 확인하고 다음으로 version을 읽는다.

```sh
docker --version
```

자료의 출력 예 `Docker version 28.0.1, build xxxxxxx`는 형태를 보여 주는 값이다. 현재 최신 버전 또는 과제의 필수 버전이라는 뜻이 아니다.

Option 2는 Homebrew 설치 후 app 실행, icon 확인, version 확인으로 이어지는 대안이다. [CA NM003 PDF p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-007)

```sh
brew install --cask docker
```

p.7에는 `docker —version`처럼 em dash가 보이지만 p.6의 표기는 두 ASCII hyphen을 쓴 `docker --version`이다. 두 표기의 문자 차이를 구분해야 한다. 위의 command block은 p.6의 철자를 사용한 것이며 p.7 원문을 조용히 바꾸어 인용한 것이 아니다.

## R/I arithmetic과 과제 사양의 범위

Lab1의 실제 안내는 **R-type과 I-type arithmetic/logic instruction만** 구현한다고 한다. 9월 1일 계획의 R-type 소개보다 구체적인 범위이다. I-type이라는 instruction format을 쓰는 모든 명령, 예를 들어 load 전체를 구현한다는 뜻은 아니다. [CA NM004 PDF p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-007) [CA NM004 PDF p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-008) [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 58:36]]

또한 일부 CPU control signal은 수업과 다르게 정의되어 있으므로 `assignment-1.md`의 사양에 따라야 한다. “같은 ALU를 선택한다”는 개념을 이해하는 것과 특정 control bit pattern을 결정하는 것은 다른 일이다. 강의의 control truth table을 그대로 복사하면 이름이 비슷해도 다른 동작을 만들 수 있다. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 59:36]]

여기에는 `assignment-1.md`, starter archive, tests가 제공되지 않았다. 따라서 정확한 signal encoding, TODO, 허용 변경 파일 목록이나 완성 implementation은 이 안내에서 도출할 수 없다. 대신 worksheet가 어떤 정보를 요구하는지는 원본 그림에서 읽을 수 있다.

### Worksheet의 port를 번호·data·control로 나누기

[CA NM004 PDF p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-009)는 완성 회로가 아니라 연결을 그려 넣는 blank worksheet이다. PC, Next PC, Control Unit, ALU Control, Instruction Memory, Register File, ALU, Immediate Generator가 떨어져 배치되어 있고, 주어진 `select 32 bits` block도 있다.

| 그림의 port 또는 block | 읽을 때 구분할 정보 |
|---|---|
| Register File의 `readreg1/readreg2`, `writereg` | 어느 register를 고르는지 나타내는 index |
| `readdata1/readdata2`, `writedata` | 선택된 register가 내거나 받을 data |
| `wen` | Register 갱신을 허용하는 control |
| ALU의 `inputx/inputy`, `operation`, `result` | 두 operand, operation 선택, 계산 결과 |
| Immediate Generator의 `instruction → sextImm` | Instruction field에서 확장한 immediate |
| Next PC의 `pc`, `imm`, `inputx/inputy`, `funct3`, `branch`, `jumptype` | 주소·조건·선택 정보의 구분 |

Control Unit은 opcode를 받아 `itype`, `aluop`, `src1/src2`, `branch`, `jumptype`, `resultselect`, `memop`, `toreg`, `regwrite`, `validinst`, `wordinst` 등을 내보낸다. ALU Control은 `aluop/itype/funct7/funct3/wordinst`를 받아 `operation`을 고른다. 이름은 정보의 역할을 읽는 단서이며, 그 이름만으로 encoding이나 truth table을 추정할 수는 없다.

Worksheet는 R/I 실행에 필요한 wire와 필요한 mux를 그리고, 각 wire의 폭과 일부 bit만 전달하는 경우의 bit slice를 표시하라고 요구한다. 예를 들어 `instruction[19:15]`의 폭은 $19-15+1=5$ bits이다. 이는 32-bit instruction 전체와도, 그 index가 선택한 register의 data 폭과도 다르다. Slice를 표시하는 이유는 단순히 선을 연결했다는 사실보다 **어떤 정보 몇 bits가 흐르는지**를 드러내기 위해서이다. 그림은 모든 module이나 port를 반드시 사용할 필요는 없다고도 적는다. 이 해설은 diagram을 읽는 방법이며 필요한 연결·mux의 완성 답을 채운 것은 아니다.

[CA NM004 PDF p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-008)과 9월 29일 59:36은 완성 worksheet 제출을 요구한다. [CA NM004 PDF p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-010)은 당시 deadline을 10/12 23:59 @ eTL로 적고 압축 파일 하나, code-only 제출과 debug/test 파일의 채점 제외를 안내한다. 이는 해당 자료에 적힌 과거 안내이며 실시간 일정 확인이 아니다. Worksheet 의무와 code-only archive 안내 사이의 구체적인 포장 방식은 제공된 자료에 없으므로 임의로 해결하지 않는다. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 STT 01:00:30]] 개념 이해, 환경 준비, 실제 제출 사양을 이렇게 구분해야 도구가 준비되었다는 사실을 구현 완료나 제출 완료로 착각하지 않게 된다.

## 핵심 정리

- Folder 열기, container build, container 연결은 서로 다른 상태다.
- Windows/WSL·Ubuntu·Mac 경로는 선택지이며 한 설치 순서로 합치지 않는다.
- Lab1은 R/I arithmetic·logic이며 control encoding은 실제 과제 문서가 기준이다.
- Register index·data·control·bit slice를 나누어 도면을 읽는다.

## 확인·연습문제

### 개념 확인

#### 확인 Q01 · Lab0의 준비 단계

Docker, Dev Containers, `dinocpu-lab1.tar.gz`, `dinocpu/`, Reopen in Container, Chisel tutorial의 역할을 순서대로 설명하라. Lab0에 제출이 필요한가?

<details><summary>해설 보기</summary>

자료는 Docker 준비 뒤 `tar -xzf dinocpu-lab1.tar.gz`로 압축 해제하여 `dinocpu/`를 만들고 VSCode에서 열도록 한다. Dev Containers의 Reopen in Container로 container build·연결을 진행한다. Folder만 열었다고 연결까지 증명되지는 않는다. Docker에 익숙하면 `assignment-0.md`의 CLI 대안이 있다. Lab0는 Chisel 소개와 선택 tutorial `first-hardware.md`를 안내하며 제출은 없다. 두 markdown과 archive 내부는 제공되지 않아 실제 syntax·build/test 명령이나 성공을 확인한 것은 아니다. 이는 source command의 역할 설명이다.

**채점·확인:** Tutorial 선택·제출 없음과 folder/build/connect 차이를 확인한다.

</details>

#### 확인 Q02 · Windows에서 Ubuntu로

Windows 자료의 WSL feature·재부팅·관리자 PowerShell·VSCode 설정·`wsl` 역할을 나누어 설명하라. Ubuntu의 설치·group·shell 재시작·실행 확인 단계는 어떤 역할인가? 명령을 실행하라는 문제가 아니라 자료 순서를 읽는 문제다.

<details><summary>해설 보기</summary>

자료 순서는 Windows Subsystem for Linux 활성화→재부팅→관리자 PowerShell의 `wsl --install`, `wsl --set-default-version 2`→Dev Containers Settings의 Dev › Containers: Execute In WSL→`wsl`로 Ubuntu shell 진입이다. 이어 Docker Engine 설치 script pipeline은 설치, `sudo usermod -aG docker $USER`는 group 구성, shell 재시작은 변경 뒤 환경 사용, `docker run hello-world`는 container 실행 확인이다. WSL에서 script의 warning·약20초 대기는 자료 설명이다. 모든 Linux 명령을 계속 PowerShell에서 실행하는 흐름이 아니며 설치 성공을 이 해설만으로 주장할 수 없다.

**채점·확인:** Shell 전환과 네 Ubuntu 단계의 다른 역할을 설명한다.

</details>

#### 확인 Q03 · Mac의 대안과 version 예

Mac option1과 option2의 설치·실행·확인을 비교하고 28.0.1 출력 및 `docker —version`/`docker --version` 차이를 설명하라.

<details><summary>해설 보기</summary>

Option1은 Apple/Intel chip에 맞는 Docker Desktop 선택→`.dmg`의 `Docker.app`을 Applications로 이동→app 실행→whale icon→version 확인이다. Option2는 `brew install --cask docker`를 쓰는 대안 뒤 app·icon·version을 확인한다. 둘을 순서대로 모두 설치하는 요구가 아니다. 28.0.1은 출력 형태 예이지 최신·필수 version 인증이 아니다. p.7 em dash와 p.6 두 ASCII hyphen은 다른 문자이며 해설에서는 p.6 철자를 구별해 읽는다.

**채점·확인:** 대안 관계, 예시 version, dash 차이를 모두 답한다.

</details>

#### 확인 Q04 · Lab1 범위와 계약

R/I arithmetic·logic 안내가 모든 I-type 구현을 뜻하는가? Classroom control table·`assignment-1.md`·제출 worksheet의 역할과 미제공 항목을 설명하라.

<details><summary>해설 보기</summary>

Load도 I-type일 수 있으므로 format만으로 과제 범위를 넓히면 안 된다. 실제 안내는 R/I arithmetic·logic이며 일부 control 정의가 수업과 달라 과제 문서가 구현 계약이다. Worksheet 제출은 요구되지만 `assignment-1.md`·starter·tests가 없어 정확한 control bits·TODO·허용 파일·완성 구현은 알 수 없다. 당시 p.10의 10/12 23:59와 압축 파일 하나·code-only·debug/test 채점 제외는 source-dated 안내다. Worksheet 의무와 archive 포장 관계는 명시되지 않아 임의로 해결하지 않는다.

**채점·확인:** 명세 부족을 추정 구현으로 채우지 않고 범위·제출 의무를 구별한다.

</details>

#### 확인 Q05 · Port의 정보 종류와 bit slice

Register File·ALU·Immediate Generator·Next PC의 port를 index/data/control로 분류하라. Control Unit과 ALU Control의 역할, `instruction[19:15]` 폭과 worksheet의 wire/mux 요구도 설명하라.

<details><summary>해설 보기</summary>

`readreg1/readreg2/writereg`는 index, `readdata1/readdata2/writedata`는 data, `wen`은 write 허용이다. ALU `inputx/inputy`는 operand, `operation`은 선택, `result`는 결과다. Immediate Generator는 instruction→`sextImm`, Next PC의 `pc/imm/inputx/inputy/funct3/branch/jumptype`는 주소·조건·선택을 구분한다. Control Unit은 opcode에서 `itype/aluop/src1/src2/branch/jumptype/resultselect/memop/toreg/regwrite/validinst/wordinst` 등을 내고 ALU Control은 `aluop/itype/funct7/funct3/wordinst`로 operation을 고른다. 이름만으로 bit encoding은 정해지지 않는다. `[19:15]`는 5 bits이며 32-bit instruction 전체·선택된 data 폭과 다르다. Worksheet는 필요한 wire·mux, 모든 wire 폭·partial slice를 표시하게 하며 모든 port를 반드시 쓰라는 것은 아니다. 제공된 `select 32 bits` block도 이 blank 도면의 일부다.

**채점·확인:** 5=19−15+1을 검산하고 정보 종류와 실제 연결 해답을 구별한다.

</details>

### 적용 연습

#### 연습 P01 · 완료 주장에 필요한 근거

새로 만든 강의·자료 기반 일반 연습이다. 한 학생이 'folder가 열리고 version 문자열이 보였으니 container 안의 Lab1 구현이 끝났다. 수업 표의 control bits를 그대로 쓰고 모든 port를 연결하면 된다'고 한다. 환경 상태와 과제 사양에 관한 주장을 각각 점검하고 다음에 확인할 근거를 적어라.

18개 exam 후보에는 Docker/WSL·Dev Containers·현재 Lab 범위와 worksheet 읽기를 평가하는 문항이 없다. Q14의 가상 ISA 확장을 현 과제 구현의 근거로 쓰지 않는다.

<details><summary>해설 보기</summary>

Folder와 version 출력은 각각 파일 열기와 version 정보만 확인한다. Container build·연결은 별도 상태이고 구현·검증·제출 완료도 따로 근거가 필요하다. Control 정의는 과제 문서와 다를 수 있고 worksheet는 불필요한 port가 있을 수 있다고 한다. 실제 `assignment-1.md`, starter와 tests에서 허용 scope·encoding·검증 기준을 확인해야 하며 현재 자료만으로 결과를 추정할 수 없다. Worksheet 제출 의무와 archive 포장 설명은 그대로 구분해 두고 미제공 포장 규칙을 만들지 않는다.

**채점·확인:** 환경·구현·검증·제출을 구분하고 실제 사양 확인을 필요한 근거로 든다.

</details>

### 짧은 복습 계획

Q01–Q03으로 자신의 OS에 해당하는 자료 흐름을 설명하고 Q04–Q05로 요구 범위를 점검하자. P01에서 확인된 상태와 아직 필요한 근거를 분리해 말하자.

## 출처

- [[courses/computer_architecture/lectures/2026-09-29-lecture-05|2026-09-29 강의 노트]]
- [Docker Install.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/Docker.Install.pdf) — [p.1](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-001), [p.2](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-002), [p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-003), [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-004), [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-005), [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-006), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-007)
- [Lab 0 1.pdf](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/Lab.0.1.pdf) — [p.2](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-002), [p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-003), [p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-004), [p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-005), [p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-006), [p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-007), [p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-008), [p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-009), [p.10](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-010)
- [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 보정 STT]] — 56:40, 57:31, 58:36, 59:36, 01:00:30 (페이지 안의 시간 표기)

9월 29일은 Docker·VSCode/CLI 선택과 Lab 안내를 확인한다. OS별 상세 설치는 자료 기반이며 현재 제품 UI·설치 상태·실행 성공을 새로 확인한 것이 아니다. `assignment-0.md`, `first-hardware.md`, `assignment-1.md`, starter archive·tests는 제공되지 않았다. 따라서 정확한 TODO·control encoding·완성 wiring·구현을 추정하지 않는다. 당시 deadline은 자료 시점의 안내이며 worksheet 의무와 code-only archive의 구체 포장 관계는 미제공이다.

시험 연결은 2025-2 복기본에 한정되며 공식 원문·정답은 독립 확인되지 않았다. 제공 답안은 검증된 정답으로 채택하지 않았고 과거 채점 규칙·출제 가능성을 현 학기로 옮기지 않는다.
