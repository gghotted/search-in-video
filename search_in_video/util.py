from datetime import time
import tempfile


def sec2time(sec, micro_sec):
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return time(h, m, s, int(micro_sec))


def load_as_tempfile(file):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        for chunk in file.chunks():
            f.write(chunk)
    return f.name