---
title: "Permission·실행 identity·확장 metadata"
description: "Permission bit, effective identity, ACL과 xattr의 역할·한계를 구별한다."
course: "system_programming"
unit_id: "permissions"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["03.IO.Unix.Filesystem.Concepts.pptx", "05.IO.Files.and.Directories_3d312c60.pptx"]
private_source_assets: []
source_lectures: ["courses/system_programming/lectures/2026-09-14-lecture-04", "courses/system_programming/lectures/2026-09-16-materials-io-review"]
---

접근 권한은 mode bit만이 아니라 대상 type과 실행 identity에 따라 해석한다. Namespace 변경·내용 접근·추가 metadata를 구분해 permission 판단의 근거를 적는다.

## Permission(접근 권한): 어떤 object에 어떤 동작을 허용하는가

`rwx`를 암기하는 것만으로는 파일 작업의 허용 여부를 판단하기 어렵다. 같은 `w`라도 file 내용 변경과 directory의 이름 변경은 다른 object에 대한 동작이다. 먼저 [[courses/system_programming/units/files-metadata|이름·inode·directory entry]]를 구분한 뒤 권한을 읽어야 한다.

기본 permission은 owner(소유자), group(그룹), other(그 밖의 사용자) 각각의 read·write·execute를 나타낸다.

| 대상 | `r` | `w` | `x` |
|---|---|---|---|
| Regular file | 내용 읽기 | 내용 쓰기 | 프로그램 실행 |
| Directory | entry 이름 목록 읽기 | entry 생성·삭제 등 namespace 변경 | directory를 통한 경로 탐색·entry 접근 |

Directory에서 실제 생성·삭제 등의 작업에는 `w`뿐 아니라 `x` 등 필요한 조건도 함께 갖추어져야 한다. 어떤 file의 내용에 write permission이 없다고 해서 그 이름을 directory에서 지울 수 없다고 결론 내리면 안 된다. 이름을 제거하는 작업은 해당 directory의 permission과 뒤에서 볼 sticky 규칙을 검사한다. [Unix filesystem slides 29–30](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)

### Octal mode와 bit 검사의 의미

Read, write, execute는 한 묶음에서 각각 4, 2, 1로 계산한다. `chmod 750`의 7은 `4+2+1`, 5는 `4+1`, 0은 아무 bit도 없는 상태다. 따라서 owner `rwx`, group `r-x`, other `---`가 된다. `chmod g+w`는 group write bit를 추가하는 symbolic 표현이다. 자료의 결과 화면에는 filename이 달라지는 오기가 있어 그 화면을 새로운 실행 결과처럼 읽지는 않는다.

C에서는 `st_mode`가 type과 permission을 함께 담는다. `S_ISREG(sb.st_mode)`는 regular file인지 판별하고, `sb.st_mode & S_IRUSR`는 owner-read bit를 확인한다. `S_IRWXU`의 `00700`은 owner의 세 permission bit를 묶은 mask다. File type 검사와 permission mask 검사는 같은 질문이 아니다. 이 `stat` 연결은 Files and Directories slide 6의 자료 설명이며 녹음이 없는 9월 16일의 정확한 진도를 뜻하지 않는다. [Files and Directories slide 6](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/05.IO.Files.and.Directories_3d312c60.pptx)

## Sticky bit와 filesystem 실행 정책

여러 사용자가 파일을 만드는 world-writable directory에서는 다른 사용자의 entry를 함부로 지우지 못하게 할 필요가 있다. Sticky bit(공유 directory의 삭제·이름 변경 제한)는 file owner, directory owner 또는 privileged process 등의 허용된 주체로 rename·delete를 제한한다. 그래서 `/tmp` 같은 공유 공간에서 보호 장치로 사용된다. File 내용을 모두 read-only로 만들지는 않는다.

`S_ISVTX`는 sticky, `S_IWOTH`는 other-write를 검사한다. 자료의 뒤쪽 요약에서 sticky를 위험한 설정들과 한데 묶은 표현은 slide 31의 보호 효과와 구분해서 읽어야 한다. [Unix filesystem slides 31–32](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)

또한 directory permission과 filesystem의 실행 정책은 다른 층이다. 자료는 world-writable 위치에 실행 파일을 놓을 수 있는 상황과 `fstatfs`의 `ST_NOEXEC` 검사를 연결한다. `ST_NOEXEC`는 직접 실행 제한, `ST_NOSUID`는 set-ID 효과 제한을 나타내는 filesystem flag다. 어느 한 bit만으로 모든 실행 경로나 권한 상승 가능성이 차단되었다고 증명할 수는 없다.

