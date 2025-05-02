# Front side (of vehicle) Point Cloud boundary for BEV
boundary = {"minX": 0, "maxX": 50, "minY": -25, "maxY": 25, "minZ": -2.73, "maxZ": 1.27}

BEV_WIDTH = 608  # across y axis -25m ~ 25m
BEV_HEIGHT = 608  # across x axis 0m ~ 50m
MAX_COUNTS = 64  # max of repetitions of the same point in the dataset

DISCRETIZATION = (boundary["maxX"] - boundary["minX"]) / BEV_HEIGHT

colors = [[0, 255, 255], [0, 0, 255], [255, 0, 0]]
