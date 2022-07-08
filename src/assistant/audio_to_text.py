#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sample main for STT.

Source: https://stt.readthedocs.io/en/latest/Python-Examples.html
"""
import shlex
import subprocess
import sys
import wave
from typing import Tuple  # noqa: TC002

import numpy
from stt import Model

try:
    from shlex import quote
except ImportError:
    from pipes import quote


def cvt_smpl_rt(path: str, ds_rate: str) -> Tuple[str, numpy.ndarray[any, any]]:  # type: ignore
    """Convert sample audio to desired sample rate."""
    sox_cmd = f'sox {quote(path)} --type raw --bits 16 --channels 1\
         --rate {ds_rate} --encoding signed-integer --endian little\
             --compression 0.0 --no-dither - '

    try:
        output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as exception:
        raise RuntimeError(f'SoX returned non-zero status: {exception.stderr}') from exception
    except OSError as exception:
        raise OSError(
            exception.errno,
            f'SoX not found, use {ds_rate}hz files or install it: {exception.strerror}',
        ) from exception

    return ds_rate, numpy.frombuffer(output, numpy.int16)


def audio_to_text(model_path: str, audio_path: str) -> str:
    """Convert audio from source file path to str."""
    print(f'Loading model from file {model_path}', file=sys.stderr)
    data_model = Model(model_path)

    desired_sample_rate = data_model.sampleRate()

    fin = wave.open(audio_path, 'rb')
    fs_orig = fin.getframerate()
    if fs_orig != desired_sample_rate:
        print(
            (
                f'Warning: original sample rate ({fs_orig}) \
                is different than {desired_sample_rate}hz. \
                Resampling might produce \
                erratic speech recognition.'
            ),
            file=sys.stderr,
        )
        fs_new, audio = cvt_smpl_rt(audio_path, desired_sample_rate)
    else:
        audio = numpy.frombuffer(fin.readframes(fin.getnframes()), numpy.int16)

    fin.close()

    print('Running inference.', file=sys.stderr)
    return str(data_model.stt(audio))
