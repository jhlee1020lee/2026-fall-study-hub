---
title: "Docker 실습 환경과 CPU 과제 사양 읽기"
description: "Docker 실습 환경의 확인 범위와 CPU 과제의 명령·port·bit width 사양을 구별하는 문제와 해설입니다."
course: "computer_architecture"
unit_id: "lab-environment-specification"
lang: "ko"
note_layout: "textbook_unit_v1"
reader_layout: "content_first"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook", "plain-document"]
source_assets: ["Docker Install.pdf", "Lab 0 1.pdf", "lab2-slides.pdf"]
private_source_assets: ["lab2-slides.pdf"]
source_lectures: ["courses/computer_architecture/lectures/2026-09-29-lecture-05"]
---

## Docker container와 실습 프로젝트의 역할

CPU를 설계하는 실습에서도 먼저 “어떤 파일을 어느 실행 환경에서 다루는가”를 분리해야 한다. **Docker container(컨테이너)**는 실습 도구가 실행되는 환경이고, **dinocpu 프로젝트**는 그 안에서 다룰 설계 파일의 묶음이다. **VSCode Dev Containers**는 편집기에서 그 container에 연결하여 작업하도록 돕는다. Folder를 여는 것, container를 준비하고 연결하는 것, CPU를 구현하는 것은 서로 다른 단계다.

[[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 강의 (computer_architecture:NT001)]] 56:40–58:36에서는 lab을 Docker container에서 수행하고 VSCode 경로를 권장하며, Docker에 익숙하면 CLI를 사용할 수 있다고 설명한다. 관련 준비와 single-cycle 설명은 [[courses/computer_architecture/lectures/2026-09-29-lecture-05|2026-09-29 Computer Architecture 강의 노트]]와 연결된다. 다음의 구체적인 환경 순서는 제공된 설치·Lab0 자료를 읽는 설명이며, 현재 제품의 설치 절차나 설치 성공을 인증하는 안내가 아니다.

자료의 흐름은 Docker 설치, 배포 archive 해제, 생성된 `dinocpu/` folder 열기, container 연결이다. Archive 해제 예는 다음과 같다. [computer_architecture:NM004 p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-004).

```sh
tar -xzf dinocpu-lab1.tar.gz
```

이 명령은 project files를 꺼내는 단계다. 그 자체로 Docker를 설치하거나 CPU를 실행하지 않는다. `dinocpu/`를 VSCode로 연 다음 [computer_architecture:NM004 p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-005)의 화면 오른쪽 아래에 보이는 **Reopen in Container**를 선택하는 것이 다음 단계다. 자료는 이 동작으로 VSCode가 container를 build하고 연결한다고 설명한다. 따라서 편집기에 파일이 보이는 것만으로 container 연결까지 끝났다고 판단하면 안 된다.

CLI 경로의 세부 안내는 `assignment-0.md`를 보도록 되어 있다. Lab0는 환경 준비와 lab에서 사용할 **Chisel**의 입문을 담당하며, `first-hardware.md` tutorial은 Chisel이 낯설 때 사용할 선택 준비다. Lab0 tutorial에는 제출 요구가 없다. 이는 뒤의 CPU 구현 과제가 선택이라는 뜻은 아니다. [computer_architecture:NM004 p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-006). 해당 두 문서의 본문은 여기의 근거에 포함되지 않으므로 build/test 명령이나 Chisel 문법을 파일 이름만으로 추정할 수는 없다.

## 운영체제별 설치 경로와 확인 동작

### Windows에서 WSL을 거쳐 Ubuntu로

설치 자료의 Windows 경로는 **WSL(Windows Subsystem for Linux)**을 활성화하여 Linux 환경으로 들어가는 순서다. Windows 기능에서 Windows Subsystem for Linux를 켜고 재부팅한 뒤 administrator PowerShell에서 다음 두 명령을 사용하도록 되어 있다. 첫 명령의 설치 단계와 둘째 명령의 기본 WSL version 설정을 구분한다. [computer_architecture:NM003 p.2](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-002).

```powershell
wsl --install
wsl --set-default-version 2
```

