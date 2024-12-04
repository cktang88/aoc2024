import re

def read_input(filename="input"):
    with open(filename, "r") as f:
        return f.read().strip()

def find_multiplications(memory, handle_conditionals=False):
    # Pattern for valid mul(X,Y) where X and Y are 1-3 digit numbers
    mul_pattern = r'mul\((\d{1,3}),(\d{1,3})\)'
    do_pattern = r'do\(\)'
    dont_pattern = r'don\'t\(\)'
    
    # Find all instructions with their positions
    instructions = []
    
    # Find multiplications
    for match in re.finditer(mul_pattern, memory):
        if match.group() == f"mul({match.group(1)},{match.group(2)})":  # Ensure exact match format
            instructions.append(('mul', match.start(), match.groups()))
    
    if handle_conditionals:
        # Find do() instructions
        for match in re.finditer(do_pattern, memory):
            instructions.append(('do', match.start(), None))
        
        # Find don't() instructions
        for match in re.finditer(dont_pattern, memory):
            instructions.append(('dont', match.start(), None))
        
        # Sort instructions by position
        instructions.sort(key=lambda x: x[1])
    
    results = []
    enabled = True  # Multiplications start enabled
    
    for inst_type, _, args in instructions:
        if inst_type == 'mul':
            x, y = map(int, args)
            if not handle_conditionals or enabled:
                results.append((x, y, x * y))
        elif inst_type == 'do':
            enabled = True
        elif inst_type == 'dont':
            enabled = False
    
    return results

def solve_part1(memory):
    multiplications = find_multiplications(memory)
    return sum(result for _, _, result in multiplications)

def solve_part2(memory):
    multiplications = find_multiplications(memory, handle_conditionals=True)
    return sum(result for _, _, result in multiplications)

def main():
    # Test with example input first
    print("Testing with example input:")
    test_input = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)do()?mul(8,5))"
    
    with open("test_input", "w") as f:
        f.write(test_input)
    
    # Test part 1
    print("Part 1:")
    print(f"Input: {test_input}")
    print("\nFound multiplications:")
    multiplications = find_multiplications(test_input)
    for x, y, result in multiplications:
        print(f"mul({x},{y}) = {result}")
    
    test_result1 = solve_part1(test_input)
    print(f"\nPart 1 result (sum of all multiplications): {test_result1}")
    print()
    
    # Test part 2
    print("Part 2:")
    print("Found enabled multiplications:")
    multiplications = find_multiplications(test_input, handle_conditionals=True)
    for x, y, result in multiplications:
        print(f"mul({x},{y}) = {result}")
    
    test_result2 = solve_part2(test_input)
    print(f"\nPart 2 result (sum of enabled multiplications): {test_result2}")
    if test_result2 == 48:
        print("✓ Test passed!")
    else:
        print("✗ Test failed!")
    print()
    
    # Now solve with real input
    print("Solving with real input:")
    memory = read_input("input")
    result1 = solve_part1(memory)
    print(f"Part 1: Sum of all multiplication results: {result1}")
    result2 = solve_part2(memory)
    print(f"Part 2: Sum of enabled multiplication results: {result2}")

if __name__ == "__main__":
    main()
