from expyriment import design, control, stimuli
from expyriment.misc.constants import C_WHITE, C_BLACK, K_j, K_f
import random, itertools

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
n_trials = 75
picture_themes = [theme for theme in pictures.keys()]

def find_derangements(lst):
    derangements = []
    for grid in lst:
        derangements.append(grid)
        for perm in itertools.permutations(grid):
            if list(perm) not in derangements:
                derangements.append(list(perm))
    return derangements

print(picture_themes)
random.shuffle(picture_themes)
print(picture_themes[:8], picture_themes[8:])

grid_placement = [[1, 1, 1, 1], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0], 
                  [0, 0, 1, 1], [0, 1, 0, 1], [0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 1, 0], 
                  [1, 1, 0, 0], [0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]]
grid_trials = grid_placement * 3
random.shuffle(grid_trials)
print(grid_trials)

dct = {'test1':'x','test2':'y'}
print(len(dct))