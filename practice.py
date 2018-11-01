import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.constants import NEXUS, PROBE, PYLON
from sc2.player import Bot, Computer

class RectagonBot(sc2.BotAI) : 
    async def on_step (self, iteration) : 
        # what to do every step
        await self.distribute_workers() # in sc2/bot_ai.py
        await self.build_workers()  # our own bot for worker
        await self.build_pylons()

    async def build_workers(self) :
        # nexus is command center in sc2
        # probe is worker in sc2
        
        # check if nexus is already build and does not create
        # anything.
        for nexus in self.units(NEXUS).ready.noqueue :
            # And then check if there is enough recource to create probe
            if self.can_afford(PROBE) :
                # create the probe
                await self.do(nexus.train(PROBE))
    
    async def build_pylons(self) :
        # pylon is supply in sc2.
        # we need to create it to expand our army

        if self.supply_left < 3 and not self.already_pending(PYLON) : 
            nexuses = self.units(NEXUS).ready

            if self.can_afford(PYLON) : 
                await self.build(PYLON, near=nexuses.first)

run_game(
    maps.get("PaladinoTerminalLE"),
    [Bot(Race.Protoss, RectagonBot()),
    Computer(Race.Terran, Difficulty.Easy)],
    realtime=True
)