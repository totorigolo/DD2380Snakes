import os
import sys


sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from client import util # noqa


def test_position_0_is_coordinate_0():
    assert util.translate_position(0, 100) == (0, 0)


def test_can_find_all_snakes(game_map):
    m = util.Map(game_map)
    for snake in game_map['snakeInfos']:
        assert m.get_snake_by_id(snake['id'])


def test_finds_food_tile(game_map):
    m = util.Map(game_map)
    for food in game_map['foodPositions']:
        coord = util.translate_position(food, game_map['width'])
        assert m.get_tile_at(coord).tile_type == util.TileType.FOOD


def test_finds_obstacle_tiles(game_map):
    m = util.Map(game_map)
    for obstacle in game_map['obstaclePositions']:
        coord = util.translate_position(obstacle, game_map['width'])
        assert m.get_tile_at(coord).tile_type == util.TileType.OBSTACLE


def test_out_of_bounds(game_map):
    m = util.Map({'height': 5, 'width': 5})
    assert m.is_coordinate_out_of_bounds((-1, -1))
    assert m.is_coordinate_out_of_bounds((5, 5))
    assert not m.is_coordinate_out_of_bounds((4, 2))
    assert m.is_coordinate_out_of_bounds((0, -1))
    assert not m.is_coordinate_out_of_bounds((0, 0))


def test_identifies_movable_directions(game_map):
    width = 3
    snake_pos = util.translate_coordinate((1, 0), width)
    obstacle_pos = util.translate_coordinate((0, 0), width)

    m = util.Map({
        'height': width,
        'width': width,
        'snakeInfos': [{
            'positions': [snake_pos],
            'id': 0
        }],
        'obstaclePositions': [obstacle_pos],
        'foodPositions': []
    })
    assert m.can_snake_move_in_direction(0, util.Direction.DOWN)
    assert not m.can_snake_move_in_direction(0, util.Direction.UP)
    assert not m.can_snake_move_in_direction(0, util.Direction.LEFT)
    assert m.can_snake_move_in_direction(0, util.Direction.RIGHT)


def test_is_within_square():
    assert util.is_within_square((1, 1), (0, 0), (2, 2))
    assert util.is_within_square((0, 0), (0, 0), (2, 2))
    assert util.is_within_square((2, 2), (0, 0), (2, 2))
    assert not util.is_within_square((3, 2), (0, 0), (2, 2))
    assert not util.is_within_square((2, 3), (0, 0), (2, 2))
