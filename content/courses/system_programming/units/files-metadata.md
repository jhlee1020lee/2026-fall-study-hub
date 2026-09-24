---
title: "Unix file·directory·inode와 metadata"
description: "File type, link와 mount, stat·directory API의 의미를 연결한다."
course: "system_programming"
unit_id: "files-metadata"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["03.IO.Unix.Filesystem.Concepts.pptx", "04.IO.Direct.and.Buffered.IO_8e725857.pptx", "05.IO.Files.and.Directories_3d312c60.pptx"]
private_source_assets: []
source_lectures: ["courses/system_programming/lectures/2026-09-09-lecture-03", "courses/system_programming/lectures/2026-09-14-lecture-04", "courses/system_programming/lectures/2026-09-16-materials-io-review", "courses/system_programming/lectures/2026-09-21-lecture-05"]
---

File을 byte·이름·inode·열린 handle로 나누어 생각한다. Metadata를 읽을 때 path 해석과 관측값의 단위를 먼저 확인한다.

## Unix file(파일): 내용·이름·metadata를 나누어 보기

Regular file(일반 파일)은 `B0, B1, …, Bm-1`이라는 m-byte sequence로 모델링한다. Alphabet `a`부터 `z`까지 저장한 예에서는 offset(파일 안의 위치) 0에 `a`, 25에 `z`가 있다. 같은 bytes를 text, image, object code로 해석하는 것은 application의 역할이다. “Text file인가”와 “regular file인가”는 서로 다른 분류다. [Unix filesystem slides 4–7](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)

Directory(디렉터리)는 이름과 i-number(inode 번호)를 연결하는 entry를 담는다. Inode(index node)는 권한·소유자·시간·크기 등의 metadata(데이터에 관한 정보)를 나타낸다. 따라서 이름이 inode 안에 반드시 하나만 들어 있다는 모델로는 같은 파일의 여러 이름을 설명할 수 없다. `struct stat` 같은 C 구조체로 metadata를 받으려면 [[courses/system_programming/units/objects-pointers|object와 pointer]]의 구분도 필요하다.

### 같은 file interface가 가리키는 서로 다른 대상

Unix의 file interface는 저장 파일 외에도 여러 대상에 적용된다.

| 대상 | 자료의 예 | 읽을 때 구분할 점 |
|---|---|---|
| Regular file | text·image·object file | byte format은 application이 해석 |
| Directory | 이름과 inode의 연결 | 내용 bytes를 읽는 것과 entry를 열거하는 것은 다른 작업 |
| Character device(문자 장치) | `/dev/tty`, `/dev/input/mice` | stream 형태 상호작용의 대표 예 |
| Block device(블록 장치) | `/dev/sda` | block 단위 저장장치 접근의 대표 예 |
| Virtual filesystem(가상 파일시스템) | `/proc`, `/sys` | kernel 상태·설정을 file처럼 표현 |
| IPC endpoint(프로세스 간 통신 끝점) | FIFO, socket | process 사이의 데이터 전달 |

이름이 있다고 모두 disk에 저장된 regular file은 아니다. `/proc`의 내용은 kernel 상태를 반영할 수 있다. Character device의 “stream”, block device의 “block”은 유용한 비교지만 모든 character device에서 seek나 buffering이 절대 불가능하다는 규칙은 아니다. I-number 역시 disk의 물리 주소를 단순 산술로 계산하는 숫자와 동일하지 않다.

## Process isolation과 FIFO·socket

서로 다른 process는 각자의 address space(주소 공간)에서 실행된다. 자기 pointer의 숫자를 다른 process의 private memory를 직접 읽는 통신 수단으로 사용할 수 없다. [[courses/system_programming/transcripts/2026-09-09|2026-09-09 STT 49:54–55:05]]은 이 격리를 IPC(Inter-Process Communication, 프로세스 간 통신)가 필요한 이유로 설명한다.

