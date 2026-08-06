from enum import Enum


class ChunkStrategy(str, Enum):
    RECURSIVE = "recursive"
    CHARACTER = "character"