#Open all the tools you might need to use in your experiment code.

from psychopy import visual, core, gui, data, event
from psychopy import prefs
from psychopy.tools.filetools import toFile
import random


#Gets data from the participant
exptInfo = {'Participant Number:':'','Age':'','Gender:':'','Native Language:':'','Number of fluently Spoken Languages:':''}
exptDate = data.getDateStr()

dlg = gui.DlgFromDict(exptInfo, title='Open-Set Memory - Words', fixed=['exptDate'])
if dlg.OK:
    toFile('lastParams.pickle', exptInfo)  # save params to file for next time
else:
    core.quit()  # the user hit cancel so exit


#This tells the computer how and where it will be displaying everything. 
#It's critical that the name of the monitor matches the dimensions of the computer
#you're actually using. All of these scripts should be set up to run on the lab 
#computers, but if you're working on scripts at home, you'll have to create a monitor
#for you. Go to "Tools" --> "Monitor Center", create a new monitor object and enter its
#dimensions (height and width in pixels). Then put its name here, next to the monitor variable.
mywin = visual.Window([1800,1000], monitor="testMonitor", units = "deg")

#TrialHandler stuff
#import the info on each trial from an Excel file
stimListTargets = data.importConditions('sampleTestingSource.xlsx')
stimuliListTargets = data.importConditions('sampleTestingData.xlsx')


#set up the trial handler for TARGETS
trialsTargets = data.TrialHandler(stimListTargets, 1, method='random',dataTypes=[], extraInfo=exptInfo)
trialsTargetsStimuli = data.TrialHandler(stimuliListTargets, 1, method='random',dataTypes=[], extraInfo=exptInfo)

#Load the instructions slides (any you need)
instruct_begin = visual.ImageStim(mywin, image='sampleTestingData.jpg')
instructTest = visual.ImageStim(mywin, image='sampleTestingInstruction.jpg')


#show the instructions slide. Wait for a key press
instruct_begin.draw()
mywin.flip()
event.waitKeys()

# present the list of words for them to remember
nDone = 0
for thisTrial in trialsTargetsStimuli:  # handler can act like a for loop
    
    #Defines image variable for interest interestStimuli file
    stimuliImage = thisTrial['images']
    targetStimuliImage = visual.ImageStim(mywin, image=stimuliImage)
    
    #remind user of which key to press for which response
    instruct_message = visual.TextStim(mywin, alignHoriz='center', text='Press "F" if stimuli intended to measure, Press "J" if it varies')
    instruct_message.pos = [0.0,8]
    instruct_message.size = 1.5
            
    targetStimuliImage.draw()
    instruct_message.draw()
    mywin.flip()
            
     #Start the clock for measuring participant's response time
    RTclock= core.Clock()
        
            #Make the computer wait until it gets either an 'f' or a 'j' keyboard press
    while True:
                
        resp = event.getKeys(keyList=['f','j'])
                
        if len(resp)>0:
            break
    #Catch participant's response time
    RT = RTclock.getTime()
    #Save participants RT and response data
    trialsTargetsStimuli.data.add('response',resp)
    trialsTargetsStimuli.data.add('RT',RT)
    
for thisTrial in trialsTargets: 
    #Defines image variable for interest engagement file
    thisImage = thisTrial['image']
    targetImage = visual.ImageStim(mywin, image=thisImage)
    
    #Text to call attention
    instruct_message = visual.TextStim(mywin, alignHoriz='center', text="Stimuli based message") #CAN MAKE THIS BIGGER AND BOLD
    instruct_message.pos = [0.0,8]
    instruct_message.size = 1.5
    
    #Trying to show image
    targetImage.pos = [18,0.0]
    targetImage.draw()
    instruct_message.draw()
    
    #Trying to add second text
    instruct_message1 = visual.TextStim(mywin, alignHoriz='center', text="Press any key to continue") #CAN MAKE THIS BIGGER AND BOLD
    instruct_message1.pos = [0.0,-8]
    instruct_message1.size = 1.5
    
    instruct_message1.draw()
    wd_text = thisTrial['word']
    
    #Start the clock for measuring participant's response time
    RTclock= core.Clock()
    
    #Set up that text to show on the screen (where it should go, mostly)
    message = visual.TextStim(mywin, alignHoriz='right', text='%s'%(wd_text))
    message.pos = [-5,0.0] #negative numbers on the left for x coordinates, down for y coordinates
    message.size = 1.5 #I'm not sure that I see the effects of this in a straightforward way

    event.waitKeys()
    
    #Catch participant's response time
    RT = RTclock.getTime()
    #Save participants RT and response data
    #trialsTargets.data.add('response',resp)
    trialsTargets.data.add('RT',RT)
    
    #message.draw()
    #mywin.flip()
    
    event.clearEvents()
    nDone += 1
    



trialsTargets.saveAsExcel(fileName='sourceDataOut',  # ...an xlsx file (which supports sheets)
                  sheetName = 'engag',
                  stimOut=['word','image'])
                  
trialsTargetsStimuli.saveAsExcel(fileName='sourceDataOut',  # ...an xlsx file (which supports sheets)
                  sheetName = 'interest',
                  stimOut=['images'])

endmsg = visual.TextStim(mywin, alignHoriz='center', text="Thank you for participating! \n\n    Press any key to exit")
endmsg.draw()
mywin.flip()

event.waitKeys()


mywin.close()
core.quit()
