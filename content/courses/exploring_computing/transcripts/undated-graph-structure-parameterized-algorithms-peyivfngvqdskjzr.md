---
title: "Graph Structure and Parameterized Algorithms · 보정 STT · 날짜 미확인"
course: exploring_computing
term: 2026_Fall
course_confidence: user_confirmed
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

수업 날짜는 미확인이다. 원음 없이 대조한 텍스트이며, 확정할 수 없는 표현은 `[[unclear: …]]`로 남겼다. 강연 슬라이드·도식은 제공되지 않았다.

````text
01:01 화자 1
오늘 강연을 해주실 [[unclear: 맥시멜리안 고르스키]] 박사님이십니다. 박사님은 컴퓨터공학부의 교수 신임교수로 조인하시기로 확정이 되어 있고요. [[unclear: 바로 다음 학기부터 신임교수로 임용되실 예정입니다.]] 그래서 알고리즘 분야에 혹은 Theory of computation 분야에 그동안 계속 우리가 열심히 좋은 분을 찾아서 교수를 찾아다녔었는데 우리 레이다에 걸린 훌륭한 연구 실적을 맺은 젊은 교수님 중에 굉장히 알고리즘 쪽에 좋은 결과를 내고 계십니다. 그래서 연구 분야가 주로 그래프 theory나 Theory of computation 쪽에 관련된 얘기들일 텐데요. 오늘 그에 관련해서 설명을 좀 해주실 거고, 그다음 대담을 통해서 좀 더 디테일한 내용들에 대한 discussion이 있을 예정입니다.

