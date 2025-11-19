"""
This script runs the Potter & Fox (2009) Experiment 2,
using the "Super-Block" counterbalancing logic described in
the CORE1_Project1_counterbalance_1101.pdf.

This single file contains all the logic. You do not need a
separate 'build_counterbalance.py' file.

- It generates the balanced 75-trial plan in memory.
- It generates the master "pools" for quadrant combinations.
- It runs the 3 practice + 75 main trials.       ************* 72 NOT 75 *************
- It "pops" from the pools for each frame, as per the PDF's logic.
- It logs all data and verifies that the pools are empty at the end.
- It no longer checks for a 'masks' folder and always uses procedural masks.
"""
### ------- ALL VARIABLES -----
## 1. Independent Variables (the things we are testing)
# "duration": It's a number (240, 400, or 720) representing the time (in milliseconds) that each frame of the 8-frame RSVP "movie" will be shown on the screen;
#             It's pulled from the duration_pool (our "Big Bucket A") when the script builds the 75-trial plan.
# "n_value": A number (0, 1, 2, 3, or 4) represents the number of pictures that will be shown on a single frame (the "group size"). 
#            An n_value of 0 means it's a "mask-only" frame.
#            This comes from the SUPER_BLOCK_PROTOTYPE which defines how many of each n_value to use.
## 2. Dependent Variables (the things we are measuring)
# "key": A number (e.g., 121 for 'y' or 110 for 'n') given by participants (did the participant say "yes" or "no"?). It's recorded by exp.keyboard.wait().
# "rt": It's a number (e.g., 542.34) which represents the participant's reaction time in milliseconds.
# "correct": A number (1 or 0). It's 1 (True) if the participant's key press was correct (e.g., they pressed 'y' for an "old" picture) and 0 (False) if they were wrong.
## 3. Counterbalancing (Variables (The "Big Buckets" from the PDF)) --> main logic variables for counterbalancing
# "SUPER_BLOCK_PROTOTYPE": A list of 5 "recipes," e.g., (4, 2, 1, 1, 0, 0). It defines the "inventory" for one 5-trial "Super-Block," ensuring it has the correct 4:3:2:1 ratio of pictures.
# "master_quadrant_pools": A set of 4 "Big BuckB" (one for each n_value 1, 2, 3, and 4). 
#                          These buckets hold all the spatial position combinations. 
#                          For example, the N=2 bucket holds 90 "tickets" like (1, 2), (1, 3), (1, 4), (2, 3), etc. 
#                          When the script needs to show 2 pictures, it "pops" a ticket from this bucket to decide where to put them. 
#                          This is the Level 1 Shuffle.
# "experiment_plan": The final 75-trial "script" for the experiment. 
#                          It's a list of 75 items. 
#                          Each item contains the trial_id, the duration (from "Big Bucket A"), and the n_values (the 6-frame recipe, shuffled by Level 3 Shuffle).
#                          The order of this 75-item list is also shuffled (Level 2 Shuffle).
# "old_pics_pool" & "new_pics_pool": The two "Big Buckets" for the 900 picture files.
#                          "old_pics_pool" holds the 600 pictures to be shown in the RSVP (Roles A+B).
#                          "new_pics_pool" holds the 300 pictures for the memory test distractors (Role C). 
#                          The script "pops" from these pools when it needs a picture file.
## 4. Setting Variables (The "Control Panel")
# "N_SUPER_BLOCKS_TO_RUN": A number (you set it to 1 or 15). The "Test Mode" switch. 15 runs the full 75-trial experiment. 1 runs a quick 5-trial test.
# "PICS_FOLDER": A file path. Tells the script where to find the stimuli folder.
# "QUADRANT_POSITIONS": A dictionary. It maps a simple number 1 to a complex (x, y) coordinate (-165, 115), telling the script where "top-left" is.


