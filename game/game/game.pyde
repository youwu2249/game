# A Simple 2D Survival Game
# Environment: Processing Python Mode.
# Purpose: Move the player to avoid falling blocks and survive.
# All visuals use Processing shapes, so external assets are unnecessary.
player_x = 300.0  # Stores the player's horizontal position; starts near the centre.
player_y = 420.0  # Stores the player's vertical position; starts near the bottom.
player_radius = 16  # Defines the player's radius for drawing, boundaries and collisions.
player_speed = 280.0  # Sets movement speed in pixels per second for time-based movement.
obstacles = []  # Stores active falling blocks so they can be updated and drawn.
held_keys = set()  # Stores pressed keys without duplicates to support continuous movement.
state = "start"  # Tracks the current screen so the game begins with instructions.
survival_time = 0.0  # Tracks time survived; this becomes the player's score.
spawn_timer = 0.0  # Tracks time since spawning a block to control obstacle frequency.
last_time = 0  # Stores the previous frame's time to calculate elapsed time.
best_score = 0  # Stores the highest score during this run; it resets when the program closes.
def setup():  # Runs once to prepare the game window and initial settings.
    global last_time  # Allows this function to update the shared timing variable.
    size(600, 500)  # Creates a 600-by-500-pixel window for the game.
    frameRate(60)  # Requests 60 frames per second for smooth animation.
    noStroke()  # Removes shape outlines to give the game a simple visual style.
    last_time = millis()  # Records the starting time to initialise frame timing.
def start_game():  # Resets a round so the same function can start or restart play.
    global player_x, player_y, obstacles  # Allows the shared player position and obstacle list to be reset.
    global state, survival_time, spawn_timer, last_time  # Allows the shared game state and timers to be reset.
    player_x = width / 2.0  # Centres the player horizontally for a consistent starting position.
    player_y = height - 80.0  # Places the player near the bottom, below incoming blocks.
    obstacles = []  # Removes previous blocks so each round starts with a clear screen.
    held_keys.clear()  # Removes old key inputs to prevent unwanted movement after restarting.
    survival_time = 0.0  # Resets the score because a new round is beginning.
    spawn_timer = 0.0  # Resets the spawning timer to give each round the same initial delay.
    last_time = millis()  # Resets frame timing so time spent on other screens is excluded.
    state = "play"  # Switches to active gameplay after the reset is complete.
def draw():  # Runs repeatedly to update the game and display the current screen.
    global last_time  # Allows the previous frame's time to be updated.
    now = millis()  # Reads the current elapsed time in milliseconds.
    dt = min((now - last_time) / 1000.0, 0.05)  # Converts frame time to seconds and caps large movement jumps.
    last_time = now  # Saves the current time for the next frame's calculation.
    if not focused:  # Checks whether the game window has lost keyboard focus.
        held_keys.clear()  # Clears inputs so movement does not remain stuck after switching windows.
    background(20, 26, 42)  # Clears the previous frame with a dark background to prevent visual trails.
    draw_background()  # Draws the grid to provide a consistent background.
    if state == "start":  # Checks whether the player is on the opening screen.
        draw_start_screen()  # Shows instructions before gameplay begins.
    elif state == "play":  # Checks whether a round is currently active.
        update_game(dt)  # Updates movement, difficulty, obstacles and collisions using elapsed time.
        draw_game()  # Displays the updated player, obstacles and score.
        if state == "over":  # Checks whether a collision ended the round during this update.
            draw_end_screen()  # Shows the game-over overlay immediately after the collision.
    elif state == "over":  # Handles frames after the round has ended.
        draw_game()  # Displays the final game scene without updating its movement.
        draw_end_screen()  # Displays the score and restart instruction over the scene.
def draw_background():  # Keeps background drawing separate to make the main loop easier to read.
    stroke(32, 41, 60)  # Enables subtle outlines so the grid lines are visible.
    for x in range(0, width, 40):  # Selects horizontal positions at 40-pixel intervals.
        line(x, 0, x, height)  # Draws a vertical grid line at each selected position.
    for y in range(0, height, 40):  # Selects vertical positions at 40-pixel intervals.
        line(0, y, width, y)  # Draws a horizontal grid line at each selected position.
    noStroke()  # Disables outlines again so later shapes retain their intended appearance.
