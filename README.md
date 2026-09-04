# Pitcher Sequencing

I got the idea for this project while listening to the [Just Baseball Show](https://www.justbaseball.com/podcasts/). They were talking about Tyler Rogers and mentioned the idea that, because his delivery and pitches are so different from what hitters normally see, he might actually make the pitcher who comes in after him more effective. They also mentioned that it is a pretty difficult effect to actually quantify, so I figured I would give it a shot.

The basic question I am trying to answer is:

**Does the pitcher you face immediately before another pitcher have an effect on how well you perform against the second pitcher?**

Tyler Rogers is the obvious example because of his submarine delivery, but the goal is eventually to look at this more generally. For example, does going from a sidearm pitcher to an over-the-top pitcher make the second pitcher more difficult to hit? What about large changes in velocity, pitch movement, handedness, or pitch mix?

## General Plan

I am using pitch-level Statcast data from my [local Statcast database](https://github.com/mrmellors/statcast-database) and first organizing games into individual pitcher appearances. From there, I can identify which pitcher immediately preceded each pitcher in a game.

The first step is to compare a pitcher's performance when following a particular pitcher to their normal performance. I am currently using appearance-level xwOBA as the main performance measure.

So, at a high level, I am looking at something like:

```text
Pitcher A → Pitcher B
             ↓
    Pitcher B's xwOBA

compared with

Pitcher B's normal xwOBA
```

There are some obvious limitations to this first comparison. Most importantly, the hitters faced by the pitcher after Tyler Rogers may not actually be the same hitters who faced Rogers. Even if I find that pitchers perform better after Rogers, that alone would not mean that facing Rogers caused hitters to perform worse against the next pitcher. There are plenty of other factors that could be driving the difference.

For now, I mainly wanted to do the data wrangling needed to connect consecutive pitcher appearances and see if there are any interesting differences worth investigating further. If there does seem to be a signal, I can then narrow the analysis to hitters who actually faced both pitchers and do a better job of accounting for some of the other factors that could explain the difference.

From there, I also want to move beyond individual pitcher pairs and look at what makes two pitchers different from each other. Using characteristics like release point, velocity, movement, handedness, and pitch usage, I could look at whether certain transitions between different *types* of pitchers seem to be more effective.

The project is still a work in progress, so for now I am treating the initial results as exploratory rather than trying to make any causal claims. The eventual goal is to see whether there is actually something measurable behind the idea that giving hitters a drastically different look from one pitcher to the next can create an advantage.

