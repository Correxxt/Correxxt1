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


def test_custom_dictionary(tmp_path):
    dict_file = tmp_path / 'dict.txt'
    # Add a word and ensure it is recognised
    run_correxxt(['--dict', str(dict_file), '--add-word', 'tst'])
    out = run_correxxt(['--dict', str(dict_file), 'tst'])
    assert 'No spelling errors detected.' in out

    # Remove the word and check again
    run_correxxt(['--dict', str(dict_file), '--remove-word', 'tst'])
    out = run_correxxt(['--dict', str(dict_file), 'tst'])
    assert 'tst ->' in out
