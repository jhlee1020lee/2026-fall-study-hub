---
title: "Unix I/O, Open-File State, and Standard I/O Buffering"
description: "Compare Unix I/O and stdio through return units, shared offsets and buffering."
course: "system_programming"
unit_id: "io-streams"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["00.Introduction.pptx", "04.IO.Direct.and.Buffered.IO.pptx", "04.IO.Direct.and.Buffered.IO_8e725857.pptx", "05.IO.Files.and.Directories_3d312c60.pptx"]
private_source_assets: []
source_lectures: ["courses/system_programming/lectures/en/2026-09-02-lecture-01", "courses/system_programming/lectures/en/2026-09-14-lecture-04", "courses/system_programming/lectures/en/2026-09-16-materials-io-review", "courses/system_programming/lectures/en/2026-09-21-lecture-05"]
---

Trace I/O through requested bytes, actual progress and open-file state. Separate stdio buffers from kernel offsets to explain short counts, dup and flushing.

## Unix I/O: kernel services and file descriptors

Applications interpret file contents, but device access needs kernel services. A system call crosses that boundary. Libc wrappers express requests as convenient C function calls. At [[courses/system_programming/transcripts/2026-09-14|September 14, 01:16:19]], the lecturer explains that a wrapper prepares a syscall number and arguments in the required passing locations before requesting kernel entry. The unclear instruction name and register details are not reconstructed.

`strlen`, `strstr`, and ordinary mathematical calculations can operate on existing user-space memory. `open`, `read`, and `write` request kernel I/O services. `printf` can eventually lead to `write` after formatting and buffering, but the calls need not correspond one-to-one.

A file descriptor, fd, is a nonnegative integer handle within a process. Conventionally, `0=STDIN_FILENO`, `1=STDOUT_FILENO`, and `2=STDERR_FILENO` correspond to standard input, output, and error, initially connected to a terminal. Redirection can change those connections. Equal descriptor numbers in different processes do not establish equal targets. [Direct and Buffered I/O slides 4–7](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO.pptx)

If a regular file starts at offset zero and two reads each successfully transfer ten bytes, its position moves `0→10→20`. Actual transferred length matters. Not every descriptor is seekable, as the distinction between [[courses/system_programming/units/en/files-metadata|FIFOs, sockets, and regular files]] shows.

### Following a typedef through headers

`off_t` represents file offsets. The lecture's underlying `long` is a target-specific example, not a universal ABI rule. The materials demonstrate this inspection workflow:

```sh
echo "#include <stdlib.h>" | gcc -E - | grep -w '_*off_t'
```

The pipe sends the include text to the compiler's stdin. `-E` stops after preprocessing, and the standalone `-` selects stdin as source input. Header declarations, including declarations from indirectly included headers, expand into the output so the typedef chain can be inspected. Quoting the grep pattern separates it from shell filename expansion; that is an explanatory qualification. Reading the command does not establish a new machine-specific result.

The source API table also introduces `pread`/`readv`, `pwrite`/`writev`, `openat`, and namespace-removal interfaces `remove`/`unlink`/`unlinkat`/`rmdir`. Listing a related variant does not establish that its full implementation has been taught.

## open and close: the lifetime of an open connection

`open` takes a pathname, access mode, and flags, creates open state, and returns an fd. `O_RDONLY`, `O_WRONLY`, and `O_RDWR` specify access direction. `O_CREAT` requests creation when needed, `O_TRUNC` truncation, and `O_APPEND` writes at the end.

The mode argument for creation requests permissions; it is not unconditionally identical to the resulting permissions. The source opens `/etc/hosts` read-only and uses `creat` with owner read/write permissions. `creat` is an older creation-and-truncation interface. The two- and three-argument presentations of `open` relate to a variadic declaration, not C++ overloading. [Direct and Buffered I/O slides 8–11](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO.pptx)

`open` returns -1 on failure, with `errno` supplying diagnostic information and `perror` able to report it. `close` returns zero on success and -1 on failure. If only descriptors 0, 1, and 2 are occupied, another open commonly receives 3, but the number is not fixed.

Descriptor **number reuse** creates a subtle lifetime problem. Suppose component A closes fd 3 in a shared process descriptor table, then B opens another file and actually receives 3. A's second close using the stale number can close B's new file. This is a double-close problem within a shared table, distinct from unrelated processes both having an fd numbered 3.

