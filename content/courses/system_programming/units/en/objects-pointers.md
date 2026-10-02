---
title: "C Objects, Types, Addresses, and Pointers"
description: "Check types, pointer assignments, array conversions, and dynamic storage size and lifetime."
course: "system_programming"
unit_id: "objects-pointers"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["00.Introduction.pptx", "02.CPointers_24a7628c.pptx", "06.MM.Variable.and.Memory.Recap.pptx", "08.MM.Dynamic.Memory.Allocation.I.pptx", "09.MM.Dynamic.Memory.Allocation.II.pptx"]
private_source_assets: []
source_lectures: ["courses/system_programming/lectures/en/2026-09-02-lecture-01", "courses/system_programming/lectures/en/2026-09-07-lecture-02", "courses/system_programming/lectures/en/2026-09-09-lecture-03", "courses/system_programming/lectures/en/2026-09-23-lecture-06"]
---

Draw the pointer object separately from the object it designates. Establish type, bounds, and lifetime before calculating sizes or tracing assignments.

## Objects, types, and addresses answer different questions

Changing a value requires storage and a rule for interpreting that storage. An object holds a value; a variable supplies a name for it. A type determines interpretation and required size. Building on [program state in C](systems-c-build.md), distinguish what a value is, where it resides, and the type through which it is accessed.

Numerical examples here use the material's x86-64 Linux target: `char`, `short`, `int`, and `long` occupy 1, 2, 4, and 8 bytes; `float` and `double` occupy 4 and 8; an object pointer occupies 8. These are not fixed C requirements across ABIs. Floating-point uses a sign, exponent, and significand; a finite representation rounds many real numbers. An eight-byte `double` cannot represent every real value exactly, and sixteen bytes of `long double` storage do not mean 128 bits of effective precision. The [[courses/system_programming/lectures/en/2026-09-02-lecture-01|2026-09-02 types and arrays lecture]] and [[courses/system_programming/transcripts/2026-09-02|transcript]] at 01:15:55 introduce the distinction without establishing detailed IEEE 754 encoding work.

### A pointer's value versus its own address

Byte-addressed memory gives each byte an address; a multi-byte object's address identifies its first byte. These source numbers are an abstract address relationship, not a literal layout of eight-byte pointers at four-byte intervals.

| Object | Own address | Stored value | Type |
|---|---:|---:|---|
| `a` | 16 | 5 | `int` |
| `ap` | 28 | 16, namely `&a` | `int *` |
| `app` | 4 | 28, namely `&ap` | `int **` |

`*app` designates `ap`, whose value is 16; `**app` designates `a`, whose value is 5. In a declaration, `*` forms a pointer type. In an expression, `*` dereferences a pointer, while `&` takes an address. Assigning to `*app` can change pointer object `ap`; assigning `**app = 9` changes `a`.

The address-printing discussion in the [[courses/system_programming/transcripts/2026-09-07|2026-09-07 transcript]] at 54:41 can be applied to initialized objects as follows, with `<stdio.h>` available:

```c
int a = 5;
int *ap = &a;
printf("%p\n", (void *)ap);
printf("%p\n", (void *)&ap);
printf("%d\n", *ap);
```

The first two calls print the target address and the pointer object's own address; the third prints 5. Supplying `void *` to `%p` is a portability qualification. Neither the actual addresses nor their printed form is fixed. The suggestion at 55:31 to print an uninitialized pointer must not be adopted as safe inspection. Likewise, M004's diagram of value 102 at address 2 is distinct from uncertain spoken numbers.

`sizeof(ap)` is 8 and `sizeof(*ap)` is 4 on this target. A `void *k` also occupies eight bytes, but `void` is not a complete object type, so standard C does not obtain a target size with `sizeof(*k)`. A cast changes the type used for interpretation; it creates neither valid storage nor lifetime nor alignment.

## What arrays and strings actually contain

An array stores consecutive objects of one type. `T a[N]` occupies `N * sizeof(T)` bytes. Here, `char c[10]` occupies 10 bytes and `double pi[5][2]` occupies `5 * 2 * 8 = 80`. `int a[10]` is a 40-byte array object; `int *p = a` introduces a separate eight-byte pointer object.

