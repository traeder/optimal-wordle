import json


class Constraint:
    def apply(self, word):
        return False


class Constraints(Constraint):
    def __init__(self):
        self.constraints = []

    def prepend(self, constraint):
        self.constraints.insert(0, constraint)

    def append(self, constraint):
        self.constraints.append(constraint)

    def apply(self, word):
        for constraint in self.constraints:
            if constraint.apply(word) is False:
                return False
        return True

    @classmethod
    def from_wordle(cls, input_data):
        d = json.loads(input_data) if isinstance(input_data, str) else input_data
        board_state = d['boardState']
        constraints = Constraints()
        evaluations = d['evaluations']
        for row, w in enumerate(board_state):
            word = w.upper()
            if len(word) == 0:
                return constraints
            for ix, evaluation in enumerate(evaluations[row]):
                letter = word[ix]
                if evaluation == 'absent':
                    constraints.append(AbsentConstraint(letter))
                elif evaluation == 'correct':
                    constraints.append(CorrectConstraint(letter, ix))
                elif evaluation == 'present':
                    constraints.append(PresentConstraint(letter, ix))
        return constraints


class CorrectConstraint(Constraint):
    def __init__(self, letter, position):
        self.letter = letter
        self.position = position

    def apply(self, word):
        return word[self.position] == self.letter


class AbsentConstraint(Constraint):
    def __init__(self, letter):
        self.letter = letter

    def apply(self, word):
        return self.letter not in word


class PresentConstraint(Constraint):
    def __init__(self, letter, not_position):
        self.letter = letter
        self.not_position = not_position

    def apply(self, word):
        return self.letter in word and word[self.not_position] != self.letter


class LengthConstraint(Constraint):
    def __init__(self, length):
        self.length = length

    def apply(self, word):
        return len(word) == self.length