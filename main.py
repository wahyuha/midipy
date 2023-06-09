import serial
import fluidsynth

# Set up the serial connection to Arduino
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Replace '/dev/ttyUSB0' with your Arduino's serial port

# Initialize FluidSynth
fs = fluidsynth.Synth()
# Start the audio driver
# fluidsynth.init("driver=alsa")

# Load the SoundFont
sfid = fs.sfload("korg_x5_drums.sf2")

# Set the sample rate to match your audio system
fluidsynth.setting(fs, "synth.sample-rate", 48000)

# Start the synthesizer
fs.start()

# Main loop to receive MIDI messages from Arduino and play sounds
while True:
    line = ser.readline().decode().strip()
    if line.startswith('MIDI:'):
        midi_note = int(line.split(':')[1])
        fs.noteon(0, midi_note, 127)  # Use channel 0, adjust velocity (127 is maximum)
    elif line.startswith('RELEASE:'):
        midi_note = int(line.split(':')[1])
        fs.noteoff(0, midi_note)

# Cleanup
fs.delete()
ser.close()
