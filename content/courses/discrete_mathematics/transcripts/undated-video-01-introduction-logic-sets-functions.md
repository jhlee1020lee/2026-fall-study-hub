---
title: "01. Introduction (Logic, Sets, Functions, ...) · 보정 STT · 날짜 미확인"
course: "discrete_mathematics"
term: "2026_Fall"
tags: ["lecture-transcript"]
source_kind: "corrected_transcript"
privacy_redacted: true
verbatim_complete: false
audio_verified: false
date_confidence: "unknown"
lecture_date: null
source_mode: "text_only_practical"
source_text_sha256: "7ea06bf3f6ff3582ed5f9c661dbfbb5ac301aa3bee243eac15024d4e16c35df3"
corrected_text_sha256: "36e07fc35898e616a63595da171b70ccfdfe97cd56aeafd3adcfcfdf82b39bdb"
source_video_number: "01"
cssclasses: ["plain-document"]
---

수업 날짜는 미확인이고, 영상 번호는 PDF 번호와 다르다. 원음 없이 대조한 텍스트로, 불확실한 표현은 `[[unclear: …]]`로 남겼다. 영상 속 시험·운영 안내는 이번 학기 공식 공지로 확인된 내용이 아니다.

````text
00:01 화자 1
네 그래서 [[unclear: 원문 Discrete mass; Discrete Math 문맥]]와 CS가 이제 밀접한 관련이 있다라고 말씀을 드렸고요. 이제 책에서 다루고 있는 토픽들을 보면은 로직도 있고 Set Theory도 있고 Graph Theory, Number Theory, Combinatorics 이런 여러 가지 수학적인 주제들이 등장을 하게 될 겁니다. 그런데 이거를 저희가 그냥 단순히 purely mathematical한 시선에서 바라보는 게 아니라 컴퓨터 사이언스의 관점에서 이런 주제들을 바라보고 이제 어플리케이션도 바라보고 그럴 예정입니다. 이건 아까 말씀드렸고 그래서 이제 첫날이라 수업을 하고 싶지가 않은데 제 경험상 제가 어쩔 수 없이 뭐 출장이나 이런 것 때문에 그 휴강을 하게 되는 경우가 있더라고요. 그러다가 이제 진도가 밀려가지고 지난 학기에 약간 학기 말에 업보청산을 당한 적이 있어가지고 오늘은 첫날이지만 수업을 그래도 조금만 나가겠습니다. 여러분.

01:01 화자 1
이번에 텍스트북을 보시면 챕터1에 Logic and Proof라는 챕터가 나와요. 그다음에 이제 챕터 2를 보시면 여기 Basic Structure 하면서 Set functions, Sequence 등등 이런 것들이 나옵니다. 이거 둘은 제가 슬라이드를 준비를 하기는 했는데 제대로 수업을 안 할 거예요. 그냥 읽어보시면 됩니다. 그러니까 제 생각에 여기 앉아계신 90%의 수강생분들은 이미 모르는 내용이 거의 없거나 아니면 그냥 노테이션 정도만 다시 한번 리캡하는 되는 수준이라고 생각을 하는데 어쨌든 오늘은 그냥 쭉쭉 넘기면서 한번 같이 볼게요. 여기서 만약에 잘 모르는 게 있다 하면 시간을 조금 더 들여서 보시면 됩니다. 자 먼저 이제 Chapter 1이 [[unclear: 원문 Logic M Proof; Logic and Proof 문맥]]가 나오는데 저희는 기본적으로 Binary Space에서 많은 걸 다루죠.

01:55 화자 1
그래가지고 0과 1로 이루어진 Binary Space [[unclear: 원문 True out, false; True or False 문맥]]로 얘기를 하기도 하고 yes or no로 얘기를 하기도 하고 binary로 쓸 때는 보통 1과 0으로 표현을 합니다. 그래서 이제 사실상 이 로지컬한 스페이스랑 그다음에 저희가 이제 [[unclear: 원문 G2; 0과 1을 모은 공간의 기호]]라고 얘기하는 0, 1 이 두 개를 모아놓은 게 사실상 그냥 아이덴티컬한 스페이스로 생각을 하는 거죠. [[unclear: 원문 트램 펄스; True/False 문맥]]. 그다음에 이제 이런 [[unclear: 원문 트램 펄스; True/False 문맥]] 같은 로지컬한 결과나 아니면 [[unclear: 원문 1년 밑; 1/0 bit 표현 관련]]으로 생각하셔도 되고요. 그것들에 대해서 여러 가지 오퍼레이션을 할 수가 있습니다. 그래서 예를 들면은 negation은 여기에다가 True의 negation을 걸면 false가 나오고 conjunction은 AND라고 보시면 되고 이거는 or라고 보시면 되고요.

