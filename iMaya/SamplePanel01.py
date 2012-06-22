import maya.cmds as cmds

# Below is the python code to create and use scriptedPanelType and scriptedPanel using the MEL
# callbacks defined above.

# Use unique flag as we don't want two panels sharing the same global data.
if not cmds.scriptedPanelType('sampleScriptedPanelType', ex=True): 
    cmds.scriptedPanelType( 'sampleScriptedPanelType', \
                        ccb='sampleCreateCallback', \
                        icb='sampleInitCallback', \
                        acb='sampleAddCallback', \
                        rcb='sampleRemoveCallback', \
                        dcb='sampleDeleteCallback', \
                        scb='sampleSaveStateCallback', \
                        unique=True )


#  This script will create an unparented scripted panel, place it
#  in one window, remove it, and place it in another window then
#  return it to the first window.
#
#
#  Create unparented scripted panel
#
cmds.scriptedPanel( 'sampleScriptedPanel', unParent=True, type='sampleScriptedPanelType', label='Sample' )

#    Create a couple of windows and parent the scripted panel to the first.
#
cmds.window( 'sampleWin' )
cmds.frameLayout( 'frm', lv=False, bv=False )
cmds.scriptedPanel( 'sampleScriptedPanel', e=True, parent='sampleWin|frm' )
cmds.showWindow()

cmds.window( 'sampleWin2', w=cmds.window('sampleWin', q=True, w=True), h=cmds.window('sampleWin', q=True, h=True) )
cmds.frameLayout( 'frm', lv=False, bv=False )
cmds.showWindow()

#    Reparent the scripted panel to the second window.
#
cmds.scriptedPanel( 'sampleScriptedPanel', e=True, unParent=True )
cmds.scriptedPanel( 'sampleScriptedPanel', e=True, parent='sampleWin2|frm' )

#    Reparent the scripted panel back to the first window.
#
cmds.scriptedPanel( 'sampleScriptedPanel', e=True, unParent=True )
cmds.scriptedPanel( 'sampleScriptedPanel', e=True, parent='sampleWin|frm' )

#    Close both windows
#
#cmds.window( 'sampleWin', e=True, visible=False )
#cmds.window( 'sampleWin2', e=True, visible=False )

#    The scripted panel should appear in the Panel menu.  Select
#    Panels->Panel->Sample and the panel should appear in the main window.
#