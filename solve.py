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
    # get all possible solutions
    lines = [line for line in generate_lines(rules, length)]
    print(len(lines), "solutions generated")
    return lines

def is_line_valid(line, rules):
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

def is_grid_valid(grid, left, top):
    for i, row in enumerate(grid):
        if not is_line_valid(row, left[i]):
            return False
    for i, col in enumerate(top):
        if not is_line_valid([row[i] for row in grid], col):
            return False
    return True

def solve(left, top):
    # initialize
    grid = [
        [2 for i in range(len(top))]
        for j in range(len(left))
    ] # grid[row][col]
    
    # 2 = unknown, 0 = white, 1 = black

    solns = [solve_line(left[i], len(top)) for i in range(len(left))]

    curr = 0
    curr_solns = [-1 for i in range(len(left))]

    while curr < len(grid):
        curr_solns[curr] += 1
        if curr_solns[curr] >= len(solns[curr]):
            curr_solns[curr] = -1
            grid[curr] = [2 for i in range(len(top))]
            curr -= 1
            continue
        grid[curr] = solns[curr][curr_solns[curr]]
        if is_grid_valid(grid, left, top):
            curr += 1
        if curr < 0:
            raise Exception("You messed up")
    return grid

def print_grid(grid):
    print("\n".join("".join("██" if val == 1 else ".." if val == 0 else "?" for val in row) for row in grid))

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