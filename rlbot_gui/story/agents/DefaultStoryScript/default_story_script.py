import eel
import random
import time

from rlbot.matchconfig.match_config import MatchConfig
from rlbot.utils.game_state_util import GameState, CarState
from rlbot.parsing.match_settings_config_parser import rumble_mutator_types, boost_amount_mutator_types, game_mode_types
from rlbot.utils.structures.game_data_struct import GameTickPacket

from rlbot_gui.story.agents.base_story_script import BaseStoryScript


class DefaultStoryScript(BaseStoryScript):
    def __init__(self):
        super().__init__("Default Story Script")
        self.index = random.randint(0, 1e5)

    @staticmethod
    def edit_match_config(match_config: MatchConfig, challenge, upgrades):
        if challenge.get("limitations", []).count("half-field"):
            match_config.game_mode = game_mode_types[5]  # Heatseeker
        match_config.mutators.max_score = challenge.get("max_score")

        if challenge.get("disabledBoost"):
            match_config.mutators.boost_amount = boost_amount_mutator_types[4]  # No boost

        if "rumble" in upgrades:
            match_config.mutators.rumble = rumble_mutator_types[1]  # All rumble

    def run(self):
        max_boost = 0
        if "boost-100" in self.upgrades:
            max_boost = 100
        elif "boost-33" in self.upgrades:
            max_boost = 33

        half_field = self.challenge.get("limitations", []).count("half-field") > 0
        last_boost_bump_time = time.monotonic()
        while True:
            eel.sleep(0)  # yield to allow other gui threads to operate.
            packet = GameTickPacket()
            self.game_interface.fresh_live_data_packet(
                packet, 1000, self.index
            )

            human_info = packet.game_cars[0]
            game_state = GameState()
            human_desired_state = CarState()
            game_state.cars = {0: human_desired_state}

            changed = False
            # adjust boost
            if human_info.boost > max_boost and not half_field:
                # Adjust boost, unless in heatseeker mode
                human_desired_state.boost_amount = max_boost
                changed = True

            if "boost-recharge" in self.upgrades:
                # increase boost at 10% per second
                now = time.monotonic()
                if human_info.boost < max_boost and (now - last_boost_bump_time > 0.1):
                    changed = True
                    last_boost_bump_time = now
                    human_desired_state.boost_amount = min(human_info.boost + 1, max_boost)

            if changed:
                self.set_game_state(game_state)


if __name__ == "__main__":
    default_story_script = DefaultStoryScript()
    default_story_script.run()