The September 14 recording connects the discussion through open and close. The detailed read/write, stdio, and buffer implementation material below provides a **materials-based bridge for the unrecorded September 16 class**, combined with the verified September 21 kernel-file-management discussion. It does not establish that missing day's exact stopping point.

## read and write: requested and actual transfer lengths

Buffers passed to these functions require [[courses/system_programming/units/en/objects-pointers|valid objects and sufficient capacity]].

```c
ssize_t read(int fd, void *buf, size_t count);
ssize_t write(int fd, const void *buf, size_t count);
```

`count` requests bytes. `size_t` represents a size, while `ssize_t` represents actual transferred bytes or error -1. For a positive-length read request, zero indicates EOF, distinct from an error. If a 512-byte request into `char buf[512]` returns 302, only 302 bytes were newly read. The remaining capacity is not part of that input. [Direct and Buffered I/O slides 12–20](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO_8e725857.pptx)

String length and storage size also differ. The source's `"Hello, world\n"` has thirteen characters; an array initialized from it has `sizeof` fourteen, including NUL. With the exclamation mark, `"Hello, world!\n"` has fourteen characters and fifteen stored bytes. Passing `strlen(str)` to `write` omits the terminator, provided `str` really is NUL-terminated.

The append example opens with `O_WRONLY|O_CREAT|O_APPEND` and requested mode `0644`, then writes and closes. It omits write and close checks. Similarly, the one-byte copy loop writes while `read(...,&c,1)>0`, but lets EOF and read error end the same loop and ignores write results. It illustrates control flow, not complete error handling.

### A short count is not automatically an error

A short count transfers fewer bytes than requested without returning -1. Causes can involve approaching EOF, available terminal input, pipe/socket data, interruptions, or filesystem space. Inspect the result and update processed length, remaining length, and the next buffer position. Not every situation has the same retry policy.

Slide 21 requests 100000 bytes from input offset 400000. After an initial 65536 bytes, the remaining request is `100000-65536=34464`, but the next transfer returns 27776.

`65536 + 27776 = 93312 bytes`  
`100000 - 93312 = 6688 bytes`

The total falls short by 6688 bytes. The display does not establish the precise cause or reveal the complete copy implementation. Also, compare the result with the actual requested `count`, not automatically with `sizeof(buf)`.

## lseek and logical positions in sparse files

`lseek(fd,offset,whence)` changes the next I/O position.

| `whence` | New position |
|---|---|
| `SEEK_SET` | `offset` from the beginning |
| `SEEK_CUR` | Current position + `offset` |
| `SEEK_END` | Current end + `offset` |

Success returns the new absolute position; failure returns -1. After `lseek(fd,100,SEEK_SET)`, the next I/O begins at offset 100. Merely seeking there in a twenty-byte file does not immediately extend its length to 100. A subsequent write can establish a later EOF and an intervening hole that reads as zeros. Physical allocation depends on the filesystem, explaining why [[courses/system_programming/units/en/files-metadata|st_size and st_blocks]] can differ. Do not assume regular-file seeking for a pipe or socket. [Direct and Buffered I/O slides 17–18](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO_8e725857.pptx)

## Descriptors, open-file entries, and inodes are different layers

Using the same file does not necessarily share the same offset.

| Layer | Relationship or state |
|---|---|
| Process descriptor table | Descriptor number → open-file entry |
| Open-file entry | Current position, reference count, and open state |
| Vnode/inode-related structure | File type, size, and access metadata |

Two independent `open` calls on one pathname can reach the same file metadata through separate open-file entries with separate positions. The [[courses/system_programming/transcripts/2026-09-21|September 21 lecture, 14:07]] explicitly distinguishes them. The statement at 10:13 about one open-file table per process conflicts with the shared relationships in the slides; the model here uses per-process descriptor tables referencing potentially shared open-file entries. [Files and Directories slides 13–14](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/05.IO.Files.and.Directories_3d312c60.pptx)

Descriptors inherited through `fork` can refer to one entry from separate parent and child descriptor tables. Descriptor passing is also more than sending an integer: the kernel establishes a receiving-process fd connected to the open entry, adding a reference. The receiving number is independently allocated and may equal or differ from the sending number. Full fork and descriptor-passing implementations remain later topics.

