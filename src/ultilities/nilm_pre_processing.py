import pandas as pd
import polars as pl
import numpy as np
import matplotlib.pyplot as plt
import time
import os
from tqdm import tqdm


class NilmPreProcessing:
    def __plot_data(self, input_df, which_plot: dict):
        plt.figure(figsize=(10, 6))
        if(which_plot["Irms"] == True):
            plt.plot(input_df['unix_ts'], input_df['Irms'], label='RMS Current (A)')
        if(which_plot["AvgPowerFactor"] == True):
            plt.plot(input_df['unix_ts'], input_df['AvgPowerFactor'], label='Power factor')
        if(which_plot["P"] == True):
            plt.plot(input_df['unix_ts'], input_df['P'], label='Power (Watt)')
        if(which_plot["Q"] == True):
            plt.plot(input_df['unix_ts'], input_df['Q'], label='Reactive Power Q (VAR)')
        if(which_plot["S"] == True):
            plt.plot(input_df['unix_ts'], input_df['S'], label='Apparent Power S (...)')
        plt.xlabel('Unix time')
        plt.ylabel('Values')
        plt.title(f'{which_plot["name"]}')
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_data_with_time(self, df: pd.DataFrame, device_name:str, start:int = None, end:int = None):
        input_df = None
        if (start is None) or (end is None):
            input_df = df
        else:
            input_df = df[start:end]
        self.__plot_data(input_df=input_df, which_plot={
            "name": device_name,
            "Irms": False,
            "AvgPowerFactor": False,
            "P": True,
            "Q": False,
            "S": False
        })
        
    def plot_distribution(self, array: np.ndarray, plot_name: str, unit_name: str, min: int, max: int) -> None:
        """
        Plots the distribution of a NumPy array using a histogram.

        Args:
            array (np.ndarray): Input array for which the distribution will be visualized.
        """
        # Plot the histogram
        if min is None:
            min = np.min(array)
        if max is None:
            max = np.max(array)
        array = array[(array >= min) & (array <= max)]
        plt.hist(array, color='lightgreen', ec='black', bins=1000)
        plt.xlabel(unit_name)
        plt.ylabel('Frequency')
        plt.title(plot_name)
        plt.show()
        
    def find_on_off_time(self, smallest_threshold, input_df: pl.DataFrame):
        power_np = input_df.select("P").to_numpy()
        # Create a numpy array with dtype 'object' to hold string values
        label_np = np.zeros(len(power_np), dtype=object)
        no_device_idx = (power_np < smallest_threshold).reshape(len(power_np),)
        unlabeled_idx = (power_np >= smallest_threshold).reshape(len(power_np),)
        label_np[no_device_idx] = "off"
        label_np[unlabeled_idx] = "on"
        input_df = input_df.with_columns(pl.Series(name="on_off_label", values=label_np))
        return input_df
    
    def get_running_segments(self, input_df: pl.DataFrame, min_length, smallest_threshold):
        on_times, off_times = [], []
        device_running_dfs = []
        new_labeled_dataset = self.find_on_off_time(smallest_threshold=smallest_threshold, 
                                            input_df=input_df)
        starting_np = new_labeled_dataset[0].to_numpy()[0]
        previous_time = starting_np[1]
        previous_state = starting_np[len(starting_np) - 1]
        
        # Initialize tqdm progress bar for labeling
        progress_bar_labeling = tqdm(total=len(new_labeled_dataset), desc="Labeling ON/OFF")
        for rows in new_labeled_dataset.iter_rows():
            current_time = rows[1]
            current_label = rows[len(rows) - 1]
            if previous_state == "off" and current_label == "on":
                on_times.append(previous_time)
            elif previous_state == "on" and current_label == "off":
                off_times.append(current_time)
            previous_state = current_label
            previous_time = current_time
            # Update tqdm progress bar for labeling
            progress_bar_labeling.update(1)
        progress_bar_labeling.close()
    
        # Initialize tqdm progress bar for segments
        progress_bar_segments = tqdm(total=np.min([len(on_times), len(off_times)]), desc="Processing segments")
        
        for i in range(np.min([len(on_times), len(off_times)])):
            running_df = input_df.filter((pl.col("unix_ts") >= on_times[i]) & (pl.col("unix_ts") <= off_times[i]))
            if (len(running_df) > min_length):
                device_running_dfs.append(running_df) 
            # Update tqdm progress bar for segments
            progress_bar_segments.update(1)
        progress_bar_segments.close()
        
        return device_running_dfs
    
    def count_labels(self, labels):
        unique_labels, counts = np.unique(labels, return_counts=True)
        label_counts = dict(zip(unique_labels, counts))
        return label_counts