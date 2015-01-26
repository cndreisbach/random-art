import random
from math import pi, sin, cos, copysign

# Your job is to create better version of create_expression and
# run_expression to create random art.
# Your expression should have a __str__() function defined for it.

class Expression:
    methods = {"sin": { "weight": 3,
                        "method": lambda n, x, y: sin(pi * n) },
               "cos": { "weight": 3,
                        "method": lambda n, x, y: cos(pi * n) },
               "avgx": { "weight": 1,
                         "method": lambda n, x, y: (x + n) / 2 },
               "avgy": { "weight": 1,
                         "method": lambda n, x, y: (y + n) / 2 },
               "square": { "weight": 1,
                           "method": lambda n, x, y: pow(n, 2) },
               "cube": { "weight": 2,
                         "method": lambda n, x, y: pow(n, 3) },
               "prodx": { "weight": 1,
                          "method": lambda n, x, y: x * n },
               "prody": { "weight": 1,
                          "method": lambda n, x, y: y * n },
               "neg": { "weight": 1,
                        "method": lambda n, x, y: -n },
               "extreme": { "weight": 2,
                            "method": lambda n, x, y: copysign(1, n) }}

    def __init__(self):
        self.commands = []

    def random(self):
        fns = []
        for command, info in self.methods.items():
            fns.extend([command] * info["weight"])
        values = ["x", "y"]

        def generate_commands(depth=0):
            end_chance = depth * 0.05
            if random.random() < end_chance:
                return random.choice(values)
            else:
                return [random.choice(fns), generate_commands(depth + 1)]

        self.commands = generate_commands()
        return self

    def evaluate(self, x, y):
        def eval_commands(commands, x, y):
            if isinstance(commands, list):
                right_value = eval_commands(commands[1], x, y)
                return self.methods[commands[0]]["method"](right_value, x, y)
            elif isinstance(commands, str):
                return locals()[commands]
            else:
                return 0

        return eval_commands(self.commands, x, y)

    def __str__(self):
        return str(self.commands)


def create_expression():
    """This function takes no arguments and returns an expression that
    generates a number between -1.0 and 1.0, given x and y coordinates."""
    # expr = lambda x, y: (random.random() * 2) - 1
    # return expr

    expr = Expression().random()
    return expr

def run_expression(expr, x, y):
    """This function takes an expression created by create_expression and
    an x and y value. It runs the expression, passing the x and y values
    to it and returns a value between -1.0 and 1.0."""
    return expr.evaluate(x, y)