def draw_start_screen():  # Displays the title and controls to explain the game before play.
    textAlign(CENTER, CENTER)  # Centres text around its coordinates for a balanced layout.
    fill(80, 200, 255)  # Selects blue to visually connect the title with the player.
    textSize(32)  # Makes the title larger than the instructions.
    text("2D SURVIVAL GAME", width / 2, 140)  # Displays the game title in the horizontal centre.
    fill(235)  # Selects light grey so instructions contrast with the background.
    textSize(19)  # Uses a smaller readable size for the instructions.
    text("Use arrow keys to move", width / 2, 220)  # Explains how to control the player.
    text("Avoid the falling red blocks", width / 2, 255)  # Explains which objects are dangerous.
    text("Survive longer to score more", width / 2, 290)  # Explains the scoring objective.
    fill(255, 210, 100)  # Highlights the start instruction in yellow.
    textSize(23)  # Makes the start instruction stand out from the other instructions.
    text("Press SPACE to start", width / 2, 365)  # Tells the player how to begin.
def update_game(dt):  # Updates gameplay separately from drawing to organise the program.
    global player_x, player_y  # Allows movement to change the shared player position.
    global survival_time, spawn_timer  # Allows elapsed time to update the shared timers.
    global state, best_score  # Allows a collision to end play and update the highest score.
    dx = 0  # Resets horizontal direction each frame so movement reflects current input.
    dy = 0  # Resets vertical direction each frame so movement reflects current input.
    if LEFT in held_keys:  # Checks whether the left arrow is being held.
        dx -= 1  # Requests movement towards the left.
    if RIGHT in held_keys:  # Checks whether the right arrow is being held.
        dx += 1  # Requests movement towards the right; opposite inputs cancel each other.
    if UP in held_keys:  # Checks whether the up arrow is being held.
        dy -= 1  # Requests upward movement because screen coordinates decrease upwards.
    if DOWN in held_keys:  # Checks whether the down arrow is being held.
        dy += 1  # Requests downward movement because screen coordinates increase downwards.
    if dx != 0 or dy != 0:  # Only calculates movement when a direction exists, avoiding division by zero.
        distance = sqrt(dx * dx + dy * dy)  # Calculates direction length so diagonal speed can be normalised.
        player_x += dx / distance * player_speed * dt  # Moves horizontally at a time-based, normalised speed.
        player_y += dy / distance * player_speed * dt  # Moves vertically without making diagonal movement faster.
    player_x = constrain(player_x, player_radius, width - player_radius)  # Keeps the entire player circle inside the left and right edges.
    player_y = constrain(player_y, 60 + player_radius, height - player_radius)  # Keeps the player below the score bar and above the bottom edge.
    survival_time += dt  # Adds this frame's elapsed time to the score timer.
    spawn_timer += dt  # Adds elapsed time to determine when another block should appear.
    level = min(8, 1 + int(survival_time / 10.0))  # Increases difficulty every ten seconds and limits it to level eight.
    spawn_interval = max(0.30, 0.95 - (level - 1) * 0.09)  # Shortens the delay between blocks as difficulty rises, with a minimum limit.
    if spawn_timer >= spawn_interval:  # Checks whether enough time has passed to create another block.
        spawn_timer -= spawn_interval  # Preserves leftover time to keep spawning intervals more consistent.
        block_size = random(24, 44)  # Varies block size to create different obstacle shapes and gaps.
        block_x = random(0, width - block_size)  # Chooses a horizontal position that keeps the block within the window.
        block_speed = random(120, 170) + (level - 1) * 22  # Varies falling speed and increases it at higher levels.
        obstacles.append({  # Adds a dictionary so each block stores its own properties.
            "x": block_x,  # Stores the block's horizontal position for drawing and collision checks.
            "y": -block_size,  # Starts the block above the window so it enters from the top.
            "size": block_size,  # Stores its width and height for drawing and collision checks.
            "speed": block_speed  # Stores its falling speed so blocks can move independently.
        })  # Completes the dictionary and adds it to the active obstacle list.
    for block in obstacles[:]:  # Iterates over a shallow copy so removing blocks does not skip list entries.
        block["y"] += block["speed"] * dt  # Moves the block down using its speed and elapsed time.
        if touches_player(block):  # Calls the collision function to check whether this block touches the player.
            state = "over"  # Ends active gameplay when a collision occurs.
            best_score = max(best_score, int(survival_time))  # Keeps whichever is greater: the previous best or the current score.
            held_keys.clear()  # Clears movement input after the round ends.
            break  # Stops updating remaining blocks because the round has finished.
        if block["y"] > height:  # Checks whether the block has moved completely below the screen.
            obstacles.remove(block)  # Removes an invisible block to prevent unnecessary processing and list growth.
