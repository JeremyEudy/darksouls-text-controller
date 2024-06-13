from random import choice
import vgamepad as vg


class MultiKeyDict():
    def __init__(self, **kwargs):
        self._keys


class Controller(vg.VX350Gamepad):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active_commands = []
        self.command_map = {
            ("forward", "run", "go"): self.forward(),
            ("backward", "run away", "flee", "bounce"): self.backward(),
            ("stop", "halt"): self.stop(),
            ("roll"): self.roll(),
            ("back", "backstep"): self.backstep(),
            ("sprint", "dash"): self.sprint(),
            ("jump"): self.jump(),
            ("right", "look right"): self.look_right(),
            ("left", "look left"): self.look_left(),
            ("turn"): self.turn(),
            ("lock-on", "lock", "lock on"): self.lock(),
            ("light attack", "swing", "hit"): self.light_attack(),
            ("heavy attack", "big swing"): self.heavy_attack(),
            ("attack"): self.attack(),
            ("charge attack"): self.charge_attack(),
            ("spell", "magic", "pray"): self.spell(),
            ("interact", "take", "pickup", "grab", "talk", "talk to", "speak"): self.interact(),
            ("use item", "use", "heal"): self.use_item(),
        }

    def execute_command(self, command):
        for shortcuts, method in self.command_map.items():
            if command in shortcuts:
                method()
                break

    def forward(self):
        self.left_joystick(x_value=0, y_value=-32768)
        self.active_commands.append("forward")

    def backward(self):
        self.left_joystick(x_value=0, y_value=32768)
        self.active_commands.append("backward")

    def stop(self):
        if len(self.active_commands) > 0:
            self.left_joystick(x_value=0, y_value=0)
            self.active_commands = []
        else:
            print("You aren't moving!")

    def turn(self):
        # BEHOLD MY SIN
        [self.left, self.right][choice([0, 1])]()

    def attack(self):
        # BEHOLD MY SIN
        [self.light_attack, self.heavy_attack][choice([0, 1])]()


def game_loop():
    gamepad = Controller()
    print("Welcome to Game to TRPG, the tool no one asked for which makes your life harder. For FUN!")
    print("Enter a command below, or type help for a symblance of guidance")
    while True:
        command = input(">").lower()
        if command == "help":
            print("""
Commands:
    - Movement:
        - forward: run, go
        - backward: run away, flee, bounce
        - stop: halt
        - roll
        - back: backstep
        - run: sprint, dash
        - jump

    - View:
        - right: turn (50% chance)
        - left: turn (50% chance)
        - lock-on: lock, lock on

    - Combat:
        - light attack: attack (50% chance), swing, hit
        - heavy attack: attack (50% chance), big swing
        - spell: magic, pray

    - General:
        - interact: take, pickup, grab, talk, talk to, speak
        - use item: use, heal
            """)
            continue
        elif command not in gamepad.command_map:
            print("Invalid command!")
            continue


if __name__ == "__main__":
    game_loop()
