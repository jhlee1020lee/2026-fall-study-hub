---
course: "computer_programming"
source_pdf: "Lab03.v2.pdf"
pdf_page: 25
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab03.v2.pdf"
generated_at: "2026-09-19T10:20:37Z"
---
Problem 1-2 : Create the Fight Class
● Methods of the Fight Class :
  ● public void proceed()
     ● Print the current round number, starting with 1, in the following format :
                 Round <Round_Number>
     ● Proceed one round. Run the players’ actions starting from player 1. Use getTactic() for
               each user and execute the corresponding actions. If player 2’s health reaches zero
               because of an attack by player 1, player 2 should not execute any action. (We will be
               assuming that during each round, player 1 takes action, then, player 2 takes action.)
          ●    Print the health of the two players in the following format :
                        <Player1_userID> health : <Player1_health>
                        <Player2_userID> health : <Player2_health>
     ● public Boolean isFinished()
       ● Return true if the fight is over. Otherwise, return false.
       ● The fight ends when one loses all of his/her health points, or if the final round ends.
     ● public Player getWinner()
       ● Return the winner of the fight.
       ● The player with more health points wins the fight. If the two players have the same health
               points, player 2 wins since player 1 takes action first.                                25
