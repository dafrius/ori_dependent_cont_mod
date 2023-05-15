# -*- coding: utf-8 -*-
"""
Created on Fri May 10 2023

@author: canoluk
"""

## if you get freetype library error, go to this website:
    #http://gnuwin32.sourceforge.net/packages/freetype.htm 
# Click on "Complete package, except sources" and download and install
# the .exe file 
# Additionally, you should install Microsoft Visual Studio Community, 
# Which somehow helps integrate the two.
# %% Importing packages

import os # for file/folder operations
import numpy as np
import numpy.random as rnd          # for random number generators
import numpy.matlib as npm  
from psychopy import visual, event, core, gui, data, monitors
import PsiMarginal
import copy

# %% Subject info/ Experiment setup
 
datapath = 'data'
# Get subject name, gender, age, handedness through a dialog box
exp_name = 'Contrast Stuff'
exp_info = {
        'language' : ('fr','en','nl','de'),
        'participant': '',
        'gender': ('male', 'female'),
        'age':'',
        'left-handed':False,
        'Stim_size':'0.75',
        'eccentricity':'1.5',
        'color_text':'.75',
        'screenwidth(cm)': '49',
        'screenresolutionhori(pixels)': '1920',
        'screenresolutionvert(pixels)': '1200',
        'refreshrate(hz)': '120'
        }

dlg = gui.DlgFromDict(dictionary=exp_info, title=exp_name)

data_fname=exp_info['participant']

# %% Instructions
instruction_dictionary={"instructions.text1": "Dans cette étude, vous verrez apparaître sur l'écran des stimuli en forme de grilles. Ces stimuli se trouveront soit à l'intérieur d'une plus grande grille, soit de manière isolée. \n\n Votre tâche consiste à localiser où les grilles vont apparaître en appuyant sur une touche de votre clavier. Si les grilles apparaissent:\n\n",
                         "instructions.text2": "Sur la gauche \nAppuyez sur 'S' ",
                         "instructions.text3": "Sur la droite \nAppuyez sur 'L' ",
                         "instructions.text4": "Après avoir répondu, vous recevrez un court feedback sur votre performance.\n\n Au total cette expérience devrait durer ~45 minutes (9 blocs, 80 essais chacun). N'hésitez pas à prendre une petite pause entre chacun des blocs.\n\nAppuyez sur la barre 'ESPACE' pour la prochaine instruction.",
                         "instructions.text5": "Maintenant, vous allez réaliser un petit entrainement. Avant de commencer, assurez vous que votre tête soit positionée de manière à ce que la croix au milieu de l'écran soit alignée avec vos yeux.",
                         "instructions.text6": "Veuillez garder votre regard fixé au centre durant toute l'expérience.\n\nAppuyez sur la barre 'ESPACE' commencer l'entrainement.",
                         "instructions.text6a": "Vous pouvez maintenant placer vos mains sur les touches 'S' et 'L' du clavier.",
                         "instructions.text6b": "Appuyez sur la barre 'ESPACE' pour voir les prochaines instructions.",
                         'instructions.text6c': "Si vous avez des questions par rapport aux consignes, sentez-vous libre de les poser.",
                         "instructions.text7": "Bravo!\nVous avez terminé l'entrainement.\nVous allez maintenant commencer l'étude.\n\nAppuyez sur la barre 'ESPACE' pour commencer l'étude .\n\nBloc:0/9",
                         "intblocktext.text":"Prenez le temps de vous reposer avant le prochain bloc. Vous pouvez appuyer sur la barre 'ESPACE' pour continuer après 30 secondes lorsque vous serez prêt.\nBloc: ",
                         'timertext.text':"Prêt",
                         "endtext.text":"Merci pour votre participation.\nAppuyez sur une touche pour quitter l'expérience"}       
       

reduce = 0


# %% Psi Parameters


