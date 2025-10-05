from expyriment import design, control, stimuli
from expyriment.misc.constants import K_SPACE, C_WHITE

def present_for(stims, t=200):
    if not stims:
        raise ValueError('Simuli list must be nonempty.')
    t0 = exp.clock.time
    exp.screen.clear()
    for stim in stims:
        stim.present(clear=False, update=False)
    exp.screen.update()
    t1 = exp.clock.time
    exp.clock.wait(t - (t1 - t0))

def make_circles(radius, w):
    inter_circle = radius // 5
    if (radius * 8 + inter_circle * 3) > w:
        raise ValueError('Circle radius too large.')
    if radius <= 0:
        raise ValueError('Circle radius must be positive and non-null.')
    circle1 = stimuli.Circle(radius=radius, position=(-(3*radius + 3*inter_circle//2), 0), colour='black', anti_aliasing=10)
    circle2 = stimuli.Circle(radius=radius, position=(-(radius + inter_circle//2), 0), colour='black', anti_aliasing=10)
    circle3 = stimuli.Circle(radius=radius, position=(radius + inter_circle//2, 0), colour='black', anti_aliasing=10)
    circle4 = stimuli.Circle(radius=radius, position=(3*radius + 3*inter_circle//2, 0), colour='black', anti_aliasing=10)
    return [circle1, circle2, circle3, circle4]

def add_tags(circles):
    tags = []
    for circle, colour in list(zip(circles, ['yellow','red','green','yellow'])):
        tags.append(circle)
        tags.append(stimuli.Circle(radius=circle.radius // 5, position=circle.position, colour=colour, anti_aliasing=10))
    return tags

def run_trial(radius=75, isi=0, with_tags=False):
    if isi < 0 or not isinstance(isi, int):
        raise ValueError('ISI must be a positive integer.')
    w, _ = exp.screen.size
    wt = isi * 16.67
    circles = add_tags(make_circles(radius, w)) if with_tags else make_circles(radius, w)
    for stim in circles:
        stim.preload()
    exp.screen.clear()
    exp.screen.update()
    sets = [circles[0:6], circles[2:8]] if with_tags else [circles[0:3], circles[1:4]]
    while True:
        if exp.keyboard.check(K_SPACE):
            break
        for set in sets:
            present_for(stims=set)
            if isi > 0:
                t0 = exp.clock.time
                exp.screen.update()
                t1 = exp.clock.time
                exp.clock.wait(wt - (t1 - t0))

exp = design.Experiment(name="Ternus Display", background_colour=C_WHITE)

#control.set_develop_mode()
control.initialize(exp)

trials = [{}, {'isi': 5}, {'with_tags': True, 'isi': 5}]

for trial_param in trials:
    run_trial(**trial_param)

control.end()