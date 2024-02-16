import maya.cmds as cmds
import random

def showScatter(*args):
    showCheckbox = cmds.checkBoxGrp(useCurve, q = True)
    cmds.floatSliderGrp(locationScatter, edit=True, enable=True)
   
def hideScatter(*args):
    showCheckbox = cmds.checkBoxGrp(useCurve, q = True, vis = False, v1 = False)
    cmds.floatSliderGrp(locationScatter, edit=True, enable=False)

#UI
window = cmds.window(title='Lilypad Generator', menuBar = True, width=250)
container = cmds.columnLayout()
cols = cmds.rowLayout(numberOfColumns=3, p=container)

leftmar = cmds.columnLayout(p=cols)
cmds.text('       ', p =leftmar)

maincol = cmds.columnLayout('Block', p=cols)
cmds.text('            ')

cmds.separator(height = 10)
nameparam = cmds.textFieldGrp(label = 'Name ')
cmds.separator(height = 10)
cmds.intSliderGrp("num", label="Number of Lilypads ", field = True, min = 1, max = 40, v = 15)
cmds.separator(height = 10)

curveInstructions = cmds.text('                Select an EP Curve or Bezier Curve to place the lilypads along?')
cmds.separator(height = 5)
useCurve = cmds.checkBoxGrp('useCurve', numberOfCheckBoxes=1, label='Use Curve ', v1=False, onc = hideScatter, ofc = showScatter)

locationScatter = cmds.floatSliderGrp("spread", label="Location Scatter ", field = True, min = 1, max = 50, v = 20)

cmds.separator(height = 10)
submitrow = cmds.rowLayout(numberOfColumns=2, p=maincol)
cmds.text(label='                                                                                                    ')
cmds.button(label="Create Lilypad(s)", c="createLilypad()", p = submitrow)

cmds.separator(height = 10, p = maincol)
rightmar = cmds.columnLayout(p=cols)
cmds.text('         ', p =rightmar)

cmds.showWindow(window)

def appendName(name, textstring):
    textstring = name + textstring
    return textstring
    
def normalDistrib(mean, std, size):
    numlist = []
    upperlim = mean + std
    otherupperlim = mean - std
    controlnum = int(size*0.341)
    for i in range(controlnum):
        numlist.append(random.uniform(mean, upperlim))
        numlist.append(random.uniform(otherupperlim, mean))
    lowerlim = upperlim
    upperlim = upperlim + std
    otherlowerlim = otherupperlim
    otherupperlim = otherupperlim - std
    if (otherupperlim < 0):
        otherupperlim = 0
    
    controlnum = int(size*0.136)
    for i in range(controlnum):
        numlist.append(random.uniform(lowerlim, upperlim))
        numlist.append(random.uniform(otherupperlim, otherlowerlim))
    lowerlim = upperlim
    upperlim = upperlim + std
    otherlowerlim = otherupperlim
    otherupperlim = otherupperlim - std
    if (otherupperlim < 0):
        otherupperlim = 0
    
    controlnum = int(size*0.021)
    for i in range(controlnum):
        numlist.append(random.uniform(lowerlim, upperlim))
        numlist.append(random.uniform(otherupperlim, otherlowerlim))
    
    while (len(numlist) < size):
        if (len(heightlist) == (size - 1)):
            sum = 0
            for h in range(len(numlist)):
                sum = sum + numlist[h]
            numlist.append((mean * size) - sum)
        else:
            upperlim = upperlim + std
            numlist.append(random.uniform(mean, upperlim))
            
    return numlist
    
def locations(curvename, level):
    position = cmds.pointOnCurve(curvename, pr = level, turnOnPercentage = True)
    return position
    
def randomLocation(size, spread):
    singleCoordinates = normalDistrib(200, spread, size)
    for i in range(len(singleCoordinates)):
        singleCoordinates[i] = singleCoordinates[i] - 200
    random.shuffle(singleCoordinates)
    return singleCoordinates
    
#main function    
def createLilypad():
    inputname = cmds.textFieldGrp(nameparam, query = True, text = True)
   
    num = cmds.intSliderGrp("num", q = True, v=True)
    spread = cmds.floatSliderGrp("spread", q = True, v = True)
    
    curvename = cmds.ls(selection = True)
    
    for x in range(1, num+1):
        #obj name
        name = inputname + str(x)
        cmds.polyCylinder(sx = 20, sc = 1, n=name)
        cmds.scale(20, 1, 20)
        
        facenums = ['.f[0]', '.f[20]', '.f[40]']
        faces = []
        for face in facenums:
            faces.append(appendName(name, face))
        
        cmds.delete(faces)
        
        cmds.select(name + '.e[78]', name + '.e[58]')
        cmds.polyBridgeEdge(ch=1, divisions=0, twist=0, taper=1, curveType=0, smoothingAngle=30, direction=0, sourceDirection=0, targetDirection=0) 
        cmds.select(name + '.e[79]', name + '.e[59]')
        cmds.polyBridgeEdge(ch=1, divisions=0, twist=0, taper=1, curveType=0, smoothingAngle=30, direction=0, sourceDirection=0, targetDirection=0) 
        
        cmds.select(name)
        cmds.rotate(0, -26.383513, 0, r=True)
        cmds.select(name + '.vtx[40]', name + '.vtx[41]')
        cmds.move(random.uniform(-8.38, 19.1), 0, 0)
        
        startn = 38
        endn = 56
        faces = []
        for i in range(startn, endn + 1, 1):
            faces.append(appendName(name, f'.f[{i}]'))
        
        cmds.polyExtrudeFacet(faces, constructionHistory=1, keepFacesTogether=1, pvx=-5.466307211e-07, pvy=0.5, pvz=-4.263250638e-06, divisions=1, twist=0, taper=1, off=0, thickness=0, smoothingAngle=30, n='polyExtrudeTop' + name)
        cmds.setAttr(f'polyExtrudeTop{x}.localTranslate', 0, 0, 0.868112, type='double3')
        cmds.scale(0.891931, 1, 0.891931, r=True, ocp=True)
        
        startn = 19
        endn = 37
        faces = []
        for i in range(startn, endn + 1, 1):
            faces.append(appendName(name, f'.f[{i}]'))
        
        cmds.polyExtrudeFacet(faces, constructionHistory=1, keepFacesTogether=1, pvx=-1.076369884e-06, pvy=23.2394006, pvz=-3.195326531e-06, divisions=1, twist=0, taper=1, off=0, thickness=0, smoothingAngle=30, n=f'polyExtrudeBottom{x}')
 
        cmds.setAttr(f'polyExtrudeBottom{x}.localTranslate', 0, 0, 1.585827, type='double3')
        cmds.scale(0.89392, 1, 0.89392, r=True, ocp=True)
        
        cmds.select(name + '.f[57]', name + '.f[79]', name + '.f[100]')
        cmds.polyExtrudeFacet(constructionHistory=1, keepFacesTogether=1, pvx=13.57891116, pvy=0, pvz=48.61849756, divisions=1, twist=0, taper=1, off=0, thickness=0, smoothingAngle=30, n=f'polyExtrudeCutRight{x}')

        cmds.setAttr(f'polyExtrudeCutRight{x}.localTranslate', 0, 0, 0.620065, type='double3')
        cmds.scale(0.672788, 0.672788, 0.672788, r=True, ocp=True)
        cmds.move(5.391176, 0, 0, r = True)
