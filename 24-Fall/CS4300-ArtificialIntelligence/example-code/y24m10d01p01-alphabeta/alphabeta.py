# pseudo code

def MINIMAX(initial_state, model):
    alpha = -INFINITY
    beta = INFINITY
    best_value = -INFINITY
    best_action = None
    for action in model.ACTIONS(current_state):
        next_state = model.RESULTS(current_state, action)
        value = MIN(next_state, model, depth+1, alpha, beta)
        if value > best_value:
            best_value = value
            best_action = action
            if best_value > beta:
                break
            if best_value > alpha:
                alpha = best_value
    return best_action
    

def MAX(current_state, model, depth, alpha, beta):
    if depth >= cutoff_depth or model.GAME_OVER(current_state):
        return model.EVALUATE(current_state)
    best_value = -INFINITY
    for action in model.ACTIONS(current_state):
        next_state = model.RESULTS(current_state, action)
        value = MIN(next_state, model, depth+1, alpha, beta)
        if value > best_value:
            best_value = value
            if best_value > beta:
                break
            if best_value > alpha:
                alpha = best_value
    return best_value

def MIN(current_state, model, depth, alpha, beta):
    if depth >= cutoff_depth or model.GAME_OVER(current_state):
        return model.EVALUATE(current_state)
    best_value = INFINITY
    for action in model.ACTIONS(current_state):
        next_state = model.RESULTS(current_state, action)
        value = MAX(next_state, model, depth+1, alpha, beta)
        if value < best_value:
            best_value = value
            if best_value < alpha:
                break
            if best_value < beta:
                beta = best_value
    return best_value


    
