from pathlib import Path

ROOT = Path(__file__).resolve().parent
HYPOTHESIS = ('Prompt-level restrictions may influence agent behaviour, but infrastructure-level '
              'controls should provide a more reliable security boundary by preventing prohibited actions even if attempted.')
REPETITIONS = 10
MAX_STEPS = 12
