import math
import FreeCAD
import FreeCADGui
import Part
import ctypes
import time
import cell_transmitter
from array import *


class CommandExportToCTL:
    def Init(self):
        pass

    def GetResources(self):
        return {"Pixmap": "",
                "Accel": "",
                "MenuText": "Export to ctl",
                "ToolTip": "exports"}

    def Activated(self):
        print("Export started\n")

        accuracy = 0.00001
        cell_radius = 0.1
        cell_diameter = cell_radius * 2
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

        cellsPerMeter = int((1 / (cell_diameter / 100)))
        print('cell per meter = ' + str(cellsPerMeter) + '\n')
        I = int((Xmax - Xmin) / cell_diameter)
        J = int((Ymax - Ymin) / cell_diameter)
        print('I = ', I)
        transmitter.TransmitInt(cellsPerMeter)
        transmitter.TransmitInt(I)
        transmitter.TransmitInt(J)

        log.write('Zmax = ' + str(Zmax) + ' Ymax = ' + str(Ymax) + ' Xmax = ' + str(Xmax)
                  + '\nZmin = ' + str(Zmin) + ' Ymin = ' + str(Ymin) + ' Zmin = ' + str(Zmin) + '\n')
        print(boundary_conditions, flush=True)
        cells_counter = 0
        try:
            Z = (Zmax - Zmin) / 5
            while Z < (Zmax - Zmin) / 5 + cell_radius:
                Y = Ymin + cell_radius
                while Y < Ymax:
                    X = Xmin + cell_radius
                    while X < Xmax:
                        Probe_Sphere.Placement.Base = FreeCAD.Vector(X, Y, Z)
                        cell_type = 0
                        s = array('l', [10, 10, 10, 10, 10, 10])
                        for boundary in boundary_conditions:
                            dist = Probe_Sphere.distToShape(boundary.Shape)[0]
                            if math.fabs(dist) < accuracy:
                                if boundary.BoundaryType == "inlet":
                                    cell_type = 1
                                    s = array('l', [0, 20, 0, 0, 0, 0])
                                    break
                                elif boundary.BoundaryType == "outlet":
                                    cell_type = 2 # outlet type
                                    s = array('l', [0, 0, 0, 0, 0, 0])
                                    break
                                elif boundary.BoundaryType == "wall" or math.fabs(Probe_Sphere.distToShape(root_object.Shape)) < accuracy:
                                    cell_type = 3 # wall type
                                    s = array('l', [0, 0, 0, 0, 0, 0])
                                    break

                        #if cell_type == 0:
                            # for i in range(0, 6):
                                # cell.s[i] = 10 error in this line, [i] indexing doesnt work like this
                        transmitter.TransmitCell(cell_type, s[0], s[1], s[2], s[3], s[4], s[5])
                        cells_counter += 1
                        X += cell_diameter
                    Y += cell_diameter
                Z += cell_diameter
            transmitter.TransmitInt(10)
            print('cells qty = ' + str(cells_counter) + '\n', flush=True)
            # retcode = transmitter.finish()
            # print('writer ret code = ' + retcode + '\n', flush=True)

        except Exception as e:
            print(e)

        finally:
            log.close()
            FreeCADGui.Selection.clearSelection()
            print('Finished\n')

    def IsActive(self):
        return True