FIFO(named pipe, 이름 있는 파이프)는 한쪽이 쓴 데이터를 다른 쪽이 같은 순서로 읽는 단방향 channel이다. Directory에 이름이 있어도 전달 데이터가 regular file처럼 disk에 누적된다는 뜻은 아니다. 자료의 흐름은 `mkfifo`로 `abc`를 만들고, consumer인 `gzip`이 그 FIFO에서 읽어 `abc.gz`로 압축하며 producer가 문서 내용을 FIFO에 쓰는 것이다. 상대가 열거나 데이터를 보낼 때까지 기다릴 수 있으므로 producer와 consumer의 실행 순서, background 실행 여부가 중요하다. 원문 명령의 `&;` 표기를 완성된 shell script로 그대로 받아들이지는 않는다. [Unix filesystem slide 8](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)

Unix domain socket은 local IPC에 사용하며 양방향 통신을 지원한다. Network socket도 유사한 I/O interface를 제공하지만 Unix domain socket 자체가 원격 network endpoint라는 뜻은 아니다. FIFO나 socket으로 얻은 handle이 file descriptor라고 해서 regular file처럼 임의 위치로 seek할 수 있는 것도 아니다. Private 주소의 숫자와 실제 공유의 차이는 [[courses/system_programming/units/memory-layout|process memory]]에서 다시 구체화된다.

## Mount point(마운트 지점)와 하나의 directory tree

Unix는 `/`라는 한 root 아래에서 경로를 해석한다. 다른 filesystem을 붙일 때에는 directory를 mount point로 삼는다. 원래 directory 안의 내용과 새 filesystem의 내용이 합쳐지는 것이 아니라 새 연결이 기존 내용을 가린다.

자료의 예에서는 먼저 `extern/hello`를 만든다. `extern`에 tmpfs를 mount하면 원래 `hello`가 보이지 않고 새 filesystem의 내용이 보인다. 그곳에 `extern`이라는 파일을 만든 뒤 unmount하면 원래 `hello`가 다시 나타난다. **가려진 것과 삭제된 것은 다르다.** 별도의 host 공유 filesystem인 vboxsf 연결과 tmpfs 연결도 서로 다르다. 이 예를 `/dev/shm` directory의 bind mount라고 임의 재해석하지 않는다. [Unix filesystem slides 11–13](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)

`echo hello`는 보통 끝의 newline까지 써서 이 예에서 6 bytes이고, `printf hello`의 출력은 5 bytes다. File 크기를 계산할 때 눈에 보이는 글자만 세면 newline을 놓친다.

### Temporary file과 mount option

[[courses/system_programming/transcripts/2026-09-14|2026-09-14 STT 06:55]]은 여러 process가 `/tmp` 같은 공통 namespace에 같은 이름을 만들면 충돌할 수 있다고 설명한다. 서로 겹치지 않는 이름을 확보하여 사용하는 절차가 필요하다. 해당 발화의 API 이름은 불명확하므로 특정 함수명으로 복원하지 않는다.

[[courses/system_programming/transcripts/2026-09-14|9월 14일 08:32]]의 tmpfs는 memory-backed filesystem이므로 reboot 뒤 내용이 유지되지 않는 volatile(휘발성) 저장의 예다. Mount에 가려진 원래 disk file과 tmpfs 자체의 휘발성은 별개다. 모든 `/tmp`가 tmpfs이거나 모든 `/var/tmp`가 같은 삭제 정책을 쓴다는 뜻도 아니다.

| Mount option | 자료에서 설명하는 역할 |
|---|---|
| `ro` | 쓰기 제한 |
| `noatime` | access-time 갱신 제한 |
| `relatime` | atime과 mtime·ctime 관계 등에 따른 갱신 정책의 요약 |
| `noexec` | 직접 실행 제한 |
| `nosuid` | set-ID 효과 제한 |
| `nodev` | device-file 해석 제한 |
| `size` | filesystem 용량 한도 예 |
| `iocharset` | filename encoding 설정 예 |

File별 permission과 filesystem 전체의 정책은 다른 층이다. 어느 한 option만으로 모든 실행·보안 문제가 해결되지는 않는다.

