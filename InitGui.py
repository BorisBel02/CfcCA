class CfdCAWorkbench(Workbench):
    MenuText = "CfdCA Workbench"
    Tooltip = "Cfd on Cellular Automata using catlib"
    Icon = ""

    def Initialize(self):
        """add functions of the Workbench"""
        from Commands.ExportCTL import CommandExportToCTL
        from Commands.RunSimulation import CommandRunSimulation
        from Commands.RunPostprocessor import CommandRunPostprocessor

        FreeCADGui.addCommand('ExportToCTL', CommandExportToCTL())
        FreeCADGui.addCommand('RunSimulation', CommandRunSimulation())
        FreeCADGui.addCommand('RunPostprocessor', CommandRunPostprocessor())


        self.list = ["ExportToCTL", "RunSimulation", "RunPostprocessor"]
        self.appendMenu("Commands", self.list)


    def Activated(self):
        print("CfdCA activated! :)")
        return

    def Deactivated(self):
        print("CfdCA deactivated! :(")
        return

    def ContextMenu(self, recipient):
        self.appendContextMenu("commands", self.list)

    def GetClassName(self):
        return "Gui::PythonWorkbench"


Gui.addWorkbench(CfdCAWorkbench())
