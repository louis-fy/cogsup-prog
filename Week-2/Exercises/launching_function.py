from expyriment import design, control, stimuli

#control.set_develop_mode()

def run_launching(temp_gap, space_gap, speed):
    square1.present(clear=True, update=False) # Load the green square without updating the display (but clearing the previous display)
    square2.present(clear=False, update=True) # Present the red square along with the green square and update the display
    exp.clock.wait(1000) # Show this display for 1 second
    while square2.position[0] < space_gap: # As long as the red square is not juxtaposed with the green square, do as follows:
        square2.move(offset=(5,0)) # Move the red square 5 pixels to the right
        square1.present(clear=True, update=False) # Load the green square without updating the display (but clearing the previous display)
        square2.present(clear=False, update=True) # Present the red square along with the green square and update the display
    exp.clock.wait(temp_gap)
    while square1.position[0] < 400: # As long as the green square is not equidistant with the red square's starting position, do as follows:
        square1.move(offset=(speed,0)) # Move the green square 5 pixels to the right
        square2.present(clear=True, update=False) # Load the red square without updating the display (but clearing the previous display)
        square1.present(clear=False, update=True) # Present the green square along with the red square and update the display
    square1.move(offset=(-400,0)) # Reset the position of the green square
    square2.move(offset=(-400-space_gap,0)) # Reset the position of the red square

exp = design.Experiment(name = "Function for launching") # Set up experiment

control.initialize(exp) # Initialise the experiment

square1 = stimuli.Rectangle(size=(50,50),colour='green') # Generate a green square of length 50
square2 = stimuli.Rectangle(size=(50,50),colour='red',position=(-400,0)) # Generate a red square of length 50

control.start(subject_id=1) # Assign an ID to the current iteration

run_launching(0,-50,5) # Run Michottean launching
exp.clock.wait(1000)

run_launching(1000,-50,5) # Run launching with a temporal gap of 1 second
exp.clock.wait(1000)

run_launching(0,-100,5) # Run launching with a spatial gap of 50 pixels
exp.clock.wait(1000)

run_launching(0,-50,15) # Run triggering (at 3x speed)
exp.clock.wait(1000)

control.end()