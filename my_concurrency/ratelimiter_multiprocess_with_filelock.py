"""Utils to send device info"""

from dataclasses import dataclass
import datetime
import logging
import os
import time
import threading
from typing import IO

from pathlib import Path

from google.protobuf import timestamp_pb2

logging.basicConfig(level=logging.DEBUG)
_LOG = logging.getLogger(__name__)


class RateLimiter:
    """Rate limiter"""
    def __init__(self, period: datetime.timedelta):
        self._interval = period
        self._ratelimit_filename = os.path.join(
            Path.cwd(),
            'ratelimiter.timestamp')
        os.makedirs(os.path.dirname(self._ratelimit_filename), exist_ok=True)

    def next_call_is_allowed(self) -> bool:
        """Check if next request is allowed.

        Lock on file access is used to limit one process at a time. After lock
        acquired, prev call timestamp is checked against rate limit rule.
        """
        lock_filename = 'ratelimiter.lock'
        try:
            lock_file = open(lock_filename, 'x')
        except FileExistsError:
            return False

        try:
            with open(self._ratelimit_filename, 'a+') as ratelimit_file:
                ratelimit_file.seek(0)
                prev_call_timestamp = _read_timestamp(ratelimit_file)
                time_since_prev_call = time.time() - prev_call_timestamp
                if time_since_prev_call < self._interval.total_seconds():
                    return False
                ratelimit_file.truncate(0)
                _write_timestamp(ratelimit_file, time.time())
                return True
        finally:
            lock_file.close()
            os.remove(lock_filename)

    def reset(self) -> None:
        """Reset expiration time."""
        os.remove(self._ratelimit_filename)


@dataclass
class DeviceInfo:
    serial_number: str
    
@dataclass
class DeviceEvent:
    device_info: DeviceInfo
    timestamp: timestamp_pb2.Timestamp


def _read_timestamp(file: IO) -> float:
    try:
        return datetime.datetime.timestamp(datetime.datetime.fromtimestamp(float(file.read())))
    except ValueError:
        return 0.0


def _write_timestamp(file: IO, timestamp: float) -> None:
    file.write(str(timestamp))



def _upload_device_event(
    event: DeviceEvent,
    cooldown_period: datetime.timedelta = datetime.timedelta(hours=12)
) -> None:
    """Uploads device event"""
    ratelimiter = RateLimiter(period=cooldown_period)
    if not ratelimiter.next_call_is_allowed():
        _LOG.info(
            'Upload board info exceeds rate limit. Please try again later.')
        return

    _LOG.info(event)


def upload_board_info_async(serial_number: str) -> None:
    device_info = DeviceInfo(serial_number)
    timestamp = timestamp_pb2.Timestamp(seconds=round(time.time()))
    event = DeviceEvent(device_info=device_info,
                                            timestamp=timestamp)
    threading.Thread(target=_upload_device_event, args=(event, )).start()
    
    
if __name__ == '__main__':
    upload_board_info_async('123')