In many expressions, `a` converts to a pointer to its first element. Then `a + i` corresponds to `&a[i]`, and `*(a + i)` designates `a[i]`. However, `sizeof(a)` measures the whole array, and `&a` points to the whole array. The array name cannot be assigned another address or incremented with `a++`; use a separate traversal pointer. Determine the operand's type before answering a `sizeof` question. That is also the demand of Q1(a), [EX:sp_2025_1_midterm_q01 p.2], available through the [[exam_questions/sp_2025_1_midterm_q01|existing question-only preview]]. For a non-VLA type, `sizeof(*p)` does not perform an ordinary read of the pointee. It therefore does not justify actually dereferencing an uninitialized `p`.

### NUL, length, and capacity

A C string is a character sequence terminated by a NUL byte. These declarations create different storage:

```c
char *p = "hello world\n";
char s[20] = "SNU CSE00800";
```

`p` stores the address of the first character in a literal; `s` is itself a twenty-byte array. `SNU` contributes three characters, the space one, `CSE` three, and `00800` five, giving length 12. The first NUL is `s[12]`; partial array initialization also makes every element through `s[19]` zero. String length excludes the terminator, but the storage must include it.

The writable array permits changing `s[0]`; modifying the literal through `p[0]` has undefined behavior. This does not make every pointer target read-only, nor does undefined behavior guarantee a particular crash. A `struct student { int id; char *name; };` groups heterogeneous members. Its `name` member stores an address, not an embedded copy of the characters, so the pointed-to string has its own lifetime.

### Function designators and structure pointers

For `void foo(void)`, the function designator `foo` converts to a function pointer in ordinary value contexts. Both `void (*fp)(void) = foo;` and `void (*fp)(void) = &foo;` identify that function. The function itself is not a pointer variable, and `sizeof(foo)` does not measure its machine-code length. Converting an arbitrary function pointer to `void *` for `%p` is not a portable rule for all C implementations.

The incomplete decay wording at 05:36–06:37 in the [[courses/system_programming/transcripts/2026-09-23|2026-09-23 transcript]] should be read alongside the declarations. The same material declares `shared` as `struct __shared *`. `sizeof(shared)` is eight, while `sizeof(*shared)` includes `sem_t m`, `int shared_int`, and padding. Without the size of `sem_t`, a numerical structure size cannot be invented. For a valid `shared`, `&shared->shared_int` addresses a member; `&shared` addresses the pointer object.

## Tracing address copies and value copies

With `p = &i` and `q = &j`, `q = p` redirects `q` to `i`. In contrast, `*q = *p` copies the value of `i` into the existing target `j`. This regularized example develops the distinction from the [[courses/system_programming/lectures/en/2026-09-07-lecture-02|2026-09-07 pointer lecture]].

```c
int i = 1, j = 7;
int *p = &i, *q = &j;
*q = *p;
q = p;
*p = 1;
*q = 2;
```

After the first assignment, `j = 1` and both targets are unchanged. After `q = p`, both pointers designate `i`. The final two assignments therefore update the same object, leaving `i = 2`, `j = 1`.

`scanf` with `%d` needs the address of a valid `int` destination. For this `i`, either `&i` or `p` supplies it. `&p` has type `int **` and does not satisfy that contract. Declaring `int a[10]` reserves element storage; declaring `int *a` reserves only pointer storage. An uninitialized-pointer dereference remains invalid even if execution happens not to crash.

### Which pointer does a pointer-to-pointer change?

The [[courses/system_programming/lectures/en/2026-09-09-lecture-03|2026-09-09 multiple-pointer lecture]] and M006 slides 31–35 extend the state trace:

```c
int i, j;
int *p = &i, *q = &j;
int **k = &p;
*p = 1;
*q = 2;
*k = q;
k = &q;
*k = &i;
*p = 3;
**k = 4;
```

`*k = q` writes the value of `q` into `p`, producing `p → j`. After `k = &q`, `*k = &i` produces `q → i`. Thus `*p = 3` changes `j`, while `**k = 4` changes `i`. The final relationships are `p → j`, `q → i`, `k → q`, with `i = 4`, `j = 3`. Counting stars is insufficient: update the designated object after each statement. Q1(b) at [EX:sp_2025_2_midterm_q01 p.3] demands the same separation between pointer movement and array-element updates. The transferable method is identifying the object on each assignment's left side, rather than memorizing a private exam output.

