---
title: "Control Hazards · 보정 STT · 날짜 미확인"
course: computer_architecture
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

수업 날짜는 미확인이다. 원음 없이 자료와 대조한 텍스트이며, 확정할 수 없는 표현은 `[[unclear: …]]`로 남겼다. 45:53 이후의 반복 발화는 실제 발언인지 확인되지 않았다.

````text
00:17 화자 1
Thank you for coming today, even though the weather is getting cold. I know it is hard for you to come to the lecture, but you come, so I appreciate it. Today's lecture is about the control hazard. Last week we discussed about the data hazard, right? Like data hazard is the situation that makes the processor cannot move, cannot execute the further instructions because of the dependency between data, between instructions of data. So that is data hazard and today we're going to learn about control hazard, which is a little bit different but the principle is the same. So, there are some notices, announcements that, which is homework number two, will be released today. So, our team will come today and he will introduce the homework number two.

01:18 화자 1
[[unclear: Until homework number two, for human, a pull method is a single cycle. I believe you have a pull method, a execution unit, the first method]], and in homework number two, you will to handle all kinds of [[unclear: extra -person]] RISC-V. And as I told you last week, [[unclear: this Thursday is the school anniversary]], [수강생 반응과 개인적 대화 비공개] So no class on Thursday. But although we missed a few classes, we are moving fast, which means that we are on schedule. So we will have some [[unclear: makeup classes around the end of the semester]].

02:18 화자 1
Then [[unclear: makeup classes will cover other topics like security]], like hardware security research or some others. And the midterm will cover up to lecture 8. And [[unclear: one or two problems will come from the problem number 1]]. The problems related to the homework number one is, it will be simple and easy if you implement it by yourself. If you ask AI to do everything [[unclear: on the Apple view]], then it might be difficult, but if you at least look at the source code, then it will be very easy. I believe. I hope so. And so let's move on to the lecture. So I'd like to show this is the control hazard.

03:17 화자 1
we discussed about the data hazard, data dependence. Data dependence, which is a read, after, write dependence, the last topic that we discussed, the topic that we learned last lecture. Anti -dependence and output dependence is related to [[unclear: algorithm or execution]], and we will learn about them later, after the midterm. So today we're gonna discuss about control dependence, which is a specific type of data dependence. So, control dependency is a kind of data dependency on program counter, which means that to know which is the next instruction is, you have to decode the current instruction and determine if it is a branch instruction or not.

04:08 화자 1
If it is a branch instruction, then you may move on to an instruction that is located somewhere in memory. But if the current instruction is not branch instruction-- if the current instruction is arithmetic operation or load word or store word operations, then the next instruction is located at [[unclear: frame count across pool]]. So to correctly know which is the next instruction, you have to decode the current instruction. So this is-- so if-- what did I say?

05:10 화자 1
So control dependence can be considered as a data dependence on the program counter. The program counter itself is a register. It stores the address of the current instruction. And the two instructions have a dependence on that address. The next instruction is determined And next instruction is determined based on the program counter, and the program counter is updated after the current instruction is correctly decoded. So there is a dependence on program counter. So it is a specific type of data dependence on the program counter. So if we follow the-- what's that?

05:57 화자 1
If we follow-- if we specify-- If we strictly follow the data hazard principle, we learned last week, that you can realize that every instruction would make a hazard. There is a typo. Anyway, that's different. Hazard occurs if and only if distance between two instructions is less than or equal to the distance between two stages. But if you look at this table, you can realize that the [[unclear: next -gen instruction]] is determined at least in instruction decoder stage or execution stage if the current instruction is a branch instruction.

06:46 화자 1
That means that for R/I type arithmetic operations or load -word operations, the program counter can be updated right after we decode the current instruction and we determine that it is R or load word or store word instructions. And we can update the program counter in execution stage if the current instruction is branch related instructions like branch or jump and link.

07:15 화자 2
Thank you.

07:15 화자 1
Jump and link register instructions. But we didn't do this, right? In previous data path and control path, we updated the program counter for [[unclear: instruction participation]]. So that is the kind of prediction as a spoiler. So that is the concept that we're going to learn today.

07:34 화자 2
Thank you.

