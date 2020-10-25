# MathQA Evaluation Suite

This repository contains a detailed evaluation suite for the [MathQA](https://math-qa.github.io/) dataset by Amini et al. 

### Usage

Run `evaluate.py` with relevant arguments. Our reverse-engineered calculator (for evaluating the MathQA programs into numeric results)

### Benchmarks

We obtained a copy of the original evaluation script from Amini et al. and compared the results.

Explanation of accuracy differences:

##### Broken Questions

We track a 1-indexed list of broken question IDs. We refer to a question as 'broken' if it is not possible to mathematically evaluate it. Examples include taking the square root of a negative number, or dividing by zero. For our evaluation, we simply ignore these broken questions i.e. they do not factor into the total question count. I'm not very certain what the original evaluation script does with broken questions, but I'm aware it factors into the total count.

##### Normalized Option String Representation

We performed some normalization of the string representations of the options (a to e) for each question. This was motivated by various differences in representing options, presence of unicode that contained relevant

1. Resolved all instances of pi and square root operations into numeric forms. The original dataset left these in as unicode.

2. Reduced all numeric expressions into one of: single integer or floating point number (5 decimal places), a simple fraction or ratio delimited by `/` or `:`, or a mixed fraction (a number and a fraction). We ignore units and other decorators.

3. Removed intermediate commas and spaces for large numbers.

In theory, this should have no impact on the correctness of the solutions, particularly with a generous solution evaluation delta.

##### Fixing Options

A number of questions contained options that were ambiguous to interpretation, especially with respect to what the question requires. For example, a question may seek two numeric values, but the options provided may be a mix of single numeric values and pairs of numeric values. In such cases we

##### Limitations of Representation Language

Some questions have solutions that are unable to be represented by the current MathQA program language. For example, some questions ask for pairs of values (e.g. the value of x and y). In such cases, the program output (single numeric value) is ambiguous and does not exactly correspond to the options.

To prevent parsing errors of the options however, we manually corrected a number of option strings. This does not change the 'correctness' of the solution, it merely prevents a parsing error.

### Footnotes



 