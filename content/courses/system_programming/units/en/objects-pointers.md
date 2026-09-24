---
title: "C Objects, Types, Addresses, and Pointers"
description: "Check pointer code and memory sizes through types, addresses and lifetimes."
course: "system_programming"
unit_id: "objects-pointers"
lang: "en"
note_layout: "textbook_unit_v1"
source_kind: "unit_chapter"
review_status: "approved"
draft: false
cssclasses: ["unit-textbook"]
source_assets: ["00.Introduction.pptx", "02.CPointers_24a7628c.pptx", "06.MM.Variable.and.Memory.Recap.pptx"]
private_source_assets: []
source_lectures: ["courses/system_programming/lectures/en/2026-09-02-lecture-01", "courses/system_programming/lectures/en/2026-09-07-lecture-02", "courses/system_programming/lectures/en/2026-09-09-lecture-03", "courses/system_programming/lectures/en/2026-09-23-lecture-06"]
---

Separate an object holding a value from a pointer holding its address. Write down types and lifetimes before tracing declarations, indirect stores and sizes.

## C objects and types: interpreting stored bytes

To understand `int n = 5;`, distinguish the name `n`, the value 5, and the object holding that value. A C object is storage for a value; a variable name provides a way to refer to it. A type determines the required size and interpretation. Assignment, introduced in [[courses/system_programming/units/en/systems-c-build|C state changes and building programs]], changes an object's stored value.

Numerical sizes in this unit use the course's x86-64 Linux target.

| Type | Size in bytes |
|---|---:|
| `char` | 1 |
| `short` | 2 |
| `int` | 4 |
| `long` | 8 |
| `float` | 4 |
| `double` | 8 |
| Object pointer | 8 |

Another ABI, or Application Binary Interface, can specify different sizes. In particular, a 64-bit OS does not universally imply an eight-byte `long`. [Introduction slides 51–54](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx)

Floating-point representations use a sign, exponent, and significand, also called a mantissa. A finite number of bit patterns cannot represent every real number exactly, so rounding is unavoidable. The [[courses/system_programming/transcripts/2026-09-02|September 2 lecture, 01:15:55]] introduces IEEE 754 without establishing detailed encoding calculations as covered material. Likewise, sixteen bytes of `long double` storage do not imply 128 bits of numerical precision.

## Addresses, pointers, and pointed-to objects

In byte-addressed memory, each byte has an address. A multibyte object's address is the address of its first byte. A pointer is a separate object whose value is an address. The `*` in `int *ap` constructs a pointer declaration; in the expression `*ap` it performs indirection, or dereferencing. `&a` obtains the address of `a`.

Memory recap slide 15 illustrates these relationships. Its small address numbers are schematic, not a literal layout satisfying the full size of every eight-byte pointer.

| Object | Schematic address of the object | Stored value |
|---|---:|---:|
| `a` | 16 | 5 |
| `ap` | 28 | 16 |
| `app` | 4 | 28 |

```c
int a = 5;
int *ap = &a;
int **app = &ap;
```

Both `ap` and `&a` have address value 16, while `&ap` is 28. Following `app` once reaches the pointer object `ap`, whose value is 16. Following it twice reaches `a`, whose value is 5. Assigning through `*app` changes the pointer `ap`; assigning through `**app` changes the `int` currently reached along that path. [Memory recap slide 15](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)

The [[courses/system_programming/transcripts/2026-09-07|September 7 lecture, 54:41]] distinguishes `%p` for an address from `%d` for an integer value. With the valid initialization above:

```c
printf("%p\n", (void *)ap);
printf("%p\n", (void *)&ap);
printf("%d\n", *ap);
```

These print the pointed-to object's address, the pointer object's own address, and 5. Converting an object pointer to the `void *` argument required by `%p` is a portability qualification. Actual address numbers can vary between executions.

