# ##### BEGIN GPL LICENSE BLOCK #####
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
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

bl_info = {
    "name": "rPies",
    "author": "Paweł Łyczkowski",
    "version": (1, 0, 0),
    "blender": (2, 71, 4),
    "description": "Enable rPie Menus in blender",
    "category": "User Interface",
}

import bpy
from bpy.types import Menu, Operator
from bpy.props import EnumProperty, IntProperty, FloatProperty, BoolProperty
import bmesh
from mathutils import *
import math

######################
#   Object shading   #
######################

#Wire on selected objects
class WireSelectedAll(bpy.types.Operator):
    bl_idname = "wire.selectedall"
    bl_label = "Wire Selected All"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):

        for obj in bpy.data.objects:
            if bpy.context.selected_objects:
                if obj.select:
                    if obj.show_wire:
                        obj.show_all_edges = False
                        obj.show_wire = False
                    else:
                        obj.show_all_edges = True
                        obj.show_wire = True
            elif not bpy.context.selected_objects:
                if obj.show_wire:
                    obj.show_all_edges = False
                    obj.show_wire = False
                else:
                    obj.show_all_edges = True
                    obj.show_wire = True
        return {'FINISHED'}

#Grid show/hide with axes
class ToggleGridAxis(bpy.types.Operator):
    bl_idname = "scene.togglegridaxis"
    bl_label = "Toggle Grid and Axis in 3D view"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.context.space_data.show_axis_y = not bpy.context.space_data.show_axis_y
        bpy.context.space_data.show_axis_x = not bpy.context.space_data.show_axis_x
        bpy.context.space_data.show_floor = not bpy.context.space_data.show_floor
        return {'FINISHED'}

#Overlays
class MeshDisplayOverlays(bpy.types.Menu):
    bl_idname = "meshdisplay.overlays"
    bl_label = "Mesh Display Overlays"
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context):
        layout = self.layout

        layout.operator("wm.context_toggle", text="Show Faces", icon='FACESEL').data_path = "object.data.show_faces"
        layout.operator("wm.context_toggle", text="Show Edges", icon='FACESEL').data_path = "object.data.show_edges"
        layout.operator("wm.context_toggle", text="Show Crease", icon='FACESEL').data_path = "object.data.show_edge_crease"
        layout.operator("wm.context_toggle", text="Show Seams", icon='FACESEL').data_path = "object.data.show_edge_seams"
        layout.operator("wm.context_toggle", text="Show Sharp", icon='FACESEL').data_path = "object.data.show_edge_sharp"
        layout.operator("wm.context_toggle", text="Show Bevel", icon='FACESEL').data_path = "object.data.show_edge_bevel_weight"
        layout.operator("wm.context_toggle", text="Show Edges Marks", icon='FACESEL').data_path = "object.data.show_freestyle_edge_marks"
        layout.operator("wm.context_toggle", text="Show Face Marks", icon='FACESEL').data_path = "object.data.show_freestyle_face_marks"
        layout.operator("wm.context_toggle", text="Show Weight", icon='FACESEL').data_path = "object.data.show_weight"

#Auto Smooth Menu
class AutoSmoothMenu(bpy.types.Menu):
    bl_idname = "auto.smooth_menu"
    bl_label = "Auto Smooth"
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context):
        layout = self.layout
        layout.operator("wm.context_toggle", text="Auto Smooth", icon='MESH_DATA').data_path = "object.data.use_auto_smooth"
        layout.operator("auto.smooth_30", text="Auto Smooth 30", icon='MESH_DATA')
        layout.operator("auto.smooth_45", text="Auto Smooth 45", icon='MESH_DATA')
        layout.operator("auto.smooth_89", text="Auto Smooth 89", icon='MESH_DATA')

#AutoSmooth_89
class AutoSmooth89(bpy.types.Operator):
    bl_idname = "auto.smooth_89"
    bl_label = "Auto Smooth"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.context.object.data.auto_smooth_angle = 1.55334
        return {'FINISHED'}

#AutoSmooth_30
class AutoSmooth30(bpy.types.Operator):
    bl_idname = "auto.smooth_30"
    bl_label = "Auto Smooth"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.context.object.data.auto_smooth_angle = 0.523599
        return {'FINISHED'}

