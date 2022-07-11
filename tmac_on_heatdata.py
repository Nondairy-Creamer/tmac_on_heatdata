import sys
import tmac.models as tm
import tmac.preprocessing as tp
import scipy.io as sio
import pickle

# this script will load in a heatData.mat file output from the 3dbrain pipeline
# https://github.com/leiferlab/3dbrain
# Then run TMAC on the raw red and green channels to infer the neural activity
# https://github.com/Nondairy-Creamer/tmac
# This script starts by linearly interpolating over nans in the data. If your data has many NaNs such that linear
# interpolation is not a good model, consider some other form of data imputation

# get the path from user input
folder_path = sys.argv[1]

if folder_path[-1] != '/' and folder_path[-1] != '\\':
    folder_path = folder_path + '/'

heat_data_path = folder_path + 'heatData.mat'
tmac_save_path = folder_path + 'tmac_output'

# load in heatmat data
heat_data = sio.loadmat(heat_data_path)
red = heat_data['rRaw'].T
green = heat_data['gRaw'].T

# interpolate to get rid of nans in data
red_interp = tp.interpolate_over_nans(red)[0]
green_interp = tp.interpolate_over_nans(green)[0]

# correct for photobleaching by dividing by an exponential fit to the fluorescence
red_corrected = tp.photobleach_correction(red_interp)
green_corrected = tp.photobleach_correction(green_interp)

# run tmac on the red and green channel to extract the activity
trained_variables = tm.tmac_ac(red_corrected, green_corrected)

# add the raw red and green to the output variables
trained_variables['r_raw'] = red
trained_variables['g_raw'] = green


# save to matlab format
sio.savemat(tmac_save_path + '.mat', trained_variables)

# save to pickle format for python
pickle_out = open(tmac_save_path + '.pkl', 'wb')
pickle.dump(trained_variables, pickle_out)
pickle_out.close()
