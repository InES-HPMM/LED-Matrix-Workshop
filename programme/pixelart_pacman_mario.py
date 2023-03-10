from utime import sleep_ms
from ledmatrix import *

#=============================================================
# List X Offset
# --> Moves list to the left edge outside of the LED Matrix
# --> Move list in x direction by given offset
#=============================================================
def list_offset_x(coords, offset, cols):
    # find the highest and lowest y coordinate value to determine width of pixel art
    highest_x = 0
    lowest_x = cols

    for coord in coords:
        if highest_x < coord[0]:
            highest_x = coord[0]
        if lowest_x > coord[0]:
            lowest_x = coord[0]

    width = highest_x-lowest_x+1

    i = -(highest_x+1)+ offset
    new_list = []
    for coord in coords:
        x,y = coord
        x = x+i
        if (x>=0) and (x<cols):
            new_list.append((x,y))
    return new_list

#=============================================================
# List Y Offset
# --> Moves list to the bottom edge inside the LED Matrix
# --> Move list in y direction by given offset
#=============================================================
def list_offset_y(coords, offset, rows):
    new_list = []
    for coord in coords:
        x,y = coord
        y = y+offset
        if (y>=0) and (y<rows):
            new_list.append((x,y))
    return new_list


# Create a LedMatrix object. Initialize it with size of the matrix size:
WCL = LedMatrix(8, 8)

# Create a ColorTable Object to use one of 16 preset CSS colors:
CL = ColorTable()

# Set brightness
WCL.set_brightness(10)