07:36 화자 1
So, without thinking about the program counter update in the instruction fetch stage, let's think about the strict following the data hazard or stalling principle. As shown in this table, we can determine the next instruction in the instruction decoder state. That is the only state that we can know the next instruction. We can know the address of the next instruction. This is the view of how a process works if we do not do the prediction. In this example, there is an instruction H. H is just random arithmetic operation. And it comes to the processor at T0.

08:32 화자 1
And T0, instruction fetching state is fetching the instruction from fetching the instruction H. And T1, instruction I comes to the processor, but it does not know which one is the next instruction. And even if the instruction H is arithmetic operation, we do not know about it at the instruction fetching state. So we know that after instruction decoder state it is done for [[unclear: instruction eight]]. So at T1, it is impossible to correctly know which one is the next day instruction. So we cancel the instruction fetch stage for InstructionI at one, and at two, instruction fetch stage for InstructionI So this is the kind of-- stalling that we learned last week.

09:32 화자 1
It is-- there is a data hazard. So same thing happens for [[unclear: Instruction A]] and Instruction K and so on. So [[unclear: every cycle we cancel the instruction fetch stage]], right? It is just because the program counter is updated in the instruction state, the instruction decode state, and the result is the performance loss even for non -controlled flow instructions. So this is not ideal and we didn't do this in previous lectures. We updated the program counter in the instruction fetch stage.

10:10 화자 1
And that is called kind of a prediction, which means that Even if we don't know which one is the next instruction correctly, we predict that the next instruction is located at current counter plus 4. Even though we didn't talk about It is a prediction. The [[unclear: current current product]] might not be the next instruction for the current instruction, but we do this based on the prediction that the next instruction is [[unclear: located at the current product]]. So you can imagine that all the instructions are arithmetic operations and we keep updating the program counter in the instruction fetch stage.

11:04 화자 1
Then instruction i will start at t1 and instruction j starts at t2 and so on. So the performance is kind of doubled. But it is not the case in reality, because your program always have a control flow, which means that here, our control flow instruction is Control flow instructions include branch instructions or conditional branch instructions, like [[unclear: a branch instruction in useful or a template or a template]] These kind of things are control flow instructions. Here, this kind of prediction is very naive, which means that we always predict that the next instruction is located at [[unclear: current current post 4]]. How good is it? It depends on the combinations of instructions in your program.

12:05 화자 1
For example, [[unclear: if your program consists of a lot of control codes, then this prediction is always incorrect]], right? Then there will be a penalty for the incorrect prediction, but if your program consists of arithmetic operations a lot, like all instructions are arithmetic operations, then this prediction is always correct. That means that there is no penalty. So the purpose of the prediction depends on your program. And there was research in 1984, I'm pretty sure that [[unclear: all of you were not bored at that time. Even I was not bored.]] But [[unclear: these kind of things are device at the time]], like a very old legacy. Anyway, there were research done by, I don't know the names of the guys, but Lee and Smith in 1984.

13:03 화자 1
They profile programs, a lot of programs, and get the average number of instructions, I mean, get the average portion of control flow instructions in the program. According to their research, [[unclear: around 20 of instruction is control flow]], which means that if your program has 100 instructions, then around 20 instructions are control flow instructions, like a branch or function calls or returns, that kind of thing. And these two are not really important, but I'll just mention. Forward control flow is a kind of control flow that moves the program counter toward forward. You understand, right? If the control flow moves the program counter to address that appears later in a program, then it is called forward control flow.

14:02 화자 1
And if the program counter-- I mean, if control flow instruction make the program move backward, then it is called backward control flow. Like if loop-- in a loop-- Even though you don't see the control flow at the end of the loop instruction, you know that the program will move back to the start of the loop instruction, right? That is called the backward control flow. According to the research, [[unclear: around 50 of forward control flow is taken, and around 90 of backward control flow is taken]]. Although this slide does not mention about a portion of forward control flow and backward control flow, [[unclear: overall, typically 70 of control flow instructions are taken, and around 30 of control flow instructions are not taken]].

