---
title: "Virtual Memory, Page Translation, Sharing, and Protection"
description: "Review page translation, faults, shared mappings, and the historical TLB/data-cache address path."
course: "system_programming"
unit_id: "virtual-memory"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["07.MM.Virtual.Memory.Recap.pptx", "07.MM.Virtual.Memory.Recap_2ffc3cf7.pptx", "06.MM.Variable.and.Memory.Recap.pptx"]
private_source_assets: []
source_lectures: ["courses/system_programming/lectures/en/2026-09-23-lecture-06", "courses/system_programming/lectures/en/2026-09-28-lecture-07"]
---

Virtual Memory separates program addresses from storage locations while supporting both isolation and sharing. Follow an access by separating address fields, residency, permissions, translation caches, and data caches.

## Separating virtual addresses from physical locations

If memory is viewed as a large byte-addressed array, a load moves data from memory to a register and a store moves register data to memory. The material's `ld`/`sd` examples illustrate these roles rather than every architecture's instruction syntax. A full 64-bit byte address expresses `2^64 bytes = 16 EiB`. This is representational address space, not installed DRAM capacity.

Each process has instruction text, global data, heap, and stack. Managing these [memory-layout regions](memory-layout.md) within one physical memory creates two requirements: isolation/protection against arbitrary access to another process, and sharing of designated data among cooperating processes. The [[courses/system_programming/lectures/en/2026-09-28-lecture-07|2026-09-28 Virtual Memory lecture]] and [[courses/system_programming/transcripts/2026-09-28|transcript]] at 01:07–09:46 connect these motivations.

Indirection inserts a mapping between an address used by a program and its actual location. Virtual Memory abstracts physical memory, while a Virtual Address (VA) is separated from a Physical Address (PA). A process sees its own memory world, with translation behind each access. Private spaces can still contain explicitly configured shared regions.

The lecture compares this to an IP layer above heterogeneous LAN addressing schemes. Distinguishing a NIC's 48-bit MAC address from an upper-layer IP address conveys the separation of a common upper address from a concrete lower address. Its virtual-machine analogy similarly describes a logical machine over a physical one: a conceptual construction can provide memory-like or machine-like functionality. These analogies do not add a complete networking or virtualization implementation. Incomplete load/store wording, “64 different bytes,” and unclear LAN phrases are not reconstructed as precise instructions or quantities.

## Translating addresses in pages

Mapping every byte independently would require excessive management. A page is the fixed-size mapping unit; the lecture's ordinary example is 4 KiB, with 2-MiB and 1-GiB large pages. A simple page table uses a Virtual Page Number (VPN) to obtain a Physical Page Number (PPN). One entry is a PTE. The source mappings VPN 0→PPN 2, VPN 1→PPN 1, and VPN 2→PPN 5 demonstrate that virtual order need not match physical placement (10:25–11:52).

### Calculating the translation of `0x233`

The small example on RM001/NM003 slides 14–15 uses `PS = 0x100 = 256 bytes`, distinct from the ordinary page-size examples above. Separate three operations:

1. `VPN = floor(0x233 / 0x100) = 2`
2. `offset = 0x233 % 0x100 = 0x33`
3. `PPN = PT[2] = 5`, so `PA = 5 * 0x100 + 0x33 = 0x533`

Equal virtual and physical page sizes preserve the offset. PPN 5 is a page **number**; `0x500` is its **base address**. If PT returns a PPN, the corresponding general formula is:

$$
PA = PT[\lfloor VA/PS\rfloor]\,PS + (VA\bmod PS).
$$

Slide 14 prints `2 (= 0x233 & 0xF00)`, omitting the shift from the actual mask result `0x200`. For this toy address, `(0x233 & 0xF00) >> 8` gives two. Slide 15's `PA = PT[VA/PS] + VA%PS` works unchanged only if PT returns a page base; its stated VPN→PPN definition requires multiplication by page size. These are explicit explanatory corrections based on the original definition and example. They do not rewrite the division/remainder confusion or “Inside page 1” wording at 13:47–16:16 into recovered speech.