### ------OUTPUT analysis:-------
# meaning of columns: 
# subject_id: The ID of participant. 
# trial_id: The trial number (1-5). Will see 8 rows for trial_id 1, 8 for trial_id 2, etc. 
# duration: (Independent Variable) The speed of the "movie" for that trial (240, 400, or 720ms). 
# test_pic_file: The filename of the picture they were just tested on.
# is_old: 
#        1 = This was an "Old" picture (it was in the RSVP sequence).
#        0 = This was a "New" picture (a distractor, not in the sequence).
# n_value: (The Most Important Variable)
#        If is_old == 1, this shows that the "group size" it was shown in (1, 2, 3, or 4).
#        If is_old == 0, this is N/A (because a "new" picture was never in a frame).
# quadrant: Where the picture was on the screen (1-4, or N/A for new pictures).
# response_key: (Dependent Variable) What the participant pressed.
#        121 = 'y' (Yes, I saw this) 
#        110 = 'n' (No, I did not see this)
# rt: (Dependent Variable) Reaction Time in milliseconds.
# correct: (Dependent Variable)
#        0 = They were wrong.
#        1 = They were correct.

import random
import itertools
import os
import sys
# NEW SCRIPT: Import libraries needed for data analysis
import csv
from collections import defaultdict
# END NEW SCRIPT
from expyriment import design, control, stimuli, io, misc
# We try to import the correct key constants, but if it fails (e.g., older version),
# we'll just use the ASCII values as a fallback.
## import the "official" names for the 'y' and 'n' keys (K_y, K_n) from the expyriment library and make the script less likely to crash due to version issues

try:
    from expyriment.misc.constants import K_y, K_n
except ImportError:
    print("Warning: Could not import K_y, K_n. Using ASCII values instead.")
    K_y = 121
    K_n = 110


# 1. Constants (from Paper & PDF)

# FOR TESTING: Change this number 
# 15 = Full 75-trial experiment
# 1  = A short 5-trial test
N_SUPER_BLOCKS_TO_RUN = 1

# Get the absolute path to the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define paths relative to the script's location (guarantee to find the "stimuli" folder)
PICS_FOLDER = os.path.join(SCRIPT_DIR, 'stimuli')
## Relative maths
N_TRIALS = 5 * N_SUPER_BLOCKS_TO_RUN # e.g. 5 * 15 = 75
N_PRACTICE = 3  # 3 practice trials
N_PICS_OLD = 40 * N_SUPER_BLOCKS_TO_RUN # e.g. 40 * 15 = 600
N_PICS_NEW = 4 * N_TRIALS # e.g. 4 * 75 = 300
N_PICS_TOTAL_NEEDED = N_PICS_OLD + N_PICS_NEW  # e.g. 600 + 300 = 900

TEST_PAUSE_DURATION = 200
TEST_PIC_DURATION = 400

# (x,y) positions for Quadrants 1, 2, 3, 4
QUADRANT_POSITIONS = {
    1: (-165, 115), # Top-Left
    2: (165, 115), # Top-Right
    3: (-165, -115), # Bottom-Left
    4: (165, -115)   # Bottom-Right
}

# 2. "Super-Block" Generator Logic (from PDF)
## COUNTERBALANCING
def get_super_block_prototype(): # defines what one 5-trial "Super-Block" looks like
    """
    Returns the 5-trial prototype
    Inventory needed: 8 (N=1), 6 (N=2), 4 (N=3), 2 (N=4), 10 (N=0)
    """
   # N is the Number of pictures that are flashed on the screen at the same time in one frame
    # e.g. the first trial has one N=4 frame, one N=2 frame, two N=1 frames, etc.
    SUPER_BLOCK_PROTOTYPE = [
        (4, 2, 1, 1, 0, 0), # Trial 1 (8 pics)
        (4, 2, 1, 1, 0, 0), # Trial 2 (8 pics)
        (3, 3, 1, 1, 0, 0), # Trial 3 (8 pics)
        (3, 2, 2, 1, 0, 0), # Trial 4 (8 pics)
        (3, 2, 2, 1, 0, 0)  # Trial 5 (8 pics)
    ]

    return SUPER_BLOCK_PROTOTYPE

