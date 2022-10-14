# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 15:28:03 2022

@author: Marius
"""




## if you get freetype library error, go to this website:
    #http://gnuwin32.sourceforge.net/packages/freetype.htm 
# Click on "Complete package, except sources" and download and install
# the .exe file 
# Additionally, you should install Microsoft Visual Studio Community, 
# Which somehow helps integrate the two.
# %%

import os # for file/folder operations
import numpy as np
import numpy.random as rnd          # for random number generators
import numpy.matlib as npm  
from psychopy import visual, event, core, gui, data, monitors
import PsiMarginal
import copy
import translators as ts # for translation

#%%
# we make a function in which the english dictionary is translated into whetever 'langage' you are selecting
# we are currently using 'google.translate' but you can use deepl and others as well
def intoenglish(input_dictionary,language): 
    instruction_dictionary_english={} # made for french word initially but doesn't matter in the end
    for k,phrase in input_dictionary.items():
       translater = ts.google(phrase, from_language='fr', to_language=language)
       instruction_dictionary_english[k] = translater
    return instruction_dictionary_english
    


datapath = 'data'

#%%=======================================
#Store info about the experiment session
#========================================
    
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
        'screenwidth(cm)': '49',
        'screenresolutionhori(pixels)': '1920',
        'screenresolutionvert(pixels)': '1200',
        'refreshrate(hz)': '100'
        }

dlg = gui.DlgFromDict(dictionary=exp_info, title=exp_name)
           
# Here we make a dictionary with all the instruction in english to be able to translate them all later on
instruction_dictionary={"instructions.text1": "Dans cette expérience, vous verez des petites parcelles de barres horizontales située soit dans un des deux endroits possible à l'intérieur d'un plus grand cercle de barres, ou isolées, sans aucun contexte.\n\n Votre tâche consiste à localiser où les barres vont apparaitre à chaque essai et à répondre en appuyant sur une touche de votre clavier. Si les barres horizontales apparaissent:\n\n",
                         "instructions.text2": "Sur la gauche \nAppuyez sur la flèche de gauche ",
                         "instructions.text3": "Sur la droite \nAppuyez sur la flèche de droite",
                         "instructions.text4": "Après avoir répondu, vous recevrez un court feedback sur votre performance.\nAu total cette expérience devrait durer ~45 minutes\n(9 blocs, 80 essais chacun).\nN'hésitez pas à prendre une petite pause entre chaque des blocs.\nAppuyez sur la barre 'ESPACE' pour la prochaine instruction.",
                         "instructions.text5": "Maintenant, vous allez réaliser un petit entrainement.\nAvant de commencer, assurez vous que votre tête soit positionée de manière à ce que la croix au milieu de l'écran soit alignée avec vos yeux.",
                         "instructions.text6": "Veuillez garder votre regard fixé au centre durant toute l'expérience.\nAppuyez sur la barre 'ESPACE' pour commencer l entrainement.",
                         "instructions.text7": "Bravo!\nVous avez terminé l'entrainement.\nAppuyez sur la barre 'ESPACE' pour commencer l'expérience .\nBloc:0/9",
                         "intblocktext.text":"Prenez le temps de vous reposer avant le prochain bloc. Vous pouvez appuyer sur la barre 'ESPACE' pour continuer après 30 secondes lorsque vous serez prêt.\nBloc: ",
                         "endtext.text":"Merci pour votre participation.\nAppuyez sur une touche pour quitter l'expérience"}       
       
#%% Now we translate the instruction if required
if exp_info['language']!='fr':
    language = exp_info['language']
    instruction_dictionary=intoenglish(instruction_dictionary, language)   

# If 'Cancel' is pressed, quit
if dlg.OK == False:
    core.quit()
        
# Get date and time
exp_info['date'] = data.getDateStr()
exp_info['exp_name'] = exp_name

# Create a unique filename for the experiment data
if not os.path.isdir(datapath):
    os.makedirs(datapath)
data_fname = exp_info['participant'] + '_' + exp_info['date'] + '_' + exp_info['eccentricity'] + '-' + exp_info['Stim_size']
data_fname = os.path.join(datapath, data_fname)
    

#%% Psi Parameters

stimRange = np.geomspace(0.001,1,350,endpoint=True)    # Contrast ranges between .001 and 1, 350 possibilities.
Pfunction = 'Weibull' #aka log Weibull 
nTrials = 40 # Trials per staircase, per block = nTrials x 2 # Must be dividible by 4
nStaircase = 2 
nConditions = 3 #Parallel, Orthogonal, Isolated
nTemporal = 1 # if only Simultaneous, 1
              # else, 2
nRunPerCond = 3

threshold = stimRange 
thresholdOrthSimPrior = ('normal',.0139,.07) # Prior for Orthogonal Context condition
thresholdParrSimPrior = ('normal',.2549, .2) # Prior for Parallel Context condition
thresholdIsoSimPrior = ('normal',.0137,.07) # Prior for Isolated condition


sigma = np.geomspace(0.5,20,50,endpoint=True) #slope
slopePrior = ('gamma', 3, 6)#('gamma',3,.1) #normal dist, mean, sd
guessRate = 0.50 #it's a 2AFC, so guessRate is 50%
guessPrior = ('uniform',None) #we enter no prior for guess rate.
lapse = 0.05 #lapse rate is observer-based errors, such as pressing a wrong key. we set it to 5%. 
lapsePrior = ('beta',2,20) #try changing this
marginalize = True

# Here we define 2 Psi staircases for each of the context conditions(parallel, orthogonal, isolated)
# 


psiParrSim1 = PsiMarginal.Psi(stimRange, Pfunction=Pfunction, nTrials=nTrials, threshold=stimRange, thresholdPrior=thresholdParrSimPrior,
                      slope=sigma, slopePrior=slopePrior, guessRate=guessRate, guessPrior=guessPrior,
                      lapseRate=lapse, lapsePrior=lapsePrior, marginalize=marginalize)
psiParrSim2 = PsiMarginal.Psi(stimRange, Pfunction=Pfunction, nTrials=nTrials, threshold=stimRange, thresholdPrior=thresholdParrSimPrior,
                      slope=sigma, slopePrior=slopePrior, guessRate=guessRate, guessPrior=guessPrior,
                      lapseRate=lapse, lapsePrior=lapsePrior, marginalize=marginalize)
psiIsoSim1 = PsiMarginal.Psi(stimRange, Pfunction=Pfunction, nTrials=nTrials, threshold=stimRange, thresholdPrior=thresholdIsoSimPrior,
                      slope=sigma, slopePrior=slopePrior, guessRate=guessRate, guessPrior=guessPrior,
                      lapseRate=lapse, lapsePrior=lapsePrior, marginalize=marginalize)
psiIsoSim2 = PsiMarginal.Psi(stimRange, Pfunction=Pfunction, nTrials=nTrials, threshold=stimRange, thresholdPrior=thresholdIsoSimPrior,
                      slope=sigma, slopePrior=slopePrior, guessRate=guessRate, guessPrior=guessPrior,
                      lapseRate=lapse, lapsePrior=lapsePrior, marginalize=marginalize)
psiOrthSim1 = PsiMarginal.Psi(stimRange, Pfunction=Pfunction, nTrials=nTrials, threshold=stimRange, thresholdPrior=thresholdOrthSimPrior,
                      slope=sigma, slopePrior=slopePrior, guessRate=guessRate, guessPrior=guessPrior,
                      lapseRate=lapse, lapsePrior=lapsePrior, marginalize=marginalize)
psiOrthSim2 = PsiMarginal.Psi(stimRange, Pfunction=Pfunction, nTrials=nTrials, threshold=stimRange, thresholdPrior=thresholdOrthSimPrior,
                      slope=sigma, slopePrior=slopePrior, guessRate=guessRate, guessPrior=guessPrior,
                      lapseRate=lapse, lapsePrior=lapsePrior, marginalize=marginalize)


#%% Background orientation has two possibilities: Parallel or Orthogonal to the target
bgorilist = npm.repmat(np.repeat([90,0,361],int(nTrials*nStaircase)),1,nTemporal)
bgorilist = bgorilist[0]

#temporal relationship: simultaneous, or leading

if nTemporal == 1:
    templist=np.sort(npm.repmat([0],1,int(nTrials)*nConditions*nStaircase))
    templist=templist[0]
else:        
    templist= np.sort(npm.repmat([0,1],1,int(nTrials*nConditions*nStaircase)))
    templist= templist[0]


staircaselist=npm.repmat(np.sort(npm.repmat(list(range(1,nStaircase+1)),1,int(nTrials))),1,nTemporal*nConditions)
staircaselist=staircaselist[0]
#print(staircaselist)

#Targets can be shown at either one of 2 locations. 
targetloclist = npm.repmat([0,1],1,int(nTrials/2*nConditions*nTemporal*nStaircase)) # We divide by two
targetloclist = targetloclist[0]




stim_order = []
    
#Creating a list of dictionaries that contains information about each single trial.
for bgori, temp, targloc, staircase in zip(bgorilist, templist, targetloclist, staircaselist):
    stim_order.append({'bgori': bgori, 'temp':temp, 'staircase':staircase, 'targetloc': targloc,})
print(stim_order)
responses = []

#%% This part is about shuffling
#We need to shuffle the staircases WITHIN each condition.
#because of the ordering I made in the stim_order, 
#conditions are always in the following order:
#ParrSim1-ParrSim2-OrthSim1-OrthSim2-IsoSim1-IsoSim2
#If you get rid of a temporal condition or a staircase, the order stays the same,
#Just that the removed ones are dropped from the order
#For example, if you do nTemporal=2, nStaircase=1
#It becomes: ParrSim1-OrthSim1-ParrLead1-OrthLead1



#Now we will intermingle the two staircases for each condition (if there is two)

#For that, we first slice the stim_order into 3 (for each condition), and shuffle within each
# slice 

ParrSim=[]
OrthSim=[]
IsoSim=[]

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

ParrSim=copy.deepcopy(PS1) 
OrthSim=copy.deepcopy(OS1)
IsoSim=copy.deepcopy(IS1) # We deepcopy, because if we don't, they are still 
                            # connected to the stim_order, and if we do any operation,
                            # stim_order gets affected from that change as well.

rnd.shuffle(ParrSim)
rnd.shuffle(OrthSim)
rnd.shuffle(IsoSim)


#Shuffling order of runs/conditions
conds=[]
cond_order= [1,2,3]
#cond_order=npm.repmat([1,2],1,3)
for i in range(nRunPerCond):
    rnd.shuffle(cond_order)
    conds.extend(cond_order)


#Tagging the conditions with the corresponding number
# Parallel = 1, Orthogonal = 2, Isolated = 3
for ind in range(0,int(len(ParrSim))):
        ParrSim[ind].update(cond=1)
for ind in range(0,int(len(OrthSim))):
        OrthSim[ind].update(cond=2)
for ind in range(0,int(len(IsoSim))):
        IsoSim[ind].update(cond=3)
    
#Putting all the shuffled, mixed, trial blocks into one final variable
#using the shuffled condition order
alltrials = []
for i in range(0,int(len(conds))):
    if conds[i] == 1:
        alltrials.extend(ParrSim)
    elif conds[i] == 2:
        alltrials.extend(OrthSim)
    elif conds[i] == 3:
        alltrials.extend(IsoSim)
        
        
#using PsychoPy's TrialHandler, makes it easier to index in a loop, and output
trials = data.TrialHandler(alltrials, nReps=1, extraInfo=exp_info,
                           method='sequential', originPath=datapath)

#%%=======================================
# Window Settings and grating properties 
#=======================================
    
#We define a monitor, which helps control for visual angle.
mon = monitors.Monitor('mon1')
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
SimEmptyFrame=int(50/framelength) #50 ms
SimFrame = int(100/framelength) #100 ms
LeadFrame = int(50/framelength) #50 ms


mon.setSizePix(scrsize)
# Open a window
win = visual.Window(monitor = mon, 
                    size =scrsize,
                    color='grey',
                    units='deg',
                    fullscr=False)
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
    size=[20,20]
)

#We put a raised cosine wave mask around it so it looks nice and smooth at the edges
gratingbg.mask = "raisedCos"
gratingbg.maskParams = {'fringeWidth': 0.4}  

gratingbg.sf=2 #1 cpd
gratingbg.contrast = 0.25 #25% contrast
gratingbg.phase = 0.0 #for now it's 0 but we randomly change and adapt this to the target in trial loop

#Each of the 2 target gratings is going to appear 
#at 5 degrees eccentricity from the center
grating_vpos = [0, 0] # height (0 = center)
grating_hpos = [-float(exp_info['eccentricity']), float(exp_info['eccentricity'])]# laterality (0 = center)

# target grating is ALWAYS HORIZONTAL:
orientations = [90.0, 90.0] 
# random phase between 0 and 1
phases = np.arange(0,1,.03)
# all of them have the identical sf as the bg grating.
grating_sf= [1,1]
# at the beginning, all four have 0 contrast, depending on where the 
# target will be shown and the staircase, we'll increase contrast at 
# one of four points in each trial.
contrasts = [0, 0]


#%%=================================
# Preparing the instruction screen 
#=================================
    
# We draw the text explaining what we will show
instructions = visual.TextStim(
    win=win,
    pos=[0,6],
    wrapWidth=None,
    height=.5,
    font="Palatino Linotype",
    alignHoriz='center'
    )

    
instructions.text = instruction_dictionary['instructions.text1']

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

instructions2.text = instruction_dictionary['instructions.text2']

instructions2.draw()

instructions2 = visual.TextStim(
    win=win,
    pos=[6,3],
    wrapWidth=None,
    height=.5,
    font="Palatino Linotype",
    alignHoriz='center'
    )

instructions2.text = instruction_dictionary['instructions.text3']
instructions2.draw()



# The last text

instructions2.text= instruction_dictionary['instructions.text4']
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

instgratingbg_vpos=[-1.5,-1.5]
instgratingbg_hpos=[-6,6]



instgrating_vpos = [0, 0]
instgrating_hpos = [-.5, .5]

instgrating_phase = [0.0, 0.0]
instorientations = [90.0, 90.0]
instbgorientations = [90,0]
instgrating.mask = "raisedCos"
instgrating.maskParams = {'fringeWidth': 0.4}  
instgrating_sf= [3,3]
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

instructions2.text= instruction_dictionary['instructions.text5']
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


instructions2.text= instruction_dictionary['instructions.text6']
instructions2.pos=[0,-3]
instructions2.draw()
win.flip()


keys = event.waitKeys(keyList=['space','escape'])#core.wait(.1)


#%%============================
# Begin of the practice trial
#============================

win.flip()
pracscont = np.geomspace(0.005,0.03,20)
pracstarg = npm.repmat([0,1,2,3],1,5)
pracstarg = pracstarg[0]

prac_order=[]
for cont, targ in zip(pracscont, pracstarg):
    prac_order.append({'cont': cont, 'targ':targ})

practrials = data.TrialHandler(prac_order, nReps=1, extraInfo=exp_info,
                           method='random', originPath=datapath)



pracno=0

for trial in practrials:
    pracno+=1
    
    if pracno%20 == 1:
        circle = visual.Circle(
                win=win,
                units="deg",
                radius=.1,
                fillColor=[-1, -1, -1],
                lineColor=[-1, -1, -1]
                )
        circle.draw()
        win.flip()
        core.wait(2)
    #Drawing the center dot
    circle = visual.Circle(
    win=win,
    units="deg",
    radius=.1,
    fillColor=[-1, -1, -1],
    lineColor=[-1, -1, -1]
    )
    
    #We prepare the gratings in the meantime

    grating.mask = "raisedCos"
    grating.maskParams = {'fringeWidth': 0.1}  
    rnd.shuffle(phases)
    currphase=phases[0]
    grating_phase = [currphase, currphase]
    gratingbg.phase=currphase

    #Draw the black fixation dot
    circle.draw()
    win.flip()
    core.wait(.5)
    
    contrast = [trial['cont']]
    #Set contrasts to 0
    contrasts = [0, 0, 0, 0]
    #Set one of the contrasts to what the staircase determines:
    contrasts[trial['targ']] = contrast
    # Inside of the fixation dot is turned white during the stimulus presentation
    
    circle.fillColor=[1,1,1]
    circle.draw()
    for nFrames in range(SimEmptyFrame):            # .05 empty screen
        circle.draw()
        win.flip()
        
    #We draw 2 target gratings and the bg grating on the screen, alongside the white fixation dot.
    for nFrames in range(SimFrame): # .1 seconds bg+target displayed
        #In isolated condition, we show no bg.
        circle.draw()
        for i_phase in range(2):
    
            grating.phase = grating_phase[i_phase]
            grating.pos = [grating_hpos[i_phase], grating_vpos[i_phase]]
            grating.sf = grating_sf[i_phase]
            grating.ori = orientations[i_phase]
            grating.contrast = contrasts[i_phase]
            grating.draw()
        win.flip()
            


    #After the presentation is completed, the inside of the fixation dot turns
    #Dark grey.
    circle.fillColor=[-.5,-.5,-.5]
    circle.draw()       
    #And we draw 2 faded circles at the 2 locations for the subject to choose.
    for circ_loc in range(2):
        circle.radius = size/2
        circle.fillColor=[0,0,0]
        circle.lineColor=[-.1,-.1,-.1]
        circle.pos = [grating_hpos[circ_loc],grating_vpos[circ_loc]]
        circle.draw()
    win.flip()
    rt_clock = core.Clock()        
    #And we wait for a key response, and we record RT
    keys = event.waitKeys(keyList=['left','right','escape'])
    rt=rt_clock.getTime()
    
    
    #we will draw a check or cross at the center of the chosen circle
    #So we first create the "text" pointer for that.
    feedback = visual.TextStim(
    win=win,
    pos=[9,0],
    wrapWidth=None,
    height=.5,
    font="Palatino Linotype",
    alignHoriz='center'
    )                         
        #If the key is pressed analyze the keypress, and change the position of
        #text pointer to the location the participant chose.
    if keys:
        if 'escape' in keys:
            win.close()
            break
        elif 'left' in keys:
            resp = 0
            #feedback.pos=[-5,0]
            feedback.pos=[-float(exp_info['eccentricity']),0]
        elif 'right' in keys:
            resp = 1
            #feedback.pos=[5,0]
            feedback.pos=[float(exp_info['eccentricity']),0]
    #We check accuracy after the key press, and show a check or cross depending on that.
    if resp == 0 and trial['targ'] == 0:
        acc = 1
        feedback.text = """✔"""
    elif resp == 1 and trial['targ'] == 1:
        acc = 1
        feedback.text = """✔"""
    elif resp == 0 and trial['targ'] == 2:
        acc = 1
        feedback.text = """✔"""
    elif resp == 1 and trial['targ'] == 3:
        acc = 1
        feedback.text = """✔"""
    else:
        acc = 0         
        feedback.text = """✘"""
    
    for circ_loc in range(2):
        circle.radius = size/2
        circle.fillColor=[0,0,0]
        circle.lineColor=[-.1,-.1,-.1]
        circle.pos = [grating_hpos[circ_loc],grating_vpos[circ_loc]]
        circle.draw()
    feedback.color = [-.5,-.5,-.5]
    feedback.draw()
    win.flip()
    core.wait(.2)
    
    
    circle = visual.Circle(
                win=win,
                units="deg",
                radius=.1,
                fillColor=[-1, -1, -1],
                lineColor=[-1, -1, -1]
                )
    
    if rt < 2:
        circle.draw()
        win.flip()
        waiter=2-rt
        core.wait(waiter)
    else:
        circle.draw()
        win.flip()



instructions2.text= instruction_dictionary['instructions.text7']
instructions2.pos=[0,0]
instructions2.draw()
win.flip()

keys = event.waitKeys(keyList=['space','escape'])#core.wait(.1)

#%%========================
# Beginning of the trials
#========================

for trial in trials:
    #Which condition, which staircase:    
    if trial['cond'] == 1:
        if trial['staircase'] == 1:
            while psiParrSim1.xCurrent == None:
                pass # hang in this loop until the psi calculation has finished
            contrast = psiParrSim1.xCurrent 
        elif trial['staircase'] == 2:
            while psiParrSim2.xCurrent == None:
                pass # hang in this loop until the psi calculation has finished
            contrast = psiParrSim2.xCurrent
    elif trial['cond'] == 2:
        if trial['staircase'] == 1:
            while psiOrthSim1.xCurrent == None:
                pass # hang in this loop until the psi calculation has finished 
            contrast = psiOrthSim1.xCurrent
        elif trial['staircase'] == 2:
            while psiOrthSim2.xCurrent == None:
                pass # hang in this loop until the psi calculation has finished
            contrast = psiOrthSim2.xCurrent
    elif trial['cond'] == 3:
        if trial['staircase'] == 1:
            while psiIsoSim1.xCurrent == None:
                pass # hang in this loop until the psi calculation has finished
            contrast = psiIsoSim1.xCurrent
        elif trial['staircase'] == 2:
            while psiIsoSim2.xCurrent == None:
                pass # hang in this loop until the psi calculation has finished 
            contrast = psiIsoSim2.xCurrent
            
    trialno=trialno+1
    if trialno%(nTrials*nStaircase) == 1:
        circle = visual.Circle(
                win=win,
                units="deg",
                radius=.1,
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
    radius=.1,
    fillColor=[-1, -1, -1],
    lineColor=[-1, -1, -1]
    )
    
    #We prepare the gratings in the meantime
    if trial['cond'] != 3:
        gratingbg.ori = trial['bgori']
    
    grating.mask = "raisedCos"
    grating.maskParams = {'fringeWidth': 0.1}  
    rnd.shuffle(phases)
    currphase=phases[0]
    grating_phase = [currphase, currphase]
    gratingbg.phase=currphase

    #Draw the black fixation dot
    circle.draw()
    win.flip()
    core.wait(.5)
    
    #Set contrasts to 0
    contrasts = [0, 0]
    #Set one of the contrasts to what the staircase determines:
    contrasts[trial['targetloc']] = contrast
    # Inside of the fixation dot is turned white during the stimulus presentation
    
    circle.fillColor=[1,1,1]
    circle.draw()
    for nFrames in range(SimEmptyFrame):            # .05 empty screen
        circle.draw()
        win.flip()
        
    #We draw 2 target gratings and the bg grating on the screen, alongside the white fixation dot.
    for nFrames in range(SimFrame): # .1 seconds bg+target displayed
        #In isolated condition, we show no bg.
        if trial['cond'] != 3: #draw a background if the condition is not the third
            gratingbg.draw() #draw a background
        circle.draw()
        for i_phase in range(2):
    
            grating.phase = grating_phase[i_phase]
            grating.pos = [grating_hpos[i_phase], grating_vpos[i_phase]]
            grating.sf = grating_sf[i_phase]
            grating.ori = orientations[i_phase]
            grating.contrast = contrasts[i_phase]
            grating.draw()
        win.flip()
            


    #After the presentation is completed, the inside of the fixation dot turns
    #Dark grey.
    circle.fillColor=[-.5,-.5,-.5]
    circle.draw()       
    #And we draw 2 faded circles at the 2 locations for the subject to choose.
    for circ_loc in range(2):
        circle.radius = size/2
        circle.fillColor=[0,0,0]
        circle.lineColor=[-.1,-.1,-.1]
        circle.pos = [grating_hpos[circ_loc],grating_vpos[circ_loc]]
        circle.draw()
    win.flip()
    rt_clock = core.Clock()        
    #And we wait for a key response, and we record RT
    keys = event.waitKeys(keyList=['left','right','escape'])
    rt=rt_clock.getTime()
    
    
    #we will draw a check or cross at the center of the chosen circle
    #So we first create the "text" pointer for that.
    feedback = visual.TextStim(
    win=win,
    pos=[9,0],
    wrapWidth=None,
    height=.5,
    font="Palatino Linotype",
    alignHoriz='center'
    )                         
        #If the key is pressed analyze the keypress, and change the position of
        #text pointer to the location the participant chose.
    if keys:
        if 'escape' in keys:
            win.close()
            break
        elif 'left' in keys:
            resp = 0
            feedback.pos=[-float(exp_info['eccentricity']),0]
        elif 'right' in keys:
            resp = 1
            feedback.pos=[float(exp_info['eccentricity']),0]
    #We check accuracy after the key press, and show a check or cross depending on that.
    if resp == 0 and trial['targetloc'] == 0:
        acc = 1
        feedback.text = """✔"""
    elif resp == 1 and trial['targetloc'] == 1:
        acc = 1
        feedback.text = """✔"""
    elif resp == 0 and trial['targetloc'] == 2:
        acc = 1
        feedback.text = """✔"""
    elif resp == 1 and trial['targetloc'] == 3:
        acc = 1
        feedback.text = """✔"""
    else:
        acc = 0         
        feedback.text = """✘"""
    
    for circ_loc in range(2):
        circle.radius = size/2
        circle.fillColor=[0,0,0]
        circle.lineColor=[-.1,-.1,-.1]
        circle.pos = [grating_hpos[circ_loc],grating_vpos[circ_loc]]
        circle.draw()
    feedback.color = [-.5,-.5,-.5]
    feedback.draw()   
    win.flip()
    core.wait(.2)
    ##
    
    
    #We add the response, and the stimulus properties to our trialHandler,
    # so that we can check them later in our csv output:
    trials.addData('resp', resp)
    trials.addData('rt', rt)
    trials.addData('acc', acc)
    trials.addData('contrast', contrast)
    if trial['cond'] == 1:
        if trial['staircase'] == 1:
            psiParrSim1.addData(acc)
        elif trial['staircase'] == 2:
            psiParrSim2.addData(acc)
    elif trial['cond'] == 2:
        if trial['staircase'] == 1:
            psiOrthSim1.addData(acc)
        elif trial['staircase'] == 2:
            psiOrthSim2.addData(acc)
    elif trial['cond'] == 3:
        if trial['staircase'] == 1:
            psiIsoSim1.addData(acc)
        elif trial['staircase'] == 2:
            psiIsoSim2.addData(acc)

    #print(psi.xCurrent)
    
    
    #Depending on how long the participant took to response, we put an ITI
    circle = visual.Circle(
                win=win,
                units="deg",
                radius=.1,
                fillColor=[-1, -1, -1],
                lineColor=[-1, -1, -1]
                )
    if rt < 2:
        circle.draw()
        win.flip()
        waiter=2-rt
        core.wait(waiter)
    else:
        circle.draw()
        win.flip()
         
    #We take a break in between blocks:
    if trialno%(nTrials*2) == 0 and trialno != alltotal:
        blockno+=1
        timer1=30
        for timetime in range(30):
            intblocktext = visual.TextStim(
                    win=win,
                    height=.5,
                    font="Palatino Linotype",
                    alignHoriz='center'
                    )   
            intblocktext.text= instruction_dictionary['intblocktext.text'] + str(blockno) + """/9"""
            intblocktext.draw()
        
            timer1-=1
            timertext = visual.TextStim(
                win=win,
                height=.5,
                pos=[0,-5],
                font="Palatino Linotype",
                alignHoriz='center')
            timertext.text=""":""" + str(timer1)
            timertext.draw()
            core.wait(1)
            win.flip()
        
        keys = event.waitKeys(keyList=['escape','space'])
        if 'escape' in keys:
            win.close()
            break
    elif trialno == alltotal:
        endtext = visual.TextStim(
                win=win,
                height=.5,
                font="Palatino Linotype",
                alignHoriz='center'
                )   
        endtext.text= instruction_dictionary['endtext.text']
        endtext.draw()
        win.flip()
        keys = event.waitKeys()

 
trials.saveAsWideText(data_fname + '.csv', delim=',')


win.close()


