"""
This file contains functions for converting from a nested program to a linear program.
This is useful since the calculator evaluates on linear programs.
"""

import logging
import re

strip_translation = str.maketrans(",()|", "    ")


def strip_to_tokens(program):
    return program.translate(strip_translation).split()


def is_arg(token):
    if len(token) == 1:
        return False
    elif token.startswith("n"):
        if token[1:].isdigit():
            return True
    elif token.startswith("const_"):
        if token[6:].isdigit():
            return True
    return False


def validate_linear_program(program, valid_operations, valid_arguments=None):
    """
    Validates a linear program, specifically that the ops and args are valid, and ops have the right number of arguments.
    :param program: list of program tokens
    :param valid_operations: dict of {op: num of args}
    :param valid_arguments: optional set of valid args
    :return: boolean indicating if program is valid
    """

    # Edge cases
    if not program:
        logging.info("Validated empty program.")
        return True

    if program[0] not in valid_operations:
        logging.error("Program cannot start with invalid operation {}. Program: {}".format(program[0], program))
        return False

    remaining_args = valid_operations[program[0]]
    if len(program) == 1 and remaining_args > 0:
        logging.error("Program cannot be composed of a single operation {}.".format(program[0]))
        return False

    for tok in program[1:]:

        # Branch for validating if arguments provided
        if valid_arguments:
            if remaining_args > 0 and tok in valid_arguments:
                remaining_args -= 1
            elif remaining_args == 0 and tok in valid_operations:
                remaining_args = valid_operations[tok]
            else:
                if remaining_args > 0:
                    logging.error("Expected {} more arguments for operation. Program: {}".format(remaining_args, program))
                else:
                    logging.error("Invalid operation {} received. Program: {}".format(program[0], program))
                return False

        # Branch of validating if no arguments provided
        else:
            if tok in valid_operations:
                if remaining_args == 0:
                    remaining_args = valid_operations[tok]
                else:
                    logging.error("Expected {} more arguments for operation. Program: {}".format(remaining_args, program))
                    return False
            else:
                if remaining_args > 0:
                    remaining_args -= 1
                else:
                    logging.error("Too many arguments. Program {}".format(program))

    # Check no remaining arguments
    if remaining_args != 0:
        logging.error("Too many arguments at end of program. Program {}".format(program))
        return False

    return True


def convert_nested_to_linear(program, operations, arguments=None):
    """
    Function to convert a nested program to a linear program

    :param program: iterator of program tokens in nested program format
    :param operations: dictionary of {k: v} where k is a valid operation string and v is the number of arguments,
                        note: program assumes that v >= 1
    :param arguments: (optional) set of valid arguments. If not provided, assume all non-ops are arguments
    :param handle_errors: (optional) if True, does not raise errors, and returns empty input for invalid programs
    :return: a list of tokens representing the linearized version of the input program
    """

    # Edge cases
    if not program:
        logging.info("Converted empty program.")
        return []

    linear_output = []
    operator_stack = []
    argument_stack = []
    op_count = 0

    # Iterate over all tokens in program
    logging.info("Converting program: {}".format(program))
    for token in program:

        # Push new operation onto stack
        if token in operations:
            operator_stack.append(token)

        # If arguments is defined, and argument is invalid
        elif arguments and token not in arguments:
            logging.error("Received invalid token: {}".format(token))
            return []

        # If arguments is not defined, and argument is invalid
        elif not arguments and not is_arg(token):
            logging.error("Received invalid token: {}".format(token))
            return []

        # Else treat it as a valid argument
        else:
            if not operator_stack:
                logging.error("Invalid program {}: Received argument with no valid operator {}".format(program, token))
                return linear_output

            argument_stack.append(token)

            # Check if need to empty stack
            while operator_stack and len(argument_stack) >= operations[operator_stack[-1]]:
                num_args = operations[operator_stack[-1]]
                linear_output.append("{}({})".format(operator_stack.pop(), ",".join(argument_stack[-num_args:])))
                for i in range(num_args):
                    argument_stack.pop()
                argument_stack.append("#{}".format(op_count))
                op_count += 1

    # Pop last
    if argument_stack and argument_stack[-1].startswith("#"):
        argument_stack.pop()

    # Validate argument stack
    if len(argument_stack) > 0:
        logging.error("Argument stack at completion non empty: {}".format(argument_stack))
        return []

    return linear_output


def _extract_special_option(token, separator=":"):
    """
    Function to handle silly ratio options like "a) 1 : 8"
    :param token: string containing the (single) individual option
    :return: the ratio expressed as a 5-decimal float i.e. LHS / RHS. None if division by 0
    """

    cidx = token.find(separator)
    lhs = float(re.findall(r"-?[0-9]+\.[0-9]*|-?[0-9]+", token[:cidx])[0])
    rhs = float(re.findall(r"-?[0-9]+\.[0-9]*|-?[0-9]+", token[cidx + 1:])[0])

    # Handle divide by zero
    if rhs == 0:
        return None
    return round(lhs / rhs, 5)


def _extract_mixed_fraction(token):
    """
    Function to extract a mixed number like "4 1 / 2" = 4.5
    :param token: string containing the (single) mixed fraction
    :return: 5 decimal float representing the mixed fraction
    """

    split_index = token.find("/")
    lhs = re.findall(r"-?[0-9]+\.[0-9]*|-?[0-9]+", token[:split_index])
    rhs = re.findall(r"-?[0-9]+\.[0-9]*|-?[0-9]+", token[split_index+1:])
    return round(float(lhs[0]) + float(lhs[1]) / float(rhs[0]), 5)


def extract_options(option_string):
    """
    Given an option string, return a list of numbers corresponding to the option positions.
    :param option_string: option string
    :return: list of numbers corresponding to option values. Can contain None if position did not contain a number.
    """

    tokens = option_string.split(", ")
    if len(tokens) != 5:
        raise ValueError("Bad options formatting: {}".format(option_string))

    options = []
    for token in tokens:
        token = token.replace(",", "") # handle commas in large numbers
        numerals = re.findall(r"-?[0-9]+\.[0-9]*|-?[0-9]+", token)
        if len(numerals) == 0:
            options.append(None)
            print("Bad option: {}".format(token))
        elif len(numerals) >= 2:
            # Handle special case of ratios e.g. "3 : 8"
            if len(numerals) == 2 and ":" in token:
                options.append(_extract_special_option(token, separator=":"))

            # Handle special case of fractions e.g. "3 / 8"
            elif len(numerals) == 2 and "/" in token:
                options.append(_extract_special_option(token, separator="/"))

            # Handle case of mixed fractions
            elif len(numerals) == 3 and ("/" in token or ":" in token):
                options.append(_extract_mixed_fraction(token))

            # Else is just a bad option
            else:
                print("Cannot parse token containing two numbers, defaulting to first: {}".format(token))
                options.append(float(numerals[0]))
        else:
            options.append(float(numerals[0]))

        if options[-1] and options[-1].is_integer():
            options[-1] = int(options[-1])

    return options


def extract_nargs(text):
    nargs = []
    for token in text.split():
        token = token.strip().replace(",", "")
        if token.isdigit():
            nargs.append(token)
        elif token.find('.') >= 0:
            index = token.find('.')
            left = token[:index]
            right = token[index + 1:]
            if left.isdigit() and right.isdigit():  # handle decimals
                nargs.append(token)
    return nargs

