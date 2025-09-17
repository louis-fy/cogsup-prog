from expyriment import design, control, stimuli

#control.set_develop_mode()

exp = design.Experiment(name = "Two Squares")

control.initialize(exp)

square1 = stimuli.Rectangle(size=(50,50),colour='green',position=(100,0))
square2 = stimuli.Rectangle(size=(50,50),colour='red',position=(-100,0))

control.start(subject_id=1)

square1.present(clear=True, update=False)
square2.present(clear=False, update=True)

exp.keyboard.wait()

control.end()