`sizeof(ap)` is eight; `sizeof(*ap)` is four, the size of `int`. A `void *k` also occupies eight bytes, but `void` is not a complete object type, so standard C does not provide a pointed-to size through `sizeof(*k)`. A cast changes a type interpretation; it does not create valid storage, lifetime, or alignment. Printing or dereferencing an uninitialized pointer is not made safe by its declaration. An accidental absence of a crash does not establish valid access.

## Assigning a pointer versus assigning a pointed-to value

Identify the object on the left of an assignment before tracing its effect.

```c
int i = 1, j = 2;
int *p = &i, *q = &j;
*q = *p;
q = p;
```

`*q = *p` copies the value 1 from `i` into `j`, leaving `p→i` and `q→j` unchanged. The subsequent `q = p` copies an address, making both pointers refer to `i`. Now `*p=1; *q=2;` changes the same object twice, leaving `i` equal to 2. [Pointers slides 13–15](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx)

The `%d` conversion in `scanf` similarly needs the address of an `int` into which it can store a result. For `int i`, supply `&i`; for `int *p=&i`, supply `p`. `&p` has type `int **` and does not meet the same contract. The rule is “supply the address of the required destination object,” not “always add `&`.”

`int a[10]` allocates storage for ten elements. `int *a` allocates only a pointer object. Immediately writing `*a=0` after the second declaration does not magically create a valid element.

## Arrays and strings have their own storage

An array contains consecutive objects of one type. Its total size is `N * sizeof(T)`: `char c[10]` occupies ten bytes, and `double pi[5][2]` occupies `5*2*8=80` bytes on this target. `int a[10]` is a forty-byte array, not an eight-byte pointer object.

In many expressions an array converts to a pointer to its first element. Thus `a+i` corresponds to `&a[i]`, and `*(a+i)` to `a[i]`. A byte-address calculation uses `base + i*sizeof(T)`, but typed pointer addition `a+i` already scales by element size. Multiplying again would apply the scale twice. Contexts such as `sizeof(a)` and `&a` must be distinguished from this conversion. An array cannot be advanced with `a++`; use a separate traversal pointer. Traversal until NUL is valid only when the terminator occurs within the array's bounds. [Pointers slides 18–25](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx)

### A literal's address and a writable character array

A C string is a character sequence terminated by the NUL byte, `'\0'`. These declarations establish different storage relationships.

```c
char *s = "hello world\n";
char text[20] = "SNU CSE00800";
```

`s` holds the address of a literal's first character. `text` stores characters in a separate twenty-byte array. The length of `SNU CSE00800` is `3+1+3+5=12`; its first NUL is `text[12]`, and the remaining array elements are also initialized to zero. Capacity twenty, string length twelve, and one terminator byte measure different things.

The elements of `text` may be changed. Modifying a string literal is undefined behavior, which does not promise any particular crash. Conversely, being reached through a pointer does not make every object read-only. In `struct student { int id; char *name; };`, `name` stores an address, not an embedded copy of all the characters. Copying the structure does not independently copy the string or extend its lifetime. [[courses/system_programming/transcripts/2026-09-02|September 2 lecture, 01:29:10–01:34:38]], [Introduction slide 54](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx)

### Function designators and structure pointers

Given `void foo(void)`, both `void (*fp)(void)=foo` and `void (*fp)(void)=&foo` designate the same function. In the first case, the function designator converts to a function pointer. The function itself is not a pointer variable, and `sizeof(foo)` does not measure its machine code. Function pointers and object pointers are distinct categories; converting arbitrary function pointers to `void *` for `%p` is not a portable general rule.

In the memory recap example, `shared` points to `struct __shared`. `sizeof(shared)` is eight, whereas `sizeof(*shared)` includes `sem_t m`, `int shared_int`, and padding. Without a concrete `sem_t` size, the complete structure size cannot be invented. With a valid pointed-to structure, `&shared->shared_int` is a member address; `&shared` is the address of the pointer object. [[courses/system_programming/transcripts/2026-09-23|September 23 lecture, 05:36–06:37]], [Memory recap slide 4](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)