02:53 화자 1
그다음에 implication은 p이면 q이다. 할 때 나오는 그 implication 이제 이제 그 예를 들면은 트루이면 트루 이렇게 4개를 봤어요. False이면 false 이거 4개를 봤을 때 얘는 true고 얘만 false고 얘는 다 true 이거를 이제 저희가 implication이라고 얘기를 하죠. 그래서 이런 operation도 있고요. 그다음에 이거는 이제 서로 equivalent 할 때 biconditional relation도 있습니다. 그런데 이것들을 저희가 이제 true, false 이렇게 보기도 하는데 이 챕터의 제일 뒤쪽이 거의 되게 뒤쪽에 챕터 12였나? 거기 이제 Boolean algebra라는 개념이 나와요.

03:45 화자 1
이제 거기서 이제 Boolean algebra라는 개념이 뭐냐면은 저희가 앞에서는 이제 true와 false 사이에서 여러 가지 operation들을 정의를 했잖아요. 이런 저런 operation들을 정의를 하는데 이 boolean algebra라는 거는 over 아까 제가 [[unclear: 원문 g2; 기호 미확인]]라고 쓰기도 했는데 보통 F₂라고 쓰기도 합니다. 0과 1사이에서 약간 모듈러 오퍼레이션처럼 쓸 수 있는데, 이거를 이제 [[unclear: 원문 불리한 엑소라; Boolean algebra 또는 XOR 관련 표현 미확정]]라고 표현을 하거든요. 그래서 만약에 저희가 true와 false를 1과 0이라고 표현을 하면 이 and라는 오퍼레이션은 사실 곱하기랑 사실상 똑같아요.

04:30 화자 1
왜냐하면, 둘 다 이 and라는 operation은 둘 다 true면 true고 나머지 경우에는 false이기 때문에 이거를 이제 mod 2 같은 느낌으로 생각을 했을 때 1 곱하기 1을 하면 1이 나오고 1 곱하기 0을 하면 0이 나오는 약간 이런 것처럼 이게 곱하기에 해당을 합니다. 이쪽으로는 그다음에 이제 or 같은 같은 경우 OR 말고 이제 XOR라는 게 있는데, XOR가 뭐냐면 이제 여기에 저희가 쓰는 XOR라는 오퍼레이션도 있는데, XOR라는 오퍼레이션이 뭐냐면 약간 이런 mod 2에서 더하기처럼 약간 이런 것들을 이제 XOR operation이라고 해요.

05:15 화자 1
그래가지고 true or false logical한 스페이스에서 저희가 뭔가 conjunction, disjunction 혹은 and or 이런 식으로 말하는 logical operation들이 사실 0과 1로 이루어진 binary field 그러니까 이런 이거를 수학에서는 Boolean algebra라고 하기도 하는데 여기서 일종의 arithmetic operation처럼 쓸 수도 있거든요. 그래가지고 이런 notation이나 이런 notation이나 사실상 equivalent 합니다. 그래가지고 여러분이 선호하시는 notation을 사용을 하시면 되는 거고요. 그다음에 negation 같은 경우는 예를 들면 위에서는 이렇게 쓰는 거를 이 밑에서는 a+1로 쓰면 돼요.

05:58 화자 1
그러면 logical한 operation에서는 true가 false가 되고 [[unclear: 원문 fresh가; False 문맥]] true가 되는데 여기서는 1과 xor를 하면 0이 1이 되고 이런 식으로 이제 logical operation을 다 arithmetic한 operation으로 바꿀 수 있는데, 이런 [[unclear: 원문 rotation; notation 문맥]]은 제가 앞으로 혼용을 해서 쓸 것 같습니다. 약간은 그다음에 이제 quantifier 이런 기호들 아마 처음 보시는 분들도 약간 있을 수 있다고 생각하는데 이거는 이제 저희가 어떤 proposition 같은 거를 쓸 때 이런 식으로 쓰면 모든 x에 대해서 p of x가 사실이다. 약간 이런 [[unclear: 원문 existent quantifier; 직전 모든 x 설명에는 universal이 맞음]]를 얘기를 하는 거고, 이거는 이제 universal quantifier를 얘기하는 거고, 예를 들면 저희가 이런 식으로 쓸 때는 Q of A를 만족하는 A라는 element가 존재한다. 이런 존재성에 대해서 얘기를 할 때는 이런 [[unclear: 원문 rotation; notation 문맥]]을 씁니다.

