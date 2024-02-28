import numpy as np
import os
import obspy
from tqdm import tqdm
import datetime
'''
This file to concatenate simple label and sac data together
so that after 
'''


def sac2binary(npy_subdir, save_dir):
    min_freq = 1
    max_freq = 50
    st_n = obspy.read(sac_n)
    st_z = obspy.read(sac_z)
    files = sorted(os.listdir(npy_subdir))
    os.makedirs(save_dir, exist_ok=True)
h

    for f in tqdm(files):
        time_stamp = f.split("_")[0]
        # npts = 4096
        start = obspy.UTCDateTime(datetime.datetime.utcfromtimestamp((float(time_stamp) - 2048) / 1000))
        end = obspy.UTCDateTime(datetime.datetime.utcfromtimestamp((float(time_stamp) + 2100) / 1000))

        st_n_slice = st_n.slice(starttime=start, endtime=end)[0].data
        st_z_slice = st_z.slice(starttime=start, endtime=end)[0].data

        st_n_slice = np.resize(st_n_slice, 1024)
        st_z_slice = np.resize(st_z_slice, 1024)

        # label = np.load(os.path.join(npy_subdir, f)).flatten()
        label = np.load(os.path.join(npy_subdir, f))
        label_trans = label.transpose()
        label_slice = label_trans[:, 1:]  # discard column "sum"
        label_flatten = label_slice.flatten()

        save_path = os.path.join(save_dir, f.split(".")[0] + ".npy")

        # if (len(st_z_slice) == 1024 and len(label) == 4096):
        if len(st_z_slice) == 1024:
            trace_data = np.concatenate((st_n_slice,st_z_slice,label_flatten))
            np.save(save_path, trace_data)
        else:
            # print(str(savepath))
            skipped.write(str(save_path) + "\n")


# concat sac data and label together
def video2array_directory(label_dir, base_dir):
    # npydir = os.path.join(path_dir, "35/res_bird64")
    # basedir = os.path.join(path_dir, "35/250nz64")
    for i, d in enumerate(sorted(os.listdir(label_dir),  key=lambda x: int(x))):
        full_path = os.path.join(label_dir, d)
        if os.path.isdir(full_path):
            save_dir = os.path.join(base_dir, str(i))
            sac2binary(full_path, save_dir)


# integrate all the npy files into one npy, so that we can manipulate one dataframe conveniently
def integrate(base_dir):
    count = 0  # total file number, to create an empty ndarray
    i = 0
    for file in os.listdir(base_dir):
        count += len(os.listdir(base_dir + "/" + file))

    label = np.empty((count, 2054))  # 2048+6
    for subdir in tqdm(os.listdir(base_dir)):
        for file in os.listdir(base_dir + "/" + subdir):
            label[i] = np.load(base_dir + "/" + subdir + "/" + file)
            i += 1
    np.save("F:/35/test/simple_data.npy", label)


if __name__ == '__main__':
    sac_n = r"F:\sac4timeshift\1122\231122.000000.EB003035.HHN250.sac"
    sac_z = r"F:\sac4timeshift\1122\231122.000000.EB003035.HHZ250.sac"
    skipped = open("noskiptry.txt", 'w')

    label_dir = r"F:\35\res_simple64"
    base_dir = r"F:\35\concate_simple"

    # video2array_directory(label_dir=label_dir, base_dir=base_dir)
    integrate(base_dir=base_dir)