## Distinguishing the MMU, page table, and TLB

The Memory Management Unit (MMU) is hardware performing VA→PA translation. The page table itself is a data structure in main memory. A Page-Table Base Register (PTBR) supplies the starting location; the Intel example names CR3. Distinguish OS-managed mapping data, the register locating it, and the hardware using it (17:16–18:05).

Repeated memory accesses to page tables can make translation expensive before the requested data access even begins. A Translation Lookaside Buffer (TLB) caches frequently used translation information. A hit uses a cached translation; a miss requires the page-table path. This is different from a data cache holding program bytes, and the TLB does not contain every PTE. The unclear “both times” at 19:02–19:55 is not changed into “most times” or a numerical hit-rate claim.

## Per-process mappings provide isolation and sharing

Each process has its own address space and page table. The PTBR identifies the running process's table, allowing the same VPN to map to different PPNs. Conversely, PTEs from two processes can designate the same physical page for sharing.

In the source sharing example, A's VPN 1 and B's VPN 1 both use PPN 1. A's VPN 4 and B's VPN 6 both use PPN 6. The latter case shows that sharing does not require identical VAs. The sharing table and the earlier isolation table are different states; do not combine their mapping numbers (54:08–55:05).

A separate toy example gives A, B, and C seven virtual pages each. With `PS=0x100`, each space is `0x700` bytes and the sum is 21 pages, or `0x1500` bytes. Physical memory contains eleven pages, or `0xB00` bytes. There is no contradiction: the model does not reserve a separate resident DRAM page for every virtual page in every process. Page tables themselves also occupy physical memory, and the example shows only some active mappings. It does not say all virtual pages are simultaneously resident in distinct physical frames (56:00).

### Address-space scale motivates multilevel tables

Dividing a full 64-bit byte space into 4-KiB pages gives `2^64 / 2^12 = 2^52` possible pages, approximately `4.5 × 10^15`. The historical Core i7 model used later has a different, **48-bit VA**. Its twelve offset bits leave a 36-bit VPN and `2^36` possible VPNs. The byte space is `2^48 bytes = 256 TiB`, not 256 trillion pages. The uncertain “256 terapheases” wording at 57:02–59:51 does not become a confirmed unit.

Even a small `ls` or `cat` would require an excessive flat array if it included an entry for every possible VPN. Multilevel page tables organize mappings hierarchically in response to this scale. Processes also need to avoid unnecessary copies of common pages, such as libc code used by `printf`. Lazy copy and copy on write (COW) are introduced as motivation and a promise of later explanation. Detailed copying on a write fault is not added here, and `fork` is not said to eagerly duplicate every physical page in all cases.

## Residency, page faults, and protection faults

When active programs demand substantial DRAM, some pages can be moved to disk while physical memory acts as a cache. The paging example's VA `0x233` is in a different state from the earlier successful mapping to PPN 5: here VPN 2 records paged-out status and a disk location.

Access to the absent page causes a page fault and temporarily suspends that execution. The OS obtains space if necessary through replacement such as [clock](cache-hierarchy.md), reads the page from disk, and updates the PTE. Retrying the faulting instruction can then complete the access (01:00:47–01:05:06). This is a recoverable nonresident-page case, not a rule that every fault terminates the process or requires disk I/O.

### Choosing a victim is different from preserving its data

Victim selection does not always require a disk write. A file-backed page unchanged since reading the original file can be discarded and read again later. The same reasoning applies when disk already holds the identical clean contents. Modified data, however, needs preservation before it is discarded. The lecture at 01:05:06–01:05:59 connects this distinction to I/O cost. Understanding clean versus modified contents does not require adding the complete later PTE D-bit layout.

### Having a mapping does not authorize a write

