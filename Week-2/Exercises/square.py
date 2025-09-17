from expyriment import design, control, stimuli

#control.set_develop_mode()

exp = design.Experiment(name = "Square")

control.initialize(exp)

fixation = stimuli.FixCross()

square = stimuli.Rectangle(size=(50,50),colour='blue')

control.start(subject_id=1)

square.present(clear=True, update=False)
fixation.present(clear=False, update=True)

exp.clock.wait(500)

square.present(clear=True, update=True)

exp.keyboard.wait()

control.end()