## Pointer arithmetic and lifetime

Typed pointer arithmetic moves in elements, not bytes. Within a permitted range, `p + k` has byte displacement `k * sizeof(*p)`. Scaling already occurs, so `p += sizeof(int)` for an `int *` skips four integers on this target rather than advancing to the next one.

| Independently initialized source example | Result |
|---|---|
| `p = &a[2]; q = p + 3; p += 6;` | `q = &a[5]`, `p = &a[8]` |
| `p = &a[8]; q = p - 3; p -= 6;` | `q = &a[5]`, `p = &a[2]` |
| `p = &a[5]; q = &a[1];` | `p-q = 4`, `q-p = -4`, `p<=q` is 0, `p>=q` is 1 |

These subtraction and ordering examples concern valid elements of the same array. Do not carry one row's final state into the next. A one-past pointer can represent a boundary but cannot be dereferenced as an extra element. Equality and relational ordering should not be reduced to one undifferentiated rule.

Lifetime also controls returned addresses. A `max(int *a, int *b)` returning `a` or `b` can identify a caller-owned object for as long as that object remains alive. A `max(int a, int b)` returning `&a` or `&b` instead exposes a parameter whose lifetime ends on return. Leftover bytes do not authorize access. A source `find_middle(a, n)` returning `&a[n/2]` needs `n > 0`, sufficient array bounds, and a still-live caller array.

### Array parameters are still passed by value

An `int a[]` parameter adjusts to `int *a`. Passing one address is different from scanning N elements. `find_largest` takes work proportional to N if it examines them all, but the call does not copy the array. In `find_largest(&b[5], 10)`, local `a[0]` designates `b[5]` and `a[9]` designates `b[14]`; all ten elements must exist. Initializing the maximum from the first element also requires `n > 0`.

C copies pointer parameter values. Writing `a[i]` can change a caller element, but assigning a new address to local parameter `a` does not change the caller's pointer variable. `const int a[]` prevents modification through this access path, not through every possible alias. Passing a whole structure containing an array by value is different: the structure value, including that member array, is copied.

## Reading size and access units from declarators

Start at the identifier and follow grouping parentheses, `[]`, function `()`, and `*`. Brackets and function parentheses bind more tightly than `*`.

| Declaration | Meaning |
|---|---|
| `int *p[10]` | Array of ten `int *` objects |
| `int (*p)[10]` | Pointer to `int[10]` |
| `int *(*p)[10]` | Pointer to `int *[10]` |
| `int (*pf)(void)` | Pointer to a no-argument function returning `int` |
| `int *pf(void)` | No-argument function returning `int *` |
| `int (*pf[10])(void)` | Array of ten such function pointers |
| `int pf[](void)` | Invalid array of functions themselves |

For `int (*p)[10]`, `p + 1` advances forty bytes on the target. For a pointer array converted to an element pointer, the element is one pointer, occupying eight bytes. Reading the type first also resolves M006 slides 38–39:

| Declaration | `sizeof(A)` | `sizeof(*A)` | `sizeof(**A)` |
|---|---:|---:|---:|
| `int A1[3]` | 12 | 4 | Invalid expression |
| `int *A2[3]` | 24 | 8 | 4 |
| `int (*A3)[3]` | 8 | 12 | 4 |

Here `A` stands for the identifier in each row. Slide 38's label `**A3: A3[0]` is inconsistent with the type: the explicit correction is `A3[0][0]`. In the source example with `A = {1,2,3}`, `B = {4,5,6}`, `A3 = &A`, and `B3 = &B`, `*A3 = *B3` is invalid array assignment. `**A3 = **B3` copies only the first integer, yielding `A = {4,2,3}`. `pA = *A3` stores the first element's address. Non-VLA `sizeof` reasoning is not permission for actual uninitialized-pointer access.

## Dynamic allocation size and lifetime