## Hard link와 symbolic link는 무엇을 공유하는가

Hard link(하드 링크)는 다른 directory entry가 **같은 inode**를 가리키는 것이다. `hello.txt`와 `helloworld.txt`가 hard link이면 한 이름을 통해 내용을 덧붙여도 다른 이름에서 같은 변경을 본다. 내용과 metadata를 따로 복사한 것이 아니기 때문이다. 한 이름을 지우면 link count가 줄고 다른 이름은 계속 같은 inode를 가리킨다.

Symbolic link(심볼릭 링크)는 자체 inode에 target pathname을 저장한다. Target이 없어져도 symlink 자체는 남아 dangling link(끊어진 링크)가 될 수 있다. Hard link는 filesystem 경계를 넘지 못하며 보통 directory에 대한 생성도 제한된다. Symlink는 경로를 통해 다른 filesystem이나 directory를 가리킬 수 있다. [Unix filesystem slides 15–18](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)

따라서 hard-link 수는 같은 inode를 가리키는 이름의 수와 연결되지만 symlink를 하나 만들었다고 target inode의 hard-link 수가 증가하지 않는다. 기출 Q3(a–b)의 핵심도 이름을 세기 전에 어떤 inode로 이어지는 참조인지 밝히는 것이다. [EX:sp_2025_2_midterm_q03 p.7]

### ls 출력과 directory link count

`ls -l`의 첫 문자 `- d l p s c b`는 각각 regular file, directory, symlink, FIFO, socket, character device, block device다. 이어 permission, hard-link 수, owner/group, byte 크기, mtime, 이름을 읽는다. `-a`는 dot으로 시작하는 숨김 이름과 `.`·`..`를 포함하고, `-d`는 directory 내용 대신 directory 자체를 표시한다. 이름을 숨기는 dot은 접근 권한을 만드는 장치가 아니다.

전통적인 directory 모델에서 `sample` 안에 `dir1`과 `dir2`가 있으면 `sample`의 link count는 다음과 같다.

`parent 안의 sample 이름 1 + sample/. 1 + dir1/.. 1 + dir2/.. 1 = 4`

자식 없는 `dir1`과 `dir2`는 각각 parent 안의 자기 이름과 내부 `.`로 2다. `sample/..`는 `sample`의 parent를 가리키므로 `sample` 자신의 count에 더하지 않는다. 이 때문에 자료의 모델에서 `2 + 직접 subdirectory 수`라는 식이 나온다. 모든 filesystem의 보편적 보장은 아니다. [Unix filesystem slides 19–21](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)

## Filesystem Hierarchy Standard: 경로의 역할을 읽기

FHS(Filesystem Hierarchy Standard, 파일시스템 계층 표준)는 경로의 역할을 이해하는 convention이다. 모든 경로를 암기하기보다 실행 파일, 설정, 변화하는 상태가 어디에 모이는지를 찾는 데 쓴다. 아래는 제공 자료의 분류이며 distribution마다 실제 연결과 배치는 다를 수 있다. [Unix filesystem slides 22–27](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)

| 경로 | 역할 |
|---|---|
| `/bin`, `/sbin` | 기본 실행·관리 도구 |
| `/boot` | boot loader와 kernel |
| `/dev` | device interface |
| `/etc` | system-wide configuration |
| `/home`, `/root` | 일반 사용자 home과 관리자 home |
| `/lib`, `/lib64` | 기본 도구의 library |
| `/media`, `/mnt` | mount point |
| `/opt` | 추가 application package |
| `/proc`, `/sys` | process·kernel·device 정보와 설정 |
| `/run` | runtime 상태 |
| `/tmp`, `/var/tmp` | 임시 저장; 보존 정책은 별도 확인 |
| `/usr` | 추가 실행 파일과 공유 자료의 계층 |
| `/var` | 실행 중 달라지는 상태와 data |