이후 VSCode의 Dev Containers extension 설정에서 **Dev › Containers: Execute In WSL**을 켜고, PowerShell의 `wsl`로 Ubuntu shell에 들어가 뒤의 Ubuntu 절차를 계속한다. [computer_architecture:NM003 p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-003). PowerShell과 Ubuntu shell은 같은 문맥이 아니므로 화면에 terminal이 보인다는 것만으로 명령을 실행할 위치가 정해지는 것은 아니다.

### Ubuntu의 Engine 설치와 group 변경

Ubuntu 자료에는 Docker Engine 설치와 현재 사용자를 docker group에 추가하는 다음 예가 실려 있다. [computer_architecture:NM003 p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-004).

```sh
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
```

첫 줄은 script를 받아 `sudo sh`에 전달하는 설치 동작이다. 둘째 줄은 현재 사용자의 group membership을 바꾸는 동작이므로 설치와 같은 일을 반복하는 줄이 아니다. 자료는 WSL에서 script warning과 약 20초의 대기가 나타날 수 있다고 설명한다. 이어 shell을 닫고 다시 열어 변경된 환경을 사용하고, WSL 경로라면 다시 `wsl`로 들어가는 순서를 제시한다.

설치 후 확인 예는 다음과 같다.

```sh
docker run hello-world
```

이 확인은 예제 container를 실행하는 동작이다. Version 문자열을 표시하는 것보다 다른 단계의 기능을 확인하지만, dinocpu가 build되거나 과제의 모든 test를 통과했다는 뜻은 아니다.

### Mac의 두 대안과 version 출력

Mac 자료의 첫 경로는 Apple chip 또는 Intel chip에 맞는 Docker Desktop을 선택하고, `.dmg`에서 `Docker.app`을 Applications로 이동한 뒤 app을 실행하는 방식이다. Menu bar의 Docker icon을 확인하고 아래 명령으로 version 출력을 확인하도록 되어 있다. [computer_architecture:NM003 p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-005); [computer_architecture:NM003 p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-006).

```sh
docker --version
```

두 번째 경로는 Homebrew를 이용한 대안이다. 두 경로를 모두 이어 수행하라는 의미가 아니다.

```sh
brew install --cask docker
```

이 경우에도 app 실행과 icon/version 확인이 뒤따른다. 자료의 `Docker version 28.0.1, build xxxxxxx`는 출력 형식의 예이며 필수 또는 최신 version 지정이 아니다. p.7의 `docker —version`은 em dash를 사용하고, p.6의 `docker --version`은 두 hyphen을 사용한다. 위 code는 p.6의 표기를 따른 것이다. 비슷해 보이는 문자도 command-line option에서는 같은 byte가 아니라는 점을 확인해야 한다. [computer_architecture:NM003 p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-007).

OS별 경로를 나누어 읽으면 확인 결과의 의미도 분명해진다. Version 확인은 version 정보를, `hello-world`는 그 예제 실행을, Reopen in Container는 프로젝트 container의 build·연결을 각각 다룬다. 어느 하나의 결과를 CPU 구현의 정확성이나 전체 test 성공으로 확대하지 않는다.

## Lab1의 instruction 범위와 control 계약

### Instruction format과 구현할 instruction 집합

초기의 R-type 중심 소개보다 구체적인 Lab1 안내는 **R-type과 I-type arithmetic·logic instruction**을 대상으로 한다. [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 강의 (computer_architecture:NT001)]] 58:36과 [computer_architecture:NM004 p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-008)을 함께 읽으면, I-type이라는 형식 이름이 같은 모든 instruction을 구현하라는 뜻이 아님을 알 수 있다. 예를 들어 load의 format이 I-type이라는 사실만으로 Lab1의 arithmetic·logic 범위에 load 전체가 들어오지는 않는다.

**Contract(구현 계약)**는 지원할 instruction, module interface, control 의미처럼 구현이 따라야 할 구체적인 약속이다. 자료는 일부 control signal 정의가 수업과 다르므로 `assignment-1.md`를 따르라고 한다. 강의 59:36도 이 사양에 맞춘 구현을 강조한다. 수업에서 어떤 select 값이 0이었다는 기억만으로 과제에서도 같은 encoding을 사용하면 안 된다. 이 차이는 ISA의 연산 의미와 과제 datapath의 control 표현을 구분하게 한다.

