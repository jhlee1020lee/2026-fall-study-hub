---
course: "computer_programming"
source_pdf: "Lab03.v2.pdf"
pdf_page: 21
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_programming/Lab03.v2.pdf"
generated_at: "2026-09-19T10:20:37Z"
---
Problem 1-1 : Create the Player Class
● Methods of the Player Class :
  ● public void attack (Player opponent)
     ● Decrease the opponent’s health points by an integer selected from [1,5] at random.
     ● Note that the health points of a player must be non-negative.
     ● Hint : Use random.nextInt()
  ● private void getDamaged(int damage)
     ● Decrease the player’s health points by the amount specified by the damage integer.
  ● public void heal()
     ● Increase the player’s health points by an integer selected from [1,3] at random.
     ● The health points of each player should not exceed the initial value of 50.
  ● public Boolean isAlive()
     ● Return true if the player’s health is higher than zero. Otherwise, return false.
  ● public char getTactic()
     ● Decide whether to attack or heal. The player should decided to attack with a chance of
         70% and to heal with a chance of 30%.
     ● If a player decides to attack, return the character ‘a’. Otherwise, return the character ‘h’.
     ● Hint : Use random.nextFloat()                                                                   21
