import os
import re

from pydub import AudioSegment
import subprocess

def slow_down_and_pitch_stretch(file_path, slowdown_factor, output_path):
    # Load the audio using pydub
    audio = AudioSegment.from_file(file_path)

    slowed_audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate / slowdown_factor)
    }).set_frame_rate(audio.frame_rate)

    # Export the original audio to a temporary file in wav format
    temp_path = "temp_original_audio.wav"
    slowed_audio.export(temp_path, format="wav")

    # Calculate the required pitch shift in semitones
    pitch_shift_semitones = 12 * np.log2(slowdown_factor)

    # Use soundstretch for slowing down and pitch correction
    subprocess.run(["soundstretch", temp_path, output_path, f"-tempo={0}", f"-pitch={pitch_shift_semitones}"])

    return output_path

