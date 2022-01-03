=====
Usage
=====

To use ``parallel_write``::

	from parallel_write import Writer
	
`Writer` will be a proxy object, which proxies all method calls to the given file(-like)
objects.
It also asserts that their return value matches and if not, raises an error.

An example with one file::

	from parallel_write import Writer
	w = Writer([open("/tmp/test", "w+")])
	w.write("foo")
	w.seek(0)
	assert w.read() == "foo"

An example with many files:

	from parallel_write import Writer
	w = Writer([open(f"/tmp/test{i}", "w+") for i in range(10)])
	w.write("foo")
	w.seek(0)
	assert w.read() == "foo"

This will write `foo` to all files and also read and check them.

You can use different file-like objects as long they implement the Python file interface:

