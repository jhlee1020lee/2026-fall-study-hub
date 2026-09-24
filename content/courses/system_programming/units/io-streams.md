---
title: "Unix I/O·열린 파일 상태·stdio buffering"
description: "Unix I/O와 stdio를 반환 단위·공유 offset·buffering으로 비교한다."
course: "system_programming"
unit_id: "io-streams"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["00.Introduction.pptx", "04.IO.Direct.and.Buffered.IO.pptx", "04.IO.Direct.and.Buffered.IO_8e725857.pptx", "05.IO.Files.and.Directories_3d312c60.pptx"]
private_source_assets: []
source_lectures: ["courses/system_programming/lectures/2026-09-02-lecture-01", "courses/system_programming/lectures/2026-09-14-lecture-04", "courses/system_programming/lectures/2026-09-16-materials-io-review", "courses/system_programming/lectures/2026-09-21-lecture-05"]
---

I/O를 요청 byte, 실제 진행량, 열린 file 상태로 나누어 추적한다. Stdio buffer와 kernel offset을 구분하면 short count·dup·flush 결과를 설명할 수 있다.

## Unix I/O: kernel 서비스와 file descriptor

파일 내용의 의미는 application이 정하지만 실제 장치 접근은 kernel의 서비스가 필요하다. System call(시스템 호출)은 이 경계를 넘는 요청이다. Libc(C library)의 wrapper(호출을 감싸는 함수)는 C 함수 형태로 요청을 표현하게 해 준다. [[courses/system_programming/transcripts/2026-09-14|2026-09-14 STT 01:16:19]]은 wrapper가 syscall number와 인자를 필요한 전달 위치에 준비하고 kernel 진입을 요청한다고 설명한다. 불명확한 실제 instruction 이름이나 register 목록까지 복원할 근거는 없다.

`strlen`·`strstr`·일반 수학 계산은 현재 user-space memory에서 수행할 수 있다. 반면 `open`·`read`·`write`는 kernel I/O 서비스를 요청한다. `printf`도 formatting과 buffering 뒤 `write`로 이어질 수 있지만 `printf` 한 번과 `write` 한 번이 일대일인 것은 아니다.

File descriptor(fd, 파일 기술자)는 process 안에서 열린 대상을 지칭하는 non-negative integer handle이다. 보통 `0=STDIN_FILENO`, `1=STDOUT_FILENO`, `2=STDERR_FILENO`가 stdin·stdout·stderr에 대응하며 terminal에 연결되어 시작한다. Redirection(입출력 재지정)은 그 연결을 바꿀 수 있다. 다른 process의 같은 fd 숫자가 같은 파일을 뜻한다는 보장은 없다. [Direct and Buffered I/O slides 4–7](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO.pptx)

Regular file의 current offset(현재 위치)이 0이고 두 번의 `read`가 각각 10 bytes를 성공적으로 읽으면 위치는 `0→10→20`이다. 실제로 전송한 길이만큼 이동한다. 모든 fd가 seek 가능한 것은 아니다. [[courses/system_programming/units/files-metadata|FIFO·socket·regular file]]의 차이가 여기서 드러난다.

### Typedef를 header에서 추적하기

`off_t`는 offset을 표현하는 typedef다. 강의의 underlying type `long`은 해당 target의 예이지 모든 ABI의 고정 규칙은 아니다. 자료가 소개한 조회 흐름은 다음과 같다.

```sh
echo "#include <stdlib.h>" | gcc -E - | grep -w '_*off_t'
```

`echo`가 만든 include 문장을 pipe로 compiler의 stdin에 보낸다. `-E`는 preprocessing까지만 수행하고 뒤의 단독 `-`는 source를 stdin에서 받는다는 뜻이다. Include된 header와 그 header가 다시 include한 선언이 펼쳐지므로 typedef 연결을 추적할 수 있다. `grep` pattern을 작은따옴표로 감싼 것은 shell의 filename expansion과 pattern을 구분하기 위한 보충이다. 이 식을 읽는 것으로 특정 machine의 조회 결과가 새로 확인되는 것은 아니다.

`pread`·`readv`, `pwrite`·`writev`는 전송 관련 variant, `openat`은 열기의 variant, `remove`·`unlink`·`unlinkat`·`rmdir`는 namespace 제거 관련 API로 자료에 소개된다. 이름이 나열되어 있다는 사실과 각 구현을 이미 다뤘다는 주장은 구분한다.

## open과 close: 열린 상태의 수명

`open`은 pathname, access mode와 여러 flag를 받아 열린 상태를 만들고 fd를 반환한다. `O_RDONLY`·`O_WRONLY`·`O_RDWR`는 접근 방향을, `O_CREAT`는 필요할 때 생성, `O_TRUNC`는 내용 길이 초기화, `O_APPEND`는 write가 끝에 붙도록 하는 동작을 표현한다.

새 file 생성 때의 mode argument는 요청 permission이다. 최종 permission과 항상 같다고 가정하지 않는다. 자료의 `/etc/hosts` 예는 `O_RDONLY`, `creat` 예는 owner read/write를 요청한다. `creat`는 생성·truncate 용도의 interface로 이해하면 된다. `open`의 두 인자·세 인자 형태는 C++ overloading이 아니라 variadic declaration과 연결된다. [Direct and Buffered I/O slides 8–11](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO.pptx)

`open` 실패는 -1이고 `errno`를 통해 원인을 설명하며 `perror`로 진단할 수 있다. `close`는 성공 0, 실패 -1을 반환한다. 보통 0·1·2만 사용 중이면 다음 open은 3을 얻지만 3으로 고정되어 있지는 않다.

Close한 **숫자의 재사용**도 생각해야 한다. 같은 process의 descriptor table을 공유하는 구성요소 A가 fd 3을 닫고 B가 다른 파일을 열어 실제로 3을 받았다고 하자. A의 오래된 fd 값을 다시 close하면 새 파일이 닫힐 수 있다. 이는 double close의 위험이며, 서로 독립적인 process의 숫자 3을 혼동하는 것과는 다른 문제다.

9월 14일 녹음은 open·close까지의 연결을 제공한다. 아래의 상세 read/write·stdio·buffer 구현 설명은 녹음이 없는 9월 16일의 **자료 기반 연결 학습**이고, 9월 21일에 확인된 kernel file management 설명과 함께 읽는다. 자료가 있다고 9월 16일의 정확한 수업 종료 지점을 추정하지 않는다.

## read와 write: 요청 길이와 실제 전송 길이

두 함수의 buffer는 [[courses/system_programming/units/objects-pointers|유효한 object와 capacity]]를 전제로 한다.

```c
ssize_t read(int fd, void *buf, size_t count);
ssize_t write(int fd, const void *buf, size_t count);
```

`count`는 요청 byte 수다. `size_t`는 크기를, `ssize_t`는 실제 byte 수와 오류 -1을 표현한다. 양의 길이를 요청한 `read`에서 0은 EOF이며 -1 오류와 다르다. `char buf[512]`에 512를 요청해 302가 반환되었다면 새로 읽힌 유효 데이터는 302 bytes다. 나머지를 이번 입력이라고 취급하면 안 된다. [Direct and Buffered I/O slides 12–20](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO_8e725857.pptx)

String과 buffer 크기도 구분해야 한다. 자료의 `"Hello, world\n"`은 13 characters이고 이를 초기값으로 둔 array의 `sizeof`는 종료 NUL까지 14다. 느낌표가 있는 `"Hello, world!\n"`은 각각 14와 15다. `write`에 `strlen(str)`를 주면 NUL은 출력하지 않는다. 이 사용은 `str`가 실제로 NUL-terminated string이라는 전제가 있다.

파일 append 예는 `O_WRONLY|O_CREAT|O_APPEND`와 요청 mode `0644`로 연 뒤 write·close한다. Source는 write·close 결과 검사를 생략한다. 한 byte copy 예 역시 `read(...,&c,1)>0`인 동안 write하지만 EOF와 read error가 같은 loop 종료 경로로 들어가고 write 결과도 무시한다. 간단한 흐름을 보여 주는 code이지 완전한 오류 처리 모범은 아니다.

### Short count는 실패 여부와 따로 판단한다

Short count(짧은 전송)는 -1 오류 없이 요청보다 적게 전송한 경우다. EOF 근처, terminal에서 현재 읽을 수 있는 입력, pipe·socket의 데이터, interrupt, filesystem 공간 상황 등이 관련될 수 있다. 반환값을 확인하여 이미 처리한 길이와 남은 길이, 다음 buffer 위치를 갱신해야 한다. 모든 상황에 같은 재시도 정책을 무조건 적용하지는 않는다.

Slide 21의 예는 offset 400000부터 100000 bytes를 복사하려 한다. 첫 65536 bytes 다음 요청은 `100000-65536=34464`이고 실제 반환은 27776이다.

`65536 + 27776 = 93312 bytes`  
`100000 - 93312 = 6688 bytes`

따라서 목표보다 6688 bytes 적다. 자료에 없는 마지막 읽기의 정확한 원인이나 보이지 않는 copy 구현을 추정해서 채우면 안 된다. Short count를 `sizeof(buf)`와만 비교하는 표현도 부정확하다. 비교 기준은 실제로 요청한 `count`다.

## lseek와 sparse file의 logical 위치

`lseek(fd,offset,whence)`는 다음 I/O 위치를 조정한다.

| `whence` | 새 위치 |
|---|---|
| `SEEK_SET` | 시작점 기준 `offset` |
| `SEEK_CUR` | 현재 위치 + `offset` |
| `SEEK_END` | 현재 끝 위치 + `offset` |

성공하면 새 absolute position, 실패하면 -1을 반환한다. `lseek(fd,100,SEEK_SET)` 뒤의 다음 I/O는 offset 100에서 시작한다. File 길이가 20일 때 seek만 100으로 했다고 길이가 즉시 100으로 늘지는 않는다. 이후 그 위치에 쓰면 새 EOF와 중간 hole이 만들어질 수 있고, hole을 읽으면 0이 나온다. 실제 할당 방식은 filesystem에 따라 달라진다. 그래서 [[courses/system_programming/units/files-metadata|st_size와 st_blocks]]는 다를 수 있다. Pipe·socket에 regular-file seek를 가정하지 않는다. [Direct and Buffered I/O slides 17–18](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO_8e725857.pptx)

## Descriptor·open-file entry·inode는 다른 층이다

같은 파일을 사용한다고 같은 offset까지 공유하는 것은 아니다. 세 층을 나누면 열린 상태가 어디에 있는지 알 수 있다.

| 층 | 보관하는 관계 또는 정보 |
|---|---|
| Process descriptor table | fd 번호 → 열린 entry의 연결 |
| Open-file entry | current position, reference count 등 열린 상태 |
| Vnode/inode 관련 구조 | file type·size·access metadata |

같은 pathname으로 `open`을 두 번 호출하면 같은 file metadata를 향해도 open-file entry와 offset은 독립이다. [[courses/system_programming/transcripts/2026-09-21|2026-09-21 STT 14:07]]은 이를 명시적으로 구분한다. 10:13의 “process마다 open-file table 하나”라는 표현은 자료의 공유 관계와 충돌하므로, 여기서는 process별 descriptor table이 공유 가능한 open-file entry를 참조하는 모델로 정리한다. [Files and Directories slides 13–14](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/05.IO.Files.and.Directories_3d312c60.pptx)

`fork`로 상속한 descriptor는 parent와 child의 별도 descriptor table에서 같은 entry를 참조할 수 있다. Descriptor passing도 정수 하나를 보내는 것과 다르다. Kernel이 수신 process의 fd를 같은 열린 entry에 연결하며 reference가 늘어나는 개념이다. 수신 fd 숫자는 송신 fd와 같을 수도 다를 수도 있다. 여기서는 공유 관계를 이해하며 fork 전체나 descriptor 전달 code의 구현은 후속 범위다.

