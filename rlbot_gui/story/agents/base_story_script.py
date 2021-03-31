import sys
import ast

from rlbot.agents.base_script import BaseScript
from rlbot.matchconfig.match_config import MatchConfig

SCRIPT_FILE_KEY = "script_file"


class BaseStoryScript(BaseScript):
    """
    A convenience class for building story scripts on top of.
    It is NOT required to use this when configuring a story script.
    """

    def __init__(self, name):
        super().__init__(name)

        try:
            pos = sys.argv.index("--challenge")
            challenge_string = sys.argv[pos + 1]
        except (ValueError, IndexError):
            # Missing the command line argument.
            pass
        else:
            self.challenge = ast.literal_eval(challenge_string)

        try:
            pos = sys.argv.index("--upgrades")
            upgrades_string = sys.argv[pos + 1]
        except (ValueError, IndexError):
            # Missing the command line argument.
            pass
        else:
            self.upgrades = ast.literal_eval(upgrades_string)

    @staticmethod
    def edit_match_config(match_config: MatchConfig, challenge: dict, upgrades: list):
        """
        Change the MatchConfig used to start the story challenge.

        :param match_config: The reference to the MatchConfig.
        :param challenge: The challenge dictionary.
        :param upgrades: The list of enabled upgrades.
        """
        pass
