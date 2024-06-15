import time
from random import choice

import vgamepad as vg
from pynput import keyboard


class Controller(vg.VX360Gamepad):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active_commands = []
        self.command_map = {
            ("forward", "run", "go"): self.forward,
            ("backward", "run away", "flee", "bounce"): self.backward,
            ("stop", "halt"): self.stop,
            # ("roll"): self.roll,
            # ("back", "backstep"): self.backstep,
            # ("sprint", "dash"): self.sprint,
            # ("jump"): self.jump,
            ("right", "look right"): self.right,
            ("left", "look left"): self.left,
            ("up", "look up"): self.up,
            ("down", "look down"): self.down,
            ("turn"): self.turn,
            # ("lock-on", "lock", "lock on"): self.lock,
            ("light attack", "swing", "hit"): self.light_attack,
            ("heavy attack", "big swing"): self.heavy_attack,
            ("attack"): self.attack,
            ("charge attack"): self.charge_attack,
            # ("spell", "magic", "pray"): self.spell,
            # ("interact", "take", "pickup", "grab", "talk", "talk to", "speak"): self.interact,
            # ("use item", "use", "heal"): self.use_item,
        }

    def execute_command(self, command):
        for shortcuts, method in self.command_map.items():
            if command in shortcuts:
                method()
                self.update()
                return
        print("Invalid command!")

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

    def left(self):
        self.right_joystick(x_value=-32768, y_value=0)

    def right(self):
        self.right_joystick(x_value=32768, y_value=0)

    def up(self):
        self.right_joystick(x_value=0, y_value=32768)

    def down(self):
        self.right_joystick(x_value=0, y_value=-32768)

    def attack(self):
        # BEHOLD MY SIN
        [self.light_attack, self.heavy_attack][choice([0, 1])]()

    def light_attack(self):
        self.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
        self.update()
        self.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)

    def heavy_attack(self):
        self.right_trigger(value=255)
        self.update()
        self.right_trigger(value=0)

    def charge_attack(self):
        self.right_trigger(value=255)
        self.update()
        time.sleep(5)
        self.right_trigger(value=255)


COMMAND = []
CONTROLLER = Controller()


def on_press(key):
    global COMMAND
    global CONTROLLER
    try:
        COMMAND.append(key.char)
    except AttributeError:
        if key == keyboard.Key.space:
            COMMAND.append(" ")
        elif key == keyboard.Key.enter:
            str_command = "".join(COMMAND)
            if str_command == "help":
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
        - right: look right, turn (50% chance)
        - left: look left, turn (50% chance)
        - up: look up
        - down: look down
        - lock-on: lock, lock on

    - Combat:
        - light attack: attack (50% chance), swing, hit
        - heavy attack: attack (50% chance), big swing
        - spell: magic, pray

    - General:
        - interact: take, pickup, grab, talk, talk to, speak
        - use item: use, heal
                """)
            elif str_command == "quit" or str_command == "exit":
                print("Thank you for ending your suffering")
                return False
            else:
                print(f"Submitted command: {str_command}")
                CONTROLLER.execute_command(str_command)
            COMMAND = []
        elif key == keyboard.Key.esc:
            return False


def splash():
    print("Welcome to Game to TRPG, the tool no one asked for which makes your life harder. For FUN!")
    print("Enter a command below, or type help for a semblance of guidance")


if __name__ == "__main__":
    splash()
    with keyboard.Listener(
        on_press=on_press
    ) as listener:
        listener.join()
    # listener = keyboard.Listener(
    #     on_press=on_press
    # )
    # listener.start()