def makePsi(nTrials=40, thresholdPrior=('normal',.0139,.07)):
# Image visibility ranges between 2 and 40, logarithmically, 40 possibilities.
    staircase = PsiMarginal.Psi(stimRange=np.geomspace(0.001,1,350,endpoint=True), # Contrast ranges between .001 and 1, 350 possibilities.
            Pfunction='Weibull', nTrials=nTrials,
            threshold=np.geomspace(0.001,1,350,endpoint=True), thresholdPrior=thresholdPrior,
            slope=np.geomspace(0.5,20,50,endpoint=True), slopePrior=('gamma', 3, 6), # with these values, the contrast starts at ~15 and can end up at ~2 in 32 trials.
            guessRate=0.5, 
            lapseRate=0.05, lapsePrior=('beta',2,20), marginalize=True)
    return staircase

nTrials=40
nStaircase = 2 
nConditions = 3 #Parallel, Orthogonal, Isolated
nRunPerCond = 3
totalblocks = 9 
thresholdOrthPrior = ('normal',.0139,.07) # Prior for Orthogonal Context condition
thresholdParrPrior = ('normal',.2549, .2) # Prior for Parallel Context condition
thresholdIsoPrior = ('normal',.0137,.07) # Prior for Isolated condition



# Here we define 2 Psi staircases for each of the context conditions(parallel, orthogonal, isolated)
# 


psiParr1 = makePsi(thresholdPrior=thresholdParrPrior)
psiParr2 = makePsi(thresholdPrior=thresholdParrPrior)
psiIso1 = makePsi(thresholdPrior=thresholdIsoPrior)
psiIso2 = makePsi(thresholdPrior=thresholdIsoPrior)
psiOrth1 = makePsi(thresholdPrior=thresholdOrthPrior)
psiOrth2 = makePsi(thresholdPrior=thresholdOrthPrior)



# %% Background orientation has three possibilities: Parallel or Orthogonal to the target, or no background
bgorilist = npm.repmat(np.repeat([90,0,361],int(nTrials*nStaircase)),1,1)
bgorilist = bgorilist[0]

staircaselist=npm.repmat(np.sort(npm.repmat(list(range(1,nStaircase+1)),1,int(nTrials))),1,nConditions)
staircaselist=staircaselist[0]
#print(staircaselist)

#Targets can be shown at either one of 2 locations. 
targetloclist = npm.repmat([0,1],1,int(nTrials/2*nConditions*nStaircase)) # We divide by two
targetloclist = targetloclist[0]


stim_order = []
    
#Creating a list of dictionaries that contains information about each single trial.
for bgori, targloc, staircase in zip(bgorilist,  targetloclist, staircaselist):
    stim_order.append({'bgori': bgori, 'staircase':staircase, 'targetloc': targloc,})
print(stim_order)
responses = []

# %% This part is about shuffling
#We need to shuffle the staircases WITHIN each condition.
#because of the ordering I made in the stim_order, 
#conditions are always in the following order:
#Parr1-Parr2-Orth1-Orth2-Iso1-Iso2
#If you get rid of a temporal condition or a staircase, the order stays the same,
#Just that the removed ones are dropped from the order
#For example, if you do nTemporal=2, nStaircase=1
#It becomes: Parr1-Orth1-ParrLead1-OrthLead1



#Now we will intermingle the two staircases for each condition (if there is two)

#For that, we first slice the stim_order into 3 (for each condition), and shuffle within each
# slice 

Parr=[]
Orth=[]
Iso=[]

total=nTrials*nStaircase*nConditions
#   we turn them into integers 
#   from floating points,because while indexing we don't want floats
PSslcr=slice(0,int(total/3),1) 
OSslcr=slice(int(total/3),int(total*2/3),1)
ISslcr=slice(int(total*2/3),total,1) 
alltotal=total*nRunPerCond

PS1=stim_order[PSslcr]
OS1=stim_order[OSslcr]
IS1=stim_order[ISslcr]

