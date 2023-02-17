import gpsd


def get_current_position():
    gpsd.connect()
    packet = gpsd.get_current()
    gpsd.close()

    if not packet.is_valid:
        raise Exception('GPS data not valid')

    return packet.position()
