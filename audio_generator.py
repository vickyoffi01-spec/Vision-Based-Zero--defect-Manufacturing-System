"""
audio_generator.py
Pure Python Audio Synthesizer (Zero External Dependencies)
Generates high-tech industrial audio cues encoded as Base64 WAV data URIs
for instantaneous playback inside the Streamlit web dashboard.
"""

import io
import math
import struct
import wave
import base64
import random

def _create_wav(samples: list[float], sample_rate: int = 22050) -> str:
    """Encodes float samples in [-1.0, 1.0] to a Base64 data:audio/wav URI."""
    buffer = io.BytesIO()
    with wave.open(buffer, 'w') as wav_file:
        wav_file.setnchannels(1)        # Mono
        wav_file.setsampwidth(2)       # 16-bit
        wav_file.setframerate(sample_rate)
        
        # Convert float to signed 16-bit PCM integer
        raw_data = bytearray()
        for s in samples:
            clamped = max(-1.0, min(1.0, s))
            int_val = int(clamped * 32767.0)
            raw_data.extend(struct.pack('<h', int_val))
            
        wav_file.writeframes(raw_data)
        
    encoded = base64.b64encode(buffer.getvalue()).decode('ascii')
    return f"data:audio/wav;base64,{encoded}"

def get_mechanical_click_audio() -> str:
    """Generates a crisp mechanical relay click / microswitch sound (~60ms)."""
    sample_rate = 22050
    duration = 0.06
    total_samples = int(sample_rate * duration)
    samples = []
    
    for i in range(total_samples):
        t = i / sample_rate
        # Transient snap (high frequency burst decaying exponentially)
        decay = math.exp(-t * 90.0)
        snap = math.sin(2 * math.pi * 3200 * t) * 0.7
        body = math.sin(2 * math.pi * 850 * t) * 0.3
        noise = (random.random() * 2.0 - 1.0) * 0.25 * math.exp(-t * 180.0)
        samples.append((snap + body + noise) * decay)
        
    return _create_wav(samples, sample_rate)

def get_pneumatic_eject_audio() -> str:
    """Generates an industrial pneumatic rejector burst/hiss sound (~150ms)."""
    sample_rate = 22050
    duration = 0.15
    total_samples = int(sample_rate * duration)
    samples = []
    
    for i in range(total_samples):
        t = i / sample_rate
        # Rapid attack, exponential decay pressurized air hiss
        if t < 0.01:
            env = t / 0.01
        else:
            env = math.exp(-(t - 0.01) * 22.0)
            
        noise = (random.random() * 2.0 - 1.0) * 0.8
        thump = math.sin(2 * math.pi * 140 * t) * 0.6 * math.exp(-t * 30.0)
        samples.append((noise * 0.7 + thump * 0.5) * env)
        
    return _create_wav(samples, sample_rate)

def get_defect_alarm_audio() -> str:
    """Generates a high-tech dual-tone industrial defect alarm beep (~180ms)."""
    sample_rate = 22050
    duration = 0.18
    total_samples = int(sample_rate * duration)
    samples = []
    
    for i in range(total_samples):
        t = i / sample_rate
        env = math.exp(-t * 14.0)
        # Dual frequency discordant tone (1450 Hz + 1850 Hz) for high urgency alert
        tone = 0.5 * math.sin(2 * math.pi * 1450 * t) + 0.5 * math.sin(2 * math.pi * 1850 * t)
        samples.append(tone * env * 0.85)
        
    return _create_wav(samples, sample_rate)

# Pre-generate singletons for fast retrieval
CLICK_URI = get_mechanical_click_audio()
EJECT_URI = get_pneumatic_eject_audio()
ALARM_URI = get_defect_alarm_audio()

def get_audio_html(sound_type: str = "click") -> str:
    """Returns an invisible autoplay HTML5 audio element."""
    uri_map = {
        "click": CLICK_URI,
        "eject": EJECT_URI,
        "alarm": ALARM_URI,
    }
    uri = uri_map.get(sound_type, CLICK_URI)
    return f"""
    <audio autoplay style="display:none;">
        <source src="{uri}" type="audio/wav">
    </audio>
    """
