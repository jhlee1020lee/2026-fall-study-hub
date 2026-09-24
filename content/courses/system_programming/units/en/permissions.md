---
title: "Permissions, Execution Identity, and Extended Metadata"
description: "Distinguish permission bits, effective identity, ACLs and xattrs."
course: "system_programming"
unit_id: "permissions"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["03.IO.Unix.Filesystem.Concepts.pptx", "05.IO.Files.and.Directories_3d312c60.pptx"]
private_source_assets: []
source_lectures: ["courses/system_programming/lectures/en/2026-09-14-lecture-04", "courses/system_programming/lectures/en/2026-09-16-materials-io-review"]
---

Interpret access through object type and execution identity as well as mode bits. Separate namespace changes, content access and additional metadata when justifying permission decisions.

## Permissions: which operation on which object?

Memorizing `rwx` is not enough to decide whether a file operation is permitted. Writing file contents and modifying a directory's names act on different objects. Begin with the [[courses/system_programming/units/en/files-metadata|distinction between names, inodes, and directory entries]].

Basic permissions assign read, write, and execute bits to owner, group, and other.

| Target | `r` | `w` | `x` |
|---|---|---|---|
| Regular file | Read contents | Write contents | Execute a program |
| Directory | List entry names | Modify the namespace, including creating or deleting entries | Search through the directory and access entries by path |

Actual directory operations require the relevant combination of permissions, including search permission where needed. A file's lack of content-write permission does not alone establish that its name cannot be deleted. Removing that name depends on the containing directory's permissions and restrictions such as the sticky bit. [Unix filesystem slides 29–30](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)

### Octal modes and bit tests

Within one permission group, read, write, and execute contribute 4, 2, and 1. In `chmod 750`, seven is `4+2+1`, five is `4+1`, and zero sets none. The result is owner `rwx`, group `r-x`, and other `---`. `chmod g+w` symbolically adds group-write permission. The source's output contains a filename inconsistency; it is not treated as a newly verified execution.

In C, `st_mode` contains both type and permission information. `S_ISREG(sb.st_mode)` tests whether the object is a regular file, while `sb.st_mode & S_IRUSR` tests its owner-read bit. `S_IRWXU`, `00700`, combines the owner's three permission bits. Type classification and permission testing answer different questions. This connection to `stat` comes from Files and Directories slide 6; it does not establish the exact coverage of the unrecorded September 16 class. [Files and Directories slide 6](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/05.IO.Files.and.Directories_3d312c60.pptx)

## Sticky directories and filesystem execution policy

A world-writable directory allows multiple users to create entries. The sticky bit restricts renaming or deleting those entries to permitted actors such as the file owner, directory owner, or a privileged process. It therefore protects shared directories such as `/tmp`. It does not make all contained file data read-only.

`S_ISVTX` tests sticky status; `S_IWOTH` tests other-write permission. The later source summary groups sticky with potentially dangerous settings, but slide 31 describes its protective role. These statements must be distinguished. [Unix filesystem slides 31–32](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)

Directory permissions and filesystem execution policy are separate layers. The materials connect executable placement in a world-writable location with checking `ST_NOEXEC` through `fstatfs`. `ST_NOEXEC` concerns direct execution restrictions; `ST_NOSUID` concerns suppression of set-ID effects. One flag alone does not prove that all execution paths or privilege-escalation risks are blocked.

## Real and effective execution identities

Separate the identity that starts a process from the identity used in access decisions. Real UID/GID describe the originating user/group in the basic model; effective UID/GID describe the execution identity used for permissions. `getuid`/`getgid` and `geteuid`/`getegid` retrieve the respective values.

Under permitted execution conditions, SUID, set-user-ID, changes the effective user to the executable's owner. SGID, set-group-ID, corresponds to its group. The file owner need not be root. [Unix filesystem slides 33–34](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)

| Mode | Special bits | Effect illustrated in the materials |
|---|---|---|
| `4755` | SUID | Effective user becomes the file owner |
| `2755` | SGID | Effective group becomes the file group |
| `6755` | Both | Request both effects |

