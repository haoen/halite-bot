import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random
import logging

LOG_FILENAME = 'log.txt'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

myID, game_map = hlt.get_init()
hlt.send_init("MyBot")

def assign_move(square, center_x, center_y):
    for direction, neighbor in enumerate(game_map.neighbors(square)):
        if neighbor.owner != myID and neighbor.strength < square.strength:
            return Move(square, direction)
    
    can_move = True
    for direction, neighbor in enumerate(game_map.neighbors(square)):
        if neighbor.owner != myID:
            can_move = False

    if square.strength < 5 * square.production or not can_move:
        return Move(square, STILL)
    else:
        return Move(square, random.choice((NORTH, EAST, SOUTH, WEST)))

def get_center(current_map):
    # find x center, find y center
    # if there are 2 or more separate parts, calculate that too
    total_x_strength = 0
    total_y_strength = 0
    total_strength = 0
    for square in current_map:
        total_x_strength += (square.x + current_map.width if square.x > current_map.width / 2 else square.x) * square.strength
        total_y_strength += (square.y + current_map.height if square.y > current_map.height / 2 else square.y) * square.strength
        total_strength += square.strength
    c_x = total_x_strength / total_strength
    c_y = total_y_strength / total_strength
    c_x = c_x - current_map.width if c_x > current_map.width else c_x
    c_y = c_y - current_map.width if c_y > current_map.width else c_y
    return c_x, c_y

while True:
    game_map.get_frame()
    center_x, center_y = get_center(game_map)
    moves = [assign_move(square, center_x, center_y) for square in game_map if square.owner == myID]
    hlt.send_frame(moves)