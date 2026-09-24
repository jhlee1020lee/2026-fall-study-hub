---
title: "Dirtree의 순회·filter·출력 계약과 설계"
description: "Dirtree의 출력 계약·depth·filter·memory 책임을 검산한다."
course: "system_programming"
unit_id: "dirtree"
lang: "ko"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["lab 2 input and output.pptx", "assign2_README.md"]
private_source_assets: ["assign2_README.md"]
source_lectures: ["courses/system_programming/lectures/2026-09-23-lecture-06"]
---

Directory 순회와 출력·통계를 서로 다른 결정으로 나누어 검토한다. Depth와 pattern의 경계가 만날 때 어떤 entry를 방문하고 표시하고 세는지 추적한다.

## Directory tree의 순회와 출력 계약

Dirtree는 [[courses/system_programming/units/files-metadata|Directory entry와 metadata]]를 실제 프로그램의 여러 책임으로 연결하는 예다. 한 directory의 이름을 읽는 일만으로는 tree를 출력할 수 없다. Entry의 type을 조사하고, 순서를 정하고, 필요한 subdirectory로 내려가며, 표시할 정보와 합계를 함께 관리해야 한다. [Lab 2: Input and Output slides 2–11](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx)은 이 프로그램을 recursive traversal(재귀적 순회), formatting(형식 맞추기), statistics(통계)의 결합으로 소개한다.

Root argument가 없으면 current directory인 `.`을 대상으로 한다. Handout의 상세 명세에서는 root를 최대 64개까지 받는다. `-d <depth>`는 최대 깊이, `-f <pattern>`은 이름 filter, `-h`는 help를 뜻한다. `-d`와 `-f`는 각각 쓰거나 함께 쓸 수 있다. 여러 root를 처리할 때도 하나의 거대한 tree처럼 섞지 않고 root별 header, tree, footer와 summary를 만든 뒤 aggregate total(누적 합계)을 낸다.

각 directory 안에서는 `.`와 `..`를 제외한다. Directory를 먼저 두고, directory끼리와 나머지 entry끼리는 각각 alphabetical order로 정렬한다. 자료의 `dirent_compare` helper는 이러한 비교 책임을 위한 것이다. Directory가 먼저라는 규칙과 전체 이름의 단순 alphabetical order를 혼동하면 이름이 빠른 일반 file이 directory 앞에 나타나게 된다.

Entry가 symbolic link인지 directory인지 판별하는 방식도 중요하다. [[courses/system_programming/units/files-metadata|stat과 lstat]]의 구별을 떠올리면 link 자체의 type·size를 보여 주는 것과 link target의 정보를 보여 주는 것이 다르다는 것을 알 수 있다. 아래 계약은 link를 별도 type으로 다룬다. Target의 metadata를 무심코 가져와 link를 directory처럼 처리해서는 원하는 통계를 얻을 수 없다.

## Column width와 metadata 표시

### Indentation도 name field에 포함된다

Tree의 깊이는 한 단계마다 두 spaces로 나타낸다. 그러나 indentation을 column 밖에 덧붙이는 것은 아니다. Path/name의 54-character field **안에** indentation이 들어가므로, 깊어질수록 실제 이름에 남는 폭이 줄어든다. [Slides 6 and 11](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx)과 handout의 Output format·FAQ 2은 다음 계약을 정한다.

| Field | Width | 정렬·길이 처리 |
| --- | ---: | --- |
| Path/name | 54 | 왼쪽 정렬, 넘치면 잘라 끝을 `...`로 표시 |
| User | 8 | 앞 8 bytes를 쓰고 오른쪽 정렬 |
| Group | 8 | 앞 8 bytes를 쓰고 왼쪽 정렬 |
| Size | 10 | 오른쪽 정렬, byte 단위 |
| Blocks | 8 | 오른쪽 정렬 |
| Type | 1 | 지정된 한 문자 |
| Summary text | 68 | 왼쪽 정렬, 넘치면 끝을 `...`로 표시 |
| Total size | 14 | 오른쪽 정렬 |
| Total blocks | 9 | 오른쪽 정렬 |

User와 group 사이에는 `:`가 있다. Entry row의 field 폭 합은 89이고, 구분 spaces와 colon까지 포함한 원문의 line 형식은 100 characters다. 따라서 field 폭만 맞췄다고 전체 line이 맞는 것은 아니다. Summary row는 별도의 68·14·9 폭과 구분 간격을 사용한다. 정확히 최대 폭과 같은 이름이나 summary는 잘라서는 안 되고, **초과할 때만** ellipsis를 넣는다.

Handout은 UTF-8 filename을 대상으로 하고 user/group 제한에는 `printf("%.8s")`처럼 byte 제한을 적용하도록 설명한다. UTF-8의 byte 수와 화면에서 차지하는 glyph 폭은 같지 않을 수 있다. 이 설명을 근거로 새로운 Unicode display-column algorithm까지 과제의 확정 요구라고 만들지는 않는다. Field width와 문자열의 저장 길이를 구별하는 것이 먼저다.

