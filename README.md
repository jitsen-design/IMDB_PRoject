#### Predicting Movie Worldwide Gross Income

This model aims to predict cumulative worldwide income of a motion picture that is predicated on a theme of 'drama'. The accompanying notebook attempts to predict movie income based on the following cirteria:

What was the budget of the movie?
What was its IMDB rating?
Did it have a Best Director Nomination?
Did it have a Best Actor nomination?
Did it have a Best Actress nomination?
What was its genre?
What was its runtime?


This project was a linear regression task, and I used both the SK-Learn and Stats Models libraries. I then engineered interaction terms and refined the predictive model. The model reached an R^2 of 0.64, but runtime and many of the iteraction terms failed to add value.

In conclusion, we would most likely keep all features for our prediction, barring 'director status'as well as the 'romance', 'thriller' and 'crime' genres.

![Slides](https://github.com/jitsen-design/IMDB_Project/blob/master/Data_Science_Meets_Hollywood.pdf)