06:54 화자 1
그리고 네, 네 이거는 proposition이 뭔지 proposition이라는 proposition이란 False나 True로 판별할 수 있는 이런 것들이 proposition이다. 그래서 제가 앞에서 몇 가지 logical한 operation 보여드렸는데 여기 디테일한 definition이 있어요. negation이나 AND나 OR 이런 것들이 있다. 그다음에 implication도 있고 그다음에 biconditional statement도 있다. 쭉쭉 보시면 됩니다. 그다음에 quantifier에 대해서도 여기 formal한 definition을 넣어놨습니다. 그래서 이제 쭉쭉 보시면 되는 거고, 그다음에 1장에서 나오는 테크닉 중에 하나가 우리말로 귀류법, proof by contradiction이라는 게 나오는데 proof technique 중에 어떤 statement가 false라는 것을 보이기 위해서는 true라고 가정을 한 다음에 뭔가 [[unclear: 원문 모션; 모순 추정]]을 찾는 방법을 귀류법이라고 얘기한다.

07:53 화자 1
그래서 여기에서 뭐 textbook에서 나온 example 중에 하나 하나가 square root 2가 irrational하다는 거를 보일 때 이거를 쓸 수 있다. rational이라고 가정을 하면 p분의 q로 표현이 되는데 넘기고 넘기고 하면서 하면 안 된다는 거를 보일 수 있다. 이런 얘기가 있고요. 이게 1장 끝입니다. 그래가지고 별 내용 없죠. 제가 이거를 이런 정도로 넘기는 이유는 제가 맨 처음 첫 해에 이산수학을 강의를 했을 때 정말 아무것도 모르고 학교에 오자마자 슬라이드에 있는 대로 그대로 갔는데 이렇게 하니까 챕터 원에 2주를 쓰게 되더라고요. 그래가지고 이제 아 이건 진짜 아니다. 싶어가지고 이제 빨리빨리 넘기고 있는 거고요. 그다음에 챕터2는 여러 가지 mathematical object에 대해서 나와요. 처음에는 집합에 대해서 나오고 그다음에 function에 대해서 나오고 sequence에 대해서 나옵니다.

08:47 화자 1
집합은 뭔지 다 아실 거라고 생각을 하고 여러 가지 집합에 대한 [[unclear: 원문 rotation; notation 문맥]]이나 집합에 대한 operation 그리고 여러 가지 형식들이 있습니다. 그다음에 function도 뭔지 다 아실 거고, function 중에서 약간 특이한 성질들을 가지는 것들을 저희가 injective one to one function onto function [[unclear: 원문 by section; bijection 문맥]] 이런 식의 이름들을 붙여서 붙일 때가 있고요. 그다음에 sequence에 대해서도 특수한 sequence들이 있죠. 예를 들면은 arithmetic progression 이게 뭐였죠? 등차수열, 등비수열 이런 것들이 있고 그다음에 시리즈나 아니면 리커런스로 정의된 시퀀스 이런 것들이 등장을 합니다.

09:31 화자 1
그래서 이제 집합론의 역사에 대해서 말하자면, 사실 이것만으로 몇 시간을 썰을 풀 수 있을 정도로 집합이 사실상 인류를 굉장히 괴롭혔던 오브젝트 중에 하나인데 저희는 그런 것까지는 필요 없고 집합은 그냥 어떤 오브젝트들의 모임이죠. 보통은 저희가 집합을 다룰 때 context에 따라서 universal set이 있고 그 안에 empty set이 있고 벤다이어그램으로 표현을 하고 이런 것들이 있습니다. 그리고 이 책에 러셀의 패러독스라는 것도 등장을 하는데 이게 이제 제가 아까 말했던 인류를 굉장히 괴롭혔던 주제 중의 하나라고 말씀을 드렸는데 집합이 수학에서 집합이 무엇인가를 포멀하게 정립하는 데 생각보다 오랜 시간이 걸렸거든요. 그게 인류가 수학적으로 집합론을 제대로 정립한 게 몇백 년 안 됐어요.

10:27 화자 1
그래 가지고 이제 러셀의 퀘스천도 이제 어떻게 보면 [[unclear: 원문 재판론이; 집합론 문맥]] 잘 [[unclear: 원문 적립; 정립 추정]]되기 전에 나왔던 질문 중에 하나인데 물론 이제 이런 것들이 집합론을 잘 정립된 그 뒤에 공부를 할 수 있게 해주는 어떤 좋은 [[unclear: 원문 프리핑 스톤; stepping stone 추정]]이 되죠. 그래서 예를 들면 여기 나오는 패러독스 중의 하나가 S가 모든 집합의 집합일 때 S가 S를 이런 식으로 정의를 하면 모든 집합의 집합이라고 할 때 만약에 그 S라는 집합이 S 자체에 들어가냐 혹은 아니냐 이것 자체를 어떤 식으로 하더라도 determine 안 되는 paradox가 생긴다. 약간 이런 유명한 paradox가 있거든요.

