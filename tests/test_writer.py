# -*- coding: utf-8 -*-

"""Performs general tests."""

from parallel_write import Writer
import hashlib
import os
import pytest
import random
import string
import tempfile


@pytest.fixture
def random_bytes(size=1024):
    """Return random bytes."""
    return os.urandom(size)


@pytest.fixture
def random_string(size=1024):
    """Return random string."""
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=size))


def is_binary(f):
    """Check if the file object is opened in binary mode or not."""
    return "b" in f.mode


def compare_files(files, hashfunc=hashlib.sha256):
    """Compares the contents of two file objects."""
    digest = None
    for f in files:
        h = hashfunc()
        f.seek(0)
        while True:
            data = f.read(64 * 1024)
            if not data:
                break
            if is_binary(f):
                h.update(data)
            else:
                h.update(data.encode("ascii"))
        if digest is not None:
            assert digest == h.digest()
        else:
            digest = h.digest()

    return True


def test_write_string(random_string):
    """Test writes with string."""
    files = [tempfile.NamedTemporaryFile(mode="w+") for i in range(128)]
    w = Writer(files)
    w.write(random_string)
    w.flush()
    assert compare_files(files)
    w.close()


def test_write_bytes(random_bytes):
    """Tests writes with binary."""
    files = [tempfile.NamedTemporaryFile(mode="w+b") for i in range(128)]
    w = Writer(files)
    w.write(random_bytes)
    w.flush()
    assert compare_files(files)
    w.close()


def test_mode_error(random_string):
    """Writing string to a binary file must raise an exception."""
    files = [tempfile.NamedTemporaryFile(mode="w+"),
             tempfile.NamedTemporaryFile(mode="w+b")]
    w = Writer(files)
    with pytest.raises(TypeError):
        w.write(random_string)


def test_encoding_error():
    """Writing UTF-8 string to an ascii file must raise an exception."""
    files = [tempfile.NamedTemporaryFile(mode="w+"),
             tempfile.NamedTemporaryFile(mode="w+", encoding="ascii")]
    w = Writer(files)
    with pytest.raises(UnicodeEncodeError):
        w.write("árvíztűrő_tükörfúrógép")


def test_tell(random_bytes):
    """Test tell."""
    files = [tempfile.NamedTemporaryFile(mode="w+b") for i in range(128)]
    w = Writer(files)
    w.write(random_bytes)
    assert w.tell() == len(random_bytes)


def test_seek(random_bytes):
    """Test seek."""
    files = [tempfile.NamedTemporaryFile(mode="w+b") for i in range(128)]
    w = Writer(files)
    w.write(random_bytes)
    pos = int(len(random_bytes) / 2)
    assert w.seek(pos) == pos
    assert w.tell() == pos
    assert w.seek(0, os.SEEK_SET) == 0
    assert w.seek(0, os.SEEK_END) == len(random_bytes)


def test_read(random_bytes):
    """Test read."""
    files = [tempfile.NamedTemporaryFile(mode="w+b") for i in range(128)]
    w = Writer(files)
    w.write(random_bytes)
    pos = int(len(random_bytes) / 2)
    w.seek(pos)
    data = w.read(32)
    assert data == random_bytes[pos:pos + 32]


def test_truncate(random_bytes):
    """Test truncate."""
    files = [tempfile.NamedTemporaryFile(mode="w+b") for i in range(128)]
    w = Writer(files)
    w.write(random_bytes)
    pos = int(len(random_bytes) / 2)
    w.truncate(pos)
    assert w.seek(0, os.SEEK_END) == pos


def test_closed(random_bytes):
    """Test closed."""
    files = [tempfile.NamedTemporaryFile(mode="w+b") for i in range(128)]
    w = Writer(files)
    w.write(random_bytes)
    assert not w.closed
    w.close()
    assert w.closed


def test_writable():
    """Test writable."""
    files = [tempfile.NamedTemporaryFile(mode="w+b") for i in range(128)]
    w = Writer(files)
    assert w.writable()


def test_not_writable():
    """Test not writable."""
    files = [tempfile.NamedTemporaryFile(mode="r") for i in range(128)]
    w = Writer(files)
    assert not w.writable()


def test_readable():
    """Test readable."""
    files = [tempfile.NamedTemporaryFile(mode="w") for i in range(128)]
    w = Writer(files)
    assert not w.readable()


def test_fileno():
    """Test fileno."""
    files = [tempfile.NamedTemporaryFile(mode="a+") for i in range(128)]
    w = Writer(files)
    assert w.fileno()


def test_context_manager(random_bytes):
    """Test context manager."""
    files = [tempfile.NamedTemporaryFile(mode="w+b") for i in range(128)]
    with Writer(files) as w:
        assert w.write(random_bytes) == len(random_bytes)
        assert not w.closed
    assert w.closed


def test_iter(random_bytes):
    """Test iterator."""
    files = [tempfile.NamedTemporaryFile(mode="w+b") for i in range(128)]
    w = Writer(files)
    w.write(random_bytes)
    w.flush()
    i = iter(w)
    with pytest.raises(StopIteration):
        # we're at the end of the file, this must raise StopIteration
        next(i)
    # verify that we get back the written data
    w.seek(0)
    i = iter(w)
    data = []
    for d in w:
        data.append(d)
    assert b"".join(data) == random_bytes


def test_workers(random_bytes):
    """Test setting the number of workers."""
    files = [tempfile.NamedTemporaryFile(mode="w+b") for i in range(128)]
    w = Writer(files, max_workers=1)
    w.write(random_bytes)
    pos = int(len(random_bytes) / 2)
    w.seek(pos)
    data = w.read(32)
    assert data == random_bytes[pos:pos + 32]
