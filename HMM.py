import os
from pathlib import Path

class HMM:
  def __init__(self):
    self.p = 0.5
    self.dices = ["D1", "D2", "D3"]
    self.emissions_prob = [[0.8, 0.1, 0.1],[0.1,0.8,0.1],[0.1,0.1,0.8]]
    self.s0 = [0.33,0.33,0.33]
    self.k = 5
    self.transition_prob = [[0.5, 0.25, 0.25],[0.25, 0.5, 0.25], [0.25, 0.25, 0.5]]
    # self.transition_table = 
    self.path = []

  def run_viterbi_algo(self, obs, prev_d1_prob, prev_d2_prob, prev_d3_prob):
    # recursion base case when observation array is empty
    if not obs:
      return
    elem = obs[0]
    prob_1 = None
    prob_2 = None 
    prob_3 = None

    # on first iteration
    if (prev_d1_prob == None):
      prob_1 = self.emissions_prob[0][int(elem) -1] * self.s0[0]
      prob_2 = self.emissions_prob[1][int(elem) -1] * self.s0[1]
      prob_3 = self.emissions_prob[2][int(elem) -1] * self.s0[2]
    else:
      prob_1 = max(prev_d1_prob * self.emissions_prob[0][int(elem) -1] *self.transition_prob[0][0],
      prev_d2_prob * self.emissions_prob[0][int(elem) -1] *self.transition_prob[1][0],
      prev_d3_prob * self.emissions_prob[0][int(elem) -1] *self.transition_prob[2][0]
      )
      prob_2 = max(prev_d1_prob * self.emissions_prob[1][int(elem) -1] *self.transition_prob[0][1],
      prev_d2_prob * self.emissions_prob[1][int(elem) -1] *self.transition_prob[1][1],
      prev_d3_prob * self.emissions_prob[1][int(elem) -1] *self.transition_prob[2][1]
      )
      prob_3 = max(prev_d1_prob * self.emissions_prob[2][int(elem) -1] *self.transition_prob[0][2],
      prev_d2_prob * self.emissions_prob[2][int(elem) -1] *self.transition_prob[1][2],
      prev_d3_prob * self.emissions_prob[2][int(elem) -1] *self.transition_prob[2][2]
      )
    dice = self.max_prob_dice(prob_1, prob_2, prob_3)
    self.path.append(dice)
    self.run_viterbi_algo(obs[1:], prob_1, prob_2, prob_3)
      
  def max_prob_dice(self, prob1, prob2, prob3):
    if (prob1 > prob2 and prob1 > prob3):
      return "D1"
    elif (prob2 > prob1 and prob2 > prob3):
      return "D2"
    else:
      return "D3"

# files = [os.path.realpath(file) for file in Path('input').rglob('*.txt')]
# file = 0
# while file < len(files):
#      file = file + 1


# print("probability of keeping the same dice")
# p_same_dice = int(float())

observations = ['1', '2', '2', '2', '3', '3', '3', '2', '2', '3', '3', '2', '3', '2', '3', '2', '3', '3', '3', '3', '2', '2', '1', '1', '2', '3', '2', '2', '1', '3', '2', '1', '2', '2', '3', '2', '2', '3', '3', '3', '1', '1', '2', '2', '1', '1', '1', '1', '3', '1', '3', '2', '1', '1', '1', '2', '2', '1', '3', '2', '3', '3', '1', '2', '2', '2', '3', '2', '2', '1', '3', '3', '2', '3', '1', '3', '2', '3', '2', '2', '1', '3', '3', '2', '1', '3', '3', '2', '2', '1', '2', '3', '3', '1', '1', '1', '3', '2', '1', '1']

hmm = HMM()
hmm.run_viterbi_algo(observations, None, None, None)
print(hmm.path)

# print("input emission probability")
# p_emission = int(input())