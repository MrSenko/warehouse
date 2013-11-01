# Copyright 2013 Donald Stufft
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals

import logging
import os.path

import webassets.ext.jinja2
import webassets.script
import werkzeug.serving

import warehouse
import warehouse.migrations.cli

from warehouse.serving import WSGIRequestHandler


class ServeCommand:

    def __call__(self, app, host, port, reloader, debugger):
        werkzeug.serving.run_simple(
            host, port, app,
            use_reloader=reloader,
            use_debugger=debugger,
            request_handler=WSGIRequestHandler,
        )

    def create_parser(self, parser):
        parser.add_argument(
            "-H", "--host",
            default="localhost",
            help="The host to bind the server to, defaults to localhost",
        )
        parser.add_argument(
            "-p", "--port",
            default=9000,
            type=int,
            help="The port to bind the server to, defaults to 6000",
        )
        parser.add_argument(
            "--no-reload",
            default=True,
            action="store_false",
            dest="reloader",
            help="Disable automatic reloader",
        )
        parser.add_argument(
            "--no-debugger",
            default=True,
            action="store_false",
            dest="debugger",
            help="Disable Werkzeug debugger",
        )


class CollectStaticCommand:

    def __call__(self, app):
        env = app.templates.assets_environment

        cmd = webassets.script.BuildCommand(
            webassets.script.CommandLineEnvironment(
                env,
                logging.getLogger("webassets.build"),
            ),
        )
        return cmd(production=not app.config.debug)


__commands__ = {
    "migrate": warehouse.migrations.cli.__commands__,
    "serve": ServeCommand(),
    "collectstatic": CollectStaticCommand(),
}
