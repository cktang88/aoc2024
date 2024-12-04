def read_input():
    with open("input", "r") as f:
        return [line.strip() for line in f.readlines()]


def find_xmas(grid):
    rows = len(grid)
    cols = len(grid[0])
    count = 0

    # All possible directions: right, down-right, down, down-left, left, up-left, up, up-right
    directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

    def check_direction(row, col, dx, dy):
        if not (0 <= row + 3 * dx < rows and 0 <= col + 3 * dy < cols):
            return False
        word = ""
        for i in range(4):
            word += grid[row + i * dx][col + i * dy]
        return word == "XMAS"

    for i in range(rows):
        for j in range(cols):
            for dx, dy in directions:
                if check_direction(i, j, dx, dy):
                    count += 1

    return count


def find_xmas_part2(grid):
    rows = len(grid)
    cols = len(grid[0])
    count = 0

    def check_diagonal(i1, j1, i2, j2):
        if not (0 <= i1 < rows and 0 <= j1 < cols and 
                0 <= i2 < rows and 0 <= j2 < cols):
            return False
        return ((grid[i1][j1] == 'M' and grid[i2][j2] == 'S') or
                (grid[i1][j1] == 'S' and grid[i2][j2] == 'M'))

    # Check each possible center point (must be 'A')
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if grid[i][j] != 'A':
                continue
            
            # Check if both diagonals form M-S patterns
            if (check_diagonal(i-1, j-1, i+1, j+1) and  # top-left to bottom-right
                check_diagonal(i-1, j+1, i+1, j-1)):    # top-right to bottom-left
                count += 1

    return count


def main():
    grid = read_input()
    result1 = find_xmas(grid)
    print(f"Part 1: XMAS appears {result1} times in the word search.")
    result2 = find_xmas_part2(grid)
    print(f"Part 2: X-MAS appears {result2} times in the word search.")


if __name__ == "__main__":
    main()
