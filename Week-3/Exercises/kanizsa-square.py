from expyriment import design, control, stimuli
from expyriment.misc.constants import C_GREY

#control.set_develop_mode()

exp = design.Experiment(name = "Kanizsa Square", background_colour=C_GREY)
control.initialize(exp)

w, _ = exp.screen.size # Get screen dimensions
d = (w*.25)//2 # Determine the distance to the square's corners
r = round(w*.05) # Get circle radius
square = stimuli.Rectangle(size=(2*d,2*d),colour=C_GREY)
circle1 = stimuli.Circle(position=(-d,-d),radius=r,colour='white',anti_aliasing=10)
circle2 = stimuli.Circle(position=(d,-d),radius=r,colour='white',anti_aliasing=10)
circle3 = stimuli.Circle(position=(-d,d),radius=r,colour='black',anti_aliasing=10)
circle4 = stimuli.Circle(position=(d,d),radius=r,colour='black',anti_aliasing=10)

control.start()

# Present all four circles and the square, updating the screen at the end
circle1.present(clear=True, update=False)
circle2.present(clear=False, update=False)
circle3.present(clear=False, update=False)
circle4.present(clear=False, update=False)
square.present(clear=False, update=True)

exp.keyboard.wait()

control.end()