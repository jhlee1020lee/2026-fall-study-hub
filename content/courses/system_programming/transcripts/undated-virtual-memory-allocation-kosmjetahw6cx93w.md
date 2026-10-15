---
title: "Virtual Memory and Allocation · 보정 STT · 날짜 미확인"
course: system_programming
term: 2026_Fall
course_confidence: materials_and_transcript_matched
tags: [lecture-transcript]
source_kind: corrected_transcript
privacy_redacted: true
verbatim_complete: false
audio_verified: false
date_confidence: unknown
lecture_date: null
source_mode: text_only_practical_20261014
cssclasses: [plain-document]
---

수업 날짜는 미확인이다. 원음 없이 대조한 텍스트이며, 확정할 수 없는 표현은 `[[unclear: …]]`로 남겼다.

````text
00:12 화자 1
So we are using 64 -bit But then out of 64 bits, [[unclear: only 8 bits are currently used. So only 8 bits addressing is possible.]] And then, there are 48 bits in the [[unclear: mature address]] in the CPU instruction. Then, Virtual address is divided into virtual page number part and page offset inside one page. So here we are assuming to use [[unclear: 4GB pages. Typical page size, one page size is 4GB.]] But it can be set to 2MB or 1GB.

01:14 화자 1
So here, 12 bits are used for offset within one page. And 36 bits are used to look up the virtual page number. Sorry, look up the physical page number. So 36 bits is the part for virtual page number. Using this number, you look up physical page number. And you go there, you put the page, and then using the VPO, virtual page offset, you go to do [[unclear: exact starting type reference]]. Then this one, in order to do the translation, you need to do the page table lookup. But then, page table is in memory. So [[unclear: it doesn't make any sense actually]].

02:11 화자 1
If you put every memory as you need to look up another memory, that doesn't make sense. So we have TLB, which is hardware that's attached to the CPU itself. So that's the cache of the page table entries. So this is cache. And then each entry is a page table entry. And then, so the [[unclear: 46 bits]] is now divided into [[unclear: TLB and TLB TLB]] So 4 bits is used to choose one of these sets. is cache, it's a set associative. So it has n, so 16 sets. And each set has four entries, so four ways.

03:08 화자 1
Any of these four slots you can go into, as long as you match to [[unclear: the same This]] is called way. So four bits are used to identify the set. And then you have four possible slots for match. Then you do the parallel match with what? [[unclear: TLB cache. 32 bits.]] And [[unclear: if that batch, it caches the matches. Entire 36 bits.]] And if it's a cache hit, TLB hit. the output is what? PPN. physical page number of 40 bits. and then output is...

04:28 화자 1
So, PPN and PPO, by looking now, you have physical memory address. You do not see anywhere in your computer. You cannot print out this one. Only it's visible to CPU. [[unclear: Inside comma, maybe.]] But using this number, it looks up the cache. Now, if the data itself is inside the cache, I want to use it instead of going to the actual memory and reading. Why? Memory access is slow. [[unclear: It takes hundred cycles.]] But then cache lookup is much faster. [[unclear: Few cycles.]]

05:26 화자 1
So then, so this [[unclear: These 52 bits are not used to access the cache here]], we will talk about the data cache, the cache. And then also, this is divided into three portions, one is tag, similar to the TLB tag. The remaining 12 bits, the first 6 bits is used as to identify the set inside this data cache. Index, right? So there are 64 sets. That's why it's 6.

06:20 화자 1
Because 6 bits can represent a number [[unclear: from 0 to 64 different Set ID rate]]. And what about the CO? Cache offset. The offset inside the cache line. And cache line size is 64 bytes. Cache line is, so this is kind of, in turn, called cache block. One cache block in CPU cache is called cache line. That's 64 bytes in Cache. recent CPU. Okay? And then why is it 6 bits? Yeah, this guy identifies out of 64 bytes cache line, right? [[unclear: Which byte should be studied.]]

07:17 화자 1
So you need to have [[unclear: 60 bits]] to go to the exact that byte. Okay, so within one cache line, it is a byte of C. [[unclear: Cache line is 6.]] And the 40 bits, [[unclear: once the standard is chosen]], you need to choose one of these 8 blocks, 8 lines, so 8 -way. Okay, and that CT, of course, you do parallel matching. Okay? And if it's a cache miss, tlb you now really want to use page table lookup. But this is slow, because [[unclear: this is software]]. Okay? And the [[unclear: page table 36 gets huge number]]. 36 gets huge number and then [[unclear: you can have a university]]. But it's easy. So they have multiple levels.

08:17 화자 1
So we say we walk through this page table. Multi -level page table. It's called multi -level page table. And then 36 nicely divided for 9 bits each. So, then you go to the first, the highest 9 bits, I used to identify the level 1 page table. So how many entries are there in the level 1? 512. Why? 9 bits. So if you [[unclear: choose voluntary]], then It has what? Starting point of the next level page table.

09:14 화자 1
Okay, so let's say one of these entry now points to this guy. And then this guy, in order to find the right entry, inside this guy, use 9 bits. Okay? So how many entries in this table? [[unclear: Same, same, partial.]] But then, of course, if all of these entries are full, you'd have many, many [[unclear: dissipated H tables]] that eventually build up the entire to the 36 bits but that's very little. Typically your LS or CAT is very small. It's [[unclear: less than one millimeter. Entire program is actually less than one millimeter.]] And page table should be very small.

10:11 화자 1
You don't want to waste a lot of memory or page table per process. So typically this guy is small and then yes finally if you reach here the address here actually points to actual physical location So let's look at, this is what I just said. So CR3 is a register, CPU register, and that is supposed to [[unclear: have the page table entry of a process]]. So each time you do context switching, CR3 changes to point to the page table, start address the page table of that process, I think. So it's multi -level.

11:09 화자 1
And then, so each individual entry covers, right, 512 gigabyte memory. And then here, next level is each entry covers one gigabyte. Here it's entry covers 2MB. The last one 4K. That's why the page size can be 4K 2MB to 1GB. But then, yeah, default is 4K. And then [[unclear: it's rare to have 2MB to 1GB page size, but it's default]]. Because you will [[unclear: waste a lot of time]]. Each individual page is 1GB. If your program is not big enough, you will not use all that memory.

12:05 화자 1
And then eventually, 40 bits physical page number is retrieved from the table entry. But offset is exactly the same. From virtual page offset to physical page offset. So let's look at the [[unclear: level of what I updated the slide]]. So if you see like It's 64 bits for each entry. And then if you look at the middle, 40 bits used to go to the next level of page table entry. Page table, physical base address, the 40 bits. And then there are many bit flags.

13:03 화자 1
P, if you look at the rightmost flag, P present, the [[unclear: page table entry present in the physical memory order]]. One, one, zero, and R, W, whether this is read only, right, right, right, Read -only or read -write access permissions for all descendant memory areas. [[unclear: Not just the central.]] Read -only or read -write access permissions for all pages which are [[unclear: through the central]]. US, whether this is used by [[unclear: user or common. Supervised common.]] WT. Whether this cache type is [[unclear: write back or write.]] And CD cache, it can disable cache.

14:02 화자 1
Every time you do memory access, you actually go to memory. So CD is also another bit. A is access something. I just said earlier, when you do memory access, this bit is automatically on right after. But then what I was wrong is that this one is set when the page table lookup is done and brought into the TLB cache. [[unclear: Only once.]] And then, [[unclear: the next step, web access]] won't change, it won't set the access again because it's already set. It's set by the hardware.

14:55 화자 1
But then, as I said earlier, when you do page replacement in OS, let's say the physical pages are full, and then you want to [[unclear: read board memory]]. You want to allocate more memory, read from disk, right? Then you need to kick out, right? So, pick out, right? Then, what algorithm that's widely used is called [[unclear: plug, or second hand]]. If [[unclear: this access with its own]], Then OS will clear it to zero and then move on. I'll give you a second chance. And then if you bump into a page that has [[unclear: access speed zero]], then OS will just kick up. [[unclear: That's an approximation of error.]]

