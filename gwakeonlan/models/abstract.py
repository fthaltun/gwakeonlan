##
#     Project: gWakeOnLAN
# Description: Wake up your machines using Wake on LAN
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2009-2022 Fabio Castelli
#     License: GPL-3+
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

from gi.repository import Gtk


class ModelAbstract(object):
    COL_KEY = 0

    def __init__(self, model):
        self.model = model
        # Fill the rows' dictionary with the model items
        self.rows = {}
        for row in self.model:
            name = row[self.COL_KEY]
            self.rows[name] = self.model.get_iter(row.path)

    def __iter__(self):
        """Iter the model"""
        return iter(self.model)

    def clear(self):
        """Clear the model"""
        self.rows.clear()
        return self.model.clear()

    def add_data(self, item):
        """Add a new row to the model if it doesn't exist"""
        pass

    def set_data(self, treeiter, item):
        """Update an existing TreeIter"""
        old_key = self.get_key(treeiter)
        # If the new name differs from the old name then update the
        # TreeIters map in self.rows
        if old_key != item.name:
            self.rows.pop(old_key)
            self.rows[item.name] = treeiter

    def get_key(self, treeiter):
        """Get the name from a TreeIter"""
        return self.model[treeiter][self.COL_KEY]

    def get_iter(self, name):
        """Get a TreeIter from a name"""
        return self.rows.get(name)

    def get_model_data(self, treeiter, column):
        """Get model data from a TreeIter column"""
        return self.model[self.get_path_from_iter(treeiter)][column]

    def get_model_row(self, treeiter):
        """Get a TreeModelRow from a TreeIter"""
        return self.model[treeiter]

    def get_path(self, treeiter):
        """Get the path from a TreeIter"""
        return self.get_model_row(treeiter).path

    def get_path_by_name(self, name):
        """Get the path from a name"""
        return self.get_model_row(self.get_iter(name)).path

    def get_path_from_iter(self, treeiter):
        """Return a TreePath from a TreeIter"""
        return (treeiter.path
                if type(treeiter) is Gtk.TreeModelRow
                else treeiter)

    def remove(self, treeiter):
        """Remove a TreeIter"""
        self.rows.pop(self.get_key(treeiter))
        self.model.remove(treeiter)

    def set_model_data(self, treeiter, column, value):
        """Set model data for a TreeIter column"""
        self.model[self.get_path_from_iter(treeiter)][column] = value

    def dump(self):
        """Extract the model data to a dict object"""
        pass

    def load(self, items):
        """Load the model data from a dict object"""
        for key in sorted(items.iterkeys()):
            self.add_data(items[key])

    def count(self):
        """Return the number of items in the model"""
        return len(self.model)
