# This file is executed on every boot (including wake-boot from deepsleep)

import gc, micropython, machine, ubinascii, esp
import network, utime
from utime import sleep, sleep_ms
from config import *

gc.collect()

if __debug__:
    def mpy_support():
        import sys
        sys_mpy = sys.implementation.mpy
        arch = [None, 'x86', 'x64',
            'armv6', 'armv6m', 'armv7m', 'armv7em', 'armv7emsp', 'armv7emdp',
            'xtensa', 'xtensawin'][sys_mpy >> 10]
        print('mpy version:', sys_mpy & 0xff)
        print('mpy flags:', end='')
        if arch:
            print(' -march=' + arch, end='')
        if sys_mpy & 0x100:
            print(' -mcache-lookup-bc', end='')
        if not sys_mpy & 0x200:
            print(' -mno-unicode', end='')
        print()

    mpy_support()


###############
# WiFi Config #
###############
dwifi = dcfg['wifi']
init_wifi = dcfg['init']['sta']
if not init_wifi:
    dcfg['hw']['id'] = '-'.join(['esp8266', ubinascii.hexlify(machine.unique_id()).decode()])
    dwifi['dhcp_hostname'] = dcfg['hw']['id']
    dcfg['init']['sta'] = True
    cfg(1)

# AP (Disable)
# TODO: Launch AP when init not complete for OTA configuration
ap = network.WLAN(network.AP_IF)
ap.active(False)
del ap

# Station
wlan = network.WLAN(network.STA_IF)  # create station interface
wlan.active(True)  # activate the interface

# Disconnect to reconnect with config.json info
if wlan.isconnected() and not init_wifi:
    wlan.disconnect()

if dwifi.get('essid', False) and dwifi.get('password', False):
    print('\nConnecting to wifi network.', end='')
    wlan.config(dhcp_hostname=dcfg['wifi'].get('dhcp_hostname', 'esp8266'))
    wlan.connect(dwifi['essid'], dwifi['password'])

    # Show connection status... until connected
    while not wlan.isconnected():
        print('.', end='')
        sleep_ms(500)
    print(' Connected!')

    # Print Network config
    print('network config:', wlan.ifconfig(), '\n')
del dwifi, dcfg

# FW & Mem
print('Firmware:')
esp.check_fw()
print('\nFree MEM: {}'.format(gc.mem_free()))

gc.collect()
