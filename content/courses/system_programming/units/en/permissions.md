---
title: "Permissions, Execution Identity, and Extended Metadata"
description: "Distinguish file/directory permissions, set-ID identities, ACLs, and xattrs."
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

Start a permission decision with the object type and requested operation. Then distinguish mode bits, execution identity, and filesystem policy.

## Permissions depend on the object and operation

Permission to read a file and permission to remove its name are different questions. First identify whether the object is an ordinary file or directory, and whether the operation accesses contents or changes the namespace. Although `st_mode` contains both type and permission information, a type-test macro such as `S_ISREG` answers a different question from a permission mask such as `S_IRUSR`.

Owner, group, and other each receive read, write, and execute bits. [system_programming:M001 slides 27–30](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx) distinguishes their meanings:

| Bit | Ordinary file | Directory |
|---|---|---|
| `r` | Read contents | Read the list of entry names |
| `w` | Change contents | Change the namespace through entry creation/removal |
| `x` | Execute | Search/traverse paths and access entries |

An actual directory-entry operation needs the relevant conditions together, including write and search. A read-only target file can sometimes have its name removed under the parent directory's permissions. Conversely, being able to list a name does not establish access to the named file's contents.

`chmod g+w file` adds group write permission. `chmod 750 file` sets owner `rwx`, group `r-x`, and other `---`. Within an octal digit, read=4, write=2, and execute=1, so `7=4+2+1`, `5=4+1`, and `0=0`. `S_IRWXU`, or `00700`, groups the owner's three bits; `(mode & S_IRUSR) != 0` tests owner read. Numeric UID/GID values are not names; name lookup is a separate operation.

The main lecture connection is [[courses/system_programming/lectures/en/2026-09-14-lecture-04|2026-09-14 permissions and metadata]]. M014 slide 6 supplies additional mode-test material. The [[courses/system_programming/lectures/en/2026-09-16-materials-io-review|2026-09-16 inferred materials review]] has no recording, so these concepts cannot establish that day's exact spoken progress.

## Sticky directories and filesystem execution policies

In a shared directory, many users may create entries, yet unrestricted removal of one another's names would be undesirable. The sticky bit limits renaming and deletion to the file owner, directory owner, privileged processes, and the relevant permitted cases. The `/tmp` discussion in the [[courses/system_programming/transcripts/2026-09-14|2026-09-14 transcript]] at 41:49–42:41 explains this protective purpose. Sticky does not make every file's contents read-only.

`S_ISVTX` tests sticky and `S_IWOTH` tests other-write. A world-writable location that can hold executables also raises separate questions about content changes and execution. The material uses `fstatfs` to inspect filesystem policy: `ST_NOEXEC` concerns execution restrictions, and `ST_NOSUID` concerns set-ID effects. These operate at a different layer from an individual file's `rwx`. One bit does not establish safety across all execution paths. The broad danger summary on M001 slide 41 must be distinguished from the protective sticky-directory explanation on slide 31.

## Real and effective identities

Separate the identity associated with starting a process from the execution identity used in permission checks. Real UID/GID and effective UID/GID provide this basic distinction. `getuid()`/`getgid()` and `geteuid()`/`getegid()` query the corresponding values.

Under permitted execution conditions, a SUID executable changes the effective user identity to its file owner; SGID concerns the effective group. These are interpretations of source mode examples, not records of permission changes performed here.

| Mode | Ordinary permissions | Additional bits |
|---|---|---|
| `4755` | `755` | SUID |
| `2755` | `755` | SGID |
| `6755` | `755` | Both |

In the material's example, a file owned by another user and group receives only `4755`. The real user remains the invoking user; the effective user becomes the file owner, but the effective group remains unchanged. A different group owner does not itself enable SGID. Policies such as `nosuid` can limit these effects. The source's overbroad claim about all root-owned binaries needing SUID is not a general rule.

Q3(e), [EX:sp_2025_2_midterm_q03 p.8], demands this identity reasoning. Distinguish the **file owner**, **invoking user**, and **effective user**, then explain why defects in a tool running with greater authority can have greater consequences. Translating SUID directly into “always becomes root” misses the owner condition. Actual settings for named binaries can also vary by system. The [[exam_questions/sp_2025_2_midterm_q03|existing question-only preview]] does not make its unrelated I/O subquestions required permission content.

