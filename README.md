# Backgammon Bot

A Python-based Backgammon game with graphical interface made with pygame and some bots. You can play against the computer or simulate different bots battle each other.
This was made for a university project and doubling dice is not implemented.

## Prerequisites
This project requires Python 3 and the `pygame` library. Install the dependency using:
```bash
pip install pygame
```

## Configuration

You can customize the game rules and players by editing the `settings.py` file. 

| Setting                 | Description                                                       | Options / Notes                                                      |
|:------------------------|:------------------------------------------------------------------|:---------------------------------------------------------------------|
| `W_Player` / `B_Player` | Determines who controls White and Black.                          | `"human"`, `"random_bot"`, `"greedy_bot"`, `"hard_bot"`, `"botond"`  |
| `starter`               | Determines who starts                                             | Integer (default: `1`)<br/>(0 for random, 1 for white, -1 for black) |
| `chip_size`             | Base unit for rendering; scales the entire board and window size. | Integer (default: `50`)                                              |
| `fps`                   | The frame rate limit for the Pygame window.                       | Integer (default: `60`)                                              |
| `summation`             | Defines how often the win/loss record is printed to the console.  | Integer (default: `1`)                                               |

## Controls

* **Rolling:** Click the "Roll" button
* **Moving:** Click on the row where you want to move from and then click where you want to move to  (invalid moves/turns are noted in the console)

## Test results
the second has starter advantage for these

| Bots           | random_bot   | greedy_bot    | hard_bot | botond |
|:---------------|:-------------|:--------------|:---------|:-------|
| **random_bot** | 48584:51416  | 9850:150      | 1000:0   | 98:2   |
| **greedy_bot** |              | 487126:512874 | 696:304  | 16:84  |
| **hard_bot**   |              |               | 474:526  | 14:86  |
| **botond**     |              |               |          | 49:51  |

