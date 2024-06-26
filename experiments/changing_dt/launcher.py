import exp
from experiments.util import generate_run_commands, generate_base_command, dict_permutations

################################################
#################### Humanoid ###################
################################################

humanoid_low_freq = {'env_name': ['humanoid', ],
                     'backend': ['generalized', ],
                     'project_name': ["HumanoidSACNoSwitchCostLowFreqMay20_13_30"],
                     'num_timesteps': [5_000_000, ],
                     'episode_time': [3.0, ],
                     'base_dt_divisor': [1, ],
                     'base_discount_factor': [0.97],
                     'seed': list(range(5)),
                     'num_envs': [256],
                     'num_env_steps_between_updates': [10, ],
                     'networks': [0, ],
                     'batch_size': [256],
                     'action_repeat': [2, 3, 5, 10, ],
                     'reward_scaling': [0.1, ],
                     'switch_cost_wrapper': [0, ],
                     'switch_cost': [0.1, ],
                     'time_as_part_of_state': [0, ],
                     'num_final_evals': [1, ],
                     'same_amount_of_gradient_updates': [0, ],
                     }

# humanoid_switch_cost_low_freq_base = {'env_name': ['humanoid', ],
#                                       'backend': ['generalized', ],
#                                       'project_name': ["HumanoidSACSwitchCostLowFreqMay20_10_00"],
#                                       'num_timesteps': [5_000_000, ],
#                                       'episode_time': [3.0, ],
#                                       'base_dt_divisor': [1, ],
#                                       'base_discount_factor': [0.97],
#                                       'seed': list(range(5)),
#                                       'num_envs': [256],
#                                       'num_env_steps_between_updates': [10, ],
#                                       'networks': [0, ],
#                                       'batch_size': [256],
#                                       'action_repeat': [1, ],
#                                       'reward_scaling': [0.1, ],
#                                       'switch_cost_wrapper': [1, ],
#                                       'switch_cost': [0.1, ],
#                                       'time_as_part_of_state': [1, ],
#                                       'num_final_evals': [1, ]
#                                       }
#
# humanoid_switch_cost_low_freq = []
# min_time_multipliers = [2, 3, 5, 10]
# for min_time_multiplier in min_time_multipliers:
#     cur_configs = humanoid_switch_cost_low_freq_base | {'min_time_repeat': [min_time_multiplier],
#                                                         'max_time_between_switches': [min_time_multiplier * 0.015]}
#     humanoid_switch_cost_low_freq.append(cur_configs)

# humanoid_no_switch_cost = {
#     'env_name': ['humanoid', ],
#     'backend': ['generalized', ],
#     'project_name': ["HumanoidNoSwitchCostMay10_16_20"],
#     'episode_time': [3.0],
#     'base_discount_factor': [0.97],
#     'seed': list(range(5)),
#     'num_envs': [256],
#     'num_env_steps_between_updates': [10, ],
#     'networks': [0, ],
#     'batch_size': [256],
#     'action_repeat': [1, ],
#     'reward_scaling': [0.1, ],
#     'switch_cost_wrapper': [0, ],
#     'same_amount_of_gradient_updates': [0, ],
#     'num_final_evals': [1, ],
#     'base_dt_divisor': [1, 2, 5, 10, 25, 50, ],
#     'num_timesteps': [5_000_000, ]
# }

# humanoid_switch_cost = {'env_name': ['humanoid', ],
#                         'backend': ['generalized', ],
#                         'project_name': ["HumanoidSwitchCostMay10_17_45"],
#                         'num_timesteps': [5_000_000, ],
#                         'episode_time': [3.0, ],
#                         'base_dt_divisor': [1, 2, 5, 10, 25, 50],
#                         'base_discount_factor': [0.97],
#                         'seed': list(range(5)),
#                         'num_envs': [256],
#                         'num_env_steps_between_updates': [10, ],
#                         'networks': [0, ],
#                         'batch_size': [256],
#                         'action_repeat': [1, ],
#                         'reward_scaling': [0.1, ],
#                         'switch_cost_wrapper': [1, ],
#                         'switch_cost': [0.1, 1.0],
#                         'max_time_between_switches': [0.015],
#                         'time_as_part_of_state': [1, ],
#                         'num_final_evals': [1, ]
#                         }

