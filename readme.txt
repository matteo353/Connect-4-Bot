Matteo Mastandrea
Matteo Jr

My evaluation function takes the current amount streaks that are 2 or larger and gets the score of a streak that's one
bigger than divides it in half. My thinking was that there's about a 50% chance that this streak will be completed,
so we would take the expected value based on a 50% success rate of completing the streak.

My thoughts behind the first test were that in that situation the correct minimax move would be to move to column 1.
My thoughts behind the second test is that minimax should move to column 2.
My thoughts behind third test were that if there are 2 spots left and one will add points to the bots score, then it
should choose the profitable one.

https://www.youtube.com/watch?v=l-hh51ncgDI&t=323s
I consulted this youtube video. It's actually a really good resource for visualizing the algorithm. It also goes over
alpha beta pruning in a really clear and concise way.

Based on the amount of states that are generated between the three algorithms it seems like everything works like it
is supposed to. Also based on the tests I ran the algorithm seems to be running correctly.