`/usr/bin`·`sbin`은 실행 도구, `include`는 C header, `lib`는 library, `libexec`는 보조 executable, `local`은 local 설치, `share`는 공유 data, `src`는 source를 담는 역할이다. `/var` 아래에서는 `cache`, `lib`, `lock`, `log`, `mail`, `run`, `spool`, `tmp`를 각각 cache, 지속 상태, 잠금 정보, log, mailbox, runtime 상태, 대기 작업, 임시 data로 읽는다. 자료의 `/var/db`는 Gentoo 사례다.

`~`는 사용자 home의 약기다. Home의 `.cache`, `.config`, `.local`과 `.mozilla`, `.ssh`, `.vim`은 사용자별 cache·설정·local data 또는 특정 application 설정이다. 예를 들어 header는 `/usr/include`, system log는 `/var/log`, 사용자 SSH 설정은 home의 `.ssh`라는 역할로 찾는다.

## stat metadata: 크기·할당량·시간을 구별하기

Metadata와 상세 I/O는 녹음이 없는 9월 16일에 대한 자료 기반 연결 학습으로도 제공된다. 9월 21일의 복습 발화가 그날의 정확한 slide 진행을 소급 증명하지는 않는다. 아래 field의 의미는 Files and Directories slides 3–7에 따른다.

| Field | 뜻 |
|---|---|
| `st_dev`, `st_ino` | filesystem device와 inode 번호 |
| `st_mode` | file type과 permission bits |
| `st_nlink` | hard-link 수 |
| `st_uid`, `st_gid` | owner의 숫자 user/group ID |
| `st_rdev` | special device 식별 정보 |
| `st_size` | logical file size, bytes |
| `st_blksize` | 선호 I/O block 크기 |
| `st_blocks` | 할당된 512-byte block 수 |

예를 들어 `st_size=8192`, `st_blocks=8`이면 logical 크기는 8192 bytes이고 표시된 할당량은 `8×512=4096` bytes다. `st_blksize`를 이 512와 혼동하면 안 된다. Sparse file(희소 파일)은 중간 hole을 읽을 때 0을 제공하면서 그 범위의 storage를 모두 할당하지 않을 수 있다. 자료의 `st_size/512 > st_blocks`는 이런 차이를 찾는 단서이지 모든 filesystem에서 필요충분한 판정식은 아니다. Seek 뒤 쓰기로 hole을 만드는 과정은 [[courses/system_programming/units/io-streams|I/O 위치 이동]]과 연결된다.

Atime은 access, mtime은 내용 변경, ctime은 inode 상태 변경의 시간이다. **Ctime은 creation time이 아니다.** Slide 5의 `st_mtim` 옆 “last access” comment는 slide 7의 modification 설명과 충돌하므로 여기서는 후자의 의미로 구분한다. `timespec`이 nanosecond를 표현할 수 있어도 실제 clock이 그만큼 정확하다는 뜻은 아니다. [Files and Directories slides 3–7](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/05.IO.Files.and.Directories_3d312c60.pptx)

[[courses/system_programming/transcripts/2026-09-21|2026-09-21 STT 02:32]]은 inode에서 data block을 직접 가리키거나 pointer를 담은 다른 block을 거치는 간접 참조를 보충한다. 이는 내부 배치 설명이지 `stat` field가 그 pointer 배열이라는 뜻은 아니다. Pointer 개수와 block 크기가 주어지지 않았으므로 특정 filesystem의 최대 file size를 계산할 근거도 없다.

## Path 기준과 metadata 조회 대상

Absolute path(절대 경로)는 `/`에서 시작한다. Relative path(상대 경로)는 기준 directory에서 시작하며 꼭 `./`로 시작할 필요는 없다. 자료의 `a/b/c/d`와 `a/b/f` 관계에서 기준이 `a/b`라면 `c/d`는 그 아래 `d`를 뜻한다.

| API | 조회 대상 |
|---|---|
| `stat(path, ...)` | pathname을 따라간 target |
| `lstat(path, ...)` | 마지막 구성요소가 symlink이면 그 link 자체 |
| `fstat(fd, ...)` | 이미 열린 fd의 대상 |
| `fstatat(dirfd, path, ..., flags)` | directory fd에 기준을 둔 상대 경로와 선택한 follow 정책 |
| `statx(...)` | mask 등으로 요청하는 확장 metadata |

