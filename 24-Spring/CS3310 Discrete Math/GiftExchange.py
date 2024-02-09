from PermutationGenerator import generatePermutations

def is_win(perm):
    for i in range(len(perm)):
        if perm[i] == i:    # If i == [i], somebody pulled their own name
            return False
    return True

def main():
    for n in range(2, 11):
        perms = generatePermutations(n)
        total_perms = len(perms)
        wins = sum(is_win(perm) for perm in perms)
        probability = wins / total_perms
        print(f"{n}. {wins} of {total_perms} wins. Probability is {probability}")

main()

'''
The probability seems to approach 1/e (0.3678794...)
as n approaches infinity.
'''