## Pointer arithmetic and object lifetime

Read pointer movement in elements, not raw bytes. The examples on slides 21–24 **reset their starting state independently**.

| Initialization | Operations | Result |
|---|---|---|
| `p=&a[2]` | `q=p+3; p+=6;` | `q=&a[5]`, `p=&a[8]` |
| `p=&a[8]` | `q=p-3; p-=6;` | `q=&a[5]`, `p=&a[2]` |
| `p=&a[5]; q=&a[1];` | `p-q`, `q-p` | 4, -4 |
| Same third initialization | `p<=q`, `p>=q` | 0, 1 |

Carrying `p=&a[2]` from the second example into the third changes the answer. Differences within one array are measured in elements. A pointer one position past the last element may be formed but cannot be dereferenced as an element. Do not extend these array-order comparisons to arbitrary addresses of unrelated objects. [Pointers slides 21–24](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx)

When returning a pointer, the target's lifetime matters more than the surviving address number. The source's `max(int *a,int *b)` can return the address of a caller object containing the larger value, usable while that object lives. In contrast, returning `&a` or `&b` from `max(int a,int b)` returns an address of an automatic parameter whose lifetime ends on return. Keeping its address does not keep the object alive.

Similarly, `find_middle(a,n)` returning `&a[n/2]` requires `n>0`, an existing element, and a still-live caller array. [Pointers slides 16–18](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx)

## Array parameters and double pointers

A function parameter declared `int a[]` is adjusted to `int *a`. Passing it copies an address rather than all `N` elements, so the act of passing it does not take time proportional to `N`. A `find_largest` scan still examines the elements and takes time proportional to `N`.

For `find_largest(&b[5],10)`, the callee's `a[0]` is the caller's `b[5]`, and `a[9]` is `b[14]`. Those ten elements must exist. An implementation initialized from `a[0]` requires nonempty input. `const int a[]` prevents element changes through that access path. Changing `a[i]` affects caller storage, but assigning a different address to the local pointer `a` does not change the caller's pointer variable. Passing an entire structure containing an array by value is different: the structure value, including its array member, is copied. [[courses/system_programming/transcripts/2026-09-09|September 9 lecture, 03:08–10:32]], [Pointers slides 26–30](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx)

### Which object does a double pointer change?

An `int **k` holds the address of an `int *` object. The source trace changes `k`'s target along the way.

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

The first two stores give `i=1,j=2`. `*k=q` writes into `p`, making `p→j`. `k=&q` then makes `k` refer to `q`; `*k=&i` therefore establishes `q→i`. Finally `*p=3` changes `j`, while `**k=4` follows `k→q→i` and changes `i`. The result is `i=4,j=3`. Update the relationships after every assignment rather than merely counting asterisks. [Pointers slides 31–35](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx), [[courses/system_programming/transcripts/2026-09-09|September 9 lecture, 15:26–19:25]]

## Deriving types from complex declarations

Start at the identifier and work outward. Postfix `[]` and function `()` bind before `*`, unless grouping parentheses change the order.

| Independent declaration | Meaning |
|---|---|
| `int *p[10];` | Array of ten `int *` objects |
| `int (*p)[10];` | Pointer to an `int[10]` array |
| `int *(*p)[10];` | Pointer to an array of ten `int *` objects |
| `int (*pf)(void);` | Pointer to a no-argument function returning `int` |
| `int *pf(void);` | No-argument function returning `int *` |
| `int (*pf[10])(void);` | Array of ten pointers to no-argument, `int`-returning functions |
| `int pf[](void);` | Invalid: requests an array of functions themselves |

After conversion, `p+1` for the first declaration advances one pointer element, eight bytes on the target. The second advances one complete `int[10]`, forty bytes. [Pointers slide 36](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx)

The following table uses non-VLA types on the same target.

