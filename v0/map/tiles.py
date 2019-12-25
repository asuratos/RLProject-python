from dataclasses import dataclass

@dataclass
class Tile:
    is_walkable : bool = False
    is_open : bool = False
    is_seen : bool = False
    blocks_vision : bool = False
    kind : str = 'wall'

    def __init__(self, data):
        for key in data:
            setattr(self, key, data[key])

class TileFactory:
    def __init__(self):
        self.tiletypes = {
            'template': {
                'is_walkable' : True,
                'is_open' : False,
                'is_seen' : False,
                'blocks_vision' : False,
                'kind' : 'wall'
            },
            'wall' : {
                'is_walkable' : False,
                'is_open' : False,
                'is_seen' : False,
                'blocks_vision' : True,
                'kind' : 'wall'
            },
            'floor' : {
                'is_walkable' : True,
                'is_open' : True,
                'is_seen' : False,
                'blocks_vision' : False,
                'kind' : 'floor'
            },
            'door_closed' : {
                'is_walkable' : True,
                'is_open' : True,
                'is_seen' : False,
                'blocks_vision' : True,
                'kind' : 'door_closed'
            }
        }

    def generate_tile(self, type):
        return Tile(self.tiletypes[type])