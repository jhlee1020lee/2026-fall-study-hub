---
title: "Dirtree의 순회·filter·출력 계약과 설계"
description: "Traversal·출력 폭·통계·pattern 문법을 구분하여 Dirtree 명세를 점검한다."
course: "system_programming"
unit_id: "dirtree"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["lab 2 input and output.pptx", "assign2_README.md", "lab 2 input and output_2b90a395.pptx"]
private_source_assets: ["assign2_README.md"]
source_lectures: ["courses/system_programming/lectures/2026-09-23-lecture-06"]
---

Dirtree 명세를 방문·표시·통계의 세 결정으로 나누어 읽자. 같은 tree라도 depth와 filter에 따라 포함 집합이 달라지므로 작은 예에서 계약을 검산하는 것이 핵심이다.

## Directory tree를 순회하는 것과 출력 계약

Dirtree는 directory의 entry를 재귀적으로 조사하고 metadata와 통계를 출력하는 프로그램이다. 단순히 이름을 나열하는 것보다 중요한 일은 **방문할 대상**, **보여 줄 대상**, **합계에 넣을 대상**을 구분하는 것이다. File metadata와 [permission](permissions.md), [pointer·storage 수명](objects-pointers.md)을 이 세 결정에 연결하면 명세를 읽기 쉬워진다. [[courses/system_programming/lectures/2026-09-23-lecture-06|2026-09-23 Dirtree 강의]]의 후반부는 이러한 계약을 소개한다.

Root argument가 없으면 `.`을 사용한다. Private 공식 README M018의 자료상 보충은 최대 64개의 root를 허용한다. `-d <depth>`는 깊이 제한, `-f <pattern>`은 이름 filter, `-h`는 help이며 `-d`와 `-f`는 독립 또는 함께 사용한다. 각 directory에서 `.`와 `..`를 제외하고 directory를 먼저, 각 범주 안에서 alphabetic order로 정렬한다. 자료는 이를 위한 `dirent_compare` helper를 안내한다. Root마다 header, entry tree, summary를 출력하고 root가 여러 개면 마지막 aggregate를 추가한다.

이 설명은 제공 명세와 일반 설계 원리를 읽는 것이며 완성된 traversal 또는 현재 과제 solution을 제공하지 않는다. 원문 README와 reference binary의 공개 링크도 만들지 않는다.

### 고정 폭은 의미뿐 아니라 bytes의 계약이다

M017 slides 6–8과 M018의 세부 format을 함께 읽으면 다음과 같다. Depth 한 단계마다 spaces 두 개를 쓰며 이 indentation도 path/name 폭에 포함한다.

| Field | 폭·정렬·제한 |
|---|---|
| Path/name | 54, 왼쪽 정렬, 초과하면 끝을 `...`로 표시 |
| User | 앞 8 bytes, 오른쪽 정렬 |
| Group | 앞 8 bytes, 왼쪽 정렬 |
| Size | 10, 오른쪽 정렬 |
| Disk blocks | 8, 오른쪽 정렬 |
| Type | 1 |
| Summary text | 68, 왼쪽 정렬, 초과하면 ellipsis |
| Summary total size / blocks | 각각 14 / 9, 오른쪽 정렬 |

구분자까지 포함한 자료의 전체 형식은 100-character line이다. Path/name이 정확히 54라면 잘라서는 안 되고 **초과할 때만** 자른다. UTF-8 filename의 byte 수와 화면 glyph 폭은 같지 않으며, source는 별도의 완성 display-column 알고리즘을 확정하지 않는다. Numeric field 폭 초과는 평가 제외지만 합계는 `int` 범위를 넘을 수 있어 충분한 integer type이 필요하다. Path overflow는 FAQ의 `MAX_PATH_LEN` 안내와 구분한다.

Type 표시는 regular file의 blank, directory `d`, symlink `l`, FIFO `f`, socket `s`다. Character·block device는 과제상 regular로 분류한다. 이 과제의 FIFO 표시는 `f`이며, 이를 Unix `ls`의 `p`로 바꾸면 안 된다. 출력 문자는 이 프로그램의 계약이다.

## 통계는 선택된 entry 집합에서 계산된다

