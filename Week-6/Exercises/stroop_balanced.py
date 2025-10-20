from expyriment import design, control, stimuli
from expyriment.misc.constants import C_WHITE, C_BLACK, K_1, K_2, K_3, K_4
import random, itertools

""" Constants """
KEYS = [K_1, K_2, K_3, K_4]
TRIAL_TYPES = ['match', 'mismatch']
COLOURS = ['red', 'blue', 'green', 'orange']
COLOUR_TO_KEY = {colour:key for colour, key in zip(COLOURS, KEYS)}

N_BLOCKS = 8
N_TRIALS_IN_BLOCK = 128 // N_BLOCKS

INSTR_START = """
In this task, you have to identify the colour of a word on the screen.
Press '1' for red, '2' for blue, '3' for green and '4' for orange.\n
Press SPACE to continue.
"""
INSTR_MID = """Well done! We're going to do that again.\nTake a break then press SPACE to move on to the next block."""
INSTR_END = """Well done!\nPress SPACE to quit the experiment."""

FEEDBACK_CORRECT = """Correct"""
FEEDBACK_INCORRECT = """Incorrect"""

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
exp = design.Experiment(name="Stroop Balanced", background_colour=C_WHITE, foreground_colour=C_BLACK)
exp.add_data_variable_names(['block_cnt', 'trial_cnt', 'trial_type', 'word', 'colour', 'RT', 'correct'])

control.set_develop_mode()
control.initialize(exp)

""" Stimuli """
fixation = stimuli.FixCross()
fixation.preload()

stims = {w: {c: stimuli.TextLine(w, text_colour=c) for c in COLOURS} for w in COLOURS}
load([stims[w][c] for w in COLOURS for c in COLOURS])

feedback_correct = stimuli.TextLine(FEEDBACK_CORRECT)
feedback_incorrect = stimuli.TextLine(FEEDBACK_INCORRECT)
load([feedback_correct, feedback_incorrect])

""" Experiment """
PERMS = find_derangements(COLOURS)

def get_trials(subject_id):
    perm = PERMS[(subject_id - 1) % len(PERMS)]
    base = [{'word': c, 'colour': c} for c in COLOURS] + [{'word': w, 'colour': c} for w, c in zip(COLOURS, perm)]
    block_reps = N_TRIALS_IN_BLOCK // len(base)
    trials = []
    for i in range(1, N_BLOCKS + 1):
        block = base * block_reps
        random.shuffle(block)
        for j, trial in enumerate(block, 1):
            trials.append(
                {'subject_id': subject_id, 'block_id': i, 'trial_id': j, 'trial_type': 'match' if trial['word'] == trial['colour'] else 'mismatch',
                 'word': trial['word'], 'colour': trial['colour'], 'correct_key': COLOUR_TO_KEY[trial['colour']]}
            )
    return trials

def run_trial(subject_id, block_id, trial_id, trial_type, word, colour, correct_key):
    stim = stims[word][colour]
    present_for(fixation, t=500)
    stim.present()
    key, rt = exp.keyboard.wait(KEYS)
    correct = key == correct_key
    exp.data.add([subject_id, block_id, trial_id, trial_type, word, colour, rt, correct])
    feedback = feedback_correct if correct else feedback_incorrect
    present_for(feedback, t=1000)

control.start(subject_id=1)

present_instructions(INSTR_START)

for trial in get_trials(exp.subject):
    if trial['trial_id'] == 1 and trial['block_id'] != 1:
        present_instructions(INSTR_MID)
    run_trial(**trial)

present_instructions(INSTR_END)

control.end()