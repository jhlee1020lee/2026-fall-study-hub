---
title: "Dynamic Memory Allocation · 보정 STT · 날짜 미확인"
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
05:13 화자 1
Okay. Thank you.

07:02 화자 2
For some reason, anything doesn't work.

07:05 화자 1
Hello.

07:12 화자 2
So I think we have to wait a little bit.

07:42 화자 1
Okay. First of all, Thank you.

13:09 화자 1
Thank you.

14:26 화자 2
[[unclear: Six times that. Do you have a sloth?]]

14:45 화자 1
Everyone?

14:49 화자 2
[[unclear: Can you go to like, please?]] So we were talking about dynamic memory allocation last time, right? Then we learned malloc and, uh, uh, uh, uh, realloc, right? So page 29, [[unclear: using his memory]], can you go there?

15:24 화자 1
Are you with me?

15:28 화자 2
We were talking about design issues of malloc and free. So as I said earlier, malloc and free [[unclear: a knot system called Heidenstein]]. So it's like standard I /O functions. So you actually, you get, it's like [[unclear: whole statement]]. Whenever you need a [[unclear: dynamic value]], you ask for big chunk, but sometimes small chunk.

16:06 화자 1
Thank you.

16:06 화자 2
You can use this. So I'll try with this. Thank you.

16:16 화자 1
Hold this for a second, please.

16:45 화자 2
I'll try to be good at it again. So this could be one reason. Or just the line between this guy and this guy is another reason. Possible cause.

17:07 화자 1
Thank you.

17:12 화자 2
Yeah, definitely. That is not the problem.

17:17 화자 1
Thank you.

17:21 화자 2
Okay, so let's go back to [[unclear: Mayhem Hall]]. So, page 29, we talked about malloc and free. I just said earlier, malloc is like wholesaler. You get a big chunk from OS OS, and then you dole out, you keep out smaller chunk, [[unclear: resale rate]] to user level application. So, next page.

17:54 화자 1
Okay.

18:07 화자 2
Okay. I wonder why it works. It's so hard. It's hard. Wait a minute. I'm so tired.

18:20 화자 1
I got it.

18:28 화자 2
Let's try. So the [[unclear: goals for malware frame]]. So two goals are important here. So you need to maximize throughput. So we need to find [[unclear: malware frame throughput]], which means that like speed has to be fast. Another thing to consider is memory utilization. So you need to, you should not waste memory. To minimize the amount of waste memory, we need to minimize the size of data structures. These data structures are referred to as [[unclear: data data that we tend to]].

19:09 화자 1
Thank you.

19:10 화자 2
Blocks that memory that themselves are not really useful for the user. These are useful for maintaining So [[unclear: strong and wide]], right? You can write free, you do nothing. [[unclear: You just read.]] Then, the speed is really fast. [[unclear: You put grade]], but you waste a lot of memory. malloc, so in order to maintain [[unclear: three -block straight]], we need to keep [[unclear: each three -block]] as a size. Some blocks are large, some blocks are small.

19:55 화자 2
But then, in order to [[unclear: maximize macro utilization]], In order to maximize the memory utilization, you can try to find the best block that fits the [[unclear: request time]]. But then, typically, [[unclear: these three blocks]] are maintained by a list. So this list operation is a checklist, right? See whether this is big enough, right? And then, yes, if it's a, you can find the best block that perfectly fits the request set. Or the best block, if the, It's the same as the request size, but then it's better than [[unclear: other programs]]. You can find the best way.

20:52 화자 2
You can implement a [[unclear: mellow tube]], which is always the [[unclear: best treatment]]. But then that could be slow. So the goal one, it does not satisfy the goal one, the [[unclear: ecosystemizing process]]. So typically inside malloc, it maintains a list of [[unclear: three blocks of memory]]. Allocate memory from one of the blocks in the free list and deallocate memory by returning the block to the free list. And you do this kind of depending on the application. So you cannot really predict the order of the allocation or deallocation. When necessary, you call sbrk to get the real memory from [[unclear: your saving]]. So any questions? How do we keep track of [[unclear: this frequency]]?

21:53 화자 2
and how to choose appropriate free block to allocate the best fit. We already learned about the strategy best fit. But then you can also do first fit as soon as you bump into a big enough block to allocate. That could be the fastest way. what to do with leftover space in a free block. So if you find a block that's larger than the request size, then you don't want to allocate the entire thing. So you can split the block, and that returns only the amount that's needed to the application, while leftover can be made inside the free block. What do you do with a block that has just been freed?

22:43 화자 2
When you free a block, If you see your [[unclear: Naples block]] is also free, it's also better to [[unclear: merge formats, same word]], to make it bigger. So that even if there's a larger block request, larger memory request, it can actually satisfy it next time. That's another thing to consider. We also need to minimize fragmentation. There are two kinds of fragmentation. One is internal fragmentation. Typical malloc actually operates with [[unclear: a base site]]. So even if you allocate just one byte, it does not allocate exactly one byte. it allocates minimum block size, [[unclear: 16 bytes or 30 bytes]].

