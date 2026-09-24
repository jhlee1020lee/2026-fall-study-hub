---
title: "Unix Files, Directories, Inodes, and Metadata"
description: "Connect file types, links, mounts and stat/directory APIs."
course: "system_programming"
unit_id: "files-metadata"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["03.IO.Unix.Filesystem.Concepts.pptx", "04.IO.Direct.and.Buffered.IO_8e725857.pptx", "05.IO.Files.and.Directories_3d312c60.pptx"]
private_source_assets: []
source_lectures: ["courses/system_programming/lectures/en/2026-09-09-lecture-03", "courses/system_programming/lectures/en/2026-09-14-lecture-04", "courses/system_programming/lectures/en/2026-09-16-materials-io-review", "courses/system_programming/lectures/en/2026-09-21-lecture-05"]
---

Separate file bytes, names, inodes and open handles. Check path interpretation and units before drawing conclusions from metadata.

## Unix files: separating contents, names, and metadata

A regular file can be modeled as an m-byte sequence `B0, B1, …, Bm-1`. In the alphabet example, offset zero contains `a` and offset 25 contains `z`. Interpreting those bytes as text, an image, or object code is the application's responsibility. “Text file” and “regular file” classify different aspects. [Unix filesystem slides 4–7](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)

A directory contains entries connecting names to inode numbers, or i-numbers. An inode, an index node, represents metadata such as permissions, ownership, timestamps, and size. A model that requires one filename inside every inode cannot explain multiple names for the same file. Receiving metadata in a C structure such as `struct stat` also depends on the [[courses/system_programming/units/en/objects-pointers|object and pointer distinction]].

### Different targets behind a file interface

The Unix file interface extends beyond stored regular files.

| Target | Source examples | Important distinction |
|---|---|---|
| Regular file | Text, image, object file | Application interprets the byte format |
| Directory | Name-to-inode entries | Enumerating entries differs from reading ordinary file contents |
| Character device | `/dev/tty`, `/dev/input/mice` | Representative stream-style interaction |
| Block device | `/dev/sda` | Representative block-oriented storage access |
| Virtual filesystem | `/proc`, `/sys` | File-like presentation of kernel state and configuration |
| IPC endpoint | FIFO, socket | Data exchange between processes |

A named object is not necessarily a regular file stored on disk. For example, `/proc` can expose current kernel state. The stream/block comparison is useful, but it does not prove that every character device universally lacks seeking or buffering. An inode number is also not simply a physical disk address obtained through one arithmetic formula.

## Process isolation, FIFOs, and sockets

Processes execute in their own address spaces. A pointer's number in one process is not a default mechanism for directly accessing another process's private memory. The [[courses/system_programming/transcripts/2026-09-09|September 9 lecture, 49:54–55:05]] uses this isolation to motivate explicit inter-process communication, or IPC.

A FIFO, a named pipe, provides a unidirectional channel: bytes written by one process are read in the same order by another. Its directory name does not imply that the payload accumulates on disk like a regular file. In the source example, `mkfifo` creates `abc`; a consumer, `gzip`, reads it and writes compressed output to `abc.gz`, while a producer writes document contents into the FIFO. Opening or reading can wait for a peer or data, making execution order and background execution relevant. The source's `&;` punctuation is not adopted as a valid complete shell script. [Unix filesystem slide 8](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)

Unix domain sockets support local, bidirectional IPC. Network sockets offer a related I/O interface, but a Unix domain socket is not itself a remote network endpoint. Obtaining a file descriptor for a FIFO or socket does not make it arbitrarily seekable. [[courses/system_programming/units/en/memory-layout|Process memory]] further explains why equal address numbers do not establish shared storage.

## Mount points and one directory tree

Unix resolves paths under a single root, `/`. Attaching another filesystem uses a directory as a mount point. The mounted contents cover the underlying directory; they do not simply merge with it.

