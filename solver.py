import argparse
import logging
import math
import json

from utils import extract_nargs


def log(arg0):
    return math.log(arg0)


def sqrt(arg0):
    return math.sqrt(arg0)


def floor(arg0):
    return math.floor(arg0)


def square_area(arg0):
    return arg0 * arg0


def circle_area(arg0):
    return math.pi * arg0 * arg0


def circumface(arg0):
    return 2.0 * math.pi * arg0


def inverse(arg0):
    return 1.0 / arg0


def negate(arg0):
    return -arg0


def cube_edge_by_volume(arg0):
    return arg0 ** (1/3)


def volume_cube(arg0):
    return arg0 ** 3


def factorial(arg0):
    if arg0 < 0:
        raise ValueError("Input to factorial " + arg0 + " is negative.")
    if arg0 > 50:
        raise ValueError("Input to factorial " + arg0 + " too large.")
    return math.factorial(arg0)


def square_perimeter(arg0):
    return 4 * arg0


def square_edge_by_perimeter(arg0):
    return arg0 / 4


def square_edge_by_area(arg0):
    return arg0 ** (1/2)


def surface_sphere(arg0):
    return 4 * math.pi * arg0 * arg0


def volume_sphere(arg0):
    return 4 / 3 * math.pi * (arg0 ** 3)


def rhombus_perimeter(arg0):
    return 4 * arg0


def negate_prob(arg0):
    assert 0 <= arg0 <= 1
    return 1 - arg0


def tangent(arg0):
    return math.tan(arg0)


def sine(arg0):
    return math.sin(arg0)


def cosine(arg0):
    return math.cos(arg0)


def surface_cube(arg0):
    return 6 * arg0 * arg0


def add(arg0, arg1):
    return arg0 + arg1


def subtract(arg0, arg1):
    return arg0 - arg1


def multiply(arg0, arg1):
    return arg0 * arg1


def divide(arg0, arg1):
    return arg0 / arg1


def amax(arg0, arg1):
    return max(arg0, arg1)


def amin(arg0, arg1):
    return min(arg0, arg1)


def power(arg0, arg1):
    return arg0 ** arg1


def speed(arg0, arg1):
    return arg0 / arg1


def choose(arg0, arg1):
    #return math.factorial(arg0) / math.factorial(arg1) / math.factorial(arg0 - arg1)
    return math.comb(arg0, arg1)


def rectangle_perimeter(arg0, arg1):
    return 2 * (arg0 + arg1)


def surface_cylinder(arg0, arg1):
    return 2 * math.pi * arg0 * (arg0 + arg1)


def remainder(arg0, arg1):
    return divmod(arg0, arg1)[1]


def original_price_before_loss(arg0, arg1):
    assert 0 < (100 - arg0) <= 100
    return 100 / (100 - arg0) * arg1


def original_price_before_gain(arg0, arg1):
    return 100 / (100 + arg0) * arg1


def lcm(arg0, arg1):
    return abs(arg0 * arg1) // math.gcd(int(arg0), int(arg1))


def rectangle_area(arg0, arg1):
    return arg0 * arg1


def rhombus_area(arg0, arg1):
    return arg0 * arg1 / 2


def volume_cylinder(arg0, arg1):
    return math.pi * arg0 * arg0 * arg1


def triangle_area(arg0, arg1):
    return arg0 * arg1 / 2


def gcd(arg0, arg1):
    return math.gcd(int(arg0), int(arg1))


# contentious definition
def p_after_gain(arg0, arg1):
    return arg0 / 100 * arg1


def permutation(arg0, arg1):
    assert (arg0 - arg1) >= 0
    return math.factorial(arg0) / math.factorial(arg0 - arg1)


def diagonal(arg0, arg1):
    return (arg0 ** 2 + arg1 ** 2) ** (1/2)


def volume_cone(arg0, arg1):
    return math.pi / 3 * arg0 * arg0 * arg1


def stream_speed(arg0, arg1):
    return (arg0 + arg1) / 2


# contentious definition
def speed_in_still_water(arg0, arg1):
    return arg0 * arg1 * 2


def volume_rectangular_prism(arg0, arg1, arg2):
    return arg0 * arg1 * arg2


def triangle_area_three_edges(arg0, arg1, arg2):
    peri = (arg0 + arg1 + arg2) / 2
    return (peri * (peri - arg0) * (peri - arg1) * (peri - arg2)) ** (1/2)


def quadrilateral_area(arg0, arg1, arg2):
    return arg0 * (arg1 + arg2) / 2


def triangle_perimeter(arg0, arg1, arg2):
    return arg0 + arg1 + arg2


def surface_rectangular_prism(arg0, arg1, arg2):
    return 2 * (arg0 * arg1 + arg1 * arg2 + arg0 * arg2)