Numeric field가 너무 커서 폭을 넘는 경우는 명세의 평가 범위 밖이다. 그러나 여러 entry의 size·blocks 합이 `int` 범위를 넘을 수 있다는 점은 별개다. 합계를 담을 때는 target에서 충분한 폭의 integer type을 선택해야 한다. 과제의 Linux target에서 제시된 `long` 계열을 다른 ABI에서도 무조건 같은 크기라고 가정하지 않는다.

### File type 문자는 도구의 계약이다

| Metadata상 종류 | Dirtree 출력 |
| --- | --- |
| Regular file | 빈칸 |
| Directory | `d` |
| Symbolic link | `l` |
| FIFO | `f` |
| Socket | `s` |
| Character/block device | 이 과제에서는 regular file로 분류 |

FIFO의 `f`는 Dirtree의 선택이다. `ls`의 type 표시에서 본 `p`를 그대로 옮기면 과제의 출력과 달라진다. Device를 regular로 분류하는 것도 이 과제의 단순화이며 Unix가 device와 regular file을 동일하게 정의한다는 뜻은 아니다. Name, ownership, byte size, allocated blocks, type은 서로 다른 metadata이므로 한 field로 다른 field를 추측하지 않아야 한다.

## Entry 통계와 root별 합계

Root는 traversal의 기준점이며 그 자체를 entry 합계에 넣지 않는다. 통계에 들어가는 것은 depth와 filter 조건에 따라 선택된 entry다. Type별 count, byte size 합, blocks 합을 구분해서 누적해야 한다. 영어 summary의 singular는 count가 정확히 1일 때만 쓰고, 0이나 2 이상이면 plural을 쓴다.

[Slide 10](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx)의 두-root 예는 합계의 단위를 구분하기 좋다.

| Root의 entry 구성 | Bytes | Blocks |
| --- | ---: | ---: |
| `subdir2`: 2 files, 2 links | 3086 | 16 |
| `subdir3`: 2 files, 1 pipe, 1 socket | 500 | 16 |
| 두 root의 합 | 3586 | 32 |

첫 root의 byte 합은 `1024 + 2048 + 8 + 6 = 3086`이고, 두 번째는 `200 + 300 + 0 + 0 = 500`이다. 합쳐서 4 files, 0 directories, 2 links, 1 pipe, 1 socket이다. Entry 수는 `4 + 0 + 2 + 1 + 1 = 8`이며 root 두 개를 다시 더하지 않는다. 자료의 aggregate에는 total entries가 있지만 root별 한 줄 summary에는 별도의 total-entry field를 추가하지 않는다.

Blocks는 자료에서 사용하는 512-byte allocation 단위다. Byte size를 512로 나누어 올림한 값과 같다고 가정해서는 안 된다. Sparse file이나 짧은 symlink는 logical size와 allocated storage의 차이를 드러낸다. [[courses/system_programming/units/files-metadata|File size와 allocated blocks]]의 구별이 여기서 합계 오류를 막아 준다.

자료에는 서로 다른 fixture(시험용 directory 구성)가 여럿 있다. 숫자가 다른 것은 하나의 실행 결과가 틀렸다는 뜻이 아니다.

| 별도 source example | 그 example 안의 계산·결과 |
| --- | --- |
| 초기 두-root example | `9192 + 14 = 9206` bytes, 16 blocks |
| 긴 이름의 세-file example | `256 + 8192 + 1000 = 9448` bytes, 24 blocks |
| Handout의 초기 전체 demo | 4 files, 3 directories, 2 links, 1 pipe, 1 socket; 21497 bytes, 56 blocks |
| Handout의 확장된 전체 demo | 9 files; 25325 bytes, 96 blocks |

마지막 example의 file이 늘어난 결과를 초기 demo의 count나 bytes와 섞으면 일관성이 깨진다. 이 값들은 제공된 example의 계산이며, 독자가 새로 만든 tree에서 보장되는 filesystem allocation 값은 아니다.

## Depth가 정하는 순회 범위

Root의 depth는 0, 바로 아래 child는 1이다. `-d`는 **포함할 최대 entry depth**이고 유효 범위는 1–20, 기본값은 20이다. 깊이 밖의 entry는 표시하지 않을 뿐 아니라 순회와 통계에서도 제외한다. 따라서 화면만 숨기고 deeper entry의 size를 더하는 구현은 계약과 다르다.

[Slides 12–15](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx)은 depth 규칙과 예제를 보여 준다. 전체 chain은 slide 12와 handout의 Option 1: Depth limit, Examples에 나오며, root `a` 아래 `b`, 그 아래 `c`, 이어 `d`와 `e`가 있는 모양이다. `b` 아래 depth 2에 file `f`가 하나 있고, `e` 아래 depth 5에도 file `f`가 하나 있다. 자료의 directory는 각각 4096 bytes와 8 blocks, 두 file은 0 bytes와 0 blocks다.

| 범위 | 포함되는 주요 entry | Files / directories | Bytes / blocks |
| --- | --- | ---: | ---: |
| `-d 1` | `b` | 0 / 1 | 4096 / 8 |
| `-d 2` | `b`, `c`, `b` 아래 `f` | 1 / 2 | 8192 / 16 |
| `-d 3` | 앞 범위에 `d` 추가 | 1 / 3 | 12288 / 24 |
| 자료의 전체 chain | `b,c,d,e`와 두 `f` | 2 / 4 | 16384 / 32 |

