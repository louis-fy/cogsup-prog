from expyriment import design, control, stimuli
from expyriment.misc.constants import C_WHITE, C_BLACK, K_j, K_f
import random, itertools

""" Constants """
keys = [K_f, K_j]
pictures = {'cheese':'Week-7/stimuli/cheese.jpg',
            'couch':'Week-7/stimuli/couch.jpg',
            'dog':'Week-7/stimuli/dog.jpg',
            'farm':'Week-7/stimuli/farm.jpg',
            'fruits':'Week-7/stimuli/fruits.jpg',
            'gorilla':'Week-7/stimuli/gorilla.jpg',
            'holding_hands':'Week-7/stimuli/holding_hands.jpg',
            'kid_bicycle':'Week-7/stimuli/kid_bicycle.jpg',
            'old_building':'Week-7/stimuli/old_building.jpg',
            'shoes':'Week-7/stimuli/shoes.jpg',
            'socks':'Week-7/stimuli/socks.jpg',
            'windmill':'Week-7/stimuli/windmill.jpg'}
positions = [(-165, 115), (165, 115), (165, -115), (-165, -115)]
grid_placement = [[1, 1, 1, 1], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0], 
                  [0, 0, 1, 1], [0, 1, 0, 1], [0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 1, 0], 
                  [1, 1, 0, 0], [0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]]
n_trials = 75
start_instructions = "Test"
post_practice_instructions = "Test"
end_instructions = "Test"

""" Helper functions """
def load(stims):
    for stim in stims:
        stim.preload()

def timed_draw(*stims):
    t0 = exp.clock.time
    exp.screen.clear()
    for stim in stims:
        stim.present(clear=False, update=False)
    exp.screen.update()
    t1 = exp.clock.time
    return t1 - t0

def present_for(*stims, t=1000):
    dt = timed_draw(*stims)
    exp.clock.wait(t - dt)

def present_instructions(text):
    instructions = stimuli.TextScreen(text=text, text_justification=0, heading="Instructions")
    instructions.present()
    exp.keyboard.wait()

def find_derangements(lst):
    derangements = []
    for perm in itertools.permutations(lst):
        if all(original != perm[i] for i, original in enumerate(lst)):
            derangements.append(perm)
    return derangements

""" Global settings """
exp = design.Experiment(name="RSVP Memory Test", background_colour=C_BLACK, foreground_colour=C_WHITE)
exp.add_data_variable_names(['trial_n', 'trial_type', 'n_stims', 'stim_position', 'stim_type', 'RT', 'correct'])

control.set_develop_mode()
control.initialize(exp)

""" Stimuli """
def get_trials():
    placement = grid_placement * (n_trials * 6 // len(grid_placement))
    random.shuffle(placement)
    trials = []
    for i in range(len(placement) - 4):
        trial_grids = placement[i:i+4]
        trial_pictures = []
        while trial_pictures == []:
            sample = random.sample(pictures)
            if len(sample) == len(set(sample.keys())):
                trial_pictures = sample
        

    return trials

fixation = stimuli.FixCross(colour=C_WHITE)
fixation.preload()

print(find_derangements([pictures.keys]))
