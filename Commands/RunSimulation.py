import subprocess


class CommandRunSimulation:
    def Init(self):
        pass

    def GetResources(self):
        return {"Pixmap": "",
                "Accel": "",
                "MenuText": "Run Simulation",
                "ToolTip": "exports"}

    def Activated(self):
        proc = subprocess.run(['/home/boris/.local/lib/catlib/models/FHP-MP/build/catmdl_fhpmp_sim',
                       '/home/boris/nsu/prakt/ca_file.dat', '/home/boris/nsu/prakt/ca_file_out.dat',
                       '100'])

    def isActive(self):
        return True