# script created by pymel.tools.mel2py from mel file:
# \\powervault\users$\fschaller\git\intelligentmaya\imaya\samplepanelmel.mel

from pymel.all import *
# NOTE: The scriptedPanelType command does not support python
#               callbacks; these callbacks must be MEL.
def sampleCreateCallback(panelName):
	melGlobals.initVar( 'float', 'gSampleState[5' )
	#
	#  Description:
	#      Create any editors unparented here and do
	#      any other initialization required.
	#
	#      In this example we will only declare a global array to
	#        maintain some state information.
	#
	

def sampleInitCallback(panelName):
	melGlobals.initVar( 'float[]', 'gSampleState' )
	#
	#  Description:
	#      Re-initialize the panel on file -new or file -open.
	#
	#      In this example we will only re-init the global array.
	#
	melGlobals['gSampleState'][0]=20.2
	melGlobals['gSampleState'][1]=50.5
	melGlobals['gSampleState'][2]=34.7
	melGlobals['gSampleState'][3]=2.0
	melGlobals['gSampleState'][4]=1.0
	

def sampleAddCallback(panelName):
	melGlobals.initVar( 'float[]', 'gSampleState' )
	#
	#  Description:  Create UI and parent any editors.
	#
	columnLayout('topCol',adj=True)
	separator(h=10,style="none")
	frameLayout(mw=10,l="Sliders")
	columnLayout('sampleCol',adj=True)
	separator(h=10,style="none")
	floatSliderGrp('fsg1',v=melGlobals['gSampleState'][0],
		l="Property A",f=True)
	floatSliderGrp('fsg2',v=melGlobals['gSampleState'][1],
		l="Property B",f=True)
	floatSliderGrp('fsg3',v=melGlobals['gSampleState'][2],
		l="Property C",f=True)
	separator(h=10,style="none")
	setParent('..')
	setParent('..')
	separator(h=10,style="none")
	frameLayout(mw=10,l="Radio Buttons")
	columnLayout('sampleCol2')
	separator(h=10,style="none")
	radioButtonGrp('rbg',nrb=3,
		l="Big Options",
		select=melGlobals['gSampleState'][3],
		la3=("Option 1", "Option 2", "Option 3"))
	radioButtonGrp('rbg2',nrb=3,
		l="Little Options",
		select=melGlobals['gSampleState'][4],
		la3=("Option 4", "Option 5", "Option 6"))
	separator(h=10,style="none")
	

def sampleRemoveCallback(panelName):
	melGlobals.initVar( 'float[]', 'gSampleState' )
	#
	#  Description:
	#        Unparent any editors and save state if required.
	#
	#  Scope the control names to this panel.
	#
	control=str(scriptedPanel(panelName,
		q=1,control=1))
	setParent(control)
	melGlobals['gSampleState'][0]=float(floatSliderGrp('fsg1',q=1,v=1))
	melGlobals['gSampleState'][1]=float(floatSliderGrp('fsg2',q=1,v=1))
	melGlobals['gSampleState'][2]=float(floatSliderGrp('fsg3',q=1,v=1))
	melGlobals['gSampleState'][3]=float(radioButtonGrp('rbg',q=1,sl=1))
	melGlobals['gSampleState'][4]=float(radioButtonGrp('rbg2',q=1,sl=1))
	

def sampleDeleteCallback(panelName):
	pass
	#
	#  Description:
	#        Delete any editors and do any other cleanup required.
	

def sampleSaveStateCallback(panelName):
	melGlobals.initVar( 'float[]', 'gSampleState' )
	#
	#  Description:
	#        Return a string that will restore the current state
	#        when it is executed.
	indent="\n\t\t\t"
	return (str(indent) + "$gSampleState[0]=" + str(melGlobals['gSampleState'][0]) + ";" + str(indent) + "$gSampleState[1]=" + str(melGlobals['gSampleState'][1]) + ";" + str(indent) + "$gSampleState[2]=" + str(melGlobals['gSampleState'][2]) + ";" + str(indent) + "$gSampleState[3]=" + str(melGlobals['gSampleState'][3]) + ";" + str(indent) + "$gSampleState[4]=" + str(melGlobals['gSampleState'][4]) + ";" + str(indent) + "setSamplePanelState $panelName;\n")
	

def setSamplePanelState(whichPanel):
	melGlobals.initVar( 'float[]', 'gSampleState' )
	#
	#  Description:
	#        This is a convenience proc to set the panel state from the
	#        global array
	#  Scope the control names to this panel.
	#
	control=str(scriptedPanel(whichPanel,
		q=1,control=1))
	if "" != control:
		setParent(control)
		floatSliderGrp('fsg1',e=1,v=melGlobals['gSampleState'][0])
		floatSliderGrp('fsg2',e=1,v=melGlobals['gSampleState'][1])
		floatSliderGrp('fsg3',e=1,v=melGlobals['gSampleState'][2])
		if 0 != melGlobals['gSampleState'][3]:
			radioButtonGrp('rbg',e=1,sl=melGlobals['gSampleState'][3])
			
		
		# radio button off bei 0??
		if 0 != melGlobals['gSampleState'][4]:
			radioButtonGrp('rbg2',e=1,sl=melGlobals['gSampleState'][4])
			
		
	