#AutoSmooth_45
class AutoSmooth45(bpy.types.Operator):
    bl_idname = "auto.smooth_45"
    bl_label = "Auto Smooth"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.context.object.data.auto_smooth_angle = 0.785398
        return {'FINISHED'}

#Normals
class NormalsMenu(bpy.types.Menu):
    bl_idname = "normals.menu"
    bl_label = "Normals Menu"
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context):
        layout = self.layout
        layout.operator("wm.context_toggle", text="Show Normals Vertex", icon='MESH_DATA').data_path = "object.data.show_normal_vertex"
        layout.operator("wm.context_toggle", text="Show Normals Loop", icon='MESH_DATA').data_path = "object.data.show_normal_vertex"
        layout.operator("normalsize.01", text="Normal Size 01")
        layout.operator("normalsize.02", text="Normal Size 02")

#Normal Size 01
class NormalSize01(bpy.types.Operator):
    bl_idname = "normalsize.01"
    bl_label = "Normal Size 01"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.context.scene.tool_settings.normal_size = 0.1
        return {'FINISHED'}

#Normal Size 02
class NormalSize02(bpy.types.Operator):
    bl_idname = "normalsize.02"
    bl_label = "Normal Size 02"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        bpy.context.scene.tool_settings.normal_size = 0.2
        return {'FINISHED'}

######################
#      Shading       #
######################

class ShadingVariable(bpy.types.Operator):
    bl_idname = "object.shadingvariable"
    bl_label = "Shading Variable"
    bl_options = {'REGISTER', 'UNDO'}
    variable = bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.context.space_data.viewport_shade=self.variable
        return {'FINISHED'}

class ShadingSmooth(bpy.types.Operator):
    bl_idname = "shading.smooth"
    bl_label = "Shading Smooth"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.object.mode == "OBJECT":
            bpy.ops.object.shade_smooth()

        elif bpy.context.object.mode == "EDIT":
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.shade_smooth()
            bpy.ops.object.mode_set(mode = 'EDIT')
        return {'FINISHED'}

class ShadingFlat(bpy.types.Operator):
    bl_idname = "shading.flat"
    bl_label = "Shading Flat"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.object.mode == "OBJECT":
            bpy.ops.object.shade_flat()

        elif bpy.context.object.mode == "EDIT":
            bpy.ops.object.mode_set(mode = 'OBJECT')
            bpy.ops.object.shade_flat()
            bpy.ops.object.mode_set(mode = 'EDIT')
        return {'FINISHED'}

###############
# Manipulator #
###############

class VIEW3D_manipulator_set(Operator):
    bl_label = "Set Manipulator"
    bl_idname = "view3d.manipulator_set"

    type = EnumProperty(
            name="Type",
            items=(('TRANSLATE', "Translate", "Use the manipulator for movement transformations"),
                   ('ROTATE', "Rotate", "Use the manipulator for rotation transformations"),
                   ('SCALE', "Scale", "Use the manipulator for scale transformations"),
                   ),
            )

    def execute(self, context):
        # show manipulator if user selects an option
        context.space_data.show_manipulator = True

        context.space_data.transform_manipulators = {self.type}

        return {'FINISHED'}

########
# Pies #
########

# Pie Mode

class VIEW3D_PIE_object_mode(Menu):
    bl_label = "Mode"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        pie.operator_enum("OBJECT_OT_mode_set", "mode")

# Pie Move
class VIEW3D_PIE_move(Menu):
    bl_label = "Manipulator"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()

        pie.operator("view3d.manipulator_set", text="Placeholder").type = 'SCALE'
        pie.operator("view3d.manipulator_set", text="Placeholder").type = 'SCALE'
        pie.operator("view3d.manipulator_set", text="Placeholder").type = 'SCALE'
        pie.operator("view3d.manipulator_set", icon='MAN_TRANS', text="Translate").type = 'TRANSLATE'

# Pie Scale
class VIEW3D_PIE_scale(Menu):
    bl_label = "Manipulator"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        pie.operator("view3d.manipulator_set", text="Placeholder").type = 'SCALE'
        pie.operator("view3d.manipulator_set", text="Placeholder").type = 'SCALE'
        pie.operator("view3d.manipulator_set", text="Placeholder").type = 'SCALE'
        pie.operator("view3d.manipulator_set", icon='MAN_SCALE', text="Scale").type = 'SCALE'

