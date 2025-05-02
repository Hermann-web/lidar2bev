import sys

import numpy as np

sys.path.append(".")

from pathlib import Path

import cv2

from config import BEV_WIDTH, DISCRETIZATION, boundary
from utils import display_bev_img, get_lidar, makeBVFeature, removePoints

lidar_path = Path("data/velodyne")
assert lidar_path.exists(), f"lidar_path {lidar_path} not found"


lidar_file = lidar_path / f"0000000000.bin"
lidarData = get_lidar(lidar_file)

b = removePoints(lidarData, boundary)
rgb_map = makeBVFeature(b, DISCRETIZATION, boundary)


# Transpose the image to (608, 608, 3) shape
bev_img = rgb_map.squeeze() * 255
bev_img = bev_img.transpose(1, 2, 0).astype(np.uint8)
bev_img_shape = bev_img.shape

# Save the image
bev_img_path = "output.png"
img_size = BEV_WIDTH
cv2.imwrite(bev_img_path, bev_img)
display_bev_img(bev_img, img_size)