23:39 화자 2
So here, the allocation unit block size is 64 bytes. Then let's say the user wants only 33 bytes. Then the remaining 31 bytes are wasted, cannot be reallocated to another That's called [[unclear: internal frequency]]. [[unclear: External frequency]] is that you have enough free memory if you combine all the free memory. But then they are not continuous because you allocate the allocate a random order. So you may have lots of blocks in the middle. So in this case, if you allocate 128 bytes, you cannot allocate [[unclear: 128 that's by continuous]]. So this is called external fragmentation.

24:35 화자 2
So external fragmentation is relative to the request size. So [[unclear: it cannot be exactly the same. Internal fragmentation is the same.]] So you have [[unclear: amino -oxide]] at a wasted amount. Now that's already allocated to a user request. so the first implementation, the approach, is called K&R, [[unclear: current Brian Kernighan and Dan Swich]]. they actually wrote a book called the [[unclear: c programming likage]]. inside the book, they show what you can do. This is a very simple [[unclear: malloc command frame]]. So here is the algorithm. The memory is allocated in [[unclear: multiple databases]].

25:34 화자 2
[[unclear: System might characterize them for inference, etc.]] And then [[unclear: three blocks]] are maintained with a single linked list. malloc and free walks through the list to [[unclear: allocate the allocator]]. And [[unclear: malloc our TST first begin up point]]. So it's not [[unclear: test bit]], [[unclear: it's first bit]]. To avoid, [[unclear: say, pointing further]], so to improve, to have a reasonably good speed, they [[unclear: chose first bit]]. And then, [[unclear: Melano -Poltz's]] splits [[unclear: the break point]]. If the free block is big enough to the much larger than the request size, you split the block in the left over block in the free list so that it can satisfy other lists. And then a linked list is circular. So the tail now points to the head.

26:34 화자 2
There is [[unclear: no head for the tail]]. Why? Because you should be able to continue where you left off. So when you try to find a block, then allocate, then the pointer stays there. [[unclear: So there's another value]], you start from that. Link list is in order of blocks that [[unclear: appear in]] So the link for this is sorted by their memory, start memory. Why? Because when you free the block, then you find the right location to free the list and see whether you can [[unclear: call this]] with [[unclear: your major]]. And these are the basic approaches.

27:37 화자 2
Again, it allocates memory in multiples of base size so that we can avoid maintaining very tiny blocks. So if the block size is one byte, but the data structure that is maintaining requires more than that, that's too much. Then align memory on the size of the largest data type. So it should be multiple, it should be multiple, double, like [[unclear: 8 bytes, pretty]]. Request size is rounded up. So allocation is in the unit of base size. So allocation is not in terms of bytes, number of bytes. Allocation is in terms of number of base blocks or base size. So how do you compute the number of base blocks?

28:35 화자 2
Request size is [[unclear: m bytes]]. And then base size is [[unclear: base of the block size, which is minus 1 divided by base size]] in integer operation in C. the [[unclear: number of flux]] that is needed for this. So let's say you... So let's say n bytes is exactly worth [[unclear: 4, 4 -Bit /s]]. So let's say the [[unclear: n -thite]] is 2 times base size. Then the number of blocks needed is 2. The base size minus 1 will just go away in integer operations, in division operations. Let's say you want to allocate [[unclear: one line]].

29:36 화자 2
There are many blocks to allocate. You plug in [[unclear: n twice to 1]]. Then it'll become a [[unclear: B -side]]. [[unclear: B -side]] divided by [[unclear: B -side]]. 1. So it makes sense. So let's say [[unclear: M by 37]], base size 16, and then you compute this 52 over 16. So [[unclear: 3 plus]]. Should be allocated. And then there is also [[unclear: internal frame ratio]]. [[unclear: So linked list of grid blocks.]] So you have [[unclear: a linked list of grid blocks]]. Then a [[unclear: mellow -caliber]] is [[unclear: picking up blocks]]. And then free has [[unclear: newly added block -to -blok list]].

30:29 화자 2
But again, this is just a general idea, but then K and R will [[unclear: position this fruit log in the order of address]]. It should traverse the right location in the list. And then plug it in. [[unclear: First allocation]]. or memory, find a free block that satisfies the request and as soon as you find the big-enough block, [[unclear: you have a key]]. That's what it's called. [[unclear: First key]]. You must have a size that is big enough or bigger. The simplest [[unclear: approach is first step]]. You want to [[unclear: learn the length of lesson]]. Stop upon encountering a big enough [[unclear: 3 -plot]].

31:25 화자 2
So here, if you want to allocate 64 bytes, then if you start from here, the first block that's big enough is 128 bytes. So you stop there. So let's say [[unclear: Mel gas]] [[unclear: for 1 to 8 flights]]. And then [[unclear: 3 block]] seconds to [[unclear: have 1 to 8 flights]]. Then it can be a perfect or best fit. simply remove the free block and return it to the user. But then, what if the request size is smaller than the free block? So, malloc has 64 bytes, but then you bump into 128 bytes. Then, you split the free block.

32:18 화자 2
And then so the [[unclear: leftover 64 bytes is still maintained inside the return in 64 bytes]]. And then, K&R uses circular linked list [[unclear: for free plots]]. So the benefits of making [[unclear: a free plot]], a circular list, is that any element in the list can be the beginning. So there's actually no end or tail. So you don't have to maintain the end of the list as special. Performance optimization. Make the head be where the last block was found. So last malloc call, stop at this block. Then the next malloc will start from that block.

33:16 화자 2
So then it's more likely to find big enough blocks later in the list because you have skipped all these smaller blocks before. Of course, it [[unclear: depends on the class]]. This is just a question. This is just a heuristic. What if there is [[unclear: no lock that fits]] the request? Then you need to traverse the entire list. So you need to know where you start. And then if you haven't found any block, even if you traverse the entire list, then you need to allocate more. You need to ask for the [[unclear: memory from the block]].

34:13 화자 2
Free blocks maintain free blocks in order of their addresses. Keep list in order of increasing addresses, make it easier to coalesce or merge adjacent neighbor free blocks. Though makes cost free more expensive, But then, yeah, so keeping the free block solid in a list, that's done, right? That's [[unclear: all end time]]. [[unclear: That's why it's called free]] You need to insert the [[unclear: new link, you will be able to lock it]] in the right place. So that is the high level ideas. And we'll talk about implementation soon.

35:10 화자 2
So the summary here, there is data that is allocated while the program is running [[unclear: is called.]]

35:16 화자 1
Thank you.

35:18 화자 2
Size does not have to be specified [[unclear: at the time]]. Dynamically allocated memory blocks are allocated on the heap. And dynamically allocated memory that is no longer used must be free. manually. But then in Python, you don't do that. [[unclear: Python automatically does that]]. So that's good in terms of memory management.

35:43 화자 1
Right.

35:44 화자 2
And correctness, but then [[unclear: of course it's slow]]. Dynamic memory allocator, three core functions we learned, malloc, realloc, and free. There's also calloc, right? [[unclear: initialize the energy memory]] to zero before return. [[unclear: Goals here are three things.]] B, as fast as possible. [[unclear: Take utilization]]. Waste as little memory as possible. The [[unclear: goals are conflicting due to the nature of the course]]. [[unclear: You can satisfy three things. One, do anything. Or maybe even meld them.]] I'm not sure. You can make the information very slow. It's always called ask for memory from operating system. But then that will waste.

36:48 화자 2
Fragmentation, internal fragmentation, internal fragmentation. [[unclear: Amuse the memory]], inside allocate the memory. Allocate the blocks. That's called... external fragment is caused by [[unclear: non -insectically located fragment]]. It's difficult to quantify because it depends on the request. That's the [[unclear: net -out]] with the K&R allocator overview. Let's move on.

37:20 화자 1
Thank you. Okay.

37:39 화자 2
Yes? Question?

37:58 화자 1
[[unclear: How do you find appropriate for.]]

38:16 화자 2
So each free block is just a [[unclear: memory chocolate]]. So the starting address, we have starting address and end address. So it's sorted by starting address. It's a block. It's basically a memory space. So you have a starting memory address and end memory address. So the free blocks are sorted by their starting memory. So you know a linked list, right? So you can plug in the order of the linked list, right? It's determined by your starting address of the free block. Yes, so you can check [[unclear: if T is your memory price]].

39:12 화자 2
Yes, if the list is This is really big. It takes a long time. Yes, yes, of course. So [[unclear: if you hang out]], you learn, you know, very simple. Actually, [[unclear: 20 lighters per week]]. Amazing. But then, it's slow. malloc is slow, [[unclear: Free's log]] is slow. [[unclear: That log needs to find it]]. So, [[unclear: the trap is different]]. Free is also slow because of the sorting. He needs to do better. That's what we'll talk about. Very good, very good. Details. The problem here. So we need information about each free block to maintain a free block. So to maintain a list, you need to have a pointer, right?

40:12 화자 2
Where do you store this pointer? Of course, each free block has a starting address. And also, [[unclear: length. of the free plan.]] How big is it? So by just storing the address, you cannot know how big it is. But the [[unclear: member plan size is big]]. And of course you have a [[unclear: pointer in the next line]]. Where should this information be stored? So if you think of a [[unclear: number of influx]], it's fluctuating. It's changing all the time. It's not known in advance. So you need to store the same information on the heap. But then we are including heap. [[unclear: We don't have a heap yet]]. So this code is what manages heap. And call, [[unclear: you cannot call map]].

41:11 화자 2
[[unclear: to allocate the beta data]]. Great. Any idea? I think this is a cool idea. The solution here is that, yes, [[unclear: totally information directly to the memory]]. Okay. So since the memory isn't being used for anything anyway, and the [[unclear: loss data source]] to grow and shrink as needed. So one idea is that you allocate the [[unclear: maximum amount of creeps]] by somewhere. So you allocate the metadata. that can satisfy the [[unclear: maximum amount of frequency]]. But then, it could be a waste, right? If the memory is not that big, then you waste a lot of memory for memory. Of course, you can, you can, you can grow it, right?

42:10 화자 2
But that's another idea. But then here, Typical implement, typical malloc implement you use this one. You have this metadata information inside the free block itself. How? So you have free block, right? And then you have some reserved area that is not returned to the application. You use this area for maintenance. And then [[unclear: return the next byte address]]. Here So how to implement this? So one simple idea. There's a [[unclear: store method]]. It's called implicit free list. So what kind of information do you need to store? [[unclear: Size of information.]]

43:07 화자 2
And also you need to have information about whether this block memory space is being used or not. So you have to have [[unclear: on -bit information]] whether this block is allocated or free. And then, maybe that's it. So you have a special location header, and then when you call malloc, you return this pointer to the user. That's why when you overwrite a memory, [[unclear: you will not get the rest]]. Because you overwrite data -structured data. But even before the memory you have this key, you have some location. So even if you write there, [[unclear: at that point it doesn't crash]].

44:08 화자 2
It's very simple, but if you think about it, it's very inefficient. So here, let's say the [[unclear: white one is an elongated gray one]]. But there's [[unclear: no point in having one]]. So this is a conceptual thing, right? So you go to the header side, okay, this is five blocks. One, two, three, four, five, and then you can... this guy is allocated. So let's say you want to allocate six blocks. Then you start from here, and then, okay, this is too small. You go here, oh, this is the allocated one. You go here, oh, this is the bigger one.

44:51 화자 2
[[unclear: When the mainboard is mostly free design]] but when is worst case when the memory is mostly allocated you go to a lot of blocks it's not not just only the you're not traversing only the free class you're traversing entirely and in memory regardless of whether being uh this is uh this is allocated or not that's it's worse than K&R. K&R has a pointer. Every free block has a header. It contains a pointer to the next free block. [[unclear: So you can't skip the allocator block.]] And then [[unclear: you have a sense]]. Of course, there's [[unclear: one more bit with the allocator on that]]. That's missing. I'm sorry.

45:53 화자 2
Okay, so K and R is a free block list of circular things. Free blocks linked together, it's also circular. And then take the list in order of increasing addresses. Why do you [[unclear: keep them so unified in address]]? Because when you free it, you can check whether you can merge with your neighbor. It makes it easier to [[unclear: call it JSON free class]].

46:43 화자 2
So the malloc, you start at the beginning of the list, sequence through the list, give a pointer to the previous element, and stop when reaching the first [[unclear: block that is beginning]]. and patch up the list and then return a pointer to the user. [[unclear: Next time the embed log is called]], you search first from the previous one. So here you start from this beginning, and then this is not big enough, so you move and you keep the previous pointer. So you have done this right for a list and for the data. And then, oh, this is not big enough also. And then you found the block this way. Then if you allocate [[unclear: this guy using his previous pointer]], you can patch this pointer to this guy.

47:45 화자 2
Suppose the [[unclear: first bit]] is a [[unclear: perfect bit]]. So you return the entire block. [[unclear: Remember the block from the list]] and link the [[unclear: previous print block]] with the [[unclear: next print block]]. Return the current to the user. So I think, so I said there is one bit here, but that's not. So here, if you have, if you're in the free list, all of them are free. If you're allocated, that's allocated. So you don't need to keep this one bit information here. But [[unclear: keeping them is actually useful and useful]]. Now, second case, what if you allocate from a block that's larger, much larger than the request?

48:43 화자 2
Suppose the block is bigger than the request. Divide the free block into two blocks, and keep the first block in the free list, and allocate the second block to the user. Why do you allocate the second block, not the first block? You don't have to [[unclear: change this function]]. The bonus here is no need to manipulate this. Okay, that's it. Very simple. That's how malloc works. So, again, because next time the search starts from the previous pointer, [[unclear: this is the first bit]], but then also sometimes [[unclear: people say next bit]], because it starts, starting the position is where it left off.

49:40 화자 2
It doesn't start from the, so there is no real true head here, just a second. [[unclear: Next step, and worst step]], the performance assessment. Let's talk about free. User passes a pointer to the [[unclear: memory card]]. And then, free's [[unclear: parameter type is what? Point.]] Because it just accepts a memory version. Free doesn't assume any [[unclear: type of display]]. That's not a big thing. It only thinks it comes to memory type. [[unclear: Free function is just blocking to the list]], identifying the start of the entry, and finding the location in the free list.

50:39 화자 2
[[unclear: green blocks are solidified there]] and add to the list and [[unclear: call this and trace it there]]. That's it. So [[unclear: finding location tensor]]. Then, to maintain the [[unclear: three blocks sorted]] by the address, you need to have actually the first row, the smallest, with the [[unclear: smallest letters]]. You sequence through the list and stop at the last entry before the [[unclear: 2B3]]. Here, you start from here. And then, This is a free block, and this is a free block. And then, this is the address. So you compare this guy and this guy.

51:36 화자 2
And then, you now know the right position. Okay, [[unclear: after this guy]].

51:43 화자 1
- Yeah.

51:43 화자 2
I can be.

51:44 화자 1
Position.

51:49 화자 2
Also, there are [[unclear: two chronic cases]]. Check for the wraparound in memory. The [[unclear: block has been tricked]]. Also, it can be an [[unclear: active velocity]]. The two are quantities. How do we insert the free block to the free list? You are going to add to the free list. Insert in between previous and next entries. Then you traverse it and you have to keep a pointer of the previous guy. And then you change pointer. This pointer to point to this guy and [[unclear: this guy should point to.]] You can do this.

52:47 화자 2
So you need to update the [[unclear: pin's pointer first]]. Because otherwise, if you update [[unclear: p next to first]], you cannot update it's pointer.

52:59 화자 1
Thanks.

53:05 화자 2
When scanning, the list finds the location for inserting. The pointer to to be free element is [[unclear: VP]], and the pointer to [[unclear: prim's element]] in the free list.

53:20 화자 1
[[unclear: It's a few months.]]

53:21 화자 2
And coalescing into [[unclear: larger frequencies]]. So if you want to free this guy, and it happens that this guy is neighbor contiguous with the upper free block and the lower free block, very lucky case, then you can merge them all. How do you do that? So you look at the upper side first here, check if the next part of the memory is [[unclear: in the full list]]. If so, make it into one larger one, one bigger one. So this is BP, and then next time, this is the [[unclear: starting point that P is next]].

54:06 화자 1
Okay.

54:08 화자 2
Then you merge it into 1, and then you [[unclear: make this guy 0 .2 BP]]. Of course, BP size should be increased. That's it. Like this. But then here, you have another version. P and the next guy can be merged together. So here, check if our previous part of memory is in the free list, and if so, [[unclear: make it to 1D]]. So you look at the right side, the upper side, or the lower side of this one. And then you can make them all [[unclear: one big challenge]].

54:47 화자 1
Thank you.

54:50 화자 2
But that's it. Strength of a K&R approach. The advantage is it's simplistic. Very simple. And the optimization to malloc is that you're splitting your large free block to your [[unclear: only factor choice]]. And the [[unclear: optimization to free is that your roving free list pointer]] is less at the last place the block was allocated to next to it. So let's find the moving pointer. I'll just start from the last block to check this again. And then, Coalescing. Coalescing continuous free blocks to [[unclear: reduce drug use]]. What's the reason that the free block list is [[unclear: solidified at this point]] in the K &R implementation?

55:45 화자 2
Because they can do coalescing. Otherwise, it's difficult. But then of course, we can use it. So inefficient use of memory. [[unclear: First -aid policy]] can leave lots of [[unclear: holes of 3 in the data]]. So best fit is good, but then best fit is critical slow. But then you can sort of find the [[unclear: highway to promote]]. In the long execution time, both of them suffer from [[unclear: O and O N]] is the number of [[unclear: read blocks in the list]].

56:44 화자 2
So [[unclear: both operations work in O]] Now let's [[unclear: scan the read list]] to [[unclear: find read block]]. [[unclear: 3 scans the read list]] to find where to insert block. Accessing a wide range of memory versus [[unclear: in read list]]. Then there's memory pressure. Sometimes memory is not really in the physical memory. It can be swapped out to disk. And then it's free, logically free, but it's swapped out. Then when you traverse it, you need to read it again from the disk just to see that Oh, this is not big enough This happens. So it can lead to [[unclear: large amount of pain from the disk]].

57:43 화자 2
Then if your system is in this state, it's [[unclear: virtually immutable. Very small.]] What's worse is that even like [[unclear: code signals, instructions are softened]]. So next instruction that you need to read from this, then it is forever. So that means that [[unclear: your memory is twofold]]. Okay, so now we'll talk about [[unclear: assignment of reframe]]. Optimization. We all are going to implement the same data optimization to [[unclear: both frame and melody]]. So how do you implement [[unclear: faster frame]]?

58:36 화자 2
[[unclear: Format problems]] are scanning the free list to know where to insert, keeping track of the previous node to do the insertion. So instead of having a [[unclear: single NL]], let's think about a [[unclear: double NL]]. And then the [[unclear: problem with three]] is what? The key problem is that the [[unclear: three block list]] is sorted. So inserting and then inserting is So instead, let's think about another idea. You have a [[unclear: hatch header]], and these two blocks are both [[unclear: meta -hacking]]. They cannot be used by the user. This [[unclear: header has a size of 1]].

59:36 화자 2
in terms of unit number of blocks. And then whether this block is free or not free, or if it's so allocated or not allocated. That would be the information there. If it's free, then it has pointed to the next one. And then you have footer, and then you have the [[unclear: same sizing coefficient]]. size of the block, again, in terms of number of units. And then [[unclear: in this tree]], it has pointed to the [[unclear: previous tree]]. So it's a doubly linked list. So what's the benefits of doubly linked lists over single linked lists in terms of list operations?

01:00:47 화자 2
You can avoid traversing. Let's say you have one block. If you have two pointers, then you can remove it from the list without keeping another pointer to another of them. Because you have a [[unclear: previous plug and next plug going to two]]. So you can actually remove this guy from the list, and then you can patch up the pointers. Of course, you need to spend one more pointer. That's overhead. Why do you want to have the size in footer? Size is kind of redundant.

01:01:46 화자 2
You have header, the [[unclear: size of header, and size of the footer]]. Why? So here, free, okay, even in best of free, we still want to [[unclear: do policy]]. In order to [[unclear: do policy]], all it had required, right, [[unclear: he blocks the solid by reverses]]. So we want to get rid of this real quick. And then we want, what, [[unclear: all one time for free and policy]]. Then if you have a footer, so if you have a header, a sizing header, you can go to the upper side, right?

01:02:39 화자 2
because you skip this amount and then you see the block structure and see whether that guy is being used or not. If it's free, you can merge it. So the upper side is easier. But what about the lower side? In order to go to the lower side, if every block has footer, if you know exactly the footer size, you can [[unclear: go to the footer size]], footer metadata, and check the size. Then you can go to the start of the previous one and check whether this guy is free or not. [[unclear: If it's free, it can work.]] Okay, so all this thing just happens. happens with just point operation. It all connected. Fix the amount of instructions. [[unclear: All one time.]] Do you understand? So here, find the next block. Go quickly to the next block, you can restart, and [[unclear: the users are data portion of the...]]

01:03:37 화자 2
So, [[unclear: three will give you the user feature]]. Then, using this pointer, you can go to the header. You know the size of it. Then you can [[unclear: type test it]]. Then you can find the address of the header. And then you can read out how many units this guy is using. Then using this size, you can go forward to the head of the next block, because you know the size of my block, so you can go to the header of the next, [[unclear: the G -SIM]]. Then you can check whether that guy is being used or not. If it's free, [[unclear: you can purchase it]]. Another thing that's really good with footer is that you can go to the previous neighboring one.

01:04:38 화자 2
So you go backwards to the head of one, and then from this point you can actually go to the start of the footer one. Then [[unclear: inside the footer you can read the site]]. Then you can go to the head of the previous neighboring one. And you can also check whether this guy is being used or not. If it's free, you can merge it. All these operations are just fixed. It doesn't depending on the [[unclear: number of green plus signals]]. So it's [[unclear: all one time]]. It's this one. This is [[unclear: full time]], right? Still you need to keep the free block list.

01:05:36 화자 2
So you go to the free block, start with the [[unclear: user's version of the block]], and you can go to the header block. The [[unclear: header of the block has the next free block]]. This free block may not be continuous. Then you go to the [[unclear: next three block]]. And then you go to the next... Why do you need this? Next and [[unclear: previous three block]]? Why do you need this?

01:06:23 화자 1
I've said it.

01:06:24 화자 2
Yes. [[unclear: Without this, you cannot allocate anything.]] If you have a free block list, you don't have a list, right? How do you find the block? OK. [[unclear: Previous guide, footer. Header]], they're needed. They can... This is really [[unclear: great for forest]]. But then, yeah, that's good for free. But you also need to implement malloc too. malloc should traverse. That's why we need this free block pointer. Previous free block pointer, next free block.

01:07:06 화자 1
Okay.

01:07:12 화자 2
Before you scan, [[unclear: you cannot scan the free list until you find the place you can scan]] because [[unclear: lots of articles are written by members]]. You need to see if [[unclear: you can pull this]]. Expensively looked with several pointer or looked with us in several pointer comparisons.

01:07:43 화자 1
Because, yeah.

01:07:45 화자 2
After with [[unclear: header filter]] and double -link list, coalescing with the previous blocking memory becomes very efficient. To check if [[unclear: previous blocking memory is altered,]]

01:07:56 화자 1
Thank you.

01:07:56 화자 2
That would be [[unclear: next to neighbors]].

01:08:00 화자 1
Great. It's all important.

01:08:07 화자 2
Then, here again, then where do you place this newly freed block in the [[unclear: free test]]?

01:08:16 화자 1
Thank you.

01:08:17 화자 2
Now the [[unclear: free list is no longer stored]]. Then you can just put it.

01:08:23 화자 1
Anyway.

01:08:26 화자 2
Here, larger block is inserted to the [[unclear: front of the system]]. That's it. It's [[unclear: no longer serving]]. Are you following me? Are you sure? Any questions about this?

01:08:42 화자 1
Okay.

01:08:46 화자 2
But [[unclear: value is still slow]] if you still maintain a list. Finding the [[unclear: first three whatever]] takes in worst case, a long time. [[unclear: Even in the average case, a long time.]]

01:09:01 화자 1
Okay.

01:09:03 화자 2
So it is kind of realist so to find the [[unclear: first best like a bluffing]] is Whatever it takes The problem is that the free blocks have, each block size are all different. The free blocks have a wide range of sizes. So instead, let's have multiple lists instead of single lists. And then each list has its own size. It's called binning. So what you need is a binning, or [[unclear: single -weighted free list]]. You separate free lists by block size. And implementation is kind of already. So this is one block and two block size. One unit size, two unit size, three unit size, four unit size. Because typically [[unclear: smaller amounts of bandwidth allocated for frequency]]. So you connect them into them.

01:10:00 화자 2
If the [[unclear: request patterns truly lend them]], you can unlink them. It degenerates to the actual link list. If request pattern, request size is popular, the smaller amount is more popular, and you can compare them. So, have a [[unclear: bin for each process]], up to a limit. Beyond the limit, you can degenerate to a [[unclear: single limit]]. [[unclear: have a main for each block size]] to limit and the advantage is [[unclear: no search for Poisson]] to this. Go ahead and [[unclear: pick Poisson]]. It's the metadata, you have metadata. And storing, it's storing. So you have, you need to spend more metadata.

01:10:58 화자 2
[[unclear: Except for a final thing]], for all [[unclear: larger grid blocks]], we're allocating larger amounts of memory, we're splitting to create smaller ones. So, I think it's larger than 4 here. And then it gives you, oh okay, [[unclear: like 4]]. What block is left over? We can plug it in. Okay? Another idea is that you can have range. Then of course you need to do the search, but then the search time is limited. Or [[unclear: two units or four units]]. Or you can combine them both. First a few blocks, right, fixed size. And then next few blocks, range, [[unclear: by the one]], right.

01:11:59 화자 2
[[unclear: anything that's minor]]. So that's how they have [[unclear: high freedom]]. So again, shift. Okay, that's it. So you implement this, [[unclear: faster free, faster free plus faster free one]]. and the [[unclear: fencer is the next sub element]]. This is what should be measured. The [[unclear: Hogan -Mainfield measurement code]] is Well, you could. I stopped on headers and footers. If the [[unclear: benefit itself is wrong]], everything is wrong. So be very careful. Making it very hard to understand where you are.

01:12:59 화자 2
So just in, debug carefully as you go along. Write a little bit of code and test it. And if the test goes, pass it, then you go to test it. and assertion checks [[unclear: assert they were literally used assertion checks]] You know assert, right? So it evaluates the expression assert if it's false, it stops it. So you typically have invariant here. Oh, here the [[unclear: point is not the same]]. And then if that condition fails, assert, your program stops at that point. And then it prints out the line. and then you can go there and see what's happening.

01:13:59 화자 2
Use functions to apply [[unclear: payload checks]] on your list. [[unclear: All three list blocks]] are marked as free. And then each block pointer is within the heap range. And each block size is in header, each block size is in [[unclear: header and foot should]] be identical or they should be the same. So there are many invariants in the heap. If something's off, right, you can [[unclear: use a string]]. And then don't write the entire thing and then try to test the entire thing [[unclear: once the data work well]]. Unless you are more experienced. Show lots and lots of pictures, okay? That's a nice suggestion. Okay, any questions so far?

01:14:50 화자 2
So [[unclear: more than Linux, MeloInfo]], and this is the first one, actually it has all the things that we learned. So they stay away from the kernel. They [[unclear: used to use Tera]], I think. Then they stay away, and then they [[unclear: become the make list]]. [[unclear: free all one time in the beginning]]. And then they also implement a [[unclear: private support thread]]. We have a run thread, but we assume that the key... [[unclear: We are focusing on the implementations that's using]] So you're moving this line and then you allocate and de -allocate. But then what if you have multiple threads?

01:15:47 화자 2
Multiple threads means that all the threads are, they may belong to the same process, same program. But then they share the memory space. But then they have a separate function to execute in. So typically a thread, a new thread, starts with this new function. And then the main thread and the child thread work together. They run concurrently, truly concurrently if you have multiple cores. But then if you have single core, and they do [[unclear: context -rich]]. Anyway, what's important about threads is that they share the memory space with you. So what do you mean by sharing the memory space? If you update one global variable by one thread, that's [[unclear: beatable to another thread]].

01:16:46 화자 2
If you're in a separate process, if you update one variable here, that's [[unclear: not beatable to another thread]] because you're independent. But all threads belong to one process. You share this [[unclear: labor space]] together. Then there is the issue of how do I [[unclear: implement the network]]? Because there is one single point of break. So that kind of issues are addressed in real implementation. Yeah, I think it's the [[unclear: only main threat is using break]]. Others are using another space. That's one thing. Another thing that we didn't learn is that we're kind of focusing on small request size. But what if the request size is larger?

01:17:45 화자 2
Then [[unclear: break is not very efficient]]. So then they actually allocate the memory using mmap. So we saw that, right? They allocate a heap using sbrk for brk. Or mmap, memory map. The MMAP, the name is very weird, but basic operation is to allocate the memory, but you also can tag the entry. Oh, this is a [[unclear: read -on]], this is a read -write, can be shareable, that kind of thing you can give. The [[unclear: MMAP itself is a system code]]. [[unclear: malloc itself is not a system code]]. [[unclear: malloc can use a system code]]. The [[unclear: MMAP is a system code]].

01:18:34 화자 2
So if the [[unclear: core size]] is much larger, I think, then a malloc [[unclear: internally used instead of a brk]]. Then it allocates memory [[unclear: separate from brk components]].

01:18:53 화자 1
Hello?

01:18:55 화자 2
Another thing to note is that, how does the OS allocate memory? We talked about user -level memory. You have a wholesaler, a malloc is a wholesaler. You get a big chunk of memory from OS and then you manage it. to provide memory to the application. But OS, does OS maintains the memory management like this? The answer is no. [[unclear: OS is much kind of easier]]. But more, I'm not sure it's easier. So we learn a virtual, we also learn page, virtual memory page. So inside OS, it allocates in the unit of [[unclear: page to page]]. So even if you allocate in the type of a [[unclear: four -kilometer]],

01:19:55 화자 1
Thank you.

01:19:56 화자 2
[[unclear: So he's beating his people.]]

01:19:58 화자 1
Oh.

01:20:00 화자 2
Think about it, sbrk, using sbrk [[unclear: for ready grade]], you can actually allocate just [[unclear: one byte, exact one byte from the training system]]. Because the increment is just the number of bytes. But even in that case, always allocate [[unclear: entire port number]]. So here again, very interesting. If you allocate one byte using sbrk, this is the goal. And then you access. and then [[unclear: this fight right to him. That's the fight.]] But yeah, logically wrong. But granularity of the memory allocation, memory measurement is And then [[unclear: actual allocation of the physical memory happens when you access it, first access it]].

01:20:57 화자 2
We learned that later when we talked about [[unclear: extensions]].

01:21:03 화자 1
Thank you.

01:21:08 화자 2
These are not directly related to [[unclear: the American Free]], but the [[unclear: member related corporations]]. So many different kinds, [[unclear: all these books are classified]] combination of not properly understanding memory system, stack, and memory allocation, and /or not correctly mastering the C. I think if you learn C and then you study, pick it up properly, you know most of them. So let's look at this. So, the [[unclear: reference is backwards]]. [[unclear: Classic scan bar, scan bar.]] [[unclear: Intel and scan bar]].

01:21:56 화자 1
Thank you.

01:21:57 화자 2
[[unclear: It compiles, right?]] But when it runs, [[unclear: it may-- so what kind of--]]

01:22:03 화자 1
Thank you.

01:22:05 화자 2
What kind of error do you see when you run this? OK, let's say, let's [[unclear: change int to int pointer]]. Then what happens? So just change, let's say, let's say the one character to this code. [[unclear: int star]]. It's OK.

01:22:44 화자 1
Thank you. Thank you.

01:22:49 화자 2
Yes, [[unclear: it has just done]]... Okay, so that's [[unclear: not the tell the memory location]]. Then what?

01:23:04 화자 1
Thank you.

01:23:05 화자 2
What patterns you see when you run it.

01:23:13 화자 1
- [[unclear: Sector.]]

01:23:16 화자 2
[[unclear: Access the file always hates them.]] I didn't get this memory. Do you want to access it? I'm all for it. It's likely that Bell, when you do this, [[unclear: Bell has a random]] [[unclear: That is not zero. That is random.]] And then scanf will try to write to the random location. That's probably not allocated. Then OS will catch it. So [[unclear: OS, the version address takes place]] and then it goes to the location that's not allocated. Because you go to the page table and oh, it's not allocated.

01:24:02 화자 1
Thanks.

01:24:03 화자 2
So how do I fix this?

01:24:05 화자 1
Thank you.

01:24:10 화자 2
How do you fix it? You know. What do you have? [[unclear: Emperors]]. So you [[unclear: add emperors before power]]. Okay, next. Assuming that [[unclear: heat the resolutions]]. So here you allocate n integers to y. and what do you do? A. So we compute y where A times x. A is matrix.

01:24:46 화자 1
Okay.

01:24:48 화자 2
Then you do this. As you can see,

01:24:52 화자 1
I don't know.

01:24:54 화자 2
So [[unclear: A is top of the LQ]].

01:24:55 화자 1
Thank you.

01:24:56 화자 2
Does it crash? [[unclear: It doesn't crash.]] Then what is the problem?

01:25:05 화자 1
Thank you.

01:25:06 화자 2
The [[unclear: answer is a book]].

01:25:12 화자 1
Thank you.

01:25:14 화자 2
How do you fix it? What is the problem? How can you fix it? How? So which value do you need to use? Zero. [[unclear: Why is your feature secure?]] Then you [[unclear: add up with actual amount of data]].

01:25:42 화자 1
Good.

01:25:43 화자 2
Another thing, what's the problem? Do you [[unclear: allocate n integers]]?

01:25:49 화자 1
Thank you.

01:25:50 화자 2
And then, [[unclear: PI.]]

01:25:54 화자 1
Thank you.

01:26:01 화자 2
So when you [[unclear: run this as a crash]], Thank you.

01:26:12 화자 1
Oh.

01:26:14 화자 2
Ready? [[unclear: Fresh hand up.]]

01:26:20 화자 1
Amen.

01:26:36 화자 2
[[unclear: Why does it crunch?]]

01:26:45 화자 1
I don't know.

01:26:53 화자 2
So how do you fix it?

01:27:05 화자 1
Okay.

01:27:12 화자 2
Integer pointer. So yeah, so you allocate integer pointers. Because [[unclear: each pi is]] So this guy [[unclear: will crash all the time]]. Are you sure? So it [[unclear: crashes on x86 64]]. But it [[unclear: does not crash on--]]

01:27:46 화자 1
Thank you.

01:27:49 화자 2
We don't use that. Why? Because in 32 -bit machine, the [[unclear: pointer size is 4 points]]. So [[unclear: it should actually in int and int pointer sizes]].

01:28:05 화자 1
Okay.

01:28:07 화자 2
[[unclear: So it doesn't crash. It didn't crash before.]] Then when you migrate, say, a program to [[unclear: IA, say, 64]], then it crashes. I brought this-- oh, I talked about this in class. This is important.

01:28:28 화자 1
So...

01:28:36 화자 2
You read [[unclear: 1, 2, 3, 4, 5, 6, 7, 8, 9]] from standard. And does it crush you? Do you know gets So you should do the [[unclear: f to get]] not gets [[unclear: gets reads one line from standard game]]. But then it has not specified the maximum size. So then it just overwrites whatever it could specify. So you allocate 8 bytes.

01:29:20 화자 1
Okay.

01:29:20 화자 2
Yes, this is an array of size 8 bytes. But then what if [[unclear: 9 bytes come in]]?

01:29:25 화자 1
Thank you.

01:29:26 화자 2
Then it will overwrite. So it may not work.

01:29:32 화자 1
Thank you.

01:29:33 화자 2
Because of reason that we talked about, right? So [[unclear: it has purpose]]. It would take some time. So it [[unclear: may not crash, or it can crash]], but logically wrong.

01:29:44 화자 1
Thank you.

01:29:45 화자 2
[[unclear: If input is big enough, it must crash.]] But if input is small enough, then it may [[unclear: overwrite some valid location]].

01:29:55 화자 1
Okay.

01:29:56 화자 2
Well again, that's very bad, so don't use that. This is the basis for classic [[unclear: vocal overflow attacks]]. In 1988, [[unclear: an internal war]] happened. Interestingly, [[unclear: this war was written by Then]], He saw this problem and then he knocked out [[unclear: almost all the machines in the world]]. At that time, the number of [[unclear: commanding machines had not been made]].

01:30:38 화자 1
Okay.

01:30:42 화자 2
So it's probably a multiple problem. And then the interesting thing is that this person later [[unclear: became a professor at MIT]]. He's very famous in my area. Anyway, and he served-- [[unclear: public service]]. Anyway, that's it. [[unclear: Mono attacks on web servers]], [[unclear: AOL, Microsoft had a big war over instant messaging]] and then they did actually attack on their counterpart using this.

01:31:31 화자 1
Thank you.

01:31:32 화자 2
[[unclear: Then the right, then the whole floor.]]

01:31:35 화자 1
Thank you.

01:31:35 화자 2
So what about this? Okay. You search. So you now, the intention here is that you [[unclear: paste an array]] and you want to find [[unclear: the bell in the array]].

01:31:53 화자 1
Okay.

01:31:56 화자 2
What's the problem? Yes, so [[unclear: P is insert]]. So if you iterate over integer element, you need to [[unclear: increment p sub i by 1]].

01:32:26 화자 1
Or...

01:32:29 화자 2
You can [[unclear: type test P as character pointer]].

01:32:33 화자 1
This is my...

01:32:34 화자 2
But that's not very good. It's very difficult to read, frankly. So the [[unclear: correct fix is that p plus p]].

01:32:43 화자 1
Thank you.

01:32:45 화자 2
What about this?

01:32:46 화자 1
Thank you.

01:32:48 화자 2
[[unclear: Bin hit delete. Not bin hit delete. Hit delete.]] So bin hit is an array, right? And then we have size. So you delete the roots, right? You know hit, there's a friend. So you delete hit. Then what you do? So you go to the last.

01:33:19 화자 1
Elements.

01:33:20 화자 2
And then you put that into the roots, and then you do So the [[unclear: algorithm itself doesn't]] but then what's wrong here?

01:33:32 화자 1
Thank you.

01:33:38 화자 2
Yes, the [[unclear: unit can what?]] Parentheses.

01:33:42 화자 1
Okay.

01:33:44 화자 2
[[unclear: Minus a decrement operator as high of message than pointed reference]]. What about this? Okay.

01:34:01 화자 1
Thank you.

01:34:05 화자 2
So when you execute [[unclear: FOOL]], does it crash?

01:34:10 화자 1
Thank you. Thank you.

01:34:21 화자 2
[[unclear: Step A, we have a goal line.]]

01:34:22 화자 1
- No. thank you.

01:34:29 화자 2
Yes, but the [[unclear: stack memory itself is all still out of key]].

01:34:35 화자 1
Thank you.

01:34:37 화자 2
Thank you.

01:34:38 화자 1
Thank you.

01:34:43 화자 2
When you execute [[unclear: frue]], [[unclear: does it crash? It doesn't.]] You just calculate the memory address and then return the memory address. [[unclear: You do not access it. You read the memory content there or write memory content there.]] But then, yeah, this is a temporary location and that may be overwritten by another function. So using this address to access later is also wrong. What about this? So you [[unclear: allocate indicators]] and then you move to x and then [[unclear: 3x]]. Then you allocate y. Then you free. You should free y instead of x. Why does it happen?

01:35:42 화자 2
Copy and paste. Copy and paste and you forgot to fix this. [[unclear: Still works. But you lose. You take it.]] What about this? You allocate n integer and then free x. And then you're going to fade it, but then [[unclear: you try to use it. That's fine.]] What about this? And we allocate [[unclear: n to the game, never 3]]. So maybe we'll leave it like that.

01:36:20 화자 1
Thank you.

01:36:22 화자 2
- Is it? - What is this?

01:36:28 화자 1
Thank you.

01:36:34 화자 2
So, head is a structure, it has two fields, and one of the fields is a pointer. So [[unclear: head itself is allocated, but then also head's next is allocated. But then you allocate only one.]] It's a typical mistake by a novice. It looks very nice if you see the [[unclear: spine and the automatic heel working]]. But then that's also... maybe that's not the intention. Sometimes this [[unclear: head next is shared by another pointer]] and they use it. Not necessarily wrong, but typically wrong. You forgot. Typically, you have this guy, [[unclear: Portuguese]]. So you need to [[unclear: allocate evidence to...]]

01:37:34 화자 1
- That's pretty cool.

01:37:36 화자 2
I think that's it. So, uh, [[unclear: critical corner]], so how to deal with memory bugs, GDB. Look for finding that pointer, uh, if you [[unclear: press hub]], detect other memory bugs. you can use malloc tracing, so whether it be malloc, memory is allocated to the [[unclear: virtual degree]], right? [[unclear: And trace, and non -trace]], [[unclear: memory is called valgrind]], separate from, very heavy, and it has [[unclear: many false positives]], so if you are developing very small, like maybe your assignment is fine, even GDB, so your current assignment is very small. in comparison to the real coding industry. [[unclear: Industry is not huge.]] It's industry code, or when you run valgrind, it shows many potential errors that are not really an issue. Yeah, but sometimes it's very useful.

01:38:36 화자 2
But then most times, you have an intuition, what went wrong? And then you use printf. [[unclear: Experience the code.]] GDB typically helps for obvious problems, like the problems that we saw so far. But then, difficult ones, you would have an intuition and then print them. They will [[unclear: project a flush]], print them with the standard error. Summary, Explicit [[unclear: free list of money]]. Comparison implicit list allocate in linear time in number of free blocks instead of all blocks. Slightly more complicated allocate in free since it needs to splice blocks in and out of the list. Some extra space for this.

01:39:36 화자 2
But then implicit list is not really that all the time. Maybe it's sometimes useful. When? When you have very small amount of memory, when your device is embedded device, very small amount of memory, you don't want to use [[unclear: 4 bytes of printer or 8 bytes of printer]]. [[unclear: Then time is not critical.]] Okay, this doesn't work. [[unclear: Heather and Kutcher for efficient holocene beaming]] maintain separate explicit free -list blocks of different size classes or objects. [[unclear: Blocks move between size classes when explicit free -list]]. The length is higher throughput than explicit free -list. [[unclear: Long -time core hollow -2 size classes]] And then a better memory is like [[unclear: first bit search]] of a [[unclear: single bit list]] approximates [[unclear: the best bit]].

01:40:37 화자 2
It approximates [[unclear: the best bit.]] [[unclear: It looks at a small,]] approximates [[unclear: the best bit search of the entire.]] Okay, so you can look at other references. That's it.
````