def create_master_pools():
    """
    Creates the master pools for the entire experiment,
    based on the Super-Block inventory from the PDF.
    Returns:
        dict: {1: [...], 2: [...], 3: [...], 4: [...]}
    """
    print("Generating master quadrant pools...")
    
    # Quadrant combos are tuples of quadrant numbers (1-4)
    N1_QUADRANTS = list(itertools.combinations([1, 2, 3, 4], 1)) # 4 combos, e.g., (1,)
    N2_QUADRANTS = list(itertools.combinations([1, 2, 3, 4], 2)) # 6 combos, e.g., (1, 2)
    N3_QUADRANTS = list(itertools.combinations([1, 2, 3, 4], 3)) # 4 combos, e.g., (1, 2, 3)
    N4_QUADRANTS = list(itertools.combinations([1, 2, 3, 4], 4)) # 1 combo,  e.g., (1, 2, 3, 4)
    
    pools = {1: [], 2: [], 3: [], 4: []}
    
    for _ in range(N_SUPER_BLOCKS_TO_RUN): # Do this 15 times (or 1 for testing)
        pools[1].extend(N1_QUADRANTS * 2) # 8 frames = 4 combos * 2 reps
        pools[2].extend(N2_QUADRANTS * 1) # 6 frames = 6 combos * 1 rep
        pools[3].extend(N3_QUADRANTS * 1) # 4 frames = 4 combos * 1 rep
        pools[4].extend(N4_QUADRANTS * 2) # 2 frames = 1 combo * 2 reps

    # PDF: Level 1 Shuffle
    print("Shuffling master pools (Level 1 Shuffle)...")
    for pool in pools.values():
        random.shuffle(pool)
        
    print(f"  Pool N=1 size: {len(pools[1])} (Expected 8*{N_SUPER_BLOCKS_TO_RUN}={8 * N_SUPER_BLOCKS_TO_RUN})")
    print(f"  Pool N=2 size: {len(pools[2])} (Expected 6*{N_SUPER_BLOCKS_TO_RUN}={6 * N_SUPER_BLOCKS_TO_RUN})")
    print(f"  Pool N=3 size: {len(pools[3])} (Expected 4*{N_SUPER_BLOCKS_TO_RUN}={4 * N_SUPER_BLOCKS_TO_RUN})")
    print(f"  Pool N=4 size: {len(pools[4])} (Expected 2*{N_SUPER_BLOCKS_TO_RUN}={2 * N_SUPER_BLOCKS_TO_RUN})")
    return pools

def create_experiment_plan():
    """
    Generates the full, 3-level-shuffled plan.
    
    Returns:
        list: A 75-item list (or less), where each item is a dict
              e.g., {"trial_id": 1, "duration": 400, "n_values": (0,2,4,0,0,2)}
    """
    print(f"Generating {N_TRIALS}-trial plan...")
    
    # Create the Super Blocks
    prototype = get_super_block_prototype()
    full_trial_list = prototype * N_SUPER_BLOCKS_TO_RUN
    
    # PDF: Level 2 Shuffle
    print("Shuffling trial order (Level 2 Shuffle)...")
    random.shuffle(full_trial_list)
    
    # Create Duration Pool (N_TRIALS / 3 durations)
    reps_per_duration = N_TRIALS // 3
    # Make sure durations are also balanced if N_TRIALS is not divisible by 3 (e.g., 5 trials)
    duration_pool = ([240] * reps_per_duration + [400] * reps_per_duration + [720] * reps_per_duration)
    # Add any remaining
    remaining_durations = [240, 400, 720] * (N_TRIALS % 3)
    duration_pool.extend(remaining_durations[:N_TRIALS - len(duration_pool)])
    random.shuffle(duration_pool)
    
    final_plan = []
    for i in range(N_TRIALS):
        
        # PDF: Level 3 Shuffle 
        # Shuffle the 6 frames within this trial
        trial_n_values = list(full_trial_list[i])
        random.shuffle(trial_n_values)
        
        final_plan.append({
            "trial_id": i + 1,
            "duration": duration_pool.pop(),
            "n_values": trial_n_values # e.g.(0, 2, 0, 4, 0, 2)
        })
        
    print("Experiment plan generation complete.")
    return final_plan

# 3. Setup Experiment

try:
    experiment_plan = create_experiment_plan()
    master_quadrant_pools = create_master_pools()
except Exception as e:
    print(f"FATAL ERROR during plan generation: {e}")
    sys.exit()

# Initialize Expyriment
exp = design.Experiment(name="Potter & Fox (2009) Exp 2 (Super-Block)")
# control.defaults.initialize_delay = 0  <-- This line was removed to fix the warning
control.initialize(exp)