15:51 화자 1
PS, page size, 0 means that you point to the next level table, 1 means that you are using large or huge page. You stop here and then [[unclear: point actual page table, physical page address]], now point to actual page. It can be 1GB, or [[unclear: QMegaWatt]], right? G, when G is on, it means that don't evict from TLB on task switch. XD, executable. [[unclear: Whether this, the page is reachable through this entry or executable.]]

16:44 화자 1
For example, physical page address, [[unclear: only most significant bits]] of physical page table address. Of course, force page tables to be 4K aligned. Then the last level, level 4 page, page table entry is slightly different because now the 40 bits address now points to the actual page. P is whether [[unclear: child case is present in the data]]. Rw again is read -only or read -write. [[unclear: Us provides user accessible]]. Wt, cd same thing. A is the same thing but then it is d. And then set by MMU [[unclear: for the right]]. [[unclear: case is 30]]. Modify.

17:44 화자 1
It's cleared by software. G, same thing. X, the same thing. So x86_64, the address translation. Currently, we use only 48 bits out of 64 bits. [[unclear: 48 bits is what's your page number.]] If you think about full 64 -bit address space, that's 16 exabytes. That's probably two big things. 48 -bit implementation provides 256 terabytes of usable virtual address space. This is very useful. Even in the data center, you will see much machine that has [[unclear: more than one computer.]]

18:43 화자 1
[[unclear: 2 .6 terabytes possible?]] I'm not sure if we have enough memory slots here. But yeah, theoretically possible. It's supportable by the operating system, that's why I think. Top 16 bits are sign -extended from bit 47, forming two canonical halves. So [[unclear: 48 bits out of 16 bits]], so [[unclear: the main bits are 16 bits]], right? So, so the... It uses...

19:38 화자 1
Okay, so whether the address is either starts with FFFF or 0000. [[unclear: 00007 or FFFF8]]. Then if you combine them all, [[unclear: it's 488]]. Okay, and then the upper part is used for kernel. The lower part is used for user addresses. Right, uh, what you want to remember is that [[unclear: abstract is a physical memory]] maintained with a per -process address translation. [[unclear: So, no virtual memory, it's just too natural. Without virtual memory, if you come up with virtual memory, that's difficult.]]

20:33 화자 1
This is, I think, [[unclear: one profound consent in the process]]. Very nice idea, actually. Otherwise, you need to deal with physical memories with multiple different process at the same time. And then you need to take up all this isolation, security, sharing, the same memory of the address space. That's the thing. So instead, each process is different. Most of it is true, right? [[unclear: Most processes do not communicate with other processes.]] So you have your own world. And then, don't worry, you will be given entire 64 -bit memory space. That's a lie, of course. Of course, you cannot use just randomly access it. But then, there's a rule. In order to use the memory, you need to allocate.

21:30 화자 1
Allocate means that OS should grant or... You should ask me, [[unclear: OSB]], to use the memory for permission. That's the implementation. But the idea of virtualization, virtual memory first, and then we move on to virtual machine, that's a very good idea. that solves many [[unclear: high -durability things]], right? That's why we call it abstraction. Dealing with physical memory directly is very complex. [[unclear: It's an error.]] you can run multiple OS using the physical machine together. But that's also difficult, right? So instead, [[unclear: just fold the OS itself]].