Parr=copy.deepcopy(PS1) 
Orth=copy.deepcopy(OS1)
Iso=copy.deepcopy(IS1) # We deepcopy, because if we don't, they are still 
                            # connected to the stim_order, and if we do any operation,
                            # stim_order gets affected from that change as well.

rnd.shuffle(Parr)
rnd.shuffle(Orth)
rnd.shuffle(Iso)


#Shuffling order of runs/conditions
conds=[]
cond_order= [1,2,3]
#cond_order=npm.repmat([1,2],1,3)
for i in range(nRunPerCond):
    rnd.shuffle(cond_order)
    conds.extend(cond_order)


#Tagging the conditions with the corresponding number
# Parallel = 1, Orthogonal = 2, Isolated = 3
for ind in range(0,int(len(Parr))):
        Parr[ind].update(cond=1)
for ind in range(0,int(len(Orth))):
        Orth[ind].update(cond=2)
for ind in range(0,int(len(Iso))):
        Iso[ind].update(cond=3)
    
#Putting all the shuffled, mixed, trial blocks into one final variable
#using the shuffled condition order
alltrials = []
for i in range(0,int(len(conds))):
    if conds[i] == 1:
        alltrials.extend(Parr)
    elif conds[i] == 2:
        alltrials.extend(Orth)
    elif conds[i] == 3:
        alltrials.extend(Iso)
        
        
#using PsychoPy's TrialHandler, makes it easier to index in a loop, and output
trials = data.TrialHandler(alltrials, nReps=1, extraInfo=exp_info,
                           method='sequential', originPath=datapath)

# %% Window Settings and grating properties 
#=======================================
    
#We define a monitor, which helps control for visual angle.
mon = monitors.Monitor('Vpixx040821')
mon.setDistance(57)

#This is just for piloting, not relevant to actual experiment, normally we'll
# go with only the functions inside the "if", but not "else".

mon.setWidth(float(exp_info['screenwidth(cm)']))
horipix = exp_info['screenresolutionhori(pixels)']
vertpix = exp_info['screenresolutionvert(pixels)']
framerate = exp_info['refreshrate(hz)']
scrsize = (float(horipix),float(vertpix))


#Depending on the framerate of the monitor, we calculate how long the duration of one frame is.
framelength = 1000/(float(framerate))
#Then depending on that, we calculate how many frames need to be shown in a duration of e.g. 500ms.
FixFrame = int(500/framelength) #500 ms
EmptyFrame=int(50/framelength) #50 ms
GratingFrame = int(100/framelength) #100 ms
LeadFrame = int(50/framelength) #50 ms


color_text = float(exp_info['color_text']) # the color of the text depends on the settings we select initialy

mon.setSizePix(scrsize)
# Open a window
win = visual.Window(monitor = mon, 
                    size =scrsize,
                    color= 'grey',
                    units='deg',
                    fullscr=False,
                    screen=2)
#Hide the cursor when the window is opened:
win.mouseVisible=False


# size of the gratings and the circles
size = float(exp_info['Stim_size'])

#We define the target grating
grating = visual.GratingStim(
    win=win,
    units="deg",
    size=[size, size]
)
#And the background grating

gratingbg = visual.GratingStim(
    win=win,
    units="deg",
    size=[7,7]
)

#We put a raised cosine wave mask around it so it looks nice and smooth at the edges
gratingbg.mask = "raisedCos"
gratingbg.maskParams = {'fringeWidth': 0.4}  

gratingbg.sf = 2 #2 cpd
gratingbg.contrast = 0.25 #25% contrast
gratingbg.phase = 0.0 #for now it's 0 but we randomly change and adapt this to the target in trial loop

#Each of the 2 target gratings is going to appear 
#at 5 degrees eccentricity from the center
grating_vpos = [0, 0] # height (0 = center)
grating_hpos = [-float(exp_info['eccentricity']), float(exp_info['eccentricity'])]# laterality (0 = center)