exp.data_variable_names = [
    "trial_id",
    "duration",
    "test_pic_file",
    "is_old", # 1 (old) or 0 (new)
    "n_value", # The N-value of the frame this pic was in (1,2,3,4)
    "quadrant",  # The quadrant this pic was in (1-4)
    "response_key",
    "rt",
    "correct"
]

# Load Stimuli
print("Loading stimuli...")
picture_stim_cache = {}
try:
    all_pic_files = [f for f in os.listdir(PICS_FOLDER) if f.endswith(('.jpg', '.png', '.jpeg'))]
    random.shuffle(all_pic_files)
    
    if len(all_pic_files) == 0:
        print(f"FATAL ERROR: No pictures found in '{PICS_FOLDER}'.")
        sys.exit()

    if len(all_pic_files) < N_PICS_TOTAL_NEEDED:
        # THIS BLOCK IS EDITED TO ALLOW TESTING 
        # In experiment we need 900 pictures
        print(f"WARNING: NOT ENOUGH PICTURES")
        print(f"Need {N_PICS_TOTAL_NEEDED}, but only found {len(all_pic_files)}.")
        print("REUSING pictures. This is for TESTING ONLY.")
        
        # Create a new list by repeating the pictures
        reused_pics_list = []
        while len(reused_pics_list) < N_PICS_TOTAL_NEEDED:
            reused_pics_list.extend(all_pic_files) # Add the pictures over and over
            
        # Trim the list to exactly the number needed
        all_pic_files = reused_pics_list[:N_PICS_TOTAL_NEEDED]
        print(f"Created a temporary list of {len(all_pic_files)} reused pictures.")

    # Split into pools
    old_pics_pool = all_pic_files[:N_PICS_OLD]
    new_pics_pool = all_pic_files[N_PICS_OLD:N_PICS_TOTAL_NEEDED]
    random.shuffle(new_pics_pool)
    print(f"Loaded {len(old_pics_pool)} 'old' pictures and {len(new_pics_pool)} 'new' pictures.")

except FileNotFoundError:
    print(f"FATAL ERROR: Picture folder '{PICS_FOLDER}' not found.")
    sys.exit()
except Exception as e:
    print(f"FATAL ERROR loading stimuli: {e}")
    sys.exit()


def get_picture(filename):
    """A helper function to load pictures from cache."""
    if filename not in picture_stim_cache:
        try:
            pic = stimuli.Picture(os.path.join(PICS_FOLDER, filename))
            pic.preload()
            picture_stim_cache[filename] = pic
        except Exception as e:
            print(f"Warning: Could not load {filename}. Using placeholder. Error: {e}")
            pic = stimuli.Rectangle(size=(300, 200), colour=misc.constants.C_GREY)
            stimuli.TextLine(text=filename, text_size=12).plot(pic)
            pic.preload()
            picture_stim_cache[filename] = pic
    return picture_stim_cache[filename]

def get_practice_picture(text="Practice"):
    """Creates a placeholder for practice trials."""
    key = f"practice_{text}"
    if key not in picture_stim_cache:
        pic = stimuli.Rectangle(size=(300, 200), colour=misc.constants.C_GREY)
        stimuli.TextLine(text=text, text_size=20).plot(pic)
        pic.preload()
        picture_stim_cache[key] = pic
    return picture_stim_cache[key]

# Always use 8 procedural grey rectangles as masks.
print("Using procedural grey rectangles as masks.")
try:
    MASK_STIMULI = [stimuli.Rectangle(size=(300, 200), colour=misc.constants.C_GREY) for _ in range(8)]
    for mask in MASK_STIMULI:
        mask.preload()
except Exception as e:
    print(f"FATAL ERROR: Could not create procedural masks: {e}")
    sys.exit()


