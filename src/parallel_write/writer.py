"""Parallel writer."""

from concurrent.futures import ThreadPoolExecutor, as_completed


class Writer:
    """Writes to given file handles `files` in parallel."""

    def __init__(self, files, max_workers=None):
        """Parallel writer.

        files: list of the input file handles to write to.
        max_workers: the maximum number of workers in the threadpool. Defaults
            to the length of `files`.
        """
        if max_workers is None:
            max_workers = len(files)
        self._files = files
        self._executor = ThreadPoolExecutor(max_workers)
        self._iterators = []

    def __getattr__(self, attr):
        """Proxy the methods/properties to the underlying file objects."""
        if callable(getattr(self._files[0], attr)):
            # if the attribute is a callable, return a function which evaluates
            # the given method on all files in parallel and expects that
            # they return the same value
            # for eg. read(), write(), seek() etc.
            def _do(*args, **kwargs):
                futures = {self._executor.submit(getattr(f, attr), *args, **kwargs): f for f in self._files}
                res = [future.result() for future in as_completed(futures)]
                # only check methods which must return the same value
                if attr not in ("fileno",):
                    assert res.count(res[0]) == len(res)
                return res[0]
            return _do
        else:
            # if the attribute is not a callable (property), collect the values,
            # check for equality and return it
            # for eg. mode, name, closed etc.
            res = [getattr(f, attr) for f in self._files]
            assert res.count(res[0]) == len(res)
            return res[0]

    def __enter__(self):
        """Context manager enter."""
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Context manager exit."""
        self.close()

    def __iter__(self):
        """Initialize the iterators."""
        self._iterators = [iter(f) for f in self._files]
        return self

    def __next__(self):
        """Read from the iterators."""
        res = [next(i) for i in self._iterators]
        assert res.count(res[0]) == len(res)
        return res[0]
