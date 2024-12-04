def read_input(filename="input"):
    with open(filename, "r") as f:
        return [list(map(int, line.strip().split())) for line in f.readlines()]

def is_safe_report(levels):
    if len(levels) < 2:
        return True
        
    # Check first difference to determine if we should be increasing or decreasing
    first_diff = levels[1] - levels[0]
    if abs(first_diff) < 1 or abs(first_diff) > 3:
        return False
    
    increasing = first_diff > 0
    
    # Check all adjacent pairs
    for i in range(1, len(levels)):
        diff = levels[i] - levels[i-1]
        
        # Check if difference is between 1 and 3
        if abs(diff) < 1 or abs(diff) > 3:
            return False
            
        # Check if direction matches the first difference
        if (increasing and diff <= 0) or (not increasing and diff >= 0):
            return False
    
    return True

def is_safe_with_dampener(levels):
    # First check if it's safe without removing any level
    if is_safe_report(levels):
        return True, None
    
    # Try removing each level one at a time
    for i in range(len(levels)):
        # Create new list without level i
        dampened_levels = levels[:i] + levels[i+1:]
        if is_safe_report(dampened_levels):
            return True, i
    
    return False, None

def count_safe_reports(reports, use_dampener=False):
    if not use_dampener:
        return sum(1 for report in reports if is_safe_report(report))
    else:
        return sum(1 for report in reports if is_safe_with_dampener(report)[0])

def main():
    # Test with example input first
    print("Testing with example input:")
    test_input = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""
    
    with open("test_input", "w") as f:
        f.write(test_input)
    
    test_reports = read_input("test_input")
    
    # Part 1 tests
    print("Part 1:")
    for i, report in enumerate(test_reports, 1):
        safe = is_safe_report(report)
        print(f"Report {i}: {report} - {'Safe' if safe else 'Unsafe'}")
    
    test_result1 = count_safe_reports(test_reports)
    print(f"\nPart 1 test result: {test_result1} safe reports")
    if test_result1 == 2:
        print("✓ Part 1 test passed!")
    else:
        print("✗ Part 1 test failed!")
    print()
    
    # Part 2 tests
    print("Part 2:")
    for i, report in enumerate(test_reports, 1):
        safe, removed_idx = is_safe_with_dampener(report)
        status = "Safe"
        if safe and removed_idx is not None:
            status = f"Safe by removing index {removed_idx} (value {report[removed_idx]})"
        elif not safe:
            status = "Unsafe"
        print(f"Report {i}: {report} - {status}")
    
    test_result2 = count_safe_reports(test_reports, use_dampener=True)
    print(f"\nPart 2 test result: {test_result2} safe reports")
    if test_result2 == 4:
        print("✓ Part 2 test passed!")
    else:
        print("✗ Part 2 test failed!")
    print()
    
    # Now solve with real input
    print("Solving with real input:")
    reports = read_input("input")
    result1 = count_safe_reports(reports)
    print(f"Part 1: Number of safe reports: {result1}")
    result2 = count_safe_reports(reports, use_dampener=True)
    print(f"Part 2: Number of safe reports with Problem Dampener: {result2}")

if __name__ == "__main__":
    main()
