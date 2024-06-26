import jax
import jax.numpy as jnp
import jax.tree_util as jtu
from brax.envs.base import PipelineEnv, State, Env
from jax.lax import cond, while_loop, scan
import chex

EPS = 1e-10


class FixedNumOfSwitchesWrapper(Env):
    def __init__(self,
                 env: PipelineEnv,
                 num_integrator_steps: int,
                 num_switches: int,
                 min_time_between_switches: float,
                 max_time_between_switches: float | None = None,
                 discounting: float = 0.99
                 ):
        self.env = env
        self.num_integrator_steps = num_integrator_steps
        self.num_switches = num_switches
        self.min_time_between_switches = min_time_between_switches
        assert min_time_between_switches >= self.env.dt, \
            'Min time between switches must be at least of the integration time dt'
        self.time_horizon = self.env.dt * self.num_integrator_steps
        if max_time_between_switches is None:
            max_time_between_switches = self.time_horizon
        self.max_time_between_switches = max_time_between_switches
        self.discounting = discounting

    def reset(self, rng: jax.Array) -> State:
        """
        The augmented state is represented by concatenated vector:
         (state, time-to-go, num_remaining_switches)
        """
        state = self.env.reset(rng)
        x0 = state.obs
        time_to_go = self.time_horizon
        num_remaining_switches = jnp.array(self.num_switches)
        augmented_obs = jnp.concatenate([x0, jnp.array(time_to_go).reshape(1), num_remaining_switches.reshape(1)])
        augmented_state = state.replace(obs=augmented_obs)
        return augmented_state

    def compute_time(self,
                     pseudo_time: chex.Array,
                     dt: chex.Array,
                     t_lower: chex.Array,
                     t_upper: chex.Array,
                     ) -> chex.Array:
        time_for_action = ((t_upper - t_lower) / 2 * pseudo_time + (t_upper + t_lower) / 2)
        return (time_for_action // dt) * dt

    # @partial(jax.jit, static_argnums=0)
    def step(self, state: State, action: jax.Array) -> State:
        obs, time_to_go, num_remaining_switches = state.obs[:-2], state.obs[-2], state.obs[-1]
        u, pseudo_time_for_action = action[:-1], action[-1]

        # Calculate the action time, i.e. Map pseudo_time_for_action from [-1, 1] to
        # time [self.min_time_between_switches, time_to_go]
        t_lower = self.min_time_between_switches
        t_upper = jnp.minimum(time_to_go, self.max_time_between_switches)

        time_for_action = self.compute_time(pseudo_time=pseudo_time_for_action,
                                            dt=self.env.dt,
                                            t_lower=t_lower,
                                            t_upper=t_upper)
        done = t_upper <= t_lower

        def last_action_true_fn(time_for_action, done):
            return time_to_go + EPS, True

        def last_action_false_fn(time_for_action, done):
            return time_for_action, done

        time_for_action, done = cond(num_remaining_switches == 1,
                                     last_action_true_fn, last_action_false_fn,
                                     time_for_action, done)

        # Calculate how many steps we need to take with action
        elapsed_time = self.time_horizon - time_to_go
        steps_passed = (elapsed_time // self.env.dt).astype(int)
        next_elapsed_time = elapsed_time + time_for_action
        next_steps_passed = (next_elapsed_time // self.env.dt).astype(int)
        num_steps = next_steps_passed - steps_passed

        # Integrate dynamics forward for the num_steps
        state = state.replace(obs=obs)

        def body_integration_step(val):
            s, r, index = val
            next_state = self.env.step(s, u)
            next_reward = r + (self.discounting ** index) * (1 - next_state.done) * next_state.reward
            return next_state, next_reward, index + 1

        def cond_integration_step(val):
            s, r, index = val
            # We continue if index is smaller that num_steps ant we are not done
            return jnp.bitwise_and(index < num_steps, jnp.bitwise_not(s.done.astype(bool)))

        init_val = (state, jnp.array(0.0), jnp.array(0))
        final_val = while_loop(cond_integration_step, body_integration_step, init_val)

        next_state, total_reward, _ = final_val

        # Done can come from running out of time, number of switches or since we overpassed the horizon
        next_done = 1 - (1 - next_state.done) * (1 - done)

        # Prepare augmented obs
        next_time_to_go = (time_to_go - time_for_action).reshape(1)
        next_num_remaining_switches = (num_remaining_switches - 1).reshape(1)
        augmented_next_obs = jnp.concatenate([next_state.obs, next_time_to_go, next_num_remaining_switches])

        augmented_next_state = next_state.replace(obs=augmented_next_obs,
                                                  reward=total_reward,
                                                  done=next_done)
        return augmented_next_state

    def simulation_step(self, state: State, action: jax.Array) -> (State, State):
        obs, time_to_go, num_remaining_switches = state.obs[:-2], state.obs[-2], state.obs[-1]
        u, pseudo_time_for_action = action[:-1], action[-1]

        # Calculate the action time, i.e. Map pseudo_time_for_action from [-1, 1] to
        # time [self.min_time_between_switches, time_to_go]
        t_lower = self.min_time_between_switches
        t_upper = jnp.minimum(time_to_go, self.max_time_between_switches)

        time_for_action = self.compute_time(pseudo_time=pseudo_time_for_action,
                                            dt=self.env.dt,
                                            t_lower=t_lower,
                                            t_upper=t_upper)
        done = t_upper <= t_lower

        def last_action_true_fn(time_for_action, done):
            return time_to_go + EPS, True

        def last_action_false_fn(time_for_action, done):
            return time_for_action, done

        time_for_action, done = cond(num_remaining_switches == 1,
                                     last_action_true_fn, last_action_false_fn,
                                     time_for_action, done)

        # Calculate how many steps we need to take with action
        elapsed_time = self.time_horizon - time_to_go
        steps_passed = (elapsed_time // self.env.dt).astype(int)
        next_elapsed_time = elapsed_time + time_for_action
        next_steps_passed = (next_elapsed_time // self.env.dt).astype(int)
        num_steps = next_steps_passed - steps_passed

        # Integrate dynamics forward for the num_steps
        state = state.replace(obs=obs)

        @jax.jit
        def scan_f(s, _):
            n_s = self.env.step(s, u)
            next_done = 1 - (1 - s.done) * (1 - n_s.done)
            n_s = n_s.replace(done=next_done,
                              reward=(1 - next_done) * n_s.reward)
            return n_s, n_s

        next_state, inner_part = scan(scan_f, state, xs=None, length=num_steps.astype(int))
        inner_part_not_done = jtu.tree_map(lambda x: x[inner_part.done == 0], inner_part)

        # Compute total reward
        total_reward = jnp.sum(inner_part_not_done.reward)

        # Done can come from running out of time, number of switches or since we overpassed the horizon
        next_done = 1 - (1 - next_state.done) * (1 - done)

        # Prepare augmented obs
        next_time_to_go = (time_to_go - time_for_action).reshape(1)
        next_num_remaining_switches = (num_remaining_switches - 1).reshape(1)
        augmented_next_obs = jnp.concatenate([next_state.obs, next_time_to_go, next_num_remaining_switches])

        augmented_next_state = next_state.replace(obs=augmented_next_obs,
                                                  reward=total_reward,
                                                  done=next_done)
        return augmented_next_state, inner_part_not_done

    @property
    def observation_size(self) -> int:
        # +1 for time-to-go ant +1 for num remaining switches
        return self.env.observation_size + 2

    @property
    def action_size(self) -> int:
        # +1 for time that we apply action for
        return self.env.action_size + 1

    @property
    def backend(self) -> str:
        return self.env.backend


if __name__ == '__main__':
    from brax import envs
    import jax.random as jr
    from jax import jit

    env_name = 'inverted_pendulum'
    backend = 'generalized'

    env = envs.get_environment(env_name=env_name,
                               backend=backend)

    env = FixedNumOfSwitchesWrapper(env,
                                    num_integrator_steps=1000,
                                    num_switches=30,
                                    min_time_between_switches=env.dt,
                                    # max_time_between_switches=10 * env.dt,
                                    discounting=1.0)

    key = jr.PRNGKey(42)
    key, subkey = jr.split(key)
    state = env.reset(subkey)

    wrapper = True

    u = jnp.array([0.1])
    time = jnp.array([0.0])
    augmented_action = jnp.concatenate([u, time]) if wrapper else u

    state, rest = env.simulation_step(state, augmented_action)
    jitted_step = jit(env.step)

    # import time
    #
    # for i in range(10):
    #     start_time = time.time()
    #     state = jitted_step(state, augmented_action)
    #     print(f'elapsed_time: {time.time() - start_time} sec')
