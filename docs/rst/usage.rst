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

An example with many files::

	from parallel_write import Writer
	
	w = Writer([open(f"/tmp/test{i}", "w+") for i in range(10)])
	w.write("foo")
	w.seek(0)
	assert w.read() == "foo"

This will write `foo` to all files and also read and check them to be the same.

You can use different file-like objects as long they implement the Python file interface::

	import s3fs
	from parallel_write import Writer

	s3 = s3fs.S3FileSystem().open("s3bucket/test/file", "wb")
	with Writer([open(f"/tmp/test", "wb"), s3]) as w:
		w.write(b"foo")

This will write `foo` to S3 and to `/tmp/test` in parallel.
Note, that all files should be opened in the same way (here: binary), otherwise, you'll get errors.