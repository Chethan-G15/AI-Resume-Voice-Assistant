import sounddevice as sd
import numpy as np


SAMPLE_RATE = 16000
DURATION = 5
MICROPHONE_DEVICE = 1


print("Speak normally for 5 seconds...")
print("Recording...")


audio = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="float32",
    device=MICROPHONE_DEVICE
)

sd.wait()


audio = audio.flatten()

max_volume = np.max(np.abs(audio))
average_volume = np.mean(np.abs(audio))


print("\nRecording completed.")

print(f"Maximum volume: {max_volume:.4f}")
print(f"Average volume: {average_volume:.4f}")


if max_volume < 0.01:
    print("\nWARNING: Microphone volume is extremely low.")

elif max_volume < 0.05:
    print("\nMicrophone volume is low.")

else:
    print("\nMicrophone is capturing audio normally.")
    