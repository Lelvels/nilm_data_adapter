from __future__ import print_function, division
from nilmtk import DataSet
from os.path import join
import nilmtk.elecmeter
from pylab import rcParams
import nilmtk as nilmtk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class IaweDAO:
    def __init__(self, h5_path) -> None:
        self.original_dataset = DataSet(h5_path)
        self.original_dataset.set_window(start="7-1-2013", end="10-1-2013")
        self.building_elec = self.original_dataset.buildings[1].elec
        pass
    
    def get_metadata_info(self):
        return self.original_dataset.metadata
    
    def get_device_and_mains_info(self):
        print("[-] Main meters:")
        for meter in self.building_elec.mains().meters:
            print(f"Main meter: {meter}, columns: {meter.available_columns()}")
        print()
        print("[-] Application meters:")
        for meter in self.building_elec.meters:
            if(isinstance(meter, nilmtk.elecmeter.ElecMeter)):
                print(f"Meter: {meter}, columns: {meter.available_columns()}")
            elif(isinstance(meter, nilmtk.metergroup.MeterGroup)):
                for submeter in meter.meters:
                    print(f"Sub meter: {submeter}, columns: {submeter.available_columns()}")
                    
    def load_main_df(self, meter_id):
        main_meter = self.building_elec.mains().meters[meter_id]
        main_meter_df = next(main_meter.load())
        return main_meter_df
    
    def load_device_df(self, meter_id):
        meter = self.building_elec.meters[meter_id]
        if (isinstance(meter, nilmtk.elecmeter.ElecMeter)):
            print(f"Meter information: {meter}")
            meter_df = next(meter.load())
            return meter_df
        else:
            print(f"This appears to be a MeterGroup, please select single device only!")
            return None
            