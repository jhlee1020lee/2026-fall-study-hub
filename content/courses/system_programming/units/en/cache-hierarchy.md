---
title: "Memory Hierarchy, Locality, and Cache Replacement"
description: "Review cache decisions from locality and block transfers to conflicts, LRU, and clock."
course: "system_programming"
unit_id: "cache-hierarchy"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["07.MM.Virtual.Memory.Recap.pptx", "07.MM.Virtual.Memory.Recap_2ffc3cf7.pptx"]
private_source_assets: []
source_lectures: ["courses/system_programming/lectures/en/2026-09-28-lecture-07"]
---

A memory hierarchy balances cost and speed by keeping frequently used data in small, fast storage. Distinguish locality, placement, and replacement while tracing hits, misses, and evictions.

## Why memory needs a hierarchy

Making all memory as fast as registers would be convenient, but capacity, speed, and cost per byte must be considered together. A memory hierarchy combines small, fast storage with larger, relatively inexpensive storage. Whereas [memory layout](memory-layout.md) distinguishes objects' roles within a process, the hierarchy reduces the cost of reaching their data.

The [[courses/system_programming/lectures/en/2026-09-28-lecture-07|2026-09-28 memory-hierarchy lecture]] and [[courses/system_programming/transcripts/2026-09-28|transcript]] at 19:55–25:38 contrast registers, SRAM CPU caches, DRAM main memory, local storage, and remote storage. Cycle-scale register/cache access, roughly 100 cycles or tens of nanoseconds for DRAM, microseconds for SSDs, and milliseconds for HDDs are lecture-scale comparisons, not measurements of every current device. HDDs have mechanical seek and rotational delays; SSDs lack those mechanical components. Do not confuse the source's hierarchy-level numbering with CPU L1/L2/L3 cache names.

### Remote storage is not invariably slowest

In the disaggregation example, compute nodes provide CPUs and memory while disk storage is collected across a network. The OS sees a disk-like service, but I/O travels through the network. Centralized replacement, maintenance, and capacity adjustment motivate the arrangement. At 22:55–25:38, the lecture explains that a sufficiently fast network can make a remote access faster than a local disk access. “Local always beats remote” is therefore not an absolute rule.

The transcript's “400/800 gigabits per minute” and remote-swap phrase remain uncertain. They are not silently converted to per-second units or a specific implementation. Unclear wording about tape prevalence likewise does not supply a firm hardware specification.

## Locality makes a small cache useful

A cache is small, fast storage temporarily holding some data from larger, slower storage. Holding a hot subset can satisfy many accesses without holding everything. Temporal locality means recently referenced items tend to be used again soon; spatial locality means nearby addresses tend to be accessed close together in time.

Consider the array-sum fragment on [system_programming:RM001 slide 18](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/07.MM.Virtual.Memory.Recap.pptx), also present in NM003. It assumes a valid array and bounds and a suitable representable sum.

```c
sum = 0;
for (i = 0; i < n; i++)
    sum += a[i];
```

`sum` is used repeatedly, illustrating temporal locality. Even if each `a[i]` is read only once, `a[i+1]` follows soon, illustrating spatial locality. Repeated loop instructions show temporal locality; consecutive instructions on a branch-free path show spatial locality. The transcript at 26:35–29:32 distinguishes the data and instruction examples. Locality is a program-dependent tendency, not a guarantee.

The relationship “level k holds a subset of level k+1” extends beyond CPU caches. Registers hold values obtained from lower memory levels; main memory caches disk data; local disks can hold remote-file copies. The design concentrates cost on hot data rather than making every byte maximally fast (30:31–31:27). The unfinished “K+” phrase is not reconstructed as additional speech.

## Block transfers, hits, and misses

Moving blocks amortizes access-startup costs across several bytes. Fixed-size blocks simplify indexing and management and are common in hardware caches. Variable-size blocks can fit objects such as whole web images but complicate management. The supplied examples are an eight-byte register word, a 64-byte cache line, ordinary 4-KiB pages, and large 2-MiB or 1-GiB pages. Sixty-four bytes is the line size, not the entire cache capacity; address width does not dictate every transfer size.

In the source example at 32:27–35:28, level k contains blocks `4,9,10,3`. Requesting 10 hits; requesting 13 misses. If 13 exists at level k+1, the same request has a different result at that level. Placement determines **where** a fetched block may go; replacement or eviction determines **which existing block** leaves when space is needed.

### Three reasons for misses

A cold or compulsory miss occurs on a block's first access because it has not yet been brought in. First execution of a code segment and first access to an array are examples. The working set is the set of currently active blocks. Capacity misses arise when the needed working set cannot remain in the cache together. The source's 1000-byte cache and 1200-byte array illustrate this shortage; these quantities are bytes, not block counts.

