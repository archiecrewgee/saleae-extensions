# import math
import numpy as np
from copy import deepcopy

from saleae.data import GraphTime
from saleae.range_measurements import AnalogMeasurer


# todo: look into get_capabiliteis
NUM_OF_SECTIONS = 100

class GradientAnalyser(AnalogMeasurer):
    supported_measurements = []

    # Initialize your measurement extension here
    # Each measurement object will only be used once, so feel free to do all per-measurement initialization here
    def __init__(self, requested_measurements):
        super().__init__(requested_measurements)

        self.slices = []

    # This method will be called one or more times per measurement with batches of data
    # data has the following interface
    #   * Iterate over to get Voltage values, one per sample
    #   * `data.samples` is a numpy array of float32 voltages, one for each sample
    #   * `data.sample_count` is the number of samples (same value as `len(data.samples)` but more efficient if you don't need a numpy array)
    def process_data(self, data):
        average = sum(data.samples) / data.sample_count
        period = float(data.end_time - data.start_time)
        
        self.slices.append((average, period))


    # This method is called after all the relevant data has been passed to `process_data`
    # It returns a dictionary of the request_measurements values
    def measure(self):
        
        # get total period
        period = sum(x[1] for x in self.slices)
        tick_period = period / NUM_OF_SECTIONS

        gradient = []
        # break into sections and calculate gradients, note that slices may be any size but ticks are constant
        for i in range(1, NUM_OF_SECTIONS - 2):
            time_offset = i * tick_period
            
            slice_index = len(self.slices) - 1
            time = 0
            for j, x in enumerate(self.slices):
                time += x[1]
                if time > time_offset:
                    slice_index = j - 1
                    break

            gradient.append(self.slices[slice_index - 1][0] - self.slices[slice_index + 1][0])

        values = {
            "average" : (self.slices[-1][0] - self.slices[0][0]) / period,
            "peak" :  max(gradient) / tick_period,
            "trough" :  min(gradient) / tick_period,
            "change_in_voltage" : self.slices[-1][0] - self.slices[0][0]
        }

        return values