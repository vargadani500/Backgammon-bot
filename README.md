# Backgammon Bot

A Python-based Backgammon game featuring a playable graphical interface and some bots. You can play against the computer or simulate different bots battle each other.

## Features
* **Graphical Interface:** Built with pygame for interactive gameplay
* **Multiple AI Bots:** Ranging from random moves to a 2-ply Expectiminimax algorithm
* **Configurable Matches:** Easily set up Human vs. Bot, Bot vs. Bot, or Human vs. Human games
* **Headless Mode:** For bot vs. bot simulations and data gathering

## Prerequisites
This project requires Python 3 and the `pygame` library. Install the dependency using:
```bash
pip install pygame
```

## Configuration

You can customize the game rules and players by editing the `settings.py` file. 

| Setting                 | Description                                                                         | Options / Notes                                                     |
|:------------------------|:------------------------------------------------------------------------------------|:--------------------------------------------------------------------|
| `W_Player` / `B_Player` | Determines who controls White and Black.                                            | `"human"`, `"random_bot"`, `"greedy_bot"`, `"hard_bot"`, `"botond"` | | `True` (UI gameplay) or `False` (headless simulations)              |
| `chip_size`             | Base unit for rendering; scales the entire board and window size.                   | Integer (default: `50`)                                             |
| `fps`                   | The frame rate limit for the Pygame window.                                         | Integer (default: `60`)                                             |
| `summation`             | Defines how often the win/loss record is printed to the console.                    | Integer (default: `1`)                                              |

## Controls

* **Roll:** Click the "Roll" button
* **Moving:** Click and drag the chip to target position (invalid moves/turns are noted in the console)

## Test results

| Bots           | random_bot   | greedy_bot | hard_bot | botond |
|:---------------|:-------------|:-----------|:---------|:-------|
| **random_bot** | 100048:99952 | 988:12     | 99:1     | 98:2   |
| **greedy_bot** |              | 506:494    | 65:35    | 16:84  |
| **hard_bot**   |              |            | 49:51    | 13:87  |
| **botond**     |              |            |          | 49:51  |
