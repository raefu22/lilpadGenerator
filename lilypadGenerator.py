import maya.cmds as cmds
import random

def showScatter(*args):
    showCheckbox = cmds.checkBoxGrp(useCurve, q = True)
    cmds.floatSliderGrp(locationScatter, edit=True, enable=True)
   
def hideScatter(*args):
    showCheckbox = cmds.checkBoxGrp(useCurve, q = True, vis = False, v1 = False)
    cmds.floatSliderGrp(locationScatter, edit=True, enable=False)
    
def showCurve(*args):
    showCheckbox = cmds.checkBoxGrp(useCurve, q = True)
    cmds.floatSliderGrp(locationScatter, edit=True, enable=True)
    cmds.checkBoxGrp(useCurve, edit=True, enable=False)
   
def hideCurve(*args):
    showCheckbox = cmds.checkBoxGrp(useCurve, q = True, vis = False, v1 = False)
    cmds.floatSliderGrp(locationScatter, edit=True, enable=False)
    cmds.checkBoxGrp(useCurve, edit=True, enable=True)
#UI
window = cmds.window(title='Lily Pad Generator', menuBar = True, width=250)
container = cmds.columnLayout()
cols = cmds.rowLayout(numberOfColumns=3, p=container)

leftmar = cmds.columnLayout(p=cols)
cmds.text('       ', p =leftmar)

maincol = cmds.columnLayout('Block', p=cols)
cmds.text('            ')

