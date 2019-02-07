# The MIT License (MIT)
#
# Copyright (c) 2019 Kattni Rembor for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_vcnl4040`
================================================================================

A CircuitPython library for the VCNL4040 proximity and ambient light sensor.


* Author(s): Kattni Rembor

Implementation Notes
--------------------

**Hardware:**

.. * `Adafruit VCNL4040 <url>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases


 * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
 * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

from micropython import const
import adafruit_bus_device.i2c_device as i2c_device
from adafruit_register.i2c_struct import Struct, UnaryStruct
from adafruit_register.i2c_bit import RWBit

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_VCNL4040.git"


_ALS_THDH_LM = const(0x01)  # ALS high interrupt threshold
_ALS_THDL_LM = const(0x02)  # ALS low interrupt threshold
_PS_CONF2 = const(0x03)  # PS output resolution selection, interrupt trigger method
_PS_CONF3 = const(0x04)  # PS smart persistence, active force mode
_PS_MS = const(0x04)  # White channel enable/disable, PS mode, PS protection setting, LED current
_PS_CANC_LM = const(0x05)  # PS cancellation level setting
_PS_THDH_LM = const(0x06)  # PS low interrupt threshold setting
_PS_THDL_LM = const(0x07)  # PS high interrupt threshold setting
_INT_Flag = const(0x0B)  # ALS, PS interrupt flags


class VCNL4040:
    # ID_LM - Device ID, address
    _device_id = UnaryStruct(0x0C, "<H")
    """Docs"""

    # PS_Data_LM - PS output data
    proximity = UnaryStruct(0x08, ">H")

    # PS_CONF1 - PS duty ratio, integration time, persistence, enable/disable
    proximity_settings = UnaryStruct(0x03, ">H")

    # ALS_Data_LM - ALS output data
    light = UnaryStruct(0x09, ">H")

    # ALS_CONF - ALS integration time, persistence, interrupt, function enable/disable
    light_settings = UnaryStruct(0x00, ">H")

    # White_Data_LM - White output data
    white = UnaryStruct(0x0A, ">H")

    white_enable = UnaryStruct(0x04, ">H")

    def __init__(self, i2c, address=0x60):
        self.i2c_device = i2c_device.I2CDevice(i2c, address)
        if self._device_id != 0x186:
            raise RuntimeError("Failed to find VCNL4040 - check wiring!")
        self.proximity_settings = 0x0001
        self.light_settings = 0x0001
        self.white_enable = 0x1000