| Declaration | `sizeof(A)` | `sizeof(*A)` | `sizeof(**A)` |
|---|---:|---:|---:|
| `int A1[3]` | 12 | 4 | Type error |
| `int *A2[3]` | 24 | 8 | 4 |
| `int (*A3)[3]` | 8 | 12 | 4 |

`*A3` has type `int[3]`. After that array converts to an element pointer, another dereference reaches its first `int`. Slide 38's label `**A3: A3[0]` is inconsistent with these types; `A3[0][0]` is the correct correspondence. Also, non-VLA `sizeof(*A3)` does not evaluate its operand. Its validity does not make an evaluated access through an uninitialized pointer safe.

With `A={1,2,3}, B={4,5,6}` and `A3=&A, B3=&B`, `*A3=*B3` attempts forbidden whole-array assignment. `**A3=**B3` copies just the first element, yielding `A={4,2,3}`. `pA=*A3` stores the address of the first element. [Pointers slides 38–39](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx)

The indexed `sizeof` question demands the same first step: decide whether the expression denotes a pointer object, a pointed-to object, or an entire array. A string literal's stored size includes its NUL terminator and differs from its string length. This type reasoning transfers; a report that some code did not crash is not a C validity rule. [EX:sp_2025_1_midterm_q01 p.2]

## Dynamic allocation: capacity, initialization, and lifetime

`malloc` returns the start address of requested storage. The pointer variable's address differs from the allocated region's address. On memory recap slide 17, `A` itself is schematically at `0xffffc1a4` and holds heap address `0x56550004`. The allocation is `1024 * sizeof(int)=4096=0x1000` bytes.

| Element | Starting address |
|---|---|
| `A[0]` | `0x56550004` |
| `A[1]` | `0x56550008` |
| `A[2]` | `0x5655000c` |
| `A[1023]` | `0x56550004 + 1023*4 = 0x56551000` |

The one-past address is `0x56551004`. The [[courses/system_programming/transcripts/2026-09-23|September 23 transcript, 24:43]] contains confused size and address wording; these values follow the slide's expression and diagram. [Memory recap slides 16–20](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)

`char buf[512]={'A','B','C'}` initializes all remaining elements to zero. Allocating with `malloc(512)` and assigning only the first three bytes does not zero the rest. `calloc` zero-initializes allocated bytes. The unclear discussion at 26:45–28:44 does not establish zeroed `malloc` storage or a trustworthy source of random values.

Check allocation failure, use storage only during its lifetime, and call `free` when it is no longer needed. OS reclamation when the process exits does not justify accumulating leaks in a long-running program.

Finally, `sizeof` does not consult an allocation record. For an actual `char buf[512]` array, `sizeof(buf)` is 512. For `char *buf` pointing to 512 allocated bytes, it is eight. Thus `read(fd,buf,sizeof(buf))` requests only eight bytes in the pointer case. Keep the real capacity separately, for example in `BUFSIZE`. To read one `char` object, supply `&buf` rather than its value. These distinctions underpin [[courses/system_programming/units/en/io-streams|requested and returned I/O lengths]].

## Key Takeaways

- Pointer value, pointer-object address and pointee value are distinct.
- Pointer sizeof does not encode array capacity or string length.
- Mark each store’s target and preserve example resets.
- Continue to [[courses/system_programming/units/en/memory-layout|alignment and memory layout]].

## Recall and Practice

### Recall and reasoning

#### Recall Q01 · Size and precision

Give the target sizes of char, short, int, long, float, double and pointers. What do eight-byte double and sixteen-byte long double not establish?

<details><summary>Show solution</summary>

Sizes are 1, 2, 4, 8, 4, 8 and 8 bytes on this target, not every ABI. Sign, exponent and significand encode finitely many values, so rounding is unavoidable. Sixteen storage bytes do not establish 128-bit precision.

**Check:** Separate size, ABI and numerical precision.

</details>

#### Recall Q02 · An object storing an address

Let `a=5`, `ap=&a`, `app=&ap` with schematic object addresses 16, 28 and 4. Explain pointer expressions, indirect assignments and printf formats.