# NEW SCRIPT: Define the Data Analysis Function
def analyze_data(data_file_path):
    """
    Reads the raw CSV data file, calculates key results,
    saves them to a new text file, and returns a summary string.
    """
    
    # These dictionaries will hold our aggregated data
    # We use defaultdict to make it easy to add new keys without checking if they exist
    # e.g., results_n_value['1'][240]['hits'] = 0
    
    # This stores Hit Rates, grouped by N-Value, then by Duration
    # results_n_value[n_value][duration] = {'hits': 0, 'total_old': 0}
    results_n_value = defaultdict(lambda: defaultdict(lambda: {'hits': 0, 'total_old': 0}))
    
    # This stores False Alarms, grouped by Duration
    # results_duration[duration] = {'false_alarms': 0, 'total_new': 0}
    results_duration = defaultdict(lambda: {'false_alarms': 0, 'total_new': 0})
    
    # These are for the simple, overall accuracy score
    total_correct = 0
    total_responses = 0

    try:
        # Must look for the .csv file, not the .xpd file
        # The data_file_path is ".../file.xpd", but the CSV is ".../file.csv"
        csv_file_path = data_file_path.replace(".xpd", ".csv")

        # Open the CSV file that Expyriment just saved
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            # Use DictReader to read each row as a dictionary,
            # which is easier than remembering column numbers
            reader = csv.DictReader(f)
            # Loop over every single row (e.g., all 576 responses)
            for row in reader:
                # Make sure row is not empty
                if not row:
                    continue

                # We are processing one response
                total_responses += 1
                
                # Read and convert data from the row
                # We must convert strings "1" or "0" into integers 1 or 0
                is_old = int(row['is_old'])
                n_value = row['n_value'] # Keep as string '1', '2', '3', '4', or 'N/A'
                duration = int(row['duration'])
                correct = int(row['correct'])
                response_key = int(row['response_key'])

                # Add to the overall accuracy count
                if correct == 1:
                    total_correct += 1

                # Now, sort this response into the correct bucket
                if is_old == 1:
                    # This was an "old" picture (Role A or B)
                    # We store its data based on its N-Value and Duration
                    
                    # 'hits' = participant correctly pressed 'y'
                    # We check if the key they pressed matches the 'y' key
                    if response_key == K_y:
                         results_n_value[n_value][duration]['hits'] += 1
                    
                    # 'total_old' = this was an "old" picture
                    results_n_value[n_value][duration]['total_old'] += 1
                
                elif is_old == 0:
                    # This was a "new" picture (Role C)
                    # The paper groups these by *duration only*
                    
                    # 'false_alarms' = participant incorrectly pressed 'y'
                    if response_key == K_y:
                        results_duration[duration]['false_alarms'] += 1
                    
                    # 'total_new' = this was a "new" picture
                    results_duration[duration]['total_new'] += 1
        
        # Data aggregation is finished. Now, build the text report. 
        
        # Create a list of strings that we will join together at the end
        report = []
        report.append("--- Experiment 2 Summary Report ---")
        report.append(f"Data file: {os.path.basename(data_file_path)}")
        report.append("\n")
        
        # Calculate overall percentage
        overall_percent = (total_correct / total_responses) * 100 if total_responses > 0 else 0
        report.append(f"Overall Accuracy (All Responses): {overall_percent:.2f}% ({total_correct} / {total_responses})")
        report.append("\n" + "="*40 + "\n")

        # Part 1: Hit Rate by N-Value (This is Figure 3 from the paper) 
        report.append("Hit Rate (% 'Yes' to OLD pictures) by N-Value (All Durations Combined):")
        
        # Get the keys '1', '2', '3', '4' and sort them numerically
        valid_n_values = sorted([k for k in results_n_value.keys() if str(k).isdigit()], key=int)
        
        for n_value in valid_n_values:
            n_hits = 0
            n_total = 0
            # Sum up hits and totals from all durations (240, 400, 720) for this n_value
            for data in results_n_value[str(n_value)].values():
                n_hits += data['hits']
                n_total += data['total_old']
            
            # Calculate percentage
            n_percent = (n_hits / n_total) * 100 if n_total > 0 else 0
            report.append(f"  N={n_value} Frames: {n_percent:.2f}% ({n_hits} / {n_total})")

        report.append("\n" + "="*40 + "\n")

        # Part 2: Hit Rate by Duration (Also in Figure 3) 
        report.append("Hit Rate (% 'Yes' to OLD pictures) by Duration (All N-Values Combined):")
        
        # Get the keys 240, 400, 720 and sort them
        sorted_durations = sorted(results_duration.keys())
        for dur in sorted_durations:
            dur_hits = 0
            dur_total_old = 0
            # We have to sum this up from the *other* dictionary (results_n_value)
            for n_data in results_n_value.values():
                if dur in n_data:
                    dur_hits += n_data[dur]['hits']
                    dur_total_old += n_data[dur]['total_old']
            
            dur_percent = (dur_hits / dur_total_old) * 100 if dur_total_old > 0 else 0
            report.append(f"  {dur} ms: {dur_percent:.2f}% ({dur_hits} / {dur_total_old})")

        report.append("\n" + "="*40 + "\n")

        # Part 3: False Alarm Rate by Duration (The other line in Figure 3) 
        report.append("False Alarm Rate (% 'Yes' to NEW pictures) by Duration:")
        for dur in sorted_durations:
            fa_hits = results_duration[dur]['false_alarms']
            fa_total = results_duration[dur]['total_new']
            
            # Calculate percentage
            fa_percent = (fa_hits / fa_total) * 100 if fa_total > 0 else 0
            report.append(f"  {dur} ms: {fa_percent:.2f}% ({fa_hits} / {fa_total})")

        report.append("\n\n--- End of Report ---")

        # Save the report to a new file 
        
        # Join all the report lines into one big string
        report_content = "\n".join(report)
        
        # Create a new filename, e.g., "my_data.csv" -> "my_data_summary.txt"
        report_filename = data_file_path.replace(".xpd", "_summary.txt")
        
        # Write the report content to the new text file
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"Analysis complete. Summary saved to: {os.path.basename(report_filename)}")
        
        # Return the simple string for the final on-screen feedback
        return f"Overall Accuracy: {overall_percent:.2f}%"

    except FileNotFoundError:
        # Handle error if the data file wasn't created
        print(f"Error: Could not find data file to analyze: {csv_file_path}")
        return f"Analysis failed (File not found: {os.path.basename(csv_file_path)})."
    except Exception as e:
        # Handle any other unexpected analysis errors
        print(f"Error during analysis: {e}")
        return "Analysis could not be completed."