### 빈 worksheet에서 읽어야 할 정보

[computer_architecture:NM004 p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-009)는 완성 datapath가 아니라 필요한 연결을 그려 넣을 worksheet다. PC, Next PC, Control Unit, ALU Control, Instruction Memory, Register File, ALU, Immediate Generator가 분리되어 있고 주어진 `select 32 bits` block도 있다. 그림을 읽을 때는 같은 이름의 선을 무조건 잇기보다 각 port가 **번호, 값, 동작 선택 중 무엇을 뜻하는지**부터 구분한다.

| Port 또는 module | 읽어야 할 의미 |
|---|---|
| `readreg1`, `readreg2`, `writereg` | 읽거나 쓸 register를 고르는 index |
| `readdata1`, `readdata2`, `writedata` | Register 사이를 이동하는 값 |
| `wen` | Register write를 허용하는 control |
| ALU의 `inputx`, `inputy`, `operation`, `result` | Operand, 연산 선택, 결과의 구분 |
| Immediate Generator의 `instruction→sextImm` | Instruction의 immediate를 해석한 결과 |
| Next PC | 현재 PC와 instruction의 control-flow 정보로 다음 주소를 결정 |

Control Unit에는 `itype`, `aluop`, `src1`, `src2`, `branch`, `jumptype`, `resultselect`, `memop`, `toreg`, `regwrite`, `validinst`, `wordinst` 같은 출력 이름이 있다. ALU Control은 `aluop`, `itype`, `funct7`, `funct3`, `wordinst`를 받아 `operation`을 내보낸다. Next PC에는 `pc`, `imm`, `inputx`, `inputy`, `funct3`, `branch`, `jumptype`가 표시되어 있다. 이 이름들은 어떤 의미를 확인해야 하는지 알려 주지만 control의 bit encoding이나 truth table 자체는 아니다.

### Bit width와 값의 의미를 함께 표시하기

Worksheet는 필요한 wire와 mux를 그리고 wire마다 bit width를 쓰도록 한다. 일부 bits만 전달한다면 bit slice도 적어야 한다. 예를 들어 `instruction[19:15]`는 양 끝을 포함하므로 19−15+1=5 bits다. 5-bit index는 2^5=32개의 register 번호를 표현한다. 이것은 32-bit instruction word 전체도, RV64 datapath에서 register가 담는 64-bit 값 전체도 아니다.

가령 두 port가 모두 register와 관련되었다고 해도 register 번호 5 bits를 전달하는 선과 register data를 전달하는 선은 의미와 폭이 다르다. 폭이 다르면 잘라낼지, 확장할지, 무엇을 선택할지 사양을 확인해야지 32와 64를 임의로 맞추어 연결할 수 없다. 반대로 폭이 같아도 address와 arithmetic operand가 같은 역할은 아니다.

그림에 보이는 모든 module과 port를 반드시 사용할 필요는 없다는 문구도 중요하다. 과제의 지원 instruction에 필요한 연결을 정하는 것이지, 빈 port를 모두 채우는 퍼즐이 아니다. `assignment-1.md`와 starter code·tests의 실제 내용은 제공되지 않았으므로 이 worksheet만으로 정확한 control encoding, 완성 연결, Chisel 구현을 결정하지 않는다.

## Lab2의 data memory·control flow와 사양 읽기

### 연산 결과 이외의 architectural effect

Lab2 소개는 Lab1의 single-cycle CPU를 확장하여 loads, stores, branches, `lui`, `auipc`, `jal`, `jalr`를 포함한 RV64I integer instructions를 다루도록 한다. [[courses/computer_architecture/transcripts/undated-control-hazards-tskkzbwcgg2lavgo|날짜 미확인 강의 (computer_architecture:NT002)]] 42:57의 소개와 computer_architecture:NM008 p.2의 자료를 함께 읽되, 다음 설명은 instruction의 일반 개념과 사양을 읽는 방법에 한정한다.