Root 자체는 entry 합계에 넣지 않는다. 선택된 entry의 type별 count, byte size, disk blocks를 더하고 count가 1이면 singular, 0 또는 2 이상이면 plural을 사용한다. Blocks는 512-byte allocation 단위의 metadata 값이며 file byte size를 단순히 반올림해서 구하는 양이 아니다.

[system_programming:M017 slide 10](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx)의 두-root 예를 계산하면 다음과 같다.

| 대상 | Type counts | Bytes | Blocks |
|---|---|---:|---:|
| `subdir2` | 2 files, 2 links | 3086 | 16 |
| `subdir3` | 2 files, 1 pipe, 1 socket | 500 | 16 |
| Aggregate | 4 files, 0 directories, 2 links, 1 pipe, 1 socket | 3586 | 32 |

Entry 수는 `4+0+2+1+1=8`이며 root 두 개를 더하지 않는다. 원본 표에서는 root별 footer와 마지막 aggregate를 비교하면 합산 범위가 보인다. 별도의 source 예인 `9192+14=9206` bytes/16 blocks와 long-name 예 `256+8192+1000=9448` bytes/24 blocks는 같은 fixture가 아니다. README의 다른 demo는 4 files·3 directories·2 links·1 pipe·1 socket, 21497 bytes/56 blocks이며 확장 tree는 9 files, 25325 bytes/96 blocks다. 이 숫자들을 하나의 실행으로 합치지 않는다.

## Depth 제한과 filter는 다른 결정을 한다

Root의 depth는 0, 직접 child는 1이다. `-d`는 포함할 최대 entry depth로서 유효값은 1–20, 기본은 20이다. 제한 밖 entry는 표시, 순회, 통계 모두에서 제외한다. M017의 chain 예를 따라가면 다음과 같다.

| 범위 | 포함하는 대상 | 통계 |
|---|---|---|
| `-d 1` | `b` | 1 directory, 4096 bytes, 8 blocks |
| `-d 2` | `b`, `c`, file `f` | 2 directories, 1 file, 8192 bytes, 16 blocks |
| `-d 3` | 위 대상과 `d` | 3 directories, 1 file, 12288 bytes, 24 blocks |
| 전체 source 예 | `b,c,d,e`와 files 두 개 | 16384 bytes, 32 blocks |

Root를 1로 시작하면 한 level을 잘못 제외한다. [[courses/system_programming/transcripts/2026-09-23|2026-09-23 STT]] 01:11:03의 혼란스러운 수치 대신 명세의 root=0을 기준으로 계산한다. Source의 `# depth N` annotation은 설명용이며 실제 출력에 추가하는 항목이 아니다.

### Nonmatching ancestor도 방문할 수 있다

Filter는 case-sensitive한 basename의 연속 substring matching이다. `b`는 `abc` 안에서 맞지만 `/home/ta/abc/def`의 basename은 `def`이므로 parent path의 `abc`로 match시키지 않는다. Root는 filter하지 않는다.

Match한 entry는 상세 metadata와 통계에 포함한다. Match하지 않은 directory도 depth 범위 안이면 descendant를 찾기 위해 방문한다. Match한 descendant가 있으면 그 ancestor는 이름만 보여 주고 metadata·통계는 제외한다. 아무 descendant도 맞지 않으면 해당 nonmatching subtree를 생략한다. 따라서 ‘안 맞음’이 곧 ‘탐색 중단’은 아니다. STT 01:13분대–01:14:44 직전의 설명은 이 구분을 돕는다.

M018의 Implementation bullet에는 nonmatching directory를 방문하지 말라는 반대 지시가 있다. 여기서는 lecture, M017 slide 18, README의 formal rule과 상세 예가 지지하는 continued traversal을 따른다. 이 충돌이 instructor의 새 확인으로 해결된 것처럼 쓰지는 않는다.

Slides 20–21의 상세 결과는 lecture에서 건너뛴 materials-only 예다. `a?c`는 `aXc`, `abc`, `axc` 세 files를 남겨 3 bytes/24 blocks이고, `subdir1`은 이름만 남는다. `(ab)*c` 예는 `c`와 `xababcx` 안의 부분 문자열도 포함하여 6 files/6 bytes/48 blocks다. `b(ab)*c`는 `c`를 제외하여 5/5/40이다. M017의 제외 이름 `zxc`와 README의 `aZZc`는 서로 다른 fixture다.

