# Copyright (c) 2022-2026, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import os


def set_assembly_runtime(assembly_id: str | None, *, if_sbc: bool | None = None, if_logging_eval: bool | None = None):
    """Set per-process assembly overrides read by AssemblyEnv at init."""
    if assembly_id is not None:
        os.environ["AUTOMATE_ASSEMBLY_ID"] = assembly_id
    if if_sbc is not None:
        os.environ["AUTOMATE_IF_SBC"] = str(if_sbc)
    if if_logging_eval is not None:
        os.environ["AUTOMATE_IF_LOG_EVAL"] = str(if_logging_eval)


def assembly_log_name(assembly_id: str) -> str:
    return f"Assembly_{assembly_id}"
