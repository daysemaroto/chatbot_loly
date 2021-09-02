import numpy as np
import torch
import re
from matplotlib import pyplot as plt
import importlib

from TTS.tts.utils.visual import plot_spectrogram


def interpolate_vocoder_input(scale_factor, spec):
    """Interpolate spectrogram by the scale factor.
    It is mainly used to match the sampling rates of
    the tts and vocoder models.

    Args:
        scale_factor (float): scale factor to interpolate the spectrogram
        spec (np.array): spectrogram to be interpolated

    Returns:
        torch.tensor: interpolated spectrogram.
    """
    print(" > before interpolation :", spec.shape)
    spec = torch.tensor(spec).unsqueeze(0).unsqueeze(0)  # pylint: disable=not-callable
    spec = torch.nn.functional.interpolate(
        spec, scale_factor=scale_factor, recompute_scale_factor=True, mode="bilinear", align_corners=False
    ).squeeze(0)
    print(" > after interpolation :", spec.shape)
    return spec


def plot_results(y_hat, y, ap, name_prefix):
    """Plot vocoder model results"""

    # select an instance from batch
    y_hat = y_hat[0].squeeze(0).detach().cpu().numpy()
    y = y[0].squeeze(0).detach().cpu().numpy()

    spec_fake = ap.melspectrogram(y_hat).T
    spec_real = ap.melspectrogram(y).T
    spec_diff = np.abs(spec_fake - spec_real)

    # plot figure and save it
    fig_wave = plt.figure()
    plt.subplot(2, 1, 1)
    plt.plot(y)
    plt.title("groundtruth speech")
    plt.subplot(2, 1, 2)
    plt.plot(y_hat)
    plt.title("generated speech")
    plt.tight_layout()
    plt.close()

    figures = {
        name_prefix + "spectrogram/fake": plot_spectrogram(spec_fake),
        name_prefix + "spectrogram/real": plot_spectrogram(spec_real),
        name_prefix + "spectrogram/diff": plot_spectrogram(spec_diff),
        name_prefix + "speech_comparison": fig_wave,
    }
    return figures

def to_camel(text):
    text = text.capitalize()
    return re.sub(r'(?!^)_([a-zA-Z])', lambda m: m.group(1).upper(), text)


def setup_generator(c):
    print(" > Generator Model: {}".format(c.generator_model))
    MyModel = importlib.import_module('TTS.vocoder.models.' +
                                      c.generator_model.lower())
    MyModel = getattr(MyModel, to_camel(c.generator_model))
    if c.generator_model in 'melgan_generator':
        model = MyModel(
            in_channels=c.audio['num_mels'],
            out_channels=1,
            proj_kernel=7,
            base_channels=512,
            upsample_factors=c.generator_model_params['upsample_factors'],
            res_kernel=3,
            num_res_blocks=c.generator_model_params['num_res_blocks'])
    if c.generator_model in 'melgan_fb_generator':
        pass
    if c.generator_model in 'multiband_melgan_generator':
        model = MyModel(
            in_channels=c.audio['num_mels'],
            out_channels=4,
            proj_kernel=7,
            base_channels=384,
            upsample_factors=c.generator_model_params['upsample_factors'],
            res_kernel=3,
            num_res_blocks=c.generator_model_params['num_res_blocks'])
    if c.generator_model in 'fullband_melgan_generator':
        model = MyModel(
            in_channels=c.audio['num_mels'],
            out_channels=1,
            proj_kernel=7,
            base_channels=512,
            upsample_factors=c.generator_model_params['upsample_factors'],
            res_kernel=3,
            num_res_blocks=c.generator_model_params['num_res_blocks'])
    if c.generator_model in 'parallel_wavegan_generator':
        model = MyModel(
            in_channels=1,
            out_channels=1,
            kernel_size=3,
            num_res_blocks=c.generator_model_params['num_res_blocks'],
            stacks=c.generator_model_params['stacks'],
            res_channels=64,
            gate_channels=128,
            skip_channels=64,
            aux_channels=c.audio['num_mels'],
            dropout=0.0,
            bias=True,
            use_weight_norm=True,
            upsample_factors=c.generator_model_params['upsample_factors'])
    return model