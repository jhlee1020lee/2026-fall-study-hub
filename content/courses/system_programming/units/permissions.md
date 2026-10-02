---
title: "Permission·실행 identity·확장 metadata"
description: "File·directory 권한, set-ID identity, ACL·xattr의 역할을 구분한다."
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

Permission을 판단할 때 object의 종류와 요청 동작부터 구분하자. 그 뒤 mode bit, 실행 identity, filesystem 정책을 차례로 확인하면 서로 다른 권한 문제를 섞지 않을 수 있다.

## Permission은 어떤 object의 어떤 동작을 허용하는가

파일을 읽는 권한과 파일 이름을 지우는 권한은 다른 문제다. Permission(접근 권한)을 읽을 때는 먼저 대상이 ordinary file인지 directory인지, 요청이 내용 접근인지 namespace 변경인지 구분해야 한다. File metadata의 `st_mode`에는 type과 permission 정보가 함께 있지만, `S_ISREG` 같은 type 판별 macro와 `S_IRUSR` 같은 permission mask는 다른 질문에 답한다.

Owner, group, other에 각각 read·write·execute bit가 주어진다. [system_programming:M001 slides 27–30](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)의 구분은 다음과 같다.

| Bit | Ordinary file | Directory |
|---|---|---|
| `r` | 내용을 읽기 | entry 이름 목록을 읽기 |
| `w` | 내용을 변경하기 | entry 생성·삭제 같은 namespace 변경 |
| `x` | 실행하기 | 경로를 search/traverse하고 entry에 접근하기 |

Directory의 실제 entry 조작에는 write와 search 등 필요한 조건을 함께 보아야 한다. Target file이 read-only여도 parent directory의 권한에 따라 그 이름을 삭제할 수 있는 상황이 있다. 반대로 directory에서 이름을 볼 수 있다고 그 이름을 통해 내용을 읽을 수 있는 것도 아니다.

`chmod g+w file`은 group write를 추가한다. `chmod 750 file`은 owner `rwx`, group `r-x`, other `---`로 설정한다. Octal 한 자리의 read=4, write=2, execute=1을 합하면 `7=4+2+1`, `5=4+1`, `0=0`이다. Owner 세 bit의 묶음 `S_IRWXU`는 `00700`이고, `(mode & S_IRUSR) != 0`은 owner read bit가 있는지 검사한다. 숫자 UID/GID는 이름 그 자체가 아니며 이름 조회는 뒤에서 별도로 다룬다.

[[courses/system_programming/lectures/2026-09-14-lecture-04|2026-09-14 permission·metadata 강의]]가 주된 연결점이다. M014 slide 6의 mode 검사도 보충 자료다. [[courses/system_programming/lectures/2026-09-16-materials-io-review|2026-09-16 inferred materials review]]에는 녹음이 없으므로 그날 정확히 어떤 설명이 발화되었는지를 이 보충에서 추론하지 않는다.

## Sticky bit와 filesystem 실행 정책

공유 directory에서는 여러 사용자가 entry를 만들 수 있어도 서로의 이름을 마음대로 지우게 해서는 곤란하다. Sticky bit는 directory 안의 rename·delete를 해당 file owner, directory owner, privileged process 등으로 제한한다. [[courses/system_programming/transcripts/2026-09-14|2026-09-14 STT]] 41:49–42:41의 `/tmp` 예는 이러한 보호 목적을 설명한다. Sticky bit가 모든 file 내용을 read-only로 만드는 것은 아니다.

`S_ISVTX`로 sticky, `S_IWOTH`로 other-write를 검사할 수 있다. World-writable directory에 executable을 둘 수 있는 상황은 내용 변경·실행과 관련된 위험도 따로 고려하게 한다. 자료의 `fstatfs`는 filesystem 정책을 조사한다. `ST_NOEXEC`는 실행 제한, `ST_NOSUID`는 set-ID 효과 제한과 관련되며 개별 file의 `rwx`와 다른 층이다. 한 bit가 있다고 모든 실행 경로나 보안 문제가 사라지는 것은 아니다. M001 slide 41의 포괄적인 위험 요약은 slide 31에서 설명한 sticky의 보호 효과와 구분해서 읽어야 한다.

## Real identity와 effective identity

Process를 시작한 identity와 접근 판정에 사용되는 실행 identity를 구분하면 set-ID bit를 이해할 수 있다. Real UID/GID는 기본 출발 identity를, effective UID/GID는 권한 판정의 실행 identity를 이해하는 출발점이다. `getuid()`/`getgid()`와 `geteuid()`/`getegid()`가 각각 조회한다.

