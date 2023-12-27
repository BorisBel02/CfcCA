import subprocess


class CellTransmitter:
    proc = None

    def __init__(self):
        self.proc = subprocess.Popen(["/home/boris/.local/lib/catlib/models/fhp_mp/build/writer"], stdin=subprocess.PIPE)

    def TransmitInt(self, i):
        print('transmit int\n')
        self.proc.stdin.write(i.to_bytes(4, byteorder="little"))

    def TransmitCell(self, cellType, s0, s1, s2, s3, s4, s5):
        self.proc.stdin.write(cellType.to_bytes(4, byteorder="little"))
        self.proc.stdin.write(s0.to_bytes(4, byteorder="little"))
        self.proc.stdin.write(s1.to_bytes(4, byteorder="little"))
        self.proc.stdin.write(s2.to_bytes(4, byteorder="little"))
        self.proc.stdin.write(s3.to_bytes(4, byteorder="little"))
        self.proc.stdin.write(s4.to_bytes(4, byteorder="little"))
        self.proc.stdin.write(s5.to_bytes(4, byteorder="little"))

    def finish(self):
        self.proc.wait()