Read slide 34 in terms of roles. The executable is reassigned to a different owner and group, then receives **4755 only**. On execution, the real user/group remain those of the invoker; the effective user changes to the file owner, but the effective group remains the original group. Changing group ownership did not set SGID. Policies such as `nosuid` can suppress the set-ID effect.

Set-ID enables a bounded task to use another identity's privileges, but a vulnerable program can expose those privileges to misuse. Historical Q3(e) accordingly connects the identity receiving authority with the program's attack surface. It does not establish that every root-owned executable needs SUID or that named tools have identical modes on all systems. [EX:sp_2025_2_midterm_q03 p.8]

## Name lookups and reusable library storage

UIDs and GIDs are numbers. `getpwuid` and `getgrgid` obtain information used to display names. Their returned pointers can refer to storage managed and reused by the library. This is an application of the [[courses/system_programming/units/en/objects-pointers|difference between copying a pointer and copying its target]].

Suppose a program saves the pointer to the real user's name and then looks up the effective user. If the next lookup reuses the same storage, the bytes reached by the earlier pointer can change. The solution is not merely another pointer variable: it is an independent copy of the required name. The source's `whoami.c` duplicates `pw_name` and `gr_name` using `strdup`, prints them, and later calls `free`. [Unix filesystem slide 35](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)

Three failure cases remain distinct: lookup can return NULL, duplication can fail to allocate, and a local pointer may never have been initialized. The original's omitted failure branches are not repaired merely by `user ? user : "n/a"` if `user` itself is uninitialized. Track ownership: a library-owned pointer and an independently allocated copy are different, and only owned copies should be freed.

## Combining metadata conditions to identify possible risk

Unix filesystem slide 36 opens a directory, obtains `dirfd`, and examines entries with `fstatat(..., AT_SYMLINK_NOFOLLOW)`. This chooses the final link itself rather than following it. The intended candidate condition combines three requirements:

1. The entry is a regular file.
2. It has both root UID and SUID, or both root GID and SGID.
3. Neither `ST_NOEXEC` nor `ST_NOSUID` is set on the inspected filesystem.

The second requirement is an OR between two AND conditions. SUID alone does not satisfy the root-user branch. The third requires both flags to be absent, not merely one.

This selects configurations for scrutiny; it does not prove an exploit exists. `getNext` is an example helper, not an established alias for standard `readdir`. Inspecting the directory descriptor's filesystem also does not necessarily cover every entry reached through a different mount. The source omits error checks and a parenthesis, so the teaching here interprets the intended predicate rather than presenting a complete scanner implementation. [Unix filesystem slides 28, 36](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)

## Extended ACLs and xattrs

Owner/group/other bits cannot conveniently express every named-user exception. An extended Access Control List, ACL, can hold finer-grained entries. After `chmod 640`, the source uses `setfacl -m u:USER:r file.txt` to add or change a named user's read entry, then `getfacl file.txt` to inspect it. USER is a role placeholder.

The displayed `ls` output gains `+`, and the ACL shows a named-user `r--` entry with mask `r--`. The mask limits effective permissions for applicable entries, so one entry alone is insufficient to determine access. `setfacl` changes the ACL; `getfacl` reads it. [Unix filesystem slide 38](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)

### Attribute keys and values

Extended attributes, xattrs, associate metadata with keys of the form `namespace.attribute`.

| Namespace | Source example |
|---|---|
| `security` | Security-module information such as SELinux data |
| `system` | Kernel-related objects |
| `trusted` | Information restricted through `CAP_SYS_ADMIN` |
| `user` | User metadata such as MIME type, encoding, and checksums |

Many examples use strings, but not every attribute value is text. Likewise, do not confuse the three basic mode-bit classes with a claim that all POSIX ACLs are limited to those classes.

The [[courses/system_programming/transcripts/2026-09-14|September 14 lecture, 01:03:44–01:04:31]] explains calculating a checksum, storing it, and distinguishing a key listing from a value lookup. Here the long checksum on slide 39 is replaced by CHECKSUM.

```sh
md5sum file.txt
setfattr -n user.checksum.md5 -v CHECKSUM file.txt
getfattr file.txt
getfattr -n user.checksum.md5 file.txt
```

