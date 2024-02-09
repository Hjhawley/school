def generatePermutations(n):
    num_list = list(range(n))
    permutations = []  # Initialize an empty list to store the permutations
    
    while True:
        permutations.append(num_list.copy())
        
        # Find the rightmost number that is smaller than its next number
        i = n - 2
        while i >= 0 and num_list[i] >= num_list[i + 1]:
            i -= 1
        
        # If they are already sorted in decreasing order, we're done
        if i == -1:
            break
        
        # Swap with the rightmost number to the right of 'i' that is greater than it
        j = n - 1
        while num_list[j] <= num_list[i]:
            j -= 1
        num_list[i], num_list[j] = num_list[j], num_list[i]
        
        # Reverse
        num_list[i + 1:] = reversed(num_list[i + 1:])
    
    return permutations  # Return the list of permutations

def printPermutations(permutations):
    for num_list in permutations:
        num_string = "".join(str(i) for i in num_list)  # Convert each permutation to a string
        print(num_string, end=' ')

if __name__ == "__main__":
    def main():
        while True:
            try:
                N = int(input("Give me an integer N between 1 and 9: "))
                if 1 <= N <= 9:
                    perms = generatePermutations(N)
                    printPermutations(perms)
                    print()
                else:
                    print("N must be between 1 and 9.")
            except ValueError:
                print("Please enter a valid integer.")

    main()