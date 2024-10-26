# pseudo code

def MINIMAX(initial_state, model):
    best_value = -INFINITY
    best_action = None
    for action in model.ACTIONS(current_state):
        next_state = model.RESULTS(current_state, action)
        value = MIN(next_state, model, depth+1)
        if value > best_value:
            best_value = value
            best_action = action
    return best_action
    

def MAX(current_state, model, depth):
    if depth >= cutoff_depth or model.GAME_OVER(current_state):
        return model.EVALUATE(current_state)
    best_value = -INFINITY
    for action in model.ACTIONS(current_state):
        next_state = model.RESULTS(current_state, action)
        value = MIN(next_state, model, depth+1)
        if value > best_value:
            best_value = value
    return best_value

def MIN(current_state, model, depth):
    if depth >= cutoff_depth or model.GAME_OVER(current_state):
        return model.EVALUATE(current_state)
    best_value = INFINITY
    for action in model.ACTIONS(current_state):
        next_state = model.RESULTS(current_state, action)
        value = MAX(next_state, model, depth+1)
        if value < best_value:
            best_value = value
    return best_value


    
