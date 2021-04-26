import klotski as problem

init_state = problem.CREATE_INITIAL_STATE()
heuristic_choice = 'h_custom'
heuristics = problem.HEURISTICS[heuristic_choice]

print("Welcome to A Star")
COUNT = None
BACKLINKS = {}


def run_a_star():
    print("Initial State:")
    print(problem.DESCRIBE_STATE(init_state))
    global COUNT, BACKLINKS
    COUNT = 0
    BACKLINKS = {}
    iterate_a_star(init_state)
    print(str(COUNT) + " states examined.")


def iterate_a_star(initial_state):
    global COUNT, BACKLINKS

    open_states = [[initial_state, heuristics(initial_state)]]
    closed_states = []

    COST = {problem.HASHCODE(initial_state): 0}

    BACKLINKS[problem.HASHCODE(initial_state)] = -1

    while open_states:
        S = open_states[0]
        del open_states[0]
        closed_states.append(S)

        if problem.GOAL_TEST(S[0]):
            print(problem.GOAL_MESSAGE_FUNCTION(S[0]))
            backtrace(S[0])
            return

        COUNT += 1
        L = []

        for op in problem.OPERATORS:
            if op.precond(S[0]):
                new_state = op.state_transf(S[0])
                occur_closed = occurs_in(new_state, closed_states)
                occur_open = occurs_in(new_state, open_states)
                new_cost = COST[problem.HASHCODE(S[0])] + 1
                if occur_closed == -1 and occur_open == -1:
                    L.append([new_state, heuristics(new_state)])
                    BACKLINKS[problem.HASHCODE(new_state)] = S[0]
                    COST[problem.HASHCODE(new_state)] = new_cost

                elif occur_open > -1:
                    if COST[problem.HASHCODE(new_state)] > new_cost:
                        COST[problem.HASHCODE(new_state)] = new_cost
                        open_states[occur_open] = [new_state, new_cost]

        for s2 in L:
            for i in range(len(open_states)):
                if problem.DEEP_EQUALS(s2, open_states[i][0]):
                    del open_states[i];
                    break

        open_states = L + open_states
        open_states.sort(key=lambda x: x[1])


def backtrace(S):
    global BACKLINKS

    path = []
    while not S == -1:
        path.append(S)
        S = BACKLINKS[problem.HASHCODE(S)]
    path.reverse()
    print("Solution path: ")
    for s in path:
        print(problem.DESCRIBE_STATE(s))
    return path


def occurs_in(s1, lst):
    index = 0
    for s2 in lst:
        if problem.DEEP_EQUALS(s1, s2[0]):
            return index
        else:
            index = index + 1
    return -1


if __name__ == '__main__':
    run_a_star()
