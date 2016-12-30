import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random
import logging

myID, game_map = hlt.get_init()
hlt.send_init("MyBot")

LOG_FILENAME = 'log.txt'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

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
    	if square.strength > 125:
    		delta_x = square.x - center_x
    		delta_y = square.y - center_y
    		if abs(delta_x) > abs(delta_y):
    			if delta_x > 0:
    				return Move(square, EAST)
    			else:
    				return Move(square, WEST)
    		else:
    			if delta_y > 0:
    				return Move(square, SOUTH)
    			else:
    				return Move(square, NORTH)
    		#return Move(square, WEST)
    	else:
    		#return Move(square, SOUTH)
    		return Move(square, random.choice((NORTH, EAST, SOUTH, WEST)))

def get_center(current_map):
    total_x_strength = 0
    total_y_strength = 0
    total_strength = 0
    for square in current_map:
    	if square.owner == myID:
    		total_x_strength += square.x * square.strength
    		total_y_strength += square.y * square.strength
    		total_strength += square.strength
    return total_x_strength / total_strength, total_y_strength / total_strength

"""def get_center(current_map):
    # find x center, find y center
    # if there are 2 or more separate parts, calculate that too
    total_x_strength = 0
    total_y_strength = 0
    total_strength = 0
    for square in current_map:
    	if square.owner == myID:
    		total_x_strength += square.x * square.strength
        	total_y_strength += square.y * square.strength
        	total_strength += square.strength
    		#temp_c_x = total_x_strength / total_strength if total_strength != 0 else current_map.width / 2
    		#temp_c_y = total_y_strength / total_strength if total_strength != 0 else current_map.height / 2
    		'''if temp_c_x < current_map.width / 4:
    			total_x_strength += (square.x - current_map.width if square.x > current_map.width * 2 / 3 else square.x) * square.strength
    		elif temp_c_x > current_map.width * 3 / 4:
    			total_x_strength += (square.x + current_map.width if square.x < current_map.width / 3 else square.x) * square.strength
    		else:
    			total_x_strength += square.x * square.strength
    		if temp_c_y < current_map.height / 4:
    			total_y_strength += (square.y - current_map.height if square.x > current_map.height * 2 / 3 else square.y) * square.strength
    		elif temp_c_y > current_map.width * 3 / 4:
    			total_y_strength += (square.y + current_map.height if square.y < current_map.height / 3 else square.y) * square.strength
    		else:
    			total_y_strength += square.y * square.strength'''
        	#total_x_strength += (square.x + current_map.width if square.x < current_map.width / 2 else square.x) * square.strength
        	#total_y_strength += (square.y + current_map.height if square.y <k current_map.height / 2 else square.y) * square.strength
        	
    c_x = total_x_strength / total_strength
    c_y = total_y_strength / total_strength
    return c_x, c_y"""

while True:
    game_map.get_frame()
    center_x, center_y = get_center(game_map)
    log_message = str(center_x) + ", " + str(center_y)
    logging.debug(log_message)
    #logging.debug("hi")
    moves = [assign_move(square, center_x, center_y) for square in game_map if square.owner == myID]
    hlt.send_frame(moves)