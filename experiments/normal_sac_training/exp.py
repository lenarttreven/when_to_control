import argparse
import datetime
import os
import pickle
import time
from datetime import datetime

import jax
import jax.numpy as jnp
import jax.random as jr
import jax.tree_util as jtu
import matplotlib.pyplot as plt
import numpy as np
import wandb
from brax import envs
from jax.nn import swish
from mbpo.optimizers.policy_optimizers.sac.sac_brax_env import SAC

from wtc.envs.drone import Crazyflie2
from wtc.envs.greenhouse import GreenHouseEnv
from wtc.envs.reacher_dm_control import ReacherDMControl
from wtc.envs.rccar import RCCar, plot_rc_trajectory

ENTITY = 'trevenl'


def experiment(env_name: str = 'inverted_pendulum',
               backend: str = 'generalized',
               project_name: str = 'GPUSpeedTest',
               num_timesteps: int = 1_000_000,
               episode_length: int = 200,
               learning_discount_factor: int = 0.99,
               seed: int = 0,
               num_envs: int = 32,
               num_env_steps_between_updates: int = 10,
               networks: int = 0,
               batch_size: int = 64,
               action_repeat: int = 1,
               reward_scaling: float = 1.0,
               video_track: int = 2,
               num_final_evals: int = 10
               ):
    envs.register_environment('drone', Crazyflie2)
    envs.register_environment('greenhouse', GreenHouseEnv)
    assert env_name in ['ant', 'halfcheetah', 'hopper', 'humanoid', 'humanoidstandup', 'inverted_pendulum',
                        'inverted_double_pendulum', 'pusher', 'reacher', 'walker2d', 'drone', 'greenhouse',
                        'swimmer', 'rccar']
    episode_length = int(episode_length / action_repeat)
    if env_name == 'rccar':
        base_dt = 0.5
        base_episode_steps = 8
        new_dt = base_dt / 1
        env = RCCar(margin_factor=20, dt=new_dt)
    elif env_name == 'reacher':
        env = ReacherDMControl(backend=backend)
    else:
        env = envs.get_environment(env_name=env_name,
                                   backend=backend)

    if networks == 0:
        policy_hidden_layer_sizes = (32,) * 5
        critic_hidden_layer_sizes = (128,) * 4

    else:
        policy_hidden_layer_sizes = (64, 64)
        critic_hidden_layer_sizes = (64, 64)

    config = dict(env_name=env_name,
                  num_timesteps=num_timesteps,
                  episode_length=episode_length,
                  learning_discount_factor=learning_discount_factor,
                  seed=seed,
                  num_envs=num_envs,
                  num_env_steps_between_updates=num_env_steps_between_updates,
                  networks=networks,
                  batch_size=batch_size,
                  action_repeat=action_repeat,
                  reward_scaling=reward_scaling)

    wandb.init(
        project=project_name,
        dir='/cluster/scratch/' + ENTITY,
        config=config,
    )
    optimizer = SAC(
        environment=env,
        num_timesteps=num_timesteps,
        episode_length=episode_length,
        action_repeat=action_repeat,
        num_env_steps_between_updates=num_env_steps_between_updates,
        num_envs=num_envs,
        num_eval_envs=32,
        lr_alpha=3e-4,
        lr_policy=3e-4,
        lr_q=3e-4,
        wd_alpha=0.,
        wd_policy=0.,
        wd_q=0.,
        max_grad_norm=1e5,
        discounting=learning_discount_factor,
        batch_size=batch_size,
        num_evals=20,
        normalize_observations=True,
        reward_scaling=reward_scaling,
        tau=0.005,
        min_replay_size=10 ** 3,
        max_replay_size=10 ** 6,
        grad_updates_per_step=num_env_steps_between_updates * num_envs,
        deterministic_eval=True,
        init_log_alpha=0.,
        policy_hidden_layer_sizes=policy_hidden_layer_sizes,
        policy_activation=swish,
        critic_hidden_layer_sizes=critic_hidden_layer_sizes,
        critic_activation=swish,
        wandb_logging=True,
        return_best_model=True,
    )

    xdata, ydata = [], []
    times = [datetime.now()]

    def progress(num_steps, metrics):
        times.append(datetime.now())
        xdata.append(num_steps)
        ydata.append(metrics['eval/episode_reward'])
        plt.xlabel('# environment steps')
        plt.ylabel('reward per episode')
        plt.plot(xdata, ydata)
        plt.show()

    start_time = time.time()
    print('Before inference')
    policy_params, metrics = optimizer.run_training(key=jr.PRNGKey(seed), progress_fn=progress)
    print('After inference')
    print('Total time: {}'.format(time.time() - start_time))

    # Now we plot the evolution
    pseudo_policy = optimizer.make_policy(policy_params, deterministic=True)

    @jax.jit
    def policy(obs):
        return pseudo_policy(obs, key_sample=jr.PRNGKey(0))

    ########################## Evaluation ##########################
    ################################################################

    if env_name == 'rccar':
        base_dt = 0.5
        base_episode_steps = 8
        new_dt = base_dt / 1
        env = RCCar(margin_factor=20, dt=new_dt)
    elif env_name == 'reacher':
        env = ReacherDMControl(backend=backend)
    else:
        base_env = envs.get_environment(env_name=env_name,
                                        backend=backend)
    step_fn = jax.jit(env.step)

    for index in range(num_final_evals):
        state = env.reset(rng=jr.PRNGKey(index))
        print('Start simulation')
        trajectory = []
        total_steps = 0
        while (not state.done) and (total_steps < episode_length):
            action = policy(state.obs)[0]
            state = step_fn(state, action)
            total_steps += 1
            trajectory.append(state)

        trajectory = jtu.tree_map(lambda *xs: jnp.stack(xs, axis=0), *trajectory)

        wandb.log({f'results/total_reward_{index}': jnp.sum(trajectory.reward),
                   f'results/num_actions_{index}': len(trajectory.reward)})

        if video_track < 2:
            traj = [jtu.tree_map(lambda x: x[i], trajectory).pipeline_state for i in range(trajectory.obs.shape[0])]
            print('End simulation, start rendering')
            if video_track == 0:
                video_frames = base_env.render(traj, camera='track')
            elif video_track == 1:
                video_frames = base_env.render(traj)
            print('Uploading video to wandb.')
            video = np.stack(video_frames)
            video = np.transpose(video, (0, 3, 1, 2))

            wandb.log({f"video_{index}": wandb.Video(video, fps=int(1 / env.dt))})

        # We save full_trajectory to wandb
        # Save trajectory rather than rendered video
        directory = os.path.join(wandb.run.dir, 'results')
        if not os.path.exists(directory):
            os.makedirs(directory)
        model_path = os.path.join(directory, f'trajectory_{index}.pkl')
        with open(model_path, 'wb') as handle:
            pickle.dump(trajectory, handle)
        wandb.save(model_path, wandb.run.dir)
    wandb.finish()