<details><summary>Show solution</summary>

`ap` is 16, `&ap` is 28 and `*ap` is 5. `*app` designates ap and has value 16; `**app` reaches a’s 5. `*app=&b` redirects ap, after which `**app=9` changes b; app itself stays unchanged. Use `%p` with `(void *)ap`/`(void *)&ap` and `%d` with `*ap`. Pointer size is 8, int size 4; `void *` is 8 but standard C has no `sizeof(void)`. Casts do not create valid lifetime/alignment/storage; non-crashing uninitialized pointers are not safe. Small addresses are schematic, not a packed eight-byte layout.

**Check:** Distinguish address, pointer object, value and each assignment target.

</details>

#### Recall Q03 · Array, function and struct pointers

Calculate sizes and a+2 for `int a[10]; int *p=a;`, plus `char[10]`/`double[5][2]`. Compare foo/&foo and struct-pointer/object sizes.

<details><summary>Show solution</summary>

`sizeof(a)=40`, `sizeof(p)=8`, and `a+2` addresses the third int, eight bytes ahead. The char and double arrays occupy 10 and 80 bytes. Arrays usually convert to element pointers, with exceptions including sizeof/address-of; `a++` is invalid. Typed addition already scales. For `void foo(void)`, foo and &foo can initialize `void (*fp)(void)`; function sizeof and portable object-pointer-style printing are not established. `sizeof(shared)=8`, but `sizeof(*shared)` includes members and padding and cannot be guessed without `sem_t` size. A member address also differs from the pointer variable’s address.

**Check:** Check 40/8/eight-byte movement, 10/80, function pointers and unknown struct size.

</details>

#### Recall Q04 · Three string-related sizes

Find length, NUL index and capacity of `char s[20]="SNU CSE00800"`. Compare `char *p="abc"`, a writable `char a[4]="abc"` array and copying a struct’s name pointer.

<details><summary>Show solution</summary>

Length is 12, first NUL index 12, capacity 20, with s[12]..s[19] zeroed. `p` stores an address; its literal occupies four bytes including NUL. `char a[4]="abc"` is writable; changing the literal through p is undefined behavior, not a guaranteed crash. Copying a struct’s `char *name` copies the address, sharing character storage without a deep copy or extended lifetime.

**Check:** Check 12/12/20 and distinguish pointer storage, character storage and lifetime.

</details>

#### Recall Q05 · Copying values and addresses

Trace `*q=*p; q=p; *p=1; *q=2;` with i=1, p=&i, q=&j. Which of &i, p and &p suits scanf’s `%d`?

<details><summary>Show solution</summary>

The first assignment makes j=1 without redirecting pointers. After q=p both reach i, so the last stores set i to 1 then 2. Final i=2, j=1. `scanf` `%d` needs `int *`: &i and p fit, &p is `int **`. Declaring a pointer does not allocate its target int.

**Check:** Check retained j, redirected q and scanf argument types.

</details>

#### Recall Q06 · Lifetime and pointer arithmetic

Compare returning a local int address and a caller-owned array element. Trace the three separately reset pointer examples over one sufficiently large array.

<details><summary>Show solution</summary>

A local object’s lifetime ends on return; its remaining address bits do not keep it alive. A caller-owned element can remain valid with a live array, n>0 and valid bounds. The first example ends q=a+5, p=a+8; the reset example ends q=a+5, p=a+2. After the final reset, p−q=4, q−p=−4, p<=q=0, p>=q=1. Differences count elements, not bytes. These require the same valid array; one-past may be formed but not dereferenced.

**Check:** Keep all resets separate and justify lifetime and element units.

</details>

#### Recall Q07 · Actual array-parameter passing

For `find_largest(&b[5],10)`, identify a[0]/a[9], passing/search cost, const restrictions, rebinding and a struct containing an array.

<details><summary>Show solution</summary>

