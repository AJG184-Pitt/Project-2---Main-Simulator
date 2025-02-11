import numpy as np
from bus import Bus
from conductor import Conductor
from geometry import Geometry
from bundle import Bundle

class TransmissionLine:

    def __init__(self, name: str, bus1: Bus, bus2: Bus, bundle: Bundle, conductor: Conductor, geometry: Geometry, length: float):
        self.name = name
        self.bus1 = bus1
        self.bus2 = bus2
        self.bundle = bundle
        self.conductor = conductor
        self.geometry = geometry
        self.length = length
        self.rseries, self.xseries = float
        self.f = 60
        self.yseries, self.zseries = self.calc_series()
<<<<<<< Updated upstream
        self.bshunt = self.calc_admitance()

=======
        self.bshunt = self.calc_admittance()
>>>>>>> Stashed changes

    def calc_series(self):
        self.rseries = self.conductor.resistance/self.bundle.num_conductors
        self.xseries = (2 * np.pi * self.f) * (2 * 10 ** -7) * np.log(self.geometry.Deq/self.bundle.DSL) * 1609.34
        self.yseries = 1 / (self.rseries + (1j * self.xseries))
        self.zseries = self.rseries + self.xseries
        return self.yseries, self.zseries

<<<<<<< Updated upstream
    def calc_admitance(self):
        self.bshunt = (2 * np.pi * self.f) * ((2 * np.pi * 8.854 * 10 ** -12) / (np.log(self.geometry.Deq / self.bundle.DSC))) * 1609.34
        return self.bshunt
=======
    def calc_admittance(self):
        return (2 * np.pi * self.f) * ((2 * np.pi * 8.854 * 10 ** -12)/(np.log(self.geometry.Deq/self.bundle.DSC))) * 1609.34
>>>>>>> Stashed changes