`-d 2`에서 `c`를 표시한다는 것은 `c`의 child까지 들어간다는 뜻이 아니다. Depth 2의 directory entry와 depth 3의 descendants는 구별된다. Source figure의 `# depth N` 표시는 설명용 annotation이며 프로그램 출력에 추가할 문자열이 아니다.

[[courses/system_programming/transcripts/2026-09-23|9월 23일 STT 01:11:03]]에는 root를 0으로 설명한 뒤 2라고 읽히는 모순된 수치가 남아 있다. 여기의 계산은 formal specification과 그림에 따라 root 0을 사용한다. 불명확한 발화를 새로 복원했다고 보지 않는다.

## Basename filter와 tree의 모양

### Match 여부와 directory 진입 여부를 분리한다

Filter는 full path가 아닌 basename(경로의 마지막 이름)에 적용되고 case-sensitive하다. Pattern `b`는 `abc` 안에서 맞지만, path `/home/ta/abc/def`의 basename `def`에는 `abc`가 없다. 상위 directory 이름까지 검색하면 같은 file을 어디에 옮겼느냐에 따라 원하지 않는 match가 생긴다.

Matching은 basename 안의 연속 substring을 찾는 partial match다. Match한 file, link, pipe, socket은 상세 정보와 통계에 포함한다. Match한 directory도 같은 방식으로 포함한다. 하지만 **directory 이름이 맞지 않아도 허용 depth 안에서는 descendants를 계속 찾는다.**

Non-matching directory에 matching descendant가 있으면 그 directory는 tree의 위치를 보여 주는 이름만 출력한다. User/group, size, blocks, type은 표시하지 않고 통계에도 더하지 않는다. Matching descendant가 전혀 없으면 그 non-matching subtree를 생략한다. Root에는 filter를 적용하지 않는다. 따라서 “출력에 이름이 보인다”와 “그 entry가 통계에 포함된다”는 항상 같은 조건이 아니다.

[Slide 18](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx)과 [[courses/system_programming/transcripts/2026-09-23|9월 23일 STT 01:13:52]]는 non-matching directory를 계속 순회하는 규칙을 설명한다. Handout의 Implementation 항목에는 이와 반대로 순회를 멈추라는 bullet도 있다. 여기서는 formal matching rule, 슬라이드, 강의가 일치하는 continued traversal을 따른다. 이 충돌은 filter와 traversal을 같은 predicate 하나로 처리하면 안 되는 이유와 직접 관계가 있다.

### Name-only ancestor와 선택된 통계

[Slides 20–21](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx)의 `a?c` example에서 선택되는 file은 `aXc`, `abc`, `axc`다. 이들을 담는 `subdir1`은 자기 이름으로 match하지 않아도 descendant를 보여 주기 위해 이름만 남는다. 세 file이 각각 1 byte와 8 blocks이므로 결과는 3 files, 3 bytes, 24 blocks이며 `subdir1`의 4096 bytes를 더하지 않는다. 제외되는 다른 이름은 슬라이드와 handout에서 서로 다르므로 두 fixture를 같은 목록이라고 읽지 않는다.

`(ab)*c` example은 `c`처럼 반복이 0회인 이름과 `xababcx` 내부의 substring도 받아 6 files, 6 bytes, 48 blocks가 된다. `b(ab)*c`는 시작의 `b`가 추가로 필요하므로 `c`를 제외해 5 files, 5 bytes, 40 blocks가 된다. `abc`도 내부 substring `bc`로 두 번째 pattern에 맞을 수 있다. 이름 전체와 pattern 길이가 같아야 한다고 가정하면 이 결과를 놓친다.

이 상세 example들은 자료를 통한 보충이다. [[courses/system_programming/transcripts/2026-09-23|9월 23일 STT 01:14:44]]에서는 operator를 설명한 뒤 일부 example을 건너뛰므로, 모든 계산을 그 시간에 실제로 풀이했다고 단정하지 않는다.

## Pattern language와 올바른 경계 판단

### 세 operator를 각각 해석한다

이 과제의 작은 pattern language는 일반 regex 전체도, shell wildcard 전체도 아니다.

| Pattern 요소 | 의미 | 자료에 따른 example |
| --- | --- | --- |
| `?` | 임의의 character 정확히 하나 | `a?c`는 `abc`와 `axc`에 맞는다. |
| `*` | 바로 앞 character 또는 group을 0회 이상 반복 | `ab*`는 `a`, `ab`, `abb`에 맞는다. |
| `()` | 여러 요소를 하나의 group으로 묶음 | `(ab)*c`는 `c`, `abc`, `ababc`에 맞는다. |

`a(bc)*d`에서는 `bc` 전체가 반복되므로 `ad`, `abcd`, `abcbcd`가 가능하다. `ab?(de)*f`에서는 `?`가 한 character를 반드시 소비하고 `de` group은 생략할 수 있어 `abcf`, `abXf`, `abXdef`, `abXdedef`가 가능하다.