`user` is the namespace; `checksum.md5` is the attribute name within it. In this example, `getfattr file.txt` lists keys, whereas `-n` requests the named attribute's value. Storing a checksum does not automatically update it when the file changes or establish the file's authenticity.

The final deletion step, `setfattr -x user.checksum.md5 file.txt`, removes the attribute from the listing and causes a named lookup to report `No such attribute`. That walkthrough is a slide-only supplement, not newly established lecture speech. Having separated access conditions, [[courses/system_programming/units/en/io-streams|open-file I/O state]] next explains how positions and buffers move during actual transfers.

## Key Takeaways

- Directory rwx differs from file-content permissions.
- SUID/SGID affect separate effective identities; owners need not be root.
- Distinguish borrowed lookup pointers from owned string copies.
- Continue with [[courses/system_programming/units/en/io-streams|I/O]].

## Recall and Practice

### Recall and reasoning

#### Recall Q01 · Mode and directory permissions

Interpret0750 and add g+w. Compare file/directory rwx, deletion permission and S_ISREG versus a permission-bit test.

<details><summary>Show solution</summary>

0750 gives owner rwx, group r-x, others ---; adding g+w yields 0770. File r/w access content and x permits execution. Directory r lists names, w changes its namespace and x searches/traverses paths. Deletion principally concerns the parent and additional restrictions, not merely file-write permission. `S_ISREG(mode)` tests type, `mode&S_IRUSR` owner read, and `S_IRWXU` is00700.

**Check:** Check0750→0770, directory search and type/permission distinction.

</details>

#### Recall Q02 · Sticky and mount restrictions

What does sticky restrict in a world-writable directory? Explain S_ISVTX, S_IWOTH, ST_NOEXEC and ST_NOSUID.

<details><summary>Show solution</summary>

Sticky restricts entry rename/deletion to owners or privileged actors; it does not make contents read-only. `S_ISVTX` tests sticky and `S_IWOTH` others-write. `ST_NOEXEC` limits direct execution and `ST_NOSUID` set-ID effects on the mount. They do not prove every interpretation/execution route or attack blocked. Preserve the difference between the source’s broad risk summary and actual deletion restrictions.

**Check:** Separate namespace restrictions, content permissions and mount restrictions.

</details>

#### Recall Q03 · Real and effective identity

Explain real/effective UID/GID and query APIs. After changing a binary’s owner/group, compare modes4755, 2755 and 6755 on execution.

<details><summary>Show solution</summary>

Real identity identifies the initiating user/group; effective identity is used for access checks. Query with `getuid/geteuid/getgid/getegid`. 4755 sets euid to the file owner, 2755 sets egid to its group, 6755 applies both. Changing ownership/group and setting only 4755 does not also change egid. Real IDs remain. Mount nosuid and other conditions can suppress effects; owners need not be root, and scripts do not inherit a universal set-ID rule.

**Check:** Check four APIs, three modes, the egid pitfall and nosuid conditions.

</details>

#### Recall Q04 · Lookup-result lifetime

Compare retaining getpwuid/getgrgid pointers with strdup. Distinguish lookup failure, allocation failure and an uninitialized pointer.

<details><summary>Show solution</summary>

Lookup results may use reusable library storage. Copying the pointer does not make an independent value and later calls may affect it. `strdup` allocates an owned string copy: check success and free it after final use, not the library storage. Lookup NULL, strdup NULL and an uninitialized pointer are different states. A conditional fallback does not make reading an uninitialized pointer valid.

**Check:** Separate borrowed/owned storage and all three failure states.

</details>

#### Recall Q05 · Reading a permission predicate

Parenthesize the checker’s intended condition and explain fstatat, dirfd and fstatfs. Why is it not a complete security scanner?

<details><summary>Show solution</summary>

The intent is regular AND ((uid==0 AND SUID) OR (gid==0 AND SGID)) AND NOT NOEXEC AND NOT NOSUID. Nofollow fstatat inspects the link itself; dirfd obtains the directory fd; fstatfs obtains filesystem/mount information. Missing source parentheses and incomplete error handling are not certified code. `getNext` is a helper, not a standard alias for readdir. Matching proves neither vulnerability nor exploit success; nonmatching proves no complete safety.