### Changing connections with dup and dup2

`dup(oldfd)` returns the lowest available descriptor referencing the same open-file entry. A variable called `fd2` can hold the number 4; its name does not make it stderr's descriptor 2.

Closing stdout 1 and then calling `dup(3)` produces 1 only if 1 is the lowest free slot at that moment. Another action can intervene, so close-plus-dup is not an atomic redirection operation. `dup2(oldfd,newfd)` establishes the specified `newfd` connection. Using a writable descriptor in `dup2(fd,STDOUT_FILENO)` redirects subsequent stdout output to that file. The source opens with `O_WRONLY`; absent `O_CREAT` or `O_TRUNC` flags must not be silently added to its behavior.

`ls > output.txt` and `cat < input.txt` redirect output and input; `ls | sort -R` connects one process's output to another's input. Once two descriptors reference an entry, closing one does not invalidate the remaining reference. For historical Q3(c), track descriptor numbers, surviving references, the shared offset, and the overwritten byte range separately at every step. [EX:sp_2025_2_midterm_q03 p.7]

## Tracing offsets in two source programs

### Independent opens followed by duplication

The input to `fwfd1.c` is `System Programming`. Three independent opens are followed by `dup2(fd2,fd3)`. fd1 retains independent state; fd2 and fd3 now share one entry.

| Operation | Position before reading | Character | Effect |
|---|---:|---|---|
| Read one byte through fd1 | Independent entry: 0 | `S` | Only that entry moves to 1 |
| Read one byte through fd2 | Shared entry: 0 | `S` | Shared entry moves to 1 |
| Read one byte through fd3 | Shared entry: 1 | `y` | Shared entry moves to 2 |

Thus `c1=S,c2=S,c3=y`. One underlying file does not merge all positions, and different descriptor numbers do not ensure independent positions. [Files and Directories slide 19](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/05.IO.Files.and.Directories_3d312c60.pptx)

### Combining append and ordinary writes

`fwfd2.c` opens fd1 with `O_CREAT|O_TRUNC|O_RDWR` and writes four bytes, `CSAP`. It separately opens fd3 with `O_APPEND`. Following the successful path gives:

| Operation | Contents | Position shared by fd1 and its duplicate |
|---|---|---:|
| Write `CSAP` through fd1 | `CSAP` | 4 |
| Append `M1522` through independent fd3 | `CSAPM1522` | Still 4 |
| `fd2=dup(fd1)` | Unchanged | 4 |
| Write `SNU` through fd2 | `CSAPSNU22` | 7 |
| Append `800` through fd3 | `CSAPSNU22800` | Still 7 |

`SNU` overwrites `M15` at positions 4–6 inherited from fd1's open entry. The final fd3 write appends at the current EOF. The final contents are `CSAPSNU22800`. The literal bytes must be distinguished from spaces introduced by text extraction. This is a trace of successful source operations, not a new runtime test of omitted error handling. [Files and Directories slide 20](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/05.IO.Files.and.Directories_3d312c60.pptx)

## Standard I/O and FILE streams

Standard I/O offers formatting and buffering through `FILE *` streams. `stdin`, `stdout`, and `stderr` conventionally connect to descriptors 0, 1, and 2. A `FILE *`, an fd integer, and a [[courses/system_programming/units/en/files-metadata|DIR *]] are different abstractions.

| Purpose | Representative APIs and related variants |
|---|---|
| Open or associate | `fopen`, `fdopen`, `freopen` |
| Transfer elements | `fread`, `fwrite` |
| Position | `fseek`, `ftell`, `rewind`, `fgetpos`, `fsetpos` |
| Character/line input | `fgets`, `fgetc`, `getc`, `getchar`, `ungetc` |
| Formatted input | `fscanf`, `scanf`, `sscanf`, `vscanf` |
| Character/line output | `fputs`, `fputc`, `putc`, `putchar`, `puts` |
| Formatted output | `fprintf`, `printf`, `dprintf`, `sprintf`, `snprintf`, `vprintf` |
| Close and status | `fclose`, `fflush`, `feof`, `ferror`, `fileno` |

