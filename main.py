import argparse

from utils import convert_nested_to_linear, preprocess
from solver import solve_linear_program


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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Evaluate correctness of MathQA test set")
    parser.add_argument("--operators_file", type=str, default="data/operators.txt")
    parser.add_argument("--arguments_file", type=str, default="arguments.json")
    parser.add_argument("--evaluation_file", type=str, default="data/test.json")
    args = parser.parse_args()

    operators = read_operators_from_txt(args.operators_file)
    #arguments = read_from_txt(ARGUMENTS_FILE)

    #programs = ["multiply(divide(multiply(120, const_1000), const_3600), 18)"]

    programs = []
    with open(args.evaluation_file, "r") as f:
        for line in f:
            programs.append(line.strip())

    #preprocessed_programs = [preprocess(p) for p in programs]


    #print(preprocessed_programs)
    #linear_programs = [convert_nested_to_linear(p, operators) for p in preprocessed_programs]

    # linear_programs = []
    # count = 0
    # for program in preprocessed_programs:
    #     count += 1
    #     print(count)
    #     linear_programs.append(convert_nested_to_linear(program, operators))

    #print(linear_programs)

    # with open("linearized.txt", "w") as f:
    #     for program in linear_programs:
    #         f.write(" ".join(program))
    #         f.write("\n")





