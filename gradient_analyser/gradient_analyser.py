# import math
import numpy as np

from saleae.data import GraphTime
from saleae.range_measurements import AnalogMeasurer


class GradientAnalyser(AnalogMeasurer):
    supported_measurements = []

    # Initialize your measurement extension here
    # Each measurement object will only be used once, so feel free to do all per-measurement initialization here
    def __init__(self, requested_measurements):
        super().__init__(requested_measurements)


    # This method will be called one or more times per measurement with batches of data
    # data has the following interface
    #   * Iterate over to get Voltage values, one per sample
    #   * `data.samples` is a numpy array of float32 voltages, one for each sample
    #   * `data.sample_count` is the number of samples (same value as `len(data.samples)` but more efficient if you don't need a numpy array)
    def process_data(self, data):
        self.test = data.sample_count / float(data.end_time - data.start_time)
        pass

    # This method is called after all the relevant data has been passed to `process_data`
    # It returns a dictionary of the request_measurements values
    def measure(self):
        values = {
            "average" : 0,
            "peak" :  0,
            "trough" :  0
        }
        return values
