GOAL_BLOCK = 'A'

CREATE_INITIAL_STATE = lambda: ["E", "E", "_", "H",
                                "B", "G", "_", "C",
                                "B", "A", "A", "C",
                                "D", "A", "A", "F",
                                "D", "I", "J", "F"]


class Piece:
    def __init__(self, id, x, y, w, h):
        self.id = id
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __str__(self):
        return self.id + " " + str(int(self.x)) + " " + str(int(self.y)) \
               + " " + str(int(self.w)) + " " + str(int(self.h))

    def can_move(self, state, direction):
        w = int(self.w)
        h = int(self.h)
        x = int(self.x)
        y = int(self.y)
        try:
            move = 1
            if direction == 1 or direction == 2:
                move = -1
            if direction == 0:
                move += w - 1
            if direction == 3:
                move += h - 1
            if direction % 2 == 0:
                for i in range(h):
                    if 0 <= x + move < 4:
                        if state[4 * (y + i) + x + move] != "_":
                            return False
                    else:
                        return False
            else:
                for i in range(w):
                    if 0 <= y + move < 5:
                        if state[4 * (y + move) + (x + i)] != "_":
                            return False
                    else:
                        return False
            return True

        except (Exception) as e:
            print(e)


def goal_message(s):
    return "Solved the Klotski puzzle, champ!"


def copy_state(s):
    new_state = list(s)
    return new_state


def DEEP_EQUALS(s1, s2):
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            return False
    return True


def DESCRIBE_STATE(state):
    result = ""
    for row in range(5):
        result = result + "   "
        for col in range(4):
            result = result + (str(state[4 * row + col]) + " ")
        result = result + "\n"
    return result


def HASHCODE(state):
    return DESCRIBE_STATE(state)


class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)


def move(s, tile, dir):
    new_state = copy_state(s)

    curr_index = tile.y * 4 + tile.x
    for width in range(tile.w):
        for height in range(tile.h):
            tile_index = int(curr_index + width + height * 4)

            if dir == 3:
                new_state[tile_index + 4] = s[tile_index]
                if height == 0:
                    new_state[tile_index] = "_"

            elif dir == 1:
                new_state[tile_index - 4] = s[tile_index]
                if height == tile.h - 1:
                    new_state[tile_index] = "_"

            elif dir == 0:
                new_state[tile_index + 1] = s[tile_index]
                if width == 0:
                    new_state[tile_index] = "_"

            else:
                new_state[tile_index - 1] = s[tile_index]
                if width == tile.w - 1:
                    new_state[tile_index] = "_"

    return new_state


def goal_test(state):
    return state[13] == GOAL_BLOCK and state[14] == GOAL_BLOCK and \
           state[17] == GOAL_BLOCK and state[18] == GOAL_BLOCK


def translate_dir(num):
    dir = ''
    if num == 0:
        dir = 'east'
    elif num == 1:
        dir = 'north'
    elif num == 2:
        dir = 'west'
    else:
        dir = 'south'
    return dir


def can_move(s, piece, direction):
    return piece.can_move(s, direction)


def combo_list():
    ls = []
    for tile in sorted(list(set(CREATE_INITIAL_STATE()) - set(['_']))):
        for i in range(4):
            ls.append((tile, i))
    return ls


def make_piece(state, tile):
    index = state.index(tile)
    curr_col = index % 4
    curr_row = int(index / 4)

    shape = [1, 1]
    if state[(index + 1) % len(state)] == state[index]:
        shape[0] += 1
    if state[(index + 4) % len(state)] == state[index]:
        shape[1] += 1
    return Piece(state[index], curr_col, curr_row, shape[0], shape[1])


OPERATORS = [Operator("Move tile " + str(tile) + " to the " + str(translate_dir(direction)),
                      lambda s, p=tile, q=direction: can_move(s, make_piece(s, p), q),
                      lambda s, p=tile, q=direction: move(s, make_piece(s, p), q))
             for (tile, direction) in combo_list()]

GOAL_TEST = lambda s: goal_test(s)


GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)


def h_custom(s):
    goal_y = int(s.index(GOAL_BLOCK) / 4) + 1
    total = 0
    empty_index = int(s.index('_'))
    if ((empty_index + 1) % 4 != 0 and s[(empty_index + 1) % 4] != '_') \
            or (s[(empty_index + 4) % 20] != '_'):
        total += 2

    for key in sorted(set(s) - set(['_'])):
        piece = make_piece(s, key)
        if (piece.y > goal_y):
            total += piece.w * piece.h
    return int(total)


HEURISTICS = {'h_custom': h_custom}


def render_state(s):
    return DESCRIBE_STATE(s)