### dup과 dup2로 연결 바꾸기

`dup(oldfd)`는 같은 open-file entry를 참조하는 가장 작은 사용 가능 fd를 반환한다. 반환값을 `fd2`라는 변수에 넣어도 실제 숫자는 4일 수 있다. 변수명과 stderr의 fd 2는 다르다.

Stdout 1을 닫고 `dup(3)`을 하면 그 순간 가장 작은 빈 번호가 1일 때 1을 얻는다. 하지만 close와 dup 사이에 다른 작업이 들어올 수 있으므로 두 호출을 원자적인 조작으로 가정하지 않는다. `dup2(oldfd,newfd)`는 지정한 `newfd`를 같은 entry에 연결한다. 쓰기 가능한 fd를 `dup2(fd,STDOUT_FILENO)`로 1에 연결하면 이후 stdout의 대상이 그 파일이 된다. 자료의 이 예는 `O_WRONLY`이며, 없는 `O_CREAT`·`O_TRUNC`를 덧붙여 원문 동작으로 읽지 않는다.

`ls > output.txt`, `cat < input.txt`는 출력·입력 재지정이고 `ls | sort -R`은 한 process의 출력을 다른 process의 입력으로 잇는다. 두 fd가 같은 entry를 참조한 뒤 하나를 닫아도 남은 reference는 유효하다. 기출 Q3(c)에 적용할 때도 fd 번호, 살아 있는 reference, 공유 offset, 덮어쓰는 범위를 각 단계에서 따로 기록해야 한다. [EX:sp_2025_2_midterm_q03 p.7]

## 두 열린 파일 예제로 offset 추적하기

### 독립 open 뒤 일부 descriptor를 묶기

`fwfd1.c`의 입력은 `System Programming`이다. 세 번 독립 open한 뒤 `dup2(fd2,fd3)`를 수행한다. 이제 fd1의 entry는 독립이고 fd2와 fd3는 같은 entry다.

| 동작 | 읽기 전 offset | 읽은 문자 | 영향 |
|---|---:|---|---|
| fd1에서 1 byte read | 독립 entry 0 | `S` | fd1 entry만 1 |
| fd2에서 1 byte read | 공유 entry 0 | `S` | fd2·fd3 entry 1 |
| fd3에서 1 byte read | 공유 entry 1 | `y` | 공유 entry 2 |

따라서 `c1=S,c2=S,c3=y`다. 파일 자체가 하나라는 이유로 처음부터 세 offset을 묶거나, fd 숫자가 다르다고 끝까지 분리하면 틀린다. [Files and Directories slide 19](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/05.IO.Files.and.Directories_3d312c60.pptx)

### Append와 일반 write가 섞일 때

`fwfd2.c`는 fd1을 `O_CREAT|O_TRUNC|O_RDWR`로 열고 `CSAP` 네 bytes를 쓴다. 별도로 연 fd3에는 `O_APPEND`가 있다. 성공하는 경로를 순서대로 추적하면 다음과 같다.

| 동작 | 내용 | fd1·그 duplicate가 공유할 위치 |
|---|---|---:|
| fd1로 `CSAP` 쓰기 | `CSAP` | 4 |
| 독립 append fd3로 `M1522` 쓰기 | `CSAPM1522` | 여전히 4 |
| `fd2=dup(fd1)` | 내용 변화 없음 | 4 |
| fd2로 `SNU` 쓰기 | `CSAPSNU22` | 7 |
| fd3로 `800` append | `CSAPSNU22800` | 여전히 7 |

`SNU`는 fd1에서 물려받은 위치 4–6의 `M15`를 덮는다. 마지막 fd3는 현재 EOF에 붙인다. 결과는 `CSAPSNU22800`이다. Slide의 따옴표 안 공백은 추출문에서 생긴 공백과 구분해야 한다. 이 trace는 source의 성공 경로 계산이며 생략된 오류 처리를 검증하는 실행 결과는 아니다. [Files and Directories slide 20](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/05.IO.Files.and.Directories_3d312c60.pptx)

## Standard I/O와 FILE stream

Standard I/O(표준 입출력)는 `FILE *` stream을 통해 formatting과 buffering을 제공한다. `stdin`·`stdout`·`stderr`는 보통 fd 0·1·2와 연결된다. `FILE *`, fd 정수, [[courses/system_programming/units/files-metadata|DIR *]]는 서로 다른 abstraction이다.

| 목적 | 대표 API와 관련 variant |
|---|---|
| 열기·연결 | `fopen`, `fdopen`, `freopen` |
| Element 전송 | `fread`, `fwrite` |
| 위치 | `fseek`, `ftell`, `rewind`, `fgetpos`, `fsetpos` |
| Character·line 입력 | `fgets`, `fgetc`, `getc`, `getchar`, `ungetc` |
| Formatted 입력 | `fscanf`, `scanf`, `sscanf`, `vscanf` |
| Character·line 출력 | `fputs`, `fputc`, `putc`, `putchar`, `puts` |
| Formatted 출력 | `fprintf`, `printf`, `dprintf`, `sprintf`, `snprintf`, `vprintf` |
| 종료·상태 | `fclose`, `fflush`, `feof`, `ferror`, `fileno` |

계열 안에서도 출력 대상, 길이 제한, 인자 전달 방식이 다르며 모든 variant가 ISO C 함수라는 뜻은 아니다. `fgets`에는 buffer 한도가 있다. 자료에서 `gets`는 취소선으로 표시되어 있으며 사용 권장이 아니다. `fputs`의 반환 type을 `char`로 적은 표와 `sprint` 철자도 그대로 API 계약으로 채택하지 않는다. [Direct and Buffered I/O slides 27–31](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO_8e725857.pptx)

