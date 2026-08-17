from math import cos, sin

import pyray as rl

MAP_WIDTH = 24
MAP_HEIGHT = 24
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

world_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 3, 0, 3, 0, 3, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0, 0, 0, 3, 0, 3, 0, 3, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 0, 0, 0, 0, 5, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 0, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

rl.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Raycaster")
rl.set_target_fps(60)

posX, posY = 22, 12  # player x and y start position
dirX, dirY = -1, 0  # initial direction vector
# camera plane vector (perpendicular to the direction vector)
planeX, planeY = 0, 0.66


while not rl.window_should_close():
    rl.begin_drawing()
    rl.clear_background(rl.BLACK)

    for x in range(SCREEN_WIDTH):
        cameraX = 2 * x / SCREEN_WIDTH - 1
        # rayDir: Vec2 = dir + plane * cameraX
        rayDirX = dirX + (planeX * cameraX)
        rayDirY = dirY + (planeY * cameraX)

        # The grid/map coordinate of the player
        mapX, mapY = int(posX), int(posY)

        # How far from the current player position to the closest grid/map square border
        sideDistX, sideDistY = None, None

        # how far from grid/map square side to the next
        deltaDistX = float("inf") if rayDirX == 0 else abs(1 / rayDirX)
        deltaDistY = float("inf") if rayDirY == 0 else abs(1 / rayDirY)

        perpWallDist = None

        # in what direction to step in the DDA algorithm : either -1 or +1
        stepX, stepY = None, None

        hit = 0
        side = None

        # compute step and initial sideDist
        if rayDirX < 0:
            stepX = -1
            sideDistX = (posX - mapX) * deltaDistX
        else:
            stepX = 1
            sideDistX = (mapX + 1.0 - posX) * deltaDistX
        if rayDirY < 0:
            stepY = -1
            sideDistY = (posY - mapY) * deltaDistY
        else:
            stepY = 1
            sideDistY = (mapY + 1.0 - posY) * deltaDistY

        # DDA
        while hit == 0:
            if sideDistX < sideDistY:
                sideDistX += deltaDistX
                mapX += stepX
                side = 0
            else:
                sideDistY += deltaDistY
                mapY += stepY
                side = 1
            if world_map[mapX][mapY] > 0:
                hit = 1

        if side == 0:
            perpWallDist = sideDistX - deltaDistX
        else:
            perpWallDist = sideDistY - deltaDistY

        # compute height of wall to draw on screen
        lineHeight = (int)(SCREEN_HEIGHT / perpWallDist)

        # compute lowest and highest pixel to fill in current stripe
        # TODO: use a clamp() function
        drawStart = (int)(SCREEN_HEIGHT / 2 - lineHeight / 2)
        if drawStart < 0:
            drawStart = 0
        drawEnd = SCREEN_HEIGHT / 2 + lineHeight / 2
        if drawEnd >= SCREEN_HEIGHT:
            drawEnd = SCREEN_HEIGHT - 1

        color = rl.YELLOW

        # choose wall color
        match world_map[mapX][mapY]:
            case 1:
                color = rl.RED
            case 2:
                color = rl.GREEN
            case 3:
                color = rl.BLUE
            case 4:
                color = rl.WHITE
            case _:
                pass

        # give and y sides differnt brightness
        if side == 1:
            color = rl.color_brightness(color, -0.5)

        rl.draw_rectangle(x, drawStart, 1, lineHeight, color)

    # speed modifiers
    frameTime = 1 / 60
    moveSpeed = frameTime * 5.0  # in squares/second
    rotSpeed = frameTime * 3.0  # in radians/second

    # move forward if no wall in front of you
    if rl.is_key_down(rl.KeyboardKey.KEY_UP):
        if world_map[int(posX + dirX * moveSpeed)][int(posY)] == 0:
            posX += dirX * moveSpeed
        if world_map[int(posX)][int(posY + dirY * moveSpeed)] == 0:
            posY += dirY * moveSpeed

    # move backwards if no wall behind you
    if rl.is_key_down(rl.KeyboardKey.KEY_DOWN):
        if world_map[int(posX - dirX * moveSpeed)][int(posY)] == 0:
            posX -= dirX * moveSpeed
        if world_map[int(posX)][int(posY - dirY * moveSpeed)] == 0:
            posY -= dirY * moveSpeed
    # rotate to the right
    if rl.is_key_down(rl.KeyboardKey.KEY_RIGHT):
        # both camera direction and camera place must be rotated
        oldDirX = dirX
        dirX = dirX * cos(-rotSpeed) - dirY * sin(-rotSpeed)
        dirY = oldDirX * sin(-rotSpeed) + dirY * cos(-rotSpeed)
        oldPlaneX = planeX
        planeX = planeX * cos(-rotSpeed) - planeY * sin(-rotSpeed)
        planeY = oldPlaneX * sin(-rotSpeed) + planeY * cos(-rotSpeed)

    # rotate to the left
    if rl.is_key_down(rl.KeyboardKey.KEY_LEFT):
        # both camera direction and camera place must be rotated
        oldDirX = dirX
        dirX = dirX * cos(rotSpeed) - dirY * sin(rotSpeed)
        dirY = oldDirX * sin(rotSpeed) + dirY * cos(rotSpeed)
        oldPlaneX = planeX
        planeX = planeX * cos(rotSpeed) - planeY * sin(rotSpeed)
        planeY = oldPlaneX * sin(rotSpeed) + planeY * cos(rotSpeed)

    rl.end_drawing()
rl.close_window()