a[0] is b[5] and a[9] is b[14], requiring ten valid elements and n>0. An array parameter adjusts to a pointer whose value is copied: passing is O(1), scanning for a maximum O(N). Const restricts writes through that access path. Rebinding local a does not rebind the caller’s pointer, though element writes reach original storage. Passing a struct by value copies its array member too.

**Check:** Check slice bounds, both costs, and pointer versus object copying.

</details>

#### Recall Q08 · Two-level indirection

Trace all seven statements from p=&i, q=&j, k=&p: `*p=1; *q=2; *k=q; k=&q; *k=&i; *p=3; **k=4;`.

<details><summary>Show solution</summary>

1 sets i=1; 2 sets j=2; 3 changes p to q’s value &j because k reaches p; 4 redirects k to q; 5 sets q=&i; 6 sets j=3 through unchanged p; 7 sets i=4 through k→q→i. Final p→j, q→i, k→q, i=4, j=3. Re-evaluate which pointer object `*k` designates at each step.

**Check:** Identify the changed target at every step, not just final values.

</details>

#### Recall Q09 · Reading compound declarations

Classify the seven independent declarations listed and compare p+1 for the first two: `int *p[10]`; `int (*p)[10]`; `int *(*p)[10]`; `int (*pf)(void)`; `int *pf(void)`; `int (*pf[10])(void)`; `int pf[](void)`.

<details><summary>Show solution</summary>

In order: array of ten int pointers; pointer to an array of ten ints; pointer to an array of ten int pointers; pointer to a no-argument int-returning function; function returning int pointer; array of ten such function pointers; invalid array of functions. After conversion, the first p+1 advances one pointer (8 bytes); the second advances int[10] (40 bytes). Function pointers are objects; functions themselves cannot be array elements.

**Check:** Check every declaration and both 8/40 strides.

</details>

#### Recall Q10 · sizeof and valid assignment

Tabulate each variable and one/two dereferences for `int A1[3], *A2[3], (*A3)[3]`. Compare sizeof to reading uninitialized A3 and whole-array versus first-element assignments.

<details><summary>Show solution</summary>

|Expressions|Types and bytes|
|---|---|
|A1, *A1, **A1|int[3]:12; int:4; invalid|
|A2, *A2, **A2|int *[3]:24; int *:8; int:4|
|A3, *A3, **A3|int (*)[3]:8; int[3]:12; int:4|

Non-VLA `sizeof(*A3)` does not evaluate its operand and yields 12 without making runtime use of an uninitialized pointer safe. With A={1, 2, 3}, B={4, 5, 6}, `*A3=*B3` is invalid array assignment; `**A3=**B3` copies only the first int, yielding A={4, 2, 3}. `*A3` can convert to an element pointer where appropriate. The source’s **A3 equivalence must read `A3[0][0]`.

**Check:** Check all types/sizes, evaluation rules and the array-assignment prohibition.

</details>

#### Recall Q11 · Allocation and capacity

For 1024 four-byte ints starting at 0x56550004, find A[1], A[2], A[1023] and one-past. Compare a 512-byte array and malloc pointer in size, initialization, read length and lifetime.

<details><summary>Show solution</summary>

The allocation is 4096=0x1000 bytes. Addresses are 0x56550008, 0x5655000c, 0x56551000 and 0x56551004. `&A` is separate pointer storage (schematically 0xffffc1a4). `char a[512]="ABC"` zeroes the remainder; malloc does not initialize, whereas calloc zeroes. Pointer sizeof is 8 versus array 512, so `read(fd,p,sizeof(p))` requests 8. Keep/pass capacity separately; a single char needs `&buf`. Check allocation, free after final use and avoid dangling access. Process-exit cleanup does not excuse runtime leaks.

**Check:** Check all four addresses, pointer storage, 8/512, initialization and lifetime.

</details>

### Practice

#### Practice P01 · Size lost at an API boundary