## Pattern 문법의 단위와 경계

이 과제에서 `?`는 임의 character **정확히 하나**, `*`는 바로 앞 character 또는 group의 **0회 이상 반복**, `()`는 group이다. 일반 shell glob이나 다른 regex의 의미를 가져오지 않는다.

| Pattern | 맞는 구조의 예 |
|---|---|
| `a?c` | `abc`, `axc` |
| `ab*` | `a`, `ab`, `abb`, … |
| `(ab)*c` | `c`, `abc`, `ababc`, … |
| `a(bc)*d` | `ad`, `abcd`, `abcbcd`, … |
| `ab?(de)*f` | `abcf`, `abXf`, `abXdef`, `abXdedef` |

`a(bc)*d`가 `ad`를 허용하는 이유는 group이 0번 반복될 수 있기 때문이다. M018의 `abc?d*(ef)`는 `abcdef`에서 `?`가 `d` 하나를 소비하고 `d*`가 0번일 수 있다. `abcXddef`, `abcXef`도 해당 구조다. Partial matching이므로 전체 basename 길이와 pattern이 소비하는 길이가 같을 필요는 없다.

Shell이 먼저 metacharacter를 처리하지 않도록 command-line pattern은 quote하여 전달한다. 최대 길이는 종료 NUL을 포함한 64다. `?`, `*`, `(`, `)`를 filename의 literal 문자로 match시키는 경우는 평가 대상이 아니다. 다른 정규식에서 `?`가 optional을 뜻한다는 기억도 이 과제에는 적용하지 않는다.

### Invalid syntax와 평가 제외 complexity

빈 pattern, 빈 group `a()b`, 선행 `*abc`, 연속 `a**b`, 먼저 닫히는 `a)bc(`, 닫히지 않은 `(abc`는 invalid syntax다. `*`는 앞의 유효한 character 또는 group에 붙어야 한다. 따라서 `a*b`는 이 규칙상 invalid 예가 아니다. STT 01:15:40의 불명확한 pattern 발화를 반대 근거로 사용하지 않는다.

Group 안의 `*`를 포함한 `a(b*c)d`와 nested groups는 평가에 나오지 않는 complexity로 별도 제시된다. 이를 반드시 invalid로 처리해야 하는 목록과 섞지 않는다. 명시된 invalid pattern은 stderr에 `Invalid pattern syntax`만 출력하고 listing과 statistics 없이 종료한다. Permission denied, 없는 path, 순회 중 rename/remove, allocation failure 등은 M018에서 grading 제외로 안내하지만 일반 프로그램에서도 무시해도 된다는 뜻은 아니다. M017의 ‘Error and overflow handling 5’ rubric과 invalid-only 조항의 정확한 배점 대응은 확인되지 않았다.

### 시작 위치 탐색과 한 위치에서의 matching

M017 slide 25는 `*`만 지원하는 partial pseudocode다. 바깥 `match`는 basename의 시작 위치를 옮기며 시도하고, 안쪽 `submatch`는 특정 시작점에서 pattern이 이어지는지 판단한다. 원본에서 볼 핵심은 `*` 처리의 zero-repetition 시도와 그 아래 비어 있는 one-or-more branch다. 반복을 한 번 이상 소비하는 처리, `?`, grouping, 빈 suffix, 전체 종료·backtracking 조건이 완성되어 있지 않다. 이 hint를 완성 matcher로 사용하면 안 된다.

[EX:sp_2025_2_midterm_q02 p.5]는 시작 위치 탐색과 한 위치의 recursive matching을 나누는 관련 사고를 요구한다. 다만 그 시험의 `*`는 임의 문자 sequence를 0개 이상 허용하는 wildcard이고, Dirtree의 `*`는 **앞 항목 반복**이다. 시험은 처음 입력 pattern/string이 비어 있지 않다는 조건도 둔다. 전달할 수 있는 것은 suffix의 의미, zero-length 선택, 재귀 진행과 종료 조건을 따로 따지는 방법이다. Private skeleton의 빈칸이나 과제의 누락 branch를 여기서 완성하지 않는다.

## Storage 책임과 도구의 역할

