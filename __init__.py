# ##### BEGIN GPL LICENSE BLOCK #####{{{1
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110 - 1301, USA.
#
# ##### END GPL LICENSE BLOCK #####}}}1
bl_info = {
        "name":        "Node Label",
        "description": "For naming or labeling of things.",
        "author":      "Shams Kitz <dustractor@gmail.com>",
        "version":     (0,1),
        "blender":     (2,80,0),
        "tracker_url": "https://github.com/dustractor/nodelabel",
        "category":    "System"
    }

import bpy

def _(c=None,r=[]):
    if c:
        r.append(c)
        return c
    return r


@_
class NODELABEL_OT_nodelabel(bpy.types.Operator):
    bl_idname = "nodelabel.nodelabel"
    bl_label = "nodelabel nodelabel"
    bl_options = {"INTERNAL"}

    txt_buffer: bpy.props.StringProperty()

    def draw(self,context):
        layout = self.layout
        layout.activate_init = True
        layout.prop(self,"txt_buffer")

    @classmethod
    def poll(self,context):
        return context.active_node

    def invoke(self,context,event):
        self.txt_buffer = ""
        return context.window_manager.invoke_props_dialog(self)

    def execute(self,context):
        if not len(self.txt_buffer):
            return {"CANCELLED"}
        context.active_node.label = self.txt_buffer
        return {"FINISHED"}

def linked_output_socket_names(node):
    names = []
    for output in node.outputs:
        for link in output.links:
            names.append(link.to_socket.name)
    return names
        

@_
class NODELABEL_OT_from_upstream_socket(bpy.types.Operator):
    bl_idname = "nodelabel.from_upstream_socket"
    bl_label = "nodelabel from upstream socket"
    bl_options = {"INTERNAL"}

    @classmethod
    def poll(self,context):
        return context.active_node and linked_output_socket_names(context.active_node)
    def execute(self,context):
        node = context.active_node
        names = linked_output_socket_names(node) 
        total = len(names)
        if node.label not in names:
            node.label = names[0]
        elif total > 1:
            cur_index = names.index(node.label)
            next_index = (cur_index + 1) % total
            node.label = names[next_index]
        else:
            node.label = names[0]

        return {"FINISHED"}



def hotkey_things(do=False,t=[]):
    if do:
        keymaps = bpy.context.window_manager.keyconfigs.addon.keymaps
        km = keymaps.new("Node Editor",space_type="NODE_EDITOR")
        mods = dict(ctrl=True,alt=True,shift=True)
        kmi = km.keymap_items.new(NODELABEL_OT_nodelabel.bl_idname,
                                  "L","PRESS",**mods)
        t.append((km,kmi))
        kmi = km.keymap_items.new(NODELABEL_OT_from_upstream_socket.bl_idname,
                                  "K","PRESS",**mods)
        t.append((km,kmi))
    else:
        for km,kmi in t:
            km.keymap_items.remove(kmi)
        t.clear()

def register():
    list(map(bpy.utils.register_class,_()))
    hotkey_things(do=True)

def unregister():
    list(map(bpy.utils.unregister_class,_()))
    hotkey_things()