function_switch = {
        "volume_rectangular_prism": volume_rectangular_prism,
        "triangle_area_three_edges": triangle_area_three_edges,
        "quadrilateral_area": quadrilateral_area,
        "triangle_perimeter": triangle_perimeter,
        "surface_rectangular_prism": surface_rectangular_prism,
        "multiply": multiply,
        "divide": divide,
        "add": add,
        "subtract": subtract,
        "power": power,
        "speed": speed,
        "choose": choose,
        "rectangle_perimeter": rectangle_perimeter,
        "surface_cylinder": surface_cylinder,
        "reminder": remainder,  # spelling wrong to map to dataset error
        "original_price_before_loss": original_price_before_loss,
        "lcm": lcm,
        "rectangle_area": rectangle_area,
        "rhombus_area": rhombus_area,
        "volume_cylinder": volume_cylinder,
        "triangle_area": triangle_area,
        "gcd": gcd,
        "p_after_gain": p_after_gain,
        "permutation": permutation,
        "max": amax,
        "diagonal": diagonal,
        "original_price_before_gain": original_price_before_gain,
        "volume_cone": volume_cone,
        "min": amin,
        "stream_speed": stream_speed,
        "speed_in_still_water": speed_in_still_water,
        "sqrt": sqrt,
        "floor": floor,
        "log": log,
        "square_area": square_area,
        "circle_area": circle_area,
        "circumface": circumface, # I think this is circumference, but well..
        "inverse": inverse,
        "negate": negate,
        "cube_edge_by_volume": cube_edge_by_volume,
        "surface_cube": surface_cube,
        "volume_cube": volume_cube,
        "factorial": factorial,
        "square_perimeter": square_perimeter,
        "square_edge_by_perimeter": square_edge_by_perimeter,
        "square_edge_by_area": square_edge_by_area,
        "surface_sphere": surface_sphere,
        "volume_sphere": volume_sphere,
        "rhombus_perimeter": rhombus_perimeter,
        "negate_prob": negate_prob,
        "tangent": tangent,
        "sine": sine,
        "cosine": cosine,
    }


def get_op_and_args(token):
    """
    Take an operation e.g. add(n0, const_4) and break it into the operator and argument list
    :param token: program operation e.g. add(n0, const_4)
    :return: (operation, argument list)
    """
    lindex = token.find("(")
    rindex = token.find(")")
    op = token[:lindex].strip()
    args = [t.strip() for t in token[lindex+1:rindex].split(",")]
    return op, args


def evaluate_args(args, memory):
    """
    Evaluates the arguments by evaluating constants and # variables placeholders from the memory bank.
    Assumes that all the n variables have been preprocessed away.
    :param args: argument list
    :param memory: memory bank
    :return: processed arguments list
    """

    ret_args = []
    for arg in args:
        if arg.startswith("#"):

            if not arg[1:].isdigit():
                raise ValueError("Received invalid placeholder variable {}".format(arg))

            index = int(arg[1:])
            if index < 0 or index >= len(memory):
                raise ValueError("Invalid index {} for memory of: {}".format(index, memory))

            ret_args.append(memory[index])

        elif arg.startswith("const_"):
            if arg[6:] == "pi":
                ret_args.append(3.14159)
            else:
                ret_args.append(float(arg[6:].replace("_", ".")))

        else:
            ret_args.append(float(arg))
    return ret_args


def solve_linear_program(program):
    """
    Solve a linear program, evaluating the expression into a final numeric value.
    This operates independently of the text, so assumes that the n arguments have been replaced.

    :param program: list of linear program tokens
    :return: numeric value of evaluated answer
    """

    memory = []

    # Iterate over program tokens
    for token in program.split():

        # In case of bad formatting
        token = token.strip()
        if not token:
            continue

        op, args = get_op_and_args(token)
        processed_args = evaluate_args(args, memory)
        result = function_switch[op](*processed_args)
        memory.append(result)

    return memory[-1]


def solve_linear_program_tokens(program, operators):
    """
    Solve a linear program, evaluating the expression into a final numeric value.
    This operates independently of the text, so assumes that the n arguments have been replaced.

    :param program: list of linear program tokens
    :return: numeric value of evaluated answer
    """

    # Empty program
    if not program:
        logging.error("Solving empty program.")
        return None

    memory = []

    # Iterate over program tokens
    idx = 0
    while idx < len(program):

        op = program[idx]
        nargs = operators[op]
        args = program[idx+1:idx+1+nargs]
        idx += nargs + 1
        processed_args = evaluate_args(args, memory)
        try:
            result = function_switch[op](*processed_args)
        except Exception as e:
            logging.error(e)
            logging.error("Could not evaluate program {}".format(program))
            return None
        memory.append(result)

    return memory[-1]


def fill_n_args(formula, text):

    nargs = extract_nargs(text)
    for i, arg in enumerate(nargs):
        formula = formula.replace("n{}".format(i), str(arg))
    return formula


def get_broken_questions(filepath):
    """
    Get list of broken question indices so we can ignore them when parsing
    :param filepath: filepath to .txt file with 1-indexed list of indices corresponding to broken questions in their
                     respective datasets. One index per line.
    :return: list of 1-indexed questions that are known to be broken
    """

    indices = []
    with open(filepath, "r") as f:
        for line in f:
            indices.append(int(line.strip()))
    return indices


def get_gold_value(gold_option, options):
    gold_option = gold_option.strip()
    if gold_option == "a":
        return options[0]
    elif gold_option == "b":
        return options[1]
    elif gold_option == "c":
        return options[2]
    elif gold_option == "d":
        return options[3]
    elif gold_option == "e":
        return options[4]
    else:
        raise ValueError("Invalid option " + gold_option)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Evaluate correctness of MathQA test set")
    parser.add_argument("--evaluation_file", type=str, default="out.json")
    parser.add_argument("--broken_questions", type=str, default="test_broken.txt")
    args = parser.parse_args()

    with open(args.evaluation_file, "r") as f:
        data = json.load(f)

    broken_questions = get_broken_questions(args.broken_questions)

    for i, datum in enumerate(data):
        if (i + 1) in broken_questions:
            continue
        formula = fill_n_args(datum["linear_formula"].replace("|", " "), datum["Problem"])
        solution = float(solve_linear_program(formula))
        if solution.is_integer():
            solution = int(solution)
        else:
            solution = round(solution, 5)
        print("Problem {}: {}".format(i+1, solution))