Members of a family differ in destination, bounds, or argument passing, and not every listed variant belongs to ISO C. `fgets` has a buffer limit. The source strikes out `gets`; it is not a recommendation. The table's `char` return type for `fputs` and `sprint` spelling are source errors, not API contracts. [Direct and Buffered I/O slides 27–31](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO_8e725857.pptx)

`fread(ptr,size,nmemb,stream)` requests `size*nmemb` bytes but returns the number of completed **elements**. A result of seven for four-byte elements represents twenty-eight bytes of complete elements; it does not fully describe a possible partial final element. `fseek` returns an `int` success status; `ftell` obtains a position. The later summary's `off_t fseek` is inconsistent with that contract. `feof` and `ferror` inspect conditions that have already occurred; they do not predict whether the next read will succeed.

### Acquiring, using, and closing a stream

The source output example begins with `fopen("./output.txt","a+")`. The mode requests reading and appending, though the example actually performs output. On NULL it calls `perror("Cannot open/create file")` and returns `EXIT_FAILURE`. Otherwise it calls `fprintf(out,"%s",str)`, then `fclose(out)`, then returns `EXIT_SUCCESS`.

`fopen` failure is a NULL pointer, while Unix `open` failure is integer -1. Since the example omits checks for `fprintf` and `fclose`, its final success status does not prove that all output and closing succeeded. Likewise, executing both `fprintf(stdout,...)` and `printf(...)` produces two outputs, not one combined alternative.

## How buffering reduces system calls

Calling into the kernel for each byte repeats boundary-crossing overhead. Standard I/O collects small operations in a user-space buffer and performs larger reads or writes. Formatting converts values to text; buffering controls transfers. These are separate services.

The source gives this ten-MiB byte-copy measurement:

| Method | real | user | sys |
|---|---:|---:|---:|
| One-byte Unix I/O | 2.679 s | 0.363 s | 2.316 s |
| Standard I/O | 0.261 s | 0.261 s | 0.000 s |

These are measurements from one example, not universal speed ratios or a fixed syscall cost. A displayed `sys=0.000` does not mean no kernel calls occurred. Larger raw transfers can change the comparison. Historical Q3(d) similarly demands an explanation of buffer use and kernel-boundary crossings for the same data, rather than a claim based only on function names. [EX:sp_2025_2_midterm_q03 p.8] [Direct and Buffered I/O slides 23–25](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO_8e725857.pptx)

### Application consumption versus the kernel offset

If a read fetches `B0…Bk-1` into a buffer, the kernel's next position becomes `Bk`. The application may have consumed only part of that buffer, with `Bs` its next logical stream byte. Those positions need not coincide.

In slide 40, distinguish the user-space FILE's `bufpos=378` and `fd=4` from the kernel open-file entry's `pos=1024, refcnt=1`. Buffered input remains available to the application while the raw fd has advanced to 1024. The FILE buffer, process descriptor table, open-file entry, vnode metadata, kernel disk-block cache, and storage are separate layers. The `fopen` label does not mean that fopen alone always immediately reads 1024 bytes. [Direct and Buffered I/O slides 26, 39–40](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO_8e725857.pptx)

## Buffering modes and flush events

The materials give representative modes, adjustable through `setvbuf`.

| Mode | Representative use | Behavior |
|---|---|---|
| Fully buffered, `_IOFBF` | Files | Refill empty input; transmit full or explicitly flushed output |
| Line buffered, `_IOLBF` | Terminals | Transmit output on newline and other applicable events |
| Unbuffered, `_IONBF` | Typical stderr default | Do not accumulate output in a stdio buffer |

Line-buffered output can be flushed by newline, a full buffer, explicit `fflush`, stream closing, or normal termination. Input-related flushing has stream and environment conditions; not every input operation flushes every output stream. Abnormal termination need not flush everything. Unbuffered stdio does not eliminate kernel or device buffers, and `fflush` is not a durable-disk-commit guarantee.

Slide 37 traces:

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

The first newline corresponds to a six-byte `hello\n` write. Explicit flushing sends six bytes `hello,`. The last newline completes six bytes `world\n`. The fragments are `wor` and `ld`, with no added spaces. Slide 32's separate calls emitting `h,e,l,l,o,newline` can likewise combine into one six-byte write. [Direct and Buffered I/O slides 32–37](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO_8e725857.pptx)

## Understanding a FILE implementation model