## Real identity와 effective identity

Process를 시작한 identity와 권한 판정에 쓰는 실행 identity를 구별하면 set-ID를 이해할 수 있다. Real UID/GID(실제 사용자·그룹 ID)는 기본적으로 시작한 주체를, effective UID/GID(유효 사용자·그룹 ID)는 실행 중 권한의 주체를 설명한다. `getuid`·`getgid`와 `geteuid`·`getegid`가 각각을 조회한다.

허용된 실행 조건에서 SUID(set-user-ID)는 effective user를 executable의 owner로 바꾸고 SGID(set-group-ID)는 effective group에 대응한다. File owner가 반드시 root인 것은 아니다. [Unix filesystem slides 33–34](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)

| Mode | 특별 bit | 자료에서 기대하는 효과 |
|---|---|---|
| `4755` | SUID | effective user가 file owner로 |
| `2755` | SGID | effective group이 file group으로 |
| `6755` | SUID와 SGID | 두 효과를 함께 요청 |

Slide 34의 예를 역할로 읽어 보자. 원래 사용자·그룹으로 실행하다가 executable owner를 다른 사용자·그룹으로 바꾸고 **4755만** 설정한다. 다시 실행하면 real user/group은 원래 주체이고 effective user만 file owner가 된다. Effective group은 원래 group이다. Group owner를 바꾸었다는 사실만으로 SGID가 설정되지는 않기 때문이다. `nosuid` 같은 정책은 이 효과를 제한할 수 있다.

Set-ID는 제한된 작업을 다른 권한으로 수행할 수 있게 하지만, 그 프로그램에 취약점이 있다면 더 높은 권한으로 문제가 발생할 수 있다. 기출 Q3(e)에 연결할 때도 필요한 권한의 주체와 프로그램이 노출하는 공격 표면을 함께 설명해야 한다. 모든 root-owned binary에 SUID가 필요하다는 결론이나 특정 시스템에서 모든 예시 도구가 같은 mode라는 결론은 성립하지 않는다. [EX:sp_2025_2_midterm_q03 p.8]

## UID를 이름으로 바꿀 때 생기는 storage 문제

UID와 GID는 숫자다. 화면에 이름을 표시하려면 `getpwuid`와 `getgrgid`로 해당 정보를 조회한다. 그런데 반환된 pointer가 library가 관리하는 재사용 storage를 가리킬 수 있다. 이 문제는 [[courses/system_programming/units/objects-pointers|pointer 값 복사와 대상 값 복사]]의 차이로 설명된다.

Real user 이름의 pointer를 저장하고 다음에 effective user를 조회한다고 하자. 두 조회가 같은 storage를 재사용하면 첫 pointer가 가리키는 bytes도 바뀐다. 두 변수가 서로 다른 주소값을 보관해야 한다는 것이 아니라, 첫 이름의 **독립 사본**이 필요하다는 문제다. 자료의 `whoami.c`는 `pw_name`과 `gr_name`을 `strdup`으로 복사하고 출력 후 `free`한다. [Unix filesystem slide 35](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)

이 흐름에서도 세 실패를 분리해야 한다. Lookup이 NULL을 반환할 수 있고, 복사 allocation이 실패할 수 있으며, 그 전에 local pointer가 초기화되지 않았을 수 있다. 원문의 실패 branch 생략을 그대로 둔 채 `user ? user : "n/a"`만 쓰면 초기화되지 않은 `user` 문제는 해결되지 않는다. Library 소유 pointer와 직접 만든 사본의 소유권을 구분하고, 자신이 확보한 사본만 해제해야 한다.

## Metadata 조건으로 잠재적 위험 설정 찾기

Unix filesystem slide 36의 예는 directory를 열고 `dirfd`를 얻어 entry마다 `fstatat(..., AT_SYMLINK_NOFOLLOW)`로 metadata를 조사한다. 마지막 symlink를 따라가지 않고 link 자체를 보는 선택이다. 의도한 판정은 다음 세 조건을 모두 만족하는 경우다.

1. Entry가 regular file이다.
2. `UID=0`과 SUID가 함께 있거나, `GID=0`과 SGID가 함께 있다.
3. 조사한 filesystem에 `ST_NOEXEC`와 `ST_NOSUID`가 모두 없다.

두 번째 조건은 `root UID AND SUID`와 `root GID AND SGID`의 OR다. SUID 하나만 있다는 이유로 root-user branch가 참이 되지 않는다. 세 번째 역시 둘 중 하나만 없는 것이 아니라 둘 다 없는지를 본다.

