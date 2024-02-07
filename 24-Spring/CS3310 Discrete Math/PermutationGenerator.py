def generatePermutations(n):
    num_list = list(range(n))
    
    while True:
        printPermutations(num_list)
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

def printPermutations(num_list):
    num_string = ""
    for i in num_list:
        num_string += str(i)
    print(num_string, end=' ')

def main():
    while True:
        try:
            N = int(input("Give me an integer N between 1 and 9: "))
            if 1 <= N <= 9:
                generatePermutations(N)
                print()
            else:
                print("N must be between 1 and 9.")
        except ValueError:
            print("Please enter a valid integer.")

main()