# Pie Rotate
class VIEW3D_PIE_rotate(Menu):
    bl_label = "Manipulator"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        pie.operator("view3d.manipulator_set", text="Placeholder").type = 'SCALE'
        pie.operator("view3d.manipulator_set", text="Placeholder").type = 'SCALE'
        pie.operator("view3d.manipulator_set", text="Placeholder").type = 'SCALE'
        pie.operator("view3d.manipulator_set", icon='MAN_ROT', text="Rotate").type = 'ROTATE'

# Specials
class VIEW3D_PIE_special_menu(Menu):
    bl_label = "Special"
    bl_idname = "VIEW3D_PIE_special_menu"


    def draw(self, context):
        layout = self.layout


        pie = layout.menu_pie()

        box = pie.split().column()
        row = box.row(align=True)
        row.operator("mesh.subdivide", text="Subdivide", icon='NONE').smoothness = 0
        row.operator("mesh.subdivide", text="Smooth", icon='NONE').smoothness = 1
        box.operator("mesh.merge", text="Merge", icon="NONE")
        box.operator("mesh.remove_doubles", text="Remove Doubles", icon="NONE")


        box = pie.split().column()

        box.operator("mesh.hide", text="Hide", icon="NONE").unselected = False
        box.operator("mesh.reveal", text="Revial", icon="NONE")
        box.operator("mesh.select_all", text="Select Inverse", icon="NONE").action = 'INVERT'

        box = pie.split().column()
        box.operator("mesh.flip_normals", text="Flip Normals", icon='NONE')
        box.operator("mesh.vertices_smooth", text="Smooth", icon='NONE')
        box.operator("mesh.vertices_smooth_laplacian", text="Smooth Laplacian", icon='NONE')


        box = pie.split().column()


        box.operator("mesh.inset", text="Insert Faces", icon='NONE')
        box.operator("mesh.bevel", text="Bevel", icon='NONE')
        box.operator("mesh.bridge_edge_loops", text="Bridge Edge Loops", icon='NONE')



        box = pie.split().column()
        box.operator("mesh.blend_from_shape", text="Blend From Shape", icon='NONE')
        box.operator("mesh.shape_propagate_to_all", text="Shape Propagate", icon='NONE')


        box = pie.split().column()


        box.operator("mesh.shortest_path_select", text="Select Shortest Path", icon='NONE')
        box.operator("mesh.sort_elements", text="Sort Mesh Elements", icon='NONE')

        box = pie.split().column()


        box.operator("mesh.symmetrize", text="Symmetrize", icon='NONE')
        box.operator("mesh.symmetry_snap", text="Snat To Symmetry", icon='NONE')

        box = pie.split().column()
        box.operator("mesh.faces_shade_smooth", text="Shade Smooth", icon='NONE')
        box.operator("mesh.faces_shade_flat", text="Shade Flat", icon='NONE')

#Pie Shading - Z
class PieShadingView(Menu):
    bl_idname = "pie.shadingview"
    bl_label = "Pie Shading"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        #4 - LEFT
        pie.operator("object.shadingvariable", text="Material", icon='MATERIAL').variable = 'MATERIAL'
        #6 - RIGHT
        pie.operator("object.shadingvariable", text="Wireframe", icon='WIRE').variable = 'WIREFRAME'
        #2 - BOTTOM
        pie.operator("object.shadingvariable", text="Texture", icon='TEXTURE_SHADED').variable = 'TEXTURED'
        #8 - TOP
        pie.operator("object.shadingvariable", text="Solid", icon='SOLID').variable = 'SOLID'
        #7 - TOP - LEFT
        pie.operator("object.shadingvariable", text="Bounding box", icon='BBOX').variable = 'BOUNDBOX'
        #9 - TOP - RIGHT
        pie.operator("object.shadingvariable", text="Render", icon='SMOOTH').variable = 'RENDERED'
        #1 - BOTTOM - LEFT
        pie.operator("shading.smooth", text="Shade Smooth", icon='SOLID')
        #3 - BOTTOM - RIGHT
        pie.operator("shading.flat", text="Shade Flat", icon='MESH_ICOSPHERE')