The [[courses/system_programming/lectures/en/2026-09-23-lecture-06|2026-09-23 dynamic-array explanation]] and [system_programming:M016 slide 17](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx) separate pointer `A` at `0xffffc1a4` from the allocated base address `0x56550004` stored in it. The figure's useful distinction is the pointer box versus the separate 1024-element region. With four-byte integers, the region occupies `4096 = 0x1000` bytes. Thus `A[1]` is at `0x56550008`, `A[2]` at `0x5655000c`, and `A[1023]` at `base + 4092 = 0x56551000`. This follows the slide, not a reconstruction of uncertain numbers at STT 24:43.

`char buf[512] = {'A','B','C'};` zero-initializes the remaining elements. Writing the first three bytes after `malloc` does not zero the rest. `calloc` supplies zero-initialization. Allocation failure checks, eventual `free`, and avoiding access after release are separate responsibilities. Uninitialized memory is not a reliable random-number source.

I/O lengths expose the same distinction. `sizeof(buf)` is 512 for that array but eight for a pointer to a heap buffer. Keep and pass the actual allocated length separately. Reading into one `char` requires its address, `&buf`, rather than its character value. OS resource reclamation at process exit does not justify accumulated leaks in a long-running program.

### Resizing and independent allocation lifetimes

RM002 slides 5–27 and RM003's error examples are optional materials-only review. They do not establish that the complete allocation decks were taught on September 28. `malloc`/`free` are libc requests; libc can interact with the OS through `brk`/`sbrk` or `mmap`. Not every allocation belongs to one contiguous `brk` heap. The material also introduces `alloca` and `sbrk(0)` as alternatives or observations, without making their implementation the task here.

For a positive-size `realloc` request, failure returns NULL and leaves the old allocation intact. The source's direct overwrite of the existing pointer can lose access to that allocation on failure. After success, use the returned pointer and do not reuse an old base or interior alias; an old allocation should not be presumed valid merely because the numerical address did not change. Contents fitting within the new size are preserved, while newly added bytes are not initialized automatically. Zero-size behavior is not adopted as a universal rule without standard and implementation conditions.

The source's growth from 256 integers to 512 means 1024 → 2048 bytes. After initially storing `0..255`, it initializes the additional elements `256..511` separately. This resizing example is distinct from the independent allocation sequence on RM002 slides 15–25. Assuming every request succeeds:

| Calls completed | Live allocations |
|---|---|
| `p1 = malloc(3); p2 = malloc(1); p3 = malloc(4);` | `p1`, `p2`, `p3` |
| `free(p2);` | `p1`, `p3` |
| `p4 = malloc(6);` | `p1`, `p3`, `p4` |
| `free(p3);` | `p1`, `p4` |
| `p5 = malloc(2);` | `p1`, `p4`, `p5` |
| `free(p1); free(p4); free(p5);` | None |

Allocation and release order need not match. Freed space may be reused, but the API does not promise that `p5` receives the former address of `p2`. This table follows the call sequence and does not assert uninspected graphical placement.

### Classifying memory errors by their causes

RM003 slides 33–45 connect pointers to diagnosis. Applying `+=` to uninitialized `y[i]` is not accumulation from zero. Allocating `N * sizeof(int)` for N pointer slots of an `int **p` is insufficient when pointers are larger than integers. Reading nine characters without a bound into `char s[8]` overflows, with the terminating NUL requiring further space. `*size--` groups as `*(size--)`, not `(*size)--`, so it moves the pointer instead of decrementing the pointed-to count.

Returning a local address, use-after-free, double free, and losing the last owning pointer are different lifetime errors. Freeing a linked structure's head does not automatically free separately allocated successors. Debuggers, `mtrace`/`muntrace`, and Valgrind are observation tools; naming them is not evidence of an executed check. Allocator lists, coalescing, and binning remain later material. Object size and lifetime now provide the foundation for [memory layout and calls](memory-layout.md).

## Key Takeaways

- `sizeof` concerns a type; a pointer does not remember the allocation's length.
- Separate address copying, copying a pointee value, and changing a pointer through a pointer-to-pointer.
- An array is an object that converts to its first-element address in many contexts.
- Valid address reasoning needs element scaling, array bounds, and a live object.
- Allocation, initialization, resizing, and release are separate responsibilities.