A PTE carries access information as well as a PPN. Pages can differ in read, write, and execute permissions. In the separate protection example, VPN 2 maps to PPN 7 but has only R permission. A store of RAX to the memory designated by RDX violates that permission; the CPU raises an exception and the OS handles it. The lecture simplifies this case as process termination (01:06:53–01:08:38).

This differs from a valid nonresident access followed by page-in and retry. Whether an address has a mapping, whether its page is resident, and whether the requested operation is permitted are separate questions. Avoiding stack execution is mentioned as a motivation, but unclear speech does not establish an additional exploit lesson.

## A private pointer can designate a shared object

At 01:08:38–01:18:04, the lecture returns to `layout.c` with actual mapping explanations. The source allocates `sizeof(struct __shared)` through `mmap`, using `PROT_READ|PROT_WRITE` and `MAP_ANONYMOUS|MAP_SHARED`. The structure contains semaphore `m` and `shared_int`. `sem_init(&shared->m, 1, 1)` specifies process-shared use and initial value one; `shared_int` starts at zero. The lecture initially treats the semaphore as a lock. The original also contains `MAP_FAILED` checking, delay, and sleep, without establishing that every line was read aloud.

The subsequent `fork` loop creates one additional process when `nproc=2`. The processes have separate address spaces. VPN 2, containing `global_int` and pointer variable `shared` itself, maps to PPN 1 for A and PPN 7 for B. VPN 3, containing the pointed-to structure, maps to PPN 2 in both. **Pointer storage can be private while its pointee is shared.** Identical names or VAs do not establish identical physical storage.

Each process increments its own `global_int` independently. The shared increment occurs between `sem_wait` and `sem_post` on the semaphore within the shared region, preventing simultaneous updates in the illustrated use. Private counters advance independently while the shared counter combines their work. No particular output interleaving is guaranteed. “So, the result is different” is unclear about pointer storage versus pointer value and does not prove the pointer values differ. The copying explanation describes logical private semantics, not mandatory eager copying of all physical pages.

## Two cache hierarchies in a historical Core i7 model

Translation information and actual data now have distinct places to be cached. RM001/NM003 slide 39 and 01:18:04–01:21:26 use a four-core Core i7 model from roughly 2009, not the specifications of every current Core i7.

| Structure | Supplied capacity and associativity | Scope |
|---|---|---|
| L1 instruction / data cache | 32 KiB each, 8-way | Separate per core |
| L2 unified cache | 256 KiB, 8-way | Per core |
| L3 unified cache | 8 MiB, 16-way | Shared by cores |
| L1 DTLB / ITLB | 64 / 128 entries, each 4-way | Data / instruction translations |
| L2 unified TLB | 512 entries, 4-way | Translations |

The lecture relates branch-free sequential instruction access to easier prediction than general data access. The source also gives a DDR3 memory-controller total of 32 GB/s and QPI connections to other cores and an I/O bridge. These are historical configuration context, not claims that every figure label was spoken.

### From VA to a TLB set and tag

In this model, `48 = 36 + 12`: a 36-bit VPN and a 12-bit VPO. Split the VPN into a 32-bit TLBT and a 4-bit TLBI. The index selects one of `2^4=16` sets; valid translation tags are compared across that set's four ways. Total capacity is `16×4=64 entries`, with up to four translations in one set. At 01:22:13–01:23:55, “at least four” is immediately corrected to “up to four.” The utterance “32 bits is now divided…” conflicts with the 36-bit VPN diagram and is not used to derive the split.

A hit yields a 40-bit PPN. A miss uses the 36-bit VPN as four nine-bit portions for a page-table walk. CR3 supplies the starting location; successive selections reach the final PTE and its PPN. The obtained translation can be cached in the TLB for subsequent access (01:24:41–01:25:41). Absence from the TLB does not imply absence from DRAM: a resident page can be reached by a table walk. Four levels and nine-bit divisions were actually explained, but the later directory-span calculations and complete PTE flags are not added here.

