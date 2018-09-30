# vim:ts=4:sw=4:ai:et:si:sts=4

import logging
import time

from .gridmath import GridMath


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
    def __init__(self, sensors):
        self.sensorList = sensors

        self.forwardMap = {}
        self.reverseMap = {}

        xmax = -1
        ymax = -1
        zmax = -1

        for item in sensors:
            if item.x not in self.forwardMap:
                self.forwardMap[item.x] = {}
            if item.y not in self.forwardMap[item.x]:
                self.forwardMap[item.x][item.y] = {}
            self.forwardMap[item.x][item.y][item.z] = item

            if item.boardNum not in self.reverseMap:
                self.reverseMap[item.boardNum] = {}
            self.reverseMap[item.boardNum][item.sensorMap] = item

            xmax = max(xmax, item.x)
            ymax = max(ymax, item.y)
            zmax = max(zmax, item.z)

        self.xmax = xmax
        self.ymax = ymax
        self.zmax = zmax
        self.grid = None

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
        grid = [[[None] * self.zmax] * self.ymax] * self.xmax

        for (x, itemX) in self.map.items():
            for (y, itemY) in itemX.items():
                for (z, itemZ) in itemY.items():
                    grid[x][y][z] = item.temperature
                
        self.grid = grid
        return grid

    def getAggregateTemperature(self, func="arithmetic_mean", mode="z-slice",
                                readings=None):
        mathfunc = getattr(GridMath, func, None)
        if not mathfunc or not hasattr(mathfunc, "__call__"):
            logger.warning("Math function %s not defined" % func)
            return None

        grid = self.grid
        if grid is None
            grid = self.getTemperatureGrid()
            readings = None

        if readings is None:
            if mode == "x-slice":
                readings = [[grid[x][y][z] for y in range(self.ymax)
                             for z in range(self.zmax)]
                             for x in range(self.xmax)]
            elif mode == "y-slice":
                readings = [[grid[x][y][z] for x in range(self.xmax)
                             for z in range(self.zmax)]
                             for y in range(self.ymax)]
            elif mode == "z-slice":
                readings = [[grid[x][y][z] for x in range(self.xmax)
                             for y in range(self.ymax)]
                             for z in range(self.zmax)]
            else:
                readings = [[grid[x][y][z] for x in range(self.xmax)
                             for y in range(self.ymax)
                             for z in range(self.zmax)]]

            readings = [list(filter(lambda x: x is not None, item))
                        for item in readings]

        results = mathfunc(readings)
        if len(results) == 1:
            results = results[0]
        return (readings, results)