## Recall and Practice

### Recall and explanation

#### Recall Q01 · Size and precision

Give the chapter target's sizes for `char/short/int/long/float/double` and distinguish type, object, and variable. Do 8-byte `double` and 16-byte `long double` imply exact real values or 128-bit precision?

<details><summary>Show solution</summary>

The sizes are 1/2/4/8/4/8 bytes. An object provides storage, a variable names it, and a type governs interpretation and size. Floating-point uses sign, exponent, and significand; finite states require rounding. Storage size is not effective precision. These are the material's x86-64 Linux assumptions, not universal C sizes.

**Checking points:** Check all six sizes, storage versus precision, and the target qualification.

</details>

#### Recall Q02 · Pointer box and target

In the abstract diagram, `a=5` is at 16, `ap=&a` at 28, and `app=&ap` at 4. Explain `ap/&ap/*app/**app` and the targets of `*app=...` and `**app=9`. Give address/int print formats and interpret `sizeof(ap)`, `sizeof(*ap)`, and `sizeof(*k)` for `void *k`.

<details><summary>Show solution</summary>

The values are 16/28/16/5. Assigning through `*app` changes `ap`; through `**app` it changes the current integer target. Print `(void *)ap` or `(void *)&ap` with `%p`, and `*ap` with `%d`. The sizes are 8/4; standard C disallows `sizeof(*k)` because `void` is incomplete. Casting creates neither storage, alignment, nor lifetime. Printing an uninitialized pointer is not safe inspection, and the diagram's spacing is not physical pointer layout.

**Checking points:** Check all four values, both assignment targets, print argument types, and the void restriction.

</details>

#### Recall Q03 · Array size and conversion

For `int a[10]; int *p=a; double pi[5][2];`, compute the three object sizes and the displacement of `a+2`. Explain `a++`, `&a`, and `sizeof(a)` relative to ordinary array conversion.

<details><summary>Show solution</summary>

The sizes are 40/8/80 bytes; `a+2` is the third integer, eight bytes from the base. Typed arithmetic already scales. In many expressions `a` converts to the first-element pointer, but `sizeof(a)` measures the array and `&a` points to the whole array. `a++` is invalid; use a separate pointer. The pointer value does not also store the count ten.

**Checking points:** Check 40/8/80, the eight-byte displacement, and both conversion exceptions.

</details>

#### Recall Q04 · Function and structure pointers

For `void foo(void)`, compare initializing a function pointer with `foo` and `&foo`. Does `sizeof(foo)` measure code? For `struct __shared {sem_t m; int shared_int;} *shared;`, distinguish the two sizes and the addresses `&shared` and `&shared->shared_int`.

<details><summary>Show solution</summary>

Both initializations designate the same function; the function is not itself a pointer variable. Standard C rejects `sizeof(foo)` because a function type is not an object type; it does not measure code, and converting a function pointer to `void *` for `%p` is not a general portability rule. `sizeof(shared)=8`; `sizeof(*shared)` includes members and padding and cannot be numerically determined without `sem_t`. The two addresses designate the pointer object and, for a valid target, its integer member.

**Checking points:** Separate function conversion from structure size and do not invent an unknown size.

</details>

#### Recall Q05 · String length, storage, and lifetime

Compare storage for `char *p="abc"; char s[20]="SNU CSE00800";`. Give s's length, first NUL, capacity, and remaining initialization. Discuss modifying `p[0]`/`s[0]` and the lifetime of a `char *name` structure member.

<details><summary>Show solution</summary>

p stores only the address of separate literal storage. s is a writable twenty-byte array with 3+1+3+5=12 characters; index 12 is the first NUL and indices 12–19 are zero. The literal separately stores three characters plus NUL. Modifying s is allowed; modifying the literal through p is undefined behavior, without a guaranteed crash. `name` likewise stores an address rather than copied characters, so the string's lifetime must be managed separately.

**Checking points:** Check 12/12/20 and distinguish pointer, literal, and array storage.

</details>

#### Recall Q06 · Address assignment and value assignment

