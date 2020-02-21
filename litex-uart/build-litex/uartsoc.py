#!/usr/bin/env python3

# This file is Copyright (c) 2015-2019 Florent Kermarrec <florent@enjoy-digital.fr>
# License: BSD

import argparse

from migen import *
from migen.genlib.resetsync import AsyncResetSynchronizer

from litex_boards.platforms import arty

from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *
from litex.soc.interconnect import wishbone

from litex.soc.cores.pwm import *
from litex.build.generic_platform import *

# ExtractSoC ------------------------------------------------------------------------------------------

class BaseSoC(SoCMini):
    SoCMini.mem_map["csr"] = 0x00000000
    def __init__(self, sys_clk_freq=int(100e6), with_uart=True, with_pwm=False, **kwargs):

        platform = arty.Platform()

        kwargs["with_uart"] = with_uart
        kwargs["with_ctrl"] = False

        # CRG --------------------------------------------------------------------------------------
        platform.add_extension([("rst", 0, Pins(1))])
        self.submodules.crg = CRG(platform.request(platform.default_clk_name), rst=platform.request("rst", 0))

        # SoCMini ---------------------------------------------------------------------------------
        SoCMini.__init__(self, platform, clk_freq=sys_clk_freq, **kwargs)

        if with_pwm:
            platform.add_extension([("pwm", 0, Pins(1))])

            pwm_s = Signal()
            pwm_m = PWM(pwm_s)

            self.submodules.pwm = pwm_m
            self.add_csr('pwm')

            self.comb += platform.request("pwm", 0).eq(pwm_s)

        self.wb_bus = wishbone.Interface(32, 17)
        self.bus.add_master(name="wb_master", master=self.wb_bus)

        self.wb_bus.connect_to_pads(self, platform, 'wb', mode='slave')

        for name, loc in sorted(self.irq.locs.items()):
            module = getattr(self, name)
            platform.add_extension([("irq_"+name, 0, Pins(1))])
            irq_pin = platform.request("irq_"+name, 0)
            self.comb += irq_pin.eq(module.ev.irq)

# Build --------------------------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="LiteX SoC")
    builder_args(parser)
    soc_mini_args(parser)
    args = parser.parse_args()

    soc = BaseSoC(**soc_mini_argdict(args))
    builder = Builder(soc, **builder_argdict(args))
    builder.build()


if __name__ == "__main__":
    main()
