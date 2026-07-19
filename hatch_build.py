# noqa: INP001
import os
import shutil
import subprocess
from pathlib import Path
from sys import stderr

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        super().initialize(version, build_data)
        stderr.write('>>> Building Open Webui frontend\n')

        # Skip frontend build if the build output already exists
        build_dir = Path(__file__).parent / 'build'
        if build_dir.exists() and (build_dir / 'index.html').exists():
            stderr.write('### Skipping npm build — build/ directory already exists\n')
            return

        npm = shutil.which('npm')
        if npm is None:
            raise RuntimeError('NodeJS `npm` is required for building Open Webui but it was not found')
        stderr.write('### npm install\n')
        subprocess.run([npm, 'install', '--force'], check=True)  # noqa: S603
        stderr.write('\n### npm run build\n')
        os.environ['APP_BUILD_HASH'] = version
        # Use increased heap for large SvelteKit build
        env = os.environ.copy()
        env['NODE_OPTIONS'] = env.get('NODE_OPTIONS', '--max-old-space-size=4096')
        subprocess.run([npm, 'run', 'build'], check=True, env=env)  # noqa: S603
