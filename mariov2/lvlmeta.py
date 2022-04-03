WORLD_ONE = 'WORLD_ONE'
LVL_ONE = 'LVL_ONE'

b11addition = [(x, 5) for x in range(80,88)]
b11addition.extend([(x, 5) for x in range(91,94)])
b11addition.extend([(x, 5) for x in range(121, 124)])

    
stone11addition = []#[(x,12) for x in range(134, 138)]
def add_stone_triangle(topx, size, left=True):
    if left:
        for i in range(size):
            for j in range(i+1):
                stone11addition.append((topx-j, 13-size+i))
    else:
        for i in range(size):
            for j in range(i+1):
                stone11addition.append((topx+j, 13-size+i))
add_stone_triangle(137, 4)
add_stone_triangle(140, 4, False)
add_stone_triangle(155, 4, False)
add_stone_triangle(152, 5)
add_stone_triangle(189, 9)
stone11addition.remove((152,8))
stone11addition.remove((189,4))


#stone11addition.extend([() for x in range(140, 144)])

WORLDS = {
    WORLD_ONE: {
        LVL_ONE: {
            'floor' : [[x for x in range(69)], [x for x in range(71,86)], [x for x in range(89, 153)], [x for x in range(155, 211)],],
            # [width, height, [x coordstarts]]
            'green_tube': [ [2, 2, [28, 163, 179]], [2, 3, [38]], [2, 4, [46, 57]]],
            'question' : [(16,9), (22,5), (21,9), (23, 9), (78,9), (94,5), (106, 9), (109, 9), (112, 9) , (129, 5), (130, 5), (109, 5), (170, 9)],
            'bricks' : [(20, 9), (22, 9), (24,9), (77, 9), (79, 9), (94, 9), (100, 9), (101, 9), (118, 9), (128, 5), (131, 5), (129, 9), (130, 9), (168, 9), (169, 9), (171, 9) ],
            'stone' : [(198,12)],
            'goomba': [(12, [30, 37, 40, 45, 48, 56, 81, 167, 174, 124, 104,112, 128])]
        }
    }
}
WORLDS[WORLD_ONE][LVL_ONE]['bricks'].extend(b11addition)
WORLDS[WORLD_ONE][LVL_ONE]['stone'].extend(stone11addition)