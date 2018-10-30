#!/usr/bin/env python3
# Python 3.6

# Import the Halite SDK, which will let you interact with the game.
import hlt

# This library contains constant values.
from hlt import constants

# This library contains direction metadata to better interface with the game.
from hlt.positionals import Direction

# This library allows you to generate random numbers.
import random

# Logging allows you to save messages for yourself. This is required because the regular STDOUT
#   (print statements) are reserved for the engine-bot communication.
import logging

""" <<<Game Begin>>> """

# This game object contains the initial game state.
game = hlt.Game()
# At this point "game" variable is populated with initial map data.
# This is a good place to do computationally expensive start-up pre-processing.
# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("fatbot")

# Now that your bot is initialized, save a message to yourself in the log file with some important information.
#   Here, you log here your id, which you can always fetch from the game object by using my_id.
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))

""" <<<Game Loop>>> """
ship_states = {}    #empy dict

while True:
    # This loop handles each turn of the game. The game object changes every turn, and you refresh that state by
    #   running update_frame().
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    game_map = game.game_map

    # A command queue holds all the commands you will run this turn. You build this list up and submit it at the
    #   end of the turn.
    command_queue = []

<<<<<<< HEAD

=======
    # postions come in north, south, east, west
    direction_order = [Direction.North, Direction.South, Direction.East, Direction.West, Direction.Still]

    position_choices = []   # will contain map coordinate
>>>>>>> 831d5a3a4e9b76e6236ef43b128601e353d48b41
    for ship in me.get_ships():
        if ship.id not in ship_states:
            ship_states[ship.id] = "collecting"

        logging.info("Ship {} has {} halite.".format(ship.id,ship.halite_amount))
<<<<<<< HEAD
        move = game_map.naive_navigate(ship, game_map[hlt.Position(1,1)].position)
        command_queue.append(move)

=======
        position_options = ship.position.get_surrounding_cardinals() + [ship.position]

        # {( 0,1): (19,38)} -> maps movement you want to make to coordinate you end up at
        position_dict = {}
        # {(0,1): 500}
        halite_dict = {}

        for n, direction in enumerate(direction_order):
            position_dict[direction] = position_options[n]

        for direction in position_dict:
            position = position_dict[direction]
            halite_amount = game_map[position].halite_amount
            # create condition that if position is occupied, do not add value into dict
            if position_dict[direction] not in position_choices:
                halite_dict[direction] = halite_amount
                # this only means that we will not add choice to dict if another ship is PLANNING to move there
                # does not account for ships that are staying still on that point
            else:
                logging.info("attempting to move to same spot\n")

        if game.turn_number == 15:
                logging.info(position_options)

        # if ship_status[ship.id] == "returning":
        #     if ship.position == me.shipyard.position:
        #         ship_status[ship.id] = "exploring"
        #     else:
        #         move = game_map.naive_navigate(ship, me.shipyard.position)
        #         command_queue.append(ship.move(move))
        #     continue
        # elif ship.halite_amount >= constants.MAX_HALITE / 2:
        #         ship_status[ship.id] = "returning"

        # For each of your ships, move randomly if the ship is on a low halite location or the ship is full.
        #   Else, collect halite.
        if ship_states[ship.id] == "depositing":
            if ship.position == me.shipyard.position:
                ship_states[ship.id] = "collecting"
            else:
                move = game_map.naive_navigate(ship, me.shipyard.position)
                # add the naive navigate position of ships to the position choices so they dont collide with collecting ships
                position_choices.append(position_dict[move])
                command_queue.append(ship.move(move))
        elif ship.halite_amount > constants.MAX_HALITE / 3:
            ship_states[ship.id] = "depositing"

        if ship_states[ship.id] == "collecting":
            # if game_map[ship.position].halite_amount < constants.MAX_HALITE / 10 or ship.is_full:    >> old code
            directional_choice = max(halite_dict, key=halite_dict.get)
            position_choices.append(position_dict[directional_choice])
            command_queue.append(ship.move(directional_choice))
            # ^^ now we know the coordinates each ship is going to
            # else:  >>> old code
            #     position_choices.append(position_dict[Direction.Still])
            #     command_queue.append(ship.stay_still())


        # if ship_states[ship.id] == "depositing":
        #     if game_map[ship.position].halite_amount >= constants.MAX_HALITE / 8:
        #         if me.halite_amount >= 5000:
        #             command_queue.append(ship.make_dropoff())
>>>>>>> 831d5a3a4e9b76e6236ef43b128601e353d48b41

    # If the game is in the first 200 turns and you have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though - the ships will collide.
    if game.turn_number <= 300 and game.turn_number % 10 == 0 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)