22:31 화자 1
And then the system software just provides [[unclear: that solution]] that there is another world, actual hardware. But then [[unclear: that's inventory]]. That's virtual machine. Also, the disk partition, /dev something, that can be virtual too. If you go there, actually behind the scene, you need to do [[unclear: depth of communication]]. So it hides the things, but still anything that runs above still works without changing anything. This is correct. Of course there is a [[unclear: performance application]]. But then, we do, this is research actually for performance.

23:25 화자 1
Anyway, we came up with the [[unclear: PER process, for instance]], we can make it through, we can put it in hardware, and we can use it in Linux, or maybe in OS. We have a [[unclear: private library, so we have a post -multiply library]], but then you can make some pages shared.

23:40 화자 2
Okay.

23:41 화자 1
And then [[unclear: fixing both the process with the larger workspace]] into one physical space. And then when memory, even when the physical memory amount is small, you can still run it because you can use the disk space. You can just also think that disk space is an extension of the physical memory. [[unclear: That's paging and]] And then you can create permission for each page, page level of permission, [[unclear: not the height please]] this is executable uh we don't need inside you can say okay let's move on.

24:39 화자 2
Thank you.

24:43 화자 3
I have a question, sir. Why is the physical memory page number is 40 bits instead of 36 bits?

24:57 화자 1
[[unclear: Every question. no need for that.]]

25:04 화자 2
Thank you.

25:05 화자 1
[[unclear: It never changes when the memory technology improves it.]] If you need truly huge memory, you can extend it. But it's kind of difficult.

25:16 화자 2
Thank you.

25:17 화자 1
So I don't know.

25:19 화자 2
Thank you.

25:20 화자 3
[[unclear: Amen.]]

25:20 화자 1
Like [[unclear: x sub i to measure b]]. But then it gives you [[unclear: real d]], maybe it could change too. This is one implementation. Or if it's [[unclear: not fixed, like fundamental limitation]] as far as you know.

25:34 화자 3
I mean the virtual page number is [[unclear: 30 Bye]]. And the physical page number is meanwhile 40 bits.

25:50 화자 1
Right, right, right. So then you can divide multiple regions, and [[unclear: some of the processors]] use some region, and some of the other processors use another region. So of course, 36 bits cannot accept all 40 bits. That's not the goal.

26:10 화자 2
Okay?

26:11 화자 1
40 bits is still used for a unified physical memory address but then note that this one is a per process right so if you have enough process you can use uh [[unclear: entire 40 bits]] actually but then just just internal mapping um so [[unclear: four bits you have left over]] right then you can still use it or if you have enough uh Any other questions? I think another reason is 36 is like... No. So that will also reduce the memory for page table. 36. So 36 is how many... [[unclear: Still, 256...]]

27:11 화자 1
But yeah, still I think it's possible that CPU vendor and memory vendor are different. I think maybe the [[unclear: memory vendor sees the future]], Ah, we will support 40 bits. That's why it has to be translated to 40 bits. That's my guess. But then again, even if you have the full memory that can be accessed by 40 bits, you can still use them all [[unclear: if you have enough]] Okay, let's move on. Dynamic memory allocation. So we learned basic concepts and K&R implementations overview. basic concept. So we learned that and we were able to review it again.

28:06 화자 1
And then heap and fragmentation and then K&R implementation overview probably we won't go through this part today because we have a Q &A session for the latter part of this lecture. So why is dynamic memory allocation necessary? You cannot, why not just use global variables? Because the size of such data structure may be known only at runtime. But when you think about it, you know how to do, you know how to write code with Python. [[unclear: Python does not have it.]] Oh, something's wrong. No. [[unclear: Python, .j4, you are wonderful.]] You don't explicitly...

29:04 화자 1
So in C, whenever you want to use new memory, you need to explicitly ask for it, unless that's allocated in local variable. But then Python, whenever you assign or you create memory, it dynamically allocates inside. And then when you're done using it, it automatically reclaims. That's very good. Very convenient. And then it avoids errors. But then, again, [[unclear: it's not efficient. It cannot be efficient if it's slow.]]

29:43 화자 2
Okay.

29:45 화자 1
[[unclear: The binary can only get three memory as needed for just.]]

29:50 화자 2
Thank you.

29:51 화자 1
And then some of the languages make it explicit. Typical languages also [[unclear: do hardware like C, C++]]. And some of them is implicit. High level languages, functional languages. You don't call memory allocation. JavaScript Python. Of course you can use C library in Python, but then you [[unclear: cannot call the output can't read]]. But that's kind of exceptional.

30:25 화자 2
Thank you.

30:27 화자 1
C++, if you look at [[unclear: STL, template library]],

30:34 화자 2
Thank you.

30:36 화자 1
So [[unclear: inside the classic]], that was actually new.

30:44 화자 2
Thank you.

30:46 화자 1
So these are the library functions that are related to dynamic memory allocation. malloc and calloc. What's the difference between malloc and calloc?

30:58 화자 2
Thank you.

31:00 화자 1
So it's a calloc initializes the content to 0.

31:04 화자 2
Thank you.

31:04 화자 1
So which one should be slower? But yeah, don't worry too much about the [[unclear: But most time, performance is not needed.]] Most applications, if you write that you need performance, you can But that's why you need to know it. realloc. What is a realloc? Have you ever used a realloc?

31:36 화자 2
Okay.

31:37 화자 1
I have not used [[unclear: realloc n]]. Okay, okay, good. We will explain that in the next slide. So when you're done using it, you need to return it back to [[unclear: what? 3.]] Actually, [[unclear: that log n 3]] looks like system calls. But not really. It's like standard library. Okay, so it tries to allocate the memory from OS when the library does not have memory available. So it's a We saw standard IO and [[unclear: Unix type]], right? [[unclear: Unix type]] is a system call.

32:24 화자 2
Okay.

32:24 화자 1
[[unclear: Second IO tries to optimize it by filtering. Melbourne does the filtering.]]

32:31 화자 2
Thank you.

32:32 화자 1
And you will [[unclear: implement that for free]]. Because you will implement malloc and free. Free is the same thing. Eventually when it does not have enough memory, it calls a system. brk or mmap. And that's implemented by OS. So, in Korean, it's [[unclear: called domain]]. It's a big thing. You have to divide it into multiple things.

32:56 화자 2
Okay.

32:57 화자 1
It's a whole thing, okay? [[unclear: Over at...]]

33:03 화자 2
[[unclear: Heights.]]

33:04 화자 1
It's very similar to the malloc, but then it allocates memory inside the stack. So when you call function call, and then you can do some memory, dynamic memory, and then you call alloca, and use it inside that function. And when you return from the function, that memory is automatically reclaimed. You don't need to call free. And [[unclear: you can use this memory across multiple functions]]. Just like a local variable that is dynamically sized. Okay? [[unclear: Next break]], we will see that soon. Basically, you have inside your program, a memory space, right? There is a code section, a [[unclear: business section]], data section.

34:02 화자 1
At the end of data section is the last line is called program break.

34:08 화자 2
Thank you.

34:11 화자 1
Is implemented by moving up [[unclear: this grid line]].

34:17 화자 2
Thank you.

34:18 화자 1
And then in order to move the line, you can use this [[unclear: best break]]. [[unclear: This one]] is, you allocate memory already. Then you want to resize it. I want to increase the memory size.

34:41 화자 2
Wait.

34:42 화자 1
Of the already dynamically allocated memory. PTR is the pointer to the dynamically allocated memory.

34:52 화자 2
Okay.

34:53 화자 1
And then you know that [[unclear: our sizes are 5]] but then I want to grow it to 10. Okay, which size? Then you call realloc using this pointer and then the new size, you know,

35:06 화자 2
Okay.

35:07 화자 1
Which is resizing [[unclear: dynamically LQ]]. PTR must point to a memory block obtained by [[unclear: previous column error, CRO or VNAP]].

35:18 화자 2
Okay.

35:19 화자 1
And size represents the new size of the block, which may be, it can be [[unclear: a largely kip's order]].

35:25 화자 2
Okay.

35:26 화자 1
Than the [[unclear: original sample.]] Return value, when it succeeds, it returns a pointer to the newly allocated memory, which may or may not be different from PTR.

35:42 화자 2
Okay.

35:44 화자 1
[[unclear: Most times it will be the same]], but sometimes it can be different. Why? Because I want to allocate more, but then you cannot allocate in place. Then we allocate another memory, [[unclear: bit memory]], and then move the existing content there, and then return. So the return value can be different from PTR. This is a very important thing. Properties of realloc. So another thing is if realloc fails, it returns null. That doesn't mean that existing PTR, existing memory is free. No. It just says, I cannot do this.

36:33 화자 2
Okay.

36:35 화자 1
So it's a really bad idea to return value. So you call [[unclear: realloc P n]], right? And then assign it to P.

36:46 화자 2
Thank you.

36:47 화자 1
If it's null, then you lose the previous pointer. Actually, I will show that there is a [[unclear: quote example]]. That's wrong. But then, yeah, you need to think about this failure case. Because if it's null, you cannot re -access because you updated the PTR itself. So don't do that. Typically, you have a temporary pointer, then you get the return value, and see whether that's not null, then you can update and see whether it's the same as PTR. Like this. When memory is expanding, realloc doesn't initialize the newly added bytes, but not initialize them. [[unclear: Same as a model.]] When ptr is null, [[unclear: if the first parameter is null, then it's the same as null]].

37:47 화자 1
[[unclear: When the size is zero, that same is free.]] So you can, realloc just covers everything. [[unclear: With real doggy doggy, they'll love it.]]

37:59 화자 2
Thank you.

38:01 화자 1
So we [[unclear: expect number]] to be reasonably efficient with reducing the size. Reducing the size is.

38:09 화자 2
[[unclear: Amen.]]

38:10 화자 1
And then the return value, [[unclear: it's always successful]]. There is no... I don't know why it should fail. When reducing the size, the realloc should shrink the block in place. The [[unclear: return value is the same as the first parameter]]. And then, the realloc [[unclear: always attempts]] to expand the block without moving. So it tries to... We need... realloc [[unclear: always attempts]] to extend the block without moving it. So when you want to increase the size, it tries to increase the in -place data. See if the next memory is available, it's not being used by other people. Then you can increase it. But if the next neighboring memory is already being used, you cannot actually extend it in place.

39:09 화자 1
So we could move the memory block. If it cannot enlarge PTR in place, if it allocates a new block elsewhere, then what's nice is it already copies existing content there. And then returns the pointer. In that case, the return pointer is not the same as PTR. Make sure to update. Then the problem is that if you have just one pointer that's increased, that's it. But let's say you have a memory block that's shared by multiple other pointers in hash table for example, and then you want to increase this guy. [[unclear: All these pointers should be updated.]]

40:00 화자 1
So if you call realloc, you think about whether some of the other points that were pointing to the previous memory block. In that case, you need to update all of them. So this is an example of malloc and realloc. So we allocate n integers. And [[unclear: p is double]]. Then you call perror. What is perror? You know, malloc. So perror prints out error message. And then [[unclear: meld meld col so meld is the string, meld col and error]] [[unclear: And then x]], you stop here. And then you initialize the array, and then you enlarge it.

40:58 화자 1
As I said earlier, don't use it with p. If it's null, then you cannot really go to previous memory again. This is a wrong example, okay? But here, [[unclear: if you know, it's tough]]. So maybe it's okay. So you may enlarge the memory size from [[unclear: N, N +M insert initializing]], then you call free. Okay?

41:37 화자 1
right and then allocate 1024 bytes and then reallocate so [[unclear: 1024 bytes and reallocate]] we call you realloc and then now it [[unclear: increased to 2048]] so fortunately you could extend the block if.

42:00 화자 2
Thank you.

42:01 화자 1
So the return value is [[unclear: the same as before]].

42:04 화자 2
Thank you.

42:08 화자 1
I think this is just an example. Probably you know this. malloc may ask for a arbitrary number of bytes, memory may be allocated in [[unclear: three different order]]. very natural, cannot reorder requests to improve performance. So here we allocate [[unclear: 3 bytes, 1 byte, 4 bytes, 4 bytes, sorry. 3, 1 by 4 bytes]] and then you free one byte, P2. There is a hole in the middle. And then [[unclear: 6 bytes, P3 is free like this]]. So when you do [[unclear: Belmont -K3]] many times, you will see many fragmentations. That's one problem that we need to deal with.

43:04 화자 2
Thank you.

43:05 화자 1
So even if there's many small holes in the middle, and [[unclear: even if some of the small hole is big enough, you cannot find big enough hole]]. So you cannot sometimes allocate.

43:20 화자 2
Okay.

43:26 화자 1
And then typically heap.

43:28 화자 2
Thank you.

43:28 화자 1
Grows from lower address to higher address. So sometimes we [[unclear: draw from zero to higher address]]. The most time we [[unclear: draw from zero to higher address]].

43:40 화자 2
Thank you.

43:41 화자 1
So don't be confused. So [[unclear: stack grows from higher address to lower address]]. Who's allocating the stack?

43:53 화자 2
Thank you.

43:55 화자 1
Okay, in order to use that you need to get permission. So when a program, first of all, the stack is allocated by OS for you,

44:04 화자 2
Okay.

44:05 화자 1
And then they put it out, [[unclear: Linux is one megabyte, one megabyte is out]]. If you go beyond one megabyte, what happens?

44:17 화자 2
Thank you.

44:20 화자 1
So that goes to the thing, what happens? It crashes. OS is very cruel. When you violate the rules, it crashes. So stack overflow is not that good. When do you see this? Does it happen when you have too many local variables? Theoretically yes, but that's very rare. [[unclear: If you have a big array, then it doesn't even compile.]] And then typical thing is that you need to function call, typically recursive call, without coming out. Then you call function call, function call, function call over and over again, and then each function call uses a little bit of stack.

45:21 화자 1
Eventually all the stack memory will be used. If the stack overflow happens, then it crashes. Let's go to the heap. So dynamic memory is allocated in an area called the heap. Again, this is a logical term. That's human understanding. If you go to the [[unclear: D -VAN]], everything is there. It has just the memory address and then You'd have to say, Oh, [[unclear: this part is here, this part is gone]]. Physical memory doesn't make sense, right? Because we are talking about virtual memory, virtual process. For each process, we think that the world looks like this. Okay? And then there are some parts that are [[unclear: used only for rhythm. The code should be rhythm. And then some data is rhythm.]] Constant data. Or what?

46:28 화자 1
the [[unclear: hello world street stuff]], right? [[unclear: That's real.]] Then also there should be some global variables that are read -write data. These are not local variables, right? These are global variables. And then, so at the end of the data section, this is called break. okay and then typically when you when you allocate small amount of memory you use this [[unclear: breakpoint]] right upward from lower address to higher that you can use more of course in order to move that you need to get the permission from the OS so you need to call system call [[unclear: that's great]] okay please allocate this memory at the end of this data section okay This is called heap.

47:21 화자 1
But then if the memory request size is large, so that is a number. [[unclear: In Linux, it's 128 kilobytes]]. Go beyond that. that portion anymore, it calls [[unclear: anywhere in the module memory space]] because it's using, it calls mmap. We learned, we saw mmap, mmap is very versatile. You can, basically it can, it allocates memory, but then also it can provide, you can set the properties of pages directly. So eventually, malloc is either using [[unclear: brk, sbrk or mmap]] to do the allocation for you when it needs actual memory. Otherwise, if the request can be satisfied from its buffered memory, then it doesn't need to call this system.

48:24 화자 1
All this [[unclear: melacalopithelium]] is used by brk and mmap if the memory is needed. So managed by [[unclear: tiny memory, allocate implement in the C set of library]]. libc uses system calls to the kernel to manage the [[unclear: upper end of the...]] So libc runs in the user library. So libc is just there for your convenience. It doesn't have to be always [[unclear: mellow, you can use some unlock]]. And then you can implement your own memory allocator yourself. Using the no need, because this is standard.

49:17 화자 1
See standard library, so whenever you write code you can see this library comes with you. But implementation can be different from version to version. Interfaces. How does [[unclear: Alan Moyer heat membrane]] moves the program break downward So it's okay. So it assumes that the [[unclear: upper location is a lower address. The download is going to be higher address]]. So I think I need to make it consistent. Again, break allocated memory from lower address to higher address. using sbrk or brk.

50:11 화자 1
sbrk, the parameter is amount of allocated memory, the size, the increment size. The increment program break, the end of the data set segment by the specified amount. Calling the function with increment of zero returns current position. [[unclear: Current question on program break]]. Return the pointer to the previous program break if successful and [[unclear: -1 otherwise]]. And then [[unclear: brk fits virtually same as sbrk]], just different interface. So it just sets new program break.

51:01 화자 1
Move the program break to the [[unclear: special address, if it's 0, if it's accessible, then -1, otherwise]] So you can [[unclear: allocate more, you can also allocate as well]]. When you are done with memory, you can return your memory [[unclear: back to yours]]. Having acquired heap memory, [[unclear: how do you allocate free]]? Again, this is the user level. Now you get the product. It's a whole set of products. You can manage it when the user wants some of the product. How do you manage this? This is a topic of much research in the past.

52:00 화자 1
then what we will learn here is [[unclear: subset of Linux documentation]]. Okay, so we will see some of We have simple implementation and then we try to understand the problems with simple implementation and then try to improve it. We show some techniques but [[unclear: all of these techniques are actually used by Linux]]. But then of course Linux has more. And then there are other implementations. FreeBSD implementation, Google implementation, Microsoft implementation, academic implementation. So used to be a lot of research in the past, [[unclear: like 20 years ago]]. These days, Yeah, performance is a reasonable deal. If you want allocated for specific use, maybe you can come up with your own implementation.

52:59 화자 1
But then, if it's for general purpose, general purpose means that it should be reasonably good for all the cases. Then I think [[unclear: Linux implementation is not that good]]. So what are the goals for a [[unclear: value -added working fleet]]? Of course, the speed should be good, right? The throughput should be good. Maximize throughput. What is the throughput? What is the difference in throughput? Number of jobs done per unit time, per second. How many requests you can satisfy per second. You can do per second. So it talks about the speed, right? Maximize the number of requests in the period of time. If both, this is a [[unclear: bell -locking frame]], both of them should have good throughput.

53:56 화자 1
Okay, the calls for both of the And then there is also memory utilization. It's really fast, but then if you call a little bit of a request, the memory is full. You cannot help him. That's not good. So minimize the amount of wasted memory. I talked about the fragmentation. I need to minimize also the data structures. data structure to manage these wholesale products. If that takes up too much memory, that's also not very good. So strawman approach. Strawman approach means that [[unclear: reasonable presence. First class]], but if you think about it, oh, that makes sense. [[unclear: approach of free]].

54:53 화자 1
So you implement free and then inside free you just call return. That's really fast. But then yes, [[unclear: memory utilization is really good. It's a little bad.]] So it doesn't make sense. Strawman [[unclear: approach for mail]]. basically malloc, so you get chunk of memory, a bill of memory from, the dynamic memory from OS. And then you will give some portion to the user. Of course, the user will call [[unclear: Metalog -M3]] not in the same order, right? Kind of random, right? Then you will see, as you move over, you will see a hole in the middle. And then what you need to do is that the user, I want a certain size memory. Then you need to scan this blocks, right? Available portion.

55:51 화자 1
And then find the right one and return. Okay? So best fit means that you find the block that's the [[unclear: perfect size]], right? That's the fit best, the request size. Then if you want to find the best fit, sometimes it's slow. But depending on the implementation, right? Sometimes it's slow. you may have to scan the list sometimes depending on your computer. So yeah, malloc finds the best fit that's best for memory utilization but that is [[unclear: poor, you know, linked to poor]]. Make sense? Right.

56:40 화자 1
So basically what malloc does is it maintains a list of a track, it keeps tracks of the free blocks, which portion is free and that is not being used by the user so that you can deliver it to the malloc. Maintain a list of free blocks. Allocate memory from all these blocks in the free list. And deallocate memory by returning the block to the free list. When necessary, you call sbrk. sbrk. When necessary, it means that you cannot really satisfy this request. Then you allocate [[unclear: more memory from yours]] using sbrk. [[unclear: to TSOS]] for additional memory and create a [[unclear: new large memory]]. So many questions, design questions. How do you keep track of these?

57:38 화자 2
Okay.

57:39 화자 1
How to choose the [[unclear: appropriate film one]]? How to deal with leftover space in a free block? How to deal with a block that has just been free? So these are design questions. So you approach this system problem like this. You have all, you think about these questions and then answer your own idea. And then in industry, [[unclear: implementation comes by AI]]. But we need to do the implementation ourselves here. That's how it works. So this is a very important thing. So I briefly talk about fragmentation.

58:39 화자 1
a while ago. But then, fragmentation is divided into two types. One is internal fragmentation and the other is external fragmentation. So what is internal fragmentation? So allocate block is larger than a malloc request. So, Let's say [[unclear: now look]], internally it manages this free of block in the [[unclear: unity of 64 bytes]].

59:11 화자 2
Okay?

59:13 화자 1
But then the user asked for 33 bytes. So [[unclear: it returns 33 bytes. No block.]] But then remaining 31 bytes, right? That's unused. That cannot be allocated for [[unclear: another metal frame]]. This is called internal fragmentation. So you allocate the block size. The allocation block size is larger than the requested memory size. So there should be leftovers that cannot be used by anybody.

59:53 화자 2
Okay.

59:54 화자 1
That's called internal fragmentation. External fragmentation is actually what we saw.

01:00:00 화자 2
Thank you.

01:00:02 화자 1
Enough free memory exists, but no block is big enough. So malloc asks for [[unclear: 120 continuous bytes]], but then [[unclear: 64 bytes is 4 bytes, 4 bytes here]], but then they are not continuous.

01:00:20 화자 2
Okay.

01:00:25 화자 1
[[unclear: So you can allocate.]] This is called external fragmentation.

01:00:31 화자 2
Okay.

01:00:35 화자 1
So K&R [[unclear: polygon in which]].

01:00:39 화자 2
Thank you.

01:00:40 화자 1
So, [[unclear: Rich, again here, David Slott]], who invented C, and also Unix as well. [[unclear: kirlingon is his friend]]. and they wrote a book together called c program language. actually, [[unclear: c program language, 1988 version]], if you look at it, you see this scope. [[unclear: only 20 lines of scope]]. Very simple, elegant, reasonably fast, but not always fast. Memory allocated in what? So they, again, the memory is allocated in multiples of a base size. Not just a variable size. You have a big chunk, but then you divide the big chunk into fixed size blocks. Okay? [[unclear: 16 bytes, it can be 16 bytes, 32 bytes, 48 bytes]]. And then you have a linked list of free blocks.

01:01:35 화자 1
malloc and free walk through the list to allocate and deallocate. So you have a list, free block list. And then malloc and free walk through the list. malloc allocates the first big enough block. Okay? and to avoid picking up plot, and then it is called first fit. So it turns the list. So in the worst case [[unclear: it can be O]] that's very bad for every time, every call, [[unclear: every valid call in this treasurer O]] that's really slow. So it tries to minimize the [[unclear: treasurer's time]]. So it goes against the [[unclear: first picking up plot]] and then Then we split the free block. To allocate what is needed, leave the rest available.

01:02:40 화자 1
And then, linked list circular, to be able to continue where we left off, linked list in the order of blocks appear, then [[unclear: appear in main group]]. So linked list, it maintains a linked list, and the free blocks are sorted by their [[unclear: first binaries]] in the list. Okay? Why? Because when you free it, you may want to find your neighbor first and make it larger. Initially, there is just one block. Allocation granularity, even if you allocate one byte, it allocates unisize. That's it, [[unclear: unisize 16 bytes allocated]]. For the 16 bytes, so you split 16 bytes and return it to the user.

01:03:39 화자 1
Remaining block should be split and then should be left in the free-block list.

01:03:50 화자 4
That's [[unclear: this part]].

01:03:51 화자 1
You allocate what is needed and leave the rest available. And then when you do this [[unclear: value gain free]] multiple times, you will see this list. And then when malloc comes in, you need to find enough block that's enough, that's [[unclear: larger than me]], It can be the block itself may be big. In that case, you split the block again, right? Block it, and then only the requested block will be returned to here. [[unclear: So I think--]]

01:04:35 화자 2
Thank you.

01:04:36 화자 1
We will actually see.

01:04:38 화자 4
[[unclear: Study.]]

01:04:39 화자 1
This a little bit again next time but we'll do Q &A [[unclear: for the left]].

01:05:15 화자 2
Thank you. Thank you.

01:05:48 화자 4
Hello, this is Q &A session for Lab 2. I first shared two assignment updates that were previously announced on the ETL. As in Lab 1, we [[unclear: updated the Makefile]] so that a code history file is automatically created and updated whenever you compile your code using the make command. So please include the [[unclear: history directory]] when you submit your solution. But we know that some of you had already started the assignment before this update. So [[unclear: work completed before the update will be taken into account carefully during grading]]. The next is reference binary file.

01:06:46 화자 4
There was a missing case in the pattern matching logic of the reference binary. More specifically, when the [[unclear: pattern ab]] was used, but [[unclear: file named a was not printed correctly]] previously. So we have fixed the issue and uploaded a new version of [[unclear: assignment to tar .gz]] compressed file. We are very sorry for the inconvenience caused by these two issues. [[unclear: I have checked the have already submitted the assignment]] so please check the update and resubmit if necessary.

01:07:37 화자 4
I have noticed that today Today, the assignment will be updated once again. Sorry for that. That is, in the tools directory, the [[unclear: compare.sh file is missed]]. So, I will add the file and update soon.

01:08:09 화자 5
Yeah.

01:08:13 화자 4
No, this is our, for the convenience. [[unclear: The computer that SSY is for.]]

01:08:24 화자 5
Thank you. Good.

01:08:29 화자 4
Compare the outputs between your solution and [[unclear: reference pipe]], reference solution. So,

01:08:36 화자 5
Thank you.

01:08:38 화자 4
Yeah.

01:08:38 화자 5
[[unclear: How did they begin this?]]

01:08:50 화자 4
I think so. Next, I share some questions posted on the ETL board. These two questions are about the meaning of macros. First is [[unclear: the max macro]]. This means the maximum number of root directories that can be given as command line arguments. The [[unclear: maximum is 64]]. And [[unclear: then max macro refers to the length of the relative path]] from the current root directory to each file or directory entry. In our grading test cases, you can assume that this [[unclear: relative path will never exceed the max]] So you may simply use these macros for your solutions.

01:09:51 화자 4
Yep.

01:09:52 화자 5
What's the difference between [[unclear: death and death in the young]]? What do you mean by it's [[unclear: a poor thing to do]]?

01:10:08 화자 4
Yeah.

01:10:09 화자 5
Thank you.

01:10:21 화자 4
And this question is important. Should we expect a directory to contain an arbitrary number of entries? The answer is yes. In other words, you should not assume a fixed maximum number of entries in a single directory. So, since you do not know in advance how many entries a directory may contain or [[unclear: any APIs for that]], you need to carefully design how to store them temporarily before sorting the entries. For example, dynamically growing the allocated memory using [[unclear: a realloc]] would be a reasonable approach.

01:11:10 화자 2
Yep.

01:11:12 화자 4
Yeah, we learned two things. When is the time to [[unclear: use the yellow]]? But the exact implementation is up to you as long as your program can correctly handle directories with varying numbers of entries and sort them as required. [[unclear: The unnoticed questions]] is... Is that all? Good. Before we go to the demo.

01:11:59 화자 2
You know what I mean?

01:11:59 화자 4
Before we show the demo commands, any other questions? Then I showed the demo commands and how to run and build the lab 2. [[unclear: Can you show this?]]

01:12:58 화자 4
Assignment 2, [[unclear: the 2 directory structure is shown there]]. Let's.

01:13:13 화자 2
Thank you.

01:13:19 화자 4
First, in the lab 1, we added the [[unclear: make history file macros]]. So if you run the make command, then.

01:13:33 화자 2
[[unclear: Peace.]]

01:13:34 화자 4
You can show and you can see that the [[unclear: history of the tree is]] And in that directory, the [[unclear: coding loads that you write, you load the code and get the logs]], it's included. So if you submit your solutions, please include the history too. And there is reference solution in the reference directory. So...

01:14:48 화자 4
If you test your solution or reference file, then First you should make the sample directory trees. How to make? If you decompress the [[unclear: assignment to file]], then firstly the gentree.sh [[unclear: share file]] and mksock program [[unclear: I have five files]]. You should check the permission for [[unclear: these two files]].

01:15:52 화자 4
And then [[unclear: make the demo screen]].

01:15:57 화자 2
Thank you.

01:15:59 화자 4
And [[unclear: all other data which is.]]

01:16:02 화자 5
Thank you.

01:16:04 화자 4
This is for the example directory structure for using the [[unclear: resume class]]. [[unclear: So if you.]]

01:16:18 화자 2
Thank you.

01:16:21 화자 4
Generally, [[unclear: the SAC make this data structure]].

01:16:30 화자 2
Thank you.

01:16:33 화자 5
What is [[unclear: the argument]]?

01:16:41 화자 2
Thank you.

01:16:54 화자 4
Thank you.

01:17:09 화자 2
Thank you.

01:17:12 화자 5
[[unclear: That sounds happy.]]

01:17:21 화자 2
Thank you. Thank you.

01:17:45 화자 4
[[unclear: Every top tree was and the pest and victory entry name and the plant size and plot size is root.]]

01:18:09 화자 5
It wasn't me.

01:18:18 화자 4
Yep. file size means that the I think [[unclear: the arbitrary file size]].

01:18:55 화자 2
Thank you.

01:19:08 화자 4
Metadata and the [[unclear: plus size]] is the [[unclear: real file size that is stored in the disk and SSD]].

01:19:29 화자 5
[[unclear: If you're not sure what to say,]]

01:19:32 화자 2
Yeah.

01:19:35 화자 5
[[unclear: How do you do?]]

01:19:54 화자 2
[[unclear: Amen.]] Thank you. Thank you. Thank you.

01:20:29 화자 4
For students, [[unclear: I'm sorry for the.]]

01:20:34 화자 2
Um.

01:20:40 화자 5
Okay, can I go ahead and first just ask one question now?

01:20:50 화자 2
Thank you.

01:20:54 화자 5
I see that the new assignment has [[unclear: two different types and they are two different types]]. So I'm wondering if we should [[unclear: replace the original history file with the old file or]].

01:21:09 화자 4
Oh yeah, yeah, yeah, sure. I will [[unclear: take it to the account]] then. [[unclear: Update it to the version.]] You can [[unclear: migrate the history files for the new versions]].
````
