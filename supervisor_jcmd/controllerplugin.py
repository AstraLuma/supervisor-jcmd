from supervisor.supervisorctl import ControllerPluginBase
import pprint
import shlex


class JcmdControllerPlugin(ControllerPluginBase):
    def __init__(self, controller):
        self.ctl = controller
        self.jcmd = controller.get_server_proxy('jcmd')

    # cache_clear

    def do_jcmd(self, args):
        args = shlex.split(args)
        if len(args) < 2:
            return self.help_cache_clear()

        value = self.jcmd.jcmd(args[0], args[1:])
        self._pprint(value)

    def help_cache_clear(self):
        self.ctl.output("jcmd <name> <args>\t"
                        "Run jcmd")

    def _pprint(self, what):
        pprinted = pprint.pformat(what)
        self.ctl.output(pprinted)


def make_controllerplugin(controller, **config):
    return JcmdControllerPlugin(controller)
