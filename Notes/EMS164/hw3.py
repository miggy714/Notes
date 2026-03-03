import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erf, erfc

T_array = [550, 635, 660, 700, 750]
X_S = [3.5, 3.75, 3, 2, 1.5]
X_L = [1, 17, 14.5, 10.5, 5]
k_array = X_S/X_L

V_array = np.linspace(0,1, 0.001)  # number of time columns



# This block of code is the theoretical solution to Fick's second law
cr = 24 #right concentration
cl = 0 #left concentration
diffusivity_gallium = 0.125
t = 5.0*60.0*60.0 # 5 hours
theoretical_concentration = (cl+cr)/2 +(cr-cl)/2*erf(xdata/(2*(diffusivity_gallium*t)**(1/2)))



#construct arrays for x and y axes to be used for the plots
dt = 1 # dt in seconds
data_timestep1 = arrayfromfile[:,0]
data_timestep2 = arrayfromfile[:,1]
data_timestep3 = arrayfromfile[:,2]

data2_timestep1 = arrayfromfile2[:,0]
data2_timestep2 = arrayfromfile2[:,1]
data2_timestep3 = arrayfromfile2[:,2]

error_mat = (data_timestep3 - theoretical_concentration)/ theoretical_concentration * 100
error_mat2 = (data2_timestep3 - theoretical_concentration)/ theoretical_concentration * 100
#now we can plot all data
fig, ax = plt.subplots(3,1, figsize = (10,14))
ax[0].plot(xdata, theoretical_concentration, 'g-', label = 't = 5 hrs')   
ax[0].legend()
ax[0].set_xlabel('position[microns]')
ax[0].set_ylabel('Concentration[at. %]')
ax[0].set_title('Ga Concentration: Fe/Fe-24Ga theoretical')

ax[1].plot(xdata, data2_timestep1,'r--',label = 't=0')          
ax[1].plot(xdata, data2_timestep2,'b--', label = 't = 2.5 hrs')
ax[1].plot(xdata, data2_timestep3,'g-', label = 't = 5 hrs')   
ax[1].legend()
ax[1].set_xlabel('position[microns]')
ax[1].set_ylabel('Concentration[at. %]')
ax[1].set_title('Ga Concentration: Fe/Fe-24Ga with boundary conditions enforced')

ax[2].plot(xdata, np.abs(error_mat), 'b-', label = "with BC")
ax[2].set_xlabel('position[microns]')
ax[2].set_ylabel('Percent error')
ax[2].set_title('Error of bounded and unbounded concentration profile at 5 hours')
ax[2].legend()

plt.show()