설계에서는 root·option·header·summary·aggregate를 조정하는 역할과 directory entry 수집·정렬·filter·출력·재귀·닫기를 구분한다. Format, summary, entry 처리, pattern validation의 계약도 따로 읽는다. 이는 M018의 skeleton을 보기 전에 흐름을 설계하라는 자료상 조언에 해당한다.

Directory entry 수에는 상한이 없다. Depth가 20이어도 한 directory의 폭은 클 수 있고, recursive 함수의 큰 local array는 호출 깊이마다 stack을 차지한다. 따라서 ‘충분히 큰’ 고정 array가 모든 입력을 해결한다는 가정은 부적절하다. 폭, 깊이, 동적 storage의 확보·해제 시점을 함께 고려해야 한다. 이는 설계 제약이며 전체 저장·확장 알고리즘은 별도로 구현할 몫이다.

Handout의 `README`, `Makefile`, `src/dirtree.c`, reference, tools, documentation은 역할이 다르다. `make`는 build, `make clean`은 build 결과 정리이며 directory 구조가 Makefile과 맞아야 한다. `compare.sh`는 reference와 출력 비교, `gentree.sh`는 `*.tree` 설명에서 fixture 생성, `mksock`는 socket entry 생성 helper다. `mksock`는 수정하지 말라는 안내다. 기존 pipe/socket fixture가 남아 재생성과 충돌하는 FAQ는 환경 상태의 문제이며 여기서 생성·삭제 command를 실행한 것은 아니다.

함수들도 책임을 나눈다. `strcmp`는 비교, `strncpy`는 제한 복사, `strdup`은 독립 사본과 그에 따른 `free` 책임, `snprintf`는 bounded formatting, `opendir/readdir/closedir`는 순회, `stat/lstat`는 metadata, `getpwuid/getgrgid`는 이름 조회, `qsort`는 정렬이다. `strncpy`가 항상 NUL 종료를 보장하거나 `snprintf`의 결과가 항상 잘리지 않는 것은 아니다. `qsort`는 수집·filter·통계를 대신하지 않으며 이름이 특정 quicksort 구현을 보장하지도 않는다. 외부 regex library와 `scandir`는 명세상 금지다.

최신 제공 [system_programming:NM002 slide 32](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output_2b90a395.pptx)는 제출 항목을 `dirtree.c`, 확장자 없는 `readme`, `Makefile`, 실제 compilation history인 `history/`로 명시한다. M017·M018의 두 파일 목록은 이전 버전이다. 제공 마감은 10월 9일 21:00이며 최신 목록을 9월 23일의 발화로 소급하지 않는다. 예시 학번은 `YourID` 역할로만 읽고 압축 command의 연도 차이에서 별도 deadline을 만들지 않는다. NM002의 나머지 설명이 유지되었다고 해서 filter bullet과 error rubric의 충돌까지 해결된 것은 아니다.

## 핵심 정리

- Root는 depth 0이며 entry 통계에 넣지 않는다.
- Nonmatching directory도 범위 내 matching descendant를 찾기 위해 방문할 수 있다.
- 이름-only ancestor와 상세 출력·통계 대상은 다르다.
- `?`는 한 문자, `*`는 앞 항목의 0회 이상 반복이며 invalid 문법과 평가 제외 복잡도를 구분한다.
- Depth 제한은 directory 폭의 상한이 아니고 도구 실행은 계약별로 확인해야 한다.

## 확인·연습문제

### 개념 확인과 설명

#### 확인 Q01 · Root·option·정렬 계약

Root 생략·최대 root 수·`-d/-f/-h`의 역할, `.`/`..` 처리·정렬 순서, root 한 개와 여러 개의 출력 차이를 설명하라.

<details><summary>해설 보기</summary>

생략하면 현재 directory `.`, 자료상 최대 64 roots다. Depth/filter/help이며 depth와 filter는 함께 또는 따로 쓸 수 있다. Special entries는 제외하고 directories first, 각 범주 안 alphabetic order로 정렬한다. 각 root에는 header·entry tree·summary, 여러 root에는 마지막 aggregate도 있다. 64 제한은 README의 자료 보충이다.

**채점·점검 기준:** Default·세 option·정렬·aggregate 조건을 확인한다.

</details>

#### 확인 Q02 · 폭과 type marker

