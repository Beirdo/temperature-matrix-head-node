# vim:ts=4:sw=4:ai:et:si:sts=4

import logging
import struct
import can
from can.bus import BusState
from threading import Thread


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


class CANBUSReceiver(Thread):
    def __init__(self, channel, bitrate, matrix):
        self.channel = channel
        self.bitrate = bitrate
        self.matrix = matrix
        self.daemon = True
        Thread.__init__(self)

    def run(self):
        logger.info("Starting CANBUSReceiver thread")

        bus = can.interface.Bus(bustype='socketcan', channel=self.channel,
                                bitrate=self.bitrate)
        bus.state = BusState.ACTIVE

        try:
            while True:
                msg = bus.recv(1)
                if msg is None:
                    continue
                message = TemperatureMessage(msg)
                self.matrix.setTemperature(message.board_number,
                        message.sensor_number, message.temperature,
                        message.timestamp)
        except KeyboardInterrupt:
            pass

        logger.info("Ending CANBUSReceiver thread")
