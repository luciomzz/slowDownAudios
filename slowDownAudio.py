from pydub import AudioSegment
import numpy as np
import subprocess
import os 

def slow_down_and_pitch_stretch(input_path, slowdown_factor, output_path):
    # Load the audio using pydub
    audio = AudioSegment.from_file(input_path)
    
    output_path_wav = output_path.replace(".mp3", ".wav")

    slowed_audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate / slowdown_factor)
    }).set_frame_rate(audio.frame_rate)

    # Export the original audio to a temporary file in wav format
    # This will create a temporary file that is updated each time you use the script
    temp_path = "temp_original_audio.wav"
    slowed_audio.export(temp_path, format="wav")

    # Calculate the required pitch shift in semitones
    pitch_shift_semitones = 12 * np.log2(slowdown_factor)

    # Use soundstretch for slowing down and pitch correction
    subprocess.run(["soundstretch", temp_path, output_path_wav, f"-tempo={0}", f"-pitch={pitch_shift_semitones}"])

    wav_audio = AudioSegment.from_wav(output_path_wav)
    wav_audio.export(output_path, format="mp3")
    os.remove(output_path_wav)
    os.remove(temp_path)

    return output_path

if __name__ == "__main__":
    # Make sure you put the right paths here 
    input_path = 'test1/testHelloOriginal.mp3'
    output_path = 'test1/testHelloFaster_0.93.mp3'

    # The higher the slower, I recommend not going above 1.2. For high values artifacts can appear.
    slowdown_output = 0.93
    slow_down_and_pitch_stretch(input_path, slowdown_output, output_path)