#
# Pseudo-code, not actual Python code
#
INFINITY = 1.e10


def SimulatedAnnealing(s0, model):
    """
    Find state with smallest obtainable objective function value.
    """
    current_state = s0
    T = model.T0
    while T > model.Tmin:
        best_objective = INFINITY
        best_neighbor = None
        for neighbor in model.RANDOM_NEIGHBOR(current_state):
            if model.OBJECTIVE(neighbor) < best_objective:
                best_objective = model.OBJECTIVE(neighbor)
                best_neighbor = neighbor
                break
            else:
                delta = model.OBJECTIVE(current_state) - model.OBJECTIVE(neighbor)
                # < 0
                if random.random() < math.exp(delta / T):
                    best_objective = model.OBJECTIVE(neighbor)
                    best_neighbor = neighbor
                    break
                
        current_state = best_neighbor
        T = model.SCHEDULE(T)
    return current_state


def FirstChoiceHillClimbing(s0, model):
    """
    Find state with largest obtainable objective function value.
    """
    current_state = s0
    while True:
        best_objective = -INFINITY
        best_neighbor = None
        for neighbor in model.RANDOM_NEIGHBOR(current_state):
            if model.OBJECTIVE(neighbor) > best_objective:
                best_objective = model.OBJECTIVE(neighbor)
                best_neighbor = neighbor
                break
        if best_objective > model.OBJECTIVE(current_state):
            current_state = best_neighbor
        else:
            break
    return current_state

def StochasticHillClimbing(s0, model):
    """
    Find state with largest obtainable objective function value.
    """
    current_state = s0
    while True:
        best_objective = -INFINITY
        best_neighbor = None
        neighbor = random.choice(model.UPHILL_NEIGHBORS(current_state))
        if model.OBJECTIVE(neighbor) > model.OBJECTIVE(current_state):
            current_state = neighbor
        else:
            break
    return current_state

def HillClimbing(s0, model):
    """
    Find state with largest obtainable objective function value.
    """
    current_state = s0
    while True:
        best_objective = -INFINITY
        best_neighbor = None

        for neighbor in model.NEIGHBORS(current_state):
            if model.OBJECTIVE(neighbor) > best_objective:
                best_objective = model.OBJECTIVE(neighbor)
                best_neighbor = neighbor
        if best_objective > model.OBJECTIVE(current_state):
            current_state = best_neighbor
        else:
            break
    return current_state


def RandomRestartHillClimbing(model):
    """
    Repeatedly execute HillClimbing() on random starting states.
    """
    best_peak = None
    #while model.OBJECTIVE(best_peak) < model.desired_objective:
    for i in range(model.desired_restarts):
        s0 = model.RANDOM_STATE()
        peak = HillClimbing(s0, model)
        if model.OBJECTIVE(peak) > model.OBJECTIVE(best_peak):
            best_peak = peak
    return best_peak
