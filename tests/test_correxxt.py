import subprocess
import sys


def run_correxxt(args):
    result = subprocess.run([sys.executable, 'correxxt.py'] + args, capture_output=True, text=True)
    assert result.returncode == 0
    return result.stdout.strip()


def test_correxxt_detects_errors():
    out = run_correxxt(['Ths', 'is', 'a', 'tst'])
    assert 'ths ->' in out
    assert 'tst ->' in out


def test_correxxt_no_errors():
    out = run_correxxt(['This', 'is', 'fine'])
    assert 'No spelling errors detected.' in out