The optional exam connection is Q4(a)'s field identification at [EX:sp_2025_1_midterm_q04 p.11], Q4(b–c)'s PA and given-VA analysis at [EX:sp_2025_1_midterm_q04 p.12], and Q4(d)'s TLB/page-table decision at [EX:sp_2025_1_midterm_q04 p.13]. Recompute offset, VPN, and PPN widths from **that question's** page size and address widths; check valid and tag in the selected set; then inspect the page table if needed. Do not assert a PA before validating the mapping. The exam's small address model and this Core i7 model have different bit counts, and the private tables and answers are not reproduced here.

### From PA to the requested data-cache byte

The 40-bit PPN and unchanged 12-bit PPO form a 52-bit PA. L1 data-cache fields are CT=40 bits, CI=6 bits, and CO=6 bits. CI selects one of `2^6=64` sets; CT is the physical tag compared across eight ways; CO selects a byte within a 64-byte line. Capacity is `64×8×64 = 32768 bytes = 32 KiB`.

The TLB's 64 **entries** and the data cache's 64 **sets** are different counts. A translation hit provides address information; a data-cache hit provides contents. A request for one `char` may need one byte, not the entire line returned to the program. An L1 miss continues toward L2, L3, and main memory (01:26:40–01:29:55).

The lecture explains a logical sequence of obtaining PA and looking up data, while also mentioning overlap using unchanged page-offset bits. Physical tagging does not require every index operation to wait until translation completes. The unclear “six step order” is not reconstructed as a formal six-step algorithm. Distinguishing translation from data selection is what makes the end-to-end address path understandable.

## Key Takeaways

- Address range differs from installed DRAM, and sharing does not require equal VAs.
- VPN→PPN translation preserves page offset; page numbers differ from base addresses.
- The MMU is hardware, the page table a memory data structure, and the TLB a translation cache.
- A TLB miss, a nonresident-page fault, and a prohibited write are distinct events.
- A private pointer object can designate a shared pointee.
- Keep the historical 48-bit VA/52-bit PA model separate from toy-model widths.

## Recall and Practice

### Recall and explanation

#### Recall Q01 · Purpose of address abstraction

Distinguish load/store, full 64-bit byte-address scale, and installed DRAM. Explain process regions, protection/sharing, indirection, and the common point of the LAN/IP and virtual-machine analogies.

<details><summary>Show solution</summary>

Load moves memory→register; store moves register→memory. The representable range is 2^64 bytes=16 EiB, not that much installed RAM. Managing process text/data/heap/stack requires protection from arbitrary cross-process access and designated sharing. Mapping separates process VAs from physical locations. IP/MAC and logical/physical-machine analogies likewise separate an upper interface from concrete implementation. Private spaces can still contain explicit shared regions; the analogies do not teach complete networking or virtualization.

**Checking points:** Explain what 16 EiB measures and both requirements/address domains.

</details>

#### Recall Q02 · Page number, offset, and base

Explain the mapping unit and VPN/PTE/PPN, then translate VA 0x233 with PS=0x100 and PT[2]=5. What corrections/qualifications are needed for `0x233 & 0xF00` and `PT[VA/PS]+VA%PS`?

<details><summary>Show solution</summary>

A page is the fixed mapping unit; VPN is the input page number, a PTE one entry, and PPN the output number. VPN=floor(0x233/0x100)=2, offset=0x33, base=5×0x100=0x500, PA=0x533. The mask yields 0x200, so >>8 is needed for 2. If PT returns a PPN use `PT[VPN]*PS+offset`; only a base-returning table fits the printed addition directly. Equal page sizes preserve offset. The toy 256-byte page differs from ordinary 4 KiB and large 2 MiB/1 GiB examples.

**Checking points:** Check 2/0x33/0x500/0x533 and both printed-formula issues.

</details>

#### Recall Q03 · MMU, table, register, and TLB

