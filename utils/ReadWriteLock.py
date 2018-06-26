import threading


class ReadWriteLock:
    """
    A lock object that allows many simultaneous "read locks", but
    only one "write lock."
    """

    class Lock:

        def __init__(self, acquire_fn, release_fn):
            self._enter_fn = acquire_fn
            self._exit_fn = release_fn

        def __enter__(self):
            self._enter_fn()
            return None

        def __exit__(self, exc_type, exc_val, exc_tb):
            self._exit_fn()
            return False

    def __init__(self):
        self._read_ready = threading.Condition(threading.Lock())
        self._readers = 0

        # convenience objects
        self.read_lock = ReadWriteLock.Lock(self.acquire_read,
                                            self.release_read)
        self.write_lock = ReadWriteLock.Lock(self.acquire_write,
                                             self.release_write)

    def acquire_read(self):
        """ Acquire a read lock. Blocks only if a thread has
        acquired the write lock. """
        self._read_ready.acquire()
        try:
            self._readers += 1
        finally:
            self._read_ready.release()

    def release_read(self):
        """ Release a read lock. """
        self._read_ready.acquire()
        try:
            self._readers -= 1
            if not self._readers:
                self._read_ready.notifyAll()
        finally:
            self._read_ready.release()

    def acquire_write(self):
        """ Acquire a write lock. Blocks until there are no
        acquired read or write locks. """
        self._read_ready.acquire()
        while self._readers > 0:
            self._read_ready.wait()

    def release_write(self):
        """ Release a write lock. """
        self._read_ready.release()
