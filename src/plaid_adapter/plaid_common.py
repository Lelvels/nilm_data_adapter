import json
import matplotlib.pyplot as plt
import pprint
import numpy as np
import pandas as pd
import h5py as h5py

class PlaidCommon:
    def __init__(self, plaid_file: h5py.File) -> None:
        self.plaid_file = plaid_file
        pass
    
    # Load data from submetered metadata file
    def load_metadata_submetered(self):
        metadata = self.plaid_file["submetered"]
        appliance_dict = {}
        for file_number in metadata:
            appliance_dict[metadata[file_number]["appliance"]["type"]]=[]
        for file_number in metadata:
            if metadata[file_number]["appliance"]["type"] in appliance_dict:
                appliance_dict[metadata[file_number]["appliance"]["type"]].append(file_number)        
        return appliance_dict

    # Load data from aggregated metadata file
    def load_metadata_aggregated(self):    
        metadatas = self.plaid_file["aggregated"]
        result_df = pd.DataFrame
        for index in metadatas:
            metadata = metadatas[str(index)].attrs["metadata"]
            metadata = json.loads(metadata)
            data_id = metadata["id"]
            for appliance in metadata["meta"]["appliances"]:
                data_dict = {}
                data_dict["metadata_id"] = data_id
                data_dict["device_name"] = f"{appliance['type']}_{appliance['brand']}"
                data_dict["on_idx"] = appliance["on"]
                data_dict["off_idx"] = appliance["off"]
                print(data_dict)
        return result_df
    
    def plot_data(self, input_df, which_plot):
        plt.figure(figsize=(10, 6))
        if which_plot.get('Irms', False):
            plt.plot(input_df['Irms'], label='RMS Current (I)')
        if which_plot.get('Urms', False):
            plt.plot(input_df['Urms'], label='RMS Voltage (V)')
        plt.xlabel('Index')
        plt.ylabel('Values')
        plt.title('Data plot')
        plt.legend()
        plt.grid(True)
        plt.show()
    
def plot_data_in_id(self, select_id, meta_datas, data_source):
    for meta_data in meta_datas:
        if meta_data["id"] == select_id:
            pprint.pprint(meta_data["meta"]["appliances"])
            selected_data = data_source[str(select_id)]
            selected_data = np.array(selected_data)
            agg_df = pd.DataFrame(selected_data, columns=["Irms", "Urms"])
            print(agg_df.shape)
            self.plot_data(agg_df[0:10000], which_plot={
                'Irms': True, 
                'Urms': False
            })