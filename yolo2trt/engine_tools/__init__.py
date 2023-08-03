# -*- coding: utf-8 -*-
# @Author  : JonathanLai
# @Time    : 8/3/23 11:09 AM
# @File    : __init__.py

from .engine import EngineBuilder, TRTModule, TRTProfilerV0, TRTProfilerV1  # isort:skip # noqa: E501
import warnings

import torch

warnings.filterwarnings(action='ignore', category=torch.jit.TracerWarning)
warnings.filterwarnings(action='ignore', category=torch.jit.ScriptWarning)
warnings.filterwarnings(action='ignore', category=UserWarning)
warnings.filterwarnings(action='ignore', category=FutureWarning)
warnings.filterwarnings(action='ignore', category=DeprecationWarning)
__all__ = ['EngineBuilder', 'TRTModule', 'TRTProfilerV0', 'TRTProfilerV1']