Handout의 `abc?d*(ef)`도 요소별로 읽으면 혼동이 줄어든다. `abcdef`에서는 `?`가 `d`를 소비하고 `d*`는 0회이며 마지막 group이 `ef`를 소비한다. `abcXddef`에서는 `?`가 `X`, `d*`가 두 개의 `d`를 소비한다. `abcXef`에서도 `d*`를 생략할 수 있다.

Pattern을 command line에 전달할 때는 shell이 먼저 해석하지 않도록 quote한다. 최대 길이는 종료 NUL을 포함하여 64다. Operator 문자를 filename의 literal 문자로 match하는 경우는 명세의 평가 범위 밖이다. 이를 근거로 새로운 escape syntax나 다른 regex operator를 추가해서는 안 된다. 또한 [[courses/system_programming/units/state-machines|Integer DFA에서 사용한 regular expression]]의 optional 의미 `?`와 여기의 “아무 character 하나”는 서로 다른 표기 계약이다.

### Invalid syntax와 평가 범위 밖의 복잡성

Pattern을 정상적인 matching 입력으로 사용하려면 먼저 syntax를 판별해야 한다.

| Invalid pattern | 문제가 되는 구조 |
| --- | --- |
| 빈 pattern | element가 없다. |
| `a()b` | 빈 group이다. |
| `*abc` | `*` 앞에 반복할 element가 없다. |
| `a**b` | 허용하지 않는 연속 `*`다. |
| `a)bc(` | 닫는 괄호가 먼저 나온다. |
| `(abc` | group이 닫히지 않았다. |

`a*b`는 앞의 `a`를 0회 이상 반복하므로 이 규칙에서는 유효하다. [[courses/system_programming/transcripts/2026-09-23|9월 23일 STT 01:15:40]]의 해당 pattern 주변에는 잘못 인식되었거나 모순된 표현이 있다. 그것을 근거로 valid pattern을 invalid 목록에 넣지 않는다.

Group 안의 `*`, 예컨대 `a(b*c)d`나 nested group은 별도로 평가하지 않는 복잡성이다. “출제하지 않음”과 “반드시 invalid로 거부해야 함”은 같은 요구가 아니다. Invalid pattern이면 제공된 `panic()` 경로로 `stderr`에 `Invalid pattern syntax`만 출력하고 종료하며, directory listing이나 statistics를 함께 출력하지 않는다.

Handout은 permission denied, 없는 path, 순회 중 rename/remove, allocation failure 등의 다른 오류를 평가에서 제외한다. 이것은 일반적인 filesystem 프로그램에서 그 오류가 없거나 중요하지 않다는 뜻은 아니다. 슬라이드의 더 넓은 error/overflow 항목만으로 handout에 없는 세부 채점 규칙을 추측할 수도 없다.

### 시작 위치 탐색과 한 위치에서의 matching

[Slide 25](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx)의 hint는 `*`만 지원하는 **부분적인 pseudocode**다. 바깥 `match`는 basename의 시작 위치를 옮겨 가며 partial match를 찾고, `submatch`는 한 시작점에서 pattern이 이어지는지를 판단한다. 이 두 책임을 나누면 “어디서 시작하는가”와 “이 repetition을 몇 번 쓰는가”를 구별할 수 있다.

반복을 만나면 먼저 0회로 두고 나머지 pattern이 맞는지 보는 경로가 있다. 맞지 않으면 반복 대상 character를 더 소비하는 경로도 필요하다. 그런데 source의 한 번 이상 반복하는 부분은 comment 수준으로 비어 있고 `?`, group, 빈 suffix, 종료 및 backtracking의 모든 조건도 완성되어 있지 않다. 따라서 그 hint를 옮기는 것만으로 완성 matcher를 얻지는 못한다.

과거 [EX:sp_2025_2_midterm_q02 p.5]도 “어느 위치에서 시작할지 찾는 바깥 함수”와 “그 위치에서 맞추는 함수”의 역할을 비교하는 데 도움을 준다. **그 시험의 `*`는 임의의 문자열을 0개 이상 소비하는 wildcard이고, 현재 과제의 `*`는 앞 character/group의 반복이다.** 가져올 수 있는 것은 책임 분리와 0회 경로를 확인하는 reasoning이며, operator semantics나 완성된 함수 내용을 현재 과제에 그대로 옮길 수는 없다.

## Entry storage와 프로그램의 책임 분리

### Directory 폭과 recursion 깊이는 다른 자원이다

Handout은 skeleton을 보기 전에 흐름을 설계하도록 권한다. `main`의 책임은 option과 roots, root별 header·summary, 여러 root의 aggregate를 조정하는 것이다. Directory 처리 부분은 열기, entry 수집, 정렬, filter 판단과 출력, 필요한 recursive traversal, 닫기의 책임을 가진다. Formatting, statistics, pattern validation을 구별해 놓으면 어떤 입력 조건이 어떤 결과에 영향을 주는지 더 쉽게 추적할 수 있다.

한 directory의 entry 수에는 주어진 상한이 없다. 그래서 “충분히 큰” 고정 array를 선택했다고 모든 입력을 수용하는 것은 아니다. Recursive 함수의 큰 local array는 깊이가 늘 때마다 stack을 차지한다. 최대 depth 20은 directory **폭**이나 전체 allocation의 작은 상한을 뜻하지 않는다.

