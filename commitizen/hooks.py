import os

from commitizen import cmd, out
from commitizen.exceptions import RunHookError


def run(hooks, _env_prefix="CZ_", **env):
    if isinstance(hooks, str):
        hooks = [hooks]

    for name, value in env.items():
        name = _env_prefix + name.upper()
        value = str(value) if value is not None else ""
        os.environ[name] = value

    for hook in hooks:
        out.info(f"Running hook '{hook}'")

        c = cmd.run(hook)

        if c.out:
            out.write(c.out)
        if c.err:
            out.error(c.err)

        if c.return_code != 0:
            raise RunHookError(f"Running hook '{hook}' failed")
