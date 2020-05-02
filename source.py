import os
import sys
import numpy
import h5py
import glob
import datetime
import pyresample
import matplotlib.pyplot as plt
from tables import *
from pyhdf.SD import SD, SDC
from pyresample import load_area, save_quicklook, SwathDefinition
from pyresample.kd_tree import resample_nearest
start = datetime.datetime.now()
file_flag = 'NPP_VMAES_L1'

process_path = '/external/b/viirs/set3'
for file_ in glob.glob1(process_path,"{}*h*".format(file_flag)):
    print(file_)
    inner_file =os.path.join(process_path,file_)
    f = SD(inner_file,SDC.READ)
    # f = h5py.File(os.path.join(process_path,file_),'r')
    # f = open_file(inner_file, mode="r", title="VIIRS")
    lat = []
    lon = []
    Radiance_M1 = []
    lat = f.select('Latitude').get()  # select sds
    lon = f.select('Longitude').get()  # select sds
    Radiance_M1 = f.select('Radiance_M1').get()  # select sds
    swath_def = pyresample.geometry.SwathDefinition(lons=lon, lats=lat, nprocs=4)
    area_def = load_area('areas.yaml', 'worldeqc3km70')
    result = resample_nearest(swath_def, Radiance_M1, area_def, radius_of_influence=50000,  nprocs=20)
    print(f.keys())
    # f.close()
    break




end = datetime.datetime.now()
print(end - start)
