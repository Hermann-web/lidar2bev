# Bird’s Eye View (BEV) LiDAR Visualization

This project processes raw LiDAR data and visualizes it as a Bird's Eye View (BEV) RGB image using basic preprocessing and point cloud filtering.

## Features

* Loads `.bin` LiDAR files
* Removes irrelevant points based on 3D spatial boundaries
* Projects the LiDAR data into a 2D BEV feature map
* Saves and displays the resulting RGB BEV image

## Directory Structure

```
project/
├── data/
│   └── velodyne/
│       └── 0000000000.bin
├── utils.py
├── config.py
├── main.py
└── output.png
```

## Dependencies

Ensure you have the following Python packages installed:

```bash
pip install numpy opencv-python
```

## File Descriptions

* `main.py`: Main script to generate and display the BEV image.
* `utils.py`: Contains helper functions for loading and processing LiDAR data.
* `config.py`: Configuration for BEV grid size, discretization, and 3D boundary limits.

## Running the Script

Place a LiDAR `.bin` file in the `data/velodyne/` directory. Then run:

```bash
python main.py
```

This will:

1. Load and preprocess the LiDAR data.
2. Generate a BEV RGB image.
3. Save it as `output.png`.
4. Display it using OpenCV.

## Configuration

Adjust `config.py` for:

* `BEV_WIDTH`: Width of the BEV map.
* `DISCRETIZATION`: Grid resolution.
* `boundary`: 3D spatial limits for filtering points.

## Acknowledgements

This project draws inspiration from and acknowledges the following works:

- [kitti2coco by packyan in Python 3.6](https://github.com/packyan/Kitti2Coco) and [another one](https://cknowledge.io/c/program/object-detection-tf-py-codereef/?action=download&version=1.0.2&filename=converter_annotations.py). they both convert from kitti to coco and inversibly
- [Complex-YOLOv3](https://github.com/ghimiredhikura/Complex-YOLOv3.git): For parsing and training on the KITTI dataset, as well as prediction on BEV lidar data. A large part of the codes is berrowed from their excellent work!