# target grating is ALWAYS HORIZONTAL:
# random phase between 0 and 1
phases = np.arange(0,1,.03)
# all of them have the identical sf as the bg grating.
# at the beginning, all four have 0 contrast, depending on where the 
# target will be shown and the staircase, we'll increase contrast at 
# one of four points in each trial.
contrasts = [0, 0]

#Drawing the center dot
circle = visual.Circle(
    win=win,
    units="deg",
    radius=.075,
    fillColor=[-1, -1, -1],
    lineColor=[-1, -1, -1]
    )

grating.mask = "raisedCos"
grating.maskParams = {'fringeWidth': 0.1}  
grating.ori= 90
grating.pos = grating_hpos
grating.sf = 2

feedback = visual.TextStim(
    win=win,
    pos=[9,0],
    wrapWidth=None,
    height=.4,
    font="Palatino Linotype",
    alignHoriz='center'
    )                        

# %% Preparing the instruction screen 

# We draw the text explaining what we will show
instructions = visual.TextStim(
    win=win,
    pos=[0,8],
    wrapWidth=None,
    height=.65, #set the size of the text
    font="Palatino Linotype",
    alignHoriz='center',
    color = [color_text,color_text,color_text] #set the color of the text 
    )

    
instructions.text = instruction_dictionary['instructions.text1']

# Four additional texts on top of our example figures:
instructions.draw()
instructions2 = visual.TextStim(
    win=win,
    pos=[-6,3],
    wrapWidth=None,
    height=.65,
    font="Palatino Linotype",
    alignHoriz='center',
    color = [color_text,color_text,color_text]
    )

instructions2.text = instruction_dictionary['instructions.text2']

instructions2.draw()

instructions2 = visual.TextStim(
    win=win,
    pos=[6,3],
    wrapWidth=None,
    height=.65,
    font="Palatino Linotype",
    alignHoriz='center',
    color = [color_text,color_text,color_text] 
    )

instructions2.text = instruction_dictionary['instructions.text3']
instructions2.draw()



# The last text

instructions2.text= instruction_dictionary['instructions.text4']
instructions2.pos=[0,-10]
instructions2.draw()



# We draw four example gratings in instruction screen. 
instgrating = visual.GratingStim(
    win=win,
    units="deg",
    size=[0.5, 0.5]
)

instgratingbg = visual.GratingStim(
    win=win,
    units="deg",
    size=[7,7]
)
instgratingbg.mask = "raisedCos"
instgratingbg.maskParams = {'fringeWidth': 0.4}  

instgratingbg.sf=4.5 #20cycles per 400pix
instgratingbg.contrast = 0.25 #25% contrast

instgratingbg_vpos=[-1.5,-1.5]
instgratingbg_hpos=[-6,6]



instgrating_vpos = [0, 0]
instgrating_hpos = [-.5, .5]

instgrating_phase = [0.0, 0.0]
instorientations = [90.0, 90.0]
instbgorientations = [90,0]
instgrating.mask = "raisedCos"
instgrating.maskParams = {'fringeWidth': 0.4}  
instgrating_sf= [4.5,4.5]
#contrast = 0.1

instcontrasts = [.5, 0]
for i_phase in range(2): #show the number of circles
    
    instgratingbg.phase = instgrating_phase[i_phase]
    instgratingbg.pos = [instgratingbg_hpos[i_phase], instgratingbg_vpos[i_phase]]
    instgratingbg.sf = instgrating_sf[i_phase]
    instgratingbg.ori = instbgorientations[i_phase]
    instgratingbg.contrast = .25
    instgratingbg.draw()
    for i_phase2 in range(2): #show the numbers of holes
        instgrating.phase = instgrating_phase[i_phase2]
        instgrating.pos = [instgratingbg_hpos[i_phase]+instgrating_hpos[i_phase2], instgratingbg_vpos[i_phase]+instgrating_vpos[i_phase2]]
        instgrating.sf = instgrating_sf[i_phase2]
        instgrating.ori = instorientations[i_phase2]
        instgrating.contrast = instcontrasts[i_phase2]
        instgrating.draw()
    instcontrasts = np.roll(instcontrasts,1)
    


