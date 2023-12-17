from enum import Enum

from game_symbols.GameSymbols import GameSymbols


class MapObjects(Enum):
    Empty = GameSymbols.Grass.value
    Tree = GameSymbols.Tree.value
    Lake = GameSymbols.Water.value
    Fire = GameSymbols.Fire.value
    Cloud = GameSymbols.Cloud.value
    Lightning = GameSymbols.Lightning.value
    Helicopter = GameSymbols.Helicopter.value
    Hospital = GameSymbols.Hospital.value
    Shop = GameSymbols.Money.value