#Pie Object Shading- Shift + Z
class PieObjectShading(Menu):
    bl_idname = "pie.objectshading"
    bl_label = "Pie Shading Object"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        #4 - LEFT
        pie.operator("wm.context_toggle", text="Backface Culling", icon="ORTHO").data_path = "space_data.show_backface_culling"
        #6 - RIGHT
        pie.operator("wire.selectedall", text="Wire", icon='WIRE')
        #2 - BOTTOM
        pie.operator("wm.context_toggle", text="Auto Merge", icon='AUTOMERGE_ON').data_path = "scene.tool_settings.use_mesh_automerge"
        #8 - TOP
        pie.operator("wm.context_toggle", text="Xray", icon='META_CUBE').data_path = "object.show_x_ray"
        #7 - TOP - LEFT
        pie.operator("wm.context_toggle", text="Show Normals Faces", icon='FACESEL').data_path = "object.data.show_normal_face"
        #9 - TOP - RIGHT
        pie.operator("wm.context_toggle", text="Hidden Wire", icon='GHOST_ENABLED').data_path = "space_data.show_occlude_wire"
        #1 - BOTTOM - LEFT
        pie.operator("wm.context_toggle", text="Double sided", icon='SNAP_FACE').data_path = "object.data.show_double_sided"
        #3 - BOTTOM - RIGHT
        pie.operator("wm.call_menu_pie", text="Others", icon='GROUP').name="pie.objectshading2"

# Vertices
class VIEW3D_PIE_vertices(Menu):
    bl_label = "Vertices"
    bl_idname = "VIEW3D_PIE_vertices"


    def draw(self, context):
        layout = self.layout


        pie = layout.menu_pie()

        # Left

        box = pie.split().column()
        box.operator("mesh.merge", text="Merge", icon='NONE')
        box.operator("mesh.remove_doubles", text="Remove Doubles", icon='NONE')

        # Right

        box = pie.split().column()
        box.operator("mesh.convex_hull", text="Convex Hull", icon="NONE")

        # Bottom

        box = pie.split().column()
        box.operator("transform.vert_slide", text="Slide", icon='NONE')

        # Top

        box = pie.split().column()
        box.operator("mesh.bevel", text="Bevel", icon="NONE").vertex_only = True
        box.operator("mesh.vert_connect", text="Connect", icon='NONE')

# Edges
class VIEW3D_PIE_edges(Menu):
    bl_label = "Edges"
    bl_idname = "VIEW3D_PIE_edges"


    def draw(self, context):
        layout = self.layout


        pie = layout.menu_pie()

        # Left

        box = pie.split().column()
        box.operator("mesh.mark_seam", text="Mark Seam", icon="NONE").clear = False
        box.operator("mesh.mark_seam", text="Clear Seam", icon="NONE").clear = True
        box.operator("mesh.mark_sharp", text="Mark Sharp", icon="NONE").clear = False
        box.operator("mesh.mark_sharp", text="Clear Sharp", icon="NONE").clear = True

        # Right

        box = pie.split().column()
        box.operator("transform.edge_bevelweight", text="Edge Bevel Weight", icon="NONE")
        box.operator("transform.edge_crease", text="Edge Crease", icon="NONE")
        box.operator("mesh.edge_rotate", text="Rotate Clockwise", icon="NONE").use_ccw = True
        box.operator("mesh.edge_rotate", text="Rotate Anti-Clockwise", icon="NONE").use_ccw = False

        # Bottom

        box = pie.split().column()
        box.operator("transform.edge_slide", text="Slide", icon='NONE')

        # Top

        box = pie.split().column()
        box.operator("mesh.bevel", text="Bevel", icon="NONE").vertex_only = False

# Faces
class VIEW3D_PIE_faces(Menu):
    bl_label = "Faces"
    bl_idname = "VIEW3D_PIE_faces"


    def draw(self, context):
        layout = self.layout


        pie = layout.menu_pie()

        # Left

        box = pie.split().column()
        box.operator("mesh.flip_normals", text="Flip Normals", icon="NONE")
        box.operator("mesh.normals_make_consistent", text="Normals Recalculate Outside", icon="NONE")
        box.operator("mesh.normals_make_consistent", text="Normals Recalculate Inside", icon="NONE").inside = True

        # Right

        box = pie.split().column()
        box.operator("transform.edge_bevelweight", text="Edge Bevel Weight", icon="NONE")
        box.operator("transform.edge_crease", text="Edge Crease", icon="NONE")
        box.operator("mesh.edge_rotate", text="Rotate Clockwise", icon="NONE").use_ccw = True
        box.operator("mesh.edge_rotate", text="Rotate Anti-Clockwise", icon="NONE").use_ccw = False

        # Bottom

        box = pie.split().column()
        box.operator("transform.edge_slide", text="Slide", icon='NONE')

        # Top

        box = pie.split().column()
        box.operator("mesh.inset", text="Inset", icon="NONE")

