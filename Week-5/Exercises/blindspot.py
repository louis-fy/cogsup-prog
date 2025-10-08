from expyriment import design, control, stimuli
from expyriment.misc.constants import C_WHITE, C_BLACK, K_SPACE, K_DOWN, K_UP, K_LEFT, K_RIGHT

""" Global settings """
exp = design.Experiment(name="Blindspot", background_colour=C_WHITE, foreground_colour=C_BLACK)
control.set_develop_mode()
control.initialize(exp)

""" Stimuli """
def make_circle(r, pos=(0,0)):
    c = stimuli.Circle(r, position=pos, anti_aliasing=10)
    c.preload()
    return c

""" Experiment """
def run_trial():
    fixation = stimuli.FixCross(size=(150, 150), line_width=10, position=[300, 0])
    fixation.preload()

    radius = 75
    circle = make_circle(radius)

    fixation.present(True, False)
    circle.present(False, True)
    
    while True:
        key, _ = exp.keyboard.wait(keys=[K_DOWN, K_UP, K_LEFT, K_RIGHT, K_SPACE, 49, 50])
        coords = {K_DOWN:(0,-10), K_UP:(0,10), K_LEFT:(-10,0), K_RIGHT:(10,0)}
        if key == K_SPACE:
            break
        elif key in [49, 50]:
            circle = make_circle(circle.radius-circle.radius//10, circle.position) if key == 49 else make_circle(circle.radius*1.1, circle.position)
        else:
            circle.move(coords[key])
        draw([fixation, circle])
    
def draw(stims):
    for i, stim in enumerate(stims):
        stim.present(clear=(i == 0), update=(i == len(stims) - 1))

control.start(subject_id=1)

run_trial()
    
control.end()