14:56 화자 1
do the math to get the accuracy of this naive branch prediction. This is very simple mathematics. So if we expect that next program counter is [[unclear: current program counter plus then]] the accuracy will be around 86 because for 80 of instructions, the prediction is always correct because For 80 of instructions, [[unclear: the primary is always the next instruction]]. And for the 20 of instruction, not taken means that the prediction is correct. And taken means that the prediction is incorrect. We can do the math. [[unclear: 0 .2 times 0 .6 is a correct prediction for control flow instructions]].

15:54 화자 1
So we can get the number. It's [[unclear: 8 plus 6]]. So 86 of instructions are correct prediction given these combinations of instructions. So for the [[unclear: remaining 8 ,000, what, 40 of instructions]], we will get some penalties, like [[unclear: proposed penalties]] [[unclear: we don't learn today]]. This slide explains about the penalties for the incorrect prediction. In this example, let's assume that instruction H is the branch instruction, and after completing the execution stage, we will know that instruction H will go to instruction K.

16:50 화자 1
In this slide, you see that instruction h is here and instruction k is here. So this is the kind of if something, then after do the if segment, then the program will jump to here. But in RISC -V, in our data path and control path, we can know that the branch is taken or not in execution stage. We need to do the arithmetic operations like [[unclear: comparing to a parent's instruction]] or whatever. know that the branch is taken in the execution stage. So at T0, the instruction H comes into the processor.

17:37 화자 1
But at T1, we do not know that this instruction will be taken or not. So this slide says that at T1, we decode the instruction. So we know that the instruction H is a control flow instruction. That means that this is the first opportunity to correct the prediction. But as I explained, we couldn't know whether this is taken or not in instruction decode stage. So at this point, we are not able to correct the incorrect prediction. Or even we could not know that this prediction is correct or not.

18:32 화자 1
So [[unclear: at P2]], another instruction comes into the processor, like Instruction J, and Instruction H moves to the execution stage. And for branch instructions, in execution stage, the ALU compares to-- or I mean, the ALU do some arithmetic operations to compare to operands. And after doing the arithmetic operation, we can conclude that if [[unclear: branch instruction is taken over]], And in this example, we are sure that the branch is a branch and it goes to the instruction k. So we know that the branch is taken. And that means that at T3, this is the first time that we can correct the incorrect prediction.

19:31 화자 1
Which means that after completing T2, after passing T2, we know that the [[unclear: prediction for the prediction instruction H]] is incorrect And we need to cancel two instructions in the middle, like [[unclear: instruction A, I, and J]], because they are actually based on the prediction, but we know that the prediction is incorrect. So similar to hazard that we learned last week, We will cancel the two instructions and we will insert bubbles. Bubbles are as a null operation. And then we update the program counter to points to the instruction K here. So this is how a processor resolves the branching instruction.

20:36 화자 1
That means that in this naive branch prediction, processor always moves to the next instruction and after it realizes that the prediction is incorrect, it cancels out the instructions that is based on the prediction and [[unclear: moves to the current instruction]]. So how to implement this kind of [[unclear: differential regression]] is similar to the bubbles that we learned last week. After that, [[unclear: we move to the current one]], and these two are canceled, and the processor works as a normal operation. So as you can see in this example, there are some performance penalties, right? We need to... We waste two cycles to execute the correct instructions.

21:35 화자 1
But overall, this provides performance improvement because of the nature of your program, which means that, as seen in this research, Many of the instructions are not control flow instructions and because of that, even if we have a performance penalty for control flow incorrect prediction, the overall performance will be improved compared to This naive compared to stalling for data dependence on program counter. This figure shows that how a processor works if we do not do the prediction.

22:32 화자 1
And this is the [[unclear: research view]] of the misprediction. There is an instruction H, and we know that H is a branch instruction that moves to the instruction K. So two instructions, branch H moves to the instruction K.

22:56 화자 2
Thank you.

22:56 화자 1
Because these two instructions are incorrect, we insert bubbles. a processor works as shown in this example. H moves to H moves as there is no dependence or there is no hazard. Instruction I and J are canceled at T3 because we know that [[unclear: after T3 we could know]] that instruction H.

23:26 화자 2
Thank you.

23:27 화자 1
Moves to the instruction K and the prediction is wrong. And at T3, instruction K comes to the instruction fetch stage and the remaining part of the process of work as we learned in last week or before. So this, what? Is this, that?

23:50 화자 2
Sure.

23:58 화자 1
Okay, that is the concept of-- actually I-- no, don't wait.

24:08 화자 2
- I don't think you do.

24:09 화자 1
That is the concept of the [[unclear: proposed penalty]] for the missed prediction. Let's do some mathematics to know the correct number for the missed prediction. Because actually this research done by these guys, we get these numbers, and based on the numbers, we know that 86 of the time, we make the correct prediction. So [[unclear: here that is D. this number comes from the previous slide]]. And for the correct guess, there is no performance penalty, which means that we expect one instruction per cycle.

25:07 화자 1
But for the 14 of instructions, there are penalties. And as shown in the previous slide, the performance penalty is two cycles, two bubbles. So we waste two cycles for each incorrect instruction. And to make the mathematics simple, let's make some assumptions. Like there is no data hazard, there is no data dependencies. Oh yeah, these numbers are the same numbers from the previous research. So 20 of instructions are control flow instructions and 70 of control flow instructions are taken. Then we can do the math based on these numbers for every instruction per cycle.

26:00 화자 1
As a reminder, in an ideal case, every instruction per cycle should be 1, which means that we want to complete one instruction for every cycle. But because of the penalty, we will get less number. Based on these numbers, the instruction per cycle for the Naive prediction is that 1 over 1 plus probability of wrong guess times penalty for wrong guess, which means that [[unclear: This number stands for the ideal case of instruction per cycle.]] That number stands for instruction per cycle for the ideal case, which means that if there is no penalty, then we complete one instruction per cycle.

26:58 화자 1
And this is the total penalties for the wrong or mispredictions. This is the probability of wrong or misprediction, and this is the penalty for the misprediction. And as you see here, the probability of a wrong guess is [[unclear: 0 .2 times 2 .7]], so it is 0 .14. And the [[unclear: probability of a wrong guess is 2 cycles]], as we studied in the previous slide. previous slide. So if you put these numbers into the equations, then you will get this number, like 1 over 1 .28, which results in 0 .78.

27:40 화자 2
Thank you.

27:42 화자 1
I'd like to say that these two cycle penalty is [[unclear: dependent on our]] which means that these numbers are not fixed [[unclear: across the old processors]]. We are talking about a specific data path and control path that we learned in previous lectures. In that design, in that five -stage pipeline design, incorrect guess will result in two cycles as a penalty. But if you implement some different design, the penalty for the incorrect guess will be different. So I'd like to say about the number, but in this lecture, we said we assume that the number 2 is just a penalty for our incorrect guess for this prediction. So the [[unclear: average instruction per cycle is 0 .6]]. which means that it is less than 1.

28:41 화자 1
So it is a little bit lower than the ideal case. As I told you, in the ideal case, the instruction per cycle should be 1. we are having [[unclear: proposed penalty]] of this prediction as 0 .22. [[unclear: 0 .22 is the penalty]]. And I keep saying that this prediction is kind of naive, which means that we always predict that the next instruction is located at the program counter plus four. But in reality, we can predict better. The next topic that we're going to learn in this course after the midterm is about the branch prediction. And you will learn-- you will implement the branch prediction [[unclear: in number four, I think]].

29:36 화자 1
So I think in our example, in our example processor design, we can improve this number to [[unclear: around 0 .9]] after we learn about the prediction. So that is one important topic regarding pipeline design. So So what we want to do after the midterm is to improve the penalty for the misprediction. But as you see here, this is the equation that appears in the previous slide. The instruction per cycle is blah blah blah and 0 .2 times 0 .7 times 2, which means that this, the number 2 is the cycle penalty and the number 0 .7 is...

30:34 화자 1
Hold on. 0 .7 is the portion of control flow instructions that are taken and 0 .2 is the portion of control flow instructions in your program. So there are many ways to improve the performance regarding the prediction, branch prediction. Like if your compiler is smarter, then your compiler may introduce the optimizations to [[unclear: improve this number of data]]. Let's take an example like this.

31:19 화자 1
If you implement a C program and the C program has if statement which compares a variable But [[unclear: if your program always stores number zero in that variable, then the bridge footprint, the infospeed is always true]]. And if your compiler is smarter and it knows about that, then the compiler will remove the branch instruction. But that is another topic in this course. And we will think about other techniques to improve this number. This number comes from your program, right? If your program introduces a lot of branching structures, then this number is proportional to the number of branching structures in your program. So that is kind of...

32:17 화자 1
Actually this is not a fixed number, but let's take this number as a fixed number. And because we fixed our data path and control path, as we learned, as the example processor design, so this number is also fixed. And what we're going to do is that [[unclear: we will improve this number. We will improve this number.]] Yeah, we will improve this number [[unclear: after the beta]]. So that is related to the branch prediction. And before I explain about this, I will talk about this.

33:03 화자 1
In hardware, [[unclear: every performance optimization will have a kind of security implications]], which means that even though you That kind of microarchitectural optimizations are not visible to programmers. That has some very subtle effects in the processor and that may make a data breach. For example, this is a C program that may have a security problem. So this is the [[unclear: A4C command]] and [[unclear: then in this code is the pet]], the [[unclear: A4C command]] says that if you have privilege to access privileged data, then the program accesses the privileged data.

34:01 화자 1
If you provide this code to some random people, then those random people do not have the privilege, so they are not allowed to access the privileged data. But what actually happens in a processor is that the [[unclear: processor predicts that this if statement is taken]] and actually accesses the data.

34:24 화자 2
Thank you.

34:26 화자 1
Think about our branch prediction in previous slides. Even though we do not know that the branch is taken or not, we move to the next instruction we execute instructions in incorrect path. So given that, [[unclear: even if a person who does not have the privilege to access the data, the processor will execute instructions here and actually access the data]]. It seems fine in the architectural viewpoint, which is fine for developers, but in micro -architectural viewpoint, it changes the micro -architectural components and states.

35:17 화자 1
One representative micro -architectural component is cache, so actually data comes from maybe memory to cache and the data resides in the cache.

35:33 화자 2
Thanks.

35:35 화자 1
Because we have not learned about cache and some kind of branch prediction, we will talk about this in detail later. Because the data moves from the main memory to the cache, it may create some security problems like data leakage. [[unclear: So these two are a representative example of the.]]

36:07 화자 2
Thank you.

36:08 화자 1
These two are representative examples of security problems in Intel processors. [[unclear: This is related to Intel and this applies to all processors.]] [[unclear: Nine years ago]], so I think you guys are in elementary school. At that time, Intel, there were very big news about the Intel processors.

36:32 화자 2
Thank you.

36:34 화자 1
I don't know how to say that. How to say this? [[unclear: It has been really low because of this.]] I don't know how to say this. I don't know what the-- I don't have vocabulary about stocks. So whatever.

36:54 화자 2
Thank you. Thank you.

37:02 화자 1
So there are security vulnerabilities in processors, one is called Meltdown and one is called Spectre. And we're going to learn about Spectre in detail in the makeup classes. And actually, [[unclear: you can in your processor]]. Spectre is still there, so you can try this later. [[unclear: I will provide an example of the Spectre implementation]]. And Meltdown was a kind of a similar problem. It [[unclear: allows a network attacker to read all data in memory even though the attacker does not have a privilege]]. This was a kind of [[unclear: procedure problems]] in the processors. We will learn about that later. And this is a kind of research object.

38:03 화자 3
Thank you.

38:06 화자 1
In security community, which is called hardware security. And if you want to do hardware security research, then please reach out to me. And you can [[unclear: come to the greatest]].

38:20 화자 3
Thank you.

38:23 화자 1
Anyway, that is the branch prediction. I mean, we are discussing about the branch prediction, but there are some other ways to avoid the stalling for every branch instruction. So what is the similar to the previous I forgot to tell. Like we learn, what is, in our, this R2000, same thing applies for the data hazard and it applies for a branch hazard, I mean control flow hazard. I forgot to tell. But this is not important because [[unclear: this disappeared. This is gone.]] Anyway, [[unclear: the idea is that it always predicts that]], it always makes that [[unclear: current color code support is a current instruction]].

39:22 화자 1
So it always moves to the current code. It always moves to the next instruction, but for the branch instruction, it is not true. We might need to move to somewhere else. So it placed some [[unclear: low operations after the branch instruction, and because of the low]] It does not have to insert bubbles, but the same disadvantages applies to this kind of [[unclear: branch -delayed load]]. It makes the compiler aware of the underlying microarchitecture And because of that kind of the burdens, [[unclear: this does not exist anymore. This disappeared.]] In fact, [[unclear: all kinds of processors that you use these days apply the branch predictions]] instead of this kind of.

40:22 화자 3
Thank you.

40:24 화자 1
Bad, stupid, I mean, this kind of bad design choices.

40:32 화자 2
Thank you.

40:33 화자 1
Actually, that's it for today's lecture because this lecture is not a part of your midterm. [[unclear: I tried to make it.]]

40:45 화자 2
Sure.

40:50 화자 1
And also we have another homework segment, I mean, homework lab session today. So our TA will introduce the homework number two. So from now on, our TA will introduce the homework number two, which is the homework.

41:10 화자 2
Thank you.

41:11 화자 1
Is related to the single cycle [[unclear: processor design in.]]

41:33 화자 2
All right.

41:40 화자 1
Even though we do not have [[unclear: official website, Office hours]], you can always reach out to TAs or me if you have any questions about lecture contents or homework assignments. Which means that you do not have to hesitate to send me an email if you think some contents in our lecture slides is confusing. So if you want to clarify about it or if you want to I don't know. So, I mean, what I want to say is that you always can send me an email and then I will [[unclear: locate my time]] to make a on -demand office hour. So you can always come to my office to ask about the lecture contents or whatever.

42:37 화자 1
I'm saying this because we are heading to the midterm, so.

42:42 화자 2
So good job.

42:43 화자 1
So if you.

42:45 화자 4
All right.

42:46 화자 1
Hard time to study, then you can always send me an email.

42:53 화자 4
Hello, everyone.

42:54 화자 2
Shh.

42:57 화자 4
In Lab 1, you build a single -cycle CPU for the R -type and I -type instructions. In Lab 2, you will complete it so that it runs all the RISC -V 64 integer instructions. The new instructions are loads, stores, branches, lui, auipc, jal, and jalr. The templates are already contains a lab1 solution. [[unclear: So I type and I type work from those tasks.]] [[unclear: You will modify the same files as in lab1.]] And the [[unclear: places to change are marked with to do]]. [[unclear: Do not change the I /O of any module.]]

43:54 화자 4
Some control signals are [[unclear: defined differently from the rest]]. So please read assignment 2 carefully and follow the definition there. The document is.

44:09 화자 3
Thank you.

44:10 화자 4
Organized as [[unclear: part 1, 2, part 9]], and each part has its own test suite. Go in order and run the test as you go. Before you start coding, draw the wires on the worksheet, including the control wire you have to submit to the completed worksheet. [[unclear: This is the left worksheet. It is the left one worksheet plus the data memories.]] Through the worksheet, you need to write down width of every wires. The due date is November 2nd, 2359 on ETL. Submit one tar file named with your student's ID.

45:07 화자 4
It contains the [[unclear: full code file]] and your worksheet. [[unclear: Only these files are ready.]] So you may readily [[unclear: modify the test files for the government]]. Any questions? Okay, it's done.

45:31 화자 3
Thank you.

45:37 화자 2
Thank you.

45:53 화자 5
Actually, I didn't expect this short session. I expected something longer than this, but that's OK. I have nothing to say. I'm just holding the mic to say something, but I don't know what to say. I hope you guys prepare well for the midterm for this course and for other courses. That's it. That's it for today's lecture.

46:34 화자 3
[[unclear: Thank you.]]

46:39 화자 6
[[unclear: Thank you.]]

46:40 화자 3
[[unclear: Thank you. All right.]]

47:14 화자 2
[[unclear: Thank you.]]

47:20 화자 3
[[unclear: Okay.]]

47:33 화자 2
[[unclear: Thank you.]]

47:38 화자 3
[[unclear: You.]]

47:47 화자 2
[[unclear: Thank you.]]

47:59 화자 3
[[unclear: Thank you. Thank you. Thank you. Thank you. Thank you.]]

48:22 화자 6
[[unclear: Thank you.]]

48:24 화자 3
[[unclear: Thank you. Thank you.]]

48:33 화자 6
[[unclear: Thank you.]]

48:34 화자 3
[[unclear: Thank you. wow.]]

48:46 화자 6
[[unclear: Um.]]

48:52 화자 3
[[unclear: Thank you.]]

49:12 화자 6
[[unclear: Thank you.]]

49:24 화자 2
[[unclear: Thank you.]]

49:26 화자 3
[[unclear: All right.]]

49:55 화자 2
[[unclear: Thank you.]]

49:56 화자 3
[[unclear: Thank you.]]

50:15 화자 2
[[unclear: Thank you.]]

50:20 화자 3
[[unclear: How are you?]]

50:26 화자 6
[[unclear: Okay.]]

50:29 화자 3
[[unclear: Thank you.]]

50:41 화자 2
[[unclear: Thank you.]]

50:42 화자 3
[[unclear: Thank you.]]

50:47 화자 6
[[unclear: Thank you.]]

51:03 화자 2
[[unclear: Thank you.]]

51:09 화자 3
[[unclear: So okay.]]

52:02 화자 2
[[unclear: Thank you.]]

52:06 화자 3
[[unclear: Okay.]]

52:19 화자 2
[[unclear: Thank you.]]

52:26 화자 3
[[unclear: Thank you. All right.]]

53:28 화자 3
[[unclear: Okay.]]

53:37 화자 2
[[unclear: Thank you.]]

53:50 화자 3
[[unclear: Okay.]]

53:53 화자 2
[[unclear: Thank you.]]

54:09 화자 3
[[unclear: You Thank you.]]

55:45 화자 2
[[unclear: Thank you.]]

55:46 화자 3
[[unclear: Okay. Thank you. Thank you.]]

56:58 화자 2
[[unclear: Thank you. Thank you.]]

57:09 화자 3
[[unclear: Thank you.]]

57:32 화자 2
[[unclear: Thank you.]]

58:20 화자 3
[[unclear: Thank you.]]

58:25 화자 2
[[unclear: Thank you.]]

58:30 화자 3
[[unclear: You Thank you. so.]]

59:13 화자 2
[[unclear: Thank you.]]

59:14 화자 3
[[unclear: Thank you. Thank you.]]

59:51 화자 2
[[unclear: Thank you.]]

01:00:11 화자 3
[[unclear: Okay. Thank you. um.]]

01:01:06 화자 2
[[unclear: Thank you.]]

01:01:23 화자 3
[[unclear: Thank you. Thank you.]]

01:01:56 화자 2
[[unclear: Thank you.]]

01:02:12 화자 3
[[unclear: Thank you. So Thank you.]]

01:03:01 화자 2
[[unclear: Thank you.]]

01:03:08 화자 3
[[unclear: Okay.]]

01:03:14 화자 2
[[unclear: Thank you.]]

01:03:34 화자 3
[[unclear: Thank you. so.]]

01:04:36 화자 2
[[unclear: Thank you.]]

01:04:40 화자 3
[[unclear: Thank you. Thank you.]]

01:05:40 화자 2
[[unclear: Thank you.]]

01:05:51 화자 3
[[unclear: Thank you. All right. Okay.]]

01:07:34 화자 2
[[unclear: Thank you.]]

01:07:52 화자 3
[[unclear: Thank you.]]

01:08:03 화자 2
[[unclear: Thank you.]]

01:08:24 화자 6
[[unclear: - Thank you.]]

01:08:25 화자 3
[[unclear: Thank you. Thank you.]]

01:08:41 화자 6
[[unclear: Thank you.]]

01:09:08 화자 2
[[unclear: Thank you.]]

01:09:13 화자 3
[[unclear: All right.]]

01:09:22 화자 2
[[unclear: Thank you.]]

01:09:27 화자 3
[[unclear: Thank you. Thank you.]]

01:09:49 화자 6
[[unclear: Thank you.]]

01:09:53 화자 2
[[unclear: Thank you.]]

01:10:04 화자 3
[[unclear: Okay. Thank you.]]

01:11:00 화자 2
[[unclear: Thank you. Thank you.]]

01:11:46 화자 3
[[unclear: Thank you. Thank you. Thank you.]]

01:12:55 화자 3
[[unclear: Thank you.]]

01:13:06 화자 3
[[unclear: so Bye.]]

01:14:39 화자 3
[[unclear: All right. so.]]

01:15:00 화자 2
[[unclear: Thank you.]]

01:15:16 화자 3
[[unclear: All right. So.]]

01:16:02 화자 2
[[unclear: Thank you.]]

01:16:07 화자 3
[[unclear: Okay. So,]]

01:17:08 화자 2
[[unclear: Thank you.]]

01:17:10 화자 3
[[unclear: Amen.]]

01:17:22 화자 2
[[unclear: Thank you.]]

01:17:27 화자 3
[수업 종료 후 개인적 발화 비공개] so.

01:18:12 화자 2
[[unclear: Thank you.]]

01:18:32 화자 3
All right. Thank you. [수업 종료 후 개인적 발화 비공개]

01:19:40 화자 3
[[unclear: - Sorry. Thank you. Thank you.]]

01:20:44 화자 3
[[unclear: Okay. All right. Thank you.]]

01:21:54 화자 2
[[unclear: Thank you.]]

01:22:04 화자 3
[[unclear: Thank you.]]

01:22:26 화자 2
[[unclear: Thank you.]]

01:22:30 화자 3
[[unclear: All right.]]

01:23:02 화자 3
[[unclear: yes so So.]]

01:24:36 화자 2
[[unclear: Thank you.]]

01:24:39 화자 3
[[unclear: You.]]

01:24:54 화자 2
[[unclear: Thank you.]]

01:24:55 화자 3
[[unclear: So Thank you. All right. Thank you.]]

01:26:04 화자 3
[[unclear: Thank you.]]

01:26:14 화자 2
[[unclear: Thank you.]]

01:26:17 화자 3
[[unclear: So All right.]]

01:27:22 화자 3
[[unclear: so so.]]

01:28:22 화자 2
[[unclear: Thank you.]]

01:28:27 화자 3
[[unclear: Thank you. So.]]

01:29:08 화자 2
[[unclear: Thank you.]]

01:29:24 화자 3
[[unclear: So.]]

01:29:41 화자 2
[[unclear: Thank you.]]

01:29:42 화자 3
[[unclear: So Okay.]]

01:30:56 화자 3
[[unclear: Thank you. Thank you. um.]]

01:32:02 화자 2
[[unclear: Thank you.]]

01:32:03 화자 3
[[unclear: Thank you.]]

01:32:40 화자 2
[[unclear: Thank you.]]

01:32:43 화자 3
[[unclear: Okay.]]

01:32:50 화자 2
[[unclear: Thank you.]]

01:32:55 화자 3
[[unclear: Thank you. All right. All right.]]

01:33:59 화자 3
[[unclear: so Okay.]]

01:34:59 화자 3
[[unclear: Thank you. So so.]]

01:36:02 화자 2
[[unclear: Thank you.]]

01:36:13 화자 3
[[unclear: Okay.]]

01:36:17 화자 2
[[unclear: Thank you. Thank you.]]

01:36:58 화자 3
[[unclear: So All right.]]

01:37:38 화자 2
[[unclear: Thank you.]]

01:37:41 화자 3
[[unclear: Thank you. Thank you.]]

01:38:55 화자 3
[[unclear: All right. All right.]]

01:39:35 화자 2
[[unclear: Thank you.]]

01:39:37 화자 3
[[unclear: Thank you.]]

01:39:46 화자 2
[[unclear: Thank you.]]

01:39:52 화자 3
[[unclear: So.]]

01:40:06 화자 2
[[unclear: Thank you. Thank you.]]

01:40:49 화자 3
[[unclear: Thank you.]]

01:41:11 화자 2
[[unclear: Thank you.]]

01:41:33 화자 3
[[unclear: Thank you. so All right.]]

01:42:27 화자 2
[[unclear: Thank you.]]

01:42:38 화자 3
[[unclear: Okay. but Thank you.]]

01:43:55 화자 3
[수업 종료 후 개인적 발화 비공개] Okay.
````
