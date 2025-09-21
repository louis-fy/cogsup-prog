from expyriment import design, control, stimuli

#control.set_develop_mode()

exp = design.Experiment(name = "Triggering") # Set up experiment

control.initialize(exp) # Initialise the experiment

square1 = stimuli.Rectangle(size=(50,50),colour='green') # Generate a green square of length 50
square2 = stimuli.Rectangle(size=(50,50),colour='red',position=(-400,0)) # Generate a red square of length 50

control.start(subject_id=1) # Assign an ID to the current iteration

square1.present(clear=True, update=False) # Load the green square without updating the display (but clearing the previous display)
square2.present(clear=False, update=True) # Present the red square along with the green square and update the display

exp.clock.wait(1000) # Show this display for 1 second

while square2.position[0] < -50: # As long as the red square is not juxtaposed with the green square, do as follows:
    square2.move(offset=(5,0)) # Move the red square 5 pixels to the right
    square1.present(clear=True, update=False) # Load the green square without updating the display (but clearing the previous display)
    square2.present(clear=False, update=True) # Present the red square along with the green square and update the display
while square1.position[0] < 400: # As long as the green square is not equidistant with the red square's starting position, do as follows:
    square1.move(offset=(15,0)) # Move the green square 15 pixels to the right: perceived causality is less obvious
    square2.present(clear=True, update=False) # Load the red square without updating the display (but clearing the previous display)
    square1.present(clear=False, update=True) # Present the green square along with the red square and update the display

exp.clock.wait(1000) # Show this display for 1 second

control.end()