이 날짜 미확인 전사는 원음 검증 없이 자료와 대조한 텍스트이며 완전한 축어 복원이 아니다. 빠진 발화, 실제 수업 날짜와 화자 신원은 복원되지 않았다.

Arithmetic·logic instruction은 operand로 result를 만들어 register에 쓰는 경로가 중심이었다. Load는 **어느 address를 읽는가**와 **읽은 data를 어디에 쓰는가**를 구분해야 한다. Store는 **어느 address인가**, **어떤 data인가**, **write가 허용되는가**를 함께 본다. Conditional branch는 비교 condition과 target을 바탕으로 next PC를 선택한다. `lui`는 upper-immediate 값 형성, `auipc`는 PC-relative 값 형성, `jal`·`jalr`는 control transfer와 link 값이라는 서로 다른 효과를 읽어야 한다. 같은 ALU나 mux를 쓴다는 사실만으로 이 architectural effect가 같아지지는 않는다.

자료에서 Lab1 R/I solution이 template에 포함된다고 안내하는 것은 제공 계획에 관한 사실이다. 그것이 실제 code를 검토했다거나 모든 연결이 맞다고 확인한 결과는 아니다. Lab2 역시 수업과 다른 control 정의가 있을 수 있어 `assignment-2.md`의 계약을 먼저 읽어야 한다. 날짜 미확인 강의 43:54의 문서 설명은 이 필요성과 연결된다.

### Data Memory port의 의미와 연결 문제의 경계

비공개 실습 자료 computer_architecture:NM008 p.3의 빈 worksheet에는 Data Memory가 추가되어 있으며 `address`, `writedata`, `valid`, `memread`, `memwrite`, `maskmode`, `sext`, `readdata`라는 port가 표시되어 있다. 원본 도면이나 연결 답안을 대신 제시하지 않고, 이 이름으로 확인할 질문을 구분해 보자.

`address`는 접근 위치이고 `writedata`는 쓸 값이다. `readdata`는 읽어서 돌아오는 값이다. `valid`와 read/write 관련 신호는 그 접근이 유효한지와 어떤 동작을 요구하는지 구분하게 한다. `maskmode`와 `sext`는 접근 폭·확장 방식을 확인해야 할 지점이지만, 이름만으로 정확한 encoding이나 폭별 표를 정할 수는 없다. Memory 동작을 요청하는 control과 그때 이동할 data가 같은 instruction에 대응하는지 확인하는 것이 기본이다.

Worksheet는 data wire뿐 아니라 필요한 control wire, mux, 각 선의 width, 일부 bits의 slice도 표시하도록 한다. 앞의 `instruction[19:15]` 5-bit 계산은 여기에도 적용되며, instruction word 32 bits와 register data 64 bits를 계속 구분해야 한다. 날짜 미확인 강의 computer_architecture:NT002 44:10의 width 설명은 이 요구와 연결된다. 45:07의 “full/four”처럼 불확실한 발화를 제출 규칙의 정확한 문장으로 바꾸어 읽지는 않는다.

자료는 Parts I–IX를 순서대로 진행하고 part별 test를 사용하도록 안내하며, worksheet와 네 code file을 제출 대상으로 적는다. 이는 작업을 작은 계약 단위로 나누어 확인하라는 안내다. `assignment-2.md`, template, tests 자체가 없으면 각 part의 내용, 허용 I/O 변경, test command나 통과 조건을 재구성할 수 없다. 실제 사양에서 instruction 범위, control 정의, interface 폭과 제출 대상을 각각 확인해야 하며, 강의 그림만으로 전체 wiring이나 구현 정답을 대신 만들 수는 없다.

## 확인·연습문제

### 복습 순서

Q01–Q03 뒤 P01에서 각 관찰이 입증하는 사실을 한 줄씩 적으세요. Q04–Q07에서는 명령 효과와 port 역할을 구분하고 5/32/64-bit를 검산한 뒤, P02의 잘못된 사양 읽기를 고쳐 보세요.

### 실습 환경과 확인의 범위

#### 확인 Q01 · 파일·환경·학습 준비