Placement restrictions reduce the comparisons needed for lookup. As explained in the [[courses/system_programming/transcripts/2026-09-28|2026-09-28 transcript]] at 38:15–39:15, allowing a block anywhere requires searching tags across many positions; doing those comparisons in parallel needs more expensive, complex hardware. Deriving an index such as `i mod 4` from the block number narrows the positions and tags to inspect, simplifying the lookup circuitry.

A conflict miss arises from placement restrictions rather than total capacity alone. If block i must use position `i mod 4`, blocks 0 and 8 both use position zero. With only one block permitted there, the sequence `0,8,0,8` continually evicts the previous occupant. The first references are compulsory, while subsequent repetition exposes the conflict. Empty positions elsewhere cannot help when the two blocks are not allowed to use them.

At 38:15–40:13, the transcript broadly uses “set associative,” but this single-position, single-block trace has direct-mapped conditions. A multiple-way arrangement able to retain both blocks need not behave the same way. This is an explicit qualification of the source's example, not a recovered utterance.

## Replacement predicts future usefulness

When a full cache must admit another block, it needs a victim. The optimal policy evicts a block never used again or whose next use lies farthest in the future. General programs have branches and inputs whose future access sequence is not known in advance.

Least Recently Used (LRU) instead uses past recency. It evicts the block unused for the longest time, assuming that block is less likely to be needed soon. The assumption can fail. The lecture describes usefulness in typical programs rather than guaranteed prediction (41:06–42:45).

The clear continuation at 44:10–46:30 moves a newly used item to the queue's tail and evicts from the older head. In a newly written explanatory trace, head-to-tail order `[A,B,C]` becomes `[B,C,A]` after a hit on A. If D must then enter, B is the victim. This distinguishes LRU from FIFO, which would not update order on the hit. The orientation can be reversed if insertion, refresh, and eviction stay consistent. Unclear student replies and the intermediate “D cubed.” phrase do not establish a particular deque implementation or pointer operation.

## Pages, page tables, PTEs, and the MMU before clock

Replacing pages when main memory caches disk data first requires a few local definitions. A process's virtual address differs from a physical location. A page is the fixed-size mapping unit. A page table records Virtual Page Number (VPN) to Physical Page Number (PPN) mappings; one row is a Page-Table Entry (PTE). The table is a data structure in main memory. The Memory Management Unit (MMU) is hardware that uses mappings to translate addresses. These distinctions come from 10:25–19:55 and RM001/NM003 slides 10–16.

It now makes sense to record that a page was accessed in a reference/access bit associated with its PTE. Detailed address calculations and full PTE bitfields are unnecessary for the replacement idea here. The address path continues in [Virtual Memory](virtual-memory.md).

### Exact LRU cost and second chance

Maintaining an exact queue on every small read or write can cost more than the original access. Even page-level management must track accesses to data within those pages. Clock, also called second chance, uses inexpensive evidence of recent use instead of maintaining a complete order (47:17–51:15).

Hardware sets the page's reference bit to one on access. Under memory pressure, the OS scans pages. A zero bit permits victim selection; a one bit is cleared and the page survives this turn while the scan proceeds. A later access lets hardware set the bit again. For a newly written short example, begin at the first of three pages with bits `[1,0,1]`: clear the first bit and give that page another chance, then select the second page because its bit is zero. This does not reconstruct exact recency. Clock approximates LRU; it is not exact LRU.

### Different levels have different managers

Compiler register allocation uses code analysis to decide which values remain in registers. Hardware manages CPU L1/L2/L3 caches with defined placement structures for fast lookup. The OS manages main-memory paging and replacement. Disk access is expensive enough that more elaborate LRU-like policies or second-chance bookkeeping can be worthwhile (51:15–54:08). A defined lookup structure does not imply equal actual latency for all hits and misses.

## Keeping cache-lookup conditions separate

Q4(e), [EX:sp_2025_1_midterm_q04 p.13], and Q4(f), [EX:sp_2025_1_midterm_q04 p.14], demand address-field reasoning and hit determination for a separately specified cache. Derive the offset width from block size, the set count from total lines and ways, the index width from set count, and the tag from remaining address bits. Within the selected set, test **valid and tag together** before selecting a byte from the matching line.

Those cache subquestions use address widths and block sizes different from the preceding VM subquestions. Reusing the preceding bit split would be incorrect. This is optional transfer of the cache concepts, without reproducing the private table or supplied answers. Locality, remote storage, LRU, and clock remain necessary primary concepts even without a direct match in this exam sample.

## Key Takeaways

