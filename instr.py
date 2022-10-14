    ##################################
#### Preparing the instruction screen ####
    ##################################
    # We draw the text explaining what we will show
def instText(xpos=0, ypos=0, height=0.5, text="text"):
    instruction = visual.TextStim(
            win=win,
            pos=[xpos, ypos],
            wrapWidth=None,
            height=height,
            font="Palatino Linotype",
            alignHoriz='center',
            text=text)
    return instruction


def instScreen1(): 
    
    instructions = visual.TextStim(
        win=win,
        pos=[0,6],
        wrapWidth=None,
        height=.5,
        font="Palatino Linotype",
        alignHoriz='center'
        )

        
    instructions.text = """
    In this experiment, you will see a small patch of horizontal bars located in one of four possible spots inside a bigger circle of bars, or isolated, without any context.\n
    Your task is to locate where it appears on each trial, and to respond by pressing a key on your keyboard.
    If the horizontal bars appear:
    """

# Four additional texts on top of our example figures:
    instructions.draw()
    instructions2 = visual.TextStim(
        win=win,
        pos=[-6,3],
        wrapWidth=None,
        height=.5,
        font="Palatino Linotype",
        alignHoriz='center'
        )

    instructions2.text = """
    On the left
    Press Left Arrow"""
    instructions2.draw()

    instructions2 = visual.TextStim(
        win=win,
        pos=[6,3],
        wrapWidth=None,
        height=.5,
        font="Palatino Linotype",
        alignHoriz='center'
        )

    instructions2.text = """
    On the right
    Press Right Arrow"""
    instructions2.draw()



# The last text

    instructions2.text= """After you respond, you will see a brief feedback about your accuracy.
    In total, the experiment is expected to last ~45 minutes
    (9 blocks, 80 trials each).
    Feel free to take a short break inbetween blocks.
    Press SPACE key for the next instruction."""
    instructions2.pos=[0,-7]
    instructions2.draw()



# We draw four example gratings in instruction screen. 
    instgrating = visual.GratingStim(
        win=win,
        units="deg",
        size=[.75, .75]
    )

    instgratingbg = visual.GratingStim(
        win=win,
        units="deg",
        size=[5,5]
    )
    instgratingbg.mask = "raisedCos"
    instgratingbg.maskParams = {'fringeWidth': 0.4}  

    instgratingbg.sf=3 #20cycles per 400pix
    instgratingbg.contrast = 0.25 #25% contrast

    instgratingbg_vpos=[-1,-1,-1,-1]
    instgratingbg_hpos=[-9,-3,3,9]



    instgrating_vpos = [1, -1, 1, -1]
    instgrating_hpos = [-1, -1, 1, 1]

    instgrating_phase = [0.0, 0.0, 0.0, 0.0]
    instorientations = [90.0, 90.0, 90.0, 90.0]
    instbgorientations = [90,0,90,0]
    instgrating.mask = "raisedCos"
    instgrating.maskParams = {'fringeWidth': 0.4}  
    instgrating_sf= [3,3,3,3]
#contrast = 0.1

    instcontrasts = [.5, 0, 0, 0]
    for i_phase in range(4):
        
        instgratingbg.phase = instgrating_phase[i_phase]
        instgratingbg.pos = [instgratingbg_hpos[i_phase], instgratingbg_vpos[i_phase]]
        instgratingbg.sf = instgrating_sf[i_phase]
        instgratingbg.ori = instbgorientations[i_phase]
        instgratingbg.contrast = .25
        instgratingbg.draw()
        for i_phase2 in range(4):
            instgrating.phase = instgrating_phase[i_phase2]
            instgrating.pos = [instgratingbg_hpos[i_phase]+instgrating_hpos[i_phase2], instgratingbg_vpos[i_phase]+instgrating_vpos[i_phase2]]
            instgrating.sf = instgrating_sf[i_phase2]
            instgrating.ori = instorientations[i_phase2]
            instgrating.contrast = instcontrasts[i_phase2]
            instgrating.draw()
        instcontrasts = np.roll(instcontrasts,1)
        


    win.flip()
# We flip
# and wait for key press to start the experiment.
    keys = event.waitKeys(keyList=['space','escape'])#core.wait(.1)


def instScreen2():
    instructions2.text= """Now you will do a short practice.
    Before you begin, please make sure that your head is positioned
    so that the cross at the center of this screen aligns with your eyes."""
    instructions2.pos=[0,3]
    instructions2.draw()

    fixcross = visual.TextStim(
        win=win,
        pos=[0,.75],
        wrapWidth=None,
        height=1,
        font="Palatino Linotype",
        alignHoriz='center',
        alignVert='center',
        color= "black",
        bold=True
        )


    fixcross.text = """
    +"""
    fixcross.draw()


    instructions2.text= """Please keep your gaze at the center at all times.
    Press SPACE key to begin the practice."""
    instructions2.pos=[0,-3]
    instructions2.draw()
    win.flip()


    keys = event.waitKeys(keyList=['space','escape'])#core.wait(.1)


    win.flip()


