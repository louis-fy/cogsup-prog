from expyriment import design, control, stimuli

#control.set_develop_mode()

exp = design.Experiment(name = "Display Edges")
control.initialize(exp)

w, h = exp.screen.size # Get screen dimensions
sl = round(w*.05) # Square side length
squares = []
# For each screen corner, create a square of length 'sl' and line width 1
for corner in [(-(w-sl)//2,-(h-sl)//2),(-(w-sl)//2,(h-sl)//2),((w-sl)//2,-(h-sl)//2),((w-sl)//2,(h-sl)//2)]:
    squares.append(stimuli.Rectangle(position=corner,size=(sl,sl),colour='red',line_width=1))

control.start()

# Present the squares, updating the screen at the end
squares[0].present(clear=True, update=False)
squares[1].present(clear=False, update=False)
squares[2].present(clear=False, update=False)
squares[3].present(clear=False, update=True)

exp.keyboard.wait()

control.end()