The source first creates `extern/hello`. Mounting tmpfs at `extern` hides that original `hello` and reveals the mounted filesystem. After a new file named `extern` is created there, unmounting reveals the original `hello` again. **Hidden is not deleted.** The separate vboxsf host-share mount and the tmpfs mount are different connections. The example must not be reinterpreted as a bind mount of the existing `/dev/shm` directory. [Unix filesystem slides 11–13](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)

In this example, `echo hello` includes a newline and produces six bytes, whereas `printf hello` produces five. File-size reasoning must count bytes that are not visible as ordinary letters.

### Temporary names and mount options

At [[courses/system_programming/transcripts/2026-09-14|September 14, 06:55]], the lecturer explains that processes creating temporary files in a shared namespace such as `/tmp` can choose colliding names. They need a procedure that obtains and uses a noncolliding name. The spoken API name is unclear, so no particular function name is reconstructed.

The tmpfs example at [[courses/system_programming/transcripts/2026-09-14|September 14, 08:32]] illustrates volatile, memory-backed storage whose contents do not survive reboot. That property is distinct from a disk-backed directory being temporarily hidden by a mount. It does not establish that every `/tmp` is tmpfs or that every `/var/tmp` has the same cleanup policy.

| Mount option | Role described in the materials |
|---|---|
| `ro` | Restrict writes |
| `noatime` | Restrict access-time updates |
| `relatime` | Summarized policy using atime's relationship to mtime/ctime |
| `noexec` | Restrict direct execution |
| `nosuid` | Suppress set-ID effects |
| `nodev` | Restrict interpretation of device files |
| `size` | Example capacity limit |
| `iocharset` | Example filename-encoding setting |

Per-file permissions and filesystem policy operate at different layers. No single option proves that every execution or security issue is resolved.

## What hard and symbolic links share

A hard link is another directory entry referring to **the same inode**. If `hello.txt` and `helloworld.txt` are hard links, appending through either name changes the contents seen through both. The data and metadata were not independently copied. Removing one name decreases the link count; the other name still reaches the inode.

A symbolic link has its own inode and stores a target pathname. It can remain as a dangling link after that target disappears. Hard links cannot cross filesystem boundaries, and creating ordinary directory hard links is restricted. A symlink can name a directory or a target in another filesystem. [Unix filesystem slides 15–18](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)

Consequently, a hard-link count concerns names that reference the same inode; creating a symlink does not increment the target inode's hard-link count. Historical Q3(a–b) demands this reasoning: identify the inode reached by each reference before counting names. [EX:sp_2025_2_midterm_q03 p.7]

### Reading ls and directory link counts

The first character of `ls -l` output, `- d l p s c b`, identifies a regular file, directory, symlink, FIFO, socket, character device, or block device. It is followed by permissions, hard-link count, owner/group, byte size, mtime, and name. `-a` includes dot-prefixed names and `.`/`..`; `-d` displays the directory itself instead of listing its contents. A leading dot hides a name from ordinary listings; it is not an access-control mechanism.

In the traditional directory model, a `sample` directory containing `dir1` and `dir2` has this count:

`parent's sample entry 1 + sample/. 1 + dir1/.. 1 + dir2/.. 1 = 4`

Each leaf directory has two references: its name in its parent and its own `.`. `sample/..` points to the parent of `sample`, so it does not add to `sample`'s count. This explains the source's `2 + number of immediate subdirectories` rule. It is a conventional filesystem example, not a universal promise for every filesystem. [Unix filesystem slides 19–21](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)

## Filesystem Hierarchy Standard: reading a path's role

The Filesystem Hierarchy Standard, FHS, is a convention for understanding where executables, configuration, and changing state belong. Use it to find roles rather than memorize every directory. The supplied organization below can differ in actual placement and links across distributions. [Unix filesystem slides 22–27](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)

