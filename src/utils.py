from pathlib import Path

import cv2
import numpy as np

from src.config import BEV_HEIGHT, BEV_WIDTH, MAX_COUNTS, colors


def get_lidar(lidar_file: str | Path) -> np.ndarray:
    lidar_file = Path(lidar_file)
    assert lidar_file.exists(), f"lidar_file {lidar_file} not found"
    return np.fromfile(str(lidar_file), dtype=np.float32).reshape(-1, 4)


def display_bev_img(img: np.ndarray, img_size: int) -> None:
    img_display = np.zeros((img_size, img_size, 3), np.uint8)
    img_display[...] = img[...]

    cv2.imshow("img-kitti-bev", img_display)

    # Wait for a key press, press 'Esc' to break the loop
    if cv2.waitKey(0) & 0xFF == 27:
        return


def removePoints(PointCloud, BoundaryCond):
    # Boundary condition
    minX = BoundaryCond["minX"]
    maxX = BoundaryCond["maxX"]
    minY = BoundaryCond["minY"]
    maxY = BoundaryCond["maxY"]
    minZ = BoundaryCond["minZ"]
    maxZ = BoundaryCond["maxZ"]

    # Remove the point out of range x,y,z
    mask = np.where(
        (PointCloud[:, 0] >= minX)
        & (PointCloud[:, 0] <= maxX)
        & (PointCloud[:, 1] >= minY)
        & (PointCloud[:, 1] <= maxY)
        & (PointCloud[:, 2] >= minZ)
        & (PointCloud[:, 2] <= maxZ)
    )
    PointCloud = PointCloud[mask]

    PointCloud[:, 2] = PointCloud[:, 2] - minZ

    return PointCloud


def makeBVFeature(PointCloud_, Discretization, bc):
    Height = BEV_HEIGHT + 1
    Width = BEV_WIDTH + 1

    max_counts = MAX_COUNTS

    # Discretize Feature Map
    PointCloud = np.copy(PointCloud_)
    PointCloud[:, 0] = np.int_(np.floor(PointCloud[:, 0] / Discretization))
    PointCloud[:, 1] = np.int_(np.floor(PointCloud[:, 1] / Discretization) + Width / 2)

    # sort-3times
    indices = np.lexsort((-PointCloud[:, 2], PointCloud[:, 1], PointCloud[:, 0]))
    PointCloud = PointCloud[indices]

    # Height Map
    heightMap = np.zeros((Height, Width))

    _, indices, counts = np.unique(
        PointCloud[:, 0:2], axis=0, return_index=True, return_counts=True
    )

    PointCloud_top = PointCloud[indices]
    # some important problem is image coordinate is (y,x), not (x,y)
    max_height = float(np.abs(bc["maxZ"] - bc["minZ"]))
    heightMap[np.int_(PointCloud_top[:, 0]), np.int_(PointCloud_top[:, 1])] = (
        PointCloud_top[:, 2] / max_height
    )

    # Intensity Map & DensityMap
    intensityMap = np.zeros((Height, Width))
    densityMap = np.zeros((Height, Width))

    normalizedCounts = np.minimum(1.0, np.log(counts + 1) / np.log(max_counts))

    intensityMap[
        np.int_(PointCloud_top[:, 0]), np.int_(PointCloud_top[:, 1])
    ] = PointCloud_top[:, 3]
    densityMap[
        np.int_(PointCloud_top[:, 0]), np.int_(PointCloud_top[:, 1])
    ] = normalizedCounts

    RGB_Map = np.zeros((3, Height - 1, Width - 1))
    RGB_Map[2, :, :] = densityMap[:BEV_HEIGHT, :BEV_WIDTH]  # r_map
    RGB_Map[1, :, :] = heightMap[:BEV_HEIGHT, :BEV_WIDTH]  # g_map
    RGB_Map[0, :, :] = intensityMap[:BEV_HEIGHT, :BEV_WIDTH]  # b_map

    return RGB_Map