What does each of the MMU, main-memory page table, PTBR/CR3, and TLB hold or do? Explain work avoided by a TLB hit and the distinction from a data cache.

<details><summary>Show solution</summary>

The OS-managed table is mapping data in main memory. PTBR/CR3 gives its starting location, and the MMU is translation hardware using it. The TLB retains some frequently used translations to reduce repeated table walks. It neither stores every PTE in registers nor caches the program's actual data bytes. A TLB hit supplies translation information; a data-cache hit supplies contents.

**Checking points:** Distinguish all four roles and translation versus contents.

</details>

#### Recall Q04 · Shared VAs and virtual capacity

Compare A VPN 1/B VPN 1→PPN 1 with A VPN 4/B VPN 6→PPN 6. With three processes of seven pages each, PS 0x100, and eleven physical pages, calculate virtual/physical sizes and explain why this is consistent.

<details><summary>Show solution</summary>

The first shares through equal VPNs; the second through different VPNs to the same PPN. Physical mapping determines sharing, not equal VAs. Each space is 0x700 bytes; total virtual space is 21 pages=0x1500 versus physical 0xB00. The model does not reserve a distinct resident frame for every virtual page simultaneously, and tables also consume physical memory. Isolation and sharing diagrams are different mapping states.

**Checking points:** Check both sharing relations, the three sizes, and the residency qualification.

</details>

#### Recall Q05 · Table scale and avoiding duplication

With 4 KiB pages, calculate page counts for full 64-bit and historical 48-bit VAs and the latter's byte space. Contrast motivations for multilevel tables and libc sharing; what is the taught COW scope?

<details><summary>Show solution</summary>

Twelve offset bits leave 2^52 pages for 64-bit VAs and 2^36 for 48-bit VAs; the latter spans 2^48 bytes=256 TiB, not 256 trillion pages. A flat entry for every possible VPN is excessive even for small programs, motivating hierarchical tables. Sharing common libc/printf pages reduces duplicate contents. COW/lazy copy appears as a name, motivation, and later topic, not a taught write-fault implementation or an unconditional eager-copy rule for fork.

**Checking points:** Separate pages from bytes and mapping-table size from duplicated contents.

</details>

#### Recall Q06 · Page-in and clean eviction

In the separate state where VPN 2 is paged out, what must occur before retrying VA 0x233? Compare clean file-backed and modified victims, and qualify general claims about all faults.

<details><summary>Show solution</summary>

Execution pauses on the fault; obtain space through replacement if needed, read the page from disk, update the PTE, and retry the instruction. Do not mix this state with the earlier VPN 2→PPN 5 mapping. Clean pages backed by identical disk contents can be discarded and reread without new writeback; modified contents need preservation first. This is a recoverable disk-backed case, not a rule that every fault needs disk I/O or termination.

**Checking points:** State all recovery steps and the clean/modified preservation distinction.

</details>

#### Recall Q07 · A prohibited write to a resident page

VPN 2 maps to PPN 7 with R-only permission. Why is a mapping insufficient for storing RAX through RDX? Compare this with a nonresident-page fault.

<details><summary>Show solution</summary>

The page can be located but writing is not permitted. The CPU raises an access exception and the OS handles it; the source simplifies this case as termination. A permitted nonresident access may instead page in, update the PTE, and retry. Mapping existence, residency, and operation permissions are separate decisions.

**Checking points:** Identify absent write permission and distinguish both fault paths.

</details>

#### Recall Q08 · Preparing the shared mapping

Explain layout.c's mmap size/protection/flags, structure contents/initialization, and process count for nproc=2. What is the bounded claim about semaphores and source code?

<details><summary>Show solution</summary>

Use sizeof(struct __shared), PROT_READ|PROT_WRITE, and MAP_ANONYMOUS|MAP_SHARED. The structure contains m and shared_int;`sem_init(&shared->m,1,1)` specifies process sharing and initial value one, and the integer starts at zero. The loop adds one process for a total of two. The semaphore is explained as a lock around shared increments; not every MAP_FAILED check, delay, or sleep line is claimed as spoken teaching.

