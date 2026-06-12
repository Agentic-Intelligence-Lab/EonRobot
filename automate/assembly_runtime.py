# Copyright (c) 2022-2026, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import importlib
import os

from .assembly_tasks_cfg import ASSET_DIR


def set_assembly_runtime(assembly_id: str | None, *, if_sbc: bool | None = None, if_logging_eval: bool | None = None):
    """Set per-process assembly overrides read by AssemblyEnv at init."""
    if assembly_id is not None:
        os.environ["AUTOMATE_ASSEMBLY_ID"] = assembly_id
    if if_sbc is not None:
        os.environ["AUTOMATE_IF_SBC"] = str(if_sbc)
    if if_logging_eval is not None:
        os.environ["AUTOMATE_IF_LOG_EVAL"] = str(if_logging_eval)


def apply_assembly_to_env_cfg(
    env_cfg,
    assembly_id: str,
    *,
    if_sbc: bool | None = None,
    if_logging_eval: bool | None = None,
) -> None:
    """Apply assembly overrides on env_cfg before logging or gym.make."""
    task_cfg = env_cfg.tasks[env_cfg.task_name]
    task_cfg.assembly_id = assembly_id
    task_cfg.assembly_dir = f"{ASSET_DIR}/{assembly_id}/"
    task_cfg.disassembly_path_json = f"{task_cfg.assembly_dir}disassemble_traj.json"
    task_cfg.eval_filename = f"evaluation_{assembly_id}.h5"
    task_cfg.fixed_asset.spawn.usd_path = f"{task_cfg.assembly_dir}{task_cfg.fixed_asset_cfg.usd_path}"
    task_cfg.held_asset.spawn.usd_path = f"{task_cfg.assembly_dir}{task_cfg.held_asset_cfg.usd_path}"
    if if_sbc is not None:
        task_cfg.if_sbc = if_sbc
    if if_logging_eval is not None:
        task_cfg.if_logging_eval = if_logging_eval


def configure_assembly(
    env_cfg,
    assembly_id: str,
    *,
    if_sbc: bool | None = None,
    if_logging_eval: bool | None = None,
) -> None:
    set_assembly_runtime(assembly_id, if_sbc=if_sbc, if_logging_eval=if_logging_eval)
    apply_assembly_to_env_cfg(env_cfg, assembly_id, if_sbc=if_sbc, if_logging_eval=if_logging_eval)


def ensure_local_automate_registered() -> None:
    """Re-register local automate after Isaac Lab may override gym envs on Kit launch."""
    import automate

    importlib.reload(automate)


def assembly_log_name(assembly_id: str) -> str:
    return f"Assembly_{assembly_id}"
