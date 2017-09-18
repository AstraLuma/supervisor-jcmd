# supervisor-jcmd

This package is an extension for [Supervisor](http://supervisord.org)
that provides the ability to `jcmd` against managed services.

## Installation

Release packages are [available](http://pypi.python.org/pypi/supervisor-jcmd)
on the Python Package Index (PyPI).  You can download them from there or you
can use `pip` to automatically install or upgrade:

    $ pip install -U supervisor-jcmd

After installing the package, you must modify your `supervisord.conf` file
to register the RPC interface and `supervisorctl` plugin:

    [rpcinterface:jcmd]
    supervisor.rpcinterface_factory = supervisor_jcmd.rpcinterface:make_rpcinterface

    [ctlplugin:jcmd]
    supervisor.ctl_factory = supervisor_jcmd.controllerplugin:make_controllerplugin

After modifying the `supervisord.conf` file, both your `supervisord` instance and
`supervisorctl` must be restarted for these changes to take effect.

## XML-RPC

The jcmd functions allow java management commands to be run over Supervisor's
XML-RPC interface. The following Python interpreter session demonstrates the usage.

First, a `ServerProxy` object must be configured.  If supervisord is listening on
an inet socket, `ServerProxy` configuration is simple:

    >>> import xmlrpclib
    >>> s = xmlrpclib.ServerProxy('http://localhost:9001')

If supervisord is listening on a domain socket, `ServerProxy` can be configured
with `SupervisorTransport`.  The URL must still be supplied and be a valid HTTP
URL to appease `ServerProxy`, but it is superfluous.

    >>> import xmlrpclib
    >>> from supervisor.xmlrpc import SupervisorTransport
    >>> s = xmlrpclib.ServerProxy('http://127.0.0.1/whatever',
    ... SupervisorTransport('', '', 'unix:///path/to/supervisor.sock'))

Once `ServerProxy` has been configured appropriately, we can now exercise
`supervisor-jcmd`:

    TODO

The key must be a string and cannot be zero-length.  The value may be any
type that can be marshalled by XML-RPC.

Please consult the inline source documentation for the specifics of each
command available.

## Supervisorctl

You can also interact with the jcmd using `supervisorctl`.  The `help` command
with no arguments will list the available jcmd commands:

    supervisor> help
    ...

    jcmd commands (type help <topic>):
    ===================================
    jcmd

Each command provides a thin wrapper around an XML-RPC method:

    TODO

## Author

[Jamie Bliss](http://github.com/astronouth7303)

Forked from `supervisor_cache` by [Mike Naberezny](http://github.com/mnaberez)
