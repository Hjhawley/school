#
# Pseudo-code, not actual Python code
#
INFINITY = 1.e10


def HillClimbing(s0, model):
    """
    Find state with largest obtainable utility function value.
    """
    current_state = s0
    while True:
        best_utility = -INFINITY
        best_neighbor = None

        for neighbor in model.NEIGHBORS(current_state):
            if model.UTILITY(neighbor) > best_utility:
                best_utility = model.UTILITY(neighbor)
                best_neighbor = neighbor
        if best_utility > model.UTILITY(current_state):
            current_state = best_neighbor
        else:
            break
    return current_state












desired_restarts = 3
def RandomRestartHillClimbing(model):
    """
    Repeatedly execute HillClimbing() on random starting states.
    """
    best_peak = None
    #while model.UTILITY(best_peak) < model.desired_utility:
    for i in range(desired_restarts):
        s0 = model.RANDOM_STATE()
        peak = HillClimbing(s0, model)
        if model.UTILITY(peak) > model.UTILITY(best_peak):
            best_peak = peak
    return best_peak












def StochasticHillClimbing(s0, model):
    """
    Find state with largest obtainable utility function value.
    """
    current_state = s0
    while True:
        uphill_neighbors = model.UPHILL_NEIGHBORS(current_state)
        if not uphill_neighbors:
            break
        neighbor = random.choice(uphill_neighbors)
        current_state = neighbor
    return current_state








def FirstChoiceHillClimbing(s0, model):
    """
    Find state with largest obtainable utility function value.
    """
    current_state = s0
    while True:
        best_utility = model.UTILITY(current_state)
        best_neighbor = None
        for neighbor in model.RANDOM_NEIGHBOR(current_state):
            if model.UTILITY(neighbor) > best_utility:
                best_utility = model.UTILITY(neighbor)
                best_neighbor = neighbor
                break
        if best_utility > model.UTILITY(current_state):
            current_state = best_neighbor
        else:
            break
    return current_state































T0 = 100
Tmin = 0.1

def SCHEDULE(T):
    return f(T)

def SimulatedAnnealing(s0, model):
    """
    Find state with smallest obtainable utility function value.
    """
    current_state = s0
    T = T0
    while T > Tmin:
        best_utility = INFINITY
        best_neighbor = None
        for neighbor in model.RANDOM_NEIGHBOR(current_state):
            if model.UTILITY(neighbor) < best_utility:
                best_utility = model.UTILITY(neighbor)
                best_neighbor = neighbor
                break
            else:
                delta = model.UTILITY(current_state) - model.UTILITY(neighbor)
                # < 0
                if random.random() < math.exp(delta / T):
                    best_utility = model.UTILITY(neighbor)
                    best_neighbor = neighbor
                    break
                
        current_state = best_neighbor
        T = SCHEDULE(T)
    return current_state







