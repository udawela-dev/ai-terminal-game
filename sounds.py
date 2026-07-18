"""Sound engine for Treasure Hunter Quest.

Generates all music and sound effects procedurally using pygame.
No external audio files required — everything is synthesised at runtime.
Falls back gracefully when no audio device is available.
"""

import pygame

# Try to initialise the mixer — gracefully degrade if no audio device
_AUDIO_AVAILABLE = True
try:
    pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
except pygame.error:
    _AUDIO_AVAILABLE = False

if _AUDIO_AVAILABLE:
    import struct
    import io

    # ============================================
    # Helper: generate a WAV byte stream in memory
    # ============================================

    def _make_wav(samples: list[int], sample_rate: int = 44100) -> io.BytesIO:
        """Convert a list of 16-bit PCM samples into an in-memory WAV file."""
        num_samples = len(samples)
        data_size = num_samples * 2
        buf = io.BytesIO()
        buf.write(b"RIFF")
        buf.write(struct.pack("<I", 36 + data_size))
        buf.write(b"WAVE")
        buf.write(b"fmt ")
        buf.write(struct.pack("<I", 16))
        buf.write(struct.pack("<H", 1))        # PCM
        buf.write(struct.pack("<H", 1))        # mono
        buf.write(struct.pack("<I", sample_rate))
        buf.write(struct.pack("<I", sample_rate * 2))
        buf.write(struct.pack("<H", 2))
        buf.write(struct.pack("<H", 16))
        buf.write(b"data")
        buf.write(struct.pack("<I", data_size))
        for s in samples:
            buf.write(struct.pack("<h", max(-32768, min(32767, s))))
        buf.seek(0)
        return buf

    # ============================================
    # Note frequencies
    # ============================================

    NOTES = {
        "C3": 131, "D3": 147, "E3": 165, "F3": 175, "G3": 196,
        "A3": 220, "B3": 247,
        "C4": 262, "D4": 294, "E4": 330, "F4": 349, "G4": 392,
        "A4": 440, "B4": 494,
        "C5": 523, "D5": 587, "E5": 659, "F5": 698, "G5": 784,
        "A5": 880, "B5": 988,
        "C6": 1047,
    }

    def _tone(freq: float, duration: float, volume: float = 0.3,
              sample_rate: int = 44100) -> list[int]:
        """Generate a sine-wave tone with a smooth fade-in/out envelope."""
        import math
        num_samples = int(sample_rate * duration)
        fade = int(sample_rate * 0.02)
        return [
            int(
                volume * 32767 * math.sin(2 * math.pi * freq * (i / sample_rate))
                * (i / fade if i < fade else (num_samples - i) / fade if i > num_samples - fade else 1)
            )
            for i in range(num_samples)
        ]

    # ============================================
    # Sound effect generators
    # ============================================

    def _generate_collect_sound() -> pygame.mixer.Sound:
        """Bright ascending arpeggio for collecting an item."""
        bpm = 600
        beat = 60.0 / bpm
        samples = (
            _tone(NOTES["E5"], beat * 0.15, 0.4) +
            _tone(NOTES["G5"], beat * 0.15, 0.4) +
            _tone(NOTES["C6"], beat * 0.25, 0.35)
        )
        return pygame.mixer.Sound(buffer=_make_wav(samples).getbuffer())

    def _generate_hazard_sound() -> pygame.mixer.Sound:
        """Low rumbling buzz for hitting a hazard."""
        samples = _tone(NOTES["C3"], 0.5, 0.5) + _tone(NOTES["G3"], 0.4, 0.4)
        return pygame.mixer.Sound(buffer=_make_wav(samples).getbuffer())

    def _generate_win_sound() -> pygame.mixer.Sound:
        """Triumphant ascending fanfare."""
        bpm = 200
        beat = 60.0 / bpm
        samples = (
            _tone(NOTES["C4"], beat, 0.35) +
            _tone(NOTES["E4"], beat, 0.35) +
            _tone(NOTES["G4"], beat, 0.35) +
            _tone(NOTES["C5"], beat * 2, 0.4)
        )
        return pygame.mixer.Sound(buffer=_make_wav(samples).getbuffer())

    def _generate_lose_sound() -> pygame.mixer.Sound:
        """Sad descending melody."""
        bpm = 200
        beat = 60.0 / bpm
        samples = (
            _tone(NOTES["E5"], beat, 0.35) +
            _tone(NOTES["D5"], beat, 0.35) +
            _tone(NOTES["C5"], beat, 0.35) +
            _tone(NOTES["C4"], beat * 2, 0.4)
        )
        return pygame.mixer.Sound(buffer=_make_wav(samples).getbuffer())

    def _generate_move_sound() -> pygame.mixer.Sound:
        """Short soft click for each step."""
        return pygame.mixer.Sound(buffer=_make_wav(_tone(NOTES["A5"], 0.03, 0.1)).getbuffer())

    # ============================================
    # Background music — classical-style loop
    # ============================================

    def _generate_bgm() -> pygame.mixer.Sound:
        """Gentle classical melody inspired by a simplified minuet
        (Bach / Notebook for Anna Magdalena). Soft sine-wave piano."""
        bpm = 140
        beat = 60.0 / bpm

        melody_notes = [
            ("E4", 1), ("G4", 1), ("A4", 0.5), ("G4", 0.5), ("E4", 1), ("F4", 1),
            ("G4", 1), ("F4", 0.5), ("E4", 0.5), ("D4", 1), ("E4", 1), ("C4", 1),
            ("A4", 1), ("G4", 0.5), ("A4", 0.5), ("B4", 1), ("C5", 1), ("B4", 1),
            ("A4", 1), ("G4", 1), ("F4", 0.5), ("E4", 0.5), ("D4", 1), ("C4", 1),
        ]

        bass_notes = [
            ("C3", 4), ("G3", 4),
            ("C3", 4), ("G3", 4),
            ("F3", 4), ("C3", 4),
            ("F3", 4), ("C3", 4),
        ]

        melody_samples = []
        for note, beats in melody_notes:
            melody_samples += _tone(NOTES[note], beat * beats * 0.9, 0.18)

        bass_samples = []
        for note, beats in bass_notes:
            bass_samples += _tone(NOTES[note], beat * beats * 0.9, 0.10)

        max_len = max(len(melody_samples), len(bass_samples))
        melody_samples += [0] * (max_len - len(melody_samples))
        bass_samples += [0] * (max_len - len(bass_samples))

        mixed = [m + b for m, b in zip(melody_samples, bass_samples)]

        return pygame.mixer.Sound(buffer=_make_wav(mixed).getbuffer())


# ============================================
# Public API
# ============================================

class SoundEngine:
    """Pre-loads all sounds so the game runs without delay.
    Falls back to silent no-ops when no audio device is available."""

    def __init__(self) -> None:
        self._available = _AUDIO_AVAILABLE
        if self._available:
            self.bgm = _generate_bgm()
            self.collect = _generate_collect_sound()
            self.hazard = _generate_hazard_sound()
            self.win = _generate_win_sound()
            self.lose = _generate_lose_sound()
            self.move = _generate_move_sound()

    def play_bgm(self) -> None:
        if self._available:
            self.bgm.play(-1)

    def stop_bgm(self) -> None:
        if self._available:
            self.bgm.stop()

    def play_collect(self) -> None:
        if self._available:
            self.collect.play()

    def play_hazard(self) -> None:
        if self._available:
            self.hazard.play()

    def play_win(self) -> None:
        if self._available:
            self.stop_bgm()
            self.win.play()

    def play_lose(self) -> None:
        if self._available:
            self.stop_bgm()
            self.lose.play()

    def play_move(self) -> None:
        if self._available:
            self.move.play()