Trace `*q=*p; q=p; *p=1; *q=2;` starting with `i=1,j=7,p=&i,q=&j`. Which of `&i`, `p`, and `&p` satisfies scanf's `%d` destination, and does declaring `int *a` allocate integer storage?

<details><summary>Show solution</summary>

First j becomes 1; then q is redirected to i. The final writes set i to 1 then 2. Thus i=2, j=1, and both pointers target i. `&i` and p are valid `int *` destinations; `&p` is `int **` and mismatches. A pointer declaration allocates only the pointer object, not a valid integer destination.

**Checking points:** Check final values 2/1, aliasing, and scanf destination types.

</details>

#### Recall Q07 · Pointer arithmetic and returned lifetime

Starting independently within a sufficiently large array, trace (a) `p=&a[2];q=p+3;p+=6;`, (b) `p=&a[8];q=p-3;p-=6;`, and (c) `p=&a[5];q=&a[1];` followed by `p-q`, `q-p`, `p<=q`, and `p>=q`. Explain one-past access and compare returning a local parameter's address with `&a[n/2]`.

<details><summary>Show solution</summary>

(a) p→a[8], q→a[5]; (b) p→a[2], q→a[5]; (c) 4, -4, 0, 1. Differences count elements of the same array, and each case resets state. One-past may mark a boundary but is not dereferenceable. A value parameter's lifetime ends on return; a pointer to a caller-owned live object can remain usable. `&a[n/2]` requires n>0, adequate bounds, and a live caller array.

**Checking points:** Check independent initialization, all comparison results, and caller/local lifetime.

</details>

#### Recall Q08 · Array parameters and slices

Where do local `a[0]` and `a[9]` refer in `find_largest(&b[5],10)`? Compare argument-passing cost with search cost, element writes with reassigning a, `const int a[]`, and passing a structure containing an array by value.

<details><summary>Show solution</summary>

They designate b[5] and b[14]. The parameter adjusts to `int *`, so passing copies one address; scanning reads all ten elements. Initializing a maximum from the first element requires n>0 and valid slice bounds. Writing `a[i]` changes caller storage, but reassigning local a does not change the caller's pointer. const restricts this access path, not every alias. Passing an entire structure by value also copies its array member.

**Checking points:** Include the slice endpoint, value passing, const access path, and structure-copy distinction.

</details>

#### Recall Q09 · Complete double-pointer trace

Initially `p=&i,q=&j,k=&p`. Identify each assignment target and final relationships for `*p=1;*q=2;*k=q;k=&q;*k=&i;*p=3;**k=4;`.

<details><summary>Show solution</summary>

The targets are i, j, p, k, q, j, i. After initializing i=1, j=2, `*k=q` redirects p to j, `k=&q` redirects k to q, and `*k=&i` redirects q to i. Finally p→j, q→i, k→q, with i=4, j=3. The last write does not affect j because k no longer targets p.

**Checking points:** Show the three pointer-changing steps, not just final values.

</details>

#### Recall Q10 · Reading seven declarators

Interpret these independent declarations: `int *p[10]`, `int (*p)[10]`, `int *(*p)[10]`, `int (*pf)(void)`, `int *pf(void)`, `int (*pf[10])(void)`, `int pf[](void)`. What are the first two traversal strides?

<details><summary>Show solution</summary>

In order: array of ten int pointers; pointer to int[10]; pointer to an array of ten int pointers; pointer to a no-argument int-returning function; function returning int pointer; array of ten such function pointers; invalid array of functions. Read from the identifier, respecting grouping and the tighter binding of []/(). Traversal through the first array's element pointer strides eight bytes; the second p strides forty. The array name itself cannot be incremented.

**Checking points:** Check all seven interpretations and the 8/40-byte strides.

</details>

#### Recall Q11 · Type-based sizeof and array assignment

With int=4 and pointer=8, tabulate the types/sizes of `int A1[3]`, `int *A2[3]`, `int (*A3)[3]` and one/two dereferences. For `A={1,2,3}`, `B={4,5,6}`, `A3=&A`, `B3=&B`, interpret `*A3=*B3`, `**A3=**B3`, and `pA=*A3`.

<details><summary>Show solution</summary>