The source pseudocode opens an fd, allocates a FILE and buffer, then sets `bufpos=0, bufsize=0`. Here `bufsize` means **remaining valid unread data**, not allocated capacity.

`refill_buffer` reads, resets `bufpos` to zero, and places a positive returned count into `bufsize`. `slide_buffer` increases `bufpos` and decreases `bufsize` by the consumed length, which must not exceed available data. The `fread` model targets `size*nmemb` bytes, refills an empty buffer, copies the smaller of remaining request and available bytes, then advances both sides.

This explains the mechanism but is not a complete libc implementation. It returns `read_bytes` rather than actual fread's completed-element count. The fclose model closes the fd and frees two allocations but omits output flushing and error propagation. Allocation cleanup, multiplication overflow, EOF/error flags, void-pointer arithmetic, and inconsistent field names also remain limitations. `fileno` illustrates access to the underlying descriptor. [Direct and Buffered I/O slides 41–43](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO_8e725857.pptx)

## Binary data and choosing an I/O interface

JPEG, GIF, and object files contain arbitrary bytes. Splitting at newlines does not necessarily produce meaningful records. `strlen` and `strcpy` stop at embedded NUL or can cross a buffer boundary if no terminator exists. Unix text's LF, `0x0A`, and the Windows/HTTP examples' CRLF, `0x0D 0x0A`, also illustrate different line conventions. [Files and Directories slide 25](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/05.IO.Files.and.Directories_3d312c60.pptx)

The limitation is not that all stdio is incapable of binary I/O. Explicit-size `fread` and `fwrite` can handle binary data. Avoid interpreting arbitrary bytes as lines or NUL-terminated strings without a valid format contract.

For ordinary disk and terminal work, consider the highest-level interface that meets the requirements. Stdio helps with formatting, buffering, and short internal transfers, but callers still inspect element counts and EOF/error state. Metadata such as size and permissions requires interfaces such as `stat` or `fstat`: [[courses/system_programming/units/en/permissions|access metadata]] and stream data transfer are different services.

Inside a signal handler, stdio must not be assumed safe. Async-signal-safety means that a call meets its contract when invoked by a handler interrupting other execution. Examine the individual contract of suitable raw interfaces such as `read` and `write`; do not extend the property to every function labeled Unix I/O. The source's socket warning likewise concerns buffering and bidirectional stream restrictions, not an absolute impossibility of associating a FILE with a socket. Detailed signal and socket mechanisms remain later topics. Raw I/O may be needed for a performance-critical workload, but transfer size and buffer management determine the result. [Direct and Buffered I/O slides 45–47](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/04.IO.Direct.and.Buffered.IO_8e725857.pptx)

## Key Takeaways

- Separate requested/actual counts and bytes/elements.
- Open-file entries determine shared offsets, not descriptor numbers.
- Buffering, formatting, kernel cache and disk durability differ.
- Continue to [[courses/system_programming/units/en/memory-layout|memory layout]].

## Recall and Practice

### Recall and reasoning

#### Recall Q01 · Libraries and syscalls

Distinguish strlen/strstr/printf from kernel I/O, identify fd0/1/2 and trace two ten-byte reads. What can an off_t preprocessing lookup establish?

<details><summary>Show solution</summary>

strlen/strstr compute in user space; printf formats/buffers and requests kernel service when needed, not one write per call. A syscall wrapper supplies a number/arguments for kernel entry without recovering uncertain register details. Fds are process-local nonnegative integers; 0/1/2 are stdin/stdout/stderr. Two successful ten-byte reads from 0 yield offsets 0→10→20. off_t is a target typedef. `echo "#include <stdlib.h>" | gcc -E - | grep -w '_*off_t'` preprocesses header input and searches tokens: `-E` means preprocessing, final `-` means stdin, with possible indirect headers. It is not a reported execution or universal type proof.

**Check:** Check user/kernel roles, fd scope, offsets and pipeline stages.

</details>

#### Recall Q02 · Open, close and reuse

Explain open access/creation flags, mode, failure and close. When can closing a stale fd number close a newly opened file?

<details><summary>Show solution</summary>

O_RDONLY/O_WRONLY/O_RDWR select access; O_CREAT creates, O_TRUNC truncates and O_APPEND appends. Mode requests creation permissions but does not alone determine actual permissions. Open is variadic, not C overloading. Failure is−1 with errno, reportable by perror; close returns 0/−1. If a new open reuses a closed number in the same table, a stale close may close the new entry. Equal numbers in independent processes are a different case.

