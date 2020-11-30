import ray
from ray import tune
from ray.rllib import agents
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

ray.init()

config = {'gamma': 0.999,
          'lr': 0.0001,
          "n_step": 1000,
          'num_workers': 3,
          'monitor': True}
trainer2 = agents.dqn.DQNTrainer(env='LunarLander-v2', config=config)
results2 = trainer2.train()