Indentation, path/user/group/size/blocks/type와 summary의 폭·정렬을 쓰라. Path가 정확히 54일 때, FIFO·device 표시, byte와 glyph·큰 합계는 어떻게 처리할 조건인가?

<details><summary>해설 보기</summary>

Depth당 2 spaces가 path 54에 포함되며 path는 왼쪽, 초과만 ellipsis다. User 앞 8 bytes 오른쪽, group 앞 8 왼쪽, size 10 오른쪽, blocks 8 오른쪽, type 1이다. Summary text 68 왼쪽·초과 ellipsis, size 14·blocks 9 오른쪽이며 구분자 포함 source 형식은 100이다. 정확히 54면 자르지 않는다. Regular blank,directory d,link l,FIFO f,socket s; char/block device는 과제상 regular다. UTF-8 bytes와 glyph 폭을 동일시하지 않고 numeric overflow 평가 제외와 합계의 int 초과 가능성을 구분한다.

**채점·점검 기준:** 모든 폭·정렬, 정확한 경계, FIFO f를 확인한다.

</details>

#### 확인 Q03 · 통계의 집합과 합산

두 root 결과가 2 files·2 links,3086 bytes·16 blocks와 2 files·1 pipe·1 socket,500 bytes·16 blocks다. Aggregate·총 entry 수·복수형을 구하라. 별도 fixture 9192+14와 256+8192+1000의 합, blocks와 byte size의 관계도 설명하라.

<details><summary>해설 보기</summary>

4 files,0 directories,2 links,1 pipe,1 socket으로 8 entries,3586 bytes,32 blocks다. Root 둘은 더하지 않는다. 1만 singular이고 0·2 이상은 plural이다. 별도 합은 9206과 9448 bytes이며 source의 16·24 blocks는 metadata다. 512-byte allocation 단위 blocks를 file size 반올림으로 계산하지 않는다. README의 21497/56 및 확장 25325/96도 다른 fixture여서 섞지 않는다.

**채점·점검 기준:** 8/3586/32와 root 제외, 별도 두 합, blocks 의미를 확인한다.

</details>

#### 확인 Q04 · Depth 경계

Root와 직접 child의 depth, 유효 `-d` 범위·default를 쓰라. Source chain의 -d 1/2/3에서 포함 대상·통계와 제외 entry 처리를 설명하라.

<details><summary>해설 보기</summary>

Root 0, child 1, 범위 1–20, default 20이다. -d1은 b만 1 directory/4096/8, -d2는 b,c,f로 2 directories·1 file/8192/16, -d3는 d 추가로 3 directories·1 file/12288/24다. 전체 source 예는 b,c,d,e와 두 files,16384/32다. 제한 밖은 방문·출력·통계에서 제외하고 root를 1로 세지 않는다. `# depth N`은 설명 annotation이다.

**채점·점검 기준:** Depth 기준과 세 포함 집합·통계를 검산한다.

</details>

#### 확인 Q05 · Nonmatching ancestor

Pattern b를 basename `def`와 path `/home/ta/abc/def`에 적용하면? 안 맞는 parent 아래 matching file이 있을 때 방문·표시·통계를 나누고 source 충돌을 설명하라. 자료의 a?c 및 두 repetition 예 통계는?

<details><summary>해설 보기</summary>

아니다. Case-sensitive basename substring만 검사한다. Root는 filter하지 않는다. Depth 내 parent는 방문하고 matching descendant가 있으면 이름만 표시하며 parent metadata·통계는 제외한다. Descendant도 없으면 subtree를 생략한다. Source의 중단 bullet은 lecture·formal rule·예와 충돌하므로 continued traversal을 따르되 미해결 충돌로 남긴다. Materials-only a?c는 3 files/3 bytes/24 blocks와 이름-only subdir1, (ab)*c는 6/6/48, b(ab)*c는 c를 제외해 5/5/40이다.

**채점·점검 기준:** 세 결정을 따로 적고 상세 예를 새 verified speech로 부르지 않는다.

</details>

#### 확인 Q06 · Pattern의 소비 단위

`?`, `*`, group의 의미를 쓰고 `ab*`, `(ab)*c`, `a(bc)*d`, `ab?(de)*f`, `abc?d*(ef)`의 zero-repeat 예를 설명하라. Quoting·64 제한·substring 범위는?

