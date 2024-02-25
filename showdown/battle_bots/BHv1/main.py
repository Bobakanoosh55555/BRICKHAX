import constants
from data import all_move_json
from showdown.battle import Battle
from showdown.engine.damage_calculator import calculate_damage
from showdown.engine.find_state_instructions import update_attacking_move
from ..helpers import format_decision


class BattleBot(Battle):
    def __init__(self, *args, **kwargs):
        super(BattleBot, self).__init__(*args, **kwargs)

    def find_best_move(self):
        state = self.create_state()
        my_options = self.get_all_options()[0]

        moves = []
        switches = []
        for option in my_options:
            if option.startswith(constants.SWITCH_STRING + " "):
                switches.append(option)
            else:
                moves.append(option)

        choice = None
        BoomUser = False
        most_damage = -1
        for move in moves:
            if move == "explosion" or move == "selfdestruct":
                BoomUser = True
                damage_amounts = calculate_damage(state, constants.USER, move, constants.DO_NOTHING_MOVE)
                damage = damage_amounts[0] if damage_amounts else 0
                if damage > 0:
                    choice = move
                    print("should boom")
                else:
                    print("should HP Ghost")
                    choice = "hiddenpower"
        Me = self.user
        if not BoomUser:
            past_move = Me.last_used_move.move
            if past_move == "hiddenpower":
                choice = "hiddenpower"
            else:
                if Me.active.name == "ninjask":
                    choice = "substitute"
                    if past_move == "substitute":
                        choice = "batonpass"
                else:
                    #suicune block
                    choice = "calmmind"
                    if past_move == "calmmind" or past_move == "surf":
                        choice = "surf"
            # if choice == None:
            #     damage_amounts = calculate_damage(state, constants.USER, move, constants.DO_NOTHING_MOVE)
            #     damage = damage_amounts[0] if damage_amounts else 0
            #     if damage > most_damage:
            #         choice = move
            #         most_damage = damage
        print("self.user =")
        print(self.user)
        print("choice =")
        print(choice)
        print(format_decision(self, choice))
        if self.force_switch or not moves:
            return format_decision(self, switches[0])
        return format_decision(self, choice)