# humanoid_no_switch_cost_base_configs = {
#     'env_name': ['humanoid', ],
#     'backend': ['generalized', ],
#     'project_name': ["HumanoidNoSwitchCostMay10_17_45"],
#     'episode_time': [3.0],
#     'base_discount_factor': [0.97],
#     'seed': list(range(5)),
#     'num_envs': [256],
#     'num_env_steps_between_updates': [10, ],
#     'networks': [0, ],
#     'batch_size': [256],
#     'action_repeat': [1, ],
#     'reward_scaling': [0.1, ],
#     'switch_cost_wrapper': [0, ],
#     'same_amount_of_gradient_updates': [0, 1, ],
#     'num_final_evals': [1, ]
# }
#
# humanoid_no_switch_cost_configs = []
# base_dt_divisor = [1, 2, 5, 10, 25, 50, ]
# base_numsteps = 5_000_000
# for dt_divisor in base_dt_divisor:
#     cur_configs = humanoid_no_switch_cost_base_configs | {'base_dt_divisor': [dt_divisor],
#                                                          'num_timesteps': [base_numsteps * dt_divisor]}
#     humanoid_no_switch_cost_configs.append(cur_configs)


################################################
#################### Reacher ###################
################################################

reacher_low_freq = {'env_name': ['reacher', ],
                    'backend': ['generalized', ],
                    'project_name': ["ReacherSACNoSwitchCostLowFreqMay20_13_30"],
                    'num_timesteps': [100_000, ],
                    'episode_time': [2.0, ],
                    'base_dt_divisor': [1, ],
                    'base_discount_factor': [0.95],
                    'seed': list(range(5)),
                    'num_envs': [256],
                    'num_env_steps_between_updates': [10, ],
                    'networks': [0, ],
                    'batch_size': [256],
                    'action_repeat': [2, 3, 5, 10, 20],
                    'reward_scaling': [0.1, ],
                    'switch_cost_wrapper': [0, ],
                    'switch_cost': [0.1, ],
                    'time_as_part_of_state': [0, ],
                    'num_final_evals': [10, ],
                    'same_amount_of_gradient_updates': [0, ],
                    }

# reacher_switch_cost_low_freq_base = {'env_name': ['reacher', ],
#                                      'backend': ['generalized', ],
#                                      'project_name': ["ReacherSACSwitchCostLowFreqMay20_10_10"],
#                                      'num_timesteps': [100_000, ],
#                                      'episode_time': [2.0, ],
#                                      'base_dt_divisor': [1, ],
#                                      'base_discount_factor': [0.95],
#                                      'seed': list(range(5)),
#                                      'num_envs': [256],
#                                      'num_env_steps_between_updates': [10, ],
#                                      'networks': [0, ],
#                                      'batch_size': [256],
#                                      'action_repeat': [1, ],
#                                      'reward_scaling': [5.0, ],
#                                      'switch_cost_wrapper': [1, ],
#                                      'switch_cost': [0.1, ],
#                                      'time_as_part_of_state': [1, ],
#                                      'num_final_evals': [10, ]
#                                      }
#
# reacher_switch_cost_low_freq = []
# min_time_multipliers = [2, 3, 5, 10, 20]
# for min_time_multiplier in min_time_multipliers:
#     cur_configs = reacher_switch_cost_low_freq_base | {'min_time_repeat': [min_time_multiplier],
#                                                        'max_time_between_switches': [min_time_multiplier * 0.02]}
#     reacher_switch_cost_low_freq.append(cur_configs)

# reacher_switch_cost = {'env_name': ['reacher', ],
#                        'backend': ['generalized', ],
#                        'project_name': ["ReacherSwitchCostApr24_09_45"],
#                        'num_timesteps': [100_000, ],
#                        'episode_time': [2.0, ],
#                        'base_dt_divisor': [1, 2, 5, 10, 25, 50],
#                        'base_discount_factor': [0.95],
#                        'seed': list(range(5)),
#                        'num_envs': [256],
#                        'num_env_steps_between_updates': [10, ],
#                        'networks': [0, ],
#                        'batch_size': [256],
#                        'action_repeat': [1, ],
#                        'reward_scaling': [5.0, ],
#                        'switch_cost_wrapper': [1, ],
#                        'switch_cost': [0.1, ],
#                        'max_time_between_switches': [0.02],
#                        'time_as_part_of_state': [1, ],
#                        'num_final_evals': [10, ]
#                        }

