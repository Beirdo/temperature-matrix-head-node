# vim:ts=4:sw=4:ai:et:si:sts=4

import logging
import struct


logger = logging.getLogger(__name__)


class TemperatureMessage(object):
    msgFormat = "[LBB[H"
    def __init__(self, canMessage):
        self.srcID = canMessage.arbitration_id
        self.timestamp = canMessage.timestamp
        raw = canMessage.data
        parts = struct.unpack(raw)
        self.remote_timestamp = parts[0]
        self.board_number = parts[1]
        self.sensor_number = parts[2]
        self.temperature = parts[3] / 256.0