win.flip()
# We flip
trialno=0
blockno=0
# and wait for key press to start the experiment.
keys = event.waitKeys(keyList=['space','escape'])#core.wait(.1)

instructions2.text= instruction_dictionary['instructions.text6c']
instructions2.pos=[0,5]
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

instructions2.text= instruction_dictionary['instructions.text6a']
instructions2.pos=[0,-7]
instructions2.draw()

instructions2.text= instruction_dictionary['instructions.text6b']
instructions2.pos=[0,-10]
instructions2.draw()
win.flip()


# last instructions screen
keys = event.waitKeys(keyList=['space','escape'])#core.wait(.1)


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

instructions2.text= instruction_dictionary['instructions.text5']
instructions2.pos=[0,5]
instructions2.draw()


instructions2.text= instruction_dictionary['instructions.text6']
instructions2.pos=[0,-9]
instructions2.draw()
win.flip()

keys = event.waitKeys(keyList=['space','escape'])#core.wait(.1)
# %% Block break function
def block_break(block_no, timer, alltotal):
    win.setColor([-.3, -.3, -.3], colorSpace='rgb')
    # timer=1
    intblocktext = visual.TextStim(
                    win=win,
                    height=.65,
                    font="Palatino Linotype",
                    alignHoriz='center',
                    color = [color_text,color_text,color_text])   
    timertext = visual.TextStim(win=win,
            height=.65, 
            pos=[0,-5],
            font="Palatino Linotype",
            alignHoriz = 'center',
            color = [color_text,color_text,color_text])
    if trialno == alltotal:
        endtext = visual.TextStim(
                win=win,
                height=.65,
                font="Palatino Linotype",
                alignHoriz='center',
                color = [color_text,color_text,color_text])     
        endtext.text= instruction_dictionary['endtext.text']
        endtext.draw()
        win.flip()
        keys = event.waitKeys()
    intblocktext.text= instruction_dictionary['intblocktext.text'] + str(block_no) + """/""" + str(totalblocks)
    for time in range(timer):
        timer-=1
        intblocktext.draw()
        timertext.text=""":""" + str(timer)
        timertext.draw()
        core.wait(1)
        win.flip()
        if timer == 0:
            timertext.text= instruction_dictionary['timertext.text']
            intblocktext.draw()
            timertext.draw()
            win.flip()
    keys = event.waitKeys(keyList=['space','escape'])
    win.color='grey'
    if 'escape' in keys:
        win.close()
        trials.saveAsWideText(data_fname + '.csv', delim=',')
    win.flip()
    core.wait(2)
# %% Trial Sequence

rnd.shuffle(phases)
currphase=phases[0]

