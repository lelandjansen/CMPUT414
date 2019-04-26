# CMPUT414
CMPUT 414 course (Winter 2019) Team Hawaii - Leland Jansen and Nathan Liebrecht

# Reproducing results

Our project is grouped into 3 broad steps:

1. Generate the 64x64 raster tiles
2. Train the YOLO CNN
3. Testing inference

To get pre-generated training data (`data.zip`) and final trained weights 
download the files at:
https://drive.google.com/drive/u/1/folders/10x4pRpnZcyZsu-ysS38-0K1WWxSCFhEj

# Pre-requisits

The following python libraries must be installed:
```
sudo pip3 -U install pptk numpy sklearn
```

Next, Darknet must be downloaded and compiled. Simply clone the darknet 
repository into the `src` folder and compile it. The compilation instructions
and code repository can be found here: https://github.com/AlexeyAB/darknet#how-to-compile-on-linux

`LIBSO=1` must be enabled for inference to work.


## 1. Generating the 64x64 raster tiles

To skip this step, simply extract the data.zip folder into the `src/darknet/build/darknet/x64` folder
created in the "Pre-requisits" section.

To re-rasterize the Sydney dataset included in the data folder into the 64x64 tiles
1. Create an `out` folder in the root of the repository
1. Run `visualize.py`. 
   Data will be output in the `out` folder. This will take around 4 hours.
   Once this is complete, copy the files in `out` into a new folder: 
   `src/darknet/build/darknet/x64/data/414`
2. Run `split_dataset.py` to regenerate the data split. Copy `test.txt` and `train.txt`
   into the `src/darknet/build/darknet/x64/data` folder.
3. Copy the remaining configuration files into the data folder from the `data.zip` file.
   These are fixed configuration files that remain constant

You should now have a file structure similar to the provided `data.zip` file.


## 2. Train the YOLO CNN

To skip this step you may just copy over the `yolov3-414_final.weights` found in the drive link
into `src/darknet/build/darknet/x64`.

To train from scratch:

1. Change to the directory with the darknet binary (`src/darknet/build/darknet/x64`)
2. Download the starting weights https://pjreddie.com/media/files/darknet53.conv.74
3. Run `darknet detector train data/414.data data/yolov3-414.cfg darknet53.conv.74 -map`
4. Move `src/darknet/build/darknet/x64/backup/yolov3-414_final.weights` up a directory.


## 3. Testing inference

1. Copy `src/infer.py` into `src/darknet/build/darknet/x64`. This file should be in the same
   folder as `darknet.py` and the dynamic darknet library (`libdarknet.so` on Linux)
2. Run `infer.py`


