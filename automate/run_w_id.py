# Copyright (c) 2022-2026, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import argparse
import os
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description="Run assembly training/evaluation for a given assembly_id.")
    parser.add_argument("--assembly_id", type=str, required=True, help="Assembly ID to use.")
    parser.add_argument("--checkpoint", type=str, help="Checkpoint path.")
    parser.add_argument("--num_envs", type=int, default=128, help="Number of parallel environment.")
    parser.add_argument("--seed", type=int, default=-1, help="Random seed.")
    parser.add_argument("--train", action="store_true", help="Run training mode.")
    parser.add_argument("--log_eval", action="store_true", help="Log evaluation results.")
    parser.add_argument("--max_iterations", type=int, default=1500, help="Number of iteration for policy learning.")
    args = parser.parse_args()

    # Per-process overrides avoid clobbering shared config files when launching many jobs.
    env = os.environ.copy()
    env["NUMBA_CUDA_LOW_OCCUPANCY_WARNINGS"] = "0"
    env["AUTOMATE_ASSEMBLY_ID"] = args.assembly_id
    env["AUTOMATE_IF_SBC"] = str(args.train)
    env["AUTOMATE_IF_LOG_EVAL"] = str(args.log_eval)

    # if sys.platform.startswith("win"):
    #     command = ["isaaclab.bat"]
    # else:
    #     command = ["./isaaclab.sh"]

    # command.append("-p")
    command = []

    if args.train:
        command.extend(
            [
                "python",
                "/home/ps/code/IsaacLab-3.0.0-beta/scripts/reinforcement_learning/rl_games/train.py",
                "--headless",
                "--task=Isaac-AutoMate-Assembly-Direct-v0",
                f"--seed={args.seed}",
                f"--max_iterations={args.max_iterations}",
                f"agent.params.config.name=Assembly_{args.assembly_id}",
            ]
        )
    else:
        if not args.checkpoint:
            raise ValueError("No checkpoint provided for evaluation.")
        command.extend(
            [
                "/home/ps/code/IsaacLab-3.0.0-beta/source/scripts/reinforcement_learning/rl_games/play.py",
                "--task=Isaac-AutoMate-Assembly-Direct-v0",
            ]
        )

    command.append(f"--num_envs={args.num_envs}")

    if args.checkpoint:
        command.append(f"--checkpoint={args.checkpoint}")

    subprocess.run(command, env=env, check=True)


if __name__ == "__main__":
    main()