# Deform
class VIEW3D_PIE_deform(Menu):
    bl_label = "Deform"
    bl_idname = "VIEW3D_PIE_deform"


    def draw(self, context):
        layout = self.layout


        pie = layout.menu_pie()

        # Left

        box = pie.split().column()
        box.operator("transform.shear", text="Shear", icon="NONE")
        box.operator("transform.bend", text="Bend", icon="NONE")
        box.operator("object.vertex_warp", text="Warp", icon="NONE")

        # Right

        box = pie.split().column()
        box.operator("mesh.vertices_smooth", text="Relax", icon="NONE")
        box.operator("transform.to_sphere", text="To Sphere", icon="NONE")

        # Bottom

        box = pie.split().column()
        box.operator("object.vertex_random", text="Randomize", icon="NONE")
        box.operator("mesh.noise", text="Displace With Texture", icon="NONE")

        # Top

        box = pie.split().column()
        box.operator("transform.push_pull", text="Push/Pull", icon="NONE")
        box.operator("transform.shrink_fatten", text="Shrink/Fatten", icon="NONE")

# Cut
class VIEW3D_PIE_cut(Menu):
    bl_label = "Cut"
    bl_idname = "VIEW3D_PIE_cut"


    def draw(self, context):
        layout = self.layout


        pie = layout.menu_pie()

        # Left

        box = pie.split().column()
        box.operator("mesh.loopcut_slide", text="Loop Cut and Slide", icon="NONE")
        box.operator("mesh.knife_tool", text="Knife Selected", icon="NONE").only_selected = True
        #op.use_occlude_geometry = False
        box.operator("mesh.bisect", text="Plane Cut", icon="NONE")

        # Right

        box = pie.split().column()
        box.operator("mesh.knife_project", text="Cut With Object", icon="NONE")
        box.operator("mesh.rip_move", text="Rip", icon="NONE")
        box.operator("mesh.rip_move_fill", text="Rip Fill", icon="NONE")

        # Bottom

        box = pie.split().column()
        box.operator("mesh.edge_split", text = "Rip Along Selected Edges", icon="NONE")

        # Top

        box = pie.split().column()
        box.operator("mesh.split", text = "Separate", icon="NONE")

# Make
class VIEW3D_PIE_make(Menu):
    bl_label = "Make"
    bl_idname = "VIEW3D_PIE_make"


    def draw(self, context):
        layout = self.layout


        pie = layout.menu_pie()

        pie.operator("mesh.bridge_edge_loops", text="Bridge", icon="NONE")
        pie.operator("mesh.fill", text = "Fill With Triangles", icon="NONE")
        pie.operator("mesh.fill_grid", text = "Grid Fill", icon="NONE")

# Extrude
class VIEW3D_PIE_extrude(Menu):
    bl_label = "Extrude"
    bl_idname = "VIEW3D_PIE_extrude"


    def draw(self, context):
        layout = self.layout


        pie = layout.menu_pie()

        pie.operator("view3d.edit_mesh_extrude_move_shrink_fatten", text="Extrude Along Normals")
        pie.operator("view3d.edit_mesh_extrude_individual_move", text="Extrude Individual")

# Snap

class VIEW3D_PIE_snap(Menu):
    bl_label = "Snapping"

    def draw(self, context):
        layout = self.layout

        toolsettings = context.tool_settings
        pie = layout.menu_pie()
        pie.prop(toolsettings, "snap_element", expand=True)
        pie.prop(toolsettings, "use_snap")

# 3d Cursor

class VIEW3D_PIE_cursor(Menu):
    bl_label = "Cursor"

    def draw(self, context):
        layout = self.layout

        toolsettings = context.tool_settings
        pie = layout.menu_pie()

        # Left

        pie.operator("view3d.snap_cursor_to_grid", text="Snap Cursor To Grid")

        # Right

        pie.operator("view3d.snap_cursor_to_active", text="Snap Cursor To Active")

        # Bottom

        pie.operator("view3d.snap_cursor_to_center", text="Snap Cursor To Center")

        # Top

        pie.operator("view3d.snap_cursor_to_selected", text="Snap Cursor To Selected")
        # pie.prop(toolsettings, "use_snap")