`fstatat`의 기준 directory와 symlink follow 여부는 별도 선택이다. `AT_SYMLINK_NOFOLLOW`는 마지막 symlink 자체를 조사하려는 의도를 나타낸다. [[courses/system_programming/transcripts/2026-09-21|2026-09-21 STT 03:59]]은 directory가 이동할 수 있을 때 열린 directory를 기준점으로 삼는 이유를 설명한다. 다만 이것만으로 모든 path race가 제거되지는 않는다. `statx`의 birth time도 filesystem과 지원 여부에 따른다. [Files and Directories slides 8–9](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/05.IO.Files.and.Directories_3d312c60.pptx)

### DIR stream을 통해 entry 열거하기

`opendir`는 `DIR *`를 반환하고 `readdir`는 entry를 하나씩 제공하며 `closedir`는 자원을 닫는다. `dirfd`는 그 DIR에 연결된 fd를 얻는다. DIR object 자체가 fd 정수이거나 stdio의 `FILE`과 같은 type은 아니다. `fdopendir`는 기존 fd를 이용하는 관련 interface이고 `mkdir`·`mkdirat`은 directory 생성에 쓰인다. [[courses/system_programming/transcripts/2026-09-21|2026-09-21 STT 05:42]]

자료의 `statter.c`는 `argv[1]` 또는 `"."`을 열고, 각 entry의 `e->d_name`을 `fstatat(dd,...,0)`에 전달하여 이름과 `st_size`를 출력한다. Flag 0이므로 symlink의 target을 따른다. `readdir`의 NULL은 정상적인 끝과 오류 모두를 뜻할 수 있다. 따라서 직전 `errno`를 0으로 만들고 NULL 뒤의 `errno`로 구분해야 한다. Entry의 `fstatat` 실패로 남은 `errno`가 나중의 열거 종료를 오류로 오인시키지 않도록 loop에서도 reset한다.

개별 조회 실패를 `perror`로 보고하고 계속하는 이 예는 마지막에 `EXIT_SUCCESS`를 반환한다. 따라서 그 상태만으로 모든 entry의 metadata 조회가 성공했다고 판단하면 안 된다. Source의 흐름을 이해하는 것과 완전한 오류 전달을 구현하는 것은 다른 단계다. [Files and Directories slides 10–11](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/05.IO.Files.and.Directories_3d312c60.pptx)

## 핵심 정리

- 같은 interface가 같은 seek·storage 특성을 뜻하지 않는다.
- Name 삭제, inode의 참조 수, symlink target은 독립해서 추적한다.
- Logical size와 allocated blocks, access와 status time을 구분한다.
- 접근 가능성은 [[courses/system_programming/units/permissions|permission과 identity]]에서 이어 본다.

## 확인·연습문제

### 개념 확인과 추론

#### 확인 Q01 · File type과 byte

Regular file·directory·character/block device·proc/sys의 역할을 구별하라. Alphabet file의 offset 0과25는 무엇이며 같은 fd API가 같은 동작을 뜻하는가?

<details><summary>해설 보기</summary>

Regular file은 byte sequence여서 예의 offset 0은 a, 25는 z이고 format은 application이 해석한다. Directory는 name→inode 관계, character device는 terminal/mouse 같은 stream, block device는 disk/partition 같은 block 접근이다. /proc·/sys는 kernel 상태·설정 등을 드러내는 virtual file interfaces다. Type code는 `- d l p s c b`다. 공통 fd API가 모든 object의 seek·buffering 특성을 같게 만들지는 않는다.

**채점·확인:** Byte·name mapping·두 device·virtual interface를 분리한다.

</details>

#### 확인 Q02 · IPC와 FIFO

별도 process가 왜 IPC를 쓰는가? FIFO producer→gzip consumer와 Unix-domain/network socket을 비교하고 순차 실행의 대기 문제를 설명하라.