SUID executable은 허용되는 실행 조건 아래 effective user를 file owner로 바꾸고, SGID는 effective group에 대응한다. 다음은 source의 bit 해석이며 실제 소유권이나 권한을 변경하는 작업 기록은 아니다.

| Mode | 보통 permission | 추가 효과 |
|---|---|---|
| `4755` | `755` | SUID |
| `2755` | `755` | SGID |
| `6755` | `755` | SUID와 SGID 모두 |

다른 사용자·group이 소유한 file에 `4755`만 설정한 자료 예에서는 real user가 유지되고 effective user만 file owner로 바뀐다. Effective group은 원래 group으로 남는다. File의 group owner가 다르다는 사실만으로 SGID가 설정되지는 않는다. `nosuid` 등 실행 정책은 set-ID 효과를 제한할 수 있다. Root 소유 binary가 모두 SUID여야 한다는 자료의 과도한 표현은 일반 규칙으로 채택하지 않는다.

이 구분을 적용하는 요구가 [EX:sp_2025_2_midterm_q03 p.8] Q3(e)다. 먼저 **file owner**, **invoking user**, **effective user**를 나누고, 그 다음 더 높은 실행 권한으로 동작하는 도구에 결함이 있을 때 영향이 커지는 이유를 설명한다. SUID를 곧바로 ‘항상 root가 된다’로 번역하면 owner 조건을 놓친다. 특정 binary의 실제 설정도 시스템마다 다를 수 있다. [[exam_questions/sp_2025_2_midterm_q03|기존 공개 question-only preview]]의 다른 I/O 소문항까지 이 permission 설명의 필수 내용으로 넓히지는 않는다.

## 이름 조회 결과의 수명

숫자 UID를 이름으로 표시하려면 `getpwuid`, GID를 이름으로 표시하려면 `getgrgid`를 사용한다. 이 함수들의 반환 pointer는 library가 관리하는 storage를 가리킬 수 있다. 첫 결과의 pointer만 저장한 채 다음 조회를 하면 같은 내부 storage가 갱신되어 앞서 얻은 이름도 바뀐 것처럼 보일 수 있다.

STT 53:51–55:01은 real/effective identity를 연이어 조회하는 예에서 이 문제를 설명한다. M001 slide 35의 `whoami.c`는 `pw_name`과 `gr_name`을 `strdup`하여 독립 사본으로 보존하고 사용 뒤 `free`한다. 이것은 [pointer와 pointee](objects-pointers.md)가 서로 다른 object라는 구분의 응용이다. Pointer 값 복사는 문자열 사본 생성이 아니다.

안전한 해석에는 세 실패 경로도 필요하다. 조회가 NULL을 반환할 수 있고, 복사 allocation이 실패할 수 있으며, local pointer가 초기화되지 않았을 수도 있다. `user ? user : "n/a"`는 이미 유효하게 초기화된 pointer를 검사하는 표현이지, 초기화하지 않은 `user`를 자동으로 안전하게 만드는 방법은 아니다. 자료의 생략된 분기를 갖춘 완성 도구로 읽으면 안 된다.

## Metadata predicate로 잠재적 위험을 좁히기

M001 slide 36은 directory를 열고 `dirfd`를 얻은 뒤 각 entry를 조사한다. `fstatat(..., AT_SYMLINK_NOFOLLOW)`는 symlink를 따라간 대상 대신 link 자체의 metadata를 볼 수 있게 한다. 예제의 `getNext`는 helper이며 표준 `readdir`의 다른 이름이라고 단정하지 않는다.

검사 조건을 자연어로 분해하면 다음과 같다. 우선 regular file이어야 한다. 그 file이 **root UID 소유이면서 SUID**, 또는 **root GID 소유이면서 SGID**여야 한다. 이어 filesystem에 `ST_NOEXEC`와 `ST_NOSUID`가 모두 없을 때 source는 잠재적으로 위험하다고 분류한다. Root 소유권만 있거나 SUID만 있다는 사실로 전체 predicate가 참이 되지는 않는다.

가령 root-owned regular file의 SUID가 꺼져 있으면 user 쪽 조건은 거짓이다. SUID가 켜져도 `ST_NOSUID`가 있으면 source의 마지막 필터를 통과하지 못한다. 이는 조건을 읽는 예이지 exploit 존재를 증명하는 검사가 아니다. Source에는 괄호·error check가 생략되어 있고 directory fd의 filesystem 검사만으로 다른 mount를 거치는 모든 entry까지 포괄한다고 보장할 수 없다.