`fread(ptr,size,nmemb,stream)`의 요청 bytes는 `size*nmemb`지만 반환값은 완료한 **element 수**다. 4-byte element를 요청하여 7이 반환되면 완성된 element는 28 bytes 분량이다. 부분적으로 읽힌 마지막 element에 대한 정보까지 그 숫자로 확정할 수는 없다. `fseek`는 성공 상태를 `int`로 반환하고 `ftell`이 위치를 얻는다. 후속 요약 표의 `off_t fseek`와 혼동하지 않는다. `feof`·`ferror`는 이미 생긴 상태를 검사하므로 다음 read의 성공을 미리 예측하는 조건이 아니다.

### fopen의 획득·사용·해제 흐름

자료의 file 출력은 `fopen("./output.txt","a+")`로 시작한다. `a+`는 reading과 append를 요청하지만 이 예가 실제 수행하는 것은 출력이다. NULL이면 `perror("Cannot open/create file")`를 호출하고 `EXIT_FAILURE`를 반환한다. 성공하면 `fprintf(out,"%s",str)`, `fclose(out)`, `EXIT_SUCCESS` 순서다.

`fopen` 실패는 pointer NULL, Unix `open` 실패는 정수 -1이다. 원문이 `fprintf`와 `fclose` 결과를 확인하지 않으므로 마지막 success를 모든 출력과 close의 성공 증거로 삼으면 안 된다. 또한 `fprintf(stdout,...)`와 `printf(...)`를 둘 다 실행하면 같은 역할의 두 호출이므로 두 번 출력한다.

## Buffering이 system call 횟수를 줄이는 방식

한 byte마다 kernel 경계를 넘으면 호출 비용이 반복된다. Standard I/O는 user-space buffer에 작은 작업을 모아 더 큰 `read`·`write`로 처리한다. Formatting은 값을 문자로 만드는 편의 기능이고 buffering은 전송 횟수를 조절하는 기능이므로 서로 구분해야 한다.

자료의 10 MiB byte-copy 측정값은 다음과 같다.

| 방식 | real | user | sys |
|---|---:|---:|---:|
| Byte마다 Unix I/O | 2.679 s | 0.363 s | 2.316 s |
| Standard I/O | 0.261 s | 0.261 s | 0.000 s |

이는 그 실행의 예시이며 보편적인 배속이나 고정 syscall 비용이 아니다. `sys=0.000`도 kernel 호출이 없었다는 뜻이 아니라 표시된 측정값이다. Raw I/O도 큰 block으로 옮기면 비교가 달라진다. 기출 Q3(d) 역시 함수 이름만 비교하기보다 같은 데이터에 대한 kernel 경계 통과 횟수와 buffer의 역할을 설명하도록 요구한다. [EX:sp_2025_2_midterm_q03 p.8] [Direct and Buffered I/O slides 23–25](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO_8e725857.pptx)

### Application의 소비 위치와 kernel offset

Input buffer에 `B0…Bk-1`을 한 번에 가져오면 kernel의 다음 위치는 `Bk`다. Application은 아직 일부만 소비하여 다음 stream byte가 `Bs`일 수 있다. 따라서 logical stream position과 fd offset은 동시에 같을 필요가 없다.

Slide 40의 그림에서는 user-space FILE 쪽 `bufpos=378`, `fd=4`와 kernel open-file entry의 `pos=1024, refcnt=1`을 구분해 보면 된다. Application에 아직 읽을 buffered bytes가 남아 있는데 raw fd는 1024 이후를 가리킬 수 있다. FILE buffer, process descriptor table, open-file entry, vnode metadata, kernel disk block cache, storage는 다른 층이다. 그림 위의 `fopen` 표시가 그 호출만으로 언제나 1024 bytes를 즉시 읽는다는 뜻은 아니다. [Direct and Buffered I/O slides 26, 39–40](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO_8e725857.pptx)

## Buffering mode와 flush 시점

자료의 대표적인 설정은 다음과 같다. 실제 stream과 환경을 함께 고려하며 `setvbuf`로 mode를 조정할 수 있다.

| Mode | 대표 용도 | 동작 |
|---|---|---|
| Fully buffered, `_IOFBF` | file | input buffer가 비면 refill, output이 차거나 명시적으로 flush하면 전송 |
| Line buffered, `_IOLBF` | terminal | newline 등 조건에서 output 전송 |
| Unbuffered, `_IONBF` | stderr의 대표 기본값 | stdio output buffer에 모아 두지 않음 |

Line-buffered output은 newline, buffer full, 명시적인 `fflush`, stream close, 정상 종료 등에서 배출될 수 있다. Input 요청과 연동되는 flush는 해당 stream과 환경 조건에 따르며 모든 입력이 모든 출력을 flush한다고 일반화하지 않는다. 비정상 종료까지 항상 flush되는 것도 아니다. Unbuffered라 해도 kernel·device buffer까지 없다는 뜻은 아니고, `fflush`도 durable disk commit(저장장치에 영속적으로 확정)과 같지 않다.

Slide 37은 line buffering에서 다음 흐름을 보여 준다.

```c
setvbuf(stdout, NULL, _IOLBF, 0);
printf("hello\n");
printf("hello");
printf(",");
fflush(stdout);
printf("wor");
printf("ld");
printf("\n");
```

첫 newline은 `hello\n` 6 bytes를, 명시적 flush는 `hello,` 6 bytes를, 마지막 newline은 `world\n` 6 bytes를 보내는 source trace와 연결된다. 마지막 두 fragment는 `wor`와 `ld`이며 공백을 새로 넣지 않는다. 여섯 `printf`로 `h,e,l,l,o,newline`을 하나씩 출력하는 slide 32 예도 하나의 6-byte write로 모일 수 있다. [Direct and Buffered I/O slides 32–37](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO_8e725857.pptx)

## FILE의 작은 구현 모형으로 buffer 계약 이해하기

자료의 pseudocode는 `open`으로 fd를 얻고 FILE과 buffer를 할당한 뒤 `bufpos=0, bufsize=0`으로 시작한다. 여기의 `bufsize`는 확보한 capacity가 아니라 **남아 있는 유효 데이터 수**다.