# reacher_no_switch_cost_base_configs = {
#     'env_name': ['reacher', ],
#     'backend': ['generalized', ],
#     'project_name': ["ReacherNoSwitchCostApr24_10_00"],
#     'episode_time': [2.0],
#     'base_discount_factor': [0.95],
#     'seed': list(range(5)),
#     'num_envs': [256],
#     'num_env_steps_between_updates': [10, ],
#     'networks': [0, ],
#     'batch_size': [256],
#     'action_repeat': [1, ],
#     'reward_scaling': [5.0, ],
#     'switch_cost_wrapper': [0, ],
#     'same_amount_of_gradient_updates': [0, 1, ],
#     'num_final_evals': [10, ]
# }

# reacher_no_switch_cost_configs = []
# base_dt_divisor = [1, 2, 5, 10, 25, 50, ]
# base_numsteps = 100_000
# for dt_divisor in base_dt_divisor:
#     cur_configs = reacher_no_switch_cost_base_configs | {'base_dt_divisor': [dt_divisor],
#                                                          'num_timesteps': [base_numsteps * dt_divisor]}
#     reacher_no_switch_cost_configs.append(cur_configs)
#
# reacher_no_switch_cost = {
#     'env_name': ['reacher', ],
#     'backend': ['generalized', ],
#     'project_name': ["ReacherNoSwitchCostMay08_15_45"],
#     'episode_time': [2.0],
#     'base_discount_factor': [0.95],
#     'seed': list(range(5)),
#     'num_envs': [256],
#     'num_env_steps_between_updates': [10, ],
#     'networks': [0, ],
#     'batch_size': [256],
#     'action_repeat': [1, ],
#     'reward_scaling': [5.0, ],
#     'switch_cost_wrapper': [0, ],
#     'same_amount_of_gradient_updates': [0, ],
#     'num_final_evals': [10, ],
#     'base_dt_divisor': [1, 2, 5, 10, 25, 50, ],
#     'num_timesteps': [100_000, ]
# }


################################################
#################### RC Car ####################
################################################

rccar_low_freq = {'env_name': ['rccar', ],
                  'backend': ['generalized', ],
                  'project_name': ["RCCarSACNoSwitchCostLowFreqMay20_13_30"],
                  'num_timesteps': [50_000, ],
                  'episode_time': [4.0, ],
                  'base_dt_divisor': [1, ],
                  'base_discount_factor': [0.9],
                  'seed': list(range(5)),
                  'num_envs': [128],
                  'num_env_steps_between_updates': [10, ],
                  'networks': [0, ],
                  'batch_size': [128],
                  'action_repeat': [2, 3, 5, ],
                  'reward_scaling': [0.1, ],
                  'switch_cost_wrapper': [0, ],
                  'switch_cost': [0.1, ],
                  'time_as_part_of_state': [0, ],
                  'num_final_evals': [1, ],
                  'same_amount_of_gradient_updates': [0, ],
                  }

# rccar_switch_cost_low_freq_base = {'env_name': ['rccar', ],
#                                    'backend': ['generalized', ],
#                                    'project_name': ["RCCarSACSwitchCostLowFreqMay20_10_15"],
#                                    'num_timesteps': [50_000, ],
#                                    'episode_time': [4.0],
#                                    'base_dt_divisor': [1, ],
#                                    'base_discount_factor': [0.9],
#                                    'seed': list(range(5)),
#                                    'num_envs': [128],
#                                    'num_env_steps_between_updates': [10, ],
#                                    'networks': [0, ],
#                                    'batch_size': [128],
#                                    'action_repeat': [1, ],
#                                    'reward_scaling': [1.0, ],
#                                    'switch_cost_wrapper': [1, ],
#                                    'switch_cost': [0.1, ],
#                                    'time_as_part_of_state': [1, ],
#                                    'num_final_evals': [1, ]
#                                    }
#
# rccar_switch_cost_low_freq = []
# min_time_multipliers = [2, 3, 5, ]
# for min_time_multiplier in min_time_multipliers:
#     cur_configs = rccar_switch_cost_low_freq_base | {'min_time_repeat': [min_time_multiplier],
#                                                      'max_time_between_switches': [min_time_multiplier * 0.5]}
#     rccar_switch_cost_low_freq.append(cur_configs)

