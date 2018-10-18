"Melting a copper cluster."

from numpy import *
from asap3 import Atoms, EMT, units
from asap3.analysis import PTMobserver
from ase.visualize.primiplotter import *
from ase.lattice.cubic import FaceCenteredCubic
from asap3.md.langevin import Langevin

# Color coding for PTM analysis
mycolors = {0: (0.3, 0.3, 1.0),  # Unknown is blue
            1: (0.2, 1.0, 0.2),  # SC is green
            2: (1.0, 1.0, 1.0),  # FCC is white
            3: (1.0, 0.0, 0.0),  # HCP is red
            4: (1.0, 1.0, 0.0),  # ICO is yellow
            5: (0.0, 0.0, 0.0)   # BCC is black
            }

# Create the atoms
atoms = FaceCenteredCubic(size=(6,6,6), symbol="Cu", pbc=False)

# Associate the EMT potential with the atoms
atoms.set_calculator(EMT())

# Temperature profile - brief run at 1750, then lower temperature gradually
t = linspace(1500, 250, 81)
temperatures = 1500 * ones(100)
temperatures[-len(t):] = t
print temperatures

# How many steps at each temperature
nsteps_total = 100000
nsteps = nsteps_total // len(temperatures)

# Interval between plots
plotinterval = 2000

# Make the Langevin dynamics module
dyn = Langevin(atoms, 5*units.fs, units.kB*temperatures[0], 0.002)

# The PTM analyser is called every plotinterval timesteps.
ptm = PTMobserver(atoms, rmsd_max=0.16)
dyn.attach(ptm.analyze, interval=plotinterval)

# The plotter
def invisible_atoms(a):
    """Return True for atoms that should be invisible."""
    r = atoms.get_positions()
    centerofmass = r.sum(axis=0) / len(atoms)
    return (r[:,2] < centerofmass[2])

plotter = PrimiPlotter(atoms)
plotter.set_invisibility_function(invisible_atoms)
plotter.set_colors(mycolors) # Map tags to colors
# plotter.set_output(X11Window())   # Plot in a window on the screen
plotter.set_output(JpegFile("ptm"))  # Save plots in files plt0000.gif ...
plotter.set_rotation((10.0, 5.0, 0))

# Attach the plotter to the PTMobserver object.  That guarantees
# that the plotter is called AFTER the PTM analysis has been done.
# Similarly, a Trajectory should be attached to the PTMobserver
# object.  By using interval=1 (the default), the plotter is called
# every time PTMobserver is called, i.e. every plotinterval
# timesteps.
ptm.attach(plotter.plot)

# The main loop
for t in temperatures:
    dyn.set_temperature(units.kB*t)
    for i in range(nsteps/100):
        dyn.run(100)
        print "E_total = %-10.5f  T = %.0f K  (goal: %.0f K, step %d of %d)" %\
              (atoms.get_total_energy()/len(atoms), atoms.get_temperature(), t, i, nsteps/100)
        
