#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sample main for STT.

Source: https://stt.readthedocs.io/en/latest/Python-Examples.html
"""

import argparse
import shlex
import subprocess
import sys
import wave
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # pylint: disable=all
    from typing import Any

import numpy
from stt import Model  # type: ignore

try:
    from shlex import quote
except ImportError:
    from pipes import quote


def convert_samplerate(audio_path: str, ds_rate: str) -> tuple[str, numpy.ndarray[Any, Any]]:
    """Convert sample audio to desired sample rate."""
    sox_cmd = f'sox {quote(audio_path)} --type raw --bits 16 --channels 1\
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


def main() -> None:
    """Run to get text from audio file."""
    parser = argparse.ArgumentParser(description='Running Coqui STT inference.')
    parser.add_argument(
        '--model',
        required=True,
        help='Path to the model (protocol buffer binary file)',
    )
    parser.add_argument(
        '--scorer',
        required=False,
        help='Path to the external scorer file',
    )
    parser.add_argument(
        '--audio',
        required=True,
        help='Path to the audio file to run (WAV format)',
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
    data_model = Model(args.model)

    if args.beam_width:
        data_model.setBeamWidth(args.beam_width)

    desired_sample_rate = data_model.sampleRate()

    if args.scorer:
        print(f'Loading scorer from files {args.scorer}', file=sys.stderr)
        data_model.enableExternalScorer(args.scorer)

        if args.lm_alpha and args.lm_beta:
            data_model.setScorerAlphaBeta(args.lm_alpha, args.lm_beta)

    if args.hot_words:
        print('Adding hot-words', file=sys.stderr)
        for word_boost in args.hot_words.split(','):
            word, boost = word_boost.split(':')
            data_model.addHotWord(word, float(boost))

    fin = wave.open(args.audio, 'rb')
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
        fs_new, audio = convert_samplerate(args.audio, desired_sample_rate)
    else:
        audio = numpy.frombuffer(fin.readframes(fin.getnframes()), numpy.int16)

    fin.close()

    print('Running inference.', file=sys.stderr)
    print(data_model.stt(audio))


if __name__ == '__main__':
    main()