이 조건은 조사할 후보를 고르는 것이지 exploit의 존재를 증명하지 않는다. 예제의 `getNext`는 helper이며 표준 `readdir`의 다른 이름이라고 단정하지 않는다. Directory fd의 filesystem 정보를 확인한 것으로 각 entry가 다른 mount를 거치는 상황까지 모두 포괄한다고 보장할 수도 없다. 원문에는 괄호 누락과 오류 검사 생략이 있으므로 이 설명은 판정 논리의 해석이다. [Unix filesystem slides 28, 36](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)

## Extended ACL과 xattrs로 표현을 넓히기

Owner/group/other만으로 특정 사용자 한 명에게 예외 권한을 주기는 어렵다. Extended ACL(확장 접근 제어 목록)은 named-user entry 같은 더 세밀한 규칙을 표현한다. 자료는 `chmod 640` 이후 `setfacl -m u:USER:r file.txt`로 특정 사용자의 read entry를 추가·수정하고 `getfacl file.txt`로 확인한다. USER는 역할을 표시한 placeholder다.

표시된 `ls`에는 `+`가 붙고 ACL에는 named-user `r--`와 mask `r--`가 나타난다. Mask는 해당 ACL entry들의 실효 권한을 제한하므로 entry 하나만 보고 허용 여부를 결정하면 안 된다. `setfacl`은 변경하고 `getfacl`은 조회한다. [Unix filesystem slide 38](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)

### Xattr의 key와 value

Extended attributes(xattrs, 확장 속성)는 `namespace.attribute` 형태의 key로 metadata를 연결한다.

| Namespace | 자료의 용도 |
|---|---|
| `security` | SELinux 등 보안 module 정보 |
| `system` | kernel 관련 object |
| `trusted` | `CAP_SYS_ADMIN`으로 제한된 정보 |
| `user` | MIME type, encoding, checksum 등 사용자 metadata |

Value를 문자열로 설명하는 예가 많지만 모든 xattr value가 text string인 것은 아니다. 또 기본 mode bit의 세 분류와 extended ACL을 혼동해 “모든 POSIX ACL은 세 분류만 가능하다”고 일반화하지 않는다.

[[courses/system_programming/transcripts/2026-09-14|2026-09-14 STT 01:03:44–01:04:31]]은 checksum을 계산하여 attribute에 저장하고 key와 value를 조회하는 차이를 설명했다. 아래는 slide 39의 긴 checksum을 CHECKSUM으로 치환한 절차다.

```sh
md5sum file.txt
setfattr -n user.checksum.md5 -v CHECKSUM file.txt
getfattr file.txt
getfattr -n user.checksum.md5 file.txt
```

`user`가 namespace, `checksum.md5`가 그 안의 attribute 이름이다. 예에서 `getfattr file.txt`는 key 목록을 보여 주고, `-n`으로 특정 key를 지정하면 value까지 보여 준다. 계산 결과를 저장했다는 사실만으로 파일 변경 시 checksum이 자동 갱신되거나 파일의 진위가 보증되는 것은 아니다.

`setfattr -x user.checksum.md5 file.txt`로 삭제하면 목록에서 사라지고 지정 조회는 `No such attribute`가 되는 마지막 단계는 slide의 자료 보충이다. 그 삭제 과정까지 확인된 강의 발화로 바꾸지 않는다. Metadata가 access의 조건을 설명했다면, [[courses/system_programming/units/io-streams|열린 파일의 I/O 상태]]는 실제 전송 위치와 buffer가 어떻게 움직이는지를 설명한다.

## 핵심 정리

- Directory rwx는 file 내용 권한과 의미가 다르다.
- SUID·SGID는 별도 effective identity를 바꾸며 owner가 반드시 root는 아니다.
- Lookup의 borrowed pointer와 owned string copy를 구별한다.
- 접근 결과를 사용하는 다음 단계는 [[courses/system_programming/units/io-streams|I/O]]다.

## 확인·연습문제

### 개념 확인과 추론

#### 확인 Q01 · Mode와 directory permission

0750을 해석하고 g+w 뒤 값을 구하라. Regular file과 directory의 rwx·삭제 권한, S_ISREG와 bit 검사 차이는?

<details><summary>해설 보기</summary>

