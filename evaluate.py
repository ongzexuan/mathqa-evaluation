import argparse
import json
import logging
import sys

from utils import convert_nested_to_linear, strip_to_tokens, validate_linear_program, extract_options, extract_nargs
from solver import solve_linear_program_tokens


def read_operators_from_txt(file):
    ops = {}
    with open(file, "r") as f:
        for line in f:
            tokens = line.split("|")
            ops[tokens[0].strip()] = int(tokens[1].strip())
    return ops


def read_from_txt(file):
    args = []
    with open(file, "r") as f:
        for line in f:
            args.append(line.strip())
    return args


def score_default(evaluated_solutions, options, option_gold, delta):

    total_score = 0
    total_correct = 0
    total_close = 0
    total_guess = 0
    total_wrong = 0
    total_error = 0
    total_count = 0

    for sol_set, opts, gold_opt in zip(evaluated_solutions, options, option_gold):

        total_count += 1
        gold_idx = ord(gold_opt[0]) - 97 # maps abcde to 12345

        # If options are broken
        if not opts:
            logging.error("Cannot evaluate score for empty options!")
            total_error += 1
            continue

        # If no valid solution, guess
        if sol is None:
            total_guess += 1
            total_score += 1 / len(opts)
            continue

        # Search for candidates within delta and append to list
        candidate_set = []
        for i, opt in enumerate(opts):
            if not opt:
                continue
            d = abs(sol - opt)
            if d == 0.0:
                candidate_set = [i]
                break # exact match special case, break loop
            elif d <= delta:
                candidate_set.append(i)

        # Score based on length of list
        if len(candidate_set) == 1 and candidate_set[0] == gold_idx:
            total_correct += 1
            total_score += 1
        elif len(candidate_set) > 1 and gold_idx in candidate_set:
            total_close += 1
            total_score += len(candidate_set)
        else:
            total_wrong += 1

    return total_count, total_correct, total_close, total_wrong, total_error, total_guess, total_score


def map_nargs(program_sets, texts):

    for program_set, text in zip(program_sets, texts):
        nargs = extract_nargs(text)

        # Iterate over all programs in program set
        for program in program_set:

            # Iterate over all tokens and replace nargs
            for i in range(len(program)):
                if program[i][0] == "n" and program[i][1:].isdigit():
                    idx = int(program[i][1:])
                    if idx >= len(nargs):
                        logging.error("{} does not exist in problem with {} nargs: {}".format(program[i], len(nargs), text))
                        if not nargs:
                            logging.error("Hard-coding narg {} to 1.".format(program[i]))
                            program[i] = "1"
                        else:
                            program[i] = nargs[0]
                    else:
                        program[i] = nargs[idx]


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Evaluate correctness of MathQA predictions")
    parser.add_argument("--predictions", type=str, default="preds.txt") # prediction file
    parser.add_argument("--operators", type=str, default="data/operators.txt")  # list of valid operations
    parser.add_argument("--arguments", type=str, default="")          # list of valid arguments (after variable removal)
    parser.add_argument("--beam_size", type=int, default=1)             # number of consecutive rows per example
    parser.add_argument("--linear", type=bool, default=True)            # if input is linear or tree
    parser.add_argument("--delta", type=float, default=1)               # delta for measuring if solution is correct
    parser.add_argument("--set", type=str, default="test")              # test / challenge
    parser.add_argument("--log_errors", type=bool, default=True)        # log errors in stdout
    parser.add_argument("--verbose", default=False, action='store_true')     # verbose mode logs output for each example
    parser.add_argument("--ignore_broken", default=False, action='store_true') # flag for ignoring broken questions
    args = parser.parse_args()

    # Set log level
    if args.verbose:
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.getLogger().setLevel(logging.WARNING)

    # Load operators and arguments
    logging.info("Reading operators from {}".format(args.operators))
    operators = read_operators_from_txt(args.operators)
    arguments = None
    if args.arguments:
        logging.info("Reading arguments from {}".format(args.arguments))
        arguments = read_from_txt(args.arguments)

    # Parse and validate data
    programs = []
    lines_read = 0
    with open(args.predictions, "r") as f:
        for i, line in enumerate(f):
            if i % args.beam_size == 0:
                programs.append([])

            # If input is linearized already
            if args.linear:
                program = strip_to_tokens(line)
                if not validate_linear_program(program, operators):
                    logging.error("Invalid linear program: {}".format(program))
                else:
                    logging.info("{}. {}".format(i+1, program))
                programs[-1].append(program)

            # Else if input is in tree form
            else:
                program = convert_nested_to_linear(strip_to_tokens(line), operations=args.operators)
                programs[-1].append(program)
                logging.info("{}. Converted program: {}".format(i + 1, program))

            lines_read += 1

    # Log lines read and check if sensible w.r.t beam size
    logging.info("Read {} lines with beam size of {}.".format(lines_read, args.beam_size))
    if lines_read % args.beam_size != 0:
        logging.warning("Lines read not multiple of beam size!")

    # Read data from test / challenge file
    gold_data = None
    source = "data/test.json" if args.set == "test" else "data/challenge_test.json"
    logging.info("Reading gold data from {}.".format(source))
    with open(source, "r") as f:
        gold_data = json.load(f)
    if len(programs) != len(gold_data):
        logging.warning("Gold data contains {} entries, but number of program sets is {}!".format(len(gold_data), len(programs)))

    # Extract options
    logging.info("Extracting gold options...")
    options = [extract_options(datum["options"]) for datum in gold_data]
    option_gold = [datum["correct"] for datum in gold_data]

    # Map n variables back to programs
    map_nargs(programs, [datum["Problem"] for datum in gold_data])

    # Evaluate all programs and pass to scoring function
    logging.info("Evaluating predicted programs...")
    evaluated_solutions = []
    for i, program_set in enumerate(programs):
        try:
            sols = [solve_linear_program_tokens(p, operators) for p in program_set]
        except Exception as e:
            logging.error("Solver failed for problem {}: {}".format(i+1, gold_data[i]["Problem"]))
            raise e

        logging.info("Predictions {}: {}".format(i + 1, sols))
        evaluated_solutions.append(sols)

    #evaluated_solutions = [[solve_linear_program_tokens(p, operators) for p in program_set] for program_set in programs]

    # Score
    logging.info("Scoring...")
    total_count, total_correct, total_close, total_wrong, total_error, total_guess, total_score\
        = score_default(evaluated_solutions, options, option_gold, args.delta)

    print("Total count: {}, total correct: {}, total wrong: {}, total error: {}, total guesses: {}, total score: {}"
          .format(total_count, total_correct, total_close, total_wrong, total_error, total_guess, total_score))