`refill_buffer`는 read를 수행한 뒤 `bufpos`를 0으로, 양수 반환값을 `bufsize`로 설정한다. `slide_buffer`는 소비한 len만큼 `bufpos`를 늘리고 `bufsize`를 줄인다. 따라서 len이 남은 데이터보다 클 수 없다. `fread` 모형은 `size*nmemb` bytes를 목표로 삼아 buffer가 비면 refill하고, 남은 요청과 남은 buffer 중 작은 길이만 복사한 뒤 양쪽 위치를 갱신한다.

이 순서는 buffering의 핵심을 보여 주지만 그대로 실제 libc 구현은 아니다. 모형은 `read_bytes`를 반환하므로 실제 `fread`의 element-count 계약과 다르다. `fclose` 모형도 close와 두 free만 보이고 output flush·실패 전달은 생략한다. Allocation 실패 cleanup, 곱셈 overflow, EOF/error flag, `void *` 산술과 field 이름 불일치도 남아 있다. `fileno`는 stream의 underlying fd를 얻는 관계를 보여 준다. [Direct and Buffered I/O slides 41–43](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO_8e725857.pptx)

## Binary data와 목적에 맞는 I/O interface

JPEG, GIF, object file에는 임의 bytes가 들어간다. Newline으로 나눈다고 의미 있는 record가 되지 않으며, `strlen`·`strcpy`는 중간 NUL에서 멈추거나 NUL이 없으면 buffer 경계를 넘어갈 수 있다. Unix text의 LF(`0x0A`)와 Windows·HTTP 예의 CRLF(`0x0D 0x0A`)도 line convention의 차이다. [Files and Directories slide 25](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/05.IO.Files.and.Directories_3d312c60.pptx)

문제는 stdio 전체가 binary를 못 다루는 데 있지 않다. 알려진 크기를 사용하는 `fread`·`fwrite`는 binary에도 사용할 수 있다. 임의 bytes를 line이나 NUL-terminated string으로 가정하는 사용법을 피해야 한다.

일반적인 disk·terminal 작업에는 요구를 충족하는 높은 수준 interface부터 고려한다. Stdio는 formatting·buffering과 내부의 짧은 전송 처리를 도와도 반환 element 수와 EOF·error 확인을 없애 주지는 않는다. File permission·size 같은 metadata에는 `stat`·`fstat` 계열이 필요하다. [[courses/system_programming/units/permissions|권한 정보]]와 stream의 데이터 전송은 다른 기능이다.

Signal handler에서는 stdio를 안전하다고 가정하면 안 된다. Async-signal-safe(비동기 signal 처리 중 호출 안전성)는 중단된 실행 중 handler에서 호출해도 정해진 계약을 지키는 속성이다. `read`·`write` 같은 raw interface의 개별 계약을 확인해야 하며 “Unix I/O라는 이름이면 모두 안전하다”는 일반화는 피한다. Network socket에 관한 자료의 경고 역시 buffering과 양방향 stream 제약을 무시하지 말라는 의미다. FILE이 socket과 원천적으로 연결 불가능하다는 뜻은 아니다. 상세 signal·socket 구현은 이후 범위다. 최고 성능을 위해 raw I/O가 필요할 수도 있지만 전송 크기와 buffer 관리에 따라 결과가 달라진다. [Direct and Buffered I/O slides 45–47](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO_8e725857.pptx)

## 핵심 정리

- 요청량과 실제 처리량, byte와 element를 구분한다.
- Fd 번호가 아닌 open-file entry가 offset 공유를 결정한다.
- Buffering·formatting·kernel cache·disk durability는 별개다.
- 주소·alignment의 다음 연결은 [[courses/system_programming/units/memory-layout|memory layout]]이다.

## 확인·연습문제

### 개념 확인과 추론

#### 확인 Q01 · Library와 syscall

strlen·strstr·printf와 kernel I/O의 차이, fd0·1·2, read 10 두 번의 offset을 설명하라. off_t와 preprocessing 조회 pipeline은 무엇을 알려 주는가?

<details><summary>해설 보기</summary>

strlen·strstr는 user-space 계산이고 printf는 format·buffer 처리를 거쳐 필요할 때 kernel 서비스를 쓴다. 매 printf가 write 한 번이라는 뜻은 아니다. Syscall wrapper는 번호·인자를 통해 kernel entry를 요청하지만 불명확한 register 세부는 추정하지 않는다. Fd는 process-local nonnegative integer이며0/1/2는 stdin/stdout/stderr다. Offset 0에서 성공한 read 10 두 번은0→10→20이다. off_t는 target의 typedef다. `echo "#include <stdlib.h>" | gcc -E - | grep -w '_*off_t'`는 header를 stdin으로 preprocess하고 관련 token을 찾는다. `-E`는 preprocessing, 마지막 `-`는 stdin이고 header가 간접 include할 수 있다. 실제 실행·보편 type 증명이 아니다.

**채점·확인:** User/kernel·fd scope·0→20·pipeline 각 역할을 확인한다.

</details>

#### 확인 Q02 · Open·close와 재사용

open의 access·creation flags와 mode, 실패 반환과 close를 설명하라. 이미 닫은 fd 숫자를 다시 close하면 언제 새 파일을 닫는가?

<details><summary>해설 보기</summary>

O_RDONLY/O_WRONLY/O_RDWR는 접근 선택, O_CREAT는 생성, O_TRUNC는 잘라내기, O_APPEND는 append다. Mode는 생성 시 요청 권한으로 실제 permission을 단독 결정하지 않는다. Open은 variadic 선언이지 C overload가 아니다. 실패는−1과 errno이며 perror로 진단한다. Close는0 성공/−1 오류다. 같은 descriptor table에서 old fd를 닫은 뒤 다른 open이 그 번호를 재사용하면 stale close는 새 entry를 닫을 수 있다. 독립 process의 같은 숫자는 이 사례와 다르다.