## The lifetime of name-lookup results

`getpwuid` obtains information associated with a numeric UID; `getgrgid` does the corresponding group lookup. Their returned pointers may refer to library-managed storage. Keeping only the first pointer while performing another lookup can expose updated contents through that same storage.

At 53:51–55:01, the transcript explains this issue while looking up real and effective identities successively. M001 slide 35's `whoami.c` uses `strdup` on `pw_name` and `gr_name` to preserve independently owned character copies, then frees them after use. This applies the distinction between [a pointer and its pointee](objects-pointers.md): copying a pointer is not copying its string.

Three failure issues remain distinct. The lookup can return NULL, allocation for a copy can fail, and a local pointer can be uninitialized. `user ? user : "n/a"` tests an already initialized pointer; it does not make an uninitialized `user` safe. The illustrative source omits branches and should not be read as a complete robust utility.

## Narrowing potential risk with metadata predicates

M001 slide 36 opens a directory, obtains its `dirfd`, and examines entries. `fstatat(..., AT_SYMLINK_NOFOLLOW)` permits examining a symbolic link's own metadata rather than following it. The example's `getNext` is a helper, not necessarily another name for standard `readdir`.

Its predicate first requires a regular file. It then requires either **root UID ownership and SUID**, or **root GID ownership and SGID**. Finally, the source classifies it as potentially dangerous only when the filesystem has neither `ST_NOEXEC` nor `ST_NOSUID`. Root ownership alone, or a set-ID bit alone, does not satisfy the whole condition.

For example, a root-owned regular file without SUID fails the user-side condition. Even with SUID, `ST_NOSUID` makes it fail the example's final filter. This is a way to read the predicate, not proof of an exploitable vulnerability. Missing parentheses and omitted error checks prevent treating the source as a complete scanner. Inspecting the directory descriptor's filesystem also does not establish coverage for every entry crossing another mount.

## Extended ACLs and xattrs serve different purposes

Extended ACLs can express finer access control than basic owner/group/other bits. In this source example, `USER` is an identity-free placeholder:

```sh
chmod 640 file.txt
setfacl -m u:USER:r file.txt
getfacl file.txt
```

The command adds or modifies a named-user read entry, and `getfacl` displays the result. The material shows `+` in the `ls` mode display, a named-user `r--` entry, and an `r--` mask. The mask can constrain effective permissions, so one entry is not the entire access decision. Distinguishing basic mode classes from extended ACLs avoids the overbroad summary that POSIX ACLs are limited to three classes.

Extended attributes, or xattrs, attach additional metadata using `namespace.attribute` keys. In the source examples, `security` holds security information such as SELinux data, `system` holds kernel-related information, `trusted` is restricted through `CAP_SYS_ADMIN`, and `user` holds metadata such as MIME type, encoding, or checksums. Values need not always be text strings.

At 01:03:44–01:04:31, the checksum explanation separates calculation, storage, key listing, and value retrieval:

```sh
md5sum file.txt
setfattr -n user.checksum.md5 -v CHECKSUM file.txt
getfattr file.txt
getfattr -n user.checksum.md5 file.txt
```

The first command's computed string supplies the role represented by `CHECKSUM` in the second. `user` is the namespace; `checksum.md5` is the attribute name within it. In the source example, general retrieval lists keys, while `-n` retrieves the specified key's value. Unclear checksum speech is not reconstructed.

M001 slide 39 additionally removes the attribute with `setfattr -x user.checksum.md5 file.txt`. The subsequent disappearance from the key list and `No such attribute` response are a materials-only walkthrough, not newly verified spoken steps. A stored digest neither updates automatically when file contents change nor guarantees authenticity. Recomputing the current contents for comparison and trusting permission to change the metadata are separate issues.

## Key Takeaways