## Extended ACL과 xattr의 다른 역할

기본 owner/group/other mode보다 세분된 접근 제어가 필요하면 extended ACL을 사용할 수 있다. 다음 source 예에서 `USER`는 개인을 식별하지 않는 placeholder다.

```sh
chmod 640 file.txt
setfacl -m u:USER:r file.txt
getfacl file.txt
```

Named-user read entry를 추가·수정한 뒤 `getfacl`로 확인한다. 자료에서는 `ls` 표시에 `+`, ACL에 named-user `r--`와 mask `r--`가 보인다. ACL mask가 실효 권한을 제한하므로 entry 하나만 보고 전체 권한을 결정하면 안 된다. 기본 mode의 세 분류와 extended ACL을 구분해야 ‘POSIX ACL이 세 분류에만 한정된다’는 과도한 요약을 피할 수 있다.

Extended attributes(xattrs)는 `namespace.attribute` 형태의 key에 추가 metadata를 연결한다. Source의 `security`는 SELinux 등 보안 정보, `system`은 kernel 관련 정보, `trusted`는 `CAP_SYS_ADMIN`으로 제한되는 정보, `user`는 MIME·encoding·checksum의 예다. Value가 반드시 text string인 것은 아니다.

STT 01:03:44–01:04:31의 checksum 예는 계산, 저장, key/value 조회를 구분한다.

```sh
md5sum file.txt
setfattr -n user.checksum.md5 -v CHECKSUM file.txt
getfattr file.txt
getfattr -n user.checksum.md5 file.txt
```

첫 줄의 계산 결과 문자열을 두 번째 줄의 `CHECKSUM` 자리에 넣는 역할 예다. `user`는 namespace이고 `checksum.md5`는 그 안의 attribute 이름이다. 일반 조회는 source 예에서 key 이름을 보여 주고, `-n` 조회는 지정 key의 value를 읽는다. 불명확한 checksum 발화는 복원하지 않는다.

M001 slide 39의 자료상 추가 단계는 `setfattr -x user.checksum.md5 file.txt`로 제거하는 것이다. 제거 뒤 key 목록에서 사라지고 지정 조회가 `No such attribute`가 되는 walkthrough는 materials-only 보충이다. 저장한 digest가 file 변경 때 자동 갱신되거나 file의 진위를 보증하는 것은 아니다. 현재 내용으로 다시 계산해 비교하는 일과 metadata 변경 권한을 신뢰하는 일은 별도 문제다.

## 핵심 정리

- File 내용 변경과 directory entry 삭제는 다른 동작이다.
- Sticky, SUID/SGID, noexec/nosuid는 서로 다른 조건을 제한한다.
- UID/GID 숫자와 표시 이름, 반환 pointer와 문자열 사본을 구분한다.
- Metadata predicate는 조건에 따른 위험 가능성 분류이며 안전 인증이 아니다.
- ACL은 접근 제어, xattr은 추가 metadata이며 저장 digest는 자동 검증이 아니다.

## 확인·연습문제

### 개념 확인과 설명

#### 확인 Q01 · File과 directory의 rwx

File/directory에서 r·w·x의 의미를 비교하라. Read-only file의 이름 삭제가 가능할 수 있는 이유, `chmod g+w`, `chmod 750`, `S_IRWXU`, `S_ISREG`와 `S_IRUSR`의 차이는?

<details><summary>해설 보기</summary>

File은 내용 읽기/쓰기/실행, directory는 이름 목록 읽기/entry 생성·삭제/search·traverse다. Entry 조작에는 parent의 write와 search 및 sticky 등 조건이 필요하므로 target 내용의 write bit만으로 삭제를 판단하지 않는다. `g+w`는 group write 추가, 750은 rwx/r-x/---이며 4+2+1의 octal 합이다. `S_IRWXU=00700`은 owner bit 묶음, `S_ISREG`는 type, `mode & S_IRUSR`는 owner read 검사다.

**채점·점검 기준:** 여섯 의미와 namespace/content 구분, type/permission 검사를 확인한다.

</details>

#### 확인 Q02 · 공유 directory의 제한

Sticky인 world-writable directory에서 모든 파일이 read-only가 되는가? `S_ISVTX`, `S_IWOTH`, `ST_NOEXEC`, `ST_NOSUID`가 각각 무엇을 검사하는가?

<details><summary>해설 보기</summary>