**Newly written synthetic practice.** On the target, consider `char text[7]="cat"; char *p=text; int a[3]={1,2,3}; int (*whole)[3]=&a;`. Find `sizeof(text)`, `sizeof(p)`, `sizeof(*whole)`, `sizeof(**whole)` and the string length of text; can a char-pointer parameter recover capacity 7 using sizeof?

[EX:sp_2025_1_midterm_q01 p.2] Q1(a) contributes type/sizeof/NUL reasoning, extended to diagnosing information lost at a parameter boundary. Prerequisites: Q03/Q04/Q10/Q11; crash prediction is excluded. [[exam_questions/sp_2025_1_midterm_q01|Authorized related question preview]]

<details><summary>Show solution</summary>

Values are 7, 8, 12, 4; string length is 3. NUL and remaining zero bytes belong to the capacity. A pointer parameter carries an address, so sizeof gives 8, not capacity 7 or length 3. Pass capacity separately: this combines type-based calculation with an API-design decision.

**Check:** Check 7/8/12/4/3 and justify explicit capacity.

</details>

### Review plan

Draw arrows for Q02/Q05/Q08 and separate reset diagrams for Q06. Rebuild the Q09/Q10 type tables from memory, then use Q11/P01 to distinguish sizeof from capacity.

## Sources

### Dated lecture notes

- [[courses/system_programming/lectures/en/2026-09-02-lecture-01|2026-09-02 lecture notes]]
- [[courses/system_programming/lectures/en/2026-09-07-lecture-02|2026-09-07 lecture notes]]
- [[courses/system_programming/lectures/en/2026-09-09-lecture-03|2026-09-09 lecture notes]]
- [[courses/system_programming/lectures/en/2026-09-23-lecture-06|2026-09-23 lecture notes]]

### Materials and lecture passages

- [Introduction slides 51–54](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx)
- [Memory recap slide 15](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)
- [Pointers slides 13–15](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx)
- [Pointers slides 18–25](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx)
- [Introduction slide 54](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/00.Introduction.pptx)
- [Memory recap slide 4](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)
- [Pointers slides 21–24](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx)
- [Pointers slides 16–18](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx)
- [Pointers slides 26–30](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx)
- [Pointers slides 31–35](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx)
- [Pointers slide 36](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx)
- [Pointers slides 38–39](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/02.CPointers_24a7628c.pptx)
- [Memory recap slides 16–20](https://jhlee1020lee.github.io/2026-fall-study-hub/materials/system_programming/06.MM.Variable.and.Memory.Recap.pptx)
- [[courses/system_programming/transcripts/2026-09-02|September 2 lecture, 01:15:55]]
- [[courses/system_programming/transcripts/2026-09-07|September 7 lecture, 54:41]]
- [[courses/system_programming/transcripts/2026-09-02|September 2 lecture, 01:29:10–01:34:38]]
- [[courses/system_programming/transcripts/2026-09-23|September 23 lecture, 05:36–06:37]]
- [[courses/system_programming/transcripts/2026-09-09|September 9 lecture, 03:08–10:32]]
- [[courses/system_programming/transcripts/2026-09-09|September 9 lecture, 15:26–19:25]]
- [[courses/system_programming/transcripts/2026-09-23|September 23 transcript, 24:43]]

The linked materials are the supplied public slide decks; no PDF page-cache link is available for these sources. Transcript timestamps are plain labels.

### Scope to retain

- Numbers apply to the lecture’s Linux x86-64 target or explicitly schematic addresses.
- Uncertain speech is not recovered speech. The **A3 source typo is interpreted as A3[0][0].
- Only Q1(a) size reasoning is connected. Supplied crash answers or writable placement do not legalize modifying const objects/literals.


---

[[courses/system_programming/units/en/systems-c-build|← Previous: System Programming and Building C Programs]] · [[courses/system_programming/units/index|Unit contents]] · [[courses/system_programming/units/en/state-machines|Next: Character Processing, DFAs, and Decommenter Boundaries →]]
