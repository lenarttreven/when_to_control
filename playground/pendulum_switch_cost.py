import datetime
from datetime import datetime

import jax
import jax.numpy as jnp
import jax.random as jr
import matplotlib.pyplot as plt
from jax.lax import scan
from jax.nn import swish
import jax.tree_util as jtu
from mbpo.optimizers.policy_optimizers.sac.sac_brax_env import SAC

from wtc.envs.pendulum import PendulumEnv
from wtc.wrappers.switching_cost import ConstantSwitchCost, SwitchCostWrapper

if __name__ == "__main__":
    wrapper = True
    PLOT_TRUE_TRAJECTORIES = True
    env = PendulumEnv(reward_source='dm-control')
    action_repeat = 1
    episode_length = 100

    if wrapper:
        env = SwitchCostWrapper(env,
                                num_integrator_steps=episode_length,
                                min_time_between_switches=1 * env.dt,
                                max_time_between_switches=50 * env.dt,
                                switch_cost=ConstantSwitchCost(value=jnp.array(0.1)))

    else:
        action_repeat = 7

    optimizer = SAC(
        environment=env,
        num_timesteps=40_000,
        episode_length=episode_length,
        action_repeat=action_repeat,
        num_env_steps_between_updates=10,
        num_envs=4,
        num_eval_envs=32,
        lr_alpha=3e-4,
        lr_policy=3e-4,
        lr_q=3e-4,
        wd_alpha=0.,
        wd_policy=0.,
        wd_q=0.,
        max_grad_norm=1e5,
        discounting=0.99,
        batch_size=32,
        num_evals=20,
        normalize_observations=True,
        reward_scaling=1.,
        tau=0.005,
        min_replay_size=10 ** 2,
        max_replay_size=10 ** 5,
        grad_updates_per_step=10 * 32,
        deterministic_eval=True,
        init_log_alpha=0.,
        policy_hidden_layer_sizes=(64, 64),
        policy_activation=swish,
        critic_hidden_layer_sizes=(64, 64),
        critic_activation=swish,
        wandb_logging=False,
        return_best_model=True,
    )

    xdata, ydata = [], []
    times = [datetime.now()]


    def progress(num_steps, metrics):
        times.append(datetime.now())
        xdata.append(num_steps)
        ydata.append(metrics['eval/episode_reward'])
        # plt.xlim([0, train_fn.keywords['num_timesteps']])
        # plt.ylim([min_y, max_y])
        plt.xlabel('# environment steps')
        plt.ylabel('reward per episode')
        plt.plot(xdata, ydata)
        plt.show()


    print('Before inference')
    policy_params, metrics = optimizer.run_training(key=jr.PRNGKey(0), progress_fn=progress)
    print('After inference')

    # Now we plot the evolution
    pseudo_policy = optimizer.make_policy(policy_params, deterministic=True)


    def policy(obs):
        return pseudo_policy(obs, key_sample=jr.PRNGKey(0))


    # @jax.jit
    def step(state, _):
        u = policy(state.obs)[0]
        print('Step')
        print(f'Time to go {u[-1]}')
        next_state, rest = env.simulation_step(state, u)
        return next_state, (next_state.obs, u, next_state.reward, rest)


    state = env.reset(rng=jr.PRNGKey(0))

    if wrapper:
        init_state = state
        LEGEND_SIZE = 20
        LABEL_SIZE = 20
        TICKS_SIZE = 20

        plt.rc('text', usetex=True)
        plt.rc('text.latex', preamble=
        r'\usepackage{amsmath}'
        r'\usepackage{bm}'
        r'\def\vx{{\bm{x}}}'
        r'\def\vf{{\bm{f}}}')

        import matplotlib as mpl

        mpl.rcParams['xtick.labelsize'] = TICKS_SIZE
        mpl.rcParams['ytick.labelsize'] = TICKS_SIZE

        trajectory = []
        full_trajectories = []
        while not state.done:
            state, one_traj = step(state, None)
            one_traj, full_trajectory = one_traj[:-1], one_traj[-1]
            trajectory.append(one_traj)
            full_trajectories.append(full_trajectory)

        trajectory = jtu.tree_map(lambda *xs: jnp.stack(xs, axis=0), *trajectory)
        full_trajectory = jtu.tree_map(lambda *xs: jnp.concatenate(xs), *full_trajectories)

        xs_full_trajectory = jnp.concatenate([init_state.obs[:-1].reshape(1, -1), full_trajectory.obs, ])
        rewards_full_trajectory = jnp.concatenate([init_state.reward.reshape(1, ), full_trajectory.reward])
        ts_full_trajectory = jnp.linspace(0, env.time_horizon, episode_length)

        fig, axs = plt.subplots(nrows=1, ncols=4, figsize=(20, 4))
        xs = trajectory[0][:, :-1]
        us = trajectory[1][:, :-1]
        rewards = trajectory[2]
        times_to_go = trajectory[0][:, -1]
        times_for_actions = trajectory[1][:, -1]

        total_time = env.time_horizon
        # All times are the times when we ended the actions
        all_ts = total_time - times_to_go
        all_ts = jnp.concatenate([jnp.array([0.0]), all_ts])

        all_xs = jnp.concatenate([state.obs[:-1].reshape(1, -1), xs])

        state_dict = {0: r'cos($\theta$)',
                      1: r'sin($\theta$)',
                      2: r'$\omega$'}

        if PLOT_TRUE_TRAJECTORIES:
            for i in range(3):
                axs[0].plot(ts_full_trajectory, xs_full_trajectory[:, i], label=state_dict[i])
            for h in all_ts:
                axs[0].axvline(x=h, color='black', ls='--', alpha=0.4)
        else:
            for i in range(3):
                axs[0].plot(all_ts, all_xs[:, i], label=state_dict[i])

        axs[0].set_xlabel('Time', fontsize=LABEL_SIZE)
        axs[0].set_ylabel('State', fontsize=LABEL_SIZE)

        axs[1].step(all_ts, jnp.concatenate([us, us[-1].reshape(1, -1)]), where='post', label=r'$u$')
        axs[1].set_xlabel('Time', fontsize=LABEL_SIZE)
        axs[1].set_ylabel('Action', fontsize=LABEL_SIZE)

        integrated_rewards = rewards / jnp.diff(all_ts) * 0.05

        if PLOT_TRUE_TRAJECTORIES:
            axs[2].plot(ts_full_trajectory, rewards_full_trajectory, label='Rewards')
            for h in all_ts:
                axs[2].axvline(x=h, color='black', ls='--', alpha=0.4)
        else:
            axs[2].step(all_ts, jnp.concatenate([integrated_rewards, integrated_rewards[-1].reshape(1, )]),
                        where='post', label='Rewards')
        axs[2].set_xlabel('Time', fontsize=LABEL_SIZE)
        axs[2].set_ylabel('Instance reward', fontsize=LABEL_SIZE)

        axs[3].plot(jnp.diff(all_ts), label='Times for actions')
        axs[3].set_xlabel('Action Steps', fontsize=LABEL_SIZE)
        axs[3].set_ylabel('Time for action', fontsize=LABEL_SIZE)

        # axs[4].plot(times_to_go, label='Time to go')
        # axs[3].plot(times_for_actions, label='Time for actions NORMALIZED')
        for ax in axs:
            ax.legend(fontsize=LEGEND_SIZE)
        plt.tight_layout()
        plt.savefig('pendulum_switch_cost.pdf')
        plt.show()
        print(f'Total reward: {jnp.sum(trajectory[2])}')
        print(f'Total number of actions {len(us)}')

    else:
        horizon = episode_length

        num_steps = horizon // action_repeat


        def repeated_step(state, _):
            u = policy(state.obs)[0]

            def f(state, _):
                nstate = env.step(state, u)
                return nstate, nstate.reward

            state, rewards = scan(f, state, (), action_repeat)
            state = state.replace(reward=jnp.sum(rewards, axis=0))
            return state, (state.obs, u, state.reward)


        x_last, trajectory = scan(repeated_step, state, None, length=num_steps)

        fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(16, 4))
        axs[0].plot(trajectory[0], label='Xs')
        axs[0].legend()
        axs[1].plot(trajectory[1], drawstyle='steps-post', label='Us')
        axs[1].legend()
        axs[2].plot(trajectory[2], label='Rewards')
        axs[2].legend()
        plt.show()
        print(f'Total reward: {jnp.sum(trajectory[2])}')

    time_to_jit = times[1] - times[0]
    time_to_train = times[-1] - times[1]

    print(f'time to jit: {time_to_jit}')
    print(f'time to train: {time_to_train}')