**Check:** Check flags, requested mode, returns and same-table reuse.

</details>

#### Recall Q03 · Requested and actual bytes

Interpret read results 302, 0, −1 for a 512-byte request; explain write counts, Hello literal length/sizeof and omissions in a simple copy loop.

<details><summary>Show solution</summary>

302 means only the first 302 bytes are new; 0 on a positive request means EOF; −1 means error. Count is size_t bytes; ssize_t reports actual bytes/error. `"Hello, world\n"` has length 13, sizeof 14; adding ! gives 14/15. `strlen` excludes NUL; 0644 in the append example is requested mode. A loop using only `read(...)>0` merges EOF/error and can ignore short writes and write/close errors.

**Check:** Check valid 302 bytes, all returns, 13/14 and 14/15, and omitted errors.

</details>

#### Recall Q04 · Short-count arithmetic

A100000-byte request returns 65536, then27776. Find the second request, accumulated total and remainder. Does a short count establish its cause or guaranteed retry success?

<details><summary>Show solution</summary>

Second request34464; accumulated total 93312; remainder6688. A positive short count reports progress, not a−1 error. Advance the buffer by accumulated bytes and reduce the remaining request. Stopping/retrying depends on the interface and actual results; the cause cannot be invented.

**Check:** Check34464/93312/6688 and progress-based updates.

</details>

#### Recall Q05 · Seeking versus file length

Explain SEEK_SET/CUR/END and lseek returns. After seeking from a 20-byte file to 100 without writing, what happens to length and a possible hole?

<details><summary>Show solution</summary>

SET uses an absolute offset, CUR adds to current position, END adds to file end; success returns the new absolute offset, failure−1. Seeking alone leaves length 20. Writing at 100 can extend the file with a gap that reads as zeros, with allocation dependent on filesystem. Do not apply this seek model to pipes/sockets.

**Check:** Separate position, length, later writing and allocation.

</details>

#### Recall Q06 · FILE* APIs and return units

Compare FILE* with fd/DIR*, stream-opening APIs, element counts, positioning and error indicators. What must be checked in the a+ and string examples?

<details><summary>Show solution</summary>

FILE* is a library stream. `fopen` opens a path, fdopen wraps an existing fd, freopen reconnects a stream. `fread`/fwrite return complete elements: size 4 and return 7 mean28 complete bytes, with a possible partial element beyond them. `fseek` returns status (0 on success); ftell position; feof/ferror inspect conditions already encountered. Fgets is bounded input; gets is not a safe substitute. Source fputs-return-char and sprint typos are not adopted as APIs. `fopen` a+ permits reading/appending; NULL requires perror/failure handling, while fprintf/fclose can also fail after a successful open. Two executed printf calls produce two outputs.

**Check:** Check elements/bytes, status/position, retrospective flags and unchecked errors.

</details>

#### Recall Q07 · Buffering costs

Why can per-character getchar/putchar and read/write(count 1) have different kernel-call counts? Interpret the lecture timings.

<details><summary>Show solution</summary>

Stdio batches characters to reduce syscalls. Formatting and buffering differ; raw I/O can also use large blocks. The roughly 10MiB example gives unbuffered2.679 real/0.363 user/2.316 sys versus buffered0.261/0.261/0.000. These are particular measurements: displayed0.000 does not mean no syscalls or a universal speed ratio.

**Check:** Distinguish library/kernel calls and the measurement’s scope.

</details>

#### Recall Q08 · Two positions in a stream

With FILE logical position378, fd4 kernel offset 1024 and refcount1, where do stdio/raw reads proceed? Distinguish buffer, cache and disk.

<details><summary>Show solution</summary>

Stdio consumes the buffered byte at logical378, with 646 bytes left in the initially filled1024-byte block. A raw read on that fd starts at kernel offset 1024. Distinguish FILE buffer, process fd table, open-file entry, inode/kernel cache and disk. `fopen` does not universally read 1024 bytes immediately.

**Check:** Check378/1024/646 and the separate storage layers.

</details>

#### Recall Q09 · Flush boundaries

Explain representative fully/line/unbuffered modes and setvbuf. Trace hello-newline, hello-comma with fflush, and wor+ld+newline; distinguish termination and durability.