Docker container, dinocpu, VSCode Dev Containers, Lab0/Chisel tutorial의 역할을 구분하라. Archive 해제부터 container 연결까지 자료의 순서를 쓰고, tutorial이 선택이라는 말이 Lab1도 선택이라는 뜻인지 판단하라.

<details><summary>해설 보기</summary>

Container는 도구의 실행 환경, dinocpu는 설계 파일 묶음, Dev Containers는 편집기에서 그 환경으로 연결하는 수단이다. 자료는 Docker 준비→`tar -xzf dinocpu-lab1.tar.gz`로 압축 해제→`dinocpu/` 열기→Reopen in Container로 build·연결 순서를 제시한다. 압축 해제나 folder 열기만으로 container 연결·CPU 실행이 된 것은 아니다. Lab0는 환경과 Chisel 입문이며 `first-hardware.md` tutorial은 선택 준비이고 Lab0 제출은 없다. 이를 CPU 구현 과제의 선택 여부로 확대할 수 없다. CLI 세부는 `assignment-0.md`에 위임되지만 해당 본문이 없어 build/test 명령을 추정하지 않는다.

확인 기준: 세 도구/파일 역할, 단계 순서, 선택 tutorial과 구현 과제의 차이를 확인한다.

근거: [Lab0·Lab1 p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-004) · [Lab0·Lab1 p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-005) · [Lab0·Lab1 p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-006)

</details>

#### 확인 Q02 · Windows에서 Ubuntu까지 읽기

자료의 Windows→WSL→Ubuntu 흐름을 shell 문맥과 함께 설명하라. `wsl --install`, `wsl --set-default-version 2`, Docker 설치 script, group 변경, shell 재시작, `hello-world`는 각각 무엇을 하는가? 명령을 실행할 필요는 없다.

<details><summary>해설 보기</summary>

Windows 기능의 WSL 활성화와 재부팅 뒤 administrator PowerShell에서 `wsl --install`은 설치, `wsl --set-default-version 2`는 기본 WSL version 설정이다. Dev Containers의 Execute In WSL 설정을 켜고 PowerShell에서 `wsl`로 Ubuntu shell에 들어간 뒤 Ubuntu 절차를 따른다. `curl -fsSL https://get.docker.com | sudo sh`는 받아온 설치 script를 실행하는 자료 예이고, `sudo usermod -aG docker $USER`는 현재 사용자의 group membership 변경이다. 자료의 약 20초 WSL warning 대기는 설명된 현상이지 CPU test가 아니다. Shell을 닫고 다시 열며 WSL이면 다시 `wsl`로 들어간다. `docker run hello-world`는 예제 container 실행을 확인할 뿐 dinocpu build나 과제 통과를 증명하지 않는다.

확인 기준: PowerShell/Ubuntu 구분과 설치·설정·group·예제 실행의 서로 다른 역할을 확인한다.

근거: [Docker Install p.1](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-001) · [Docker Install p.2](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-002) · [Docker Install p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-003) · [Docker Install p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-004)

</details>

#### 확인 Q03 · Mac 대안과 확인의 범위

Mac의 두 설치 경로를 구분하고 설치 뒤 무엇을 확인하는지 설명하라. `Docker version 28.0.1`과 `docker —version`/`docker --version`을 어떻게 읽어야 하는가? Version 출력, `hello-world`, Reopen in Container가 각각 무엇을 입증하지 못하는가?

<details><summary>해설 보기</summary>

첫 경로는 chip에 맞는 Docker Desktop 선택→`.dmg`의 `Docker.app`을 Applications로 이동→app 실행→menu bar icon과 version 확인이다. 두 번째는 `brew install --cask docker`라는 대안 뒤 같은 app 실행·확인을 한다. 두 경로를 모두 순서대로 할 필요가 있다는 뜻은 아니다. 28.0.1은 출력 예이며 필수·최신 지정이 아니다. p.7의 em dash `—`와 p.6의 두 hyphen `--`는 다른 문자이고 code는 p.6의 `docker --version`을 따른다. Version은 표시 정보, `hello-world`는 예제 실행, Reopen in Container는 프로젝트 container build·연결 단계다. 어느 하나만으로 CPU 구현이나 전체 test 정확성을 인증할 수 없다.

