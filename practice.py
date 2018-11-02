import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.constants import NEXUS, PROBE, PYLON, ASSIMILATOR
from sc2.player import Bot, Computer

class RectagonBot(sc2.BotAI) : 
    async def on_step (self, iteration) : 
        # what to do every step
        await self.distribute_workers() # in sc2/bot_ai.py
        await self.build_workers()  # our own bot for worker
        await self.build_pylons() # build supply
        await self.expand() # expand base
        await self.build_assimilators() # build the gas-getter building
        

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

        if self.supply_left < 6 and not self.already_pending(PYLON) : 
            nexuses = self.units(NEXUS).ready

            if self.can_afford(PYLON) : 
                await self.build(PYLON, near=nexuses.first)

    async def expand(self) :
        if self.units(NEXUS).amount < 2 and self.can_afford(NEXUS) :
            await self.expand_now()

    async def build_assimilators(self) :
        for nexus in self.units(NEXUS).ready :
            vespenes = self.state.vespene_geyser.closer_than(25.0, nexus)

            for vespene in vespenes :
                if not self.can_afford(ASSIMILATOR) :
                    break
                
                worker = self.select_build_worker(vespene.position)
                if worker is None :
                    break
                
                if not self.units(ASSIMILATOR).closer_than(1.0, vespene).exists :
                    await self.do(worker.build(ASSIMILATOR, vespene))

run_game(
    maps.get("PaladinoTerminalLE"),
    [Bot(Race.Protoss, RectagonBot()),
    Computer(Race.Terran, Difficulty.Easy)],
    realtime=True
)