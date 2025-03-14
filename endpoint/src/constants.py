from typing import List
cmds: List = [
    "CREATE fruits",
    "CREATE vegetables",
    "CREATE grains",
    "CREATE fruits/apples",
    "CREATE fruits/apples/fuji",
    "LIST",
    "CREATE grains/squash",
    "MOVE grains/squash vegetables",
    "CREATE foods",
    "MOVE grains foods",
    "MOVE fruits foods",
    "MOVE vegetables foods",
    "LIST",
    "DELETE fruits/apples",
    "DELETE foods/fruits/apples",
    "LIST"
]