<details><summary>해설 보기</summary>

Process는 private address space를 가지므로 다른 process memory를 주소만으로 읽지 못한다. FIFO는 이름이 있어도 내용이 disk file에 저장되는 것이 아니라 kernel을 통한 한 방향 ordered byte channel이다. Open/read가 상대를 기다릴 수 있어 producer가 끝나기만 기다린 뒤 consumer를 시작하면 진행을 막을 수 있다. 강의의 background 실행은 동시 진행 기회를 준다. Unix-domain socket은 local 양방향, network socket은 network endpoint 간 통신이다. Fd가 있다는 이유로 pipe/socket seek가 가능한 것은 아니다.

**채점·확인:** Private memory·kernel channel·대기 원인·socket 범위를 설명한다.

</details>

#### 확인 Q03 · Mount가 숨기는 것

`extern` directory에 tmpfs를 mount하면 기존 파일 `extern/hello`는 어떻게 되는가? Unmount·reboot, echo/printf의 byte 차이와 mount options를 설명하라.

<details><summary>해설 보기</summary>

기존 파일은 가려질 뿐 지워지지 않아 unmount 뒤 다시 보인다. Tmpfs의 새 내용은 volatile하며 기존 disk 파일과 구별된다. `echo hello`는 newline 포함6 bytes, `printf hello`는5다. `ro`는 read-only, `noatime/relatime`은 access-time 정책, `noexec/nosuid/nodev`는 실행·set-ID·device 해석 제한, `size`는 용량, `iocharset`는 해당 filesystem의 문자 설정이다. 완전한 보안 경계는 아니다. 모든 /tmp가 tmpfs라는 주장이나 bind mount 설명으로 확대하지 않는다. Shared tmp 이름 충돌 문제는 남지만 불명확한 생성 API 이름은 추정하지 않는다.

**채점·확인:** 숨김/삭제·6/5 bytes·option 한계를 확인한다.

</details>

#### 확인 Q04 · Name과 inode의 연결

Hard/symbolic link의 inode·count·삭제·cross-filesystem 차이를 설명하라. 전통적 directory에서 자식 directory 두 개면 link count는? ls -a/-d는 무엇을 바꾸는가?

<details><summary>해설 보기</summary>

Hard link는 같은 inode를 이름으로 참조하여 metadata·content를 공유하고 count를 늘린다. 한 이름 제거가 다른 이름을 지우지는 않는다. Symlink는 별도 inode에 target path를 보유해 target hard-link count를 늘리지 않고 target 삭제 후 dangling할 수 있다. Symlink는 filesystem을 건널 수 있지만 hard link는 보통 못 하고 directory hard link는 제한된다. 전통적 부모 directory는 부모의 이름1+자신의 .1+두 자식의 ..2=4, 각 leaf는2다. 자신의 ..는 자기 아닌 부모를 가리킨다. `ls -a`는 숨김 이름을 표시하고 `-d`는 directory 자체를 표시하며 보안 권한을 바꾸지 않는다.

**채점·확인:** 4와 leaf2의 각 참조를 세고 보편 법칙으로 확대하지 않는다.

</details>

#### 확인 Q05 · Filesystem hierarchy 활용

Header, log, 개인 SSH 설정을 찾을 위치와 /bin, /sbin, /etc, /home, /root, /tmp, /usr, /var, /dev, /proc, /sys, /boot, /lib, /mnt, /media의 역할을 설명하라.

<details><summary>해설 보기</summary>

Header는 /usr/include, log는 /var/log, 개인 SSH 설정은 ~/.ssh다. /bin·/sbin은 command·관리 도구, /etc는 system 설정, /home·/root는 사용자·관리자 home, /tmp는 임시 파일, /usr는 설치된 도구·자료, /var는 변하는 상태다. /dev는 device, /proc·/sys는 kernel interface, /boot는 boot 파일, /lib는 library, /mnt·/media는 mount 위치 관례다. 경로 역할로 자료를 찾는 것이 목적이며 모든 배포판의 정확한 배치를 보장하지 않는다. /var/db 사례도 배포판 문맥을 유지한다.