# END NEW SCRIPT


# 4. Define Trial-Running Function 
def run_trial(trial_data, is_practice=False):
    """
    Runs a single trial by "popping" from the master pools
    as described in the PDF.
    """
    trial_id = trial_data["trial_id"]
    duration = trial_data["duration"]
    n_values = trial_data["n_values"] # e.g. [0, 2, 4, 0, 0, 2]
    
    rsvp_frames = []
    trial_picture_log = [] # To store (file, n_value, quadrant)
    
    # PDF "Final Logic": "Popping" from the Pools 
    for n in n_values: # For each of the 6 frames (Frame 2-7)
        frame_canvas = stimuli.Canvas(size=exp.screen.size)
        quad_combos_to_plot = [] # This will be a tuple of quad numbers, e.g. (1, 4)
        
        if n > 0:
            if is_practice:
                # Practice: just grab a random combo
                quad_combos_to_plot = random.sample([1, 2, 3, 4], n)
            else:
                try:
                    # "Pop" one item from the correct master pool
                    quad_combos_to_plot = master_quadrant_pools[n].pop()
                except IndexError:
                    print(f"FATAL ERROR: Ran out of items in master_quadrant_pools[{n}]!")
                    print("This means the balancing logic is flawed.")
                    control.end()
                    sys.exit()
                except KeyError:
                    print(f"FATAL ERROR: Tried to pop from a pool that doesn't exist (N={n})")
                    control.end()
                    sys.exit()
        
        # Plot masks first in all 4 positions
        random.shuffle(MASK_STIMULI)
        for i in range(4):
            quad_num = i + 1
            pos_tuple = QUADRANT_POSITIONS[quad_num]
            MASK_STIMULI[i].reposition(pos_tuple)
            MASK_STIMULI[i].plot(frame_canvas)
            
        # Now plot the pictures over the masks
        # The code was plotting N pictures, but only logging the last one.
        # This new loop correctly iterates over the tuple of quadrants.
        for quad_num in quad_combos_to_plot:
            # quad_combos_to_plot is a tuple like (1,) or (1, 4) or (1, 2, 3)
            # This loop will run N times.
            position = QUADRANT_POSITIONS[quad_num]
            
            if is_practice:
                pic_file = "practice"
                pic_stim = get_practice_picture(f"N={n}")
            else:
                try:
                    pic_file = old_pics_pool.pop()
                    pic_stim = get_picture(pic_file)
                except IndexError:
                    print("FATAL ERROR: Ran out of 'old' pictures in the pool!")
                    control.end()
                    sys.exit()

            pic_stim.reposition(position)
            pic_stim.plot(frame_canvas) # Plot on top
            
            # Log this picture's info
            trial_picture_log.append({
                "file": pic_file,
                "n_value": n,
                "quadrant": quad_num
            })

        frame_canvas.preload()
        rsvp_frames.append(frame_canvas)
        
    # Add frames 1 and 8 (mask-only)
    frame_1_and_8 = stimuli.Canvas(size=exp.screen.size)
    random.shuffle(MASK_STIMULI)
    for i in range(4):
        quad_num = i + 1
        pos_tuple = QUADRANT_POSITIONS[quad_num]
        MASK_STIMULI[i].reposition(pos_tuple)
        MASK_STIMULI[i].plot(frame_1_and_8)
    frame_1_and_8.preload()

    final_rsvp_sequence = [frame_1_and_8] + rsvp_frames + [frame_1_and_8]

    # 5b. Run the RSVP Sequence 
    exp.screen.clear()
    exp.screen.update()
    
    # Present fixation cross
    stimuli.FixCross(size=(20, 20), line_width=3, colour=misc.constants.C_WHITE).present()
    exp.clock.wait(500) # 500ms fixation

    for frame in final_rsvp_sequence:
        frame.present(clear=True, update=True)
        exp.clock.wait(duration)
    
    stimuli.BlankScreen().present(clear=True, update=True)
    exp.clock.wait(TEST_PAUSE_DURATION)

    # We need to test 4 "old" (Role B) and 4 "new" (C)
    
    if is_practice:
        # Create 4 dummy "old" and 4 "new" test items
        old_test_pics = [{"file": "practice", "n_value": 0, "quadrant": 0}] * 4
        new_test_pics = [{"file": "practice_new", "n_value": "N/A", "quadrant": "N/A"}] * 4
    else:
        # Randomly select 4 "old" pics (Role B) from the 8 we showed
        random.shuffle(trial_picture_log)
        old_test_pics = trial_picture_log[:4] # Role B
        # Role A (not tested) are the ones left: trial_picture_log[4:]
        
        # Get 4 "new" pics (Role C)
        new_test_pics = []
        for _ in range(4):
            try:
                new_file = new_pics_pool.pop()
                new_test_pics.append({"file": new_file, "n_value": "N/A", "quadrant": "N/A"})
            except IndexError:
                print("FATAL ERROR: Ran out of 'new' pictures in the pool!")
                control.end()
                sys.exit()
    
    # Create and shuffle the final test list
    test_list = []
    for pic_log in old_test_pics:
        test_list.append((pic_log, 1)) # (log, is_old=1)
    for pic_log in new_test_pics:
        test_list.append((pic_log, 0)) # (log, is_old=0)
    random.shuffle(test_list)

    for pic_log_tuple, is_old in test_list:
        pic_log = pic_log_tuple
        filename = pic_log["file"]
        
        # Present the test picture (centered)
        if is_practice:
            if is_old:
                test_stim = get_practice_picture("N=...")
            else:
                test_stim = get_practice_picture("Practice New")
        else:
            test_stim = get_picture(filename)
            
        test_stim.reposition((0, 0))
        test_stim.present(clear=True, update=True)
        exp.clock.wait(TEST_PIC_DURATION)

        # Present blank screen until response
        stimuli.BlankScreen().present(clear=True, update=True)
        key, rt = exp.keyboard.wait(keys=[K_y, K_n])

        if not is_practice:
            correct = (key == K_y and is_old) or (key == K_n and not is_old)
            exp.data.add([
                trial_id,
                duration,
                filename,
                is_old,
                pic_log["n_value"],
                pic_log["quadrant"],
                key,
                rt,
                1 if correct else 0
            ])