| Path | Role |
|---|---|
| `/bin`, `/sbin` | Essential execution and administration tools |
| `/boot` | Boot loader and kernel |
| `/dev` | Device interfaces |
| `/etc` | System-wide configuration |
| `/home`, `/root` | Ordinary users' homes and the administrator's home |
| `/lib`, `/lib64` | Libraries for essential tools |
| `/media`, `/mnt` | Mount points |
| `/opt` | Additional application packages |
| `/proc`, `/sys` | Process, kernel, and device information/configuration |
| `/run` | Runtime state |
| `/tmp`, `/var/tmp` | Temporary storage; retention policy is separate |
| `/usr` | Additional executables and shared data hierarchy |
| `/var` | Changing state and data |

Within `/usr`, `bin`/`sbin` contain tools, `include` C headers, `lib` libraries, `libexec` helper executables, `local` local installations, `share` shared data, and `src` source code. Within `/var`, `cache`, `lib`, `lock`, `log`, `mail`, `run`, `spool`, and `tmp` represent caches, persistent application state, locks, logs, mailboxes, runtime state, queued work, and temporary data. The `/var/db` example is distribution-specific to Gentoo.

`~` abbreviates the user's home. Directories such as `.cache`, `.config`, `.local`, `.mozilla`, `.ssh`, and `.vim` hold user-specific data or application settings. This gives a practical lookup: headers under `/usr/include`, system logs under `/var/log`, and a user's SSH configuration under home's `.ssh`.

## stat metadata: size, allocation, and timestamps

Metadata and detailed I/O also form a materials-based bridge for September 16, which has no recording. The September 21 recap does not establish that missing day's exact slide progression. The following fields come from Files and Directories slides 3–7.

| Field | Meaning |
|---|---|
| `st_dev`, `st_ino` | Filesystem device and inode number |
| `st_mode` | File type and permission bits |
| `st_nlink` | Hard-link count |
| `st_uid`, `st_gid` | Numeric owner user/group IDs |
| `st_rdev` | Special-device identification |
| `st_size` | Logical file size in bytes |
| `st_blksize` | Preferred I/O block size |
| `st_blocks` | Allocated 512-byte block count |

For example, `st_size=8192` and `st_blocks=8` mean 8192 logical bytes and `8×512=4096` bytes of reported allocation. Do not substitute `st_blksize` for that 512-byte accounting unit. A sparse file can return zeros from a hole without allocating storage for every logical byte. The slide's `st_size/512 > st_blocks` is an allocation clue, not a necessary-and-sufficient test across all filesystems. Creating a hole by seeking and then writing connects to [[courses/system_programming/units/en/io-streams|I/O positioning]].

Atime records access, mtime content modification, and ctime inode status change. **Ctime is not creation time.** Slide 5 incorrectly labels `st_mtim` as “last access”; the modification distinction on slide 7 is used here. Nanosecond representation in `timespec` does not guarantee nanosecond clock accuracy. [Files and Directories slides 3–7](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/05.IO.Files.and.Directories_3d312c60.pptx)

The [[courses/system_programming/transcripts/2026-09-21|September 21 lecture, 02:32]] adds that an inode can point directly to data blocks or indirectly through another block containing pointers. This describes internal organization, not an assertion that `stat` exposes that pointer array. No pointer counts or block sizes are supplied for calculating a particular filesystem's maximum file size.

## Path anchors and metadata targets

An absolute path starts at `/`. A relative path starts from a reference directory and need not begin with `./`. In the source's `a/b/c/d` and `a/b/f` tree, `c/d` relative to `a/b` identifies the descendant `d`.

| API | Target |
|---|---|
| `stat(path, ...)` | Target reached through the pathname |
| `lstat(path, ...)` | The final symlink itself, when present |
| `fstat(fd, ...)` | Object already opened through a descriptor |
| `fstatat(dirfd, path, ..., flags)` | Relative pathname anchored to a directory fd, with selected follow policy |
| `statx(...)` | Extended metadata requested through a mask and related arguments |

