def get_directional_letter(latitude, longitude):
    if latitude >= 0:
        lat_letter = 'N'
    else:
        lat_letter = 'S'

    if longitude >= 0:
        long_letter = 'E'
    else:
        long_letter = 'W'

    return lat_letter + long_letter