**채점·확인:** 세 실제 위치와 역할 중심 해석·배포판 한계를 확인한다.

</details>

#### 확인 Q06 · Metadata와 allocation

stat의 주요 field를 설명하라. size 8192, blocks 8이면 allocated bytes는? atim·mtim·ctim, timespec과 inode block pointers의 한계도 설명하라.

<details><summary>해설 보기</summary>

dev/ino는 filesystem·inode identity, mode는 type/permission, nlink는 hard links, uid/gid는 owner, rdev는 device identity다. size는 logical bytes, blksize는 권장 I/O 크기, blocks는512-byte 단위이므로8×512=4096이다. 8192보다 작은 allocation은 sparse 가능성을 보이지만 이것만으로 모든 filesystem에서 증명되지는 않는다. atim은 access, mtim은 내용 수정, ctim은 status 변경이며 creation이 아니다. 자료 p.5의 mtim last-access 표기는 p.7과 충돌한다. timespec의 표현 resolution이 실제 정확성을 보장하지 않는다. Inode의 direct/indirect pointer는 data block 위치 탐색이며 stat의 pointer array도 아니고 수 없이 최대 크기를 계산할 수도 없다.

**채점·확인:** 4096·각 시간 의미·ctime 오해·pointer 범위를 확인한다.

</details>

#### 확인 Q07 · Path와 stat family

Relative c/d를 a/b에 anchor하면 어디인가? stat/lstat/fstat/fstatat와 statx의 역할·한계를 설명하라.

<details><summary>해설 보기</summary>

a/b/c/d다. Relative path는 ./로 시작할 필요가 없고 absolute는 /에서 시작한다. stat은 마지막 symlink target, lstat은 link 자체, fstat은 이미 열린 fd를 조사한다. fstatat는 dirfd를 relative anchor로 쓰며 flags0은 follow, AT_SYMLINK_NOFOLLOW는 마지막 link 자체다. Anchor 선택과 follow 선택은 별개다. `statx`는 mask로 원하는/반환된 정보를 표현하고 birth time은 선택적 지원이다. 이 API만으로 모든 rename·race 문제가 제거되지는 않는다.

**채점·확인:** Anchor·follow·opened object를 세 축으로 구분한다.

</details>

#### 확인 Q08 · Directory 순회와 오류

DIR* lifecycle과 dirfd/fdopendir/mkdir 계열을 설명하라. Statter가 argv[1] 또는 .를 읽을 때 readdir NULL·fstatat 실패·종료값을 어떻게 해석하는가?

<details><summary>해설 보기</summary>

opendir→readdir 반복→closedir이며 DIR*는 FILE*·정수 fd와 다르다. dirfd는 directory fd를 얻고 fdopendir는 fd에서 stream을 만들며 mkdir/mkdirat는 directory 생성이다. Statter는 entry 이름을 dirfd 기준 fstatat(flags0)로 조사해 link를 따른다. `readdir` NULL은 끝 또는 오류다. 해당 호출 직전 errno를 clear하고 NULL일 때 확인해야 하며 중간 fstatat 실패의 stale errno를 끝 오류로 착각하지 않는다. 예가 entry 오류 후 계속해서 마지막 success를 내면 모든 entry가 조사됐다는 뜻이 아니다.

**채점·확인:** API 역할·errno 시점·부분 성공 한계를 확인한다.

</details>

### 응용 연습

#### 연습 P01 · Count를 바꾸는 이름

**새로 만든 합성 연습.** 전통적 모델의 D는 빈 자식 directory A, B를 가진다. 별도 regular inode R의 유일한 이름은 `D/r`이다. R의 hard link `D/h`와 symlink `D/s`를 만든 뒤 `D/r`을 제거한다. D와 R의 link count, s의 상태를 설명하라. `D/s`의 target path는 상대 경로 `r`이므로 `D/r`을 가리킨다.

