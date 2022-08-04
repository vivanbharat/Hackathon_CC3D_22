
from cc3d.core.PySteppables import *
import numpy as np
from numpy import random as rng


class Model1_projectSteppable(SteppableBasePy):

    def __init__(self, frequency=1):

        SteppableBasePy.__init__(self,frequency)

    def start(self):
        """
        Called before MCS=0 while building the initial simulation
        """
        # for cell in self.cell_list:

            # cell.targetVolume = 25
            # cell.lambdaVolume = 3.0
            # cell.targetSurface = 20.0
            # cell.lambdaSurface = 2.0
            
        # self.build_wall(self.WALL)
        # iterating over cells of type 1
        # list of  cell types (capitalized)
        for cell in self.cell_list:
            # you can access/manipulate cell properties here
            #print ("id=", cell.id, " type=", cell.type)
            # cell.targetVolume = 68
            # cell.lambdaVolume = 8.0
            theta = rng.uniform(0, 2*np.pi)
            bias = np.array((np.cos(theta), np.sin(theta), 0)) # because dealing with numpy arrays is much more easier
            cell.dict['bias'] = bias
            cell.dict['angle'] = theta
            

            cell.lambdaVecX = -100 * cell.dict['bias'][0]  # force component pointing along X axis - towards positive X's
            cell.lambdaVecY = -100 * cell.dict['bias'][1]  # force component pointing along Y axis - towards negative Y's
            cell.lambdaVecZ = 0.0  # force component pointing along Z axis
        
        
            
            # self.plot_win = self.add_new_plot_window(title='Av vol Non_sen',
                                                     # x_axis_title='MonteCarlo Step (MCS)',
                                                     # y_axis_title='Variables', 
                                                     # x_scale_type='linear', 
                                                     # y_scale_type='linear',
                                                     # grid=False)
            
            # self.plot_win.add_plot("vol", style='Lines', color='red', size=2)
            # self.plot_win.add_plot("Ypos", style='Lines', color='cyan', size=2)
            # self.plot_win.add_plot("Zpos", style='Lines', color='yellow', size=2)
        
    

    def step(self, mcs):
        """
        Called every frequency MCS while executing the simulation
        
        :param mcs: current Monte Carlo step
        """
        # for cell in self.cell_list:
            # cell.targetSurface = 2*(3.14159*cell.targetVolume)**0.5
            # cell.targetVolume += 25/500 
        
                   
        alpha = 0.25
        # iterating over cells of type 1
        # list of  cell types (capitalized)
        for cell in self.cell_list:
            # you can access/manipulate cell properties here
            #print ("id=", cell.id, " type=", cell.type)
            
            # Make sure CenterOfMass plugin is loaded
            # READ ONLY ACCESS
            xCOM = cell.xCOM
            yCOM = cell.yCOM
            zCOM = cell.zCOM
                  
            # arguments are (name of the data series, x, y)
            # self.plot_win.add_data_point("Ypos", mcs, yCOM)
            # self.plot_win.add_data_point("Zpos", mcs, zCOM)
            # access/modification of a dictionary attached to cell - make sure to declare in main script that
            # you will use such attribute
            cell.dict['velocity'] = np.array((cell.xCOM - cell.xCOMPrev, cell.yCOM - cell.yCOMPrev, 0))
            
            v_norm = cell.dict['velocity'][:] / np.linalg.norm(cell.dict['velocity'])
            
            cell.dict['bias'][:] = alpha * cell.dict['bias'][:] + (1 - alpha) * v_norm[:]
            
            cell.lambdaVecX = -100 * cell.dict['bias'][0]  # force component pointing along X axis - towards positive X's
            cell.lambdaVecY = -100 * cell.dict['bias'][1]  # force component pointing along Y axis - towards negative Y's
            cell.lambdaVecZ = 0.0  # force component pointing along Z axis
            
        
        # Av_volume = 0
        # L = self.cell_list_by_type(self.NON_SEN)
        for cell in self.cell_list_by_type(self.NON_SEN):
            cell.targetVolume += 5
            # Av_volume += cell.volume
            
        # Av_volume = Av_volume/L   
        # self.plot_win.add_data_point("vol", mcs, Av_volume)

    def finish(self):
        """
        Called after the last MCS to wrap up the simulation
        """

    def on_stop(self):
        """
        Called if the simulation is stopped before the last MCS
        """