def main(args):
    experiment(env_name=args.env_name,
               backend=args.backend,
               project_name=args.project_name,
               num_timesteps=args.num_timesteps,
               episode_length=args.episode_length,
               learning_discount_factor=args.learning_discount_factor,
               seed=args.seed,
               num_envs=args.num_envs,
               num_env_steps_between_updates=args.num_env_steps_between_updates,
               networks=args.networks,
               batch_size=args.batch_size,
               action_repeat=args.action_repeat,
               reward_scaling=args.reward_scaling,
               video_track=args.video_track,
               num_final_evals=args.num_final_evals,
               )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--env_name', type=str, default='rccar')
    parser.add_argument('--backend', type=str, default='generalized')
    parser.add_argument('--project_name', type=str, default='GPUSpeedTest')
    parser.add_argument('--num_timesteps', type=int, default=50_000)
    parser.add_argument('--episode_length', type=int, default=8)
    parser.add_argument('--learning_discount_factor', type=float, default=0.9)
    parser.add_argument('--seed', type=int, default=20)
    parser.add_argument('--num_envs', type=int, default=128)
    parser.add_argument('--num_env_steps_between_updates', type=int, default=10)
    parser.add_argument('--networks', type=int, default=1)
    parser.add_argument('--batch_size', type=int, default=128)
    parser.add_argument('--action_repeat', type=int, default=1)
    parser.add_argument('--reward_scaling', type=float, default=1.0)
    parser.add_argument('--video_track', type=int, default=1)
    parser.add_argument('--num_final_evals', type=int, default=1)

    args = parser.parse_args()
    main(args)