[[courses/system_programming/units/memory-layout|Stack과 heap의 배치]]를 떠올리면 storage의 수명도 분명해진다. 수집한 entry나 이름의 사본은 사용하는 동안 유효해야 하고 더 이상 필요 없으면 동적으로 할당한 memory를 해제해야 한다. 반대로 하위 호출이 아직 쓰는 storage를 먼저 해제해서도 안 된다. 이 문제는 sorting과 filtering을 어느 책임에서 수행하는지와 함께 설계해야 한다. 여기서는 책임과 수명 조건을 설명하며 과제 전체의 traversal 또는 matcher implementation을 제시하지 않는다.

### Library와 test 도구의 역할

다음 함수들은 handout과 [slides 27–30](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx)에서 안내하는 작업을 나누어 맡는다.

| 기능 | 함수·도구 | 주의할 경계 |
| --- | --- | --- |
| 문자열 비교 | `strcmp` | Case-sensitive name 비교와 정렬 규칙을 연결한다. |
| 길이를 제한한 복사 | `strncpy` | Source가 제한 길이 이상이면 NUL 종료를 보장하지 않는다. |
| 이름 사본의 수명 | `strdup`, `free` | 별도 사본의 소유권과 해제 시점을 관리한다. |
| 제한된 buffer에 형식 출력 | `snprintf` | Buffer에 맞춰 썼다는 것과 원하는 내용이 잘리지 않았다는 것은 다르다. |
| Directory 읽기 | `opendir`, `readdir`, `closedir` | Entry 수집과 자원 반환이 필요하다. |
| Metadata와 소유자 이름 | `stat`, `lstat`, `getpwuid`, `getgrgid` | Link 자체와 target, numeric ID와 이름을 구별한다. |
| 수집한 entry 정렬 | `qsort` | Traversal을 대신하지 않으며 이름이 특정 quicksort 구현을 보장하지 않는다. |

이 과제는 `scandir`와 외부 pattern-matching library, 예를 들어 `regex.h` 사용을 금지한다. 사용할 수 있는 library를 안다는 것과 과제의 filter를 그 library로 대체할 수 있다는 것은 별개다.

Handout의 `README.md`는 계약, `Makefile`은 build, `src/dirtree.c`는 skeleton, `doc/`는 Doxygen 관련 문서, `reference/`는 비교할 구현, `tools/`는 fixture 도구를 담는다. `make`와 `make clean`의 역할은 각각 build와 build 산출물 정리이며 directory 구조는 Makefile이 기대하는 구조와 맞아야 한다.

`gentree.sh`는 `*.tree` 설명으로 directory fixture를 만들고, `compare.sh`는 자신의 출력과 reference 출력을 비교한다. `mksock`는 socket entry를 만드는 helper이며 수정 대상이 아니다. 같은 fixture를 다시 생성할 때 기존 pipe/socket 때문에 충돌할 수 있다는 FAQ는 시험 환경도 상태를 가진다는 점을 보여 준다. 반면 출력이 한 번 같았다는 사실만으로 다른 depth, non-matching ancestor, 빈 반복, column 경계까지 모두 확인한 것은 아니다. Source의 fixture와 비교 도구는 각 계약을 구체적으로 확인하는 출발점이다.

## 핵심 정리

- Nonmatching ancestor도 matching descendant를 찾기 위해 방문한다.
- Name-only placeholder는 통계에 기여하지 않는다.
- 현재 *는 앞 element의 반복이며 과거 wildcard와 다르다.
- Metadata 기초는 [[courses/system_programming/units/files-metadata|file과 directory]], 수명은 [[courses/system_programming/units/memory-layout|memory layout]]과 연결한다.

## 확인·연습문제

### 개념 확인과 추론

#### 확인 Q01 · Root·정렬·출력 단위

Dirtree의 기본 root·최대 root 수와 -d/-f/-h를 설명하라. 여러 root와 directory 내부 정렬·symlink 분류는 어떻게 처리하는가?

<details><summary>해설 보기</summary>

Root 생략 시 .이고 최대64 roots다. -d는 depth, -f는 pattern, -h는 help이며 depth/filter를 함께 쓸 수 있다. 각 root는 별도 header·tree·footer·summary를 갖고 여러 root 뒤 aggregate를 더한다. 각 directory에서 .과..를 빼고 directory를 먼저, 각 그룹 안을 alphabetic으로 정렬한다. 전체 이름만 한꺼번에 정렬하면 안 된다. Symlink 자신의 type/size와 target의 metadata를 구별해야 link를 directory로 잘못 세지 않는다.

**채점·확인:** 64·독립 root 출력·directory 우선·link metadata를 확인한다.

</details>

#### 확인 Q02 · 출력 폭과 type

Name54/user8/group8/size 10/blocks 8/type 1의 alignment·overflow, summary fields와 indentation을 설명하라. Type 문자·UTF-8·큰 total의 한계는?

<details><summary>해설 보기</summary>

