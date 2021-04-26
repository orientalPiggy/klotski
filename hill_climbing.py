import klotski as problem
import random

print("Welcome to Hill Climbing")
COUNT = None
BACKLINKS = {}
heuristic_choice = 'h_custom'
heuristics = problem.HEURISTICS[heuristic_choice]


def run_hill_climbing():
    initial_state = problem.CREATE_INITIAL_STATE()
    print("Initial State:")
    print(problem.DESCRIBE_STATE(initial_state))
    global COUNT, BACKLINKS
    COUNT = 0
    BACKLINKS = {}
    iterative_hill_climbing(initial_state)
    print(str(COUNT) + " states examined.")


def iterative_hill_climbing(initial_state):
    global COUNT, BACKLINKS

    open_states = [initial_state]
    closed_states = []
    BACKLINKS[problem.HASHCODE(initial_state)] = -1

    while open_states:
        s = open_states[0]
        del open_states[0]
        closed_states.append(s)

        if problem.GOAL_TEST(s):
            print(problem.GOAL_MESSAGE_FUNCTION(s))
            backtrace(s)
            return

        COUNT += 1

        L = []
        for op in problem.OPERATORS:
            if op.precond(s):
                new_state = op.state_transf(s)
                if not occurs_in(new_state, closed_states) and open_states.count(new_state) == 0:
                    L.append(new_state)
                    BACKLINKS[problem.HASHCODE(new_state)] = s

        for s2 in L:
            for i in range(len(open_states)):
                if problem.DEEP_EQUALS(s2, open_states[i]):
                    del open_states[i];
                    break

        if len(L) > 0:
            open_states = [random.choice(L)]
        else:
            open_states = []
        if len(open_states) == 0:
            backtrace(s)
            print("Move stuck! Cannot find solution by hill climbing")
            return



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
    for s2 in lst:
        if problem.DEEP_EQUALS(s1, s2): return True
    return False


if __name__ == '__main__':
    run_hill_climbing()
