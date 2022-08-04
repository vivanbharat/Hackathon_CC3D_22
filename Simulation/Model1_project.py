
from cc3d import CompuCellSetup
        

from Model1_projectSteppables import Model1_projectSteppable

CompuCellSetup.register_steppable(steppable=Model1_projectSteppable(frequency=1))


CompuCellSetup.run()

from Ext_potential_col_motionSteppables import Ext_potential_col_motionSteppable

CompuCellSetup.register_steppable(steppable=Ext_potential_col_motionSteppable(frequency=1))


CompuCellSetup.run()