**Check:** Check AND/OR grouping, nofollow and incompleteness.

</details>

#### Recall Q06 · ACLs and xattrs

Explain adding/querying ACL user-read access, xattr namespaces, and storing/listing/reading/deleting a checksum attribute. When is the checksum insufficient?

<details><summary>Show solution</summary>

Use `setfacl -m u:USER:r FILE` and inspect with `getfacl FILE`; a mask can limit effective access and ls + can indicate an extended ACL. User/trusted/security/system xattr namespaces differ in access semantics; values need not be text. Compute with `md5sum FILE`, then store using `setfattr -n user.checksum.md5 -v CHECKSUM FILE`. `getfattr FILE` lists keys; `getfattr -n user.checksum.md5 FILE` reads the value. `setfattr -x user.checksum.md5 FILE` deletes it; the later missing-attribute result is material-only. Transcript01:03:44–01:04:31 supports computation/storage/retrieval. A checksum may become stale and does not itself establish authenticity or prevent attacks.

**Check:** Check ACL masks, key/value distinction, material-only deletion and stale checksums.

</details>

### Practice

#### Practice P01 · Identity changes and risk

**Newly written synthetic practice.** A process with real/effective UID/GID 1001 executes a regular binary owned by UID 2000, group3000. Compare4755, 6755 and a nosuid mount. Explain why limiting these binaries can reduce risk without assuming root.

[EX:sp_2025_2_midterm_q03 p.8] Q3(e) contributes reasoning about acquired authority and risk, applied to user/group/mount cases. Prerequisites: Q02/Q03/Q05. Historical binary lists and script SUID policy are not imported as current facts. [[exam_questions/sp_2025_2_midterm_q03|Authorized related question preview]]

<details><summary>Show solution</summary>

Absent other suppression, 4755 yields euid 2000, egid 1001; 6755 yields euid 2000, egid 3000. Real IDs stay1001. Nosuid suppresses set-ID changes, retaining existing effective IDs. A vulnerable binary may misuse owner/group access unavailable to its caller, so reducing such execution paths reduces exposure. UID 2000 is not assumed root, and these conditions alone prove no exploit.

**Check:** Check both effective IDs per mode, retained real IDs and conditional risk.

</details>

### Review plan

Build a file/directory and real/effective table for Q01–Q03. Explain storage lifetime and observational limits in Q04–Q06, then vary both mode and mount in P01.

## Sources

### Dated lecture notes

- [[courses/system_programming/lectures/en/2026-09-14-lecture-04|2026-09-14 lecture notes]]
- [[courses/system_programming/lectures/en/2026-09-16-materials-io-review|2026-09-16 associated materials]]

### Materials and lecture passages

- [Unix filesystem slides 29–30](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)
- [Files and Directories slide 6](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/05.IO.Files.and.Directories_3d312c60.pptx)
- [Unix filesystem slides 31–32](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)
- [Unix filesystem slides 33–34](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)
- [Unix filesystem slide 35](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)
- [Unix filesystem slides 28, 36](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)
- [Unix filesystem slide 38](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)
- [[courses/system_programming/transcripts/2026-09-14|September 14 lecture, 01:03:44–01:04:31]]

The linked materials are the supplied public slide decks; no PDF page-cache link is available for these sources. Transcript timestamps are plain labels.

### Scope to retain

- September16 is an inferred materials review without a recording, not verified exact speech or coverage.
- The broad sticky-risk summary and checker’s missing parentheses/error handling do not establish a complete security tool.
- September14 speech supports xattr computation/storage/retrieval; deletion and its subsequent error example are material-only.
- Historical binary settings and script behavior are not current policy. Supplied answers are not independently verified authority.


---

[[courses/system_programming/units/en/files-metadata|← Previous: Unix Files, Directories, Inodes, and Metadata]] · [[courses/system_programming/units/index|Unit contents]] · [[courses/system_programming/units/en/io-streams|Next: Unix I/O, Open-File State, and Standard I/O Buffering →]]
