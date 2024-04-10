from __future__ import print_function, division
import h5py as h5py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pprint as pprint
from plaid_common import PlaidCommon

plaind_file = h5py.File("../../data/PLAID/plaid_new_.hdf5")
aggregated = plaind_file["aggregated"]
submetered = plaind_file["submetered"]

plaind_common = PlaidCommon(plaid_file=plaind_file)
plaind_common.load_metadata_aggregated()