Name은 left·초과 시 ...이고 depth당2 spaces를54 안에 넣는다. User는 첫8 bytes를 right, group은 첫8을 left, size 10·blocks 8은 right, type 1이다. Width 합89에 colon·공백을 더해 entry line100이다. Summary text68 left·초과 ..., total size 14 right, total blocks 9 right는 별도 spacing이다. 정확히54/68이면 자르지 않는다. Type은 regular blank, directory d, link l, FIFO f, socket s이며 device는 이 과제에서 regular로 취급한다. UTF-8 byte와 표시 glyph 폭은 같지 않고 새 Unicode 알고리즘을 요구하지 않는다. Numeric field overflow는 제외되어도 누적값이 int를 넘을 수 있어 target에 충분한 type이 필요하다.

**채점·확인:** 폭·정렬·경계·FIFO f·byte/display·누적 type을 모두 확인한다.

</details>

#### 확인 Q03 · Summary의 단위

두 root가 각각2 files+2 links=3086 bytes/16 blocks, 2 files+pipe+socket=500/16이면 aggregate는? Root·plural·다른 fixture·blocks 계산은?

<details><summary>해설 보기</summary>

4 files, 0 directories, 2 links, 1 pipe, 1 socket로8 entries, 3586 bytes, 32 blocks다. 3086=1024+2048+8+6, 500=200+300+0+0이다. 두 root 자체를 더하지 않는다. Count 1만 singular, 0과2 이상은 plural이며 total entries는 aggregate field다. Blocks는 metadata의512-byte 단위 allocation count를 더하며 logical size를512로 나눠 올림하지 않는다. 다른 fixture의9206/16, 9448/24, 21497/56, 확장 demo25325/96은 각 입력에 속해 섞지 않는다.

**채점·확인:** 8/3586/32·root 제외·allocation 독립을 확인한다.

</details>

#### 확인 Q04 · Depth가 제외하는 것

Root a 아래 b, c, d, e chain과 b 밑 depth 2의 f, e 밑 depth 5의 f가 있다. Directory마다4096 bytes/8 blocks, file은0/0이다. `-d 1`/2/3/default의 결과와 경계를 설명하라.

<details><summary>해설 보기</summary>

Root는depth 0, 유효 limit 1..20, default 20이다. `-d 1`은 b:0 files/1 directory, 4096/8; `-d 2`는 b, c, f:1/2, 8192/16; `-d 3`는 여기에 d:1/3, 12288/24; 전체는2/4, 16384/32다. Limit을 넘으면 출력뿐 아니라 순회·통계에서도 제외한다. Depth 2의 c를 표시하는 것과 그 자식 방문은 다르다. 그림 #depth 문구는 출력이 아니다. 녹취의 root0 뒤 root2 상충은 명세의0으로 계산하되 불명확한 발화를 복구했다고 하지 않는다.

**채점·확인:** 세 boundary·전체 수치·순회/통계 제외를 확인한다.

</details>

#### 확인 Q05 · Filter와 traversal 분리

Filter는 path인가 basename인가? Nonmatching directory와 root·placeholder 통계 규칙을 설명하고 a?c 및 두 group-pattern fixture totals를 비교하라.

<details><summary>해설 보기</summary>

Case-sensitive basename partial match다. Nonmatching directory도 depth 안에서는 들어가 descendant를 찾는다. Match가 있으면 ancestor는 name-only placeholder로 남고 metadata·통계에는 기여하지 않으며 없으면 subtree를 생략한다. Root는 filter하지 않는다. a?c 예는 aXc, abc, axc의3 files/3 bytes/24 blocks다. (ab)*c는6/6/48, b(ab)*c는5/5/40이다. `abc`에서도 substring bc가 두 번째 pattern의 zero-repeat와 맞는다. Slide의 zxc와 handout의 aZZc는 다른 fixture 이름이며 섞지 않는다. Handout Implementation의 nonmatch에서 순회 중단 bullet은 정식 rule·slide·강의와 충돌하므로 그대로 채택하지 않는다.

**채점·확인:** Basename·계속 순회·placeholder0·3/6/5 totals·문서 충돌을 확인한다.

</details>

#### 확인 Q06 · 현재 pattern 문법

?, *, ()의 뜻을 설명하고 a(bc)*d, ab?(de)*f, abc?d*(ef)를 분해하라. 세 문자열 abcdef·abcXddef·abcXef는 왜 마지막 pattern에 맞는가?

<details><summary>해설 보기</summary>

?는 정확히 임의 한 문자, *는 바로 앞 문자/group0회 이상, ()는 grouping이다. a(bc)*d는 a+bc반복+d라 ad도 가능하다. ab?(de)*f는 ab+한 문자+de반복+f다. abc?d*(ef)는 abc+한 문자+d반복+ef다. `abcdef`는 ?가 d, d*0; abcXddef는 ?가 X, d*2; abcXef는 ?가 X, d*0이다. Shell 확장을 막도록 pattern을 quote한다. 최대64는 NUL 포함이어서 payload63 bytes다. Literal operator escape와 전체 regex 기능은 새로 도입하지 않는다.

**채점·확인:** 세 소비 경로·zero repeat·quote·63-byte 한계를 확인한다.

</details>

#### 확인 Q07 · Invalid와 제외 범위

