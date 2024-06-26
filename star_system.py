import random

import constants as const


class StarSystem:

    def __init__(self, name, x, y, size, tech_level, political_system_type, system_pressure):
        self.name = name
        self.x = x
        self.y = y
        self.size = size
        self.tech_level = tech_level
        self.political_system_type = political_system_type
        self.system_pressure = system_pressure
        self.special_resource = None
        self.quest_system = False
        self.trade_items = [0] * 10
        self.count_down = 0
        self.visited = False
        self.shipyard_id = None

        self.initialize_trade_items()

    def get_location(self):
        return (self.x, self.y)

    def get_inventory(self):
        return self.trade_items

    def set_visited(self):
        self.visited = True

    def get_system_pressure(self):
        """
        System pressures:

        0 = under no particular pressure; Uneventful
        1 = at war; Ore and Weapons in demand
        2 = ravaged by a plague; Medicine in demand
        3 = suffering from a drought; Water in demand
        4 = suffering from extreme boredom; Games and Narcotics in demand
        5 = suffering from a cold spell; Furs in demand
        6 = suffering from a crop failure; Food in demand
        7 = lacking enough workers; Machinery and Robots in demand
        """
        return self.system_pressure

    def set_system_pressure(self, value):
        self.system_pressure = value

    """
    Political system types:
    
    """

    def set_political_system_type(self, value):
        self.political_system_type = value

    def get_political_system_type(self):
        return self.political_system_type

    def get_tech_level(self):
        """
        Tech levels:

        0 = Pre-Agricultural
        1 = Agricultural
        2 = Medieval
        3 = Renaissance
        4 = Early Industrial
        5 = Industrial
        6 = Post-Industrial
        7 = Hi-Tech
        """
        return self.tech_level

    def set_tech_level(self, value):
        self.tech_level = value

    def get_size(self):
        """
        System sizes:

        0 = Tiny
        1 = Small
        2 = Medium
        3 = Large
        4 = Huge
        5 = Gargantuan
        """
        return self.size

    # TODO maybe weight or limit this for things that make sense, i.e. medieval system can't be lifeless
    def get_special_resource(self):
        """
        Special resources:

        0 = Nothing Special
        1 = Mineral Rich
        2 = Mineral Poor
        3 = Desert
        4 = Sweetwater Oceans
        5 = Rich Soil
        6 = Poor Soil
        7 = Rich Fauna
        8 = Lifeless
        9 = Weird Mushrooms
        10 = Special Herbs
        11 = Artistic Populace
        12 = Warlike Populace
        """
        if self.visited:
            return self.special_resource
        else:
            self.special_resource = random.choice(const.SPECIALRESOURCES)
            return self.special_resource

    def initialize_trade_items(self):
        for i in range(len(Consts.TradeItems)):
            if not self.is_item_traded(Consts.TradeItems[i]):
                self.trade_items[i] = 0
            else:
                self.trade_items[i] = (self.size.cast_to_int() + 1) * (
                    random.randint(9, 14)
                    - abs(Consts.TradeItems[i].tech_top_production.cast_to_int() - self.tech_level.cast_to_int())
                )

                if i >= TradeItemType.NARCOTICS.cast_to_int():
                    self.trade_items[i] = (
                        (self.trade_items[i] * (5 - Game.current_game.difficulty_id))
                        / (6 - Game.current_game.difficulty_id)
                    ) + 1

                if self.special_resource == Consts.TradeItems[i].resource_low_price:
                    self.trade_items[i] = self.trade_items[i] * 4 / 3

                if self.special_resource == Consts.TradeItems[i].resource_high_price:
                    self.trade_items[i] = self.trade_items[i] * 3 / 4

                if self.system_pressure == Consts.TradeItems[i].pressure_price_hike:
                    self.trade_items[i] = self.trade_items[i] / 5

                self.trade_items[i] = self.trade_items[i] - random.randint(10) + random.randint(10)

                if self.trade_items[i] < 0:
                    self.trade_items[i] = 0

    def is_item_traded(self, item):
        return (
            (item.item_type != TradeItemType.NARCOTICS or self.get_political_system().is_drugs_ok())
            and (item.item_type != TradeItemType.FIREARMS or self.get_political_system().is_firearms_ok())
            and self.tech_level.cast_to_int() >= item.tech_production.cast_to_int()
        )

    def item_used(self, item):
        return (
            (item.item_type != TradeItemType.NARCOTICS or self.get_political_system().is_drugs_ok())
            and (item.item_type != TradeItemType.FIREARMS or self.get_political_system().is_firearms_ok())
            and self.tech_level.cast_to_int() >= item.tech_usage.cast_to_int()
        )

    def dest_is_ok(self):
        comm = Game.current_game.commander
        return self != comm.current_system and (
            self.get_distance() <= comm.ship.fuel or Functions.wormhole_exists(comm.current_system, self)
        )

    def get_distance(self):
        return Functions.distance(self, Game.current_game.commander.current_system)

    def get_mercenaries_for_hire(self):
        cmdr = Game.current_game.commander
        return [
            merc
            for merc in Game.current_game.mercenaries.values()
            if merc.is_mercenary() and merc.current_system == cmdr.current_system and not cmdr.ship.has_crew(merc.id)
        ]

    def is_quest_system(self):
        return self.quest_system

    def set_quest_system(self, value):
        self.quest_system = value
