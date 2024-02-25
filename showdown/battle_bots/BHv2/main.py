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
        if self.turn == 1:
            print("it's turn 1")
            if self.rqid > 3:
                print("not first move")
                if self.force_switch or not moves:
                    print("gotta switch (normal)")
                    return format_decision(self, switches[0])
            else:
                print("please boom turn 1")
                return format_decision(self, "selfdestruct")
        else:
            if self.force_switch or not moves:
                print("why am i here")
                return format_decision(self, switches[0])

        choice = None
        BoomUser = False
        # most_damage = -1
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
        if not BoomUser:
            past_move = self.user.last_used_move.move
            if past_move == "hiddenpower":
                choice = "hiddenpower"
            else:
                if self.user.active.name == "ninjask":
                    choice = "substitute"
                    if past_move == "substitute":
                        choice = "batonpass"
                    if constants.TAUNT in self.user.active.volatile_statuses:
                        choice = "aerialace"
                else:
                    #suicune block
                    choice = "calmmind"
                    if past_move == "calmmind":
                        if self.user.active.hp < 401:
                            choice = "rest"
                        else:
                            choice = "calmmind"
                    elif past_move == "rest":
                        choice = "sleeptalk"
                    elif past_move == "sleeptalk":
                        if self.user.active.moves[3].current_pp % 2 == 1:
                            choice = "sleeptalk"
                        else:
                            choice = "rest"
                    elif past_move == "surf":
                        if self.user.active.hp < 401:
                            choice = "rest"
                            self.user.restcount += 1
                            print("restcount...")
                            print(self.user.restcount)
                        else:
                            choice = "calmmind"
                    else:
                        print("FUCK")
                    if constants.TAUNT in self.user.active.volatile_statuses:
                        choice = "surf"
        print("self.user =")
        print(self.user)
        print("choice =")
        print(choice)
        print(format_decision(self, choice))
        return format_decision(self, choice)