- Hierarchies trade speed, capacity, and cost; local versus remote speed is not absolute.
- Temporal locality concerns reuse; spatial locality concerns nearby addresses, for data and instructions.
- Placement chooses allowed locations; replacement chooses victims.
- Distinguish first accesses, working-set capacity, and placement conflicts.
- LRU uses past order, optimal replacement future knowledge, and clock reference bits.

## Recall and Practice

### Recall and explanation

#### Recall Q01 · Hierarchy and disaggregated storage

Explain capacity/cost/latency trends from registers through SRAM, DRAM, and local/remote storage, plus SSD/HDD differences. In disaggregation, what does the OS see, why centralize storage, and when can remote beat local?

<details><summary>Show solution</summary>

Upper levels are smaller/faster and costlier per byte. Lecture scales are cycles for registers/caches, tens of ns or roughly 100 cycles for DRAM, microseconds for SSDs, and milliseconds for HDDs with seek/rotation delays. All-fast capacity is costly. Disaggregation presents a disk-like OS service while I/O crosses a network, easing centralized replacement, maintenance, and scaling. A fast network/storage path can outperform a slow local disk. Uncertain per-minute bandwidth, remote-swap, and tape speech is not corrected into a hardware specification.

**Checking points:** Include all three tradeoffs, device delays, network I/O, management motivations, and uncertainty.

</details>

#### Recall Q02 · Data and instruction locality

Classify sum, a[i], loop instructions, and consecutive branch-free instructions in an array-sum loop. Why can a small cache work, and how does the relation extend beyond CPU caches?

<details><summary>Show solution</summary>

Repeated sum access is temporal; a[i] followed by a[i+1] is spatial. Repeated loop instructions are temporal and sequential instructions spatial. Access concentration in a hot subset lets a small fast store satisfy many requests. Level k caches part of k+1: registers hold lower-level values, main memory caches disk data, and local disks can cache remote files. These are tendencies, not guarantees for every program.

**Checking points:** Explain all four locality cases and the hot-subset mechanism.

</details>

#### Recall Q03 · Blocks, hits, and placement

Explain fixed/variable block tradeoffs and distinguish the 8-byte register, 64-byte line, and 4 KiB/2 MiB/1 GiB page examples. With 4, 9, 10, 3 in level k and 13 in k+1, classify requests for 10/13 and placement/replacement.

<details><summary>Show solution</summary>

Fixed sizes simplify management/indexing; variable sizes can fit objects such as web images but complicate management. Transfers amortize startup cost across bytes. The sizes describe distinct transfer units; 64 is not total cache capacity, and address width does not determine every block size. Request 10 hits in k; 13 misses there but hits in k+1. Placement chooses where fetched 13 may go; replacement chooses a victim if space is needed.

**Checking points:** Distinguish units from capacity, both requests, and both decisions.

</details>

#### Recall Q04 · Three miss causes

Distinguish cold, capacity, and conflict misses using a 1000-byte cache/1200-byte working array and the single-way `i mod4` sequence `0,8,0,8`. What if other slots are empty, or the set has two ways? What lookup cost does restricting placement reduce?

<details><summary>Show solution</summary>

Allowing a block anywhere requires finding and comparing tags across many positions; performing those comparisons in parallel needs more expensive, complex hardware. Deriving an index such as `i mod 4` narrows the positions and tags to inspect, simplifying lookup circuitry.

Cold means first reference before loading; capacity means the active working set cannot fit; conflict means placement restrictions. The 1000/1200 figures are bytes. Blocks 0/8 both map to slot 0: first references are cold; subsequent misses reflect mutual conflict eviction. Empty forbidden slots do not help. Two ways could retain both after loading, so the single-way trace is not a universal set-associative result.

**Checking points:** Explain first versus later causes, the two-way counterexample, and why a restricted index reduces comparison-hardware cost.

</details>

#### Recall Q05 · Optimal, LRU, and FIFO

Compare optimal and LRU information and LRU's assumption. With head=oldest in [A, B, C], trace a hit on A then insertion of D and compare FIFO.

<details><summary>Show solution</summary>

Optimal uses future next-use knowledge, evicting never-reused or farthest-next-use blocks. LRU uses oldest last use, which need not predict future reuse correctly. After the hit:[B, C, A]; inserting D evicts B, yielding [C, A, D]. FIFO does not refresh on hits, so it remains [A, B, C] and evicts A. The clear tail-refresh explanation is sufficient without recovering uncertain deque speech.

**Checking points:** Check information sources, hit refresh, and B-versus-A victims.

</details>

#### Recall Q06 · Mapping concepts before clock

Distinguish virtual/physical addresses, page, page table, PTE, and MMU, and identify the unit represented by a reference bit.

<details><summary>Show solution</summary>

