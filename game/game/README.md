# A Simple 2D Survival Game

## Project Overview

This is a simple 2D survival game made using Processing Python Mode.

The player controls a blue circle and avoids falling red blocks. The goal is to survive for as long as possible. The score increases with survival time, and the difficulty increases every ten seconds, up to level eight.

## Software Requirements

- Processing with Python Mode installed.
- A keyboard with arrow keys.

The game uses built-in shapes and drawing functions. No external images, sounds or additional libraries are required.

The project must be opened in Processing Python Mode. It is not designed to run directly in a standard Python editor.

## Project Files

- `game.pyde`: The complete game code, including comments explaining its functions.
- `README.md`: The project description and instructions.

Keep `game.pyde` inside the folder named `game`.

## How to Run

1. Download the complete project folder. If downloaded as a ZIP file, extract it first.
2. Open Processing.
3. Select Python Mode.
4. Open `game.pyde` from the `game` folder.
5. Click the Run button.
6. Click inside the game window if needed to give it keyboard focus.
7. Press Space to start playing.

## Controls

| Key | Action |
| --- | --- |
| Left arrow | Move left |
| Right arrow | Move right |
| Up arrow | Move up |
| Down arrow | Move down |
| Space | Start from the opening screen |
| R | Restart after game over |

Hold two arrow keys to move diagonally.

## Main Features

### Player Movement

The player can move horizontally, vertically and diagonally. Diagonal movement is adjusted to keep its speed consistent with movement in one direction.

The player cannot move outside the play area or into the score bar.

### Falling Blocks

Red blocks appear at random horizontal positions above the screen. Each block has its own size and falling speed.

Blocks are removed after they leave the bottom of the screen.

### Increasing Difficulty

The difficulty increases every ten seconds, up to level eight.

At higher levels, blocks fall faster and appear more frequently.

### Collision Detection

The game finds the point on each block nearest to the centre of the player.

If the distance between this point and the player centre is equal to or smaller than the player's radius, a collision is detected and the round ends.

### Score and Best Score

The score shows survival time in whole seconds.

The best score is updated when a round ends. It is kept between rounds while the program remains open, but it resets when the program closes.

### Game Screens

The game includes a start screen, a gameplay screen and a game-over screen.

After game over, pressing R resets the player, obstacles and timers for a new round.

## Code Structure

- `setup()`: Creates the game window and initial settings.
- `start_game()`: Resets the variables and starts a new round.
- `draw()`: Runs the main loop and displays the current screen.
- `draw_background()`: Draws the background grid.
- `draw_start_screen()`: Displays the title and instructions.
- `update_game(dt)`: Updates movement, timing, difficulty and obstacles.
- `touches_player(block)`: Checks whether a block touches the player.
- `draw_game()`: Draws the player, obstacles and score bar.
- `draw_end_screen()`: Displays the final score and restart instruction.
- `keyPressed()`: Records movement input and handles starting or restarting.
- `keyReleased()`: Removes released keys from the movement input.

## Known Limitations

- The best score is not saved after closing the program.
- The game does not automatically pause when the window loses focus.
- Random block positions can make some situations harder than others.

## Assets and Dependencies

All game visuals are drawn using Processing's built-in functions.

No external image files, sound files or additional libraries are used.