# general_configs = {
#     'project_name': ["RCCarSwitchCostApr17_14_00"],
#     'backend': ['generalized', ],
#     'num_timesteps': [50_000, ],
#     'base_discount_factor': [0.9],
#     'num_envs': [128],
#     'num_env_steps_between_updates': [10, ],
#     'seed': list(range(5)),
#     'networks': [0, ],
#     'batch_size': [128],
#     'action_repeat': [1, ],
# }
#
# rccar_switch_cost = {'env_name': ['rccar', ],
#                      'reward_scaling': [1.0, ],
#                      'episode_time': [4.0],
#                      'base_dt_divisor': [1, 2, 5, 10, 25, 50, 80, 100, 150, 200],
#                      'switch_cost_wrapper': [1, ],
#                      'switch_cost': [0.1, 0.5, 1.0],
#                      'max_time_between_switches': [0.5],
#                      'time_as_part_of_state': [1, ]
#                      } | general_configs
#
# rccar_no_switch_cost_base_configs = {
#     'project_name': ["RCCarNoSwitchCostApr17_14_00"],
#     'env_name': ['rccar', ],
#     'reward_scaling': [1.0, ],
#     'episode_time': [4.0],
#     'switch_cost_wrapper': [0, ],
#     'backend': ['generalized', ],
#     'base_discount_factor': [0.9],
#     'num_envs': [128],
#     'num_env_steps_between_updates': [10, ],
#     'seed': list(range(5)),
#     'networks': [0, ],
#     'batch_size': [128],
#     'action_repeat': [1, ],
#     'same_amount_of_gradient_updates': [0, 1, ],
# }
#
# rccar_no_switch_cost_configs = []
# base_dt_divisor = [1, 2, 5, 10, 25, 50, 80, 100, 150, 200]
# base_numsteps = 50_000
# for dt_divisor in base_dt_divisor:
#     cur_configs = rccar_no_switch_cost_base_configs | {'base_dt_divisor': [dt_divisor],
#                                                        'num_timesteps': [base_numsteps * dt_divisor]}
#     rccar_no_switch_cost_configs.append(cur_configs)

# rccar_no_switch_cost = {
#     'project_name': ["RCCarNoSwitchCostMay08_15_45"],
#     'env_name': ['rccar', ],
#     'reward_scaling': [1.0, ],
#     'episode_time': [4.0],
#     'switch_cost_wrapper': [0, ],
#     'backend': ['generalized', ],
#     'base_discount_factor': [0.9],
#     'num_envs': [128],
#     'num_env_steps_between_updates': [10, ],
#     'seed': list(range(5)),
#     'networks': [0, ],
#     'batch_size': [128],
#     'action_repeat': [1, ],
#     'same_amount_of_gradient_updates': [0, 1, ],
#     'base_dt_divisor': [1, 2, 5, 10, 25, 50, 80, 100, 150, 200],
#     'num_timesteps': [50_000, ],
#     'num_final_evals': [1, ]
# }


#
# ################################################
# #################### Hopper ####################
# ################################################
#
# general_configs = {
#     'project_name': [PROJECT_NAME],
#     'backend': ['generalized', ],
#     'num_timesteps': [1_000_000, ],
#     'base_discount_factor': [0.99],
#     'num_envs': [128],
#     'num_env_steps_between_updates': [10, ],
#     'seed': list(range(5)),
#     'networks': [0, ],
#     'batch_size': [128],
#     'action_repeat': [1, ],
# }
#
# hopper_switch_cost = {'env_name': ['hopper', ],
#                       'reward_scaling': [30.0, ],
#                       'episode_time': [4.0],
#                       'base_dt_divisor': [1, 2, 4, 10, 15, 20, 25, 30, ],
#                       'switch_cost_wrapper': [1, ],
#                       'switch_cost': [0.1, 0.2, 0.5, 0.8, 1.0, 1.5, 2.0],
#                       'max_time_between_switches': [0.008],
#                       'time_as_part_of_state': [1, ]
#                       } | general_configs


###########################################################################


#################### halfcheetah ####################

halfcheetah_low_freq = {'env_name': ['halfcheetah', ],
                        'backend': ['generalized', ],
                        'project_name': ["HalfcheetahSACNoSwitchCostLowFreqMay20_13_30"],
                        'num_timesteps': [1_000_000, ],
                        'episode_time': [10.0, ],
                        'base_dt_divisor': [1, ],
                        'base_discount_factor': [0.99],
                        'seed': list(range(5)),
                        'num_envs': [128],
                        'num_env_steps_between_updates': [10, ],
                        'networks': [0, ],
                        'batch_size': [128],
                        'action_repeat': [2, 3, 5, 10],
                        'reward_scaling': [0.1, ],
                        'switch_cost_wrapper': [0, ],
                        'switch_cost': [0.1, ],
                        'time_as_part_of_state': [0, ],
                        'num_final_evals': [1, ],
                        'same_amount_of_gradient_updates': [0, ],
                        }