def trialsequence(currcontrast, currphase, bgori, maskParam, position):
    #Draw the black fixation dot
    circle.pos=[0,0]
    circle.radius=.075
    circle.fillColor=[-1, -1, -1]
    circle.lineColor=[-1, -1, -1]
    circle.draw()
    win.flip()
    core.wait(.5)
    #Set contrasts to 0
    contrasts = [0, 0]
    # increase one of them to the current contrast
    contrasts[position] = currcontrast
    #We prepare the gratings in the meantime
    
    gratingbg.ori = bgori
    gratingbg.maskParams =  {'fringeWidth': maskParam}
    gratingbg.phase=currphase
    grating_phase = [currphase, currphase]
    
    #Draw the black fixation dot
    circle.draw()
    win.flip()
    core.wait(.5)
    
    for nFrames in range(EmptyFrame):            # .05 empty screen
        circle.draw()
        win.flip()
        
    #We draw 2 target gratings and the bg grating on the screen, alongside the white fixation dot.
    for nFrames in range(GratingFrame): # .1 seconds bg+target displayed
        #In isolated condition, we show no bg.
        if bgori != 361: #draw a background if the condition is not the third
            gratingbg.draw() #draw a background
        circle.draw()
        for i_phase in range(2):
            grating.pos = [grating_hpos[i_phase], grating_vpos[i_phase]]
            grating.phase = grating_phase[i_phase]
            grating.contrast = contrasts[i_phase]
            grating.draw()
        win.flip()

    #After the presentation is completed, the inside of the fixation dot turns
    #Dark grey.
    circle.fillColor=[-.5,-.5,-.5]
    circle.lineColor=[-.5,-.5,-.5]
    circle.draw()       
    #And we draw 2 faded circles at the 2 locations for the subject to choose.
    for circ_loc in range(2):
        circle.radius = size/2
        circle.fillColor=[0,0,0]
        circle.lineColor=[-.1,-.1,-.1]
        circle.lineWidth=0.75
        circle.pos = [grating_hpos[circ_loc],grating_vpos[circ_loc]]
        circle.draw()
    win.flip()
    rt_clock = core.Clock()        
    #And we wait for a key response, and we record RT
    keys = event.waitKeys(keyList=['s','l','escape','p'])
    rt=rt_clock.getTime()
    resp=0
            #If the key is pressed analyze the keypress, and change the position of
        #text pointer to the location the participant chose.
    if keys:
        if 's' in keys:
            resp = 0
            feedback.pos=[-float(exp_info['eccentricity']),0]
        elif 'l' in keys:
            resp = 1
            feedback.pos=[float(exp_info['eccentricity']),0]
        elif 'esc' in keys:
            win.close()
            
    
    #We check accuracy after the key press, and show a check or cross depending on that.
    if resp == 0 and position == 0:
        acc = 1
        feedback.text = """✔"""
    elif resp == 1 and position == 1:
        acc = 1
        feedback.text = """✔"""
    else:
        acc = 0         
        feedback.text = """✘"""
    
    for circ_loc in range(2): #circle that appears with the feedback
        circle.radius = size/2
        circle.fillColor=[0,0,0]
        circle.lineColor=[-.1,-.1,-.1]
        circle.lineWidth=0.75
        circle.pos = [grating_hpos[circ_loc],grating_vpos[circ_loc]]
        circle.draw()
    feedback.color = [-.5,-.5,-.5]
    feedback.draw()
    win.flip()
    core.wait(.2)
    
    if rt < 2:
        #circle.draw()
        win.flip()
        waiter=2-rt
        core.wait(waiter)
    else:
        #circle.draw()
        win.flip()
    
    return acc, keys, rt, resp
    

#%% Practice trial

win.flip()
pracscont = np.geomspace(0.01,0.1,12)
pracstarg = npm.repmat([0,1],1,6)
pracstarg = pracstarg[0]
pracsbgori = npm.repmat([0,90,361],1,4)
pracsbgori = pracsbgori[0]

prac_order=[]
for cont, targ, bgori in zip(pracscont, pracstarg, pracsbgori):
    prac_order.append({'cont': cont, 'targ':targ,'bgori':bgori})

practrials = data.TrialHandler(prac_order, nReps=1, extraInfo=exp_info,
                           method='random', originPath=datapath)
pracno=0

for trial in practrials:
    pracno+=1
    
    #We prepare the gratings in the meantime

    rnd.shuffle(phases)
    trialphase=phases[0]
    trialcontrast = [trial['cont']]
    if trial['bgori'] == 361:
        maskParams = 0.01
    else:
        maskParams = 0.4
    
    position = trial['targ']
    bgori = trial['bgori']
    
    acc, keys, rt, resp = trialsequence(trialcontrast, trialphase, bgori, maskParams, position)
    #keys = trseq2(trialcontrast, trialphase, bgori, position)
    
    if 'escape' in keys:
        win.close()
        break
    elif 'p' in keys:
        break
    
