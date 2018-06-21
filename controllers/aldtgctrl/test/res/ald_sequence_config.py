"""Each valve configuration, e.g. valve_1_conf, valve2_conf
is a list of dictionaries where each dictionary represents
one aperture of the valve.

The valve's aperture is described by the Initial configuration
(time in seconds from the start of the sequence) and the
Active configuration (time in seconds during which the valve
should be opened).
"""

from sardana.pool import SynchDomain, SynchParam 

Initial = SynchParam.Initial
Active = SynchParam.Active
Time = SynchDomain.Time


valve1_conf = [
    {
        Initial: {Time: 1},
        Active:  {Time: 0.3}
    },
    {
        Initial: {Time: 5},
        Active:  {Time: 0.3}
    }
]

valve2_conf = [
    {
        Initial: {Time: 1},
        Active:  {Time: 0.5}
    }
]

valve3_conf = [
    {
        Initial: {Time: 20},
        Active:  {Time: 0.5}
    }
]

valve4_conf = [
    {
        Initial: {Time: 21},
        Active:  {Time: 0.3}
    },
    {
        Initial: {Time: 25},
        Active:  {Time: 0.3}
    }
]
