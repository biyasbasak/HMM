import os
from pathlib import Path


def read_file(file):
    p = 0
    emission_prob = []
    observations = []
    with open(file, "r") as f:
        valid_input = 0
        for l in f:
            if l.startswith("#"):
                continue
            else:
                if valid_input == 0:
                    p = float(l)
                if valid_input > 0 and valid_input <= 3:
                    emission = list(map(float, l.split(" ")))
                    emission_prob.append(emission)

                if valid_input > 3 and valid_input <= 4:
                    obs = list(map(float, l.split(",")))
                    observations = obs
                valid_input += 1
    return (p, emission_prob, observations)


class HMM:
    def __init__(self, p, emission_prob):
        self.p = p
        self.p_1 = 1 - self.p
        self.dices = ("D1", "D2", "D3")

        self.emissions_prob = emission_prob
        # initial transition state
        self.s = [0.33, 0.33, 0.33]
        self.path = []

    def print(self):
        print(f'transition probability:- \n current Dice:- {round(self.p,4)}, \n Other Dices:- {round(self.p_1/2,4)}' )

        print(f'emission probabilities:- {self.emissions_prob}')

        print(f'initial state:- {self.s}')
        

    def run(self, obs, prev_d1_prob, prev_d2_prob, prev_d3_prob):
        # recursion base case when observation array is empty
        if not obs:
            print(f'final D1 prob: {prev_d1_prob} \nfinal D2 prob: {prev_d2_prob} \nfinal D3 prob: {prev_d3_prob}')
            return
        elem = int(obs[0])
        prob_1 = None
        prob_2 = None
        prob_3 = None

        # on first iteration
        if (prev_d1_prob == None):
            prob_1 = self.emissions_prob[0][elem - 1] * self.s[0]
            prob_2 = self.emissions_prob[1][elem - 1] * self.s[1]
            prob_3 = self.emissions_prob[2][elem - 1] * self.s[2]
        else:
            prob_1 = max(prev_d1_prob * self.emissions_prob[0][elem - 1] * self.s[0],
                         prev_d2_prob *
                         self.emissions_prob[0][elem - 1] * self.s[1],
                         prev_d3_prob *
                         self.emissions_prob[0][elem - 1] * self.s[2]
                         )
            prob_2 = max(prev_d1_prob * self.emissions_prob[1][elem - 1] * self.s[0],
                         prev_d2_prob *
                         self.emissions_prob[1][elem - 1] * self.s[1],
                         prev_d3_prob *
                         self.emissions_prob[1][elem - 1] * self.s[2]
                         )
            prob_3 = max(prev_d1_prob * self.emissions_prob[2][elem - 1] * self.s[0],
                         prev_d2_prob *
                         self.emissions_prob[2][elem - 1] * self.s[1],
                         prev_d3_prob *
                         self.emissions_prob[2][elem - 1] * self.s[2]
                         )
        self.update_path_state(prob_1, prob_2, prob_3)
        self.run(obs[1:], prob_1, prob_2, prob_3)

    def update_path_state(self, prob1, prob2, prob3):
        if (prob1 > prob2 and prob1 > prob3):
            self.path.append("D1")
            self.s = [self.p, self.p_1/2, self.p_1/2]
        elif (prob2 > prob1 and prob2 > prob3):
            self.path.append("D2")
            self.s = [self.p_1/2, self.p, self.p_1/2]
        else:
            self.path.append("D3")
            self.s = [self.p_1/2, self.p_1/2, self.p]


files = [os.path.realpath(file) for file in Path('input').rglob('*.txt')]
i = 0
while i < len(files):
    (p, emission_prob, observations) = read_file(files[i])
    # print(emission_prob)
    hmm = HMM(p, emission_prob)
    hmm.print()
    hmm.run(observations, None, None, None)
    print(f'Most Probable Outcome:- \n{hmm.path}')
    i = i + 1
