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

import adafruit_bus_device.i2c_device as i2c_device
from adafruit_register.i2c_struct import UnaryStruct, ROUnaryStruct
from adafruit_register.i2c_bits import RWBits, ROBits
from adafruit_register.i2c_bit import RWBit, ROBit
import digitalio

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_VCNL4040.git"


class VCNL4040:
    # ID_LM - Device ID, address
    _device_id = UnaryStruct(0x0C, "<H")
    """The device ID"""

    # PS_Data_LM - PS output data
    proximity = ROUnaryStruct(0x08, "<H")
    """The proximity data"""

    # PS_CONF1 - PS duty ratio, integration time, persistence, enable/disable
    # PS_CONF2 - PS output resolution selection, interrupt trigger method
    # PS_CONF3 - PS smart persistence, active force mode
    proximity_shutdown = RWBit(0x03, 0, register_width=2)
    """Proximity sensor shutdown. When True, proximity data is disabled."""
    proximity_persistence = RWBits(3, 0x03, 1, register_width=2)
    proximity_smart_persistence = RWBit(0x04, 4, register_width=2)
    proximity_interrupt = RWBits(2, 0x03, 8, register_width=2)
    """Interrupt enable. (0:0) disable. (0:1) trigger when close, 
    (1:0) trigger when away, (1:1) trigger when close or away"""
    proximity_cancellation_level = UnaryStruct(0x05, "<H")

    # PS_THDL_LM - PS low interrupt threshold setting
    proximity_low_threshold = UnaryStruct(0x06, "<H")
    # PS_THDH_LM - PS high interrupt threshold setting
    proximity_high_threshold = UnaryStruct(0x07, "<H")
    # INT_FLAG - PS interrupt flag
    proximity_high_interrupt = ROBit(0x0B, 9, register_width=2)
    """If close: proximity rises above high threshold interrupt trigger event"""
    proximity_low_interrupt = ROBit(0x0B, 8, register_width=2)
    """If away: proximity drops below low threshold trigger event"""

    # ALS_Data_LM - ALS output data
    light = ROUnaryStruct(0x09, "<H")
    """Ambient light data"""

    # ALS_CONF - ALS integration time, persistence, interrupt, function enable/disable
    light_settings = UnaryStruct(0x00, "<H")
    light_shutdown = RWBit(0x00, 0, register_width=2)
    """Ambient light sensor shutdown. When True, ambient light data is disabled."""

    # ALS_THDL_LM - ALS low interrupt threshold setting
    light_low_threshold = UnaryStruct(0x02, "<H")
    # ALS_THDH_LM - ALS high interrupt threshold setting
    light_high_threshold = UnaryStruct(0x01, "<H")
    # INT_FLAG - ALS interrupt flag
    light_high_interrupt = ROBit(0x0B, 12, register_width=2)
    """If high: ambient light sensor crosses high interrupt threshold trigger event"""
    light_low_interrupt = ROBit(0x0B, 13, register_width=2)
    """If low: ambient light sensor crosses low interrupt threshold trigger event"""

    # White_Data_LM - White output data
    white = ROUnaryStruct(0x0A, "<H")
    """White light data"""

    # PS_MS - White channel enable/disable, PS mode, PS protection setting, LED current
    # White_EN - PS_MS_H, 7th bit - White channel enable/disable
    # white_enable = RWBit(0x04, 15, register_width=2)

    def __init__(self, i2c, address=0x60, interrupt_pin=None):
        self.i2c_device = i2c_device.I2CDevice(i2c, address)
        if self._device_id != 0x186:
            raise RuntimeError("Failed to find VCNL4040 - check wiring!")

        self._interrupt_pin = interrupt_pin
        if self._interrupt_pin:
            self._interrupt_pin.switch_to_input(pull=digitalio.Pull.UP)

        self.proximity_shutdown = False
        self.light_shutdown = False
        # self.proximity_smart_persistence = True
        # self.white_enable = False