11:18 화자 1
왜냐면은 얘가 s가 이제 정확히는 모든 집합 중에서 U가 U에 속하지 않는 약간 이런 집합들의 집합이라고 정의를 했을 때 S가 S에 속한다고 하면은 S가 여기에 속하니까 S가 S에 속하면 안 돼서 모순이고 S가 S에 속하지 않는다고 하면은 이게 또 반대로 성립하면 안 되니까. S가 S에 속해야 돼서 안 돼서 이런 모순이 생기는 건데 여기서 사실 이 패러독스가 생기는 이유는 저희의 관심사를 벗어나는 거기는 하지만 애초에 이거 자체가 집합이 아니라서 그래요. 그러니까 이게 자기 자신의 멤버 아닌 집합들을 다 모아놓으면 집합이 아닌 게 됩니다. 집합보다 더 큰 무언가가 돼요. 그래서 이제 이런 모순이 생긴 이 모순이 사실 모순이 아니게 되는 건데 이런 것들은 저희는 상관없이 그냥 저희가 익숙한 스페이스들에서 볼 겁니다.

12:17 화자 1
여러 가지 익숙한 집합들이 있고 그다음에 서브셋 개념 그다음에 이제 cardinality set이 finite일 때 원소의 개수를 cardinality라고 하고 그다음에 이제 물론 이제 원소의 개수가 무한히 [[unclear: 원문 맞는; 많은 추정]] 그거를 이제 infinite이라고 하고요. 그런데 이제 infinite set이 다 똑같은 infinite set이 아닌 게 infinite set 중에 이제 정수 혹은 이제 자연수 [[unclear: 원문 지갑과; 집합 문맥]] 동일한 cardinality를 가지고 있는 [[unclear: 원문 지갑들을; 집합 문맥]] 저희가 countable이라고 합니다. 이 countable이라고 하는 것은 이 단어가 가지고 있는 말 그대로 이제 집합에 있는 집합이 [[unclear: 원문 유핀이 셋; 문맥상 infinite set 추정]]이지만 집합을 원소들에다가 이렇게 넘버링을 해가지고 모든 element를 빠지지 않고 이렇게 한 번씩 다 지나갈 수 있으면 이제 그거를 countable 셋이라고 하고 그런 cardinality를 가진 거를 이제 이런 aleph zero, aleph null이라는 notation으로 표현을 합니다.

13:14 화자 1
그래서 이거는 infinite set인데 countable인 거는 이런 [[unclear: 원문 로테이션; notation 문맥]]을 쓴다라는 얘기가 있고요. [[unclear: 원문 무한 비판; 무한집합 추정]] 중에서 리얼 넘버 같은 거는 countable하지 않다라는 얘기를 증명을 할 수가 있습니다. 이것도 되게 유명한 리얼 넘버가 이제 countable하지 않다는 것을 보여주는 유명한 논리 중에 하나인데 이것도 이제 귀류법을 써가지고 countable하다고 가정을 한 다음에 이제 countable하면 모든 element가 이렇게 리스팅이 돼야 되는데 그러면 이 리스트에 없는 것을 찾을 수 있다. 약간 이런 식으로 그다음에 이제 countably infinite set에 대해서 여러 가지 약간 직관적인 설명을 듣고자 책에 이제 이런 힐버트의 그랜드 호텔이라는 [[unclear: 원문 이그장들도; examples 추정]] 나와요. 그래가지고 만약에 그냥 상상 게임인 거죠.

14:10 화자 1
만약에 countably many room을 가지고 있는 호텔이 있으면 이때 만약에 모든 룸이 occupied 되어 있을 때 새 게스트가 왔을 때 이 게스트를 [[unclear: 원문 지을 수; 재울 수 추정]] 있느냐 이게 이게 [[unclear: 원문 파이나이시드는; finite 문맥]] 당연히 [[unclear: 원문 지을 수가; 재울 수가 추정]] 없는데 이런 Countable infinite set인 경우에는 이게 가능하다. 가능한 방법은 이제 모든 게스트를 다음 룸으로 밀면 된다. 약간 이런 얘기가 있습니다. 그래서 이거에 조금 더 다양한 버전들이 있어요. 예를 들면 그랜드 호텔 두 개가 있으면 그 두 개를 하나로 합칠 수 있느냐 그러면 이제 뭐 홀짝 방에 넣는다 뭐 약간 이런 것들도 있고요. 그 다음에 뭐 그랜드 호텔 있는데, 방마다 [[unclear: 원문 브랜드 호텔; 그랜드 호텔 문맥]]이 하나씩 들어가 있을 때 그걸 다시 [[unclear: 원문 브랜드 호텔; 그랜드 호텔 문맥]]에 넣을 수 있는 약간 이런 것도 있고 이거를 여러 레이어로 생각을 할 수가 있는데, 이런 것들에 대한 example이 궁금하신 분은 책을 좀 보시면 될 것 같고요.