cmds.separator(height = 10)
nameparam = cmds.textFieldGrp(label = 'Name ')
cmds.separator(height = 10)
cmds.intSliderGrp("num", label="Number of Lily Pads ", field = True, min = 1, max = 40, v = 15)
cmds.separator(height = 10)
cmds.intSliderGrp("size", label="Average Size ", field = True, min = 0.5, max = 15, v = 1)
cmds.floatSliderGrp("sizestd", label="Size Standard Deviation ", field = True, min = 0.01, max = 5, v = 0.25)
cmds.separator(height = 10)
curveInstructions = cmds.text('                Select an EP Curve or Bezier Curve to place the lilypads along?')
cmds.separator(height = 5)
useCurve = cmds.checkBoxGrp('useCurve', numberOfCheckBoxes=1, label='Use Curve ', v1=False, onc = hideScatter, ofc = showScatter)
scatter = cmds.checkBoxGrp('scatter', numberOfCheckBoxes=1, label='Scatter ', v1=False, onc = showCurve, ofc = hideCurve)
locationScatter = cmds.floatSliderGrp("spread", label="Location Scatter ", field = True, min = 1, max = 50, v = 20)
cmds.floatSliderGrp(locationScatter, edit=True, enable=False)
cmds.separator(height = 10)
submitrow = cmds.rowLayout(numberOfColumns=2, p=maincol)
cmds.text(label='                                                                                                    ')
cmds.button(label="Create Lily Pad(s)", c="createLilypad()", p = submitrow)

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
        if (len(numlist) == (size - 1)):
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
    size = cmds.intSliderGrp("size", q = True, v=True)
    sizestd = cmds.floatSliderGrp("sizestd", q = True, v=True)
    sizeList = normalDistrib(size, sizestd, num)  
    spread = cmds.floatSliderGrp("spread", q = True, v = True)
    useCurve = cmds.checkBoxGrp("useCurve", q = True, v1=True)
    scatter = cmds.checkBoxGrp("scatter", q = True, v1=True)
    
    if useCurve:
        curvename = cmds.ls(selection = True)
    else:
        xCoordinates = randomLocation(num, spread)
        zCoordinates = randomLocation(num, spread)

    
    for x in range(1, num+1):
        #obj name
        name = inputname + str(x)
        cmds.polyCylinder(sx = 20, sc = 1, n=name)
        cmds.scale(20, 0.6, 20)
        
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
        cmds.move(random.uniform(-8.38, 12), 0, 0)
        
        startn = 38
        endn = 56
        faces = []
        for i in range(startn, endn + 1, 1):
            faces.append(appendName(name, f'.f[{i}]'))
        
        node = cmds.polyExtrudeFacet(faces, constructionHistory=1, keepFacesTogether=1, pvx=-5.466307211e-07, pvy=0.5, pvz=-4.263250638e-06, divisions=1, twist=0, taper=1, off=0, thickness=0, smoothingAngle=30, n='polyExtrudeTop' + name)
        cmds.rename(node, f'polyExtrudeTop{x}')
  
        cmds.setAttr(f'polyExtrudeTop{x}.localTranslate', 0, 0, 0.5, type='double3')
        cmds.scale(0.891931, 1, 0.891931, r=True, ocp=True)
        
        startn = 19
        endn = 37
        faces = []
        for i in range(startn, endn + 1, 1):
            faces.append(appendName(name, f'.f[{i}]'))
        
        node = cmds.polyExtrudeFacet(faces, constructionHistory=1, keepFacesTogether=1, pvx=-1.076369884e-06, pvy=23.2394006, pvz=-3.195326531e-06, divisions=1, twist=0, taper=1, off=0, thickness=0, smoothingAngle=30, n=f'polyExtrudeBottom{x}')
        
        cmds.rename(node, f'polyExtrudeBottom{x}')
  
        cmds.setAttr(f'polyExtrudeBottom{x}.localTranslate', 0, 0, 0.4, type='double3')
        cmds.scale(0.89392, 1, 0.89392, r=True, ocp=True)
        
        cmds.select(name + '.f[57]', name + '.f[79]', name + '.f[100]')
        node = cmds.polyExtrudeFacet(constructionHistory=1, keepFacesTogether=1, pvx=13.57891116, pvy=0, pvz=48.61849756, divisions=1, twist=0, taper=1, off=0, thickness=0, smoothingAngle=30, n=f'polyExtrudeCutRight{x}')
        cmds.rename(node, f'polyExtrudeCutRight{x}')
        cmds.setAttr(f'polyExtrudeCutRight{x}.localTranslate', 0, 0, 0.3, type='double3')
        cmds.scale(0.672788, 0.672788, 0.672788, r=True, ocp=True)
        cmds.move(3.391176, 0, 0, r = True)
        cmds.select(name + '.f[58]', name + '.f[60]', name + '.f[81]')
        node = cmds.polyExtrudeFacet(constructionHistory=1, keepFacesTogether=1, pvx=8.24462092, pvy=22.98021709, pvz=-1.670525561, divisions=1, twist=0, taper=1, off=0, thickness=0, smoothingAngle=0)
        cmds.rename(node, f'polyExtrudeCutLeft{x}')
        cmds.setAttr(f'polyExtrudeCutLeft{x}.localTranslate', 0, 0, 0.3, type='double3')
        cmds.setAttr(f'polyExtrudeCutLeft{x}.localScale', 0.626892, 1, 1, type='double3')
        cmds.move(3.012829, 0, 0, r=True)
        cmds.move(0, 0, -0.736701, r=True)
        cmds.scale(0.851077, 1, 1, p=(11.404541, 23.022894, -1.634293))
        cmds.rotate(0, -4.675311, 0, p=(11.40517, 23.022894, -1.639525), r=True, os=True, fo=True)
        
        #randomize shape 
        repeatk = random.randint(1,16) 
        already = []
        for k in range(repeatk):
            randnum = random.randint(2, 19)
            if (randnum not in already):
                already.append(randnum)
                cmds.select(f'{name}.vtx[{randnum}]', f'{name}.vtx[{randnum + 20}]', f'{name}.vtx[{randnum + 22}]', f'{name}.vtx[{randnum + 21}]')
                cmds.select(name + '.vtx[40]', name + '.vtx[41]', d=True)
                cmds.move(0, random.uniform(-2.2, 4.5), 0, r=True)
        
        #scale
        cmds.select(name)
        cmds.scale(sizeList[x-1], 1, sizeList[x-1], r=True)
        
        #UVs
        cmds.polyAutoProjection(name + '.f[0:116]', lm=0, pb=0, ibd=1, cm=0, l=2, sc=1, o=1, p=6, ps=0.2, ws=0)
        cmds.u3dUnfold(name + '.f[0:116]', ite=1, p=0, bi=1, tf=1, ms=1024, rs=0)
        cmds.u3dLayout(name + '.f[0:116]', res=256, scl=1, box=[0, 1, 0, 1])

        #location
        cmds.select(name)
        if useCurve:
            position = locations(curvename, (x-0.0)/num)
            cmds.move(position[0], position[1], position[2], relative = True)
        elif scatter:
            cmds.move(xCoordinates[x-1], 0, zCoordinates[x-1], relative = True)
            print(xCoordinates[x-1])
           
        cmds.rotate(0, random.uniform(0, 360), 0, r=True)
        
        #smooth and clear history
        cmds.select(name)
        cmds.polySmooth(mth=0, sdt=2, ovb=1, ofb=3, ofc=0, ost=0, ocr=0, dv=2, bnr=1, c=1, kb=1, ksb=1, khe=0, kt=1, kmb=1, suv=1, peh=0, sl=1, dpe=1, ps=0.1, ro=1, ch=1)
        cmds.u3dUnfold(name, ite=1, p=0, bi=1, tf=1, ms=1024, rs=0)
        cmds.delete(name, constructionHistory = True)
        cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0, pn=1)