<details><summary>해설 보기</summary>

`?`는 정확히 한 임의 문자, `*`는 앞 character/group의 0회 이상 반복이다. 예로 `a`,`c`,`ad`,`abXf`가 각각 앞 네 pattern에 맞는다. 마지막은 `abcdef`에서 `?`가 `d`를 소비하고 `d*`가 0회, `(ef)`가 `ef`여서 맞으며 `abcXef`도 맞는다. 전체 basename을 소비할 필요 없는 연속 substring이다. Shell의 선처리를 막도록 quote하고 최대 64에는 NUL이 포함된다. Operator를 literal filename 문자로 맞추는 것은 평가 범위 밖이며 다른 regex의 optional `?`를 가져오지 않는다.

**채점·점검 기준:** 다섯 pattern 분해, zero-repeat와 NUL 포함 제한을 확인한다.

</details>

#### 확인 Q07 · Invalid와 제외된 complexity

빈 pattern, `a()b`, `*abc`, `a**b`, `a)bc(`, `(abc`, `a*b`, `a(b*c)d`와 nested group을 분류하라. Invalid일 때 stream·message·출력 종료 계약과 오류 rubric 한계는?

<details><summary>해설 보기</summary>

앞 여섯은 invalid다. a*b는 유효한 앞 항목 repetition이며 group 안 *와 nested group은 별도의 평가 제외 complexity다. Invalid는 stderr에 `Invalid pattern syntax`만 내고 listing·statistics 없이 종료한다. Permission·없는 path·concurrent 변경·allocation 실패가 grading 제외라고 일반 프로그램에서도 무시해도 되는 것은 아니다. Error/overflow 5 rubric과 invalid-only 조항의 정확한 배점 대응은 미해결이다.

**채점·점검 기준:** a*b를 invalid로 분류하지 않고 두 제외 범주를 구분한다.

</details>

#### 확인 Q08 · 시작점과 suffix

바깥 match와 안쪽 submatch의 질문은 무엇이 다른가? Star zero-repeat와 one-or-more의 역할, 제공 hint의 누락 범위를 설명하라.

<details><summary>해설 보기</summary>

바깥은 basename의 어느 시작점에서 맞는지, 안쪽은 고정 시작점에서 남은 pattern이 맞는지 판단한다. Zero-repeat는 앞 항목을 소비하지 않고 뒤 pattern을 시도하며 one-or-more는 앞 항목 소비와 이후 suffix 판정이 필요하다. Hint는 star-only partial pseudocode로 반복 branch·?·group·빈 suffix·완전한 종료/backtracking이 누락되어 전체 matcher가 아니다. 시험 Q2의 star는 임의 sequence wildcard여서 의미가 다르다.

**채점·점검 기준:** 두 책임과 누락된 부분을 설명하며 구현 빈칸을 완성하지 않는다.

</details>

#### 확인 Q09 · Depth와 memory 폭

Depth가 최대 20이면 recursive 함수에 큰 고정 entry array를 두어도 모든 입력을 처리하는가? Coordination·entry 처리·storage release 책임을 나누어 설명하라.

<details><summary>해설 보기</summary>

아니다. Directory 폭은 무제한이고 큰 local array는 활성 호출마다 stack에 누적된다. `main` 쪽 root/option/header/summary/aggregate 조정과 directory 열기·수집·정렬·filter·출력·재귀·닫기를 구분한다. Format·pattern validation도 별도 계약이다. 폭·깊이·allocation 양과 수명을 함께 계획하고 더 쓰지 않는 동적 storage를 해제해야 하며 depth만으로 총 memory의 작은 상한을 얻지 못한다.

**채점·점검 기준:** 폭/깊이를 분리하고 역할·해제 시점을 설명한다.

</details>

#### 확인 Q10 · 도구·API·자료 version

make/clean, compare.sh/gentree.sh/mksock와 주요 API 역할을 나누라. Copy/format의 함정·금지 API, 최신 제공 slide의 제출 목록과 옛 목록의 차이도 설명하라.

<details><summary>해설 보기</summary>