**Checking points:** Check flags, members, initial values, two processes, and scope limits.

</details>

#### Recall Q09 · Private pointer, shared pointee

VPN 2 maps A→PPN 1, B→PPN 7; VPN 3 maps both→PPN 2. Globals and pointer shared lie in VPN 2, while m/shared_int lie in VPN 3. Which state is private/shared and how are increments protected? What is not guaranteed about pointer values/output order?

<details><summary>Show solution</summary>

Globals and pointer objects occupy separate physical storage, but their pointee structure is in shared PPN 2. Each global_int advances independently; shared_int combines work. The shared semaphore protects sem_wait–increment–sem_post against simultaneous updates in this example. Private pointer storage does not imply different stored VA values, nor does the example guarantee output interleaving or eager copying of every physical page.

**Checking points:** Distinguish storage, pointer value, and pointee, and identify the semaphore as shared.

</details>

#### Recall Q10 · The historical Core i7 hierarchy

Give capacities/ways/sharing for L1I/L1D, L2, L3 and entry counts/ways for DTLB/ITLB/L2 TLB in the supplied four-core model. What is the context for instruction locality and DDR3/QPI figures?

<details><summary>Show solution</summary>

Per core, L1I and L1D are each 32 KiB/8-way and unified L2 is 256 KiB/8-way; shared L3 is 8 MiB/16-way. L1 DTLB/ITLB have 64/128 entries and unified L2 TLB 512; each is 4-way. Sequential branch-free instruction access motivates easier prediction than general data. DDR3 total 32 GB/s and QPI connections describe the roughly 2009 model, not all current Core i7s or proof every diagram label was spoken.

**Checking points:** Distinguish data-capacity units from translation entries and check sharing scopes.

</details>

#### Recall Q11 · TLB fields and the table walk

Derive VPO/VPN/TLBI/TLBT widths and set count for 48-bit VAs, 4 KiB pages, and a 64-entry 4-way TLB. Give PPN width on hit and the four-level/CR3 path on miss. Why is a miss not always a page fault?

<details><summary>Show solution</summary>

VPO=12 and VPN=36. There are 64/4=16 sets, so TLBI=4 and TLBT=32, with at most four translations per set. A hit yields a 40-bit PPN. A miss splits the 36-bit VPN into four 9-bit portions for a walk starting at CR3; the final PTE supplies a translation to cache. A resident page needs no disk page-in merely because the TLB lacked it. Retain the source's correction from at least to up to and distinguish inconsistent 32-bit speech from the 36-bit diagram.

**Checking points:** Verify all four decompositions and the resident-TLB-miss case.

</details>

#### Recall Q12 · From PA to a data byte

A 40-bit PPN plus 12-bit PPO forms PA with CT 40/CI 6/CO 6. Explain fields, sets/ways/line size/capacity, contrast TLB 64 entries, and describe L1 misses and possible overlap.

<details><summary>Show solution</summary>

PA has 52 bits; CI 6 selects 64 sets, CT 40 compares physical tags across eight ways, and CO 6 selects a byte in a 64-byte line. Capacity is 64×8×64=32768 bytes=32 KiB. TLB 64 counts translation entries; here 64 counts data sets. A `char` request may need one byte; L1 misses continue to L2/L3/main memory. Unchanged VPO=PPO bits can support overlap of indexing and translation, so physical tagging does not force every lookup operation to wait.

**Checking points:** Check 52-bit composition, 32 KiB capacity, the two meanings of 64, and the overlap qualification.

</details>

### Apply and check

#### Practice P01 · Separating a TLB miss from faults

**Newly written synthetic practice.** Use address-field and TLB→PTE decisions from Q4(a) [EX:sp_2025_1_midterm_q04 p.11], Q4(b–c) [EX:sp_2025_1_midterm_q04 p.12], and Q4(d) [EX:sp_2025_1_midterm_q04 p.13]. Prerequisites are the chapter's offset, set/tag, residency, and permission concepts; this model differs from Core i7.