Directory anchoring and symlink-following policy are separate decisions. `AT_SYMLINK_NOFOLLOW` requests inspection of the final symlink itself. The [[courses/system_programming/transcripts/2026-09-21|September 21 lecture, 03:59]] motivates an open directory anchor when directory names or locations can change. This does not eliminate every path race. Birth-time information from `statx` also depends on support and the filesystem. [Files and Directories slides 8–9](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/05.IO.Files.and.Directories_3d312c60.pptx)

### Enumerating entries with a DIR stream

`opendir` returns a `DIR *`; `readdir` supplies entries one at a time; `closedir` releases the stream resources. `dirfd` obtains its associated descriptor. A DIR object is neither an fd integer nor the same type as stdio's `FILE`. `fdopendir` uses an existing descriptor; `mkdir` and `mkdirat` create directories. [[courses/system_programming/transcripts/2026-09-21|September 21 lecture, 05:42]]

The source's `statter.c` opens `argv[1]` or `"."`, then passes each `e->d_name` to `fstatat(dd,...,0)` and prints the name and `st_size`. Flag zero follows symlink targets. A NULL from `readdir` can indicate either normal completion or an error. Clear `errno` before the relevant read and inspect it after NULL. The example also resets it after entry processing so an earlier `fstatat` failure does not contaminate the later enumeration-end check.

The example reports individual lookup failures with `perror`, continues, and ultimately returns `EXIT_SUCCESS`. That status therefore does not establish that every entry was successfully inspected. Understanding the demonstrated flow differs from implementing complete error propagation. [Files and Directories slides 10–11](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/05.IO.Files.and.Directories_3d312c60.pptx)

## Key Takeaways

- A common interface does not imply common seek/storage behavior.
- Trace names, inode references and symlink targets separately.
- Distinguish logical size from allocation and access time from status time.
- Continue with [[courses/system_programming/units/en/permissions|permissions and identity]].

## Recall and Practice

### Recall and reasoning

#### Recall Q01 · File types and bytes

Distinguish regular files, directories, character/block devices and proc/sys. What are alphabet-file offsets 0/25, and does a shared fd API imply identical behavior?

<details><summary>Show solution</summary>

A regular file is bytes: the example has a at offset 0 and z at 25, with format interpreted by applications. Directories associate names with inodes; character devices include terminals/mice, block devices disks/partitions. /proc and /sys expose kernel state/configuration through virtual files. Type codes are `- d l p s c b`. A shared fd API does not make seekability or buffering uniform.

**Check:** Separate bytes, name mappings, device types and virtual interfaces.

</details>

#### Recall Q02 · IPC and FIFOs

Why do processes need IPC? Compare a FIFO producer/gzip consumer with Unix-domain/network sockets, including waiting in a sequential launch.

<details><summary>Show solution</summary>

Private address spaces require an IPC mechanism rather than merely reusing another process’s address. A FIFO is a named, unidirectional ordered byte channel through the kernel, not a disk-stored payload. Open/read may wait for a peer; waiting for the producer to finish before launching the consumer can block progress. Background execution permits concurrent progress. Unix-domain sockets connect local endpoints bidirectionally; network sockets connect network endpoints. Having an fd does not imply seekability.

**Check:** Explain memory isolation, channel location, waiting and socket scope.

</details>

#### Recall Q03 · What a mount hides

What happens to existing file `extern/hello` when tmpfs is mounted at directory `extern`? Explain unmount/reboot, echo/printf byte counts and mount-option roles.

<details><summary>Show solution</summary>

The mount hides rather than deletes underlying files; unmount reveals them. New tmpfs content is volatile, distinct from the original disk file. `echo hello` includes a newline (6 bytes), while `printf hello` gives 5. `ro` is read-only; `noatime/relatime` affect access times; `noexec/nosuid/nodev` restrict execution, set-ID or device interpretation; `size` controls capacity and `iocharset` an applicable filesystem’s encoding. These are not complete security boundaries. Do not infer all /tmp is tmpfs or turn this into bind-mount semantics. Temporary-name collisions matter, but the uncertain API name is not recovered.

