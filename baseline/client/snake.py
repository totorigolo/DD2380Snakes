import logging
import util
import numpy as np
import random
import sys

sys.setrecursionlimit(2000)

log = logging.getLogger("client.snake")


M = np.zeros((34, 46))

TILE_VALUES = { util.TileType.EMPTY: 1,
                util.TileType.FOOD: 2,
                util.TileType.WALL: -1,
                util.TileType.OBSTACLE: -1,
                util.TileType.SNAKE_HEAD: -5,
                util.TileType.SNAKE_BODY: -1,
                util.TileType.SNAKE_TAIL: 5}

def update_M(game_map):
    for y in range(34):
        for x in range(46):
            M[y][x] = TILE_VALUES[game_map.get_tile_at((x, y)).tile_type]


deltas = [util.Deltas.DOWN, util.Deltas.UP, util.Deltas.LEFT, util.Deltas.RIGHT]
def dfs(position, dmap):

    if not util.is_within_square(position, (0, 0), (45, 33)):
        return 0 

    if dmap[position[1]][position[0]] < 0:
        return 0 

    score                          = dmap[position[1]][position[0]]
    dmap[position[1]][position[0]] = -1
    for x, y in deltas:
        score += dfs((position[0] + x, position[1] + y), dmap)

    return score


def area(position, delta, dmap):

    perp_delta1 = (-delta[1], delta[0])
    perp_delta2 = (delta[1], -delta[0])

    score = 0
    while util.is_within_square(position, (0, 0), (45, 33)) and dmap[position[1]][position[0]] >= 0:
        

        perp_p1 = position
        perp_p2 = position

        while util.is_within_square(perp_p1, (0, 0), (45, 33)) and dmap[perp_p1[1]][perp_p1[0]] >= 0:
            score += dmap[perp_p1[1]][perp_p1[0]]
            perp_p1 = (perp_p1[0] + perp_delta1[0], perp_p1[1] + perp_delta1[1])

        while util.is_within_square(perp_p2, (0, 0), (45, 33)) and dmap[perp_p2[1]][perp_p2[0]] >= 0:
            score += dmap[perp_p2[1]][perp_p2[0]]
            perp_p2 = (perp_p2[0] + perp_delta2[0], perp_p2[1] + perp_delta2[1])

        position = (position[0] + delta[0], position[1] + delta[1])

    return score



class Snake(object):
    def __init__(self):
        self.name = "Monty"
        self.snake_id = None
        self.directions = [util.Direction.DOWN, util.Direction.UP, util.Direction.LEFT, util.Direction.RIGHT]

    def get_next_move(self, game_map):

        update_M(game_map)

        me   = game_map.get_snake_by_id(self.snake_id)
        head = util.translate_position(me["positions"][0], 46)



        ## BFS CHECK
        left_head  = (head[0] + util.Deltas.LEFT[0], head[1] + util.Deltas.LEFT[1])
        right_head = (head[0] + util.Deltas.RIGHT[0], head[1] + util.Deltas.RIGHT[1])
        down_head  = (head[0] + util.Deltas.DOWN[0], head[1] + util.Deltas.DOWN[1])
        up_head    = (head[0] + util.Deltas.UP[0], head[1] + util.Deltas.UP[1])

        max_score = -1
        action    = util.Direction.DOWN
        for delta, head, direction in zip(deltas, [down_head, up_head, left_head, right_head], self.directions):
            dfs_score  = dfs(head, np.array(M, copy=True)) 
            area_score = area(head, delta, M)

            # print("DFS: ", dfs_score, " AREA: ", area_score, " DIRECTION: ", direction)


            score = dfs_score + (area_score * 5 if area_score > 200 else area_score)
            # print(score)
            if score >= max_score:
                max_score = score
                action    = direction


        # Last resort Check
        if not game_map.can_snake_move_in_direction(self.snake_id, action):
            available_directions = []
            for direction in self.directions:
                if game_map.can_snake_move_in_direction(self.snake_id, direction):
                    available_directions.append(direction)

            if available_directions:
                action = random.choice(available_directions)

        # print("CHOOSE: ", action)
        # print()
        # print()

        return action

    def on_game_ended(self):
        log.debug('The game has ended!')

    def on_snake_dead(self, reason):
        log.debug('Our snake died because %s', reason)

    def on_game_starting(self):
        log.debug('Game is starting!')

    def on_player_registered(self, snake_id):
        log.debug('Player registered successfully')
        self.snake_id = snake_id

    def on_invalid_player_name(self):
        log.fatal('Player name is invalid, try another!')

    def on_game_result(self, player_ranks):
        log.info('Game result:')
        for player in player_ranks:
            is_alive = 'alive' if player['alive'] else 'dead'
            log.info('%d. %d pts\t%s\t(%s)' %
                     (player['rank'], player['points'], player['playerName'],
                      is_alive))


def get_snake():
    return Snake()