확인 기준: 대안 관계, app 실행 뒤 확인, version 예시와 dash 차이, 성공 범위의 한계를 확인한다.

근거: [Docker Install p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-005) · [Docker Install p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-006) · [Docker Install p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-007)

</details>

### 과제 범위와 사양 읽기

#### 확인 Q04 · Format과 구현 범위

Lab1을 I-type 구현 과제라고만 기억하면 왜 load까지 잘못 포함할 수 있는가? 강의 mux select 값과 과제 문서가 다를 때 어느 쪽을 따라야 하며 그 이유는 무엇인가?

<details><summary>해설 보기</summary>

상세 Lab1 소개는 R-type과 I-type 중 arithmetic/logic instructions를 대상으로 한다. I-type은 encoding 형식이고 모든 I-type instruction이 arithmetic/logic은 아니므로 load를 format 이름만으로 추가할 수 없다. 구현은 `assignment-1.md`의 control 정의를 따라야 한다. ISA의 연산 의미와 특정 datapath의 select encoding은 서로 다른 계약이므로 강의에서 0이었다는 이유만으로 과제도 0이라고 정할 수 없다. 해당 문서·starter·tests가 없으므로 지금 정확한 truth table이나 완성 code를 만들 근거는 없다.

확인 기준: R/I arithmetic·logic 범위와 format의 차이, assignment-specific control 우선 이유를 확인한다.

근거: [Lab0·Lab1 p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-008)

</details>

#### 확인 Q05 · Port의 의미와 bit width

Blank worksheet의 `readreg1`/`writereg`, `readdata1`/`writedata`, `wen`, ALU `operation`, `instruction→sextImm`를 분류하라. `instruction[19:15]` 폭과 표현 가능한 register 수를 구하고 instruction word·RV64 data 폭과 비교하라. Control Unit·ALU Control·Next PC의 이름만으로 모든 배선을 정할 수 있는가?

<details><summary>해설 보기</summary>

`readreg1`·`writereg`는 index, `readdata1`·`writedata`는 data, `wen`은 write enable, `operation`은 ALU 동작 선택이다. Immediate Generator는 instruction에서 immediate를 해석해 `sextImm`을 낸다. Slice는 19−15+1=5 bits이고 2^5=32개 register를 고른다. 32-bit instruction word나 64-bit register data와 다르다. Control Unit은 `itype`, `aluop`, `src1`, `src2`, `branch`, `jumptype`, `resultselect`, `memop`, `toreg`, `regwrite`, `validinst`, `wordinst` 등을 내며, ALU Control은 `aluop`, `itype`, `funct7`, `funct3`, `wordinst`로 `operation`을 결정한다. Next PC의 `pc`, `imm`, `inputx`, `inputy`, `funct3`, `branch`, `jumptype`도 역할 확인의 단서다. 이름은 encoding 표가 아니므로 필요한 wire·mux·width·slice를 사양에 따라 정한다. 주어진 `select 32 bits` block을 임의의 64-bit data선으로 보지 않으며 모든 port를 채울 의무도 없다. 같은 폭이어도 address와 operand의 의미는 다르다.

확인 기준: 5/32/64의 층위를 구별하고 index·data·enable·선택의 의미, 명시해야 할 width/slice와 사양 경계를 확인한다.

근거: [Lab0·Lab1 p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-009)

</details>

#### 확인 Q06 · Lab2의 architectural effect

Lab2 소개의 새 instruction 종류를 열거하고 load·store·branch·`lui`·`auipc`·`jal`·`jalr`가 구별해야 하는 효과를 설명하라. Template에 Lab1 solution이 있다는 안내를 어떻게 해석해야 하는가?

<details><summary>해설 보기</summary>

