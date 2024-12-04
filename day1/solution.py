def read_input(filename="input"):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f.readlines()]
    
    left_list = []
    right_list = []
    
    for line in lines:
        if not line:  # skip empty lines
            continue
        left, right = line.split()
        left_list.append(int(left))
        right_list.append(int(right))
    
    return left_list, right_list

def calculate_total_distance(left_list, right_list, debug=False):
    # Sort both lists
    left_sorted = sorted(left_list)
    right_sorted = sorted(right_list)
    
    if debug:
        print("Left list sorted:", left_sorted)
        print("Right list sorted:", right_sorted)
    
    # Calculate differences between pairs
    total_distance = 0
    for i, (left, right) in enumerate(zip(left_sorted, right_sorted)):
        distance = abs(left - right)
        if debug:
            print(f"Pair {i+1}: {left} and {right}, distance = {distance}")
        total_distance += distance
    
    return total_distance

def calculate_similarity_score(left_list, right_list, debug=False):
    # Count occurrences in right list
    right_counts = {}
    for num in right_list:
        right_counts[num] = right_counts.get(num, 0) + 1
    
    # Calculate similarity score
    total_score = 0
    for i, num in enumerate(left_list):
        count = right_counts.get(num, 0)
        score = num * count
        if debug:
            print(f"Number {num} appears {count} times in right list: {num} * {count} = {score}")
        total_score += score
    
    return total_score

def main():
    # Test with example input first
    print("Testing with example input:")
    left_list, right_list = read_input("test_input")
    
    print("Part 1:")
    result1 = calculate_total_distance(left_list, right_list, debug=True)
    print(f"Test result for part 1: {result1}")
    print()
    
    print("Part 2:")
    result2 = calculate_similarity_score(left_list, right_list, debug=True)
    print(f"Test result for part 2: {result2}")
    print()
    
    # Now solve with real input
    print("Solving with real input:")
    left_list, right_list = read_input("input")
    result1 = calculate_total_distance(left_list, right_list)
    print(f"Part 1: The total distance between the lists is: {result1}")
    result2 = calculate_similarity_score(left_list, right_list)
    print(f"Part 2: The similarity score is: {result2}")

if __name__ == "__main__":
    main()