<details><summary>Show solution</summary>

Typical modes are _IOFBF for files, _IOLBF for terminals and _IONBF for stderr, adjustable through setvbuf. In line mode, `hello\n` emits6 bytes at newline. Hello plus comma then fflush emits6; wor+ld+newline emits `world\n`, also6. Full buffers, applicable newlines, explicit fflush, close and normal exit can flush. Input-triggered flushing is conditional; abnormal exit is no equivalent guarantee. Unbuffered does not eliminate kernel buffering, and fflush does not guarantee disk durability.

**Check:** Check all three six-byte outputs, conditional flushing and durability.

</details>

#### Recall Q10 · Stdio pseudocode invariants

Explain allocation, bufpos/bufsize, refill and consumption in the lecture pseudocode; identify where it differs from the standard API.

<details><summary>Show solution</summary>

Allocate fd/FILE/buffer; initial bufpos=0, bufsize=0 means zero valid unread data, not zero capacity. Refill resets position and records actual read bytes. Consumption len is bounded by request and valid bytes, then pos+=len, size−=len; a loop may refill repeatedly. Returning bytes from the sample fread differs from standard element counts. The fclose sketch omits output flushing/error handling; allocation cleanup, overflow, void-pointer arithmetic and naming remain pseudocode limits.

**Check:** Check valid size/capacity, updates and differences from the API.

</details>

#### Recall Q11 · Descriptors and shared offsets

What is shared by independent opens, dup, inherited fds and descriptor passing? Are matching numbers or inodes sufficient?

<details><summary>Show solution</summary>

Process fd-table entries reference open-file entries with position/refcount, above underlying file identity. Independent opens of the same inode have separate positions; dup and corresponding inherited fds share an open-file entry/offset. Descriptor passing transfers a kernel association, not merely an integer, and the receiver’s number may differ. Keep the September21 10:13 conflicting wording distinct from the explicit independent-open explanation at 14:07.

**Check:** Check all three layers and sharing mechanisms.

</details>

#### Recall Q12 · Redirection and dup

Explain shell >, <, | and dup/dup2. When does close(1); dup(3) produce1, and what is the two-call limitation?

<details><summary>Show solution</summary>

> redirects stdout, < stdin, and | connects producer output to consumer input. `dup` selects the lowest free number; a variable called fd2 need not equal2. After close1, dup3 yields 1 only if1 remains lowest free and 3 valid; two separate calls permit intervening reuse. `dup2` targets a specified descriptor to the same open-file entry. Offsets are shared and closing one reference leaves others usable. Do not add O_CREAT/O_TRUNC effects to the source’s O_WRONLY-only open.

**Check:** Check lowest-free allocation, specified targets, shared state and separate calls.

</details>

#### Recall Q13 · Two successful execution traces

For fwfd1, independently opened fd1/fd2 read System Programming and dup2 connects fd3 to fd2: read one byte through1, 2, 3. For fwfd2 trace write CSAP, separate append M1522, write SNU through dup(fd1), then append800.

<details><summary>Show solution</summary>

`fwfd1` yields S, S, y: fd1’s offset is1 and the shared fd2/fd3 offset 2. In fwfd2, CSAP gives fd1 offset 4, length 4. Appending M1522 gives CSAPM1522, length 9 while fd1 stays4. SNU through dup(fd1) overwrites M15 at 4, giving CSAPSNU22 and shared offset 7. Appending800 yields CSAPSNU22800, length 12. Keep independent and append positions separate. This is a successful-call paper trace, not an execution report.

**Check:** Check S/S/y, 1/2 and every content/offset/length state.

</details>

#### Recall Q14 · Binary data and interface choice

Why is strlen copying unsuitable for binary data with NUL/newlines, while fread/fwrite can work? Explain LF/CRLF and API choices for metadata, signals and sockets.

<details><summary>Show solution</summary>

Binary data contains arbitrary bytes including NUL, so strlen may stop early; newline is not automatically a record boundary. `fread`/fwrite handle binary data with explicit lengths. LF is0A; CRLF is0D0A. Choose the highest-level interface meeting required control; use stat/fstat for metadata. General stdio is unsafe in signal contexts, requiring specific async-signal-safe rules. Socket streams have constraints, not a universal prohibition on stdio. Raw I/O is not always faster.