01:57 화자 1
그러면 먼저 큰 박수로 우리 신임 교수님을 환영해 주시면 좋겠습니다. [[unclear: If you're having me, I hope you do well, I come to you from somewhere.]]

02:23 화자 2
네

02:29 화자 1
[[unclear: No one plays I can also just talk about it so I come to you somewhere from there, so somewhere out in the country]], my goal today is not so much to explain to you like a particular concept or something like this so it's not really about the exact thing that I'm talking about. [[unclear: I think that's a bit too much, but thank you think it might still be a bit high.]] This is it's not really about the exact problem I'm talking about, it's more about the perspective I take on these kinds of problems, so I'll talk you through [[unclear: how to attack a precipitous specific problem]] or think about a specific problem in my area. [[unclear: Unless you start with, let me start with]] just talking about the fact that I'm talking about graphs, so you have some dots, they're connected by edges, these lines.

03:25 화자 1
They could represent really anything so often you would say something like [[unclear: sweet networks]] or protein or some chemical compound that you're analyzing or just something very abstract you could have like data in a database and then things are connected [[unclear: if some entry overlast. This will have the same value as a column]], so you can represent a lot of things with graphs and I'm interested in this.

03:56 화자 1
[[unclear: Catus one has follow]] which is pretty easy to explain it turns out to be pretty difficult so here I have my graph and some of the vertices I have colored so [[unclear: the blue guys are a pair and the orange guys are a pair and the pink guys are a pair]] and what I want to find is to be Connections between them, which means paths in this so line that I can draw through this graph that connect same color pairs without these lines overlapping. It turns out this problem can be solved on this particular graph it's not that hard, but [[unclear: in general this is empty and if you don't know much, maybe, you know, p versus empty empty is the stuff that's hard we would like things to not be empty]] but this kind of problem it shows up in Practice so something you might want to do is you have some idea of how you want to lay out a chip, you have some parts of the chip.

04:52 화자 1
[[unclear: That you want to push on some project shit and you just want to connect them because somehow you have to get mixed connected]] and for this you need to know is it possible [[unclear: on the kind of That I can manufacture to get the kind of connections that I need to a question to be specific]] in practice, you will need a lot more than just knowing that things can be connected you don't want interference so you want the connections to be a little bit further apart, maybe you want something like I want a certain connection to be short. You don't want to go all the way around the chip to get somewhere all this kind of things can be done in addition, but the base problem is already hard and we're already trying to solve this in practice so you can maybe see that this is a problem.

05:32 화자 1
That people would want to solve [[unclear: so it's complete]], but maybe there's some way to do something in specific instances because this is what a practice happens, is that the instances you're looking at is not General instances, but something very restrictive so a specific instance might be something like a planar graph [[unclear: we call a graph planar if I can draw it on a sheet of paper. An infinitely log sheet of paper]], and then I can have something like a very abstract thing where I just say on the edge of this sheet of paper, I put some dots and then tell me if through the middle you can connect these dots. And in this case, if I have to stay within this circle that I drew, I cannot actually find the appropriate connections because [[unclear: the purple pair and the blue pair kind of block each other, they kind of form across]].

06:22 화자 1
But I could I could exchange them and then you do find a solution so on the bottom here if I have changed them then you can actually find a solution [[unclear: the data blinds would for the dash blinds would give you a solution]] so there is some part of this that has to do with drawing on certain surfaces so there's Topological aspects of this problem and something that's a little bit annoying is that, okay, maybe I just identified when you can draw something and when you cannot draw something, so maybe I can [[unclear: solve the disturbance problem]]. [[unclear: On planar graphs while it turns out even on planar graphs this process and even peak and even on grid graphs]] so even if I give you a very structured graph that has like [[unclear: very new connections]] that should be easy to analyze this is still a hard problem but There is this something called a fixed parameter algorithm for this that basically says that [[unclear: if you're only looking for a fixed number of pairs, let's say you only have 20 pairs]].

07:20 화자 1
[[unclear: Then your runtime will be of the algorithm will be that in terms of the number of pairs]], but there's only a fixed number of them, but it will be okay in terms of the size of the instance, so [[unclear: the size of the chip doesn't matter that much, the size of the grid doesn't matter. That much]], what is important is how many things you want to connect and in practice this is the kind of algorithm we're using, we're kind of abusing the fact that we have a very large structure on which we can do stuff and we're only looking at a very few pairs that we want to connect.

07:51 화자 1
Can this be generalized so can we get such an algorithm in general because okay, I said it was [[unclear: empty complete]] but maybe in general I can do something like for a restricted number of pairs, I can solve something quickly [[unclear: in the United States yes]], and I have like a [[unclear: A squiggly line to the 12th year because Robertson's Lord gave an answer to this]] is just that [[unclear: the answer took a very long time to come home]] and what I want to talk about is how they approach this answer so in general the problem is hard how do you get it easy if you know that you only have [[unclear: a bounded number of pairs that you have to commit]]? So let's start with maybe I should say two things I gave here two functions f. Can be very different the thing here above [[unclear: this runtime that read found for his algorithm this is like some single or double exponential function it's that but it's expressible this function f prime here is unknown]].

08:50 화자 1
The proof that they gave just shows that there exists an algorithm which was absurd at the time now it's just a little bit more common, but it's still fairly absurd. They gave a proof that there exists an algorithm that can do something, but [[unclear: there is no algorithm in the paper, they're just purely existential]]. So I want to talk about what they did there and how to make it practical. And [[unclear: for this app to start at]] how do you reduce the complexity in your graph if you know you have a bounded number of pairs so here we're getting an okay, how do I reduce my problem in complexity this is finding reductions, finding parts of my instance that are Easy to look at and then say, okay, I can exclude the fact that maybe I have large, in this case, large cliques so what is a clique, a clique is a graph where all pairs of vertices are connected.

09:41 화자 1
Here are some small cliques [[unclear: from K1, which is a clique with one vertex up to K6]] and maybe let's say we have three pairs of vertices There is a large clique in my graph. Maybe we can do something like this and you're not saying, what if our graph contains a large thing [[unclear: I'm using contains a little clucity, it's not super important what the exact definition of what I mean?]] Okay, so maybe my pairs are connected to this clique this would be nice if all of them kind of go into the clique because the clique allows me to route however I want if I can get onto the clique, then I can just use the edges of the clique to route however I want [[unclear: that might prompt have a solution everything is one]].

10:26 화자 1
So what about the opposite, what if there are no or not sufficiently many connections into this clique into this thing that allows me to route however I want well, in this case there has to be something that cuts me off of this only a few vertices were really an interface between the pairs and the clique exists. In this case, because the clique has so much structure, I can say I can just leave one of the vertices of the clique out because [[unclear: only three paths can come from the pairs onto these three vertices]], those three paths can do stuff in here, but [[unclear: there's so much. Virtual here]], that it doesn't really matter for these three paths, [[unclear: whether there's this one guy there or a number]], because the thing is large enough, there's enough space to run.

11:12 화자 1
So this is a reduction we do so maybe, you know, this is data reduction or kernelization or something like this this is a basic technique to say okay, maybe we can find some way to reduce the size of our problem and keep iterating this until our problem has a specific structure in our case that [[unclear: our problem doesn't contain much]] So in this case, I would delete this irrelevant vertex and get a smaller instance and then ask again, do I still have a large clique [[unclear: because I just deleted a vertex to a clique, it might just be that there may no longer be a large clique.]]

11:44 화자 1
So now we get to the part that I'm more of an expert in and that is what about [[unclear: graphs that don't contain large cliques]] generally cliques for a lot of problems are good things to have and the problem is analyzing things that don't have large cliques so here Let's say maybe we suspect that graphs that don't have large cliques might be built from graphs that are planar well, if I fix some size of clique, this might not be true. We saw the K5 at some point here, this graph was not planar. But if I have like a [[unclear: K one thousand that I'm excluding as the large clique, then my planar graph on the SK four]] and I could actually add some vertices on top that see the entire planar graph and all I'm doing is [[unclear: slightly increasing the size of the clique by giving me something to draw on that it's a universal in some sense]].

12:36 화자 1
So it's not enough to just say the simple parts are planar, you also have to say the simple parts are planar, maybe there's some vertices that allow me some stuff, but there's not many and actually this is still not enough because it could be that the place that we're drawing on is not actually a Sheet of paper but maybe like [[unclear: a donut or a double tourist or some kind of surface like a client bottle or the projective plane]] [[unclear: all of this doesn't allow you to draw that complicated up clique but still a little bit more]] so there's more structure I have to exclude or more structure I have to account for so maybe what I actually have is [[unclear: Some bounded gene and surface]] and there's some vertices that kind of see everything. But actually this is still not enough because it could be that actually what I'm drawing here exactly might be [[unclear: slightly fussy because the connections that I need this week are not as straightforward]].

13:34 화자 1
So if you analyze this further, you figure out that actually you have to abstract a little bit more. And then say that, okay, [[unclear: we're drawn on some balance in the surface]] and then there's some vertices, and then you have to look. A little bit closer and then it's not drawn exactly correctly, but it's almost drawn exactly correctly. And even that is not enough because it could be that locally somewhere stuff is not drawn at all properly, [[unclear: not even visit properly, but really improper]] and then maybe if this is controlled enough, then you could be in this kind of graph. [[unclear: This is what we call hortices]], doesn't really matter so much what this is in specific and [[unclear: it turns on that this is then finally correct]], what we're kind of seeing is that we went from the intuition that planar graphs are somewhat easy to figure out what doesn't work with planar graphs.

14:27 화자 1
So I have to add something then trying to think of, okay, what else could possibly happen well, [[unclear: I might not be playing it]] because I can be drawn on something slightly more complicated, then you have to analyze the slightly more complicated thing that you have to analyze your notion. Of what drawing means, this has to be slightly generalized and then once you have this down and this is actually this previous thing was what people thought was correct, people thought that you could just [[unclear: draw on some biology in the surface. Have some in this approximate way]] and have some vertices on top [[unclear: people conjecture that this was the right answer]], but then if you really dig deep, then it turns out that there's some very annoying counter examples that show you that you need to account for small local nonplanarity. [[unclear: This is what non suddenarily will not tell you much, but crosses that are kind of locally contained]] and this is how you get [[unclear: these orange areas, these borders]].

15:22 화자 1
The fact that this is correct was first proved by [[unclear: Robertson, Simon]], and my contribution to all of this is that we very recently, that is [[unclear: last year found out]] that it's not only correct, but it also exists with good. And explicit bounds so this again, [[unclear: this correct mistake here is existential they just say you can that this decomposition exists, you can take your part of the graph, a part of this way]] we tell you how to do this algorithmically and [[unclear: the algorithm is not even bad, it's not even that disease and it's actually polynomial time]]. Um. And then finally this was [[unclear: this year we solved this K, this one past problem with an explicit runtime]], this was open for a very long time [[unclear: as double exponential in K and Q, big and N, all of these you could try to still prove you're definitely not getting out of the double exponential ink that you're not getting out of.]]

16:16 화자 1
[[unclear: Being at a single exponential, but it's not clear maybe our single exponential, this is still on]], as I said, the specifics of what I was talking about are not super. Important, it's more what we do in our area is kind of abstract away, look at a simple problem and then try to reconstruct whether our abstraction and our perspective was too narrow and this is kind of the process of slightly widening your perspective until you hit the right amount of [[unclear: Concreteness after an abstracting swatch wonder, that was what I wanted to press upon the children.]]

17:19 화자 1
Okay, there are a lot of [[unclear: freshmen in a second year strategy]] here, and probably they have some trouble understanding [[unclear: what journey explained]], that's fine. He just explained all the structural graph theory and complexity theory and exponential complexities I never seen before, to be honest, and that kind of thing. Actually starting your talk, starting from some application of this problem, [[unclear: Kd's joint problem]] and But that's the motivation at the beginning, after then you still think that application in your mind to solve that problem [[unclear: where SI design and circuit design and things like that]].

18:16 화자 1
Not really if you're closer to the application that you would try to figure out what are the constraints of my instance that I can use to make my problem easier, but [[unclear: there's the worst level of abstraction and then there's the practical material]]. And if you're [[unclear: designing for the practical materially]], you're abstracting away from it and then trying to approach it somehow, and we're kind of on this level and trying to get as general as possible to not just get this very specific application where you can say, I know that a chip is never going to be worse than Whatever [[unclear: a double tourist or something like this, in effect]], so the way I think most of this problem is really drawing on surfaces, this is [[unclear: the most sensible way to About this]], if you're looking at it very much from the theory.

19:14 화자 1
Whenever I ask this kind of question to my mathematician friends, they really don't like me, but so if so. Well, why do people have to study graph theory or structural graph theory most of people in the world only small fraction of people understands the problem [[unclear: so what do you think I'm not worth saying anyone to study structure?]] If you're thinking purely of utility, I mean, it is interesting, I know a lot of students just find the fact that this looks very complex, kind of attractive, the thing that we're doing.

19:58 화자 1
Takes a whole class of problems the thing I explained I'm using a tool to solve a problem the tool can be used to solve a very large class of problems a lot of the [[unclear: the last 25 or like 30 years]] this parameterized complexity is idea that you take [[unclear: Not just an entire class, I promise]], but say I only look at problems where something is bounded, let's say the number of pairs I want to connect is bounded. This is very much inspired by this perspective. [[unclear: Roberts and Simo]] did not formulate their original algorithms in this perspective, it was more like people saw what they were doing and they said, okay, this is actually a very clever way to look at this, [[unclear: to get close. The two applications and close over the needs that you come from.]] And this is how they got inspired about this, if you're looking even more broadly, [[unclear: why structurally or graph really might be interesting]].

20:59 화자 1
[[unclear: The tools we're developing are used in a very broad setting, but don't have to do ultimately a lot of the techniques]] that we're doing, this kernelization, this finding small reductions and why they work, this can be done even in practical algorithms. This is ultimately how this kind of filters through, but the very abstract perspective pushes us to find these kinds of new approaches to reducing problems. Tell us if there are some real big challenges in graph theory that might impact our life to some extent, is there any important problem you can easily explain? [[unclear: Instead of some problem worse to protecting]] there are plenty, I think one of the problems is that the question is a bit too broad because traveling salesman, if you know this problem.

21:57 화자 1
This is a graph theory problem, you have some given graph and you're a traveling salesman in the sense that [[unclear: you want to visit every node of the graph]] and maybe the edges you have also have some weights which may represent, for example, distances in a country. I think [[unclear: Bill Cook was here recently this year or last year]], and he did a traveling salesman of all the major cities in Korea, and the distances he took was just how long does [[unclear: Google Maps or neighbors]] tell you, does it take between the cities?

22:28 화자 1
This is not just for finding routes, but this is the general problem that has a lot of applications that you could solve this quickly this would clearly have some impact in your lives now there's the side that I studied like this kind of stuff would this have an immediate Impact on your life probably not would this have a large impact on how people understand graphs yes, but then you would have to be interested in graphs but again, this kind of trickles down if you can anything you can model the graphs can be attacked using graph theoretical methods and it turns out that a lot of things can be the model the graphs So this is kind of the perspective I would take, but graph theory nowadays is very broad, you can go into very applied stuff, there are people doing [[unclear: improving this chunk past algorithm specifically for finding nice routings of minds and chips]] and [[unclear: there's people like me who are very more extracted]].

23:24 화자 1
Probably we have to jump into some AI questions yeah, [[unclear: Openai opened that released 722 papers regularly recently]] and that papers is impacting the academia to some extent. In their papers are there some papers related to your own research so can you tell us what problem so the one really big one that people got I guess. Depressed about was so I talked about graphs that do not contain KT contain here means as a minor the most prominent structural graph here conjecture was is it true that [[unclear: if you do not contain KT as a minor, are you t minus one, colorable]], whatever that means? It's a very natural extension of the.

24:22 화자 1
[[unclear: Four colored your maybe your business like the nice popular science thing]] where you say if I have a planar graph, maybe colored with four colors, maybe, you know, [[unclear: this is not coloring, the not coloring problem]]. [[unclear: People are very interested in this people kind of conjectured that it probably should be wrong that you get this coming it turned out to be true so Openai did find a counter example]], the thing people were depressed about was not that it was a counter example, but then Openai found it So there are impacts in my field from this, although I have to say the methods that they use are very distinct from what I would use so the way they construct a counter example is as very usual as [[unclear: they kind of do some random graph construction that analyze as well]]. It seems to me the AI is just not staying at the level of just a tool for convenience.

25:17 화자 1
But it's doing more than there and what do you? What's going to be the future of theoretical computer science in post AI world [[unclear: AI is doing all the theory proof]] and are we going to compete with them or so what's what will think about them? I don't know about other areas in TCS I am not ready to say that AI will actually completely eradicate [[unclear: like a theory part of TCS or path]] there have been similar revolutions specifically for in computer science [[unclear: computer science is older than the computer]].

26:03 화자 1
And there was a point where there were people called computers, and once commercial machines, commercial actual computers were available, they were obsolete, you could just punch an algorithm in, but [[unclear: they were previously executed by And then it could just be the number sin]] and it would give you the results, these people became obsolete. I have heard people kind of make an analogy between AI and the calculator, maybe this is true, maybe some certain proof methods are essentially like using a calculator that the AI can execute well, it could be that I don't know, it could be that [[unclear: in a year the capabilities of AI will be such that I'm kind of irrelevant]]. We're kind of just take a historical view and read the papers that it puts out and [[unclear: make drive, explain them]], or it could be that we're just at a point where It takes significantly longer to get an original result, and the intermediate steps to getting that original result may involve you.

27:02 화자 1
Talking to an AI to get like an initial hypothesis out, they give you counter examples to this, maybe you find out through the counter examples [[unclear: where you're predictable. Well, in your justice and in this way it might anyway]], this is kind of an optimistic view because this would mean that less papers get published. Which might make it more reviewable, but for graduate students, there's something in mathematics that's kind of parallel to this So the TCS and graph theory and combinatorics are very young, [[unclear: they're slightly older than your science, maybe 100 years, 150 years if you want to be generous]]. But there's other areas of mathematics, like [[unclear: analysis or algebra, that are very real]]. A Phd student or a graduate student would work in those areas is to work on one problem for the entirety of their graduate studies and then have [[unclear: maybe one, maybe two, maybe three papers]] that are being submitted at the point that they finish the degree.

27:59 화자 1
It may be that TCS just starts to look like this more [[unclear: because that's a select to use AI. To prove to serve your problems]], I started using it to [[unclear: generate certain small classes and then check injectors]]. Because it's good at making proof and making code, so I use it for that I have tried to get some proofs out of it, I don't want to say it can't, but [[unclear: it's very much curved, is still struggling with the kind of thing]]. But I've tried it, it can do like small things.

28:43 화자 1
But I think in my area specifically, this is [[unclear: more of a memory implementation]] if you gave me, like in AI that had [[unclear: twice as a memory]], which would be very costly, but if it had twice as much memory, I think it could do the kind of things I do, [[unclear: at least some of them in the way that currently 볼까요?]] 뭐 편하게 질문하세요.

29:17 화자 3
Like before we go for the Q&A session, I'm going to make a quick announcement, so [[unclear: our rotor]] says there are like [[unclear: 130 people present in this room]]. [[unclear: Which obviously is in the case]], so we're going to run a quick reauthentication, so I'm going to send a push notification to your phone now so everyone present this room should do that. The number is [공개본 개인정보 삭제: 출석 인증번호], I'm going to show it here.

30:12 화자 3
So anyone who has issues to authenticate with the app should [[unclear: take a photo of your student card to the screen as a attachment]] so that you can later prove that you were actually present in this room. So like, you would have. [[unclear: Time to this class either by the app or student cards]] so anyone who has the issues with reauthentication please just take the photo here then we'll proceed with Q&A session.

30:56 화자 1
다들 했어요. 우리 그럼 다시 질문으로 넘어가 볼까요? 저 위에 질문이 있었는데, [[unclear: 정확히]]

31:14 화자 4
Thank you for your lecture. And I have two questions after listening to lecture [[unclear: first question was here currently in discrete mathematics. Your picture]] and graph theory kind of more related to mathematics instead of my perspective of computer science so I was wondering if now you were coming to our professor of computer science department. Are you trying to more focus on application of graph theory into computer science or focusing on theoretical problems and the second question was I am currently Getting conducting a research under [공개본 개인정보 삭제: 학생 연구기관] currently and [공개본 개인정보 삭제: 학생 소속 대학] by some [공개본 개인정보 삭제: 학생 지도자 식별 표현].

32:15 화자 4
And I'm also using graphs. To graph neural networks or network propagation things but I felt it's quite different from the graph theory so can you explain some relations between graph theory or graph applications to neural networks problems?

32:41 화자 1
[[unclear: This should get your question]] yeah, the second question I have to think about. So I think for the second question, it demonstrates how broad graph theory is I would not be able to tell you how to relate these two fields at all. what you're looking at in neural networks are graphs, where you're concerned with maybe a specific layout. And it has weights on all the edges and you're running a process through the graph, this is very much not what I care about graph classes, many graphs that kind of shares of common properties and [[unclear: I've tried it to do from these common properties, a structure that I want to find]].

33:24 화자 1
I want to say that for your first question, I learned all of this and I have a degree in computer science, so I have [[unclear: a bachelor's and a master's and a Phd in computer science]] and all of this is done as theoretical computer science, so the kind of work I will be doing would still be classified as computer science, I publish a computer science conferences, although I also submit to journals, although a lot less than into the conferences. So it's more of a prospective thing, yes, I interface also with discrete mathematics, but you can see your split in the cultures, the kind of papers we write in how we deal with these problems. Is very much distinct from the way that mathematicians seem to think about this, [[unclear: the bigger breakthroughs we did in the last two years]] were very much Tcs in the sense that the way we ultimately tackle the problem was to set up a very clever data structure.

34:22 화자 1
Work with this data structure [[unclear: much more than the natural tissue would have wanted]] so what will I focus on the work that we're doing is algorithmic but it's not applied in the sense that you might be used to I'm not looking at how to specifically improve the performance of a specific I don't know, network I'm looking at how to improve an algorithm that solves a very general problem and when I say that I'm improving performance or something like this, I'm proving a theoretical measure of performance and not running it on anything and then try to say on this test data set, it now runs quicker than that. 질문 답이 좀 됐어요. 또 다음 질문으로 넘어가 볼까요?

35:21 화자 5
Good lecture, do you have a plan to open a lecture about advanced graph theory or [[unclear: advanced diagram]]?

35:30 화자 1
[[unclear: I have a plan to from the plan for the lecture, if you want to hold me back]], I think the first thing I have to cover is basically [[unclear: your courses]]. So I think the plan is that I do one of the basic theory courses first, [[unclear: then next semester, I'll probably not do this kind of graph theory]], but more of a basic course and have it in the graph theory. [[unclear: Maybe now this week, the next spring]], I will teach a mandatory TCS course, [[unclear: something like this week map or algorithms or data structures]] and then [[unclear: the planets to in the fall have an algorithmic graph theory, of course, but not on this stuff, this would be more graphical]].

36:18 화자 1
For your information, [[unclear: we hire the two theoretical affected members at the same time]] so we will have more undergraduate theory courses we can provide and we will hire some more. 또 다른 질문 아무거나 질문해도 돼요. 뭐든지 하고 싶은 얘기 다 해도 됩니다. 저한테 여기도 있고 여기도 있네. 누가 먼저 있나? 제 쪽 먼저 하고 뒤쪽으로 넘어갑시다. [[unclear: Thank you for your grading lecture.]]

37:03 화자 1
I'm curious about that I am also a student who wants to pursue this theory, [공개본 개인정보 삭제: 학생의 개인 감정·대인 경험] what's the point, what is it useful, but [[unclear: what is the superficial meaning? Of this is the useful work what]] [공개본 개인정보 삭제: 학생의 개인 감정] so what I want to ask you is that how should we can [[unclear: prove ourselves worst fullness]] and how should we deal with it to pursue what we want to and [공개본 개인정보 삭제: 학생의 개인 감정·대인 경험] so I'm interested in your story about the theory.

37:58 화자 1
I think there's two aspects to this, there's the part where you have to justify it to yourself, but why am I doing theory, why is this like a worthwhile thing to do with my life I know other people who do work in Ngos. [[unclear: There's like an Africa pity people I'm not an Africa pity people]] for me, it was very intrinsic I found this to be, first of all, something that challenged me in the way that I found. Different from anything else I could find there was a kind of a sense of being able to completely grasp something this is nice about math, there's a subject that is so clearly.

38:44 화자 1
Outline that you can have a complete grasp of it and make an advance of it it's also something that and I think this depends on you, it can be a very solitary activity or a small group activity this also appeal to me and ultimately The advances you do in mathematics are more philosophical than anything else if you're looking at very pure math. If I look at the kind of algorithms I did, I can tell you that [[unclear: previously there was no function, now I have a double exponential]] and I can measure the progress, but if you're talking about in terms of understanding we understand or after this work, we understand something that was considered to be basically ununderstandable. [[unclear: Maybe I can have Levi structure]], so he had something that was basically ununderstandable and explained it in a simpler way and to maybe give an analogy to the AI, I think [[unclear: Rubbish and Simo]] wrote a series.

39:43 화자 1
[[unclear: Of 20 papers and it's like 500 pages long]] and I can guarantee you as somebody who works in the area that very, very few people have actually read it, fewer people understand it and [[unclear: working through it, improving everything]] and Giving an exposition of it that is more understandable is itself kind of rewarding because it refines the understanding we have for future generations as well, because [[unclear: they can leave the paper and I'll just ask me]] so this is my personal motivation. [[unclear: How do you justify the team]] I mean, at some point if you want to stay a theory, you may want to get a postdoc or [[unclear: get a tenure transposition, you have to apply for some brand]] the general approach is to say most of the problems do come from [[unclear: practical advantages. A graph theory itself kind of grew out of applications for electric engineering chemistry a lot.]]

40:38 화자 1
In fact, [[unclear: the way we notate graphs come through chemistry]] and you can always dig into what the source of your problem was and then route back and tell me, [[unclear: how does this actually prove the core application of that?]] There is also the part where you can say we want to refine our understanding of a large problem class. And we are working on the higher level theory, but this kind of trickles down, even though this is kind of a bad word in economics, it does trickle down this knowledge down the hierarchy of how applied fields are. So these are justifications you can make, but how to actually justify it, what the particular thing you're studying does depends a lot on what you're studying, I know people were further in TCS that could actually tell you that [[unclear: the outer that we're looking at does lead to the implementer of candy]]. And then it's easier to justify because you can say this is implemented here and used here by this company.

41:40 화자 1
Thank you, but sorry, there's no good and easy answer [[unclear: I actually quite influence kind of good influence on your answer and it seems to look to achieve it.]]

41:59 화자 4
Do you have any other interests apart from graph theory or like any pastimes, do you?

42:05 화자 1
Do I have hobbies?

42:06 화자 4
Yes, what kind of hobbies do you have?

42:10 화자 1
[공개본 개인정보 삭제: 개인 독서·여행 이야기] the Vegetarian, which is a good book. [[unclear: Maybe worth a Nobel Prize]], [공개본 개인정보 삭제: 개인 취미·현지 생활 이야기] I told you to jump the usual things.

42:45 화자 4
Do you think any of these hobbies help you out in your actual research for giving some kind of inspiration in some sense?

42:56 화자 1
I mean, only in the complicated sense of if you would have other things to do, especially from the sports and arts, in the sense of doing music or listening to music and also physical exercise, [[unclear: this balances you in a way that it replaces, if you don't have these things, you can work properly, anything]] If you want to think in this optimizing way, you need some kind of exchange between physical exercise that is completely detached from what you do and some kind of creative outlet that is also completely detached from what you normally do as a job to function, because otherwise you're just overloaded. So one thing that is kind of bad about, I don't know about your area in mind is that [[unclear: there is nothing that is required to do theoretical neuroscience]], you can do it at any point in the day and if you start studying it, that you will do it at any point in the day [[unclear: so you have to find]]

43:58 화자 4
Thank you.

44:01 화자 1
I have [[unclear: some friends facing theory]] and [공개본 개인정보 삭제: 지인의 개인 취미 이야기]. Thank you. [공개본 개인정보 삭제: 지인의 구체적 운동·시간 이야기], I think that I don't know why, but What they are saying is that they are using brains very intensely, so at some point they want to use their bodies intensely as well. [[unclear: If it says]], I'm not sure, but anyway, they often say that way in your case, [[unclear: you don't have that kind of copies ago]].

44:52 화자 1
Don't you do any sports, [공개본 개인정보 삭제: 개인 운동 생활], I mean, I think it's [공개본 개인정보 삭제: 특정 지인의 운동·나이·건강 관련 이야기] if you just Sit in the entire day and think that this is maybe not the best way to stay healthy and so I think of this level, [[unclear: a lot of applications I know just two sports]] to stay healthy [[unclear: so that doesn't really say another question check in the book.]]

45:37 화자 5
[[unclear: Most TCS conference recently mentioned also should write how they used AI]] so how do you think about [[unclear: whether they will give a penalty with She's too much there. Although the result is very difficult.]]

46:04 화자 1
[[unclear: I think quite understand all of the questions.]] 질문을 다시 한번은 한국말로 해볼래요?

46:10 화자 5
[[unclear: 최근에 TCS 컨퍼런스에서 AI를 어떻게 썼는지 적으라는 공지가 많이 올라왔는데]] AI를 조금 과도하게 썼을 경우에 결과와 상관없이 학회에서 페널티를 줄 가능성이 있다고 생각하시면 되나요?

46:29 화자 1
In some theory conferences there was announcement explicitly mentioned how you use AI in your paper and the question is, are they penalizing the use of AI in academic work? [[unclear: It's not the question I heard at all previously wait so never heard about in chance it's time no, no]], I mean, the question I previously understood was something along the lines of two I believe that papers will be rejected because it's too much AI use. [[unclear: And what will be yet]] that's probably what about penalization [[unclear: as I don't the use of AI, is it penalized at the point or penalized, I just noticed it.]]

47:26 화자 1
A very difficult question so in our area, [[unclear: if you look at archive. Which is where most of the papers in my area are published for frequent artists]], people are already very diligent. About declaring how they used AI, [[unclear: I had a paper that was had a page of overview]] like [[unclear: in this proof the AI tried to for this mamma, this proof tried this AI made a proof and the proof sucked so we rotate completely]] and here it actually gave a proof and it was way better than what we were doing. So [[unclear: people are very particular about authority]]. And I think it conferences this will if you do this, honestly, [[unclear: this will probably not affect too much]] I think there is a distinction between [[unclear: we use AIS in some parts of this paper]] and this paper is essentially just reported by us.

48:22 화자 1
But the result was found entirely by AI, I think we have conferences where this has happened, I think the Next major conferences where this will be very prominent because the big leap kind of or [[unclear: the most new results come from Astra and Astra was released just after the deadline for the last big conference]]. [[unclear: So the war will already some AI difference in the last few conference]], but it seems like [[unclear: mostly we were rejecting because AI and mostly AI]]. Let's see for the next conference, I think ultimately you will have to have some venue where these papers get published at some point, [[unclear: the ones that are entirely written by I will record if I cannot be some form of quality problem.]]
````