아니다. Sticky는 주로 rename/delete를 file owner·directory owner·privileged process 등의 허용 경우로 제한한다. 내용 쓰기 권한은 별도로 본다. 앞 두 mask는 sticky와 other-write, 뒤 두 flag는 filesystem의 실행 제한과 set-ID 효과 제한이다. Directory가 world-writable이거나 sticky라는 사실 하나로 전체 실행 경로의 안전을 증명할 수 없다.

**채점·점검 기준:** Sticky의 대상 동작과 file mode/filesystem 정책의 층을 구분한다.

</details>

#### 확인 Q03 · 누구의 권한으로 실행되는가

Caller user/group이 A/G이고 executable owner/group이 B/H다. 허용되는 set-ID 실행을 가정할 때 4755·2755·6755의 effective user/group과 real identity는? 조회 함수와 nosuid 한정도 설명하라.

<details><summary>해설 보기</summary>

각각 effective B/G, A/H, B/H이고 real A/G는 유지된다. 4는 SUID, 2는 SGID, 6은 둘의 합이다. `getuid/getgid`는 real, `geteuid/getegid`는 effective 조회다. File group이 H라는 사실만으로 4755에서 group이 바뀌지 않는다. `nosuid` 등 정책은 효과를 제한하며 SUID는 항상 root가 아니라 file owner로의 변경이다.

**채점·점검 기준:** 세 identity 쌍·네 함수·group owner와 SGID의 차이를 확인한다.

</details>

#### 확인 Q04 · 조회 pointer의 수명

Real user 이름의 `pw_name` pointer만 보관한 뒤 effective user를 조회하면 왜 이름이 바뀐 것처럼 보일 수 있는가? `strdup`, NULL, allocation 실패, `user ? user : "n/a"`를 함께 설명하라.

<details><summary>해설 보기</summary>

`getpwuid/getgrgid` 결과는 다음 조회에 재사용되는 library storage일 수 있어 pointer 복사만으로 문자열이 보존되지 않는다. 성공한 조회 결과를 `strdup`하면 독립 문자 사본이 생기지만 allocation 확인과 free가 필요하다. 조회 NULL은 member 접근 전에 처리하고 사본 생성 실패도 따로 처리한다. 조건식은 이미 초기화된 pointer의 NULL 여부를 검사할 뿐 미초기화 user를 안전하게 만들지 않는다.

**채점·점검 기준:** Pointer/문자 사본 구별과 세 실패 경로를 각각 설명한다.

</details>

#### 확인 Q05 · 위험 가능성 predicate

자료의 scanner 조건을 type, owner/set-ID, filesystem flag 순으로 풀어 쓰라. Root-owned regular file에 SUID가 없거나 nosuid가 있으면? `AT_SYMLINK_NOFOLLOW`, `getNext`, error·mount 한정도 설명하라.

<details><summary>해설 보기</summary>

Regular이면서 `(root UID && SUID) || (root GID && SGID)`이고 noexec·nosuid가 모두 없어야 source 필터를 통과한다. SUID 없는 root ownership은 user 분기를 만족하지 않고 nosuid가 있으면 마지막 필터를 통과하지 못한다. NOFOLLOW는 link 자체 metadata를 조사하며 getNext는 source helper다. 괄호·error check 생략과 다른 mount 가능성 때문에 완성 scanner나 exploit/안전 증명이 아니다.

**채점·점검 기준:** AND/OR 묶음과 두 반례, source의 한계를 함께 적는다.

</details>

#### 확인 Q06 · ACL과 namespace

`chmod 640` 뒤 named USER의 read ACL을 추가하고 확인할 command는? `+`와 mask는 무엇인가? xattr의 security/system/trusted/user와 ACL을 구별하라.

<details><summary>해설 보기</summary>

`setfacl -m u:USER:r file.txt`와 `getfacl file.txt`다. `+`는 확장 ACL 표시이고 mask는 관련 entry의 실효 권한을 제한할 수 있다. ACL은 기본 owner/group/other보다 세분된 접근 제어다. Xattr은 추가 metadata로 security는 보안 정보, system은 kernel 관련, trusted는 CAP_SYS_ADMIN 제한, user는 MIME·encoding·checksum 예다. Value가 반드시 문자열일 필요는 없다.

**채점·점검 기준:** 두 command, mask 효과, 접근 제어와 추가 metadata의 차이를 확인한다.

</details>

#### 확인 Q07 · Checksum 계산·저장·조회·삭제

