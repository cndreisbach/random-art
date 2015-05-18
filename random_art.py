import random
from math import pi, sin, cos, copysign, fabs

# Your job is to create better version of create_expression and
# run_expression to create random art.
# Your expression should have a __str__() function defined for it.

class Expression:
    methods = {"sin": { "weight": 10,
                        "method": lambda n: sin(pi * n) },
               "cos": { "weight": 10,
                        "method": lambda n: cos(pi * n) },
               "avg": { "weight": 7,
                        "arity": 2,
                        "method": lambda m, n: (m + n) / 2 },
               "sincos": { "method":
                   lambda n: sin(pi * n) if n < 0 else cos(pi * n) },
               "cossin": { "method":
                   lambda n: sin(pi * n) if n > 0 else cos(pi * n) },
               "sqrt": { "method": lambda n: copysign(pow(fabs(n), 0.5), n)},
               "square": { "method": lambda n: pow(n, 2) },
               "cube": { "weight": 1,
                         "method": lambda n: pow(n, 3) },
               "prod": { "arity": 2,
                         "method": lambda m, n: m * n },
               "half": { "method": lambda n: n / 2 },
               "double": { "method":
                   lambda n: n * 2 if fabs(n) < 0.5 else n },
               "neg": { "method": lambda n: -n },
               "flip": { "method": lambda n: copysign(1 - fabs(n), -n) },
               "invert": { "method":
                   lambda n: copysign((1 / n) % 1, n) if n != 0 else n },
               "shiftleft": { "method": lambda n: (10 * n) % 1 },
               "shiftright": { "method": lambda n: n / 10 },
               "rotate": { "method":
                   lambda n: n - 1 if n > 0 else n + 1 },
               "extreme": { "method": lambda n: copysign(1, n) }}


    def __init__(self):
        self.commands = []

    def random(self):
        fns = []
        for command, info in self.methods.items():
            fns.extend([command] * info.get("weight", 1))
        fns.sort()

        # values = ["x", "y", "x", "y", "rand"]
        values = ["x", "y"]

        def generate_commands(depth=0):
            end_chance = 1 - pow(0.95, depth)
            if random.random() < end_chance:
                return random.choice(values)
            else:
                fn = random.choice(fns)
                commands = [fn]
                for _ in range(self.methods[fn].get("arity", 1)):
                    commands.append(generate_commands(depth + 1))
                return commands

        self.commands = generate_commands()
        return self

    def evaluate(self, x, y):
        def eval_commands(commands, x, y):
            if isinstance(commands, list):
                args = [eval_commands(command, x, y) for command in commands[1:]]
                return self.methods[commands[0]]["method"](*args)
            elif isinstance(commands, str):
                rand = random.random()
                return locals()[commands]
            else:
                return 0

        return eval_commands(self.commands, x, y)

    def __str__(self):
        def sexp(commands):
            if isinstance(commands, list):
                return "({})".format(" ".join(sexp(command) for command in commands))
            else:
                return str(commands)

        return sexp(self.commands)


def create_expression():
    """This function takes no arguments and returns an expression that
    generates a number between -1.0 and 1.0, given x and y coordinates."""
    expr = Expression().random()
    return expr

def run_expression(expr, x, y):
    """This function takes an expression created by create_expression and
    an x and y value. It runs the expression, passing the x and y values
    to it and returns a value between -1.0 and 1.0."""
    return expr.evaluate(x, y)