**Check:** Check binary lengths, line-ending bytes and capability-based choices.

</details>

### Practice

#### Practice P01 · Tracing shared and independent handles

**Newly written synthetic practice.** Initially the file is ABCDEFGH. Independent opens a/b start at 0, c=dup(a). Assume success: lseek(c, 2, SET), write(a, "xy", 2), read(b, 3), close(a), write(c, "Z", 1). Find final bytes, read bytes and offsets.

[EX:sp_2025_2_midterm_q03 p.7] Q3(c) transfers dup/seek/close overwrite reasoning, with an independent reader added. Prerequisites: Q05/Q11–Q13; regular file and successful calls are stipulated. [[exam_questions/sp_2025_2_midterm_q03|Authorized related question preview]]

<details><summary>Show solution</summary>

C’s seek moves the a/c shared offset to 2. Writing xy replaces C/D: ABxyEFGH, shared offset 4. B independently reads ABx from 0 and ends at 3. Closing a leaves c’s reference alive. C writes Z over E at 4: ABxyZFGH, shared offset 5, length 8. Seek/dup/close do not insert string characters.

**Check:** Justify ABx, ABxyZFGH, b3/c5 and length 8.

</details>

#### Practice P02 · Call counts and flushing

**Newly written synthetic practice.** Copy8192 bytes: A uses one-byte raw reads/writes; B uses 4096-byte blocks. Assume full transfers and include a final EOF read. Count calls and compare character stdio and terminal newline behavior.

[EX:sp_2025_2_midterm_q03 p.8] Q3(d) contributes syscall-cost reasoning, extended to block raw I/O and flush conditions. Prerequisites: Q07–Q09/Q14. No private file-size setup or supplied answer is reproduced.

<details><summary>Show solution</summary>

A makes8192 reads+1 EOF read+8192 writes=16385 calls. B makes2 reads+1 EOF read+2 writes=5. In the analogous EOF-driven character stdio loop, `getchar` is called 8193 times including the final EOF check and `putchar` 8192 times. Buffering may reduce kernel calls; exact syscall counts require buffer/flush assumptions. Terminal newlines can flush earlier. The call-count ratio is not a runtime speedup guarantee.

**Check:** Check16385/5 including EOF, library/kernel differences and no timing-ratio guarantee.

</details>

### Review plan

Write units beside every return in Q01–Q06. Draw FILE-buffer/fd/open-entry layers for Q08/Q11–Q13 before tracing P01. Revisit Q07/Q09/Q14 while counting P02 calls.

## Sources

### Dated lecture notes

- [[courses/system_programming/lectures/en/2026-09-02-lecture-01|2026-09-02 lecture notes]]
- [[courses/system_programming/lectures/en/2026-09-14-lecture-04|2026-09-14 lecture notes]]
- [[courses/system_programming/lectures/en/2026-09-16-materials-io-review|2026-09-16 associated materials]]
- [[courses/system_programming/lectures/en/2026-09-21-lecture-05|2026-09-21 lecture notes]]

### Materials and lecture passages

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
- [[courses/system_programming/transcripts/2026-09-14|September 14, 01:16:19]]
- [[courses/system_programming/transcripts/2026-09-21|September 21 lecture, 14:07]]

The linked materials are the supplied public slide decks; no PDF page-cache link is available for these sources. Transcript timestamps are plain labels.

- [00.Introduction.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx)
- [[courses/system_programming/transcripts/2026-09-02|Lecture transcript · 2026-09-02 01:12:09]]

### Scope to retain

- September16 is inferred from materials, with no recording or exact taught-scope evidence; later recap does not retroactively verify it.
- September21 10:13 sharing wording conflicts with the14:07 independent-open explanation. Uncertain register details are not recovered speech.
- `fputs`/sprint typos and pseudocode omissions in element returns, flushing and errors are not actual API contracts.
- Traces assume successful calls. Lecture timing is environment-specific; supplied exam answers are not authority.


---

[[courses/system_programming/units/en/permissions|← Previous: Permissions, Execution Identity, and Extended Metadata]] · [[courses/system_programming/units/index|Unit contents]] · [[courses/system_programming/units/en/memory-layout|Next: Process Memory, Alignment, and Parameter Passing →]]
