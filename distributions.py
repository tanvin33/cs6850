from new_model import self_testing_model
import numpy as np 
import matplotlib.pyplot as plt
from scipy import stats
import pickle

if __name__ == "__main__":
  Zt = 1500
  Zc = 30
  k = 2
  distributions = {
      "uniform": stats.uniform(),
      "normal": stats.skewnorm(0),
      "pos-skew": stats.skewnorm(1),
      "neg-skew": stats.skewnorm(-1),
      "lognorm": stats.lognorm(0.39)
  }

  result = np.zeros((101,101))

  # for distr_name in distributions:
  #       print(distr_name)
  #       distribution = distributions[distr_name]
  #       for p1 in range(0, 101):
  #           for q1 in range(0, 101):
  #               num_contained = 0
  #               for i in range(10):
  #                   G, color_map, return_code = self_testing_model(Zc, Zt, k, p1 / 100.0, q1 / 100.0, distribution)
  #                   if return_code == 2:
  #                       num_contained += 1
  #               result[p1, q1] = num_contained / 10.0
        
  #       pickle.dump(result, open(f"distributions/{distr_name}.pckl", "wb"))
  #       result = np.zeros((101,101))

  for distr_name in distributions:
    result = pickle.load(open(f'distributions/{distr_name}.pckl', 'rb'))
    print(result)
    fig, ax = plt.subplots()
    ax.set(xlim=(0, 100), ylim=(0, 100))
    ax.set_xticklabels([str(i/10) for i in range(0, 11, 2)])
    ax.set_yticklabels([str(i/10) for i in range(0, 11, 2)])
    im = ax.imshow(result, cmap="YlGn", interpolation="nearest")
    cbar = ax.figure.colorbar(im, ax=ax)
    plt.title(f"{distr_name[0].capitalize() + distr_name[1:]} Distribution")
    plt.xlabel("q")
    plt.ylabel("p")
    plt.savefig(f"distributions/{distr_name}_graph.png")
  
  distr_arr = [distr_name for distr_name in distributions]
  avg = []

  for distr_name in distributions:
      result = pickle.load(open(f'distributions/{distr_name}.pckl', 'rb'))
      avg.append(np.sum(result)/(100*100))
  
  fig, ax = plt.subplots()
  ax.bar(distr_arr, avg)
  ax.set_ylabel('Average Probability')
  ax.set_xlabel('Distribution')
  ax.set_title('Average Probability of Containment per Distribution')
  plt.savefig("distributions/avgprobs.png")
  