# 5. Run Experiment Flow 

control.start(skip_ready_screen=True)

# Instructions
stimuli.TextScreen(
    "Welcome to the Experiment",
    ("You will see a series of rapidly presented pictures.\n\n"
     "Please watch carefully and try to remember them.\n\n"
     "After each sequence, you will be given a memory test.\n"
     "Several pictures will be shown one by one.\n\n"
     "--- TEST INSTRUCTIONS ---\n"
     "1. A picture will FLASH for a very short time (400ms).\n"
     "2. The screen will then go BLANK.\n"
     "3. *When the screen is blank*, please respond:\n\n"
     "Press 'y' for YES (you saw it in the sequence).\n"
     "Press 'n' for NO (you did not see it).\n\n"
     "We will begin with 3 practice trials.\n\nPress any key to start."),
    text_size=24,
    text_justification=0
).present()
exp.keyboard.wait()

# Practice Trials (using a "dummy" trial plan)
practice_plan = [
    {"trial_id": -1, "duration": 400, "n_values": [1, 0, 2, 0, 3, 0]},
    {"trial_id": -2, "duration": 400, "n_values": [4, 0, 0, 1, 0, 1]},
    {"trial_id": -3, "duration": 400, "n_values": [0, 2, 0, 2, 0, 2]},
]
for trial in practice_plan:
    run_trial(trial, is_practice=True)

