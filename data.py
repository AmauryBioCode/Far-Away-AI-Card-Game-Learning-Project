#[x,x,x] = [stone, dear, pineapple]

#color: grey (w), blue (b), red (r), green (g) j'ai choisi w comme white pour gris car g est déjà pris par green

# ["points", x] (x points),  ["night", x] (x points par carte nuit),  ["bre", x] (x point par carte rouge et bleu (re = red, b = blue, g = green, y = yellow, w = gray),  

# ["color", x] (x points pour chaque 4 couleurs différentes), ["stone", x] (x points par pierre), ["parchment", x], 

# ["resources", x] (x points pour chaque 3 resources différentes)

cards_data= {

    "0": {"resources": [1,1,1], "parchment": False, "color": 'w', "night": False, "condition": None, "points": None},

    1: {"resources": [1, 1, 0], "parchment": False, "color": "r", "night": False, "condition": None, "points": None},

    2: {"resources": [2, 0, 0], "parchment": False, "color": "b", "night": False, "condition": None, "points": None},

    3: {"resources": [0, 0, 0], "parchment": False, "color": "g", "night": False, "condition": None, "points": ["points", 4]},

    4: {"resources": [1, 0, 1], "parchment": False, "color": "r", "night": False, "condition": None, "points": None},

    5: {"resources": [0, 1, 0], "parchment": False, "color": "g", "night": False, "condition": None, "points": ["points", 2]},

    6: {"resources": [1, 0, 0], "parchment": True, "color": "b", "night": False, "condition": None, "points": None},

    7: {"resources": [0, 1, 1], "parchment": False, "color": "r", "night": False, "condition": None, "points": None},

    8: {"resources": [0, 1, 0], "parchment": True, "color": "g", "night": False, "condition": None, "points": None},

    9: {"resources": [0, 0, 0], "parchment": False, "color": "b", "night": False, "condition": None, "points": ["points", 5]},

    10: {"resources": [0, 0, 0], "parchment": False, "color": "r", "night": False, "condition": None, "points": ["night", 3]},

    11: {"resources": [0, 0, 0], "parchment": False, "color": "g", "night": False, "condition": None, "points": ["parchment", 2]},

    12: {"resources": [0, 0, 1], "parchment": True, "color": "y", "night": False, "condition": None, "points": None},

    13: {"resources": [0, 0, 0], "parchment": False, "color": "b", "night": False, "condition": None, "points": ["stone", 2]},

    14: {"resources": [0, 0, 1], "parchment": False, "color": "r", "night": False, "condition": None, "points": ["night", 2]},

    15: {"resources": [0, 0, 0], "parchment": True, "color": "g", "night": False, "condition": None, "points": ["dear", 2]},

    16: {"resources": [0, 1, 0], "parchment": False, "color": "r", "night": False, "condition": None, "points": ["dear", 2]},

    17: {"resources": [1, 0, 0], "parchment": False, "color": "b", "night": False, "condition": [0, 2, 0], "points": ["stone", 3]},

    18: {"resources": [0, 1, 0], "parchment": False, "color": "g", "night": False, "condition": None, "points": ["color", 10]},

    19: {"resources": [0, 0, 1], "parchment": False, "color": "r", "night": False, "condition": None, "points": ["pineapple", 2]},

    20: {"resources": [0, 0, 0], "parchment": True, "color": "g", "night": True, "condition": [1, 0, 0], "points": ["night", 2]},

    21: {"resources": [0, 0, 0], "parchment": False, "color": "b", "night": True, "condition": [2, 0, 0], "points": ["points", 8]},

    22: {"resources": [0, 0, 0], "parchment": True, "color": "g", "night": True, "condition": None, "points": ["parchment", 1]},

    23: {"resources": [1, 1, 0], "parchment": False, "color": "r", "night": True, "condition": None, "points": ["color", 10]},

    24: {"resources": [0, 1, 0], "parchment": False, "color": "g", "night": True, "condition": [0, 1, 0], "points": ["night", 2]},

    25: {"resources": [0, 0, 0], "parchment": False, "color": "y", "night": True, "condition": None, "points": ["gy", 1]},

    26: {"resources": [0, 1, 0], "parchment": False, "color": "r", "night": True, "condition": None, "points": ["pineapple", 3]},

    27: {"resources": [0, 0, 0], "parchment": False, "color": "y", "night": True, "condition": None, "points": ["yb", 1]},

    28: {"resources": [1, 0, 0], "parchment": False, "color": "r", "night": True, "condition": None, "points": ["dear", 3]},

    29: {"resources": [0, 0, 1], "parchment": False, "color": "y", "night": True, "condition": None, "points": ["pineapple", 3]},

    30: {"resources": [1, 0, 0], "parchment": False, "color": "r", "night": True, "condition": None, "points": ["stone", 2]},

    31: {"resources": [0, 0, 0], "parchment": False, "color": "y", "night": True, "condition": None, "points": ["yre", 1]},

    32: {"resources": [1, 1, 0], "parchment": False, "color": "r", "night": True, "condition": [3, 0, 0], "points": ["points", 7]},

    33: {"resources": [0, 0, 0], "parchment": True, "color": "y", "night": True, "condition": None, "points": ["pineapple", 3]},

    34: {"resources": [0, 1, 0], "parchment": False, "color": "g", "night": True, "condition": [2, 0, 0], "points": ["dear", 3]},

    35: {"resources": [0, 1, 0], "parchment": False, "color": "y", "night": True, "condition": None, "points": ["color", 10]},

    36: {"resources": [0, 0, 0], "parchment": False, "color": "r", "night": True, "condition": [0, 2, 0], "points": ["pineapple", 4]},

    37: {"resources": [0, 0, 0], "parchment": False, "color": "y", "night": True, "condition": [0, 0, 1], "points": ["night", 3]},

    38: {"resources": [1, 0, 0], "parchment": False, "color": "g", "night": True, "condition": [0, 1, 1], "points": ["parchment", 3]},

    39: {"resources": [1, 0, 1], "parchment": False, "color": "r", "night": True, "condition": [0, 2, 0], "points": ["points", 9]},

    40: {"resources": [0, 0, 0], "parchment": False, "color": "b", "night": True, "condition": [1, 1, 1], "points": ["night", 3]},

    41: {"resources": [0, 0, 1], "parchment": False, "color": "g", "night": False, "condition": [2, 1, 0], "points": ["night", 4]},

    42: {"resources": [0, 0, 0], "parchment": False, "color": "y", "night": False, "condition": [1, 1, 0], "points": ["gy", 2]},

    43: {"resources": [1, 0, 0], "parchment": False, "color": "b", "night": False, "condition": None, "points": ["color", 10]},

    44: {"resources": [0, 0, 0], "parchment": False, "color": "y", "night": False, "condition": [1, 0, 1], "points": ["yb", 2]},

    45: {"resources": [1, 0, 0], "parchment": False, "color": "g", "night": False, "condition": [0, 3, 0], "points": ["points", 13]},

    46: {"resources": [0, 0, 0], "parchment": True, "color": "b", "night": False, "condition": [2, 1, 0], "points": ["points", 10]},

    47: {"resources": [0, 0, 0], "parchment": False, "color": "y", "night": False, "condition": [0, 1, 1], "points": ["yre", 2]},

    48: {"resources": [0, 1, 0], "parchment": False, "color": "r", "night": False, "condition": None, "points": ["stone", 3]},

    49: {"resources": [0, 0, 0], "parchment": True, "color": "b", "night": False, "condition": [2, 0, 1], "points": ["points", 12]},

    50: {"resources": [1, 0, 0], "parchment": False, "color": "y", "night": False, "condition": [0, 0, 2], "points": ["g", 2]},

    51: {"resources": [1, 0, 0], "parchment": False, "color": "b", "night": False, "condition": [4, 0, 0], "points": ["points", 14]},

    52: {"resources": [0, 0, 0], "parchment": False, "color": "r", "night": False, "condition": [3, 0, 0], "points": ["dear", 4]},

    53: {"resources": [0, 1, 0], "parchment": False, "color": "y", "night": False, "condition": [0, 2, 0], "points": ["re", 4]},

    54: {"resources": [0, 1, 0], "parchment": False, "color": "g", "night": False, "condition": [0, 0, 2], "points": ["parchment", 4]},

    55: {"resources": [1, 0, 0], "parchment": True, "color": "b", "night": False, "condition": [0, 1, 2], "points": ["stone", 3]},

    56: {"resources": [0, 0, 1], "parchment": False, "color": "y", "night": False, "condition": [1, 2, 0], "points": ["b", 4]},

    57: {"resources": [0, 0, 0], "parchment": False, "color": "r", "night": False, "condition": [0, 0, 3], "points": ["stone", 4]},

    58: {"resources": [0, 0, 0], "parchment": True, "color": "g", "night": False, "condition": [0, 3, 0], "points": ["parchment", 3]},

    59: {"resources": [0, 0, 0], "parchment": True, "color": "y", "night": False, "condition": [1, 3, 0], "points": ["yre", 3]},

    60: {"resources": [0, 0, 0], "parchment": True, "color": "b", "night": False, "condition": [2, 2, 0], "points": ["points", 16]},

    61: {"resources": [0, 0, 1], "parchment": False, "color": "g", "night": False, "condition": [0, 4, 0], "points": ["points", 17]},

    62: {"resources": [0, 0, 0], "parchment": True, "color": "y", "night": False, "condition": [0, 0, 3], "points": ["yb", 3]},

    63: {"resources": [0, 0, 0], "parchment": True, "color": "g", "night": False, "condition": [0, 2, 1], "points": ["points", 15]},

    64: {"resources": [0, 0, 0], "parchment": True, "color": "b", "night": False, "condition": [2, 0, 2], "points": ["points", 18]},

    65: {"resources": [0, 0, 0], "parchment": True, "color": "y", "night": False, "condition": [0, 0, 3], "points": ["gy", 3]},

    66: {"resources": [0, 0, 0], "parchment": False, "color": "b", "night": False, "condition": [4, 0, 0], "points": ["points", 20]},

    67: {"resources": [0, 0, 0], "parchment": True, "color": "g", "night": False, "condition": [0, 2, 2], "points": ["points", 20]},

    68: {"resources": [0, 0, 0], "parchment": False, "color": "b", "night": False, "condition": [5, 0, 0], "points": ["points", 24]},

    69: {"resources": [0, 0, 0], "parchment": True, "color": "r", "night": False, "condition": None, "points": ["resources", 7]},

    70: {"resources": [0, 0, 0], "parchment": True, "color": "w", "night": False, "condition": None, "points": ["points", 6]},

    71: {"resources": [1, 0, 0], "parchment": False, "color": "g", "night": True, "condition": None, "points": ["resources", 7]},

    72: {"resources": [0, 0, 0], "parchment": True, "color": "w", "night": True, "condition": [0, 5, 0], "points": ["points",26]},

    73: {"resources": [0, 1, 0], "parchment": False, "color": "y", "night": True, "condition": [0, 0, 4], "points": ["w", 5]},

    74: {"resources": [0, 0, 1], "parchment": False, "color": "w", "night": True, "condition": None, "points": ["resources", 7]},

    75: {"resources": [0, 0, 0], "parchment": True, "color": "b", "night": True, "condition": [6, 0, 0], "points": ["points", 28]},

    76: {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": True, "condition": [2, 2, 2], "points": ["w", 4]},

}



sanctuary_data = {

 "100": {"resources": [0, 1, 0], "parchment": False, "color": "r", "night": False, "points": None},

    "102": {"resources": [0, 1, 0], "parchment": False, "color": "g", "night": False, "points": None},

    "103": {"resources": [0, 1, 0], "parchment": False, "color": "b", "night": False, "points": None},

    "104": {"resources": [0, 1, 0], "parchment": False, "color": "w", "night": False, "points": ["w", 1]},

    "105": {"resources": [0, 1, 0], "parchment": False, "color": "w", "night": False, "points": ["dear", 1]},

    "106": {"resources": [0, 1, 0], "parchment": False, "color": "w", "night": True, "points": None},

    "107": {"resources": [0, 1, 0], "parchment": False, "color": "w", "night": False, "points": ["parchment", 1]},

    "108": {"resources": [0, 1, 0], "parchment": True, "color": "w", "night": False, "points": None},

    "109": {"resources": [1, 0, 0], "parchment": False, "color": "r", "night": False, "points": None},

    "110": {"resources": [1, 0, 0], "parchment": False, "color": "b", "night": False, "points": None},

    "111": {"resources": [1, 0, 0], "parchment": False, "color": "g", "night": False, "points": None},

    "112": {"resources": [1, 0, 0], "parchment": False, "color": "y", "night": False, "points": None},

    "113": {"resources": [1, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["night", 1]},

    "114": {"resources": [1, 0, 0], "parchment": False, "color": "w", "night": True, "points": None},

    "115": {"resources": [1, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["parchment", 1]},

    "116": {"resources": [1, 0, 0], "parchment": True, "color": "w", "night": False, "points": None},

    "117": {"resources": [1, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["stone", 1]},

    "118": {"resources": [2, 0, 0], "parchment": False, "color": "w", "night": False, "points": None},

    "119": {"resources": [0, 0, 1], "parchment": False, "color": "r", "night": False, "points": None},

    "120": {"resources": [0, 0, 1], "parchment": False, "color": "b", "night": False, "points": None},

    "121": {"resources": [0, 0, 1], "parchment": False, "color": "w", "night": False, "points": ["w", 1]},

    "122": {"resources": [0, 0, 1], "parchment": False, "color": "w", "night": False, "points": ["pineapple", 1]},

    "123": {"resources": [0, 0, 1], "parchment": True, "color": "w", "night": False, "points": None},

    "124": {"resources": [0, 0, 1], "parchment": False, "color": "w", "night": True, "points": None},

    "125": {"resources": [0, 0, 0], "parchment": True, "color": "b", "night": False, "points": None},

    "126": {"resources": [0, 0, 0], "parchment": True, "color": "y", "night": False, "points": None},

    "127": {"resources": [0, 0, 0], "parchment": True, "color": "g", "night": False, "points": None},

    "128": {"resources": [0, 0, 0], "parchment": True, "color": "w", "night": False, "points": ["color", 4]},

    "129": {"resources": [0, 0, 0], "parchment": True, "color": "w", "night": False, "points": ["parchment", 1]},

    "130": {"resources": [0, 0, 0], "parchment": True, "color": "w", "night": False, "points": ["resources", 3]},

    "131": {"resources": [0, 0, 0], "parchment": False, "color": "y", "night": True, "points": ["w", 1]},

    "132": {"resources": [0, 0, 0], "parchment": False, "color": "r", "night": True, "points": None},

    "133": {"resources": [0, 0, 0], "parchment": False, "color": "y", "night": False, "points": ["y", 1]},

    "134": {"resources": [0, 0, 0], "parchment": False, "color": "y", "night": False, "points": ["parchment", 1]},

    "135": {"resources": [0, 0, 0], "parchment": False, "color": "y", "night": False, "points": ["color", 4]},

    "136": {"resources": [0, 0, 0], "parchment": False, "color": "g", "night": False, "points": ["night", 1]},

    "137": {"resources": [0, 0, 0], "parchment": False, "color": "g", "night": False, "points": ["resources", 3]},

    "138": {"resources": [0, 0, 0], "parchment": False, "color": "g", "night": False, "points": ["g", 1]},

    "139": {"resources": [0, 0, 0], "parchment": False, "color": "b", "night": False, "points": ["w", 2]},

    "140": {"resources": [0, 0, 0], "parchment": False, "color": "b", "night": False, "points": ["b", 1]},

    "141": {"resources": [0, 0, 0], "parchment": False, "color": "r", "night": False, "points": ["re", 1]},

    "142": {"resources": [0, 0, 0], "parchment": False, "color": "r", "night": False, "points": ["resources", 3]},

    "143": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["yre", 1]},

    "144": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["stone", 2]},

    "145": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["bre", 1]},

    "146": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["gy", 1]},

    "147": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["bg", 1]},

    "148": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["gre", 1]},

    "149": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["by", 1]},

    "150": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["parchment", 2]},

    "151": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["pineapple", 2]},

    "152": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["dear", 2]},

    "153": {"resources": [0, 0, 0], "parchment": False, "color": "w", "night": False, "points": ["points", 5]},

}
