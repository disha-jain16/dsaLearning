# Langton's Ant Simulation  
  
# Directions: 0=up, 1=right, 2=down, 3=left  
directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  
  
def langtons_ant(steps):  
    grid = {}  
    x, y = 0, 0  
    direction = 0  # start facing up  
  
    for step in range(steps):  
        # Determine current color (white by default)  
        color = grid.get((x, y), 0)  
  
        if color == 0:  # white square  
            direction = (direction + 1) % 4  # turn right  
            grid[(x, y)] = 1  # flip to black  
        else:  # black square  
            direction = (direction - 1) % 4  # turn left  
            grid[(x, y)] = 0  # flip to white  
  
        dx, dy = directions[direction]  
        x += dx  
        y += dy  
  
        print(f"Step {step+1}: Position=({x},{y}), Direction={direction}")  
  
    return grid  
  
# Run simulation  
steps = int(input("Enter number of steps: "))  
final_grid = langtons_ant(steps)  