**채점·확인:** Flags·requested mode·반환값·같은 table 재사용을 확인한다.

</details>

#### 확인 Q03 · 요청 byte와 실제 byte

512 요청에 read가302·0·−1이면 각각 무슨 뜻인가? write의 count, 두 Hello literal의 length/sizeof와 간단한 copy loop의 누락을 설명하라.

<details><summary>해설 보기</summary>

302는 앞302 bytes만 새 데이터이며 positive count 요청의0은 EOF, −1은 오류다. Count는 size_t byte 수, 결과 ssize_t는 실제 수/오류다. `"Hello, world\n"`는 length 13, sizeof 14이고 !를 더한 `"Hello, world!\n"`는14/15다. strlen은 NUL을 세지 않는다. Append 예의0644는 요청 mode다. `while(read(...)>0)`만 쓰면 EOF와 오류가 합쳐지고 write short count·write/close 오류를 무시할 수 있다.

**채점·확인:** 302 유효 범위·세 반환·13/14와14/15·오류 누락을 확인한다.

</details>

#### 확인 Q04 · Short count 계산

100000 bytes 요청 후65536, 이어27776 bytes를 받았다. 둘째 요청 크기·누적·남은 수는? Short count만으로 원인이나 retry 성공을 알 수 있는가?

<details><summary>해설 보기</summary>

둘째 요청은100000−65536=34464, 누적은65536+27776=93312, 남은 수는6688이다. Short positive count는 그만큼 진행했다는 뜻이며 자체가−1 오류는 아니다. Buffer 시작을 누적 수만큼 이동하고 남은 요청을 줄여야 한다. 종료·재시도 판단은 실제 interface와 결과에 달려 있고 원인을 임의로 단정하지 않는다.

**채점·확인:** 34464/93312/6688과 진행량 기반 갱신을 확인한다.

</details>

#### 확인 Q05 · Seek와 file length

SEEK_SET/CUR/END와 lseek 반환은? 길이20 파일에서100으로 seek한 뒤 아직 write하지 않았다면 길이·hole은?

<details><summary>해설 보기</summary>

SET은 주어진 absolute offset, CUR은 현재+offset, END는 끝+offset을 기준으로 새 위치를 정하고 성공 반환은 새 absolute offset, 오류는−1이다. Seek만으로 길이는20 그대로다. 이후 offset 100에 write하면 사이 gap이 생기며 읽을 때 zero로 보이고 실제 allocation은 filesystem에 달린다. Pipe/socket에는 같은 seek 모델을 적용하지 않는다.

**채점·확인:** 위치/길이와 write 시점·allocation을 구별한다.

</details>

#### 확인 Q06 · FILE* API와 반환 단위

FILE*와 fd/DIR*, fopen/fdopen/freopen, fread/fwrite와 fseek/ftell, feof/ferror를 비교하라. a+ 예와 문자열 API에서 확인해야 할 오류는?

<details><summary>해설 보기</summary>

FILE*는 library stream이다. `fopen`은 path, fdopen은 기존 fd, freopen은 stream 재연결이다. `fread`/fwrite는 byte 아닌 complete element 수: size 4에서7은28 complete bytes이며 partial element 가능성도 있다. `fseek`는 성공0/오류 status, ftell은 위치, feof/ferror는 이미 발생한 상태를 확인한다. Fgets는 bounded line input이고 gets는 안전한 대체가 아니다. 자료의 fputs return char와 sprint 표기는 그대로 API로 쓰지 않는다. `fopen` a+는 읽기+append이고 NULL 실패 시 perror/EXIT_FAILURE; 성공 후 fprintf/fclose도 실패 가능해 체크가 필요하다. 소개된 두 printf가 실행되면 출력도 두 번이다.

**채점·확인:** 요소/byte·status/position·retrospective flag·누락 오류를 확인한다.

</details>

#### 확인 Q07 · Buffering의 비용

한 글자씩 getchar/putchar를 부르는 것과 read/write count 1의 kernel call 수가 왜 다른가? 강의 time 결과를 어떻게 해석하는가?

<details><summary>해설 보기</summary>

Stdio는 여러 문자를 buffer로 묶어 syscall을 줄인다. Formatting과 buffering은 다른 역할이며 raw I/O도 큰 block으로 묶을 수 있다. 예의 약10MiB에서 unbuffered2.679 real/0.363 user/2.316 sys, buffered0.261/0.261/0.000은 해당 측정이다. 표시0.000은 syscall 부재가 아니고 모든 workload의 같은 speedup을 보장하지 않는다.

**채점·확인:** Library 호출 수와 kernel 호출 수·측정 범위를 구분한다.

</details>

#### 확인 Q08 · 두 위치를 가진 stream

FILE buffer의 logical position378, fd4의 kernel offset 1024, refcount1이면 다음 stdio/raw read는 어디서 시작하는가? Cache·disk와도 구별하라.

<details><summary>해설 보기</summary>

이미 읽어 둔 첫1024-byte block에서 stdio는 logical378의 buffered byte를 소비하고646 bytes가 남아 있다. 같은 fd에 raw read하면 kernel offset 1024부터 요청하므로 두 위치를 같다고 가정하면 안 된다. FILE buffer, process fd table, open-file entry, inode/kernel cache, disk는 서로 다른 층이다. `fopen` 자체가 항상1024 bytes를 읽는 규칙은 아니다.

**채점·확인:** 378/1024/646과 각 저장 층을 구분한다.

</details>

#### 확인 Q09 · Flush 경계

Fully/line/unbuffered의 대표 대상과 setvbuf를 설명하라. hello newline, hello와 comma 후 fflush, wor+ld+newline 출력과 종료 시점을 추적하라.

<details><summary>해설 보기</summary>