# halfcheetah_switch_cost_low_freq_base = {'project_name': ['HalfcheetahSACSwitchCostLowFreqMay20_10_00'],
#                                          'backend': ['generalized', ],
#                                          'env_name': ['halfcheetah', ],
#                                          'num_timesteps': [1_000_000, ],
#                                          'episode_time': [10.0],
#                                          'base_dt_divisor': [1, ],
#                                          'base_discount_factor': [0.99],
#                                          'seed': list(range(5)),
#                                          'num_envs': [128],
#                                          'num_env_steps_between_updates': [10, ],
#                                          'networks': [0, ],
#                                          'batch_size': [128],
#                                          'action_repeat': [1, ],
#                                          'reward_scaling': [1.0, ],
#                                          'switch_cost_wrapper': [1, ],
#                                          'switch_cost': [2.0, ],
#                                          'time_as_part_of_state': [1, ]
#                                          }
#
# halfcheetah_switch_cost_low_freq = []
# min_time_multipliers = [2, 3, 5, 10]
# for min_time_multiplier in min_time_multipliers:
#     cur_configs = halfcheetah_switch_cost_low_freq_base | {'min_time_repeat': [min_time_multiplier],
#                                                            'max_time_between_switches': [min_time_multiplier * 0.05]}
#     halfcheetah_switch_cost_low_freq.append(cur_configs)


# general_configs = {
#     'project_name': [PROJECT_NAME],
#     'backend': ['generalized', ],
#     'num_timesteps': [1_000_000, ],
#     'base_discount_factor': [0.99],
#     'num_envs': [128],
#     'num_env_steps_between_updates': [10, ],
#     'seed': list(range(5)),
#     'networks': [0, ],
#     'batch_size': [128],
#     'action_repeat': [1, ],
# }

# halfcheetah_switch_cost = {'env_name': ['halfcheetah', ],
#                            'reward_scaling': [1.0, ],
#                            'episode_time': [10.0],
#                            'base_dt_divisor': [1, 2, 4, 10, 15, 20, 25, 30, ],
#                            'switch_cost_wrapper': [1, ],
#                            'switch_cost': [0.5, 1.0, 2.0, 3.0],
#                            'max_time_between_switches': [0.05],
#                            'time_as_part_of_state': [1, ]
#                            } | general_configs


# halfcheetah_no_switch_cost_base_configs = {
#     'project_name': [PROJECT_NAME],
#     'env_name': ['halfcheetah', ],
#     'reward_scaling': [1.0, ],
#     'episode_time': [10.0],
#     'switch_cost_wrapper': [0, ],
#     'backend': ['generalized', ],
#     'base_discount_factor': [0.99],
#     'num_envs': [128],
#     'num_env_steps_between_updates': [10, ],
#     'seed': list(range(5)),
#     'networks': [0, ],
#     'batch_size': [128],
#     'action_repeat': [1, ],
#     'same_amount_of_gradient_updates': [0, 1,],
# }
#
# halfcheetah_no_switch_cost_configs = []
# base_dt_divisor = [1, 2, 4, 10, 15, 20, 25, 30,]
# base_numsteps = 1_000_000
# for dt_divisor in base_dt_divisor:
#     cur_configs = halfcheetah_no_switch_cost_base_configs | {'base_dt_divisor': [dt_divisor],
#                                                              'num_timesteps': [base_numsteps * dt_divisor]}
#     halfcheetah_no_switch_cost_configs.append(cur_configs)

###########################################################################


def main():
    command_list = []
    # flags_combinations = None
    # for conf in reacher_switch_cost_low_freq:
    #     if flags_combinations is None:
    #         flags_combinations = dict_permutations(conf)
    #     else:
    #         flags_combinations += dict_permutations(conf)
    flags_combinations = dict_permutations(reacher_low_freq)
    flags_combinations += dict_permutations(rccar_low_freq)
    flags_combinations += dict_permutations(halfcheetah_low_freq)

    for flags in flags_combinations:
        cmd = generate_base_command(exp, flags=flags)
        command_list.append(cmd)

    # submit jobs
    generate_run_commands(command_list,
                          num_cpus=1,
                          num_gpus=1,
                          mode='euler',
                          duration='23:59:00',
                          prompt=True,
                          mem=32000)


if __name__ == '__main__':
    main()
