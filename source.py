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

lats = []
data = []
for en, file_ in enumerate(glob.glob1(process_path, "{}*h*".format(file_flag))):

    print(file_, en)
    inner_file = os.path.join(process_path, file_)
    f = SD(inner_file, SDC.READ)
    # f = h5py.File(os.path.join(process_path,file_),'r')
    # f = open_file(inner_file, mode="r", title="VIIRS")
    lat = []
    lon = []
    dat = []
    lat = f.select('Latitude').get()  # select sds
    lon = f.select('Longitude').get()  # select sds
    dat = f.select('Radiance_M1').get()  # select sds
    if en == 0:
        lats = numpy.vstack([lat, lat])
        lons = numpy.vstack([lon, lon])
        data = numpy.vstack([dat, dat])
    else:
        lats = numpy.vstack([lats, lat])
        lons = numpy.vstack([lons, lon])
        data = numpy.vstack([data, dat])

swath_def = pyresample.geometry.SwathDefinition(lons=lon, lats=lat, nprocs=4)
area_def = load_area('areas.yaml', 'worldeqc3km70')
result = resample_nearest(swath_def, data, area_def, radius_of_influence=50000, nprocs=30)
print(f.keys())
# f.close()


flag = "EIIRP"
end = datetime.datetime.now()
print(end - start)
print("{}".format(flag))
