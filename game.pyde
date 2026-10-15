# A Simple 2D Survival Game
# Processing Python Mode
# No external images or libraries required.

player_x = 300.0
player_y = 420.0
player_radius = 16
player_speed = 280.0

obstacles = []
held_keys = set()

state = "start"
survival_time = 0.0
spawn_timer = 0.0
last_time = 0
best_score = 0


def setup():
    global last_time

    size(600, 500)
    frameRate(60)
    noStroke()
    last_time = millis()


def start_game():
    global player_x, player_y, obstacles
    global state, survival_time, spawn_timer, last_time

    player_x = width / 2.0
    player_y = height - 80.0
    obstacles = []
    held_keys.clear()

    survival_time = 0.0
    spawn_timer = 0.0
    last_time = millis()
    state = "play"


def draw():
    global last_time

    now = millis()
    dt = min((now - last_time) / 1000.0, 0.05)
    last_time = now

    # Release movement when the window loses focus.
    if not focused:
        held_keys.clear()

    background(20, 26, 42)
    draw_background()

    if state == "start":
        draw_start_screen()

    elif state == "play":
        update_game(dt)
        draw_game()

        if state == "over":
            draw_end_screen()

    elif state == "over":
        draw_game()
        draw_end_screen()


def draw_background():
    stroke(32, 41, 60)

    for x in range(0, width, 40):
        line(x, 0, x, height)

    for y in range(0, height, 40):
        line(0, y, width, y)

    noStroke()


def draw_start_screen():
    textAlign(CENTER, CENTER)

    fill(80, 200, 255)
    textSize(32)
    text("2D SURVIVAL GAME", width / 2, 140)

    fill(235)
    textSize(19)
    text("Use arrow keys to move", width / 2, 220)
    text("Avoid the falling red blocks", width / 2, 255)
    text("Survive longer to score more", width / 2, 290)

    fill(255, 210, 100)
    textSize(23)
    text("Press SPACE to start", width / 2, 365)


def update_game(dt):
    global player_x, player_y
    global survival_time, spawn_timer
    global state, best_score

    dx = 0
    dy = 0

    if LEFT in held_keys:
        dx -= 1
    if RIGHT in held_keys:
        dx += 1
    if UP in held_keys:
        dy -= 1
    if DOWN in held_keys:
        dy += 1

    # Keep diagonal movement at the same speed.
    if dx != 0 or dy != 0:
        distance = sqrt(dx * dx + dy * dy)
        player_x += dx / distance * player_speed * dt
        player_y += dy / distance * player_speed * dt

    # Keep the player inside the play area.
    player_x = constrain(
        player_x, player_radius, width - player_radius
    )
    player_y = constrain(
        player_y, 60 + player_radius, height - player_radius
    )

    survival_time += dt
    spawn_timer += dt

    # Difficulty increases every 10 seconds, up to level 8.
    level = min(8, 1 + int(survival_time / 10.0))
    spawn_interval = max(0.30, 0.95 - (level - 1) * 0.09)

    if spawn_timer >= spawn_interval:
        spawn_timer -= spawn_interval

        block_size = random(24, 44)
        block_x = random(0, width - block_size)
        block_speed = random(120, 170) + (level - 1) * 22

        obstacles.append({
            "x": block_x,
            "y": -block_size,
            "size": block_size,
            "speed": block_speed
        })

    # Iterate over a copy so blocks can be removed safely.
    for block in obstacles[:]:
        block["y"] += block["speed"] * dt

        if touches_player(block):
            state = "over"
            best_score = max(best_score, int(survival_time))
            held_keys.clear()
            break

        if block["y"] > height:
            obstacles.remove(block)


def touches_player(block):
    # Find the point on the block nearest to the player.
    nearest_x = constrain(
        player_x, block["x"], block["x"] + block["size"]
    )
    nearest_y = constrain(
        player_y, block["y"], block["y"] + block["size"]
    )

    dx = player_x - nearest_x
    dy = player_y - nearest_y

    return dx * dx + dy * dy <= player_radius * player_radius


def draw_game():
    # Falling obstacles.
    fill(255, 90, 105)

    for block in obstacles:
        rect(
            block["x"], block["y"],
            block["size"], block["size"], 5
        )

    # Player glow and body.
    fill(70, 190, 255, 45)
    ellipse(player_x, player_y, 48, 48)

    fill(80, 200, 255)
    ellipse(
        player_x, player_y,
        player_radius * 2, player_radius * 2
    )

    fill(225, 250, 255)
    ellipse(player_x - 5, player_y - 5, 8, 8)

    # Score bar.
    fill(12, 17, 29)
    rect(0, 0, width, 55)

    fill(240)
    textSize(18)
    textAlign(LEFT, CENTER)
    text("Score: " + str(int(survival_time)), 18, 27)

    level = min(8, 1 + int(survival_time / 10.0))
    textAlign(CENTER, CENTER)
    text("Level: " + str(level), width / 2, 27)

    textAlign(RIGHT, CENTER)
    text("Best: " + str(best_score), width - 18, 27)


def draw_end_screen():
    fill(0, 0, 0, 185)
    rect(0, 0, width, height)

    textAlign(CENTER, CENTER)

    fill(255, 100, 115)
    textSize(42)
    text("GAME OVER", width / 2, 180)

    fill(245)
    textSize(24)
    text(
        "Your score: " + str(int(survival_time)),
        width / 2, 245
    )
    text("Best score: " + str(best_score), width / 2, 285)

    fill(255, 210, 100)
    textSize(22)
    text("Press R to restart", width / 2, 355)


def keyPressed():
    if key == CODED:
        if state == "play":
            held_keys.add(keyCode)

    elif key == " " and state == "start":
        start_game()

    elif (key == "r" or key == "R") and state == "over":
        start_game()


def keyReleased():
    if key == CODED:
        held_keys.discard(keyCode)  
