#!/usr/bin/env python3

import sys
import n_queens
import local_search
import logging
import argparse

def parse_args(argv):
    parser = argparse.ArgumentParser(prog=argv[0], description='Run Local Search on the N-Queens problem.')
    parser.add_argument('action', default='hillclimb',
                        choices=[ "hillclimb", "neighbor-count" ],
                        nargs='?', help="desired action")
    parser.add_argument(
        "--queen-count",
        "-q",
        type=int, 
        help="number of queens",
        default=4
    )
    parser.add_argument(
        "--logging-level",
        "-l",
        type=str,
        help="logging level: warn, info, debug",
        choices=("warn", "info", "debug"),
        default="warn",
    )
    parser.add_argument(
        "--restarts",
        "-r",
        type=int, 
        help="maximum restarts (default is infinite)",
        default=0
    )
    parser.add_argument(
        "--utility",
        "-u",
        type=float, 
        help="desired utility (default use restart count)",
        default=-local_search.INFINITY
    )
    parser.add_argument(
        "--neighbors-mode",
        "-n",
        type=str, 
        help="mode for selecting neighbors",
        choices=("all-rows", "next-row"),
        default="all-rows"
    )


    my_args = parser.parse_args(argv[1:])
    if my_args.logging_level == "warn":
        my_args.logging_level = logging.WARN
    elif my_args.logging_level == "info":
        my_args.logging_level = logging.INFO
    elif my_args.logging_level == "debug":
        my_args.logging_level = logging.DEBUG

    return my_args

def set_neighbor_mode(my_args, model):
    if my_args.neighbors_mode == "all-rows":
        model.set_neighbors_all_rows()
    elif my_args.neighbors_mode == "next-row":
        model.set_neighbors_next_row()
    return

def hillclimb(my_args):
    model = n_queens.NQueensProblem(my_args.queen_count)
    set_neighbor_mode(my_args, model)
    solution = local_search.RandomRestartHillClimbing(model, my_args.restarts, my_args.utility)
    print(solution, model.UTILITY(solution))
    return

def neighbor_count(my_args):
    model = n_queens.NQueensProblem(my_args.queen_count)
    set_neighbor_mode(my_args, model)
    s0 = model.RANDOM_STATE()
    neighbors = model.NEIGHBORS(s0)
    print("Neighbor count: ", len(neighbors))
    return

def main(argv):
    my_args = parse_args(argv)
    logging.basicConfig(level=my_args.logging_level)
    actions = {
        "hillclimb": hillclimb,
        "neighbor-count": neighbor_count,
    }
    if my_args.action in actions:
        actions[my_args.action](my_args)
    else:
        raise Exception("{} not in known actions.".format(my_args.action))

    return

if __name__ == "__main__":
    main(sys.argv)
