# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 by Simmo Saan <simmo.saan@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

#
# History:
#
# 2019-06-27, Simmo Saan <simmo.saan@gmail.com>
#   version 0.3: fix completions
# 2015-07-24, Simmo Saan <simmo.saan@gmail.com>
#   version 0.2: add command /help
# 2015-07-24, Simmo Saan <simmo.saan@gmail.com>
#   version 0.1: initial script
#

"""
Run /key commands on sets of keys by regex
"""

from __future__ import print_function

SCRIPT_NAME = "key_regex"
SCRIPT_AUTHOR = "Simmo Saan <simmo.saan@gmail.com>"
SCRIPT_VERSION = "0.3"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC = "Run /key commands on sets of keys by regex"

SCRIPT_COMMAND = "key_regex"

IMPORT_OK = True

try:
	import weechat
except ImportError:
	print("This script must be run under WeeChat.")
	print("Get WeeChat now at: https://weechat.org/")
	IMPORT_OK = False

import re

def command_cb(data, buffer, args):
	cmd, args = tuple(args.split(" ", 1))

	if cmd == "list" or cmd == "listctxt":
		ctxt = ""
		if cmd == "listctxt":
			ctxt, args = tuple(args.split(" ", 1))

		r = re.compile(args)

		keys = weechat.infolist_get("key", "", ctxt)
		cnt = 0
		while weechat.infolist_next(keys):
			key = weechat.infolist_string(keys, "key")

			if (r.search(key)):
				cnt += 1

		prntr = args
		if cmd == "list":
			weechat.prnt("", "%d key bindings matching \"%s\"" % (cnt, prntr))
		elif cmd == "listctxt":
			weechat.prnt("", "%d key bindings for context \"%s\" matching \"%s\"" % (cnt, ctxt, prntr))

		weechat.infolist_reset_item_cursor(keys)
		while weechat.infolist_next(keys):
			key = weechat.infolist_string(keys, "key")
			command = weechat.infolist_string(keys, "command")

			if (r.search(key)):
				weechat.prnt("", "  %s %s=>%s %s" % (key, weechat.color("green"), weechat.color("reset"), command))

		weechat.infolist_free(keys)

	elif cmd == "reset" or cmd == "resetctxt":
		ctxt = ""
		if cmd == "resetctxt":
			ctxt, args = tuple(args.split(" ", 1))

		r = re.compile(args)

		keys = weechat.infolist_get("key", "", ctxt)
		while weechat.infolist_next(keys):
			key = weechat.infolist_string(keys, "key")

			if (r.search(key)):
				if cmd == "reset":
					weechat.command("", "/key reset %s" % key)
				elif cmd == "resetctxt":
					weechat.command("", "/key resetctxt %s %s" % (ctxt, key))

		weechat.infolist_free(keys)

	elif cmd == "unbind" or cmd == "unbindctxt":
		ctxt = ""
		if cmd == "unbindctxt":
			ctxt, args = tuple(args.split(" ", 1))

		r = re.compile(args)

		keys = weechat.infolist_get("key", "", ctxt)
		while weechat.infolist_next(keys):
			key = weechat.infolist_string(keys, "key")

			if (r.search(key)):
				if cmd == "unbind":
					weechat.command("", "/key unbind %s" % key)
				elif cmd == "unbindctxt":
					weechat.command("", "/key unbindctxt %s %s" % (ctxt, key))

		weechat.infolist_free(keys)

	return weechat.WEECHAT_RC_OK

if __name__ == "__main__" and IMPORT_OK:
	if weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, "", ""):
		weechat.hook_command(
			SCRIPT_COMMAND,
			SCRIPT_DESC,
"""list <regex>
 || listctxt <context> <regex>
 || reset <regex>
 || resetctxt <context> <regex>
 || unbind <regex>
 || unbindctxt <context> <regex>""",
"""      list: list keys
  listctxt: list keys for given context
     reset: reset keys to default binding
 resetctxt: reset keys to default binding, for given context
    unbind: remove key bindings
unbindctxt: remove key bindings, for given context

All commands take a regular expression to match keys against as an argument.""",
"""list
 || listctxt %(keys_contexts)
 || reset
 || resetctxt %(keys_contexts)
 || unbind
 || unbindctxt %(keys_contexts)""".replace("\n", ""),
			"command_cb", "")