**Check:** Check hidden versus deleted, 6/5 bytes and option limits.

</details>

#### Recall Q04 · Names and inode references

Compare hard/symbolic links in inode identity, counts, deletion and cross-filesystem behavior. Calculate a conventional directory’s count with two child directories and explain ls -a/-d.

<details><summary>Show solution</summary>

Hard links name the same inode, share metadata/content and increment its link count; removing one name preserves others. A symlink has its own inode containing a target path, does not increment the target’s hard-link count, and may dangle. Symlinks can cross filesystems; hard links generally cannot and directory hard links are restricted. In the conventional model: parent entry1 + own dot1 + two child dot-dots2 =4; leaves have2. Its own dot-dot refers to its parent, not itself. `ls -a` reveals dot names; `-d` lists the directory itself. Neither changes access control.

**Check:** Account for each reference giving 4/2 without making it universal.

</details>

#### Recall Q05 · Using the hierarchy

Locate headers, logs and personal SSH configuration, and explain the roles of the main hierarchy directories.

<details><summary>Show solution</summary>

Headers: /usr/include; logs: /var/log; personal SSH settings: ~/.ssh. /bin and /sbin hold commands/admin tools; /etc configuration; /home and /root home directories; /tmp temporary files; /usr installed tools/data; /var changing state. /dev represents devices, /proc and /sys kernel interfaces, /boot boot files, /lib libraries, and /mnt, /media conventional mount locations. Use roles to locate resources, without assuming identical layouts across distributions; /var/db examples retain their distribution context.

**Check:** Check the three concrete locations, role-based reasoning and distribution limits.

</details>

#### Recall Q06 · Metadata and allocation

Explain key stat fields. For size 8192 and blocks 8, calculate allocated bytes; distinguish timestamps, timespec and inode block pointers.

<details><summary>Show solution</summary>

dev/ino identify filesystem/inode; mode holds type/permissions; nlink counts hard links; uid/gid identify ownership; rdev identifies a device. size is logical bytes, blksize preferred I/O size, and blocks uses 512-byte units:8×512=4096. Allocation below8192 suggests sparsity but is not a universal proof. atim is access, mtim content modification, ctim status change, not creation. The p.5 mtim/access label conflicts with p.7. Timespec representation resolution does not guarantee clock accuracy. Direct/indirect inode pointers locate data blocks; they are not a stat pointer array, and unspecified counts cannot yield maximum file size.

**Check:** Check4096, time meanings, the ctime pitfall and pointer scope.

</details>

#### Recall Q07 · Paths and the stat family

Where does relative c/d anchored at a/b resolve? Compare stat, lstat, fstat, fstatat and statx, including limitations.

<details><summary>Show solution</summary>

It resolves to a/b/c/d. Relative paths need not start with ./; absolute paths start at /. stat follows a final symlink; lstat examines it; fstat examines an open fd. fstatat anchors relative paths at dirfd; flags0 follows, AT_SYMLINK_NOFOLLOW selects the final link. Anchoring and following are separate choices. `statx` uses masks for requested/available fields; birth time is optional. These APIs do not eliminate every rename/race problem.

**Check:** Distinguish anchor, follow policy and an already opened object.

</details>

#### Recall Q08 · Directory traversal and errors

Explain the DIR* lifecycle and related APIs. In a statter over argv[1] or ., interpret readdir NULL, fstatat failures and overall status.

<details><summary>Show solution</summary>

Use opendir→repeated readdir→closedir; DIR* differs from FILE* and integer fd. dirfd obtains a directory fd; fdopendir builds a stream from one; mkdir/mkdirat create directories. The statter uses fstatat(flags0) relative to dirfd, following links. `readdir` NULL can mean end or error: clear errno before the relevant call and inspect it on NULL, avoiding stale errno from an intermediate fstatat failure. Continuing after an entry error and returning success does not mean every entry was examined.

