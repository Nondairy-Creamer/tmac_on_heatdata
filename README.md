## Two-channel motion artifact correction (TMAC)

### Installation:
clone this repo to a directory.
Navigate to the python project directory in a terminal
```
git clone https://github.com/Nondairy-Creamer/tmac
cd tmac
pip install -e .
```

### Usage:
In a terminal run

```
python tmac_on_heatdata.py <brinascanner folder>
```

The script will 
* linearly interpolate over nans. Make sure your data does not have so many nans that linear interpolation is innaccurate
* correct for photobleaching by dividing by an exponential
* output tmac\_output.mat (MATLAB) and tmac\_output.pkl (python) which contains a dictionary of the outputs

The output dictionary contains
* a: The neural activity (time, neurons)
* m: The motion artifact (time, neurons)
* g\_raw, r\_raw: the green and red fluorescence input (time, neurons)
* length\_scale\_a, length\_scale\_m: the timescale of the gaussian process for a and m in units of time indicies
* variance\_a, variance\_m: the amplitude of a and m
* variance\_g\_noise, variance\_r\_noise: the amplitude of the channel noise for r and g