instructions2.text= instruction_dictionary['instructions.text7']
instructions2.pos=[0,0]
instructions2.draw()
win.flip()

keys = event.waitKeys(keyList=['space','escape'])#core.wait(.1)


#%% Trial Block 
block_no = 0
for trial in trials:
    if trialno > 0 and trialno%80 == 0:
        block_no += 1 
        block_break(block_no,30, alltotal)
        #Which condition, which staircase:    
            
            
    
            
    
    if trial['cond'] == 1:
        if trial['staircase'] == 1:
            while psiParr1.xCurrent == None:
                pass # hang in this loop until the psi calculation has finished
            contrast = psiParr1.xCurrent 
        elif trial['staircase'] == 2:
            while psiParr2.xCurrent == None:
                pass # hang in this loop until the psi calculation has finished
            contrast = psiParr2.xCurrent
    elif trial['cond'] == 2:
        if trial['staircase'] == 1:
            while psiOrth1.xCurrent == None:
                pass # hang in this loop until the psi calculation has finished 
            contrast = psiOrth1.xCurrent
        elif trial['staircase'] == 2:
            while psiOrth2.xCurrent == None:
                pass # hang in this loop until the psi calculation has finished
            contrast = psiOrth2.xCurrent
    elif trial['cond'] == 3:
        if trial['staircase'] == 1:
            while psiIso1.xCurrent == None:
                pass # hang in this loop until the psi calculation has finished
            contrast = psiIso1.xCurrent
        elif trial['staircase'] == 2:
            while psiIso2.xCurrent == None:
                pass # hang in this loop until the psi calculation has finished 
            contrast = psiIso2.xCurrent

    trialno+=1
    if trialno%(nTrials*nStaircase) == 1:
        circle = visual.Circle(
                win=win,
                units="deg",
                radius=.075,
                fillColor=[-1, -1, -1],
                lineColor=[-1, -1, -1]
                )
        circle.draw()
        win.flip()
        core.wait(2)
    
    print('Trial %d of %d' % (trialno, alltotal))
    #Fixation dot, black during the 500 ms preparatory period
    circle = visual.Circle(
    win=win,
    units="deg",
    radius=.075,
    fillColor=[-1, -1, -1],
    lineColor=[-1, -1, -1]
    )
    
    
    rnd.shuffle(phases)
    trialphase=phases[0]
    if trial['bgori'] == 361:
        maskParams = 0.01
    else:
        maskParams = 0.4
    
    position = trial['targetloc']
    bgori = trial['bgori']
    
    acc, keys, rt, resp = trialsequence(contrast, trialphase, bgori, maskParams, position)
    
    #We add the response, and the stimulus properties to our trialHandler,
    # so that we can check them later in our csv output:
    trials.addData('resp', resp)
    trials.addData('rt', rt)
    trials.addData('acc', acc)
    trials.addData('contrast', contrast)
    if trial['cond'] == 1:
        if trial['staircase'] == 1:
            psiParr1.addData(acc)
        elif trial['staircase'] == 2:
            psiParr2.addData(acc)
    elif trial['cond'] == 2:
        if trial['staircase'] == 1:
            psiOrth1.addData(acc)
        elif trial['staircase'] == 2:
            psiOrth2.addData(acc)
    elif trial['cond'] == 3:
        if trial['staircase'] == 1:
            psiIso1.addData(acc)
        elif trial['staircase'] == 2:
            psiIso2.addData(acc)
    if 'escape' in keys:
        win.close()
        trials.saveAsWideText(data_fname + '.csv', delim=',')
        break

    #print(psi.xCurrent)
    
trials.saveAsWideText(data_fname + '.csv', delim=',')


win.close()