#=============================================================
# Pixel Art Lists
#=============================================================
ghost_body = [(0,0),(2,0),(4,0),(6,0),(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(0,2),(1,2),(2,2),(3,2),(4,2),(5,2),(6,2),(0,3),(1,3),(2,3),(3,3),(4,3),(5,3),(6,3),(0,4),(3,4),(6,4),(0,5),(3,5),(6,5),(1,6),(2,6),(3,6),(4,6),(5,6),(2,7),(3,7),(4,7)]
ghost_eyes_right = [(1,4),(2,5),(1,5),(4,5),(5,5),(4,4)]
ghost_eyes_left = [(2,4),(2,5),(1,5),(4,5),(5,5),(5,4)]
pacman_closed =[(3,0),(4,0),(5,0),(2,1),(3,1),(4,1),(5,1),(6,1),(1,2),(2,2),(3,2),(4,2),(5,2),(6,2),(7,2),(1,3),(2,3),(3,3),(4,3),(5,3),(6,3),(7,3),(1,4),(2,4),(4,4),(5,4),(6,4),(7,4),(2,5),(3,5),(4,5),(5,5),(6,5),(3,6),(4,6),(5,6)]
pacman_open = [(2,0),(3,0),(4,0),(5,0),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(3,2),(4,2),(5,2),(6,2),(7,2),(5,3),(6,3),(7,3),(3,4),(4,4),(5,4),(6,4),(7,4),(1,5),(2,5),(4,5),(5,5),(6,5),(2,6),(3,6),(4,6),(5,6),]
pacman_closed1 =[(2,0),(3,0),(4,0),(5,0),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(0,2),(1,2),(2,2),(3,2),(4,2),(5,2),(6,2),(7,2),(0,3),(1,3),(2,3),(3,3),(4,3),(5,3),(6,3),(7,3),(0,4),(1,4),(2,4),(3,4),(4,4),(5,4),(6,4),(7,4),(1,5),(2,5),(4,5),(5,5),(6,5),(2,6),(3,6),(4,6),(5,6)]
heart = [(3,0),(2,1),(3,1),(4,1),(1,2),(2,2),(3,2),(4,2),(5,2),(0,3),(1,3),(2,3),(3,3),(4,3),(5,3),(6,3),(0,4),(1,4),(2,4),(3,4),(4,4),(5,4),(6,4),(1,5),(2,5),(4,5),(5,5)]
mario_red = [[1, 0], [2, 0], [4, 0], [5, 0], [1, 1], [3, 1], [5, 1], [2, 2], [4, 2], [0, 6], [1, 6], [2, 6], [3, 6], [4, 6], [5, 6], [6, 6], [7, 6], [1, 7], [2, 7], [3, 7], [4, 7], [5, 7]]
mario_skin = [[0, 1], [2, 1], [4, 1], [6, 1], [1, 3], [2, 3], [3, 3], [1, 4], [3, 4], [4, 4], [6, 4], [7, 4], [3, 5], [5, 5], [6, 5]]
mario_brown = [[1, 2], [3, 2], [5, 2], [4, 3], [5, 3], [6, 3], [5, 4], [2, 4], [0, 4], [0, 5], [1, 5], [2, 5], [4, 5]]
mario_eye = [[4, 5]]
shroom_white = [[2, 0], [5, 0], [2, 1], [5, 1], [1, 3], [5, 3], [6, 3], [0, 4], [1, 4], [2, 4], [4, 4], [5, 4], [6, 4], [7, 4], [3, 5], [2, 5], [6, 5], [7, 5], [3, 6], [6, 6], [3, 7], [4, 7], [5, 7]]
shroom_red = [[3, 0], [4, 0], [3, 4], [4, 5], [5, 5], [4, 6], [5, 6], [0, 5], [1, 5], [1, 6], [2, 6], [2, 7]]
shroom_orange = [[1, 1], [3, 1], [4, 1], [6, 1], [2, 2], [3, 2], [4, 2], [5, 2], [3, 3]]
shroom_orange_2 = [[1, 2], [3, 1], [4, 1], [6, 2], [2, 2], [3, 2], [4, 2], [5, 2], [3, 3]]



while True:
    # ------------------------------------------------------------------------------
    # GHOSTS AND PACMAN
    # ------------------------------------------------------------------------------
    for offset in range(50):
        WCL.clear()

        ghost_body1 = list_offset_x(ghost_body, offset, WCL.cols)
        ghost_eyes_right1 = list_offset_x(ghost_eyes_right, offset-1, WCL.cols)
        WCL.draw_list(ghost_body1, CL.BLUE)
        WCL.draw_list(ghost_eyes_right1, CL.WHITE)

        ghost_body2 = list_offset_x(ghost_body, offset-10, WCL.cols)
        ghost_eyes_right2 = list_offset_x(ghost_eyes_right, offset-11, WCL.cols)
        WCL.draw_list(ghost_body2, CL.PINK)
        WCL.draw_list(ghost_eyes_right2, CL.WHITE)

        ghost_body3 = list_offset_x(ghost_body, offset-20, WCL.cols)
        ghost_eyes_right3 = list_offset_x(ghost_eyes_right, offset-21, WCL.cols)
        WCL.draw_list(ghost_body3, CL.RED)
        WCL.draw_list(ghost_eyes_right3, CL.WHITE)

        ghost_body4 = list_offset_x(ghost_body, offset-30, WCL.cols)
        ghost_eyes_right4 = list_offset_x(ghost_eyes_right, offset-31, WCL.cols)
        WCL.draw_list(ghost_body4, CL.ORANGE)
        WCL.draw_list(ghost_eyes_right4, CL.WHITE)

        WCL.apply()
        sleep_ms(300)

    for offset in reversed(range(-12,50)):
        WCL.clear()

        ghost_body1 = list_offset_x(ghost_body, offset, WCL.cols)
        ghost_eyes_left1 = list_offset_x(ghost_eyes_left, offset-1, WCL.cols)
        WCL.draw_list(ghost_body1, CL.BLUE)
        WCL.draw_list(ghost_eyes_left1, CL.WHITE)

        ghost_body2 = list_offset_x(ghost_body, offset-10, WCL.cols)
        ghost_eyes_left2 = list_offset_x(ghost_eyes_left, offset-11, WCL.cols)
        WCL.draw_list(ghost_body2, CL.PINK)
        WCL.draw_list(ghost_eyes_left2, CL.WHITE)

        ghost_body3 = list_offset_x(ghost_body, offset-20, WCL.cols)
        ghost_eyes_left3 = list_offset_x(ghost_eyes_left, offset-21, WCL.cols)
        WCL.draw_list(ghost_body3, CL.RED)
        WCL.draw_list(ghost_eyes_left3, CL.WHITE)

        ghost_body4 = list_offset_x(ghost_body, offset-30, WCL.cols)
        ghost_eyes_left4 = list_offset_x(ghost_eyes_left, offset-31, WCL.cols)
        WCL.draw_list(ghost_body4, CL.ORANGE)
        WCL.draw_list(ghost_eyes_left4, CL.WHITE)

        if offset%2==0:
            pacman = list_offset_x(pacman_closed,offset+10, WCL.cols)
        else:
            pacman = list_offset_x(pacman_open,offset+10, WCL.cols)
        WCL.draw_list(pacman, CL.YELLOW)

        WCL.apply()
        sleep_ms(50)

    # ------------------------------------------------------------------------------
    # HEART
    # ------------------------------------------------------------------------------
    WCL.clear()
    WCL.draw_list(heart, CL.RED)
    WCL.apply()
    sleep_ms(800)

    new_heart = []
    for coords in heart:
        x,y = coords
        new_heart.append([x+1,y+2])
    WCL.clear()
    WCL.draw_list(new_heart, CL.RED)
    WCL.apply()
    sleep_ms(800)

    new_heart = []
    for coords in heart:
        x,y = coords
        new_heart.append([x,y+2])
    WCL.clear()
    WCL.draw_list(new_heart, CL.RED)
    WCL.apply()
    sleep_ms(800)

    new_heart = []
    for coords in heart:
        x,y = coords
        new_heart.append([x+1,y])
    WCL.clear()
    WCL.draw_list(new_heart, CL.RED)
    WCL.apply()
    sleep_ms(800)


    # ------------------------------------------------------------------------------
    # Super MARIO - Jumping
    # ------------------------------------------------------------------------------
    for offset in range(18):
        WCL.clear()

        # super mario jumping
        mario_red_o = list_offset_x(mario_red, offset, WCL.cols)
        mario_skin_o = list_offset_x(mario_skin, offset, WCL.cols)
        mario_brown_o = list_offset_x(mario_brown, offset-1, WCL.cols)
        mario_eye_o = list_offset_x(mario_eye, offset-3, WCL.cols)

        # jump every fifth time
        if offset%5==0:
            mario_red_oo = list_offset_y(mario_red_o, 1, WCL.rows)
            mario_skin_oo = list_offset_y(mario_skin_o, 1, WCL.rows)
            mario_brown_oo = list_offset_y(mario_brown_o, 1, WCL.rows)
            mario_eye_oo = list_offset_y(mario_eye_o, 1, WCL.rows)
        else:
            mario_red_oo = mario_red_o
            mario_skin_oo = mario_skin_o
            mario_brown_oo = mario_brown_o
            mario_eye_oo = mario_eye_o

        WCL.draw_list(mario_red_oo, CL.RED)
        WCL.draw_list(mario_skin_oo, CL.ORANGE)
        WCL.draw_list(mario_brown_oo, (60,30,0))
        WCL.draw_list(mario_eye_oo, CL.BLACK)

        WCL.apply()
        sleep_ms(200)

    # ------------------------------------------------------------------------------
    # Mushroom
    # ------------------------------------------------------------------------------
    for offset in range(40):
        WCL.clear()

        #SHROOM 1
        shroom_white_o = list_offset_x(shroom_white, offset, WCL.cols)
        shroom_red_o = list_offset_x(shroom_red, offset-2, WCL.cols)
        if offset%2==0:
            shroom_orange_o = list_offset_x(shroom_orange, offset-1, WCL.cols)
        else:
            shroom_orange_o = list_offset_x(shroom_orange_2, offset-1, WCL.cols)

        WCL.draw_list(shroom_white_o, CL.WHITE)
        WCL.draw_list(shroom_red_o, CL.RED)
        WCL.draw_list(shroom_orange_o, CL.ORANGE)

        #HEART
        heart_o = list_offset_x(heart, offset-10, WCL.cols)
        WCL.draw_list(heart_o, CL.RED)

        #SHROOM 2
        shroom_white_o2 = list_offset_x(shroom_white, offset-19, WCL.cols)
        shroom_red_o2 = list_offset_x(shroom_red, offset-21, WCL.cols)
        shroom_orange_o2 = list_offset_x(shroom_orange, offset-20, WCL.cols)

        if offset%2==0:
            shroom_orange_o2 = list_offset_x(shroom_orange, offset-20, WCL.cols)
        else:
            shroom_orange_o2 = list_offset_x(shroom_orange_2, offset-20, WCL.cols)

        WCL.draw_list(shroom_white_o2, CL.WHITE)
        WCL.draw_list(shroom_red_o2, CL.RED)
        WCL.draw_list(shroom_orange_o2, CL.ORANGE)

        WCL.apply()
        sleep_ms(160)