def touches_player(block):  # Separates circle-to-rectangle collision detection into a reusable function.
    nearest_x = constrain(player_x, block["x"], block["x"] + block["size"])  # Finds the closest horizontal coordinate on the block to the player centre.
    nearest_y = constrain(player_y, block["y"], block["y"] + block["size"])  # Finds the closest vertical coordinate on the block to the player centre.
    dx = player_x - nearest_x  # Measures horizontal separation from the nearest point.
    dy = player_y - nearest_y  # Measures vertical separation from the nearest point.
    return dx * dx + dy * dy <= player_radius * player_radius  # Detects contact when squared distance is within the squared radius, avoiding a square root.
def draw_game():  # Draws the gameplay scene without changing the game's movement or score.
    fill(255, 90, 105)  # Colours obstacles red to distinguish them from the blue player.
    for block in obstacles:  # Visits each active block so every obstacle is displayed.
        rect(block["x"], block["y"], block["size"], block["size"], 5)  # Draws the block at its stored position with slightly rounded corners.
    fill(70, 190, 255, 45)  # Uses transparent blue for a soft glow around the player.
    ellipse(player_x, player_y, 48, 48)  # Draws a decorative glow; it does not define the collision area.
    fill(80, 200, 255)  # Selects a brighter blue for the player's visible body.
    ellipse(player_x, player_y, player_radius * 2, player_radius * 2)  # Draws the player using the same radius used for collision detection.
    fill(225, 250, 255)  # Selects a pale colour for a small visual highlight.
    ellipse(player_x - 5, player_y - 5, 8, 8)  # Adds a highlight to make the player easier to recognise.
    fill(12, 17, 29)  # Selects a dark colour for the score-bar background.
    rect(0, 0, width, 55)  # Covers the top of the scene to keep score information readable.
    fill(240)  # Selects light text for contrast against the score bar.
    textSize(18)  # Sets a readable text size that fits within the bar.
    textAlign(LEFT, CENTER)  # Aligns the current score with the left side.
    text("Score: " + str(int(survival_time)), 18, 27)  # Converts survived seconds into text and displays whole seconds as the score.
    level = min(8, 1 + int(survival_time / 10.0))  # Calculates the displayed level using the same rule as the difficulty system.
    textAlign(CENTER, CENTER)  # Centres the level display in the score bar.
    text("Level: " + str(level), width / 2, 27)  # Displays the current difficulty level.
    textAlign(RIGHT, CENTER)  # Aligns the best score with the right side of the bar.
    text("Best: " + str(best_score), width - 18, 27)  # Displays the highest completed-round score from this program run.
def draw_end_screen():  # Draws an overlay that communicates the result and restart control.
    fill(0, 0, 0, 185)  # Selects transparent black so the final scene remains partly visible.
    rect(0, 0, width, height)  # Darkens the whole screen to make the result text stand out.
    textAlign(CENTER, CENTER)  # Centres the result text for a consistent layout.
    fill(255, 100, 115)  # Uses red to signal that the round has ended.
    textSize(42)  # Makes the game-over message the most prominent text.
    text("GAME OVER", width / 2, 180)  # Clearly tells the player the round is finished.
    fill(245)  # Selects light text to keep the scores readable.
    textSize(24)  # Uses a smaller size for the result details.
    text("Your score: " + str(int(survival_time)), width / 2, 245)  # Displays the final survival score in whole seconds.
    text("Best score: " + str(best_score), width / 2, 285)  # Displays the highest score for comparison.
    fill(255, 210, 100)  # Highlights the restart instruction in yellow.
    textSize(22)  # Sets a readable size for the restart prompt.
    text("Press R to restart", width / 2, 355)  # Explains how to begin another round.
def keyPressed():  # Processing calls this function when a key is pressed.
    if key == CODED:  # Identifies special keys, including the arrow keys.
        if state == "play":  # Accepts movement input only while a round is active.
            held_keys.add(keyCode)  # Remembers the pressed key so movement continues across frames.
    elif key == " " and state == "start":  # Checks for Space on the opening screen.
        start_game()  # Resets the game variables and starts the first round.
    elif (key == "r" or key == "R") and state == "over":  # Accepts either lowercase or uppercase R after game over.
        start_game()  # Reuses the reset function to begin a fresh round.
def keyReleased():  # Processing calls this function when a key is released.
    if key == CODED:  # Checks whether the released key is a special key.
        held_keys.discard(keyCode)  # Removes the key safely so its movement stops, even if it was already cleared.