**Check:** Check API roles, errno timing and partial-success limits.

</details>

### Practice

#### Practice P01 · Which names change counts?

**Newly written synthetic practice.** In the conventional model, D has empty child directories A/B. Separate regular inode R has exactly one name, `D/r`. Add hard link `D/h` to R and symlink `D/s`, then remove `D/r`; `D/s` stores relative target path `r`, which resolves to `D/r`. Explain D/R link counts and s’s state.

[EX:sp_2025_2_midterm_q03 p.7] Q3(a–b) contributes inode-reference counting, combined here with deletion and dangling paths. Prerequisite: Q04. The conventional directory model is stipulated, not a universal 2+N law. [[exam_questions/sp_2025_2_midterm_q03|Authorized related question preview]]

<details><summary>Show solution</summary>

D starts at 4 and stays4: regular name h and symlink s create no child dot-dot references. R goes1→2 when h is added, then2→1 when r is removed. `s` never contributes to R’s count and dangles because its stored path r is gone. `h` still reaches R’s data. Count names, path strings and inode references separately.

**Check:** Justify D=4, R=1, dangling s and surviving h.

</details>

### Review plan

Review Q01–Q04 with object/name diagrams and Q06–Q08 with units and API choices. In P01 count surviving references and revisit Q04 for any mistaken assumptions.

## Sources

### Dated lecture notes

- [[courses/system_programming/lectures/en/2026-09-09-lecture-03|2026-09-09 lecture notes]]
- [[courses/system_programming/lectures/en/2026-09-14-lecture-04|2026-09-14 lecture notes]]
- [[courses/system_programming/lectures/en/2026-09-16-materials-io-review|2026-09-16 associated materials]]
- [[courses/system_programming/lectures/en/2026-09-21-lecture-05|2026-09-21 lecture notes]]

### Materials and lecture passages

- [Unix filesystem slides 4–7](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)
- [Unix filesystem slide 8](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)
- [Unix filesystem slides 11–13](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)
- [Unix filesystem slides 15–18](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)
- [Unix filesystem slides 19–21](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)
- [Unix filesystem slides 22–27](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx)
- [Files and Directories slides 3–7](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/05.IO.Files.and.Directories_3d312c60.pptx)
- [Files and Directories slides 8–9](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/05.IO.Files.and.Directories_3d312c60.pptx)
- [Files and Directories slides 10–11](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/05.IO.Files.and.Directories_3d312c60.pptx)
- [[courses/system_programming/transcripts/2026-09-09|September 9 lecture, 49:54–55:05]]
- [[courses/system_programming/transcripts/2026-09-14|September 14, 06:55]]
- [[courses/system_programming/transcripts/2026-09-14|September 14, 08:32]]
- [[courses/system_programming/transcripts/2026-09-21|September 21 lecture, 02:32]]
- [[courses/system_programming/transcripts/2026-09-21|September 21 lecture, 03:59]]
- [[courses/system_programming/transcripts/2026-09-21|September 21 lecture, 05:42]]

The linked materials are the supplied public slide decks; no PDF page-cache link is available for these sources. Transcript timestamps are plain labels.

- [04.IO.Direct.and.Buffered.IO_8e725857.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO_8e725857.pptx)

### Scope to retain

- September16 is an inferred materials-only review without a recording. The September21 recap does not prove its exact coverage.
- The uncertain temporary-file API and conflicting mtim label remain; neither is converted into recovered speech or creation-time semantics.
- Directory 2+N is limited to the stipulated conventional model. Mount, sparsity and timestamp behavior depend on filesystem/environment.
- Only the selected subquestions are connected; supplied answers are not treated as independently verified authority.


---

[[courses/system_programming/units/en/state-machines|← Previous: Character Processing, DFAs, and Decommenter Boundaries]] · [[courses/system_programming/units/index|Unit contents]] · [[courses/system_programming/units/en/permissions|Next: Permissions, Execution Identity, and Extended Metadata →]]
