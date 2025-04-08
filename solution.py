from bus import Bus
from circuit import Circuit
from settings import s
from load import Load
import numpy as np
import pandas as pd

class Solution:

    def __init__(self, name: str, bus: Bus, circuit: Circuit, load: Load):
        self.name = name
        self.bus = bus
        self.circuit = circuit
        self.load = load
        self.delta = dict()
        self.voltage = dict()
        self.P = self.calc_Px()
        self.Q = self.calc_Qx()
        self.x = self.initialize_x()
        self.y = self.initialize_y()
        self.mismatch = self.calc_mismatch()

    #power injection
    def start(self):
        self.delta = {bus: 0 for bus in self.bus.index}
        self.voltages = {bus: 1 for bus in self.bus.index}


    def calc_Px(self):
        Px = {bus: 0 for bus in self.bus.index}

        for k, bus_k in enumerate(self.bus.index):
            V_k = self.voltage[bus_k]
            delta_k = self.delta[bus_k]
            P_k = 0
            for j, bus_j in enumerate(self.bus.index):
                V_j = self.voltage[bus_j]
                delta_j = self.delta[bus_j]
                Y_kj = self.circuit.ybus[k, j]
                P_k = V_k * V_j * abs(Y_kj) * np.cos(delta_k - delta_j - np.angle(Y_kj))

            Px[bus_k] = P_k

        return Px

    def calc_Qx(self):
        Qx = {bus: 0 for bus in self.bus.bus_count}

        for k, bus_k in enumerate(self.bus.bus_count):
            V_k = self.voltage[bus_k]
            delta_k = self.delta[bus_k]
            Q_k = 0
            for j, bus_j in enumerate(self.bus.bus_count):
                V_j = self.voltage[bus_j]
                delta_j = self.delta[bus_j]
                Y_kj = self.circuit.ybus[k, j]
                Q_k = V_k * V_j * abs(Y_kj) * np.sin(delta_k - delta_j - np.angle(Y_kj))

            Qx[bus_k] = Q_k

        return Qx

    #mismatch
    def initialize_x(self):
        delta_vector = np.array(list(self.delta.values()))
        voltage_vector = np.array(list(self.voltage.values()))
        x=np.concatenate((delta_vector, voltage_vector))
        return x

    def initialize_y(self):

        for load in enumerate(self.circuit.load.values()):
            real_power_vector = np.array(list(load["real_power"]))/s.base_power
            reactive_power_vector = np.array(list(load["reactive_power"]))/s.base_power

        for bus in self.bus.bus_count:
            if self.bus.bus_type[bus] != 'slack':
                real_power_vector.append(real_power_vector[self.bus.bus_count(bus)])

        for bus in self.bus.bus_count:
            if self.bus.bus_type[bus] not in ['slack', 'PV']:
                reactive_power_vector.append(reactive_power_vector[self.bus.bus_count(bus)])

        y = np.concatenate(real_power_vector, reactive_power_vector)
        return y

    def calc_mismatch(self):
        return self.y-self.x