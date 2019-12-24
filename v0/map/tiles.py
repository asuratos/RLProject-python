from dataclasses import dataclass

@dataclass
class Tile:
    is_walkable : bool = False
    is_open : bool = False
    blocks_vision : bool = False
    kind : str = 'wall'

    def set_walkable(self, walk):
        self.is_walkable = walk

    def set_open(self, opened):
        self.is_open = opened

    def set_opacity(self, blocks_v):
        self.blocks_vision = blocks_v

    def set_kind(self, kind):
        self.kind = kind