소개는 Lab1 CPU를 loads, stores, branches, `lui`, `auipc`, `jal`, `jalr`를 포함한 RV64I integer instruction으로 확장한다. Load는 읽을 address와 반환 data의 destination, store는 address·쓸 data·write 허용을 구분한다. Branch는 condition과 target으로 next PC를 고른다. `lui`는 upper-immediate, `auipc`는 PC-relative 값을 형성하며 `jal`·`jalr`는 control transfer와 link를 만든다. 같은 ALU를 쓴다고 효과가 같지는 않다. Template의 Lab1 R/I solution 포함은 제공 계획이며 실제 code의 확인·정확성 판정은 아니다. Control 정의는 `assignment-2.md`를 따라야 하지만 그 본문·template·tests는 이 자료에 없어 전체 구현을 정할 수 없다.

확인 기준: 모든 instruction 종류와 효과 차이, 제공 계획과 실제 검증의 차이를 확인한다.

근거: computer_architecture:NM008 p.2

</details>

#### 확인 Q07 · Memory port와 미제공 사양

Data Memory의 `address`, `writedata`, `readdata`, `valid`, `memread`, `memwrite`, `maskmode`, `sext`에서 무엇을 구별해야 하는가? Worksheet 표시, Parts I–IX·test·제출 안내가 알려 주는 것과 알려 주지 않는 것도 설명하라.

<details><summary>해설 보기</summary>

`address`는 위치, `writedata`는 쓸 값, `readdata`는 돌아오는 값이다. `valid`와 read/write 신호는 접근 유효성과 동작을 구별하며 `maskmode`·`sext`는 접근 폭과 확장 의미를 사양에서 확인할 지점이다. 이름만으로 bit encoding을 정할 수 없다. Data와 control은 같은 instruction의 효과에 대응해야 하고 필요한 data/control wire·mux, 각 width, 일부 bit의 slice를 표시한다. 5-bit index·32-bit instruction·64-bit data를 계속 구분한다. Parts I–IX를 순서대로 하고 part별 test를 쓰라는 안내와 네 code file+worksheet라는 제출 범주는 주어졌지만 각 part의 구현, test command·통과 조건, 허용 I/O 변경은 제공되지 않은 문서를 추정해 채우지 않는다. 날짜 미확인 45:07의 full/four 표현도 자료로 정확한 발화가 되지는 않는다.

확인 기준: 위치·값·제어, width/slice, 순차 작업 안내와 실제 구현 계약의 경계를 확인한다.

근거: computer_architecture:NM008 p.2 · computer_architecture:NM008 p.3 · computer_architecture:NM008 p.4

</details>

### 새로 쓴 일반 연습

#### 연습 P01 · 확인 결과를 과장하지 않기

새로 쓴 강의·자료 기반 일반 연습이다. 전체 기출 후보에는 Docker·Dev Containers 준비 상태를 판별하는 직접 대응 문항이 없다. 선수 개념은 Q01–Q03이다.

한 학생이 (1) version 문자열을 확인하고, (2) `hello-world` 실행 결과를 보고, (3) 압축 해제한 folder를 편집기에 연 뒤 “CPU 과제 test까지 끝났다”고 썼다. 각 관찰로 말할 수 있는 범위와 아직 확인해야 할 단계를 구분하라. 새 설치 명령이나 test 명령을 만들지는 말라.

<details><summary>해설 보기</summary>

(1)은 version 정보의 관찰이고 (2)는 예제 container 실행의 관찰이다. (3)은 project files를 연 상태다. 세 결과 어디에도 Reopen in Container를 통한 해당 project 환경 연결, dinocpu build, 과제 test의 결과는 없다. 자료의 container 연결 단계를 별도로 확인하고 실제 과제 문서에서 build/test 절차와 결과 기준을 확인해야 한다. 그 문서가 없으므로 지금 명령을 추측하거나 통과라고 쓸 수 없다.

확인 기준: 관찰별 근거를 대응시키고 container 연결·project build·과제 통과를 서로 구분한다.

근거: [Docker Install p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-004) · [Docker Install p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-006) · [Lab0·Lab1 p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-005)

</details>

#### 연습 P02 · 설계 메모의 세 오류

새로 쓴 자료 기반 일반 연습이다. 전체 복기 후보에는 해당 Lab worksheet의 사양 읽기를 직접 평가하는 문항이 없어 기출 변형으로 부르지 않는다. 선수 개념은 Q04–Q07이다.