15:09 화자 1
그다음에 두 집합이 있을 때 Cartesian product라는 [[unclear: 원문 로테이션; notation 문맥]]도 정의를 하고 이거는 그냥 두 집합의 pair들을 모아놓은 집합이고요. 그다음에 이제 여러 가지 set operation이 나오는데 set union도 나오고 set intersection도 나오고 그다음에 intersection이 empty인 경우는 이제 저희가 disjoint set이라고 얘기를 하고요. 그다음에 complement라는 개념도 나옵니다. 그다음에 마지막으로, difference라는 operation도 나오고요. 이런저런 operation들이 쭉 나오고 마지막으로, 이 operation들과 관련해서 여러 가지 기본적인 identity들을 모아놓은 테이블이 나옵니다. 여기까지 별거 없죠. 그다음에 Function, function이 뭐냐 다 아실 거라고 생각하고 function에 대한 definition이 하나 있고요. function은 이제 저희가 map이나 transform 이런 다른 이름으로 부르기도 합니다.

16:06 화자 1
그래서 이제 domain이 뭐냐, codomain이 뭐냐, image가 뭐냐, preimage가 뭐냐, range image 이런 단어들이 있고요. 그다음에 이제 어떤 function이 [[unclear: 원문 원턴; one-to-one 문맥]]이다. 혹은 이제 injective하다라고 하는 건 뭐냐면은 서로 다른 element가 서로 다른 element로 대응되면 그러니까 한마디로 이런 collision이 발생하지 않으면 [[unclear: 원문 onto function; 정의상 one-to-one function]]이라고 얘기를 합니다. 그다음에 onto function은 [[unclear: 원문 susceptive function; surjective function 문맥]]은 이제 [[unclear: 원문 onton; one-to-one 추정]]일 필요는 없고 여기 모든 codomain이 있는 원소가 적어도 하나 이상의 element에 대응되면 적어도 하나 이상의 element의 image가 되면 얘를 이제 onto라고 하고요. 이제 bijection은 injective이면서 surjective입니다. one-to-one이면서 onto가 둘 다 되는 것들을 이제 저희는 bijective라고 얘기를 하고 [[unclear: 원문 원통 correspondence; one-to-one correspondence 문맥]]라고 얘기하기도 합니다.

17:02 화자 1
이제 F가 bijection인 경우에는 이제 inverse function이라는 것을 정의를 할 수 있는데, 그리고 오직 이때만 정의를 할 수 있는데, 왜 그러냐면 이제 임의의 codomain 상에 b를 잡더라도 b가 f of a가 되는 a가 유니크하게 존재하기 때문에 이 element b를 그 preimage a로 보내주는 function을 저희가 정의를 할 수가 있어서 그거를 이제 f의 inverse function이라고 얘기를 하고 notation은 f inverse로 쓴다. 그리고 이제 두 함수가 있을 때 a에서 b로 가는 함수와 b에서 c로 가는 함수가 있을 때 그 2개를 합성할 수 있다. 그 합성하는 거를 이제 저희는 composition이라고 얘기를 하고 definition은 저렇게 된다. 거라서 재미가 없죠. 그리고 이제 시퀀스도 나오고 무슨 여러 가지 [[unclear: 원문 바리시네틱; arithmetic 문맥]], geometric 이 progression, 그다음에 이제 어떤 recurrence relation 같은 방식으로 정의된 시퀀스도 나옵니다.

18:02 화자 1
그리고 서메이션이라든가 여러 가지 등차수열, [[unclear: 원문 준비수열의; 등비수열 문맥]] 서메이션 [[unclear: 원문 부분 확보하는 법; 부분합 구하는 법 추정]] 그다음에 조금 더 어려운 버전들의 여러 가지 formula들 이런 것들 모르셔도 돼요. 모르셔도 되는데 그냥 이런 것들이 있다. 여기까지가 이제 챕터1 2입니다. 오늘 첫날 챕터 2개를 했네요. 그러면은 이제 다음
````