|Declaration|Object|One *|Two *|
|---|---|---|---|
|A1|int[3], 12|int, 4|Invalid|
|A2|int *[3], 24|int *, 8|int, 4|
|A3|int (*)[3], 8|int[3], 12|int, 4|

Non-VLA sizeof follows types and does not authorize reading an uninitialized pointer. The first assignment is invalid array assignment; the second changes only A[0], producing `{4,2,3}`; the third stores the first-element address in pA. `**A3` means `A3[0][0]`, correcting the source's inconsistent `A3[0]` label.

**Checking points:** Supply types as well as sizes and distinguish invalid assignment from the source's label error.

</details>

#### Recall Q12 · Heap addresses, initialization, and I/O length

A points to 1024 ints beginning at 0x56550004. Find the allocation size and addresses of A[1], A[2], A[1023]. Compare partial array initialization with writing three malloc bytes, for allocated `char *p`, interpret `read(fd,p,sizeof(p))`, and explain a one-char destination and failure/free duties.

<details><summary>Show solution</summary>

The allocation is 4096=0x1000 bytes; the addresses are 0x56550008/0x5655000c/0x56551000. A's own object address is separate. Partial initialization of `char buf[512]={'A','B','C'}` zeros the remainder; malloc does not, while calloc zero-initializes. `sizeof(p)=8`, so that read requests eight bytes; retain the allocated length separately. For a separate `char c`, `read(fd,&c,1)` supplies its address and requests one byte. Check allocation failure, free when finished, and avoid use after release. Exit-time reclamation does not fix long-running leaks.

**Checking points:** Verify all three addresses, 4096 bytes, initialization differences, and the eight-byte request.

</details>

#### Recall Q13 · Reallocation success and failure

For resizing 256 ints to 512, give byte sizes and preserved/new ranges. Explain directly overwriting the old pointer on positive-size realloc failure, aliases after success, and libc versus OS roles.

<details><summary>Show solution</summary>

The sizes are 1024→2048 bytes. Existing values 0..255 are preserved within the new range; new elements 256..511 require initialization. Failure returns NULL while the old block survives, so overwriting the sole pointer can lose access. After success use the returned pointer and do not reuse old base/interior aliases. malloc/free are libc operations; libc may interact with the OS through brk/sbrk or mmap. Not all allocations lie in one contiguous heap. No universal zero-size rule or allocator implementation is inferred.

**Checking points:** Separate failure preservation, successful pointer replacement, and initialization of growth.

</details>

#### Recall Q14 · Independent allocation lifetimes

Assume success for `p1=malloc(3);p2=malloc(1);p3=malloc(4);free(p2);p4=malloc(6);free(p3);p5=malloc(2);`. List live allocations after each free and after p5. Is p5's address or the final release order prescribed?

<details><summary>Show solution</summary>

After free(p2): p1, p3; after free(p3): p1, p4; after p5: p1, p4, p5. Releasing those three separately finishes the sequence; release order need not match request order. Freed space may be reused, but p5 need not receive p2's former address. Old p2/p3 accesses remain invalid. These independent allocations are distinct from resizing one allocation.

**Checking points:** Check all three live sets and the absence of an address-reuse guarantee.

</details>

#### Recall Q15 · Classifying memory errors

Diagnose each: `+=` on uninitialized y[i], `N*sizeof(int)` for N int-pointer slots, nine characters plus NUL into `char s[8]`, `p+=sizeof(int)`, `*size--`, a returned local address, use-after-free, double free, and freeing only a head. Which diagnostic tools can help, and does an observed crash define C validity?

<details><summary>Show solution</summary>

Respectively: accumulation does not start from zero; four-byte int sizing is insufficient for eight-byte pointer slots; ten bytes are needed including NUL; pointer scaling advances four ints; `*size--` groups as `*(size--)`, moving the pointer rather than decrementing the count. Local lifetime ends on return; accessing freed storage and freeing twice are invalid. Separately allocated successors survive freeing the head and may become leaked. Debuggers can inspect state; mtrace/muntrace and Valgrind can help investigate allocation or access errors. Diagnostic observations help locate a defect, but absence of a crash does not make undefined behavior valid.

