from gym.envs.registration import registry, register, make, spec

register(
    id='Yahtzee-v0',
    entry_point='yahtzee:YahtzeeEnv',
    tags={'wrapper_config.TimeLimit.max_episode_steps': 100}
)

env = make('Yahtzee-v0')
env.reset()
scores = []
while True:
    action = env.action_space.sample()
    state, reward, done, info_dict = env.step(action)
    env.render()
    print("Action:", action, ", Reward:", reward)
    if done:
        scores.append(env.total_score())
        state = env.reset()
        done = False
        if len(scores) == 1:
            break
print("Avg.:", float(sum(scores))/len(scores), "Max:", max(scores), "Min:", min(scores))
