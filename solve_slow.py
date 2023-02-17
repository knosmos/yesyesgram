import copy

def generate_lines(rules, rem):
    space_needed = sum(rules) + len(rules) - 1 # how many more spaces we need to fill black strings
    for left_pad in range(rem - space_needed + 1):
        if len(rules) == 1:
            yield [0] * left_pad + [1] * rules[0] + [0] * (rem - left_pad - rules[0])
        else:
            for soln in generate_lines(rules[1:], rem - left_pad - rules[0] - 1):
                yield [0] * left_pad + [1] * rules[0] + [0] + soln

def solve_line(rules, length):
    # try to reduce each line, filling in things that must be true
    # generate all possible solutions
    line = [2] * length
    n = 0
    for soln in generate_lines(rules, length):
        for i, val in enumerate(soln):
            if line[i] == 2 or line[i] == val:
                line[i] = val
            else:
                line[i] = 3 # contested
        n += 1
    print(n, "solutions generated")
    for i, val in enumerate(line):
        if val == 3:
            line[i] = 2
    print(line)
    return line

def is_valid(line, rules):
    curr_rule = 0
    curr_count = 0
    on_black = False
    for val in line:
        if val == 2:
            return True
        if val == 1:
            on_black = True
            curr_count += 1
        elif val == 0:
            if on_black:
                on_black = False
                if curr_rule >= len(rules) or curr_count != rules[curr_rule]:
                    return False
                curr_rule += 1
                curr_count = 0
    if on_black:
        if curr_rule != len(rules) - 1 or curr_count != rules[curr_rule]:
            #print("last rule failed", curr_rule, curr_count, rules)
            return False
    return True

def solve(left, top):
    # initialize
    grid = [
        [2 for i in range(len(top))]
        for j in range(len(left))
    ] # grid[row][col]
    # 2 = unknown, 0 = white, 1 = black

    # solve rows
    for i, row in enumerate(left):
        grid[i] = solve_line(row, len(top))
        #print(i, grid[i])
    
    # solve columns
    for i, col in enumerate(top):
        col = solve_line(col, len(left))
        for j, val in enumerate(col):
            if grid[j][i] == 2 or grid[j][i] == val:
                grid[j][i] = val
            else:
                grid[j][i] = 3
        for j, val in enumerate(grid):
            if val[i] == 3:
                val[i] = 2
        #print(i, col)
    
    print_grid(grid)
    
    # backtracking
    curr = 0
    grid_solved = copy.deepcopy(grid)
    #print(grid_solved)
    while curr < len(grid) * len(grid[0]):
        row = curr // len(grid[0])
        col = curr % len(grid[0])
        #print(curr, row, col, grid)
        if grid_solved[row][col] != 2: # skip if solved in preliminary steps 
            curr += 1
        else:
            if grid[row][col] == 2:
                grid[row][col] = 0
            elif grid[row][col] == 0:
                grid[row][col] = 1
            elif grid[row][col] == 1: # nothing here works, backtrack
                grid[row][col] = 2
                curr -= 1
                row = curr // len(grid[0])
                col = curr % len(grid[0])
                while grid_solved[row][col] != 2:
                    curr -= 1
                    row = curr // len(grid[0])
                    col = curr % len(grid[0])
                    #print("decrementing to", curr, row, col, grid)
                continue
            
            # check if this is a valid solution
            if is_valid(grid[row], left[row]) and is_valid([grid[j][col] for j in range(len(grid))], top[col]):
                curr += 1
                #print("incrementing to", curr, grid)
        if curr < 0:
            raise Exception("You messed up")
    return grid

def print_grid(grid):
    print("\n".join("".join("X" if val == 1 else "." if val == 0 else "?" for val in row) for row in grid))

if __name__ == "__main__":
    '''
    print_grid(
        solve(
            [[2],[1],[3],[3],[2,1]],
            [[1],[3],[2],[5],[1]]
        )
    )
    '''
    '''
    print_grid(
        solve(
            [[2,1,1,2],[11],[7],[3],[1]],
            [[1],[2],[3],[2],[4],[4],[4],[2],[3],[2],[1]]
        )
    )
    '''
    print_grid(
        solve(
            [[14],[1,1],[1,3,4,1],[1,1,1,1],[1,3,4,1],[1,1],[1,8,1],[1,1],[14],[2],[2],[6],[6]],
            [[9],[1,1],[1,3,1],[1,1,1,1,1],[1,3,1,1,2],[1,1,1,2],[1,1,5],[1,1,5],[1,1,1,1,1,2],[1,1,1,1,1,2],[1,1,1,1,1],[1,1,1,1],[1,1],[9]]
        )
    )
    #print(list(generate_lines([3], 4)))
    #print(is_valid([0,0,0,1,1], [2]))