**Checking points:** Identify all nine causes and do not equate C validity with whether a crash occurs.

</details>

### Apply and check

#### Practice P01 · What is measured after an alias change?

**Newly written synthetic practice.** Combine Q1(a)'s operand-type reasoning [EX:sp_2025_1_midterm_q01 p.2] with Q1(b)'s pointer/element trace [EX:sp_2025_2_midterm_q01 p.3]. Prerequisites are array conversion, aliases, and non-VLA sizeof; this is not an original exam question. Use int=4, pointer=8.

```c
int a[3]={2,4,6};
int *p=a, *q=&a[2];
int **r=&p;
*r=q;
**r=a[0]+1;
q=a;
*q=9;
```
Find a, the pointer relationships, and `sizeof(a)`, `sizeof(*r)`, `sizeof(**r)`. In an independent run replacing `*r=q` with `*p=*q`, what changes?

<details><summary>Show solution</summary>

Originally p is redirected to a[2], which receives 3; q later targets a[0], which receives 9. Final a is `{9,4,3}`, p→a[2], q→a[0], r→p; sizes are 12/8/4. In the modified run the first assignment sets a[0]=6 without moving p. The next sets a[0]=7, and the final write sets it to 9, yielding `{9,4,6}`. Types are unchanged, so all three sizes remain the same.

**Checking points:** Track each left-hand object and verify both final arrays and unchanged sizeof results.

</details>

### Review plan

Redraw object boxes for Q02, Q06, and Q09, then compare P01's two runs. Write types before sizes in Q10–Q11, and track size, initialization, and live allocations in separate columns for Q12–Q15.

## Sources

[[courses/system_programming/lectures/en/2026-09-02-lecture-01|2026-09-02 · lecture note]]

[[courses/system_programming/lectures/en/2026-09-07-lecture-02|2026-09-07 · lecture note]]

[[courses/system_programming/lectures/en/2026-09-09-lecture-03|2026-09-09 · lecture note]]

[[courses/system_programming/lectures/en/2026-09-23-lecture-06|2026-09-23 · lecture note]]

[00.Introduction.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx) — slide 51; slide 54

[02.CPointers_24a7628c.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx) — slides 3, 9, 15, 17, 23–25, 28–29, 31–36, 38–39

[06.MM.Variable.and.Memory.Recap.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx) — slide 15; slide 34; slide 4; slide 17; slide 20

[[courses/system_programming/transcripts/2026-09-02|2026-09-02 · corrected transcript]] — 01:15:55, 01:21:23, 01:34:38, 01:29:10

[[courses/system_programming/transcripts/2026-09-07|2026-09-07 · corrected transcript]] — 54:41

[[courses/system_programming/transcripts/2026-09-09|2026-09-09 · corrected transcript]] — 01:22–20:26, 21:19

[[courses/system_programming/transcripts/2026-09-23|2026-09-23 · corrected transcript]] — 05:36, 06:37

[08.MM.Dynamic.Memory.Allocation.I.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/08.MM.Dynamic.Memory.Allocation.I.pptx) — slides 5, 7–9, 15–25, 27

[09.MM.Dynamic.Memory.Allocation.II.pptx](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/09.MM.Dynamic.Memory.Allocation.II.pptx) — slide 35; slide 38; slide 40; slide 44

Numerical work uses the stated x86-64 Linux model. The A3 label/array-assignment errors and incomplete function-decay speech remain distinguished; non-VLA sizeof does not authorize uninitialized-pointer access. The allocation decks are optional materials-based review; allocator lists, coalescing, and binning are outside scope. Whole-slide layout has not been verified for the newer decks, so use the call sequence and stated types/sizes. Uncertain September 23 allocation numbers and initialization speech are not recovered. Historical supplied crash lists do not define all undefined behavior.

Historical exam connections below use only the stated reasoning demands. Supplied answers are reference material, not independently certified solutions; current exam scope or frequency cannot be inferred.

[[exam_questions/sp_2025_1_midterm_q01|2025-1 Midterm Q1 · C pointers (existing preview)]]

[[exam_questions/sp_2025_2_midterm_q01|2025-2 Midterm Q1 · C programming (existing preview)]]
