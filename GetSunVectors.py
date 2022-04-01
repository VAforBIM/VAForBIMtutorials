# Getting everything imported into Python
import sys
import clr
import math
clr.AddReference('ProtoGeometry')
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.Attributes import *
from Autodesk.DesignScript.Geometry import *
import Autodesk.Revit.DB
import Autodesk.Revit.UI
import Autodesk.Revit.Attributes
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
# The = IN is the input of this node
dataEnteringNode = IN
Xlist = []
Ylist = []
Zlist = []
SunHeight = []
#getting the document from the document manager
doc = DocumentManager.Instance.CurrentDBDocument
#Getting the active view
view = doc.ActiveView
#Getting the Sunsettings from the current view, currently displayed in Revit
sunSettings = view.SunAndShadowSettings
initialDirection = XYZ.BasisY
altitude = sunSettings.GetFrameAltitude(sunSettings.ActiveFrame)
## Starting a transaction
TransactionManager.Instance.EnsureInTransaction(doc)
for i in range (1, int(sunSettings.NumberOfFrames +1)):
	sunSettings.ActiveFrame = i
	altitudeRotation = Transform.CreateRotation(XYZ.BasisX, altitude)
	altitudeDirection = altitudeRotation.OfVector(initialDirection)
	azimuth = sunSettings.GetFrameAzimuth(sunSettings.ActiveFrame)
	actualAzimuth = 2 * math.pi - azimuth
	azimuthRotation = Transform.CreateRotation(XYZ.BasisZ, actualAzimuth)
	sunDirection = azimuthRotation.OfVector(altitudeDirection)
	Xlist.append(sunDirection.X*100)
	Ylist.append(sunDirection.Y*100)
	Zlist.append(sunDirection.Z*100)
	SunHeight.append(math.degrees(sunSettings.GetFrameAltitude(sunSettings.ActiveFrame)))
TransactionManager.Instance.TransactionTaskDone()
# Althought we may not use the Zlist but it's a good idea to get it anyway.
OUT = [Xlist, Ylist, Zlist,SunHeight]