from supervisor.options import split_namespec
from supervisor.states import SupervisorStates
from supervisor.xmlrpc import Faults
from supervisor.xmlrpc import RPCError

import subprocess

API_VERSION = '0.1'


class JcmdNamespaceRPCInterface:
    """ A Supervisor RPC interface that provides the ability
    to cache abritrary data in the Supervisor instance as key/value pairs.
    """

    def __init__(self, supervisord):
        self.supervisord = supervisord
        self.cache = {}

    def _update(self, text):
        self.update_text = text  # for unit tests, mainly

        if isinstance(self.supervisord.options.mood, int) and \
           self.supervisord.options.mood < SupervisorStates.RUNNING:
            raise RPCError(Faults.SHUTDOWN_STATE)

    # RPC API methods

    def getAPIVersion(self):
        """ Return the version of the RPC API used by supervisor_cache

        @return string  version
        """
        self._update('getAPIVersion')
        return API_VERSION

    def _getGroupAndProcess(self, name):
        # get process to start from name
        group_name, process_name = split_namespec(name)

        group = self.supervisord.process_groups.get(group_name)
        if group is None:
            raise RPCError(Faults.BAD_NAME, name)

        if process_name is None:
            return group, None

        process = group.processes.get(process_name)
        if process is None:
            raise RPCError(Faults.BAD_NAME, name)

        return group, process

    def jcmd(self, name, cmd):
        """ Store a string value in the cache, referenced by 'key'

        @param  array cmd  A list of strings to give to jcmd
        @return struct     Results of the command
        """
        self._update(cmd)

        _, process = self._getGroupAndProcess(name)

        # TODO: Raise an error if it's not RUNNING

        pid = process.pid

        proc = subprocess.Popen(['jcmd', 'pid'] + list(cmd),
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)

        out, _ = proc.communicate()

        return {
            'status': proc.returncode,
            'output': out,
        }


def make_rpcinterface(supervisord, **config):
    return JcmdNamespaceRPCInterface(supervisord)
