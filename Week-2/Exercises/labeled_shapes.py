from expyriment import design, control, stimuli, misc

#control.set_develop_mode()

def create_shape(x, y, sides, length, colour, label):
    polygon = stimuli.Shape(position=(x,y),vertex_list=misc.geometry.vertices_regular_polygon(sides,length),colour=colour)
    line = stimuli.Line(start_point=(x,y),end_point=(x,y+50),line_width=3,colour='white')
    text = stimuli.TextLine(text=label,position=(x,y+70),text_colour='white')
    return polygon,line,text

exp = design.Experiment(name = "Two Polygons")

control.initialize(exp)

polygon1,line1,text1 = create_shape(-100,0,3,50,'purple','triangle')
polygon2,line2,text2 = create_shape(100,0,6,25,'yellow','hexagon')

control.start(subject_id=1)

line1.present(clear=True, update=False)
text1.present(clear=False, update=False)
polygon1.present(clear=False, update=False)
line2.present(clear=False, update=False)
text2.present(clear=False, update=False)
polygon2.present(clear=False, update=True)

exp.keyboard.wait()

control.end()