Regular file은 _IOFBF, terminal은 _IOLBF, stderr는 _IONBF의 대표 예이며 setvbuf로 조정한다. Line buffer의 `hello\n`는6 bytes를 newline에 내보낸다. `hello`+comma 뒤 fflush는6 bytes를 보내고, `wor`+`ld`+newline은 `world\n`6 bytes다. Buffer full·해당 newline·명시적 fflush·close·정상 종료가 flush 계기가 될 수 있다. Input에 의한 flush는 조건부이며 비정상 종료를 같은 보장으로 보지 않는다. Unbuffered도 kernel buffer가 없다는 뜻이 아니고 fflush는 disk durability 보장이 아니다.

**채점·확인:** 세6-byte 출력·조건부 flush·durability를 확인한다.

</details>

#### 확인 Q10 · Stdio 의사코드의 불변식

강의 FILE 의사코드의 allocation·bufpos·bufsize·refill·consume을 설명하고 표준 API와 다른 부분을 지적하라.

<details><summary>해설 보기</summary>

Fd·FILE object·buffer를 확보하고 초기 bufpos=0, bufsize=0은 valid unread data가0이라는 뜻이지 capacity 0이 아니다. Refill은 위치를 reset하고 실제 read 수를 valid size로 둔다. Consume len은 요청과 valid bytes 이하로 제한한 뒤 pos+=len, size−=len이다. Loop는 여러 refill로 요청을 채운다. 예의 fread가 byte를 반환하는 것은 표준의 element 반환과 다르다. `fclose` 예는 output flush·오류 처리가 빠졌고 allocation cleanup·overflow·void* 연산·이름도 개념 코드 한계다.

**채점·확인:** Valid size/capacity·갱신식·표준과의 차이를 확인한다.

</details>

#### 확인 Q11 · Fd와 공유 offset

독립 open, dup, fork로 받은 fd, 다른 process로 descriptor 전달에서 무엇을 공유하는가? 같은 숫자나 같은 inode가 충분한가?

<details><summary>해설 보기</summary>

Process fd table entry는 offset/refcount를 가진 open-file entry를 가리키고 그 아래 file identity가 있다. 같은 file을 독립 open하면 inode는 같아도 offset은 별개다. `dup`와 fork로 inherited된 해당 fd는 같은 open-file entry·offset을 공유한다. Descriptor passing은 kernel이 entry 연결을 전달하는 것이지 integer만 보내는 것이 아니며 수신 숫자는 달라도 된다. 9월21일10:13의 상충 표현을14:07의 명시적 독립-open 설명과 구별한다.

**채점·확인:** Fd table·open entry·inode 세 층과 세 공유 경로를 확인한다.

</details>

#### 확인 Q12 · Redirection과 dup

Shell의 >, <, |와 dup/dup2를 설명하라. close(1); dup(3)가1을 만드는 조건과 두 호출의 한계는?

<details><summary>해설 보기</summary>

>는 stdout, <는 stdin, |는 앞 출력과 뒤 입력을 연결한다. `dup`는 최저 free fd를 택하며 변수 fd2라는 이름이 숫자2를 뜻하지 않는다. Close1 뒤1이 가장 낮은 free이고 fd3이 유효하면 dup3은1이지만 둘은 별도 호출이라 중간 재사용 가능성이 있다. `dup2`는 지정 target을 source와 같은 open entry에 연결한다. Offset은 공유하고 하나를 close해도 다른 참조가 남으면 사용할 수 있다. Source의 O_WRONLY만 있는 open에 O_CREAT/O_TRUNC 효과를 덧붙이지 않는다.

**채점·확인:** Lowest free·지정 target·공유 상태·별도 호출을 확인한다.

</details>

#### 확인 Q13 · 두 성공 경로 추적

강의의 fwfd1에서 같은 System Programming 파일의 독립 fd1/fd2와 dup2(fd2, fd3)로 한 글자씩 fd1, fd2, fd3를 읽으면? fwfd2에서 CSAP write 4, 별도 append M1522, dup(fd1)로 SNU write, 마지막 append800을 추적하라.

<details><summary>해설 보기</summary>

`fwfd1`의 결과는 S, S, y다. Fd1 offset은1, fd2/fd3 shared offset은2다. `fwfd2`는 CSAP 뒤 fd1 offset 4, length 4; append M1522 뒤 content CSAPM1522, length 9, fd1은4 그대로다. `dup`(fd1)의 SNU는 offset 4부터 M15를 덮어 CSAPSNU22, shared offset 7이 된다. Append800은 끝에 붙여 CSAPSNU22800, length 12다. Append entry와 독립 entry의 position을 섞지 않는다. 이는 모든 call 성공을 둔 종이 trace이며 실제 실행 보고가 아니다.

**채점·확인:** S/S/y·1/2·각 content·offset·length를 모두 확인한다.

</details>

#### 확인 Q14 · Binary와 interface 선택

NUL·newline이 있는 binary data에 strlen copy가 부적절한 이유와 fread/fwrite 가능성을 설명하라. LF/CRLF, metadata·signal·socket에서 API 선택은?

<details><summary>해설 보기</summary>

Binary는 NUL을 포함한 임의 byte라 strlen이 중간에서 멈추며 newline도 일반 byte이지 자동 record 경계가 아니다. `fread`/fwrite는 명시적 길이로 binary를 처리할 수 있다. LF는0A, CRLF는0D0A다. 필요한 제어를 만족하는 높은 수준 interface를 고르되 metadata는 stat/fstat를 사용한다. Signal 문맥에서 일반 stdio는 안전하지 않고 개별 async-signal-safe 규칙이 필요하다. Socket은 stream 제약을 확인해야 하지만 stdio 사용이 절대 불가능한 것은 아니다. Raw I/O가 항상 빠르다는 주장도 틀리다.

**채점·확인:** Binary length·줄 끝 bytes·필요 기능별 선택을 확인한다.

</details>

### 응용 연습

#### 연습 P01 · Shared와 independent를 함께 추적

**새로 만든 합성 연습.** 초기 file ABCDEFGH. 독립 open a, b는 offset 0이고 c=dup(a)다. 모든 call이 성공한다고 할 때 lseek(c, 2, SET), write(a, "xy", 2), read(b, 3), close(a), write(c, "Z", 1) 뒤 file·read bytes·offset은?