- Changing file contents differs from removing a directory entry.
- Sticky, SUID/SGID, and noexec/nosuid constrain different operations.
- Separate numeric identities from names and returned pointers from copied strings.
- A metadata predicate classifies potential risk; it does not certify safety.
- ACLs control access; xattrs hold metadata, and a stored digest does not automatically verify contents.

## Recall and Practice

### Recall and explanation

#### Recall Q01 · File and directory rwx

Compare r/w/x for files and directories. Why can a read-only file's name sometimes be removed? Explain `chmod g+w`, `chmod 750`, `S_IRWXU`, and `S_ISREG` versus `S_IRUSR`.

<details><summary>Show solution</summary>

File bits concern reading/writing contents and execution; directory bits concern listing names, changing entries, and search/traversal. Entry operations need parent write/search and other conditions such as sticky, so the target's content-write bit alone does not decide removal. `g+w` adds group write; 750 means rwx/r-x/--- using 4+2+1. `S_IRWXU=00700` groups owner bits; `S_ISREG` tests type and `mode & S_IRUSR` tests owner read.

**Checking points:** Check all six meanings, namespace versus contents, and type versus permission tests.

</details>

#### Recall Q02 · Restrictions on a shared directory

Does sticky make every file in a world-writable directory read-only? What do `S_ISVTX`, `S_IWOTH`, `ST_NOEXEC`, and `ST_NOSUID` test?

<details><summary>Show solution</summary>

No. Sticky mainly restricts rename/delete to permitted cases such as file owner, directory owner, or privileged processes. Content writes have separate checks. The first masks test sticky and other-write; the filesystem flags concern execution and set-ID restrictions. Neither world-write nor sticky alone establishes safety across all execution paths.

**Checking points:** Distinguish sticky's operations from file modes and filesystem policy.

</details>

#### Recall Q03 · Whose identity is used?

The caller is A/G and executable ownership is B/H. Assuming permitted set-ID execution, give effective user/group for 4755, 2755, and 6755 and the real identities. Name the query functions and nosuid qualification.

<details><summary>Show solution</summary>

Effective identities are B/G, A/H, and B/H, respectively; real A/G remain. 4 means SUID, 2 SGID, and 6 both. `getuid/getgid` query real identities; `geteuid/getegid` query effective identities. Ownership by H does not change the group under 4755 alone. `nosuid` can suppress the effects; SUID refers to the file owner, not automatically root.

**Checking points:** Check all three pairs, four functions, and ownership versus the SGID bit.

</details>

#### Recall Q04 · Lifetime of lookup results

Why might a saved `pw_name` appear to change after looking up the effective user? Explain `strdup`, NULL lookup results, allocation failure, and `user ? user : "n/a"`.

<details><summary>Show solution</summary>

`getpwuid/getgrgid` may return library-managed storage reused by subsequent lookups; copying its pointer does not preserve the characters. `strdup` creates an independent copy after a successful lookup, with allocation checks and eventual free. Check lookup NULL before member access and copy failure separately. The conditional tests an initialized pointer; it does not repair an uninitialized user variable.

**Checking points:** Distinguish pointer and character copies and all three failure cases.

</details>

#### Recall Q05 · Potential-risk predicate

Decompose the scanner predicate into type, owner/set-ID, and filesystem flags. What if a root-owned regular file lacks SUID or is on nosuid? Explain `AT_SYMLINK_NOFOLLOW`, `getNext`, and error/mount limitations.

<details><summary>Show solution</summary>

Require a regular file, then `(root UID && SUID) || (root GID && SGID)`, and then neither noexec nor nosuid. Root ownership without SUID fails the user branch; nosuid fails the final filter. NOFOLLOW examines link metadata itself; getNext is a source helper. Omitted parentheses/error checks and entries crossing mounts prevent treating this as a complete scanner or proof of exploitation or safety.

**Checking points:** Preserve AND/OR grouping, both counterexamples, and the source limitations.

</details>

#### Recall Q06 · ACLs and namespaces

After `chmod 640`, how does the example add and inspect a named USER's read ACL? Explain `+` and the mask, then distinguish security/system/trusted/user xattrs from ACLs.

<details><summary>Show solution</summary>

