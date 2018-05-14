#!/usr/bin/python
# -*- coding: utf-8 -*-

def decode(polyline_str, precision=5):
    values = list(_decode(polyline_str, precision))

    polyline = [[0, 0]]
    for i in range(0, len(values), 2):
        latitude = round(polyline[-1][0] + values[i], precision)
        longitude = round(polyline[-1][1] + values[i + 1], precision)
        polyline.append([latitude, longitude])
    return polyline[1:]

def _decode(polyline_str, precision):
    coordinate = []

    for char in polyline_str:
        decimal = ord(char) - 63

        if decimal & 0x20:
            coordinate.append(decimal & 0x1F)
            continue

        coordinate.append(decimal)
        coordinate.reverse()

        result = 0
        for v in coordinate:
            result = (result << 5) | v
        coordinate = []

        yield (~(result >> 1) if (result & 1) else (result >> 1)) / (10 ** precision)

def encode(polyline, precision=5):
    coordinates = []

    for i in range(0, len(polyline)):
        for x in range(0, 2):
            coordinates.append(_encode(polyline[i][x], precision) if (i == 0) else _encode(polyline[i][x] - polyline[i - 1][x], precision))

    return ''.join(coordinates)

def _encode(coordinate, precision):
    decimal = round(coordinate * (10 ** precision))
    decimal <<= 1
    decimal = decimal if (coordinate > 0) else (~decimal | 0x01)

    polyline = []

    while decimal >= 0x20:
        polyline.append(chr((decimal & 0x1F | 0x20) + 63))
        decimal >>= 5

    polyline.append(chr(decimal + 63))

    return ''.join(polyline)