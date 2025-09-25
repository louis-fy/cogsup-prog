from expyriment import design, control, stimuli
from expyriment.misc import constants

#control.set_develop_mode()

def get_grid(w, sq_size, sq_colour, spacing, rows, cols):
    dist = round(w*(sq_size+spacing)) # Determine distance between each square (space between square + side length) relative to screen size
    side = round(w*sq_size) # Determine square side length relative to screen size
    mid_col = (cols-1)/2 # Index of middle column (average of both middle indexes if even)
    mid_row = (rows-1)/2 # Index of middle row (average of both middle indexes if even)
    squares = []
    for i in range(rows):
        for j in range(cols):
            # Square position as a factor of distance from middle row and column
            squares.append(stimuli.Rectangle(position=((j-mid_col)*dist,(i-mid_row)*dist),size=(side,side),colour=sq_colour))
    return squares

def create_exp(sq_size, spacing, sq_colour, back_colour, rows, cols):
    exp = design.Experiment(name = "Hermann Grid Illusion", background_colour=back_colour) # Use given background colour
    control.initialize(exp)
    w, _ = exp.screen.size # Get screen size for square length and spacing
    squares = get_grid(w, sq_size, sq_colour, spacing, rows, cols) # Create a matrix of square stimuli based on given parameters
    return exp, squares

exp, squares = create_exp(.1, .03, constants.C_BLACK, constants.C_WHITE, 5, 5)

control.start()

squares[0].present(clear=True, update=False) # Present the first square, clearing the display
for square in squares[1:-1]: # Present each subsequent square in the matrix without updating the screen
    square.present(clear=False, update=False)
squares[-1].present(clear=False, update=True) # Present the final square, updating the display

exp.keyboard.wait()

control.end()