Use `setfacl -m u:USER:r file.txt` and `getfacl file.txt`. `+` indicates an extended ACL; its mask can constrain effective entry permissions. ACLs refine basic owner/group/other access. Xattrs carry additional metadata: security information, kernel-related system data, trusted data restricted through CAP_SYS_ADMIN, and user metadata such as MIME, encoding, or checksums. Values need not be strings.

**Checking points:** Check both commands, the mask's effect, and access control versus metadata.

</details>

#### Recall Q07 · Checksum calculation, storage, retrieval, removal

Split the namespace/name of `user.checksum.md5` and explain calculation, storage, key listing, value retrieval, and removal commands. What supports the removal step, and what does storing the value fail to guarantee?

<details><summary>Show solution</summary>

user is the namespace and checksum.md5 the attribute name. Compute with `md5sum file.txt`, then store its result using `setfattr -n user.checksum.md5 -v CHECKSUM file.txt`. In the source, `getfattr file.txt` lists keys, `getfattr -n user.checksum.md5 file.txt` retrieves the value, and `setfattr -x user.checksum.md5 file.txt` removes it. It then disappears from the list and named retrieval reports No such attribute. Calculation/storage/retrieval also have September 14 speech support; removal is slide-only. Stored values do not update automatically or guarantee authenticity; recomputation and trust in metadata modification rights remain separate.

**Checking points:** Check key versus value retrieval, the removal evidence limit, and lack of automatic updating.

</details>

### Apply and check

#### Practice P01 · Separating identity from deletion permission

**Newly written synthetic practice.** Transfer execution-identity and defect-consequence reasoning from Q3(e) [EX:sp_2025_2_midterm_q03 p.8]. Prerequisites are rwx, set-ID, and sticky; no real binary configuration or exploit is assumed.

A/G executes a regular executable owned by B/H with mode 4755. Set-ID is permitted and B has greater authority than A. (a) Give real/effective identities. (b) Does placing it in a world-writable sticky directory by itself reduce the consequences of an internal defect? (c) Can this mode alone decide whether A may delete another user's entry?

<details><summary>Show solution</summary>

(a) Real A/G, effective B/G. (b) No. Sticky restricts directory rename/delete, not all erroneous operations performed with B's effective authority. A defect can therefore have consequences within B's greater authority. (c) No. Check parent write/search, sticky ownership conditions, and the actual acting identity. Potential privilege consequences and permission to delete are separate decisions.

**Checking points:** State B/G, sticky's narrow role, and the missing directory conditions.

</details>

### Review plan

Organize Q01–Q03 by object, operation, and identity before applying P01. Draw the pointer/copy lifetimes in Q04, then match Q06–Q07's commands to purposes without viewing the solutions.

## Sources

[[courses/system_programming/lectures/en/2026-09-14-lecture-04|2026-09-14 · lecture note]]

[[courses/system_programming/lectures/en/2026-09-16-materials-io-review|2026-09-16 · inferred materials review]]

[03.IO.Unix.Filesystem.Concepts.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/03.IO.Unix.Filesystem.Concepts.pptx) — slide 29; slide 31; slide 34; slide 35; slide 36; slide 37; slide 39; slide 38

[05.IO.Files.and.Directories_3d312c60.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/05.IO.Files.and.Directories_3d312c60.pptx) — slide 6

[[courses/system_programming/transcripts/2026-09-14|2026-09-14 · corrected transcript]] — 01:03:44, 01:04:31

The September 16 note is an inferred materials review without a recording, not exact spoken progress. Checksum removal is slide-only and uncertain checksum values remain unresolved. Read the source's broad sticky-risk, root-binary SUID, and basic-mode/extended-ACL claims with the stated qualifications. The scanner omits checks and has mount-scope limits; it does not assess a real system's safety. Historical binary settings are not current-environment facts.

Historical exam connections below use only the stated reasoning demands. Supplied answers are reference material, not independently certified solutions; current exam scope or frequency cannot be inferred.

[[exam_questions/sp_2025_2_midterm_q03|2025-2 Midterm Q3 · Files and I/O (existing preview)]]
