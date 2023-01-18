# Copyright 2019 The Magenta Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Modification copyright 2020 Bui Quoc Bao.
# Add Latent Constraint VAE model.
# Add Small VAE model.

"""Configurations for MusicVAE models."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections

import tensorflow as tf
from magenta.common import merge_hparams
from magenta.contrib import training as contrib_training
from magenta.models.music_vae import Config
from magenta.models.music_vae import MusicVAE
from magenta.models.music_vae import lstm_models
from magenta.models.music_vae import data
from magenta.models.music_vae.configs import CONFIG_MAP

HParams = contrib_training.HParams

class Config(collections.namedtuple(
        'Config', [
            'model', 'hparams', 'note_sequence_augmenter', 'data_converter',
            'train_examples_path', 'eval_examples_path', 'tfds_name', 'pretrained_path',
            'var_train_pattern', 'encoder_train', 'decoder_train'])):
    """Config class."""
    def values(self):
        """Return value as dictionary."""
        return self._asdict()


Config.__new__.__defaults__ = (None,) * len(Config._fields)


def update_config(config, update_dict):
    """Update config with new values."""
    config_dict = config.values()
    config_dict.update(update_dict)
    return Config(**config_dict)


CONFIG_MAP = dict()

CONFIG_MAP['cat-drums_longbar_small'] = Config(
    model=MusicVAE(lstm_models.BidirectionalLstmEncoder(),
                   lstm_models.HierarchicalLstmDecoder(
            lstm_models.CategoricalLstmDecoder(),
            level_lengths=[16, 16],
            disable_autoregression=True))
    hparams=merge_hparams(
        lstm_models.get_default_hparams(),
        HParams(
            batch_size=8,
            max_seq_len=960,  # 2 bars w/ 16 steps per bar
            z_size=128,
            enc_rnn_size=[512],
            dec_rnn_size=[128, 128],
            free_bits=48,
            max_beta=0.2,
            sampling_schedule='inverse_sigmoid',
            sampling_rate=1000,
        )),
    note_sequence_augmenter=None,
    data_converter=data.DrumsConverter(
        max_bars=100,  # Truncate long drum sequences before slicing.
        # pitch_classes=data.FULL_DRUM_PITCH_CLASSES,
        slice_bars=2,
        steps_per_quarter=4,
        roll_input=True),
    train_examples_path=None,
    eval_examples_path=None,
)