from iocbuilder import Device, AutoSubstitution
from iocbuilder.arginfo import *
from iocbuilder.modules.asyn import Asyn, AsynPort
from iocbuilder.modules.sscan import Sscan
from iocbuilder.modules.std import Std, scaler32
from iocbuilder.modules.seq import Seq
from iocbuilder.modules.calc import Calc

class Mca(Device):
    LibFileList = ['mca']
    DbdFileList = ['mcaSupport']
    AutoInstantiate = True

class SIS38XX_template(AutoSubstitution):
    """Template for supporting SIS38XX seq program"""
    TemplateFile = "SIS38XX.template"

class simple_mca_template(AutoSubstitution):
    """Just contains a single mca record"""
    Dependencies = (Mca,)    
    TemplateFile = "simple_mca.db"

class mca_template(AutoSubstitution):
    """mca record and associated records for doing acquisition"""
    Dependencies = (Calc,Mca)
    TemplateFile = "mca.db"

class sis3820(AsynPort):
    """Startup script to setup an sis3820 scaler"""
    Dependencies = (Asyn, Sscan, Std, Mca, Seq)
    LibFileList=["SIS38XX"]
    DbdFileList=["SIS38XXSupport"]
    
    def __init__(self, name, P, S, M, nchans, nsignals, baseAddress="0x05000000", 
            intLevel=6):
        self.__dict__.update(locals())        
        scaler32(P = P, S = S, DTYP = "Asyn Scaler", FREQ = 50000000, 
            OUT = "@asyn(%s)" % name, gda_name = name, gda_desc = "Scaler Card")        
        SIS38XX_template(P = P + M + ":", edmMacros = "P=%s\,M=%s:\,S=%s"%(P,M,S), 
            PORT = name, SCALER = P + S, name = name, gda_name = name + ".MCS", 
            gda_desc = "Scaler MCS")       
        for i in range(nsignals):
             simple_mca_template(P=P, M=M+":mca%d"%(i+1), DTYP="asynMCA", 
                 CHANS=nchans, PREC=3, INP="@asyn(%s %d)"%(name, i), 
                 gda_name = name + ".MCS", S = i + 1)
        self.vector = self.AllocateIntVector()        
        self.__super.__init__(name)
        
    def Initialise(self):
        print '#drvSIS3820Config(Port name, baseAddress, interruptVector, ' \
            'interruptLevel, channels, signals, use DMA?, fifoBufferWords)'
        print 'drvSIS3820Config("%(asyn_name)s", %(baseAddress)s, %(vector)d, '\
            '%(intLevel)d, %(nchans)d, %(nsignals)d, 0, 0x200000)'%self.__dict__

    def PostIocInitialise(self):
        print 'seq(&SIS38XX_SNL, "P=%(P)s%(M)s:, R=mca, NUM_SIGNALS=%(nsignals)d, FIELD=READ")' % self.__dict__


    ArgInfo = makeArgInfo(__init__,
        name = Simple("Asyn port name"),
        P = Simple("Device prefix"),
        S = Simple("Suffix for scaler card"),
        M = Simple("Suffix for SNL records"),        
        nchans = Simple("Number of channels (bins for mcs mode)", int),
        nsignals = Simple("Number of signals (normally 32)", int),
        intLevel = Simple("Interrupt level", int),                
        baseAddress = Simple("Base Address in hex"))


