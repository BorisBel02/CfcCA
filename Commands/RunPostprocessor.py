import subprocess


class CommandRunPostprocessor:
    def Init(self):
        pass

    def GetResources(self):
        return {"Pixmap": "",
                "Accel": "",
                "MenuText": "Create image",
                "ToolTip": "exports"}

    def Activated(self):
        subprocess.run(['/home/boris/.local/lib/catlib/models/FHP-MP/build/catmdl_fhpmp_post',
                       '/home/boris/nsu/prakt/postprocessorCfdCA.conf'])

    def isActive(self):
        return True