[EX:sp_2025_2_midterm_q03 p.7] Q3(c)의 dup·seek·close 뒤 overwrite 추론에 독립 reader를 추가했다. 선행: Q05·Q11–Q13. 성공 call·regular file 가정이며 private 원문 변형 복사가 아니다. [[exam_questions/sp_2025_2_midterm_q03|허용된 관련 문항 미리보기]]

<details><summary>해설 보기</summary>

C seek는 a/c shared offset 2로 만든다. Write xy는 C, D를 덮어 ABxyEFGH, shared 4다. B는 독립0부터 ABx를 읽어 b offset 3이다. Close a 후에도 c가 entry를 유지한다. C의 Z는 offset 4의 E를 덮어 ABxyZFGH, shared offset 5, length 8이다. Seek·dup·close는 string 삽입을 하지 않는다.

**채점·확인:** ABx·ABxyZFGH·b3/c5·length 8을 이유와 함께 제시한다.

</details>

#### 연습 P02 · 호출 수와 flush 조건

**새로 만든 합성 연습.** 8192-byte file 복사에서 A는 raw1-byte read/write, B는4096-byte block read/write다. 모든 요청이 완전히 처리되고 마지막 EOF read를 포함한다. 호출 수를 계산하고 character stdio 및 terminal newline 조건을 비교하라.

[EX:sp_2025_2_midterm_q03 p.8] Q3(d)의 syscall 비용 추론을 block raw I/O와 flush 조건 비교로 확장했다. 선행: Q07–Q09·Q14. 기출의 file 크기·제공 답안을 복사하지 않는다.

<details><summary>해설 보기</summary>

A는8192 read+1 EOF read+8192 write=16385 calls다. B는2 read+1 EOF read+2 write=5다. 같은 EOF-driven character stdio loop의 `getchar`는 EOF 확인을 포함해 8193회, `putchar`는 8192회 호출된다. 내부 buffering으로 syscall 수는 더 적을 수 있으나 buffer 크기·flush 조건 없이 정확한 syscall 수를 정하지 않는다. Terminal line buffer의 newline은 더 이른 flush를 유발할 수 있다. Ratio16385/5를 실행시간 speedup으로 바꾸지 않는다.

**채점·확인:** EOF 포함16385/5·library/kernel 차이·시간 비례 금지를 확인한다.

</details>

### 복습 계획

Q01–Q06에서 반환값 옆에 단위를 적는다. Q08·Q11–Q13은 FILE buffer/fd/open entry 세 층으로 그린 뒤 P01을 추적한다. Q07·Q09·Q14를 P02의 호출 수와 함께 복습한다.

## 출처

### 날짜별 강의 노트

- [[courses/system_programming/lectures/2026-09-02-lecture-01|2026-09-02 강의 노트]]
- [[courses/system_programming/lectures/2026-09-14-lecture-04|2026-09-14 강의 노트]]
- [[courses/system_programming/lectures/2026-09-16-materials-io-review|2026-09-16 연계 자료]]
- [[courses/system_programming/lectures/2026-09-21-lecture-05|2026-09-21 강의 노트]]

### 수업자료와 강의 구간

- [Direct and Buffered I/O slides 4–7](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO.pptx)
- [Direct and Buffered I/O slides 8–11](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO.pptx)
- [Direct and Buffered I/O slides 12–20](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO_8e725857.pptx)
- [Direct and Buffered I/O slides 17–18](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO_8e725857.pptx)
- [Files and Directories slides 13–14](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/05.IO.Files.and.Directories_3d312c60.pptx)
- [Files and Directories slide 19](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/05.IO.Files.and.Directories_3d312c60.pptx)
- [Files and Directories slide 20](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/05.IO.Files.and.Directories_3d312c60.pptx)
- [Direct and Buffered I/O slides 27–31](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO_8e725857.pptx)
- [Direct and Buffered I/O slides 23–25](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO_8e725857.pptx)
- [Direct and Buffered I/O slides 26, 39–40](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO_8e725857.pptx)
- [Direct and Buffered I/O slides 32–37](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO_8e725857.pptx)
- [Direct and Buffered I/O slides 41–43](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO_8e725857.pptx)
- [Files and Directories slide 25](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/05.IO.Files.and.Directories_3d312c60.pptx)
- [Direct and Buffered I/O slides 45–47](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO_8e725857.pptx)
- [[courses/system_programming/transcripts/2026-09-14|2026-09-14 STT 01:16:19]]
- [[courses/system_programming/transcripts/2026-09-21|2026-09-21 STT 14:07]]

연결된 공개 자료는 slide deck이며, 이 자료들의 PDF 페이지 보기 링크는 제공되지 않았다. 녹취 시각은 일반 텍스트로 표시한다.

- [00.Introduction.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx)
- [[courses/system_programming/transcripts/2026-09-02|강의 녹취 · 2026-09-02 01:12:09]]

### 자료 범위와 한계

- 9월 16일은 자료 기반 추정 복습이며 녹음·정확한 당일 진도 증거가 없다. 이후 recap은 이를 소급 확정하지 않는다.
- 9월 21일10:13의 공유 관련 상충 표현은14:07의 독립 open 설명과 구분한다. 불명확한 register 설명을 보충 발화로 만들지 않는다.
- `fputs`·sprint 표기 오류와 stdio 의사코드의 element 반환·flush·error 처리 누락을 실제 API 계약으로 채택하지 않는다.
- Trace는 명시한 성공 가정이다. 강의 timing은 환경별 측정이고 기출 제공 답안은 정답 권위가 아니다.


---

[[courses/system_programming/units/permissions|← 이전: Permission·실행 identity·확장 metadata]] · [[courses/system_programming/units/index|단원 목차]] · [[courses/system_programming/units/memory-layout|다음: Process memory·alignment·호출의 실제 표현 →]]
