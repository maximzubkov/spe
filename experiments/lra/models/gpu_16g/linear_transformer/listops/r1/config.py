# Copyright 2020 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Configuration and hyperparameter sweeps."""

from fast_self_attention import fast_self_attention as favor
import jax

from lra_benchmarks.listops.configs import base_listops_config


def get_config():
  """Get the default hyperparameter configuration."""
  config = base_listops_config.get_config()
  config.random_seed = 0
  config.model_type = "transformer"
  config.attention_fn = favor.make_fast_generalized_attention(
    qkv_dim=config.qkv_dim // config.num_heads,
    features_type='deterministic',
    kernel_fn=lambda x: jax.nn.elu(x) + 1,
    lax_scan_unroll=16)
  config.batch_size = 8
  config.learning_rate = config.learning_rate / 32 * 8
  config.num_train_steps = 10000
  return config


def get_hyper(hyper):
  return hyper.product([])
