import sys
import ncs
from ncs.application import Service



with ncs.maapi.Maapi() as m:
     with ncs.maapi.Session(m, 'admin', 'python'):
             with m.start_read_trans() as t:
                     root = ncs.maagic.get_root(t)
                     ping = root.devices.device['R3'].live_status.cisco_ios_xr_stats__exec.any
             ping_input = ping.get_input()
             ping_input.args = ["show ip int brief"]
             ping_output = ping(ping_input)
             print type(ping_output)
             print type(ping_output.result)
             print ping_output
             result=ping_output.result

print result