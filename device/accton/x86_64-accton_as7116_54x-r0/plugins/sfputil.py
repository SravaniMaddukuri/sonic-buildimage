#!/usr/bin/env python

try:
    import time
    from sonic_sfp.sfputilbase import SfpUtilBase 
except ImportError, e:
    raise ImportError (str(e) + "- required module not found")


class SfpUtil(SfpUtilBase):
    """Platform specific SfpUtill class"""

    _port_start = 0
    _port_end = 53
    _qsfp_port_start = 48
    _ports_in_block = 54

    _port_to_eeprom_mapping = {}
    _port_to_i2c_mapping = {
        0 : 37,
        1 : 38,
        2 : 39,
        3 : 40,
        4 : 41,
        5 : 42,
        6 : 43,
        7 : 44,
        8 : 45,
        9 : 46,
        10 : 47,
        11 : 48,
        12 : 49,
        13 : 50,
        14 : 51,
        15 : 52,
        16 : 53,
        17 : 54,
        18 : 55,
        19 : 56,
        20 : 57,
        21 : 58,
        22 : 59,
        23 : 60,
        24 : 61,
        25 : 62,
        26 : 63,
        27 : 64,
        28 : 65,
        29 : 66,
        30 : 67,
        31 : 68,
        32 : 69,
        33 : 70,
        34 : 71,
        35 : 72,
        36 : 73,
        37 : 74,
        38 : 75,
        39 : 76,
        40 : 77,
        41 : 78,
        42 : 79,
        43 : 80,
        44 : 81,
        45 : 82,
        46 : 83,
        47 : 84,
        48 : 21,
        49 : 22,
        50 : 23,
        51 : 24,
        52 : 25,
        53 : 26,
    }

    _qsfp_ports = range(_qsfp_port_start, _ports_in_block + 1)

    def __init__(self):
        eeprom_path = '/sys/bus/i2c/devices/{0}-0050/sfp_eeprom'
        for x in range(self._port_start, self._port_end + 1):
            port_eeprom_path = eeprom_path.format(self._port_to_i2c_mapping[x])
            self._port_to_eeprom_mapping[x] = port_eeprom_path
                
            SfpUtilBase.__init__(self)

    def reset(self, port_num):
        # Check for invalid port_num
        if port_num < self._port_start or port_num > self._port_end:
            return False

        path = "/sys/bus/i2c/devices/{0}-0050/sfp_port_reset"
        port_ps = path.format(self._port_to_i2c_mapping[port_num])
          
        try:
            reg_file = open(port_ps, 'w')
        except IOError as e:
            print "Error: unable to open file: %s" % str(e)
            return False

        #toggle reset
        reg_file.seek(0)
        reg_file.write('1')
        time.sleep(1)
        reg_file.seek(0)
        reg_file.write('0')
        reg_file.close()
        return True

    def set_low_power_mode(self, port_nuM, lpmode):
        raise NotImplementedError

    def get_low_power_mode(self, port_num):
        raise NotImplementedError
        
    def get_presence(self, port_num):
        # Check for invalid port_num
        if port_num < self._port_start or port_num > self._port_end:
            return False

        path = "/sys/bus/i2c/devices/{0}-0050/sfp_is_present"
        port_ps = path.format(self._port_to_i2c_mapping[port_num])

          
        try:
            reg_file = open(port_ps)
        except IOError as e:
            print "Error: unable to open file: %s" % str(e)
            return False

        reg_value = reg_file.readline().rstrip()
        if reg_value == '1':
            return True

        return False
    
    def get_transceiver_change_event(self, timeout=0):
        raise NotImplementedError

    @property
    def port_start(self):
        return self._port_start

    @property
    def port_end(self):
        return self._port_end

    @property
    def qsfp_ports(self):
        return self._qsfp_ports

    @property 
    def port_to_eeprom_mapping(self):
         return self._port_to_eeprom_mapping