`user.checksum.md5`의 namespace와 이름을 나누고 계산→저장→key 목록→value→삭제 command를 설명하라. 삭제 단계의 근거와 저장값의 신뢰 한계는?

<details><summary>해설 보기</summary>

user가 namespace, checksum.md5가 이름이다. `md5sum file.txt` 결과를 `setfattr -n user.checksum.md5 -v CHECKSUM file.txt`로 저장한다. Source 예의 `getfattr file.txt`는 key 목록, `getfattr -n user.checksum.md5 file.txt`는 value, `setfattr -x user.checksum.md5 file.txt`는 제거다. 뒤에는 목록에서 없어지고 지정 조회가 No such attribute가 된다. 계산·저장·조회는 9월14일 발화도 있지만 삭제 walkthrough는 slide-only다. File 변경 때 자동 갱신되지 않고 현재 내용 재계산·비교와 metadata 변경 권한의 신뢰가 별도다.

**채점·점검 기준:** Key/value 조회 차이, 삭제의 자료 한정, 자동 갱신 부재를 확인한다.

</details>

### 적용과 점검

#### 연습 P01 · Identity와 삭제 권한을 분리하기

**새로 만든 합성 연습.** [EX:sp_2025_2_midterm_q03 p.8] Q3(e)의 실행 identity와 높은 권한의 결함 영향을 옮긴다. 선수는 본문의 rwx·set-ID·sticky이며 실제 binary 설정이나 exploit 구현은 필요 없다.

A/G가 B/H 소유의 4755 regular executable을 실행한다. Set-ID가 허용되고 B는 A보다 높은 권한을 가진다고 가정한다. (a) Real/effective identity는? (b) Executable이 세계 쓰기 가능 sticky directory에 있다는 이유만으로 내부 결함의 영향이 줄어드는가? (c) A가 소유하지 않은 다른 entry를 삭제할 권한을 executable의 mode만 보고 판단할 수 있는가?

<details><summary>해설 보기</summary>

(a) Real A/G, effective B/G다. (b) 아니다. Sticky는 directory rename/delete를 제한하며 프로그램이 effective B로 수행하는 잘못된 동작을 일반적으로 차단하지 않는다. 결함은 B의 더 큰 권한 범위에 영향을 줄 수 있다. (c) 아니다. Parent write/search와 sticky의 owner 조건 및 실제 동작 identity를 따로 확인해야 한다. 높은 권한 가능성과 삭제 허용 여부는 다른 판단이다.

**채점·점검 기준:** B/G와 sticky의 좁은 역할, 누락된 directory 조건을 명시한다.

</details>

### 복습 순서

Q01–Q03은 object/operation/identity 세 열로 정리하고 P01에 적용하라. Q04는 pointer와 사본의 수명을 그린 뒤 Q06–Q07의 command를 목적별로 가리고 다시 맞춰 보라.

## 출처

[[courses/system_programming/lectures/2026-09-14-lecture-04|2026-09-14 · 강의 노트]]

[[courses/system_programming/lectures/2026-09-16-materials-io-review|2026-09-16 · 자료 기반 추정 복습]]

[03.IO.Unix.Filesystem.Concepts.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx) — slide 29; slide 31; slide 34; slide 35; slide 36; slide 37; slide 39; slide 38

[05.IO.Files.and.Directories_3d312c60.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/05.IO.Files.and.Directories_3d312c60.pptx) — slide 6

[[courses/system_programming/transcripts/2026-09-14|2026-09-14 · 보정 STT]] — 01:03:44, 01:04:31

9월16일 노트는 녹음 없는 자료 기반 추정이며 정확한 발화 진도가 아니다. Checksum 삭제 walkthrough는 slide-only이고 불명확한 checksum 값은 복원하지 않는다. Source의 sticky 위험 요약, 모든 root binary의 SUID 주장, 기본 mode와 extended ACL의 혼동은 한정해 읽는다. 예제 scanner는 error check·괄호·mount 범위가 불완전하며 실제 시스템의 안전 상태를 판정하지 않는다. 과거 시험의 특정 binary 설정은 현재 환경 사실로 옮기지 않는다.

아래 과거 시험 연결은 명시한 추론 요구에 한정한다. 제공 답안은 참고자료이며 독립 검증된 정답으로 간주하지 않고, 현재 시험 범위나 출제 빈도를 추정하지 않는다.

[[exam_questions/sp_2025_2_midterm_q03|2025-2 중간 Q3 · 파일과 I/O (기존 미리보기)]]