### OPERATORS

def r_all_select_modes(context):
    bpy.ops.mesh.select_mode(use_extend=True, use_expand=False, type='VERT', action='ENABLE')
    bpy.ops.mesh.select_mode(use_extend=True, use_expand=False, type='EDGE', action='ENABLE')
    bpy.ops.mesh.select_mode(use_extend=True, use_expand=False, type='FACE', action='ENABLE')

class RAllSelectModes(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "mesh.r_all_select_modes"
    bl_label = "All Select Modes"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        r_all_select_modes(context)
        return {'FINISHED'}



# Keymaps

addon_keymaps = []

# Register

def register():
    bpy.utils.register_module(__name__)

    wm = bpy.context.window_manager

    if wm.keyconfigs.addon:

        # Object Mode

        km = wm.keyconfigs.addon.keymaps.new(name='Object Non-modal')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'TAB', 'HOLD')
        kmi.properties.name = 'VIEW3D_PIE_object_mode'
        kmi = km.keymap_items.new('wm.call_menu_pie', 'W', 'HOLD')
        kmi.properties.name = 'VIEW3D_PIE_move'
        kmi = km.keymap_items.new('wm.call_menu_pie', 'R', 'HOLD')
        kmi.properties.name = 'VIEW3D_PIE_scale'
        kmi = km.keymap_items.new('wm.call_menu_pie', 'E', 'HOLD')
        kmi.properties.name = 'VIEW3D_PIE_rotate'

        #All

        kmi = km.keymap_items.new('wm.call_menu_pie', 'MIDDLEMOUSE', 'HOLD')
        kmi.properties.name = 'VIEW3D_PIE_cursor'
        kmi = km.keymap_items.new('wm.call_menu_pie', 'S', 'HOLD')
        kmi.properties.name = 'VIEW3D_PIE_snap'

        # Edit Mode

        # kmi = km.keymap_items.new('wm.call_menu_pie', 'W', 'HOLD')
        # kmi.properties.name = 'VIEW3D_PIE_special_menu'
        kmi = km.keymap_items.new('wm.call_menu_pie', 'D', 'HOLD')
        kmi.properties.name = 'VIEW3D_PIE_deform'
        kmi = km.keymap_items.new('wm.call_menu_pie', 'C', 'HOLD')
        kmi.properties.name = 'VIEW3D_PIE_cut'
        kmi = km.keymap_items.new('wm.call_menu_pie', 'F', 'HOLD')
        kmi.properties.name = 'VIEW3D_PIE_make'
        kmi = km.keymap_items.new('wm.call_menu_pie', 'A', 'HOLD')
        kmi.properties.name = 'VIEW3D_PIE_extrude'

        kmi = km.keymap_items.new('wm.call_menu_pie', 'ONE', 'HOLD')
        kmi.properties.name = 'VIEW3D_PIE_vertices'
        kmi = km.keymap_items.new('wm.call_menu_pie', 'TWO', 'HOLD')
        kmi.properties.name = 'VIEW3D_PIE_edges'
        kmi = km.keymap_items.new('wm.call_menu_pie', 'THREE', 'HOLD')
        kmi.properties.name = 'VIEW3D_PIE_faces'

        kmi = km.keymap_items.new('mesh.r_all_select_modes', 'FOUR', 'CLICK')

        #Shading
        km = wm.keyconfigs.addon.keymaps.new(name = '3D View Generic', space_type = 'VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'Z', 'HOLD')
        kmi.properties.name = "pie.shadingview"

        #Object shading
        km = wm.keyconfigs.addon.keymaps.new(name = '3D View Generic', space_type = 'VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu_pie', 'Z', 'PRESS', shift=True)
        kmi.properties.name = "pie.objectshading"

        addon_keymaps.append(km)


def unregister():
    bpy.utils.unregister_module(__name__)


    wm = bpy.context.window_manager

    if wm.keyconfigs.addon:
        for km in addon_keymaps:
            for kmi in km.keymap_items:
                km.keymap_items.remove(kmi)

            wm.keyconfigs.addon.keymaps.remove(km)

    # clear the list
    del addon_keymaps[:]

if __name__ == "__main__":
    register()
