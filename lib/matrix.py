# vim:ts=4:sw=4:ai:et:si:sts=4

import logging
import time


logger = logging.getLogger(__name__)


class SensorNode(object):
    def __init__(self, boardNum, sensorNum, x, y, z):
        self.boardNum = boardNum
        self.sensorNum = sensorNum
        self.x = x
        self.y = y
        self.z = z
        self.temperature = None
        self.timestamp = 0


class Matrix(object):
    def __init__(self, mapping):
        self.map = mapping

        self.reverseMap = {}
        for (x, itemX) in item.items():
            for (y, itemY) in itemX.items():
                for (z, itemZ) in itemY.items():
                    boardNum = item.boardNum
                    sensorNum = item.sensorNum
                    if boardNum not in self.reverseMap:
                        self.reverseMap[boardNum] = {}
                    self.reverseMap[boardNum][sensorMap] = itemZ

    def setTemperature(self, boardNum, sensorNum, temperature, timestamp):
        item = self.reverseMap.get(boardNum, {}).get(sensorNum, {})
        if not item:
            logger.warning("Unmapped sensor: board %02X, sensor %02X" %
                           (boardNum, sensorNum))
            return

        item.temperature = temperature
        item.timestamp = timestamp

    def getTemperature(self, x, y, z):
        item = self.map.get(x, {}).get(y, {}).get(z, {})
        if not item:
            logger.warning("Unmapped sensor: (%s, %s, %s)" % (x, y, z))
            return None

        if not item.timestamp:
            return None

        age = time.time() - item.timestamp
        if age > 60.0:
            logger.warning("Temperature reading for (%s, %s, %s) "
                           "aged out (%.3fs old)" % (x, y, z, age))
            return None

        return item.temperature

    def getTemperatureGrid(self):
        return [[[self.getTemperature(x, y, z) for z in sorted(itemY.keys())]
                 for (y, itemY) in sorted(itemX.items())]
                for (x, itemX) in sorted(self.map.items())]


    def getAverageTemperature(self, mode="z-slice"):
        grid = self.getTemperatureGrid()

        xmax = len(grid)
        ymax = max([len(y) for y in grid])
        zmax = max([len(z) for y in grid for z in y])

        if mode == "x-slice":
            readings = [[grid[x][y][z] for y in range(ymax)
                         for z in range(zmax)] for x in range(xmax)]
        elif mode == "y-slice":
            readings = [[grid[x][y][z] for x in range(xmax)
                         for z in range(zmax)] for y in range(ymax)]
        elif mode == "z-slice":
            readings = [[grid[x][y][z] for x in range(xmax)
                         for y in range(ymax)] for z in range(zmax)]
        else:
            readings = [[grid[x][y][z] for x in range(xmax)
                         for y in range(ymax) for z in range(zmax)]]

        readings = [list(filter(lambda x: x is not None, item))
                    for item in readings]
        sums = [sum(item) if item else None for item in readings]
        counts = [len(item) if item else None for item in readings]
        averages = [total / count if item is not None else none
                    for (total, count) in zip(sums, counts)]

        if len(averages) == 1:
            averages = averages[0]

        return averages
