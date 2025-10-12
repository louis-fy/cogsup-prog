from expyriment import design, control, stimuli
from expyriment.misc.constants import C_WHITE, C_BLACK, K_SPACE, K_DOWN, K_UP, K_LEFT, K_RIGHT

""" Global settings """
exp = design.Experiment(name="Blindspot", background_colour=C_WHITE, foreground_colour=C_BLACK)
control.set_develop_mode()
control.initialize(exp)
exp.add_data_variable_names(['eye','keypress','radius','x_coord','y_coord'])

""" Stimuli """
def make_circle(r, pos=(0,0)):
    c = stimuli.Circle(r, position=pos, anti_aliasing=10)
    c.preload()
    return c

def circle_error(fixation):
    error = stimuli.TextLine(text='Circle cannot exit the screen.', text_bold=True, text_colour='black')
    draw([error, fixation])
    exp.clock.wait(1000)

def draw(stims):
    for i, stim in enumerate(stims):
        stim.present(clear=(i == 0), update=(i == len(stims) - 1))

def instruction_screen(side):
    eyes = ['right', 'left'] if side == 'L' else ['left', 'right']
    instructions = stimuli.TextScreen(heading='Find your blind spot', text=
                                      f'''We\'re now going to find your {eyes[1]} blind spot!
                                      
                                      When the task starts, cover your {eyes[0]} eye and stare at the fixation cross on the screen.
                                      
                                      To find your blind spot, move the circle using the arrows on your keyboard until the circle seems to disappear from sight. You can also change its size using the number keys '1' (smaller) and '2' (larger).
                                      
                                      When you've found your blind spot, press 'SPACE' to end the task.
                                      
                                      Press 'SPACE' when you're ready to begin.''', 
                                      heading_bold=True, heading_colour='black', text_colour='black', text_justification=0)
    instructions.present(clear=True, update=True)
    exp.keyboard.wait(keys=K_SPACE)

""" Experiment """
def add_data(side, key, keys, circle):
    exp.data.add(['left' if side == 'L' else 'right',
                  keys[key],
                  circle.radius,
                  circle.position[0],
                  circle.position[1]])

def run_trial(side='L'):
    w, h = exp.screen.size
    if side == 'L':
        fixation = stimuli.FixCross(size=(150, 150), line_width=10, position=[300, 0])
        instruction_screen('L')
    elif side == 'R':
        fixation = stimuli.FixCross(size=(150, 150), line_width=10, position=[-300, 0])
        instruction_screen('R')
    else:
        raise ValueError('Invalid side input.')
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
        elif key == 49:
            circle = make_circle(circle.radius-circle.radius//10, circle.position)
        elif key == 50:
            if w//2 < circle.radius*1.1 + abs(circle.position[0]) or h//2 < circle.radius*1.1 + abs(circle.position[1]):
                circle_error(fixation)
            else:
                circle = make_circle(circle.radius*1.1, circle.position)
        else:
            if w//2 < circle.radius + abs(circle.position[0]+coords[key][0]) or h//2 < circle.radius + abs(circle.position[1]+coords[key][1]):
                circle_error(fixation)
            else:
                circle.move(coords[key])
        add_data(side, key, {K_DOWN:'down', K_UP:'up', K_LEFT:'left', K_RIGHT:'right', 49:'1', 50:'2'}, circle)
        draw([fixation, circle])

control.start(subject_id=1)

for trial in ['L','R']:
    run_trial(trial)
    
control.end()