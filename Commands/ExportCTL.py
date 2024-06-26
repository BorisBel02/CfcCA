import math

import FreeCAD
import FreeCADGui
from PySide2 import QtGui, QtCore
import Part
from array import *
from threading import Thread

from Commands import cell_transmitter

sqrt3 = 1.732050807568877

CELL_TYPE_SPACE = 0
CELL_TYPE_INLET = 1
CELL_TYPE_OUTLET = 2
CELL_TYPE_WALL = 15


def getCAPressureFromString(s):
    P = float(str(s).split(maxsplit=1)[0]) * 1000
    particlesQty = int(P / 1000)
    return particlesQty


def StartExport(cell_radius):
    print("Export started\n")

    accuracy = 0.001
    cell_diameter = cell_radius * 2
    y_offset = sqrt3 * cell_radius
    boundary_conditions = []

    for obj in FreeCAD.ActiveDocument.Objects:
        if 'BoundaryType' in obj.PropertiesList:
            boundary_conditions.append(obj)
            print(obj.BoundaryType)

    sel = FreeCADGui.Selection.getSelection()

    if len(sel) != 1:
        print("select one item")
        return

    root_object = sel[0]

    root_object_faces = root_object.Shape.Faces
    print(root_object_faces)

    working_area = root_object.Shape.BoundBox
    Zmin = working_area.ZMin
    Ymin = working_area.YMin
    Xmin = working_area.XMin
    Zmax = working_area.ZMax
    Ymax = working_area.YMax
    Xmax = working_area.XMax

    log = open('/home/boris/nsu/prakt/ca_log.txt', 'w+')
    Probe_Sphere = Part.makeSphere(cell_radius)

    transmitter = cell_transmitter.CellTransmitter()
    print('X length = ' + str(Xmax - Xmin) + ' Y length = ' + str(Ymax - Ymin) + '\n')

    I = int((Xmax - Xmin) / (sqrt3 * cell_radius)) + 1
    J = int((Ymax - Ymin) / cell_diameter) + 2
    print('I = ', I)
    print('J = ', J)

    transmitter.TransmitFloat(Xmax - Xmin)
    transmitter.TransmitFloat(Ymax - Ymin)
    transmitter.TransmitFloat(1 / cell_diameter)

    transmitter.TransmitInt(I)
    transmitter.TransmitInt(J)

    log.write('Zmax = ' + str(Zmax) + ' Ymax = ' + str(Ymax) + ' Xmax = ' + str(Xmax)
              + '\nZmin = ' + str(Zmin) + ' Ymin = ' + str(Ymin) + ' Zmin = ' + str(Zmin) + '\n')
    print(boundary_conditions, flush=True)

    cells_counter = 0
    try:
        Z = (Zmax - Zmin) / 2
        while Z < (Zmax - Zmin) / 2 + cell_radius:
            i = 0
            Y = Ymin + cell_radius
            while i < I:
                j = 0
                X = Xmin + (cell_radius * (i % 2))
                log.write('\n')
                while j < J:
                    Probe_Sphere.Placement.Base = FreeCAD.Vector(X, Y, Z)
                    cell_type = CELL_TYPE_SPACE
                    s = array('l', [3, 3, 3, 3, 3, 3])
                    for boundary in boundary_conditions:
                        dist = Probe_Sphere.distToShape(boundary.Shape)[0]
                        if math.fabs(dist) < accuracy:
                            if boundary.BoundaryType == "inlet":
                                cell_type = CELL_TYPE_INLET
                                P = getCAPressureFromString(boundary.Pressure)
                                print("inlet pressure = " + str(P) + '\n')
                                s = array('l', [P, P, P, P, P, P])
                                log.write('i')
                                break
                            elif boundary.BoundaryType == "outlet":
                                cell_type = CELL_TYPE_OUTLET  # outlet type
                                P = getCAPressureFromString(boundary.Pressure)
                                print("outlet pressure = " + str(P) + '\n')
                                s = array('l', [P, P, P, P, P, P])
                                log.write('o')
                                break
                            elif boundary.BoundaryType == "wall" or math.fabs(
                                    Probe_Sphere.distToShape(root_object.Shape)) < accuracy:
                                cell_type = CELL_TYPE_WALL  # wall type
                                log.write('*')
                                break

                    if cell_type == 0:
                        log.write(' ')
                        # for i in range(0, 6):
                        # cell.s[i] = 10 error in this line, [i] indexing doesnt work like this
                    transmitter.TransmitCell(cell_type, s[0], s[1], s[2], s[3], s[4], s[5])
                    transmitter.TransmitInt(i)
                    transmitter.TransmitInt(j)
                    cells_counter += 1
                    X += cell_diameter
                    j += 1
                Y += y_offset
                i += 1
            Z += cell_diameter
        transmitter.TransmitInt(10)
        print('cells qty = ' + str(cells_counter) + '\n', flush=True)
        retcode = transmitter.finish()
        # print('writer ret code = ' + retcode + '\n', flush=True)

    except Exception as e:
        print(e)

    finally:
        log.close()
        FreeCADGui.Selection.clearSelection()
        print('Finished\n')


class CommandExportToCTL:
    def Init(self):
        pass

    def Activated(self):
        StartExport(0.025)
        #self.form = FreeCADGui.PySideUic.loadUi(
         #   "/home/boris/.local/share/FreeCAD/Mod/CfdCA/gui/panels/CA_Parameters_Panel.ui")
        #self.form.coord.addItem('Z')  # addItems(['X', 'Y', 'Z']) now i calculate I and J from X and Y
        #self.cellRadius = 0.1
        #FreeCADGui.Control.showDialog(self.form)

    def GetResources(self):
        return {"Pixmap": "",
                "Accel": "",
                "MenuText": "Export to ctl",
                "ToolTip": "exports"}

    def accept(self):
        self.cellRadius = self.form.cellRadius.value()
        #FreeCADGui.Control.closeDialog()

        thread = Thread(target=StartExport, args=(self.cellRadius,))
        thread.daemon = True
        thread.start()

    #def reject(self):
        #FreeCADGui.Control.closeDialog()

    def IsActive(self):
        return True
