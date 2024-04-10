import pandas as pd
import numpy as np
import scipy.io
import matplotlib.pyplot as plt

# Load the .mat file
mat_data = scipy.io.loadmat('/home/mrcong/Code/mylab-nilm-files/data_adapter/data/ECO/01/2012-05-29.mat')

# Extract the structured array for 'Appliance010020120529'
structured_array = mat_data['Appliance010020120529']
structured_array = np.array(structured_array)
# Print the DataFrame
real_power = structured_array[0][0][0]
real_power = real_power.reshape(real_power.shape[0], )
# Create a plot
plt.plot(real_power[0:10000])

# Add title and labels
plt.title('Array Data Plot')
plt.xlabel('Index')
plt.ylabel('Value')

# Show the plot
plt.show()
