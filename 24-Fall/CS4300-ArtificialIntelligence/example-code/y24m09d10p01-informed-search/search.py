


def bfs(s0, model):
    
    Q = fifo_queue()
    Q.push(s0)

    while(len(Q) > 0): # frontier not empty
        s = Q.pop()
        if model.GOAL_TEST(s):
            return sequence_to_reach(s)
        for a in model.ACTIONS(s):
            s1 = model.RESULT(s, a)
            Q.push(s1)
    return False





def sequence_to_reach_r(n):
    if n.parent is None:
        return []
    else:
        return sequence_to_reach_r(n.parent) + [n.action]

def sequence_to_reach(n):
    action_sequence = []
    while n.parent is not None:
        action_sequence.append(n.action)
        n = n.parent
    return action_sequence[::-1]

def bfs(s0, model):
    
    Q = fifo_queue()
    # state, action, parent, depth
    Q.push(Node(s0, None, None, 0))

    while(len(Q) > 0): # frontier not empty
        n = Q.pop()
        if model.GOAL_TEST(n.state):
            return sequence_to_reach(n)
        for a in model.ACTIONS(n.state):
            s1 = model.RESULT(n.state, a)
            Q.push(Node(s1, a, n, 1+n.depth))
    return False














def dfs(s0, model):
    
    Q = lifo_queue()
    Q.push(s0)

    while(len(Q) > 0): # frontier not empty
        s = Q.pop()
        if model.GOAL_TEST(s):
            return sequence_to_reach(s)
        for a in model.ACTIONS(s):
            s1 = model.RESULT(s, a)
            Q.push(s1)
    return False















        
        
    

def uniform_cost_search(s0, model):
    # (state, parent, action, depth, cost)
    n0 = (s0, None, None, 0, 0.0)
    
    Q = priority_queue() # min-heap on cost
    Q.push(n0)

    while(len(Q) > 0): # frontier not empty
        n = Q.pop() # pops the node with the least cost
        (s, p, a, d, c) = n
        if model.GOAL_TEST(s):
            return sequence_to_reach(n)
        for a in model.ACTIONS(s):
            s1 = model.RESULT(s, a)
            n1 = (s1, n, a, d+1, c+model.STEP_COST(s, a, s1))
            Q.push(n1)
    return False


def greedy_search(s0, model):
    # (state, parent, action, depth, cost, heuristic)
    n0 = (s0, None, None, 0, 0.0, model.HEURISTIC(s0))
    
    Q = priority_queue() # min-heap on heuristic
    Q.push(n0)

    while(len(Q) > 0): # frontier not empty
        n = Q.pop() # pops the node with the least heuristic
        (s, p, a, d, c, h) = n
        if model.GOAL_TEST(s):
            return sequence_to_reach(n)
        for a in model.ACTIONS(s):
            s1 = model.RESULT(s, a)
            n1 = (s1, n, a, d+1, c+model.STEP_COST(s, a, s1), model.HEURISTIC(s1))
            Q.push(n1)
    return False



def astar_search(s0, model):
    # (state, parent, action, depth, cost, heuristic)
    n0 = (s0, None, None, 0, 0.0, model.HEURISTIC(s0))
    
    Q = priority_queue() # min-heap on cost+heuristic
    Q.push(n0)

    while(len(Q) > 0): # frontier not empty
        n = Q.pop() # pops the node with the least heuristic
        (s, p, a, d, c, h) = n
        if model.GOAL_TEST(s):
            return sequence_to_reach(n)
        for a in model.ACTIONS(s):
            s1 = model.RESULT(s, a)
            n1 = (s1, n, a, d+1, c+model.STEP_COST(s, a, s1), model.HEURISTIC(s1))
            Q.push(n1)
    return False






def astar_graph_search(s0, model):
    # (state, parent, action, depth, cost, heuristic)
    n0 = (s0, None, None, 0, 0.0, model.HEURISTIC(s0))
    closed_list = empty_store()
    
    Q = priority_queue() # min-heap on cost+heuristic
    Q.push(n0)
    closed_list.add(s0)

    while(len(Q) > 0): # frontier not empty
        n = Q.pop() # pops the node with the least heuristic
        (s, p, a, d, c, h) = n
        if model.GOAL_TEST(s):
            return sequence_to_reach(n)
        for a in model.ACTIONS(s):
            s1 = model.RESULT(s, a)
            if s1 not in closed_list:
                n1 = (s1, n, a, d+1, c+model.STEP_COST(s, a, s1), model.HEURISTIC(s1))
                Q.push(n1)
                closed_list.add(s1)
    return False