0750은 owner rwx, group r-x, others ---이며 g+w 뒤0770이다. File r/w는 내용 읽기/쓰기, x는 실행이다. Directory r은 name 나열, w는 namespace 변경, x는 search·경로 통과다. 삭제는 주로 parent directory 권한과 추가 제한을 따르므로 file의 w만 보면 안 된다. `S_ISREG(mode)`는 type, `mode&S_IRUSR`는 owner read, `S_IRWXU`는00700 permission mask다.

**채점·확인:** 0750→0770·directory x·type/permission을 구별한다.

</details>

#### 확인 Q02 · Sticky와 mount 제한

World-writable directory에서 sticky bit는 무엇을 제한하는가? S_ISVTX·S_IWOTH와 ST_NOEXEC·ST_NOSUID의 역할을 설명하라.

<details><summary>해설 보기</summary>

Sticky는 해당 directory 안 entry rename/delete를 file owner·directory owner·권한 있는 주체 등에 제한하며 file 내용 전체를 read-only로 만들지 않는다. `S_ISVTX`는 sticky, `S_IWOTH`는 others write를 확인한다. `ST_NOEXEC`는 직접 실행, `ST_NOSUID`는 set-ID 효과를 제한하는 mount 상태다. 이 flag들이 모든 해석·실행 경로나 공격을 막는다는 결론은 안 된다. 자료의 sticky 위험 요약과 삭제 제한 의미는 구별해 읽는다.

**채점·확인:** Namespace 제한과 내용 권한·mount 제한을 분리한다.

</details>

#### 확인 Q03 · Real/effective identity

Real/effective UID·GID와 조회 API는? 소유 user/group을 바꾼 binary mode 4755, 2755, 6755에서 실행 identity가 어떻게 달라지는가?

<details><summary>해설 보기</summary>

Real identity는 시작한 주체, effective identity는 접근 검사에 쓰이는 주체다. `getuid/geteuid/getgid/getegid`로 각각 조회한다. 4755는 SUID라 euid를 file owner로, 2755는 SGID라 egid를 file group으로, 6755는 둘 다 바꾼다. Owner/group을 모두 chown했어도4755만 있으면 egid까지 바뀌는 것은 아니다. Real identity는 유지된다. Mount nosuid 등 조건이 효과를 막을 수 있고 owner가 반드시 root도 아니며 script에 그대로 적용되는 보편 규칙도 아니다.

**채점·확인:** 네 API·세 mode·egid 오해·nosuid 조건을 확인한다.

</details>

#### 확인 Q04 · Lookup 결과의 수명

getpwuid/getgrgid의 반환 pointer를 저장하는 것과 strdup는 어떻게 다른가? Lookup 실패·allocation 실패·uninitialized pointer를 구별하라.

<details><summary>해설 보기</summary>

Lookup은 재사용될 수 있는 library storage를 가리킨다. Pointer 복사만 하면 값의 독립 사본이 아니어서 후속 호출 영향을 받을 수 있다. `strdup`는 문자열의 owned copy를 만들어 성공 확인 후 마지막 사용 뒤 free한다. Library storage 자체는 free하지 않는다. Lookup NULL, strdup NULL, 초기화되지 않은 pointer는 다른 상태다. 초기값도 없는 pointer에 ternary fallback을 붙인다고 유효해지지 않는다.

**채점·확인:** Borrowed/owned storage와 세 실패 상태를 구별한다.

</details>

#### 확인 Q05 · Permission 조건식 읽기

강의 checker가 찾으려는 조건을 괄호로 적고 fstatat·dirfd·fstatfs 역할을 설명하라. 왜 완성 보안 scanner가 아닌가?

<details><summary>해설 보기</summary>

의도는 regular AND ((uid==0 AND SUID) OR (gid==0 AND SGID)) AND NOT NOEXEC AND NOT NOSUID다. `fstatat`의 nofollow는 link 자체 조사, `dirfd`는 directory fd, `fstatfs`는 filesystem/mount 정보를 얻는다. Source의 괄호 누락과 error handling 미비를 그대로 정답 code로 읽지 않는다. `getNext`는 helper이지 readdir의 표준 별명이 아니다. 조건을 만족해도 취약성·공격 성공을 입증하지 않고, 만족하지 않아도 완전한 안전을 증명하지 않는다.

**채점·확인:** AND/OR grouping·nofollow·누락 한계를 확인한다.

</details>

#### 확인 Q06 · ACL과 xattr

ACL user read 추가/조회, xattr namespace와 checksum 저장·key/value 조회·삭제를 설명하라. Checksum은 언제 믿을 수 없는가?

<details><summary>해설 보기</summary>

