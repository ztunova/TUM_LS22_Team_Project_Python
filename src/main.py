#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sample main for STT.

Source: https://stt.readthedocs.io/en/latest/Python-Examples.html
"""

from __future__ import absolute_import, division, print_function

import argparse
import json
import shlex
import subprocess
import sys
import wave
from timeit import default_timer as timer
from typing import Tuple, Any

import numpy as np
from stt import Model

try:
    from shlex import quote
except ImportError:
    from pipes import quote


def convert_samplerate(audio_path: str, desired_sample_rate: type) -> Tuple[type, np.ndarray[Any, Any]]:
    """Convert sample audio to desired sample rate."""
    sox_cmd = f'sox {quote(audio_path)} --type raw --bits 16 --channels 1\
         --rate {desired_sample_rate} --encoding signed-integer --endian little\
             --compression 0.0 --no-dither - '
    try:
        output = subprocess.check_output(shlex.split(sox_cmd), stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f'SoX returned non-zero status: {e.stderr}')
    except OSError as e:
        raise OSError(
            e.errno,
            f'SoX not found, use {desired_sample_rate}hz files or install it: {e.strerror}',
        )

    return desired_sample_rate, np.frombuffer(output, np.int16)

def main() -> None:
    """Run to get text from audio file."""
    parser = argparse.ArgumentParser(description='Running Coqui STT inference.')
    parser.add_argument(
        '--model', required=True, help='Path to the model (protocol buffer binary file)',
    )
    parser.add_argument(
        '--scorer', required=False, help='Path to the external scorer file',
    )
    parser.add_argument(
        '--audio', required=True, help='Path to the audio file to run (WAV format)',
    )
    parser.add_argument('--beam_width', type=int, help='Beam width for the CTC decoder')
    parser.add_argument(
        '--lm_alpha',
        type=float,
        help='Language model weight (lm_alpha).\
             If not specified, use default from the scorer package.',
    )
    parser.add_argument(
        '--lm_beta',
        type=float,
        help='Word insertion bonus (lm_beta).\
             If not specified, use default from the scorer package.',
    )
    parser.add_argument(
        '--extended',
        required=False,
        action='store_true',
        help='Output string from extended metadata',
    )
    parser.add_argument(
        '--json',
        required=False,
        action='store_true',
        help='Output json from metadata with timestamp of each word',
    )
    parser.add_argument('--hot_words', type=str, help='Hot-words and their boosts.')
    args = parser.parse_args()

    print(f'Loading model from file {args.model}', file=sys.stderr)
    model_load_start = timer()
    # sphinx-doc: python_ref_model_start
    ds = Model(args.model)
    # sphinx-doc: python_ref_model_stop
    model_load_end = timer() - model_load_start
    print(f'Loaded model in {model_load_end:.3}s.', file=sys.stderr)

    if args.beam_width:
        ds.setBeamWidth(args.beam_width)

    desired_sample_rate = ds.sampleRate()

    if args.scorer:
        print(f'Loading scorer from files {args.scorer}', file=sys.stderr)
        scorer_load_start = timer()
        ds.enableExternalScorer(args.scorer)
        scorer_load_end = timer() - scorer_load_start
        print(f'Loaded scorer in {scorer_load_end:.3}s.', file=sys.stderr)

        if args.lm_alpha and args.lm_beta:
            ds.setScorerAlphaBeta(args.lm_alpha, args.lm_beta)

    if args.hot_words:
        print('Adding hot-words', file=sys.stderr)
        for word_boost in args.hot_words.split(','):
            word, boost = word_boost.split(':')
            ds.addHotWord(word, float(boost))

    fin = wave.open(args.audio, 'rb')
    fs_orig = fin.getframerate()
    if fs_orig != desired_sample_rate:
        print(
            ('Warning: original sample rate ({}) is different than {}hz. Resampling might produce\
             erratic speech recognition.').format(
                fs_orig, desired_sample_rate,
            ),
            file=sys.stderr,
        )
        fs_new, audio = convert_samplerate(args.audio, desired_sample_rate)
    else:
        audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)

    audio_length = fin.getnframes() * (1 / fs_orig)
    fin.close()

    print('Running inference.', file=sys.stderr)

    inference_start = timer()
    print(ds.stt(audio))
    inference_end = timer() - inference_start

    print(
        ('Inference took %0.3fs for %0.3fs audio file.') % (inference_end, audio_length),
        file=sys.stderr,
    )


if __name__ == '__main__':
    main()
