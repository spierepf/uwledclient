import logging
import socket
import struct

log = logging.getLogger(__name__)


def update_broadcast(bri=255,
                     col=None,
                     nightlight_active=False,
                     nightlight_delay_mins=0,
                     effect_current=0,
                     effect_speed=0,
                     white=255,
                     col_sec=None,
                     white_sec=255,
                     effect_intensity=255,
                     transition_delay=0,
                     effect_palette=0):
    if col_sec is None:
        col_sec = [255, 255, 255]
    if col is None:
        col = [255, 255, 255]

    BROADCAST_IP = "255.255.255.255"
    BROADCAST_PORT = 21324  # Choose an appropriate port

    MESSAGE = struct.pack("<BBBBBBBBBBBBBBBBBBHBxxx",
                          0,  # Notifier Protocol
                          1,  # Direct Change via UI or API
                          bri,
                          col[0],
                          col[1],
                          col[2],
                          nightlight_active,
                          nightlight_delay_mins,
                          effect_current,
                          effect_speed,
                          white,
                          5,  # Palettes supported
                          col_sec[0],
                          col_sec[1],
                          col_sec[2],
                          white_sec,
                          effect_intensity,
                          transition_delay,
                          effect_palette
                          )
    assert len(MESSAGE) == 24
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(MESSAGE, (BROADCAST_IP, BROADCAST_PORT))
    except Exception as e:
        log.error(f"Error sending broadcast: {e}")

    if __name__ == "__main__":
        update_broadcast()