Empty, a()b, *abc, a**b, a)bc(, (abc, a*b를 분류하라. a(b*c)d와 ((ab))는 반드시 reject인가? 오류 출력과 평가 범위는?

<details><summary>해설 보기</summary>

앞 여섯은 각각 empty pattern/group, 앞 element 없는 star, 중복 star, 잘못된/unmatched parentheses로 invalid다. `a*b`는 a 0회 이상 뒤 b이므로 valid다. Slides 22·24와 handout은 `a**b`를 invalid로 구분한다. 불명확하거나 모순된 `a*b` 표현은 9월 23일 STT 01:15:40에 있으며 slide의 invalid 표기가 아니다. Group 안 star와 nested group은 평가에서 제외된 복잡성이지 반드시 invalid로 reject하라는 요구가 아니다. Invalid이면 panic으로 stderr에 `Invalid pattern syntax`만 출력하고 listing·statistics 없이 종료한다. 다른 permission/path/race/allocation 오류는 자료의 평가 범위 밖이며 실제로 존재하지 않는다는 뜻도 숨은 규칙이 있다는 뜻도 아니다.

**채점·확인:** a*b valid·excluded≠invalid·stderr only를 확인한다.

</details>

#### 확인 Q08 · 두 matcher 책임

Outer match와 submatch/matchat를 분리하는 이유와 zero-repeat branch를 설명하라. Slide hint를 완성 구현으로 쓸 수 없는 이유, 과거 *와 현재 *의 차이는?

<details><summary>해설 보기</summary>

Outer match는 가능한 시작 위치를 옮기고 submatch는 하나의 위치에서 pattern 소비를 검사한다. Repeat의0회 branch는 input을 소비하지 않고 pattern의 나머지를 검사한다. 실패하면 양의 반복 경로도 필요하다. Slide hint는 star-only 일부이며 positive branch가 comment 수준이고 ?, group, empty suffix, 종료·backtracking을 모두 완성하지 않는다. [EX:sp_2025_2_midterm_q02 p.5]의 *는 임의 문자열0개 이상, 현재 *는 앞 element 반복이다. 역할 분리·zero branch만 전이하고 historical nonempty input 가정과 다른 문법을 유지한다.

**채점·확인:** 시작 위치/한 위치 검사·0회 소비·네 미완성 부분을 확인한다.

</details>

#### 확인 Q09 · Width와 lifetime

Depth 20 제한이 큰 고정 entry array를 정당화하는가? Recursive local storage, owned name copy의 수명과 main/순회/format/statistics 책임을 설명하라.

<details><summary>해설 보기</summary>

한 directory entry 수의 상한이 없어 depth 20으로 width를 제한할 수 없다. 큰 local array는 active recursive call마다 stack에 누적된다. Entry/name storage는 sort·출력·하위 호출이 쓰는 동안 유효해야 하고 owned copy는 마지막 사용 뒤 free한다. 필요한 ancestor storage를 일찍 지우면 안 된다. `main`은 옵션·roots·header·summary·aggregate를 조정하고 directory 처리는 open·collect·sort·filter·필요한 recursion·close를 담당한다. Format·통계·pattern validation을 분리하면 표시와 계산 조건을 검토하기 쉽다. 이것은 책임 설계이지 완성 traversal code가 아니다.

**채점·확인:** Width/depth·recursive stack·마지막 사용·역할 분리를 확인한다.

</details>

#### 확인 Q10 · 도구와 테스트의 범위

String·directory·metadata·sorting API와 README/Makefile/src/doc/reference/tools의 역할을 설명하라. 금지 API와 fixture 상태·비교 성공의 한계는?

<details><summary>해설 보기</summary>

strcmp는 비교, strncpy는 제한 복사지만 NUL 보장 아님, strdup/free는 소유 사본, snprintf는 bounded formatting이나 truncation 확인이 필요하다. `opendir/readdir/closedir`로 directory를 다루며 stat/lstat는 link follow 차이, getpwuid/getgrgid는 이름 조회, qsort는 수집한 entry 정렬이지 traversal이나 특정 quicksort 보장이 아니다. `scandir`와 regex.h 같은 외부 matcher는 금지다. README는 계약, Makefile은 build, src는 skeleton, doc은 Doxygen, reference는 비교 실행, tools는 fixture다. `gentree.sh`는 *.tree에서 생성, compare는 비교, mksock은 socket 생성 helper로 수정하지 않는다. Make clean/build는 build 상태를 다루고 pipe/socket 재생성 충돌은 fixture 상태 문제다. 한 비교 성공이 depth/filter/폭/zero-repeat 전부를 입증하지 않는다.

**채점·확인:** API별 한계·금지 기능·도구 역할·test 상태를 확인한다.

</details>

### 응용 연습

#### 연습 P01 · 문법 차이를 드러내는 witness

**새로 만든 합성 연습.** 현재 문법 pattern a*b를 basename zzb에 적용할 때 outer search와 zero-repeat branch를 설명하라. 같은 글자 pattern을 과거의 임의-sequence star 문법으로 읽으면 결과가 같은가? 완성 matcher를 작성하지 말고 소비 경로만 제시하라.

[EX:sp_2025_2_midterm_q02 p.5]의 outer/local 책임과 zero-consumption 점검을 서로 다른 문법을 판별하는 witness로 옮겼다. 선행: Q06·Q08. 과거 * semantics·nonempty 가정을 현재 요구사항으로 복사하지 않는다.

<details><summary>해설 보기</summary>

현재 outer search가 마지막 b 위치를 시도하면 a*를0회 소비하고 b를 맞춰 성공한다. 앞 z 위치에서 같은0회 branch는 b와 z가 달라 실패하므로 시작 위치 탐색도 필요하다. 과거 문법은 literal a 뒤 임의 sequence star, 마지막 b이므로 a가 전혀 없는 zzb에는 맞지 않는다. 두 입력은 nonempty라 과거 가정도 위반하지 않는다. 성공 사례만으로 ?, group, 종료 조건의 완성을 주장하지 않는다.

**채점·확인:** 현재 success·과거 failure·시작 위치·0회 경로를 설명한다.

</details>

#### 연습 P02 · Depth와 filter의 교차

**강의 기반 일반 연습.** 새 tree의 root 아래 nonmatching directory docs(depth 1)가 있고 그 안 aXc(depth 2, size 1, blocks 8)가 있다. Root의 다른 file은 abc(depth 1, size 5, blocks 8), aZZc(depth 1, size 9, blocks 8)다. Filter a?c에서 `-d 1`과`-d 2`의 표시·통계를 구하라.

현재 강의·handout 규칙을 결합한 새 일반 연습이다. 이 depth·filter·통계 결합에 직접 대응하는 indexed 기출 style 근거는 없다. 선행: Q02–Q05. 실제 reference 실행 결과가 아니다.

<details><summary>해설 보기</summary>

`-d 1`에서는 aXc를 방문하지 않아 docs subtree를 생략하고 abc만 상세 출력한다:1 file, 0 directories, 5 bytes, 8 blocks. `-d 2`에서는 docs를 name-only placeholder로 표시하고 aXc·abc를 상세 출력한다:2 files, 0 directories, 6 bytes, 16 blocks. `aZZc`는 ?가 두 글자를 소비할 수 없어 두 경우 모두 제외한다. Root와 placeholder는 합계에 넣지 않는다.

**채점·확인:** 1/5/8과2/6/16·placeholder·depth 제외를 확인한다.

</details>

### 복습 계획

Q01–Q05는 visit/display/count 세 칸과 field 폭으로 다시 계산한다. Q06–Q08은 소비 문자를 표시해 P01의 문법 차이를 확인한다. Q09–Q10의 lifetime·test 한계를 적은 뒤 P02로 두 option을 함께 점검한다.

## 출처

### 날짜별 강의 노트

- [[courses/system_programming/lectures/2026-09-23-lecture-06|2026-09-23 강의 노트]]

### 수업자료와 강의 구간

- [Lab 2: Input and Output slides 2–11](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx)
- [Slides 6 and 11](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx)
- [Slide 10](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx)
- [Slides 12–15](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx): depth 규칙과 예제. 전체 chain은 slide 12와 비공개 handout의 Option 1: Depth limit, Examples에 있다.
- [Slide 18](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx)
- [Slides 20–21](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx)
- [Slide 25](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx)
- [slides 27–30](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/lab.2.input.and.output.pptx)
- [[courses/system_programming/transcripts/2026-09-23|9월 23일 STT 01:11:03]]
- [[courses/system_programming/transcripts/2026-09-23|9월 23일 STT 01:13:52]]
- [[courses/system_programming/transcripts/2026-09-23|9월 23일 STT 01:14:44]]
- [[courses/system_programming/transcripts/2026-09-23|9월 23일 STT 01:15:40]]
- 9월 23일 Assignment 2 handout의 요구사항은 자료 보충으로 다룬다. 비공개 원문과 완성 구현의 공개 링크는 없다.

연결된 공개 자료는 slide deck이며, 이 자료들의 PDF 페이지 보기 링크는 제공되지 않았다. 녹취 시각은 일반 텍스트로 표시한다.

### 자료 범위와 한계

- 9월 23일 강의·slide와 비공개 handout 요구사항을 함께 참고하되 세부 자료 요구를 모두 발화로 단정하지 않는다. 완성 과제 구현이나 원문 handout을 제공하지 않는다.
- Root depth의0/2 불명확한 녹취는 유지하고 정식 rule의0을 사용한다.
- Nonmatch traversal을 중단하라는 Implementation bullet은 정식 rule·slide·강의와 충돌한다. Slides 22·24와 handout은 `a**b`를 invalid로 구분하며 `a*b`는 앞 element 반복 문법에 따라 valid다. 불명확하거나 모순된 `a*b` 표현은 9월 23일 STT 01:15:40에 있으며 slide의 invalid 표기가 아니다.
- Star-in-group·nested group은 제외 범위이지 자동 invalid 규칙이 아니다. Slide/handout의 다른 fixture 이름·합계를 섞지 않는다.
- Hint는 미완성 star-only 설명이다. 기출은 다른 star semantics와 nonempty 가정을 갖고 제공 답안은 정답 권위가 아니다. 새로운 question preview나 private answer를 제공하지 않는다.


---

[[courses/system_programming/units/memory-layout|← 이전: Process memory·alignment·호출의 실제 표현]] · [[courses/system_programming/units/index|단원 목차]]
