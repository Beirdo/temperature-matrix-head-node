# vim:ts=4:sw=4:ai:et:si:sts=4

import logging
import statistics
import scippy


logger = logging.getLogger(__name__)


class GridMath(object):
    @staticmethod
    def arithmetic_mean(readings):
        return [statistics.mean(item) if item else None for item in readings]

    @staticmethod
    def harmonic_mean(readings):
        return [scipy.hmean(item) if item else None for item in readings]

    @staticmethod
    def geometric_mean(readings):
        return [scipy.gmean(item) if item else None for item in readings]

    @staticmethod
    def min(readings):
        return [min(item) if item else None for item in readings]

    @staticmethod
    def max(readings):
        return [max(item) if item else None for item in readings]

    @staticmethod
    def median(readings):
        return [statistics.median(item) if item else None for item in readings]

    @staticmethod
    def mode(readings):
        return [statistics.mode(item) if item else None for item in readings]

    @staticmethod
    def variance(readings):
        return [statistics.pvariance(item) if item else None
                for item in readings]

    @staticmethod
    def stdev(readings):
        return [statistics.pstdev(item) if item else None for item in readings]