# Main Experiment
stimuli.TextScreen(
    "Practice Complete",
    "The main experiment will now begin.\n\n" +
    "The rules are the same as in the practice.\n" +
    "Remember: Respond *after* the picture disappears, when the screen is blank.\n\n" +
    "Please try your best to remember the pictures.\n\nPress any key to start.",
    text_size=24,
    text_justification=0
).present()
exp.keyboard.wait()


for i, trial in enumerate(experiment_plan):
    run_trial(trial, is_practice=False)
    
    # Rest breaks every 15 trials (if running full 75 trials)
    if N_TRIALS > 5: # Only add breaks if not in a short test mode
        if (i + 1) % 15 == 0 and (i + 1) < N_TRIALS:
            stimuli.TextScreen(
                "Rest Break",
                f"You have completed {i+1} / {N_TRIALS} trials.\n\n" +
                "Please take a short break.\n\nPress any key to continue.",
                text_size=24,
                text_justification=0
            ).present()
            exp.keyboard.wait()



# 6. End Experiment, Analyze & Verify

#  get the name of the data file 
data_file_path = exp.data.filename

# Analysis before ending the experiment 
if N_TRIALS > 0: # Only run analysis if we ran real trials (not 0)
    print("Running analysis...")
    feedback_summary = analyze_data(data_file_path)
    
    # Create the final text to show the participant
    final_goodbye_text = (f"Experiment complete. Thank you!")
else:
    # This just handles the case where N_SUPER_BLOCKS_TO_RUN was set to 0
    print("No trials run, skipping analysis.")
    feedback_summary = "No trials run."
    final_goodbye_text = "Experiment complete."


# We end the Expyriment session, which finalizes and closes the data file
# We pass our feedback string to the 'goodbye_text'
# and add a 5-second delay so the user can read it.
control.end(goodbye_text=final_goodbye_text, goodbye_delay=5000)


# Verification (as PDF) 
# This final check runs in the console (not the experiment window)
print("\n--- Experiment Finished. Verifying balance... ---")
# Check if all the "Big Buckets" for quadrants are empty
if all(len(pool) == 0 for pool in master_quadrant_pools.values()):
    print("VERIFICATION SUCCESS: All master pools are empty.")
    print("All balanced items were used exactly once.")
else:
    # If a bucket is not empty, something went wrong in our logic
    print("VERIFICATION FAILED: Some master pools still have items.")
    for n, pool in master_quadrant_pools.items():
        if len(pool) > 0:
            print(f"  Pool N={n} has {len(pool)} items left.")

# Check if the picture "Big Buckets" are empty
if len(old_pics_pool) > 0:
    print(f"VERIFICATION FAILED: {len(old_pics_pool)} 'old' pictures were left unused.")
if len(new_pics_pool) > 0:
    print(f"VERIFICATION FAILED: {len(new_pics_pool)} 'new' pictures were left unused.")

print("-------------------------------------------------")
# END NEW SCRIPT


