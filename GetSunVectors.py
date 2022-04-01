# Загрузить стандартную библиотеку Python и библиотеку DesignScript
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
# Введенные в этом узле данные сохраняется в виде списка в переменных IN.
dataEnteringNode = IN
Xlist = []
Ylist = []
Zlist = []
SunHeight = []

doc = DocumentManager.Instance.CurrentDBDocument
view = doc.ActiveView
sunSettings = view.SunAndShadowSettings
initialDirection = XYZ.BasisY
altitude = sunSettings.GetFrameAltitude(sunSettings.ActiveFrame)
## Transaction
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
# Разместите код под этой строкой

# Назначьте вывод переменной OUT.
OUT = [Xlist, Ylist, Zlist,SunHeight]