[EX:sp_2025_2_midterm_q03 p.7] Q3(a–b)의 inode reference 계수를 삭제·dangling 시나리오와 결합했다. 선행: Q04. 전통적 directory 모델에 한정하며 모든 filesystem의 2+N 법칙을 주장하지 않는다. [[exam_questions/sp_2025_2_midterm_q03|허용된 관련 문항 미리보기]]

<details><summary>해설 보기</summary>

D는 처음4이며 regular name h와 symlink s는 자식의 .. 참조를 추가하지 않으므로 여전히4다. R은 r만 있을 때1, h 생성 후2, r 제거 후1이다. `s`는 R count에 기여하지 않으며 target path r이 없어 dangling한다. `h`를 통해 R data는 남는다. 이름·path 문자열·inode reference를 따로 계산해야 한다.

**채점·확인:** D=4, R=1, dangling s와 살아 있는 h를 각각 설명한다.

</details>

### 복습 계획

Q01–Q04는 object·name 그림으로, Q06–Q08은 field 단위와 API 선택표로 복습한다. P01에서 삭제 후에도 남는 참조를 세고 잘못된 가정을 Q04로 되돌아가 교정한다.

## 출처

### 날짜별 강의 노트

- [[courses/system_programming/lectures/2026-09-09-lecture-03|2026-09-09 강의 노트]]
- [[courses/system_programming/lectures/2026-09-14-lecture-04|2026-09-14 강의 노트]]
- [[courses/system_programming/lectures/2026-09-16-materials-io-review|2026-09-16 연계 자료]]
- [[courses/system_programming/lectures/2026-09-21-lecture-05|2026-09-21 강의 노트]]

### 수업자료와 강의 구간

- [Unix filesystem slides 4–7](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)
- [Unix filesystem slide 8](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)
- [Unix filesystem slides 11–13](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)
- [Unix filesystem slides 15–18](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)
- [Unix filesystem slides 19–21](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)
- [Unix filesystem slides 22–27](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)
- [Files and Directories slides 3–7](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/05.IO.Files.and.Directories_3d312c60.pptx)
- [Files and Directories slides 8–9](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/05.IO.Files.and.Directories_3d312c60.pptx)
- [Files and Directories slides 10–11](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/05.IO.Files.and.Directories_3d312c60.pptx)
- [[courses/system_programming/transcripts/2026-09-09|2026-09-09 STT 49:54–55:05]]
- [[courses/system_programming/transcripts/2026-09-14|2026-09-14 STT 06:55]]
- [[courses/system_programming/transcripts/2026-09-14|9월 14일 08:32]]
- [[courses/system_programming/transcripts/2026-09-21|2026-09-21 STT 02:32]]
- [[courses/system_programming/transcripts/2026-09-21|2026-09-21 STT 03:59]]
- [[courses/system_programming/transcripts/2026-09-21|2026-09-21 STT 05:42]]

연결된 공개 자료는 slide deck이며, 이 자료들의 PDF 페이지 보기 링크는 제공되지 않았다. 녹취 시각은 일반 텍스트로 표시한다.

- [04.IO.Direct.and.Buffered.IO_8e725857.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO_8e725857.pptx)

### 자료 범위와 한계

- 9월 16일은 녹음 없는 자료 기반 추정 복습이다. 9월 21일 recap은 16일의 정확한 진도를 입증하지 않는다.
- Tmp file API의 불명확한 발화와 mtim 표기 충돌은 남아 있다. 이를 새 발화나 creation-time 설명으로 바꾸지 않는다.
- Directory 2+N은 제시된 전통적 모델 범위다. Mount·sparse·timestamp 동작은 filesystem·환경에 따라 달라진다.
- 기출의 해당 subquestion만 연결하며 제공 답안을 독립 검증된 권위로 삼지 않는다.


---

[[courses/system_programming/units/state-machines|← 이전: 문자 처리와 DFA·Decommenter의 경계조건]] · [[courses/system_programming/units/index|단원 목차]] · [[courses/system_programming/units/permissions|다음: Permission·실행 identity·확장 metadata →]]