`setfacl -m u:USER:r FILE`로 ACL을 추가하고 `getfacl FILE`로 확인한다. Mask가 effective permission을 제한할 수 있고 ls의 +가 확장 ACL을 알릴 수 있다. Xattr의 user·trusted·security·system namespace는 접근 의미가 다르며 값이 항상 text는 아니다. `md5sum FILE`로 값을 계산한 뒤 `setfattr -n user.checksum.md5 -v CHECKSUM FILE`로 저장한다. `getfattr FILE`의 key 목록과 `getfattr -n user.checksum.md5 FILE`의 value 조회는 다르다. `setfattr -x user.checksum.md5 FILE`는 삭제이며 이후 no-such-attribute는 자료 예시다. 녹취01:03:44–01:04:31은 계산·저장·조회 근거다. 파일 변경 후 stale할 수 있고 저장된 checksum만으로 진위·공격 방지를 보장하지 않는다.

**채점·확인:** ACL mask·key/value·삭제의 자료 범위·stale checksum을 확인한다.

</details>

### 응용 연습

#### 연습 P01 · Identity 변화와 위험 판단

**새로 만든 합성 연습.** Real/effective UID=1001, GID=1001인 process가 owner UID=2000, group=3000인 regular binary를 실행한다. Mode4755와6755, 그리고 nosuid mount를 비교하라. 해당 binary 수를 줄이는 이유를 root 단정 없이 설명하라.

[EX:sp_2025_2_midterm_q03 p.8] Q3(e)의 권한 상승 이유·위험 설명을 user/group·mount 비교로 옮겼다. 선행: Q02·Q03·Q05. 기존 binary 목록이나 script SUID 정책을 현재 사실로 전용하지 않는다. [[exam_questions/sp_2025_2_midterm_q03|허용된 관련 문항 미리보기]]

<details><summary>해설 보기</summary>

다른 억제 조건이 없으면4755는 euid 2000, egid 1001이고6755는 euid 2000, egid 3000이다. Real IDs는1001이다. Nosuid는 두 set-ID 효과를 억제하여 기존 effective IDs를 유지시킨다. 취약한 binary가 얻는 owner/group 권한으로 caller에게 없던 자원에 접근할 수 있으므로 권한을 가진 실행 경로를 줄이는 것이 의미 있다. Owner2000을 root라 부르거나 이 조건만으로 exploit 성공을 주장하지 않는다.

**채점·확인:** 각 mode의 두 effective ID와 real ID 유지·조건부 위험을 확인한다.

</details>

### 복습 계획

Q01–Q03은 file/directory·real/effective 축으로 표를 만든다. Q04–Q06은 저장소 수명과 관측 한계를 말로 설명한 뒤 P01에서 mode와 mount를 함께 바꿔 본다.

## 출처

### 날짜별 강의 노트

- [[courses/system_programming/lectures/2026-09-14-lecture-04|2026-09-14 강의 노트]]
- [[courses/system_programming/lectures/2026-09-16-materials-io-review|2026-09-16 연계 자료]]

### 수업자료와 강의 구간

- [Unix filesystem slides 29–30](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)
- [Files and Directories slide 6](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/05.IO.Files.and.Directories_3d312c60.pptx)
- [Unix filesystem slides 31–32](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)
- [Unix filesystem slides 33–34](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)
- [Unix filesystem slide 35](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)
- [Unix filesystem slides 28, 36](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)
- [Unix filesystem slide 38](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)
- [[courses/system_programming/transcripts/2026-09-14|2026-09-14 STT 01:03:44–01:04:31]]

연결된 공개 자료는 slide deck이며, 이 자료들의 PDF 페이지 보기 링크는 제공되지 않았다. 녹취 시각은 일반 텍스트로 표시한다.

### 자료 범위와 한계

- 9월 16일은 녹음 없는 추정 자료 복습이며 그날 정확한 발화·진도를 확인한 것이 아니다.
- Sticky 위험 요약과 checker의 누락된 괄호·error handling을 완성된 보안 도구로 해석하지 않는다.
- Xattr 계산·저장·조회는 9월 14일 녹취에 있지만 삭제와 그 이후 오류 예는 자료 범위다.
- 기출의 과거 binary 설정·script 동작을 현재 정책으로 옮기지 않는다. 제공 답안은 독립 검증된 권위가 아니다.


---

[[courses/system_programming/units/files-metadata|← 이전: Unix file·directory·inode와 metadata]] · [[courses/system_programming/units/index|단원 목차]] · [[courses/system_programming/units/io-streams|다음: Unix I/O·열린 파일 상태·stdio buffering →]]