Use 12-bit VAs, 10-bit PAs, 64-byte pages, and a 4-entry/2-way TLB initially all invalid. VPN 0x12 is resident PPN 5/RW; VPN 0x13 is a permitted page paged out to disk; VPN 0x14 is resident PPN 7/R. No other access or mapping change occurs; successful walks fill the TLB.

Classify reads at 0x4A7, 0x4B2, 0x4E0, then a write at 0x501. Only classify the final two faults without handling them. Give field widths, the first set/tag/PA, the second-hit reason, and the two distinct failure causes.

<details><summary>Show solution</summary>

Offset=6 bits, VPN=6, PPN=4. Two TLB sets require index 1 and tag 5. VA 0x4A7 has VPN 0x12, offset 0x27, set 0, tag 0x9. The initial miss walks to a resident RW PTE, giving PA=5×64+0x27=0x167 and filling the translation. VA 0x4B2 uses the same VPN with offset 0x32, so it hits and gives PA 0x172. VA 0x4E0 has VPN 0x13, offset 0x20 and faults on nonresidency; do not assert a current resident PA. VA 0x501 has VPN 0x14, offset 1 but R-only protection forbids writing despite residency. Address arithmetic and permission are distinct; not every TLB miss is a disk fault.

**Checking points:** Verify 6/6/4 and 1/5, 0x167/0x172, same-page reuse, and both fault causes.

</details>

### Review plan

Solve Q02, Q04, and Q05 with explicit units, then classify faults in Q06–Q07. Draw pointer boxes and shared pages for Q08–Q09; draw separate translation/data paths for Q10–Q12 before combining them in P01's access table.

## Sources

[[courses/system_programming/lectures/en/2026-09-23-lecture-06|2026-09-23 · lecture note]]

[[courses/system_programming/lectures/en/2026-09-28-lecture-07|2026-09-28 · lecture note]]

[[courses/system_programming/transcripts/2026-09-28|2026-09-28 · corrected transcript]] — 01:07–19:55 (abstraction and translation), 54:08–01:08:38 (sharing, capacity, faults), 01:08:38–01:18:04 (shared mapping example), 01:18:04–01:29:55 (Core i7 path)

[07.MM.Virtual.Memory.Recap.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/07.MM.Virtual.Memory.Recap.pptx) — slide 4; slide 5; slide 7; slide 8; slide 10; slide 11; slide 16; slide 27; slide 28; slide 29; slide 30; slide 31; slide 32; slide 34; slide 35; slide 37; slide 39; slide 40

[07.MM.Virtual.Memory.Recap_2ffc3cf7.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/07.MM.Virtual.Memory.Recap_2ffc3cf7.pptx) — slide 4; slide 5; slide 7; slide 8; slide 10; slide 11; slide 16; slide 27; slide 28; slide 29; slide 30; slide 31; slide 32; slide 34; slide 35; slide 37; slide 39; slide 40

[06.MM.Variable.and.Memory.Recap.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx) — slide 11; slide 7

Uncertain September 28 load/store, LAN, page units, TLB frequency, pointer-value, and six-step speech is not recovered. Missing mask shifts and PPN/base formulas receive explicit explanatory corrections without altering originals. Isolation, sharing, paged-out, and protection diagrams represent different states. Core i7 is historical; unclear diagram labels do not establish additional properties. COW implementation, later PTE flags, allocator algorithms, and full synchronization theory remain outside scope. The 2024 duplicate VPN 1F/invalid-PA notation and 2025-2 Q4 score discrepancy remain unrepaired, and supplied answers are not copied as certified solutions.

Historical exam connections below use only the stated reasoning demands. Supplied answers are reference material, not independently certified solutions; current exam scope or frequency cannot be inferred.
