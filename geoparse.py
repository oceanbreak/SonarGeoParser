#!/usr/bin/env python
# coding: utf-8

import re

# Public variables and functions
    
def georead(filename):
    coord_array = [] # initialize array of coordinates
    with open(filename, 'r') as f_read:
        try:
            for line in f_read:
                sample_string = line.strip()
                coord_array.append(sample_string)
        except:
            raise ValueError
    return coord_array


def geosave(coord_array, filename, delimiter=';'):
    with open(filename, 'w') as csvfile:
        for line in coord_array:
            n_line = [None] * len(line)
            for i in range(len(n_line)):
                if type(line[i]) == float:
                    n_line[i] = '%8.5f' % line[i]
                else:
                    n_line[i] = str(line[i])
            csvfile.write(delimiter.join(n_line) + '\n')
            

def getCoordinatesDegMin(input_array):
    coord_array = [] # initialize array of coordinates
    for line in input_array:
        out = _processCoordString(line)
        if out: coord_array.append(out[0] + out[1])
    if coord_array:
        return coord_array
    else:
        raise ValueError

def getCoordinatesDeg(input_array):
    coord_array = [] # initialize array of coordinates
    for line in input_array:
        out = _processCoordString(line)
        if out:
            coord_array.append((_convertToDegrees(*out[1]),
                                _convertToDegrees(*out[0])))
    if coord_array:
        return coord_array
    else:
        raise ValueError


# Private variables and functions

_multiplier = {'N':1, 'S':-1, 'E':1, 'W':-1}

def _processCoordString(sample_string):
    # Get two coordinates in foramt DDMM.mmmN*
    lat_pattern = re.compile('\d*\D*\d*\.\d*\D*[NS]')
    lon_pattern = re.compile('\d*\D*\d*\.\d*\D*[EW]')

    lat_reg = re.search(lat_pattern, sample_string)
    lon_reg = re.search(lon_pattern, sample_string)

    if lat_reg and lon_reg:
        lat_string = sample_string[lat_reg.start() : lat_reg.end()]
        lon_string = sample_string[lon_reg.start() : lon_reg.end()]

        deg_pattern = re.compile('\d\d*[^.]')
        lat_reg = re.search(deg_pattern, lat_string)
        lon_reg = re.search(deg_pattern, lon_string)
        lat_deg = int(lat_string[lat_reg.start() : lat_reg.end()-1])
        lon_deg = int(lon_string[lon_reg.start() : lon_reg.end()-1])

        minutes_patern = re.compile('\d\d\.\d*')
        lat_min = float(re.search(minutes_patern, lat_string).group(0))
        lon_min = float(re.search(minutes_patern, lon_string).group(0))

        lat = lat_string[-1]
        lon = lon_string[-1]

        return (((lat_deg, lat_min, lat),
                (lon_deg, lon_min, lon)))
    else:
       return None

    
def _convertToDegrees(lat_deg, lat_min, lat):
    return _multiplier[lat] * (lat_deg + lat_min/60)
    

if __name__=='__main__':        
    a = georead('Gals_East.txt')
    b = getCoordinatesDegMin(a)
    c = getCoordinatesDeg(a)
    geosave(c, 'temp.csv')