from expyriment import design, control, stimuli
from expyriment.misc.constants import C_GREY

#control.set_develop_mode()

exp = design.Experiment(name = "Kanizsa Rectangle", background_colour=C_GREY)
control.initialize(exp)

def get_kanizsa(ratio,sf_rec,sf_c):
    w, _ = exp.screen.size # Get screen width; height is unimportant
    x = (w*sf_rec)//2 # Determine |x| for each corner of the rectangle
    y = x//ratio # Determine |y| for each corner of the rectangle
    r = round(w*sf_c) # Circle radius
    square = stimuli.Rectangle(size=(2*x,2*y),colour=C_GREY)
    circle1 = stimuli.Circle(position=(-x,-y),radius=r,colour='white',anti_aliasing=10)
    circle2 = stimuli.Circle(position=(x,-y),radius=r,colour='white',anti_aliasing=10)
    circle3 = stimuli.Circle(position=(-x,y),radius=r,colour='black',anti_aliasing=10)
    circle4 = stimuli.Circle(position=(x,y),radius=r,colour='black',anti_aliasing=10)
    return square, [circle1,circle2,circle3,circle4]

square, circles = get_kanizsa(1.5,.25,.05) # Get square and circle stimuli based on given parameters

control.start()

# Present all four circles, followed by the square, updating the screen with the latter
circles[0].present(clear=True, update=False)
circles[1].present(clear=False, update=False)
circles[2].present(clear=False, update=False)
circles[3].present(clear=False, update=False)
square.present(clear=False, update=True)

exp.keyboard.wait()

control.end()