`make`는 build, clean은 build 결과 정리, compare는 reference 비교, gentree는 .tree fixture 생성, mksock은 수정 금지 socket helper다. strcmp 비교, strncpy 제한 복사(항상 NUL 종료 아님), strdup 사본/free, snprintf bounded format(잘릴 수 있음), opendir/readdir/closedir 순회, stat/lstat metadata, getpwuid/getgrgid 이름, qsort 정렬이다. 정렬은 수집/filter/통계를 대신하지 않으며 특정 quicksort 보장도 아니다. 외부 regex와 scandir는 금지다. 최신 제공 목록은 dirtree.c·확장자 없는 readme·Makefile·실제 compilation history/이며 옛 두-file 목록에 뒤 둘이 추가되었다. 제공 마감 10월9일 21:00을 유지하고 archive 예의 연도에서 새 마감을 만들지 않는다.

**채점·점검 기준:** 도구 목적·API 한계·추가된 두 제출 항목을 확인하고 실행 성공을 주장하지 않는다.

</details>

### 적용과 점검

#### 연습 P01 · Greedy 선택을 반례로 점검

**새로 만든 합성 연습.** [EX:sp_2025_2_midterm_q02 p.5]의 시작점 탐색과 recursive suffix 판단을 연결한다. 시험의 `*`는 임의 sequence wildcard지만 여기서는 본문처럼 **앞 group 반복**이다. 선수는 substring·group·zero-repeat이며 matcher code를 완성하지 않는다.

Basename `xabcdz`와 Dirtree pattern `a(bc)*bcd`를 생각하라. 첫 x에서 시작과 a에서 시작을 구분하고, a 뒤 group을 0번 또는 1번 소비하는 두 경우의 남은 문자와 pattern을 비교하라. '가능한 만큼 group을 먹고 실패하면 곧바로 전체 실패'가 맞는가?

<details><summary>해설 보기</summary>

`x` 위치는 첫 literal `a`부터 맞지 않는다. `a` 위치에서는 `a` 소비 후 남은 string이 bcdz다. Group 0번이면 남은 pattern bcd가 string prefix bcd에 맞고 trailing z는 substring 규칙으로 남을 수 있다. 1번이면 bc 소비 후 dz에 bcd를 맞추어야 하므로 실패한다. 따라서 1번의 실패를 전체 실패로 보면 유효한 0번 경로를 잃는다. 시작 위치 탐색과 한 위치의 repetition 선택을 분리해야 한다.

**채점·점검 기준:** 0회 성공·1회 실패의 suffix를 명시하고 시험과 Dirtree의 star 의미를 섞지 않는다.

</details>

### 복습 순서

Q01–Q05는 작은 tree에 depth·방문·출력·통계 네 열을 붙여 점검하라. Q06–Q08과 P01은 소비한 문자와 남은 suffix를 써서 풀고, 마지막에 Q09–Q10으로 storage와 도구의 책임을 설명하라.

## 출처

[[courses/system_programming/lectures/2026-09-23-lecture-06|2026-09-23 · 강의 노트]]

[lab 2 input and output.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx) — slide 5; slide 6; slide 9; slide 10, 실제 aggregate 표; slide 12; slide 15; slide 19; slide 23; slide 25; slide 28; slide 30

[[courses/system_programming/transcripts/2026-09-23|2026-09-23 · 보정 STT]] — 01:13:52–01:14:44

[lab 2 input and output_2b90a395.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output_2b90a395.pptx) — slide32; slide30

공식 README와 reference binary는 비공개다. Nonmatching directory 탐색 중단 bullet과 formal rule·발화·예의 충돌, error/overflow rubric과 invalid-only 조항의 대응은 해결되지 않았다. 상세 filter fixture와 최신 제공 slide의 최신 제출 목록은 자료 기반이며 9월23일 발화로 소급하지 않는다. Root-depth·pattern의 불명확한 발화를 복원하지 않는다. UTF-8 표시 폭 알고리즘과 완성 matcher·과제 구현은 제공하지 않는다. Source command와 도구는 설명이며 실제 실행·reference 비교 결과가 아니다.

아래 과거 시험 연결은 명시한 추론 요구에 한정한다. 제공 답안은 참고자료이며 독립 검증된 정답으로 간주하지 않고, 현재 시험 범위나 출제 빈도를 추정하지 않는다.