메모에 “모든 I-type은 Lab1 범위다. `instruction[19:15]`는 register와 관련되므로 64 bits다. Lab2의 `maskmode`는 이름이 있으니 encoding을 임의로 정해도 된다”라고 적혔다. 각각을 바로잡고, 완성 wiring을 만들지 않고도 지금 작성할 수 있는 사양 확인 목록을 제시하라.

<details><summary>해설 보기</summary>

첫째, Lab1은 R/I arithmetic·logic으로 한정되므로 format만으로 loads를 포함하지 않는다. 둘째, inclusive slice는 19−15+1=5 bits인 register index이며 64-bit register data와 다르다. 셋째, `maskmode`는 폭 관련 정의를 확인할 이름일 뿐 encoding은 `assignment-2.md`의 계약에 따른다. 지금 적을 목록은 지원 instruction의 효과, 각 port의 index/data/control 역할, 필요한 wire·mux의 폭과 slice, control 정의의 근거, 제공된 part/test·제출 안내와 실제 사양에서 더 확인할 사항이다. 미제공 truth table, TODO와 전체 연결은 채우지 않는다.

확인 기준: 세 오류를 각각 이유와 함께 고치고, 확인 질문과 구현 정답을 구분한다.

근거: [Lab0·Lab1 p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-008) · [Lab0·Lab1 p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-009) · computer_architecture:NM008 p.2 · computer_architecture:NM008 p.3

</details>

## 출처

### 강의와 자료

[[courses/computer_architecture/lectures/2026-09-29-lecture-05|2026-09-29 · Microcode·자원 공유·실습 안내]]

- [[courses/computer_architecture/transcripts/2026-09-29|2026-09-29 (computer_architecture:NT001)]] 56:40, 57:31, 58:36, 59:36 — 당시 강의 전사.

- [[courses/computer_architecture/transcripts/undated-control-hazards-tskkzbwcgg2lavgo|날짜 미확인 강의 (computer_architecture:NT002)]] 42:57, 43:54, 44:10, 45:07 — 강의 날짜 미확인. 불확실한 발화는 자료 설명과 구분합니다. TXT 전사를 자료와 대조했으며 원음은 검증되지 않았습니다. 완전한 축어록이 아니며 빠진 발화·실제 수업 날짜·화자 신원은 복원되지 않았습니다.

- [Lab0·Lab1 원문](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/Lab.0.1.pdf): [Lab0·Lab1 p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-004), [Lab0·Lab1 p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-005), [Lab0·Lab1 p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-006), [Lab0·Lab1 p.8](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-008), [Lab0·Lab1 p.9](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/lab.0.1/page-009). Lab0·Lab1 소개와 blank worksheet; 상세 과제 문서의 대체물이 아님.

- [Docker Install 원문](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/Docker.Install.pdf): [Docker Install p.1](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-001), [Docker Install p.2](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-002), [Docker Install p.3](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-003), [Docker Install p.4](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-004), [Docker Install p.5](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-005), [Docker Install p.6](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-006), [Docker Install p.7](https://jhlee1020lee.github.io/2026-fall-study-hub/page_cache/computer_architecture/docker.install/page-007). 자료에 제시된 설치 예; 현재 제품·실행 상태 검증이 아님.

- Lab2 소개 자료 pp.2–4: 비공개 자료로 공개 원문·페이지 링크가 없습니다. 소개된 범위와 port 의미만 사용하며 실제 assignment2·template·tests는 제공되지 않았습니다.

전체 복기 후보에는 Docker/WSL/container 확인이나 해당 Lab1·Lab2 worksheet 사양 읽기에 직접 대응하는 문항이 없습니다. 관련 CPU 설계 문항을 이 실습의 실제 시험 근거로 옮기지 않고 P01–P02를 일반 연습으로 두었습니다.


---

[[courses/computer_architecture/units/microcode-resource-reuse|← 이전: Microcode·자원 공유·Pipelining과 Hazard]] · [[courses/computer_architecture/units/index|단원 목차]]