A virtual address is used by a process; a physical address identifies memory location. A page is a fixed mapping unit; the page table is a main-memory VPN→PPN data structure; a PTE is one entry; the MMU is translation hardware. The reference bit records access to the corresponding page. The MMU is not the table, and a complete PTE bitfield is unnecessary for clock.

**Checking points:** Check all six concepts and hardware versus data structure.

</details>

#### Recall Q07 · Tracing second chance

Why can maintaining exact LRU on every memory access be costly? Trace scanning bits [1, 0, 1] from the first page and explain hardware/OS roles and the difference from exact LRU.

<details><summary>Show solution</summary>

Queue updates on tiny reads/writes can cost more than the access itself. Hardware sets the bit on access; the OS scan clears a one and grants a chance, or selects a zero. Clear the first bit, then choose the second page; the third remains unexamined at one. Later access can set a cleared bit again. Clock approximates recency without retaining a total LRU order.

**Checking points:** State first-bit clearing, second-page selection, unchanged third bit, and both actors.

</details>

#### Recall Q08 · Managers at each level

Who manages registers, CPU L1/L2/L3, and main-memory paging? Why can the OS consider more elaborate replacement, and what does a fixed lookup structure not imply about latency?

<details><summary>Show solution</summary>

Compiler register allocation, hardware cache management, and OS paging/replacement serve these roles. The compiler analyzes reuse; hardware uses defined placement for fast lookup. Avoiding expensive disk I/O can justify more elaborate OS LRU-like/second-chance bookkeeping. A defined lookup structure does not mean equal latency for every hit and miss.

**Checking points:** Connect all three managers to the relative cost of disk I/O.

</details>

### Apply and check

#### Practice P01 · Changing placement at fixed capacity

**Newly written synthetic practice.** Use Q4(e)'s fields [EX:sp_2025_1_midterm_q04 p.13] and Q4(f)'s valid/tag/offset reasoning [EX:sp_2025_1_midterm_q04 p.14]. Prerequisites are the chapter's block, placement, and lookup explanation; no VM configuration is imported.

Compare empty caches with 8-bit physical addresses, 4-byte lines, and four total lines: (A) direct-mapped, (B) 2-way. Access 0x04, 0x14, 0x05, 0x15 with no other accesses. Derive offset/index/tag widths and hits/misses. Block 0x04 contains hex bytes 31, 32, 33, 34; block 0x14 contains 41, 42, 43, 44. Which bytes do B's final two accesses return? If the 0x04 line's valid bit is then cleared without changing its tag, is 0x05 a hit?

<details><summary>Show solution</summary>

Offset width is log2(4)=2. A has four sets, index 2/tag 4; block numbers 1/5 both use set 1 and produce M, M, M, M. B has two sets, index 1/tag 5; the blocks share set 1 but have tags 0/2 and fit in separate ways, producing M, M, H, H. Offset 1 selects 0x32 and 0x42. After valid is cleared, a matching stale tag does not give a hit; 0x05 misses. Placement changed without increasing total capacity.

**Checking points:** Check 2/2/4 and 2/1/5, both traces, 0x32/0x42, and the valid requirement.

</details>

### Review plan

Mark locality in Q02's code, then trace Q04–Q05 by access. Explain Q06 before Q07–Q08's clock roles, and check P01 using separate field-calculation and hit-decision columns.

## Sources

[[courses/system_programming/lectures/en/2026-09-28-lecture-07|2026-09-28 · lecture note]]

[[courses/system_programming/transcripts/2026-09-28|2026-09-28 · corrected transcript]] — 10:25–19:55 (page/translation background), 19:55–25:38 (hierarchy and remote storage), 26:35–40:13 (locality, blocks, misses), 41:06–54:08 (replacement and managers)

[07.MM.Virtual.Memory.Recap.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/07.MM.Virtual.Memory.Recap.pptx) — slide 17; slide 18; slide 19; slide 20; slide 21; slide 23; slide 24; slide 25; slide 11

[07.MM.Virtual.Memory.Recap_2ffc3cf7.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/07.MM.Virtual.Memory.Recap_2ffc3cf7.pptx) — slide 17; slide 18; slide 19; slide 20; slide 21; slide 23; slide 24; slide 25; slide 11

Uncertain September 28 bandwidth units, remote-swap/tape phrases, queue replies, and redactions remain unresolved. The i mod 4 example is explicitly single-way; broad set-associative speech is not generalized. The worked examples use the stated block sizes, code, and mapping conditions; unclear graphical details do not supply additional assumptions. Timing figures are dated scale comparisons. Historical cache and VM subquestions use different address/block conditions, and supplied answers are not certified solutions.

Historical exam connections below use only the stated reasoning demands. Supplied answers are reference material, not independently certified solutions; current exam scope or frequency cannot be inferred.
