import numpy as np
import matplotlib.pyplot as plt

stress = np.array([0,50,100,151,199,242,268,290,298,302,305,309,315,319,322,323,320,311,293,267,246,223]) #MPa
pstrain = np.array([0,0.069,0.138,0.210,0.280,0.343,0.384,0.438,0.493,0.761,0.992,2.00,3.51,5.02,6.51,7.44,8.48,9.52,10.90,12.51,13.63,14.59])/100 #elongation

elasticmodulus = 72463.7

offset_strain = 0.2 / 100
xlindata = np.linspace(offset_strain, 3.5 * offset_strain, 5)
ylindata = elasticmodulus*(xlindata-offset_strain)




#fig, ax = plt.subplots(figsize=(10, 6))
#
#
#ax.plot(pstrain, stress, marker='o', linestyle='-', color="#000000", markersize=5, linewidth=2, label='Engineering Stress-Strain Curve')
#ax.plot(xlindata, ylindata)
#
#ax.set_title('Engineering Stress vs. Strain', fontsize=16, fontweight='bold', pad=15)
#ax.set_xlabel('Strain (Fractional)', fontsize=14)
#ax.set_ylabel('Stress (MPa)', fontsize=14)
#ax.grid(True, linestyle='--', alpha=0.7)
#ax.legend(loc='lower right', fontsize=12)

tstress = stress*(1+pstrain) #MPa
tstrain = np.log(1+pstrain) #elongation
elasticstrain = tstrain[7]
max_idx = np.argmax(stress)
tstress = tstress[:max_idx+1]
tstrain = tstrain[:max_idx+1]


#fig, trueplot = plt.subplots(figsize=(10, 6))
#
#trueplot.plot(pstrain, stress, marker='o', linestyle='-', color="#000000", markersize=5, linewidth=2, label='Engineering Stress-Strain Curve')
#trueplot.plot(tstrain, tstress, marker='o', linestyle='--', color="#3B48FF", markersize=5, linewidth=2, label='True Stress-Strain Curve')
#
#trueplot.set_title('True Stress vs. Strain', fontsize=16, fontweight='bold', pad=15)
#trueplot.set_xlabel('Strain (Fractional)', fontsize=14)
#trueplot.set_ylabel('Stress (MPa)', fontsize=14)
#trueplot.grid(True, linestyle='--', alpha=0.7)
#trueplot.legend(loc='lower right', fontsize=12)


xplastic = tstrain[7:] - elasticstrain
yplastic = tstress[7:]
k = 415.7
yholloman = k * xplastic ** xplastic[-1]
k_l = 202.19
n_l = 0.478
yludwik = 291.27 + k_l * xplastic ** n_l
print(xplastic[0:])
fig, hollomanplot = plt.subplots(figsize=(10, 6))

hollomanplot.plot(xplastic, yplastic, marker='o', linestyle='-', color="#000000", markersize=5, linewidth=2, label='True Stress-Strain Curve(plastic)')
#hollomanplot.plot(xplastic, yholloman, marker='o', linestyle='--', color="#32FF65", markersize=5, linewidth=2, label='Holloman model')
hollomanplot.plot(xplastic, yludwik, marker='o', linestyle='--', color="#3235FF", markersize=5, linewidth=2, label='Ludwik model')
hollomanplot.set_title('Plastic', fontsize=16, fontweight='bold', pad=15)
hollomanplot.set_xlabel('Strain (Fractional)', fontsize=14)
hollomanplot.set_ylabel('Stress (MPa)', fontsize=14)
hollomanplot.grid(True, linestyle='--', alpha=0.7)
hollomanplot.legend(loc='lower right', fontsize=12)

plt.tight_layout()

plt.show()