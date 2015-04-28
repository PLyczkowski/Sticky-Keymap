# ##### BEGIN GPL LICENSE BLOCK #####
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {'name': 'Modifier Listbox Test',
           'author': 'russcript',
           'version': (0, 0, 1),
           'blender': (2, 71, 0),
           'location': 'Properties Editor > Modifiers Panel',
           'warning': 'Work in Progress',
           #'wiki_url': '',
           #'tracker_url': '',
           'description': "An addon to test the Listbox GUI for modifiers and physics",
           'category': ''}









import bpy
from bpy.types import Menu,Panel,UIList
from bpy.app.translations import pgettext_iface as iface_


from bl_ui.properties_physics_common import (point_cache_ui,
                                             effector_weights_ui)
                                             
                                      
                                             

mod_icon_map = {m.identifier: m.icon for m in bpy.types.OBJECT_OT_modifier_add.bl_rna.properties['type'].enum_items}


class OBJECT_OT_modifier_move(bpy.types.Operator): 
    bl_idname = "object.modifier_action"
    bl_label = "Modifier Action"

    action = bpy.props.EnumProperty(
        items=(
            ('UP', "Up", ""),
            ('DOWN', "Down", ""),
            ('REMOVE', "Remove", "")
        )
    )

    def invoke(self, context, event):

        ob = context.object
        idx = ob.modifier_active_index
        
        try:
            mod = ob.modifiers[idx]
        except IndexError:
            pass
        else:
            if self.action == 'DOWN' and idx < len(ob.modifiers) - 1:
                if bpy.ops.object.modifier_move_down(modifier=mod.name) == {'FINISHED'}:
                    ob.modifier_active_index += 1
            elif self.action == 'UP' and idx >= 1:
                if bpy.ops.object.modifier_move_up(modifier=mod.name) == {'FINISHED'}:
                    ob.modifier_active_index -= 1                
            elif self.action == 'REMOVE':
                bpy.ops.object.modifier_remove(modifier=mod.name)
                if idx >= 1:
                    ob.modifier_active_index -= 1
            

        return {"FINISHED"}
        
count = 0


class MODIFIER_UL_listtype(bpy.types.UIList): #custom UIList type for modifiers
    def draw_item(self, context, layout, data, item, active_data, active_propname, index):
        
        modifier = item
        
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            global count
            count=count+1
            layout.prop(modifier, "name", text=str(count), emboss=False, icon=mod_icon_map[modifier.type])

            icon = 'RESTRICT_RENDER_OFF' if item.show_render else 'RESTRICT_RENDER_ON'
            layout.prop(item, "show_render", text="", icon=icon, emboss=False)

            icon = 'RESTRICT_VIEW_OFF' if item.show_viewport else 'RESTRICT_VIEW_ON'
            layout.prop(item, "show_viewport", text="", icon=icon, emboss=False)

            icon = 'EDITMODE_HLT' if item.show_in_editmode else 'OBJECT_DATAMODE'
            layout.prop(item, "show_in_editmode", text="", icon=icon, emboss=False)

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label("", icon=mod_icon_map[modifier.type])


class OBJECT_PT_Modifiers(bpy.types.Panel): #panel draw class
    """Creates a Panel in the Object properties window"""
    bl_label = ""
    bl_idname = "OBJECT_PT_Modifiers"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "modifier"
    bl_options = {"HIDE_HEADER"}


    def draw(self, context):
        layout = self.layout

        ob = bpy.context.object
        idx = ob.modifier_active_index
        rows = 2
        
        try:
            mod = ob.modifiers[idx]
            label = mod.name + " Properties:"
        except IndexError:
            label = ""
            pass

        row = layout.row()
        row.template_list("MODIFIER_UL_listtype", "", ob, "modifiers", ob, "modifier_active_index", rows=rows)
        col = row.column(align=True)
        col.operator("object.modifier_add", icon='ZOOMIN', text="")
        col.operator("object.modifier_action", icon='ZOOMOUT', text="").action = 'REMOVE'
        col.separator()
        if len(ob.modifiers) > 1:
            col.operator("object.modifier_action", icon='TRIA_UP', text="").action = 'UP'
            col.operator("object.modifier_action", icon='TRIA_DOWN', text="").action = 'DOWN'



        
        row = layout.row()
        layout.label(text = label)
        
  

        for md in ob.modifiers:
            if md.name == mod.name:
                box = self.layout #layout.template_modifier(md)
                if box:
                # match enum type to our functions, avoids a lookup table.
                    getattr(self, md.type)(box, ob, md)

    # the mt.type enum is (ab)used for a lookup on function names
    # ...to avoid lengthy if statements
    # so each type must have a function here.

    def ARMATURE(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.label(text="Object:")
        col.prop(md, "object", text="")
        col.prop(md, "use_deform_preserve_volume")

        col = split.column()
        col.label(text="Bind To:")
        col.prop(md, "use_vertex_groups", text="Vertex Groups")
        col.prop(md, "use_bone_envelopes", text="Bone Envelopes")

        layout.separator()

        split = layout.split()

        row = split.row(align=True)
        row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
        sub = row.row(align=True)
        sub.active = bool(md.vertex_group)
        sub.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

        split.prop(md, "use_multi_modifier")

    def ARRAY(self, layout, ob, md):
        layout.prop(md, "fit_type")

        if md.fit_type == 'FIXED_COUNT':
            layout.prop(md, "count")
        elif md.fit_type == 'FIT_LENGTH':
            layout.prop(md, "fit_length")
        elif md.fit_type == 'FIT_CURVE':
            layout.prop(md, "curve")

        layout.separator()

        split = layout.split()

        col = split.column()
        col.prop(md, "use_constant_offset")
        sub = col.column()
        sub.active = md.use_constant_offset
        sub.prop(md, "constant_offset_displace", text="")

        col.separator()

        col.prop(md, "use_merge_vertices", text="Merge")
        sub = col.column()
        sub.active = md.use_merge_vertices
        sub.prop(md, "use_merge_vertices_cap", text="First Last")
        sub.prop(md, "merge_threshold", text="Distance")

        col = split.column()
        col.prop(md, "use_relative_offset")
        sub = col.column()
        sub.active = md.use_relative_offset
        sub.prop(md, "relative_offset_displace", text="")

        col.separator()

        col.prop(md, "use_object_offset")
        sub = col.column()
        sub.active = md.use_object_offset
        sub.prop(md, "offset_object", text="")

        layout.separator()

        layout.prop(md, "start_cap")
        layout.prop(md, "end_cap")

    def BEVEL(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.prop(md, "width")
        col.prop(md, "segments")
        col.prop(md, "profile")

        col = split.column()
        col.prop(md, "use_only_vertices")
        col.prop(md, "use_clamp_overlap")

        layout.label(text="Limit Method:")
        layout.row().prop(md, "limit_method", expand=True)
        if md.limit_method == 'ANGLE':
            layout.prop(md, "angle_limit")
        elif md.limit_method == 'VGROUP':
            layout.label(text="Vertex Group:")
            layout.prop_search(md, "vertex_group", ob, "vertex_groups", text="")

        layout.label(text="Width Method:")
        layout.row().prop(md, "offset_type", expand=True)

    def BOOLEAN(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.label(text="Operation:")
        col.prop(md, "operation", text="")

        col = split.column()
        col.label(text="Object:")
        col.prop(md, "object", text="")

    def BUILD(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.prop(md, "frame_start")
        col.prop(md, "frame_duration")
        col.prop(md, "use_reverse")

        col = split.column()
        col.prop(md, "use_random_order")
        sub = col.column()
        sub.active = md.use_random_order
        sub.prop(md, "seed")

    def MESH_CACHE(self, layout, ob, md):
        layout.prop(md, "cache_format")
        layout.prop(md, "filepath")

        layout.label(text="Evaluation:")
        layout.prop(md, "factor", slider=True)
        layout.prop(md, "deform_mode")
        layout.prop(md, "interpolation")

        layout.label(text="Time Mapping:")

        row = layout.row()
        row.prop(md, "time_mode", expand=True)
        row = layout.row()
        row.prop(md, "play_mode", expand=True)
        if md.play_mode == 'SCENE':
            layout.prop(md, "frame_start")
            layout.prop(md, "frame_scale")
        else:
            time_mode = md.time_mode
            if time_mode == 'FRAME':
                layout.prop(md, "eval_frame")
            elif time_mode == 'TIME':
                layout.prop(md, "eval_time")
            elif time_mode == 'FACTOR':
                layout.prop(md, "eval_factor")

        layout.label(text="Axis Mapping:")
        split = layout.split(percentage=0.5, align=True)
        split.alert = (md.forward_axis[-1] == md.up_axis[-1])
        split.label("Forward/Up Axis:")
        split.prop(md, "forward_axis", text="")
        split.prop(md, "up_axis", text="")
        split = layout.split(percentage=0.5)
        split.label(text="Flip Axis:")
        row = split.row()
        row.prop(md, "flip_axis")

    def CAST(self, layout, ob, md):
        split = layout.split(percentage=0.25)

        split.label(text="Cast Type:")
        split.prop(md, "cast_type", text="")

        split = layout.split(percentage=0.25)

        col = split.column()
        col.prop(md, "use_x")
        col.prop(md, "use_y")
        col.prop(md, "use_z")

        col = split.column()
        col.prop(md, "factor")
        col.prop(md, "radius")
        col.prop(md, "size")
        col.prop(md, "use_radius_as_size")

        split = layout.split()

        col = split.column()
        col.label(text="Vertex Group:")
        col.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
        col = split.column()
        col.label(text="Control Object:")
        col.prop(md, "object", text="")
        if md.object:
            col.prop(md, "use_transform")

    def CLOTH(self, layout, ob, md):
        #layout.label(text="Settings are inside the Physics tab")
        return True


    def COLLISION(self,layout ,ob,md):

        md = bpy.context.collision

        split = layout.split()

        coll = md.settings

        if coll:
            settings = bpy.context.object.collision

            layout.active = settings.use

            split = layout.split()

            col = split.column()
            col.label(text="Particle:")
            col.prop(settings, "permeability", slider=True)
            col.prop(settings, "stickiness")
            col.prop(settings, "use_particle_kill")
            col.label(text="Particle Damping:")
            sub = col.column(align=True)
            sub.prop(settings, "damping_factor", text="Factor", slider=True)
            sub.prop(settings, "damping_random", text="Random", slider=True)

            col.label(text="Particle Friction:")
            sub = col.column(align=True)
            sub.prop(settings, "friction_factor", text="Factor", slider=True)
            sub.prop(settings, "friction_random", text="Random", slider=True)

            col = split.column()
            col.label(text="Soft Body and Cloth:")
            sub = col.column(align=True)
            sub.prop(settings, "thickness_outer", text="Outer", slider=True)
            sub.prop(settings, "thickness_inner", text="Inner", slider=True)

            col.label(text="Soft Body Damping:")
            col.prop(settings, "damping", text="Factor", slider=True)

            col.label(text="Force Fields:")
            col.prop(settings, "absorption", text="Absorption")


    def CURVE(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.label(text="Object:")
        col.prop(md, "object", text="")
        col = split.column()
        col.label(text="Vertex Group:")
        col.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
        layout.label(text="Deformation Axis:")
        layout.row().prop(md, "deform_axis", expand=True)

    def DECIMATE(self, layout, ob, md):
        decimate_type = md.decimate_type

        row = layout.row()
        row.prop(md, "decimate_type", expand=True)

        if decimate_type == 'COLLAPSE':
            layout.prop(md, "ratio")

            split = layout.split()
            row = split.row(align=True)
            row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
            row.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

            split.prop(md, "use_collapse_triangulate")
        elif decimate_type == 'UNSUBDIV':
            layout.prop(md, "iterations")
        else:  # decimate_type == 'DISSOLVE':
            layout.prop(md, "angle_limit")
            layout.prop(md, "use_dissolve_boundaries")
            layout.label("Delimit:")
            row = layout.row()
            row.prop(md, "delimit")

        layout.label(text=iface_("Face Count: %d") % md.face_count, translate=False)

    def DISPLACE(self, layout, ob, md):
        has_texture = (md.texture is not None)

        col = layout.column(align=True)
        col.label(text="Texture:")
        col.template_ID(md, "texture", new="texture.new")

        split = layout.split()

        col = split.column(align=True)
        col.label(text="Direction:")
        col.prop(md, "direction", text="")
        col.label(text="Vertex Group:")
        col.prop_search(md, "vertex_group", ob, "vertex_groups", text="")

        col = split.column(align=True)
        col.active = has_texture
        col.label(text="Texture Coordinates:")
        col.prop(md, "texture_coords", text="")
        if md.texture_coords == 'OBJECT':
            col.label(text="Object:")
            col.prop(md, "texture_coords_object", text="")
        elif md.texture_coords == 'UV' and ob.type == 'MESH':
            col.label(text="UV Map:")
            col.prop_search(md, "uv_layer", ob.data, "uv_textures", text="")

        layout.separator()

        row = layout.row()
        row.prop(md, "mid_level")
        row.prop(md, "strength")

    def DYNAMIC_PAINT(self, layout, ob, md):
        #layout.label(text="Settings are inside the Physics tab")
        return {"FINISHED"}

    def EDGE_SPLIT(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.prop(md, "use_edge_angle", text="Edge Angle")
        sub = col.column()
        sub.active = md.use_edge_angle
        sub.prop(md, "split_angle")

        split.prop(md, "use_edge_sharp", text="Sharp Edges")

    def EXPLODE(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.label(text="Vertex group:")
        col.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
        sub = col.column()
        sub.active = bool(md.vertex_group)
        sub.prop(md, "protect")
        col.label(text="Particle UV")
        col.prop_search(md, "particle_uv", ob.data, "uv_textures", text="")

        col = split.column()
        col.prop(md, "use_edge_cut")
        col.prop(md, "show_unborn")
        col.prop(md, "show_alive")
        col.prop(md, "show_dead")
        col.prop(md, "use_size")

        layout.operator("object.explode_refresh", text="Refresh")

    def FLUID_SIMULATION(self, layout, ob, md):
        #layout.label(text="Settings are inside the Physics tab")
        return {"FINISHED"}

    def HOOK(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.label(text="Object:")
        col.prop(md, "object", text="")
        if md.object and md.object.type == 'ARMATURE':
            col.label(text="Bone:")
            col.prop_search(md, "subtarget", md.object.data, "bones", text="")
        col = split.column()
        col.label(text="Vertex Group:")
        col.prop_search(md, "vertex_group", ob, "vertex_groups", text="")

        layout.separator()

        split = layout.split()

        col = split.column()
        col.prop(md, "falloff")
        col.prop(md, "force", slider=True)

        col = split.column()
        col.operator("object.hook_reset", text="Reset")
        col.operator("object.hook_recenter", text="Recenter")

        if ob.mode == 'EDIT':
            layout.separator()
            row = layout.row()
            row.operator("object.hook_select", text="Select")
            row.operator("object.hook_assign", text="Assign")

    def LAPLACIANDEFORM(self, layout, ob, md):
        is_bind = md.is_bind

        layout.prop(md, "iterations")

        row = layout.row()
        row.active = not is_bind
        row.label(text="Anchors Vertex Group:")

        row = layout.row()
        row.enabled = not is_bind
        row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")

        layout.separator()

        row = layout.row()
        row.enabled = bool(md.vertex_group)
        row.operator("object.laplaciandeform_bind", text="Unbind" if is_bind else "Bind")

    def LAPLACIANSMOOTH(self, layout, ob, md):
        layout.prop(md, "iterations")

        split = layout.split(percentage=0.25)

        col = split.column()
        col.label(text="Axis:")
        col.prop(md, "use_x")
        col.prop(md, "use_y")
        col.prop(md, "use_z")

        col = split.column()
        col.label(text="Lambda:")
        col.prop(md, "lambda_factor", text="Factor")
        col.prop(md, "lambda_border", text="Border")

        col.separator()
        col.prop(md, "use_volume_preserve")
        col.prop(md, "use_normalized")

        layout.label(text="Vertex Group:")
        layout.prop_search(md, "vertex_group", ob, "vertex_groups", text="")

    def LATTICE(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.label(text="Object:")
        col.prop(md, "object", text="")

        col = split.column()
        col.label(text="Vertex Group:")
        col.prop_search(md, "vertex_group", ob, "vertex_groups", text="")

        layout.separator()
        layout.prop(md, "strength", slider=True)

    def MASK(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.label(text="Mode:")
        col.prop(md, "mode", text="")

        col = split.column()
        if md.mode == 'ARMATURE':
            col.label(text="Armature:")
            col.prop(md, "armature", text="")
        elif md.mode == 'VERTEX_GROUP':
            col.label(text="Vertex Group:")
            row = col.row(align=True)
            row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
            sub = row.row(align=True)
            sub.active = bool(md.vertex_group)
            sub.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

    def MESH_DEFORM(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.active = not md.is_bound
        col.label(text="Object:")
        col.prop(md, "object", text="")

        col = split.column()
        col.label(text="Vertex Group:")

        row = col.row(align=True)
        row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
        sub = row.row(align=True)
        sub.active = bool(md.vertex_group)
        sub.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

        layout.separator()

        if md.is_bound:
            layout.operator("object.meshdeform_bind", text="Unbind")
        else:
            layout.operator("object.meshdeform_bind", text="Bind")

            row = layout.row()
            row.prop(md, "precision")
            row.prop(md, "use_dynamic_bind")

    def MIRROR(self, layout, ob, md):
        split = layout.split(percentage=0.25)

        col = split.column()
        col.label(text="Axis:")
        col.prop(md, "use_x")
        col.prop(md, "use_y")
        col.prop(md, "use_z")

        col = split.column()
        col.label(text="Options:")
        col.prop(md, "use_mirror_merge", text="Merge")
        col.prop(md, "use_clip", text="Clipping")
        col.prop(md, "use_mirror_vertex_groups", text="Vertex Groups")

        col = split.column()
        col.label(text="Textures:")
        col.prop(md, "use_mirror_u", text="U")
        col.prop(md, "use_mirror_v", text="V")

        col = layout.column()

        if md.use_mirror_merge is True:
            col.prop(md, "merge_threshold")
        col.label(text="Mirror Object:")
        col.prop(md, "mirror_object", text="")

    def MULTIRES(self, layout, ob, md):
        layout.row().prop(md, "subdivision_type", expand=True)

        split = layout.split()
        col = split.column()
        col.prop(md, "levels", text="Preview")
        col.prop(md, "sculpt_levels", text="Sculpt")
        col.prop(md, "render_levels", text="Render")

        col = split.column()

        col.enabled = ob.mode != 'EDIT'
        col.operator("object.multires_subdivide", text="Subdivide")
        col.operator("object.multires_higher_levels_delete", text="Delete Higher")
        col.operator("object.multires_reshape", text="Reshape")
        col.operator("object.multires_base_apply", text="Apply Base")
        col.prop(md, "use_subsurf_uv")
        col.prop(md, "show_only_control_edges")

        layout.separator()

        col = layout.column()
        row = col.row()
        if md.is_external:
            row.operator("object.multires_external_pack", text="Pack External")
            row.label()
            row = col.row()
            row.prop(md, "filepath", text="")
        else:
            row.operator("object.multires_external_save", text="Save External...")
            row.label()

    def OCEAN(self, layout, ob, md):
        if not bpy.app.build_options.mod_oceansim:
            layout.label("Built without OceanSim modifier")
            return

        layout.prop(md, "geometry_mode")

        if md.geometry_mode == 'GENERATE':
            row = layout.row()
            row.prop(md, "repeat_x")
            row.prop(md, "repeat_y")

        layout.separator()

        split = layout.split()

        col = split.column()
        col.prop(md, "time")
        col.prop(md, "depth")
        col.prop(md, "random_seed")

        col = split.column()
        col.prop(md, "resolution")
        col.prop(md, "size")
        col.prop(md, "spatial_size")

        layout.label("Waves:")

        split = layout.split()

        col = split.column()
        col.prop(md, "choppiness")
        col.prop(md, "wave_scale", text="Scale")
        col.prop(md, "wave_scale_min")
        col.prop(md, "wind_velocity")

        col = split.column()
        col.prop(md, "wave_alignment", text="Alignment")
        sub = col.column()
        sub.active = (md.wave_alignment > 0.0)
        sub.prop(md, "wave_direction", text="Direction")
        sub.prop(md, "damping")

        layout.separator()

        layout.prop(md, "use_normals")

        split = layout.split()

        col = split.column()
        col.prop(md, "use_foam")
        sub = col.row()
        sub.active = md.use_foam
        sub.prop(md, "foam_coverage", text="Coverage")

        col = split.column()
        col.active = md.use_foam
        col.label("Foam Data Layer Name:")
        col.prop(md, "foam_layer_name", text="")

        layout.separator()

        if md.is_cached:
            layout.operator("object.ocean_bake", text="Free Bake").free = True
        else:
            layout.operator("object.ocean_bake").free = False

        split = layout.split()
        split.enabled = not md.is_cached

        col = split.column(align=True)
        col.prop(md, "frame_start", text="Start")
        col.prop(md, "frame_end", text="End")

        col = split.column(align=True)
        col.label(text="Cache path:")
        col.prop(md, "filepath", text="")

        split = layout.split()
        split.enabled = not md.is_cached

        col = split.column()
        col.active = md.use_foam
        col.prop(md, "bake_foam_fade")

        col = split.column()

    def PARTICLE_INSTANCE(self, layout, ob, md):
        layout.prop(md, "object")
        layout.prop(md, "particle_system_index", text="Particle System")

        split = layout.split()
        col = split.column()
        col.label(text="Create From:")
        col.prop(md, "use_normal")
        col.prop(md, "use_children")
        col.prop(md, "use_size")

        col = split.column()
        col.label(text="Show Particles When:")
        col.prop(md, "show_alive")
        col.prop(md, "show_unborn")
        col.prop(md, "show_dead")

        layout.separator()

        layout.prop(md, "use_path", text="Create Along Paths")

        split = layout.split()
        split.active = md.use_path
        col = split.column()
        col.row().prop(md, "axis", expand=True)
        col.prop(md, "use_preserve_shape")

        col = split.column()
        col.prop(md, "position", slider=True)
        col.prop(md, "random_position", text="Random", slider=True)

    def PARTICLE_SYSTEM(self, layout, ob, md):
        layout.label(text="Settings can be found inside the Particle context")

    def SCREW(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.prop(md, "axis")
        col.prop(md, "object", text="AxisOb")
        col.prop(md, "angle")
        col.prop(md, "steps")
        col.prop(md, "render_steps")
        col.prop(md, "use_smooth_shade")

        col = split.column()
        row = col.row()
        row.active = (md.object is None or md.use_object_screw_offset is False)
        row.prop(md, "screw_offset")
        row = col.row()
        row.active = (md.object is not None)
        row.prop(md, "use_object_screw_offset")
        col.prop(md, "use_normal_calculate")
        col.prop(md, "use_normal_flip")
        col.prop(md, "iterations")
        col.prop(md, "use_stretch_u")
        col.prop(md, "use_stretch_v")

    def SHRINKWRAP(self, layout, ob, md):
        split = layout.split()
        col = split.column()
        col.label(text="Target:")
        col.prop(md, "target", text="")
        col = split.column()
        col.label(text="Vertex Group:")
        col.prop_search(md, "vertex_group", ob, "vertex_groups", text="")

        split = layout.split()

        col = split.column()
        col.prop(md, "offset")

        col = split.column()
        col.label(text="Mode:")
        col.prop(md, "wrap_method", text="")

        if md.wrap_method == 'PROJECT':
            split = layout.split()
            col = split.column()
            col.prop(md, "subsurf_levels")
            col = split.column()

            col.prop(md, "project_limit", text="Limit")
            split = layout.split(percentage=0.25)

            col = split.column()
            col.label(text="Axis:")
            col.prop(md, "use_project_x")
            col.prop(md, "use_project_y")
            col.prop(md, "use_project_z")

            col = split.column()
            col.label(text="Direction:")
            col.prop(md, "use_negative_direction")
            col.prop(md, "use_positive_direction")

            col = split.column()
            col.label(text="Cull Faces:")
            col.prop(md, "cull_face", expand=True)

            layout.prop(md, "auxiliary_target")

        elif md.wrap_method == 'NEAREST_SURFACEPOINT':
            layout.prop(md, "use_keep_above_surface")

    def SIMPLE_DEFORM(self, layout, ob, md):

        layout.row().prop(md, "deform_method", expand=True)

        split = layout.split()

        col = split.column()
        col.label(text="Vertex Group:")
        col.prop_search(md, "vertex_group", ob, "vertex_groups", text="")

        split = layout.split()

        col = split.column()
        col.label(text="Origin:")
        col.prop(md, "origin", text="")

        if md.deform_method in {'TAPER', 'STRETCH', 'TWIST'}:
            col.label(text="Lock:")
            col.prop(md, "lock_x")
            col.prop(md, "lock_y")

        col = split.column()
        col.label(text="Deform:")
        if md.deform_method in {'TAPER', 'STRETCH'}:
            col.prop(md, "factor")
        else:
            col.prop(md, "angle")
        col.prop(md, "limits", slider=True)

    def SMOKE(self, layout, ob, md):
        #layout.label(text="Settings are inside the Physics tab")
        return {"FINISHED"}

    def SMOOTH(self, layout, ob, md):
        split = layout.split(percentage=0.25)

        col = split.column()
        col.label(text="Axis:")
        col.prop(md, "use_x")
        col.prop(md, "use_y")
        col.prop(md, "use_z")

        col = split.column()
        col.prop(md, "factor")
        col.prop(md, "iterations")
        col.label(text="Vertex Group:")
        col.prop_search(md, "vertex_group", ob, "vertex_groups", text="")

    def SOFT_BODY(self, layout, ob, md):
        #layout.label(text="Settings are inside the Physics tab")
        return {"FINISHED"}

    def SOLIDIFY(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.prop(md, "thickness")
        col.prop(md, "thickness_clamp")

        col.separator()

        row = col.row(align=True)
        row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
        sub = row.row(align=True)
        sub.active = bool(md.vertex_group)
        sub.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')

        sub = col.row()
        sub.active = bool(md.vertex_group)
        sub.prop(md, "thickness_vertex_group", text="Factor")

        col.label(text="Crease:")
        col.prop(md, "edge_crease_inner", text="Inner")
        col.prop(md, "edge_crease_outer", text="Outer")
        col.prop(md, "edge_crease_rim", text="Rim")

        col = split.column()

        col.prop(md, "offset")
        col.prop(md, "use_flip_normals")

        col.prop(md, "use_even_offset")
        col.prop(md, "use_quality_normals")
        col.prop(md, "use_rim")

        col.separator()

        col.label(text="Material Index Offset:")

        sub = col.column()
        row = sub.split(align=True, percentage=0.4)
        row.prop(md, "material_offset", text="")
        row = row.row(align=True)
        row.active = md.use_rim
        row.prop(md, "material_offset_rim", text="Rim")

    def SUBSURF(self, layout, ob, md):
        #layout.panel()
        layout.row().prop(md, "subdivision_type", expand=True)

        split = layout.split()
        col = split.column()
        col.label(text="Subdivisions:")
        col.prop(md, "levels", text="View")
        col.prop(md, "render_levels", text="Render")

        col = split.column()
        col.label(text="Options:")
        col.prop(md, "use_subsurf_uv")
        col.prop(md, "show_in_editmode",text = "Show in edit mode",toggle = True)
        col.prop(md, "show_only_control_edges")

    def SURFACE(self, layout, ob, md):
        layout.label(text="Settings are inside the Physics tab")

    def UV_PROJECT(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.label(text="Image:")
        col.prop(md, "image", text="")

        col = split.column()
        col.label(text="UV Map:")
        col.prop_search(md, "uv_layer", ob.data, "uv_textures", text="")

        split = layout.split()
        col = split.column()
        col.prop(md, "use_image_override")
        col.prop(md, "projector_count", text="Projectors")
        for proj in md.projectors:
            col.prop(proj, "object", text="")

        col = split.column()
        sub = col.column(align=True)
        sub.prop(md, "aspect_x", text="Aspect X")
        sub.prop(md, "aspect_y", text="Aspect Y")

        sub = col.column(align=True)
        sub.prop(md, "scale_x", text="Scale X")
        sub.prop(md, "scale_y", text="Scale Y")

    def WARP(self, layout, ob, md):
        use_falloff = (md.falloff_type != 'NONE')
        split = layout.split()

        col = split.column()
        col.label(text="From:")
        col.prop(md, "object_from", text="")

        col.prop(md, "use_volume_preserve")

        col = split.column()
        col.label(text="To:")
        col.prop(md, "object_to", text="")
        col.prop_search(md, "vertex_group", ob, "vertex_groups", text="")

        col = layout.column()

        row = col.row(align=True)
        row.prop(md, "strength")
        if use_falloff:
            row.prop(md, "falloff_radius")

        col.prop(md, "falloff_type")
        if use_falloff:
            if md.falloff_type == 'CURVE':
                col.template_curve_mapping(md, "falloff_curve")

        # 2 new columns
        split = layout.split()
        col = split.column()
        col.label(text="Texture:")
        col.template_ID(md, "texture", new="texture.new")

        col = split.column()
        col.label(text="Texture Coordinates:")
        col.prop(md, "texture_coords", text="")

        if md.texture_coords == 'OBJECT':
            layout.prop(md, "texture_coords_object", text="Object")
        elif md.texture_coords == 'UV' and ob.type == 'MESH':
            layout.prop_search(md, "uv_layer", ob.data, "uv_textures")

    def WAVE(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.label(text="Motion:")
        col.prop(md, "use_x")
        col.prop(md, "use_y")
        col.prop(md, "use_cyclic")

        col = split.column()
        col.prop(md, "use_normal")
        sub = col.column()
        sub.active = md.use_normal
        sub.prop(md, "use_normal_x", text="X")
        sub.prop(md, "use_normal_y", text="Y")
        sub.prop(md, "use_normal_z", text="Z")

        split = layout.split()

        col = split.column()
        col.label(text="Time:")
        sub = col.column(align=True)
        sub.prop(md, "time_offset", text="Offset")
        sub.prop(md, "lifetime", text="Life")
        col.prop(md, "damping_time", text="Damping")

        col = split.column()
        col.label(text="Position:")
        sub = col.column(align=True)
        sub.prop(md, "start_position_x", text="X")
        sub.prop(md, "start_position_y", text="Y")
        col.prop(md, "falloff_radius", text="Falloff")

        layout.separator()

        layout.prop(md, "start_position_object")
        layout.prop_search(md, "vertex_group", ob, "vertex_groups")
        split = layout.split(percentage=0.33)
        col = split.column()
        col.label(text="Texture")
        col = split.column()
        col.template_ID(md, "texture", new="texture.new")
        layout.prop(md, "texture_coords")
        if md.texture_coords == 'MAP_UV' and ob.type == 'MESH':
            layout.prop_search(md, "uv_layer", ob.data, "uv_textures")
        elif md.texture_coords == 'OBJECT':
            layout.prop(md, "texture_coords_object")

        layout.separator()

        split = layout.split()

        col = split.column()
        col.prop(md, "speed", slider=True)
        col.prop(md, "height", slider=True)

        col = split.column()
        col.prop(md, "width", slider=True)
        col.prop(md, "narrowness", slider=True)

    def REMESH(self, layout, ob, md):
        layout.prop(md, "mode")

        row = layout.row()
        row.prop(md, "octree_depth")
        row.prop(md, "scale")

        if md.mode == 'SHARP':
            layout.prop(md, "sharpness")

        layout.prop(md, "use_smooth_shade")
        layout.prop(md, "use_remove_disconnected")
        row = layout.row()
        row.active = md.use_remove_disconnected
        row.prop(md, "threshold")

    @staticmethod
    def vertex_weight_mask(layout, ob, md):
        layout.label(text="Influence/Mask Options:")

        split = layout.split(percentage=0.4)
        split.label(text="Global Influence:")
        split.prop(md, "mask_constant", text="")

        if not md.mask_texture:
            split = layout.split(percentage=0.4)
            split.label(text="Vertex Group Mask:")
            split.prop_search(md, "mask_vertex_group", ob, "vertex_groups", text="")

        if not md.mask_vertex_group:
            split = layout.split(percentage=0.4)
            split.label(text="Texture Mask:")
            split.template_ID(md, "mask_texture", new="texture.new")
            if md.mask_texture:
                split = layout.split()

                col = split.column()
                col.label(text="Texture Coordinates:")
                col.prop(md, "mask_tex_mapping", text="")

                col = split.column()
                col.label(text="Use Channel:")
                col.prop(md, "mask_tex_use_channel", text="")

                if md.mask_tex_mapping == 'OBJECT':
                    layout.prop(md, "mask_tex_map_object", text="Object")
                elif md.mask_tex_mapping == 'UV' and ob.type == 'MESH':
                    layout.prop_search(md, "mask_tex_uv_layer", ob.data, "uv_textures")

    def VERTEX_WEIGHT_EDIT(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.label(text="Vertex Group:")
        col.prop_search(md, "vertex_group", ob, "vertex_groups", text="")

        col.label(text="Default Weight:")
        col.prop(md, "default_weight", text="")

        col = split.column()
        col.prop(md, "use_add")
        sub = col.column()
        sub.active = md.use_add
        sub.prop(md, "add_threshold")

        col = col.column()
        col.prop(md, "use_remove")
        sub = col.column()
        sub.active = md.use_remove
        sub.prop(md, "remove_threshold")

        layout.separator()

        layout.prop(md, "falloff_type")
        if md.falloff_type == 'CURVE':
            layout.template_curve_mapping(md, "map_curve")

        # Common mask options
        layout.separator()
        self.vertex_weight_mask(layout, ob, md)

    def VERTEX_WEIGHT_MIX(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.label(text="Vertex Group A:")
        col.prop_search(md, "vertex_group_a", ob, "vertex_groups", text="")
        col.label(text="Default Weight A:")
        col.prop(md, "default_weight_a", text="")

        col.label(text="Mix Mode:")
        col.prop(md, "mix_mode", text="")

        col = split.column()
        col.label(text="Vertex Group B:")
        col.prop_search(md, "vertex_group_b", ob, "vertex_groups", text="")
        col.label(text="Default Weight B:")
        col.prop(md, "default_weight_b", text="")

        col.label(text="Mix Set:")
        col.prop(md, "mix_set", text="")

        # Common mask options
        layout.separator()
        self.vertex_weight_mask(layout, ob, md)

    def VERTEX_WEIGHT_PROXIMITY(self, layout, ob, md):
        split = layout.split()

        col = split.column()
        col.label(text="Vertex Group:")
        col.prop_search(md, "vertex_group", ob, "vertex_groups", text="")

        col = split.column()
        col.label(text="Target Object:")
        col.prop(md, "target", text="")

        split = layout.split()

        col = split.column()
        col.label(text="Distance:")
        col.prop(md, "proximity_mode", text="")
        if md.proximity_mode == 'GEOMETRY':
            col.row().prop(md, "proximity_geometry")

        col = split.column()
        col.label()
        col.prop(md, "min_dist")
        col.prop(md, "max_dist")

        layout.separator()
        layout.prop(md, "falloff_type")

        # Common mask options
        layout.separator()
        self.vertex_weight_mask(layout, ob, md)

    def SKIN(self, layout, ob, md):
        layout.operator("object.skin_armature_create", text="Create Armature")

        layout.separator()

        col = layout.column(align=True)
        col.prop(md, "branch_smoothing")
        col.prop(md, "use_smooth_shade")

        split = layout.split()

        col = split.column()
        col.label(text="Selected Vertices:")
        sub = col.column(align=True)
        sub.operator("object.skin_loose_mark_clear", text="Mark Loose").action = 'MARK'
        sub.operator("object.skin_loose_mark_clear", text="Clear Loose").action = 'CLEAR'

        sub = col.column()
        sub.operator("object.skin_root_mark", text="Mark Root")
        sub.operator("object.skin_radii_equalize", text="Equalize Radii")

        col = split.column()
        col.label(text="Symmetry Axes:")
        col.prop(md, "use_x_symmetry")
        col.prop(md, "use_y_symmetry")
        col.prop(md, "use_z_symmetry")

    def TRIANGULATE(self, layout, ob, md):
        row = layout.row()

        col = row.column()
        col.label(text="Quad Method:")
        col.prop(md, "quad_method", text="")
        col = row.column()
        col.label(text="Ngon Method:")
        col.prop(md, "ngon_method", text="")

    def UV_WARP(self, layout, ob, md):
        split = layout.split()
        col = split.column()
        col.prop(md, "center")

        col = split.column()
        col.label(text="UV Axis:")
        col.prop(md, "axis_u", text="")
        col.prop(md, "axis_v", text="")

        split = layout.split()
        col = split.column()
        col.label(text="From:")
        col.prop(md, "object_from", text="")

        col = split.column()
        col.label(text="To:")
        col.prop(md, "object_to", text="")

        split = layout.split()
        col = split.column()
        obj = md.object_from
        if obj and obj.type == 'ARMATURE':
            col.label(text="Bone:")
            col.prop_search(md, "bone_from", obj.data, "bones", text="")

        col = split.column()
        obj = md.object_to
        if obj and obj.type == 'ARMATURE':
            col.label(text="Bone:")
            col.prop_search(md, "bone_to", obj.data, "bones", text="")

        split = layout.split()

        col = split.column()
        col.label(text="Vertex Group:")
        col.prop_search(md, "vertex_group", ob, "vertex_groups", text="")

        col = split.column()
        col.label(text="UV Map:")
        col.prop_search(md, "uv_layer", ob.data, "uv_textures", text="")

    def WIREFRAME(self, layout, ob, md):
        has_vgroup = bool(md.vertex_group)

        split = layout.split()

        col = split.column()
        col.prop(md, "thickness", text="Thickness")

        row = col.row(align=True)
        row.prop_search(md, "vertex_group", ob, "vertex_groups", text="")
        sub = row.row(align=True)
        sub.active = has_vgroup
        sub.prop(md, "invert_vertex_group", text="", icon='ARROW_LEFTRIGHT')
        row = col.row(align=True)
        row.active = has_vgroup
        row.prop(md, "thickness_vertex_group", text="Factor")

        col.prop(md, "use_crease", text="Crease Edges")
        col.prop(md, "crease_weight", text="Crease Weight")

        col = split.column()

        col.prop(md, "offset")
        col.prop(md, "use_even_offset", text="Even Thickness")
        col.prop(md, "use_relative_offset", text="Relative Thickness")
        col.prop(md, "use_boundary", text="Boundary")
        col.prop(md, "use_replace", text="Replace Original")

        col.prop(md, "material_offset", text="Material Offset")
        
        
########## CLOTH MODIFIER

def cloth_panel_enabled(md):
    return md.point_cache.is_baked is False


class CLOTH_MT_presets(Menu):
    bl_label = "Cloth Presets"
    preset_subdir = "cloth"
    preset_operator = "script.execute_preset"
    draw = Menu.draw_preset


class PhysicButtonsPanel():
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "modifier"

    @classmethod
    def poll(cls, context):
        ob = context.object
        rd = context.scene.render
        indx = ob.modifier_active_index
        try:
            mod = ob.modifiers[indx]
        except IndexError:
            return False
        return (ob and mod.type == 'CLOTH') and (not rd.use_game_engine) and (context.cloth)


class PHYSICS_PT_cloth(PhysicButtonsPanel, Panel):
    bl_label = "Cloth"

    def draw(self, context):
        layout = self.layout

        md = context.cloth
        ob = context.object
        cloth = md.settings

        split = layout.split()

        split.active = cloth_panel_enabled(md)

        col = split.column()

        col.label(text="Presets:")
        sub = col.row(align=True)
        sub.menu("CLOTH_MT_presets", text=bpy.types.CLOTH_MT_presets.bl_label)
        sub.operator("cloth.preset_add", text="", icon='ZOOMIN')
        sub.operator("cloth.preset_add", text="", icon='ZOOMOUT').remove_active = True

        col.label(text="Quality:")
        col.prop(cloth, "quality", text="Steps", slider=True)

        col.label(text="Material:")
        col.prop(cloth, "mass")
        col.prop(cloth, "structural_stiffness", text="Structural")
        col.prop(cloth, "bending_stiffness", text="Bending")

        col = split.column()

        col.label(text="Damping:")
        col.prop(cloth, "spring_damping", text="Spring")
        col.prop(cloth, "air_damping", text="Air")
        col.prop(cloth, "vel_damping", text="Velocity")

        col.prop(cloth, "use_pin_cloth", text="Pinning")
        sub = col.column()
        sub.active = cloth.use_pin_cloth
        sub.prop_search(cloth, "vertex_group_mass", ob, "vertex_groups", text="")
        sub.prop(cloth, "pin_stiffness", text="Stiffness")

        col.label(text="Pre roll:")
        col.prop(cloth, "pre_roll", text="Frames")

        # Disabled for now
        """
        if cloth.vertex_group_mass:
            layout.label(text="Goal:")

            col = layout.column_flow()
            col.prop(cloth, "goal_default", text="Default")
            col.prop(cloth, "goal_spring", text="Stiffness")
            col.prop(cloth, "goal_friction", text="Friction")
        """

        key = ob.data.shape_keys

        if key:
            col.label(text="Rest Shape Key:")
            col.prop_search(cloth, "rest_shape_key", key, "key_blocks", text="")


class PHYSICS_PT_cloth_cache(PhysicButtonsPanel, Panel):
    bl_label = "Cloth Cache"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        md = context.cloth
        point_cache_ui(self, context, md.point_cache, cloth_panel_enabled(md), 'CLOTH')


class PHYSICS_PT_cloth_collision(PhysicButtonsPanel, Panel):
    bl_label = "Cloth Collision"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        cloth = context.cloth.collision_settings

        self.layout.active = cloth_panel_enabled(context.cloth)
        self.layout.prop(cloth, "use_collision", text="")

    def draw(self, context):
        layout = self.layout

        cloth = context.cloth.collision_settings
        md = context.cloth
        ob = context.object

        layout.active = cloth.use_collision and cloth_panel_enabled(md)

        split = layout.split()

        col = split.column()
        col.prop(cloth, "collision_quality", slider=True, text="Quality")
        col.prop(cloth, "distance_min", slider=True, text="Distance")
        col.prop(cloth, "repel_force", slider=True, text="Repel")
        col.prop(cloth, "distance_repel", slider=True, text="Repel Distance")
        col.prop(cloth, "friction")

        col = split.column()
        col.prop(cloth, "use_self_collision", text="Self Collision")
        sub = col.column()
        sub.active = cloth.use_self_collision
        sub.prop(cloth, "self_collision_quality", slider=True, text="Quality")
        sub.prop(cloth, "self_distance_min", slider=True, text="Distance")
        sub.prop_search(cloth, "vertex_group_self_collisions", ob, "vertex_groups", text="")

        layout.prop(cloth, "group")


class PHYSICS_PT_cloth_stiffness(PhysicButtonsPanel, Panel):
    bl_label = "Cloth Stiffness Scaling"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        cloth = context.cloth.settings

        self.layout.active = cloth_panel_enabled(context.cloth)
        self.layout.prop(cloth, "use_stiffness_scale", text="")

    def draw(self, context):
        layout = self.layout

        md = context.cloth
        ob = context.object
        cloth = context.cloth.settings

        layout.active = (cloth.use_stiffness_scale and cloth_panel_enabled(md))

        split = layout.split()

        col = split.column()
        col.label(text="Structural Stiffness:")
        col.prop_search(cloth, "vertex_group_structural_stiffness", ob, "vertex_groups", text="")
        col.prop(cloth, "structural_stiffness_max", text="Max")

        col = split.column()
        col.label(text="Bending Stiffness:")
        col.prop_search(cloth, "vertex_group_bending", ob, "vertex_groups", text="")
        col.prop(cloth, "bending_stiffness_max", text="Max")


class PHYSICS_PT_cloth_sewing(PhysicButtonsPanel, Panel):
    bl_label = "Cloth Sewing Springs"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        cloth = context.cloth.settings

        self.layout.active = cloth_panel_enabled(context.cloth)
        self.layout.prop(cloth, "use_sewing_springs", text="")

    def draw(self, context):
        layout = self.layout

        md = context.cloth
        ob = context.object
        cloth = context.cloth.settings

        layout.active = (cloth.use_sewing_springs and cloth_panel_enabled(md))

        layout.prop(cloth, "sewing_force_max", text="Sewing Force")

        split = layout.split()

        col = split.column(align=True)
        col.label(text="Shrinking:")
        col.prop_search(cloth, "vertex_group_shrink", ob, "vertex_groups", text="")

        col = split.column(align=True)
        col.label()
        col.prop(cloth, "shrink_min", text="Min")
        col.prop(cloth, "shrink_max", text="Max")


class PHYSICS_PT_cloth_field_weights(PhysicButtonsPanel, Panel):
    bl_label = "Cloth Field Weights"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        cloth = context.cloth.settings
        effector_weights_ui(self, context, cloth.effector_weights, 'CLOTH')


######### Dynamic Paint

class PHYSICS_UL_dynapaint_surfaces(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # assert(isinstance(item, bpy.types.DynamicPaintSurface)
        surf = item
        sticon = layout.enum_item_icon(surf, "surface_type", surf.surface_type)
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.label(text="", icon_value=icon)
            row.prop(surf, "name", text="", emboss=False, icon_value=sticon)
            row = layout.row(align=True)
            if surf.use_color_preview:
                row.prop(surf, "show_preview", text="", emboss=False,
                         icon='RESTRICT_VIEW_OFF' if surf.show_preview else 'RESTRICT_VIEW_ON')
            row.prop(surf, "is_active", text="")
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            row = layout.row(align=True)
            row.label(text="", icon_value=icon)
            row.label(text="", icon_value=sticon)


class PhysicButtonsPanel():
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "modifier"

    @classmethod
    def poll(cls, context):
        ob = context.object
        rd = context.scene.render
        indx = ob.modifier_active_index
        try:
            mod = ob.modifiers[indx]
        except IndexError:
            return False
        return (ob and mod.type == 'DYNAMIC_PAINT') and (not rd.use_game_engine) and context.dynamic_paint


class PHYSICS_PT_dynamic_paint(PhysicButtonsPanel, Panel):
    bl_label = "Dynamic Paint"

    def draw(self, context):
        layout = self.layout

        md = context.dynamic_paint

        layout.prop(md, "ui_type", expand=True)

        if md.ui_type == 'CANVAS':
            canvas = md.canvas_settings

            if canvas is None:
                layout.operator("dpaint.type_toggle", text="Add Canvas").type = 'CANVAS'
            else:
                layout.operator("dpaint.type_toggle", text="Remove Canvas", icon='X').type = 'CANVAS'

                surface = canvas.canvas_surfaces.active

                row = layout.row()
                row.template_list("PHYSICS_UL_dynapaint_surfaces", "", canvas, "canvas_surfaces",
                                  canvas.canvas_surfaces, "active_index", rows=1)

                col = row.column(align=True)
                col.operator("dpaint.surface_slot_add", icon='ZOOMIN', text="")
                col.operator("dpaint.surface_slot_remove", icon='ZOOMOUT', text="")

                if surface:
                    layout.prop(surface, "surface_format")

                    col = layout.column()
                    if surface.surface_format != 'VERTEX':
                        col.label(text="Quality:")
                        col.prop(surface, "image_resolution")
                    col.prop(surface, "use_antialiasing")

                    col = layout.column()
                    col.label(text="Frames:")
                    split = col.split()

                    col = split.column(align=True)
                    col.prop(surface, "frame_start", text="Start")
                    col.prop(surface, "frame_end", text="End")

                    split.prop(surface, "frame_substeps")

        elif md.ui_type == 'BRUSH':
            brush = md.brush_settings
            use_shading_nodes = context.scene.render.use_shading_nodes

            if brush is None:
                layout.operator("dpaint.type_toggle", text="Add Brush").type = 'BRUSH'
            else:
                layout.operator("dpaint.type_toggle", text="Remove Brush", icon='X').type = 'BRUSH'

                split = layout.split()

                col = split.column()
                col.prop(brush, "use_absolute_alpha")
                col.prop(brush, "use_paint_erase")
                col.prop(brush, "paint_wetness", text="Wetness")

                col = split.column()
                if not use_shading_nodes:
                    sub = col.column()
                    sub.active = (brush.paint_source != 'PARTICLE_SYSTEM')
                    sub.prop(brush, "use_material")
                if brush.use_material and brush.paint_source != 'PARTICLE_SYSTEM' and not use_shading_nodes:
                    col.prop(brush, "material", text="")
                    col.prop(brush, "paint_alpha", text="Alpha Factor")
                else:
                    col.prop(brush, "paint_color", text="")
                    col.prop(brush, "paint_alpha", text="Alpha")


class PHYSICS_PT_dp_advanced_canvas(PhysicButtonsPanel, Panel):
    bl_label = "Dynamic Paint Advanced"

    @classmethod
    def poll(cls, context):
        md = context.dynamic_paint
        rd = context.scene.render
        ob = context.object
        indx = ob.modifier_active_index
        try:
            mod = ob.modifiers[indx]
        except IndexError:
            return False        
        return md and (mod.type == 'DYNAMIC_PAINT') and md.ui_type == 'CANVAS' and md.canvas_settings and md.canvas_settings.canvas_surfaces.active and (not rd.use_game_engine)

    def draw(self, context): 
        layout = self.layout

        canvas = context.dynamic_paint.canvas_settings
        surface = canvas.canvas_surfaces.active

        surface_type = surface.surface_type

        layout.prop(surface, "surface_type")
        layout.separator()

        # dissolve
        if surface_type == 'PAINT':
            split = layout.split(percentage=0.35)
            split.prop(surface, "use_drying", text="Dry:")

            col = split.column()
            col.active = surface.use_drying
            split = col.split(percentage=0.7)
            col = split.column(align=True)
            col.prop(surface, "dry_speed", text="Time")
            col.prop(surface, "color_dry_threshold")
            split.prop(surface, "use_dry_log", text="Slow")

        if surface_type != 'WAVE':
            split = layout.split(percentage=0.35)
            col = split.column()
            if surface_type == 'WEIGHT':
                col.prop(surface, "use_dissolve", text="Fade:")
            else:
                col.prop(surface, "use_dissolve", text="Dissolve:")
            col = split.column()
            col.active = surface.use_dissolve
            split = col.split(percentage=0.7)
            split.prop(surface, "dissolve_speed", text="Time")
            split.prop(surface, "use_dissolve_log", text="Slow")

        # per type settings
        if surface_type == 'DISPLACE':
            layout.prop(surface, "use_incremental_displace")
            if surface.surface_format == 'VERTEX':
                row = layout.row()
                row.prop(surface, "depth_clamp")
                row.prop(surface, "displace_factor")

        elif surface_type == 'WAVE':
            layout.prop(surface, "use_wave_open_border")

            split = layout.split()

            col = split.column(align=True)
            col.prop(surface, "wave_timescale")
            col.prop(surface, "wave_speed")

            col = split.column(align=True)
            col.prop(surface, "wave_damping")
            col.prop(surface, "wave_spring")
            col.prop(surface, "wave_smoothness")

        layout.separator()
        layout.prop(surface, "brush_group")
        row = layout.row()
        row.prop(surface, "brush_influence_scale")
        row.prop(surface, "brush_radius_scale")


class PHYSICS_PT_dp_canvas_output(PhysicButtonsPanel, Panel):
    bl_label = "Dynamic Paint Output"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        md = context.dynamic_paint
        rd = context.scene.render
        ob = context.object
        indx = ob.modifier_active_index
        try:
            mod = ob.modifiers[indx]
        except IndexError:
            return False        
        if not (md and md.ui_type == 'CANVAS' and md.canvas_settings):
            return 0
        surface = context.dynamic_paint.canvas_settings.canvas_surfaces.active
        return (surface and (mod.type == 'DYNAMIC_PAINT') and
                (not (surface.surface_format == 'VERTEX' and (surface.surface_type in {'DISPLACE', 'WAVE'}))) and
                (not rd.use_game_engine))

    def draw(self, context):
        layout = self.layout

        canvas = context.dynamic_paint.canvas_settings
        surface = canvas.canvas_surfaces.active
        ob = context.object

        surface_type = surface.surface_type

        # vertex format outputs
        if surface.surface_format == 'VERTEX':
            if surface_type == 'PAINT':
                # toggle active preview
                layout.prop(surface, "preview_id")

                # paint-map output
                row = layout.row()
                row.prop_search(surface, "output_name_a", ob.data, "vertex_colors", text="Paintmap layer")
                if surface.output_exists(object=ob, index=0):
                    ic = 'ZOOMOUT'
                else:
                    ic = 'ZOOMIN'

                row.operator("dpaint.output_toggle", icon=ic, text="").output = 'A'

                # wet-map output
                row = layout.row()
                row.prop_search(surface, "output_name_b", ob.data, "vertex_colors", text="Wetmap layer")
                if surface.output_exists(object=ob, index=1):
                    ic = 'ZOOMOUT'
                else:
                    ic = 'ZOOMIN'

                row.operator("dpaint.output_toggle", icon=ic, text="").output = 'B'

            elif surface_type == 'WEIGHT':
                row = layout.row()
                row.prop_search(surface, "output_name_a", ob, "vertex_groups", text="Vertex Group")
                if surface.output_exists(object=ob, index=0):
                    ic = 'ZOOMOUT'
                else:
                    ic = 'ZOOMIN'

                row.operator("dpaint.output_toggle", icon=ic, text="").output = 'A'

        # image format outputs
        if surface.surface_format == 'IMAGE':
            layout.operator("dpaint.bake", text="Bake Image Sequence", icon='MOD_DYNAMICPAINT')
            layout.prop_search(surface, "uv_layer", ob.data, "uv_textures", text="UV Map")
            layout.separator()

            layout.prop(surface, "image_output_path", text="")
            row = layout.row()
            row.prop(surface, "image_fileformat", text="")
            row.prop(surface, "use_premultiply", text="Premultiply alpha")

            if surface_type == 'PAINT':
                split = layout.split(percentage=0.4)
                split.prop(surface, "use_output_a", text="Paintmaps:")
                sub = split.row()
                sub.active = surface.use_output_a
                sub.prop(surface, "output_name_a", text="")

                split = layout.split(percentage=0.4)
                split.prop(surface, "use_output_b", text="Wetmaps:")
                sub = split.row()
                sub.active = surface.use_output_b
                sub.prop(surface, "output_name_b", text="")
            else:
                col = layout.column()
                col.prop(surface, "output_name_a", text="Filename:")
                if surface_type == 'DISPLACE':
                    col.prop(surface, "displace_type", text="Displace Type")
                    col.prop(surface, "depth_clamp")
                elif surface_type == 'WAVE':
                    col.prop(surface, "depth_clamp", text="Wave Clamp")


class PHYSICS_PT_dp_canvas_initial_color(PhysicButtonsPanel, Panel):
    bl_label = "Dynamic Paint Initial Color"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        md = context.dynamic_paint
        rd = context.scene.render
        ob = context.object
        indx = ob.modifier_active_index
        try:
            mod = ob.modifiers[indx]
        except IndexError:
            return False             
        if not (md and md.ui_type == 'CANVAS' and md.canvas_settings):
            return 0
        surface = context.dynamic_paint.canvas_settings.canvas_surfaces.active
        return (mod.type == 'DYNAMIC_PAINT') and (surface and surface.surface_type == 'PAINT') and (not rd.use_game_engine)

    def draw(self, context):
        layout = self.layout

        canvas = context.dynamic_paint.canvas_settings
        surface = canvas.canvas_surfaces.active
        ob = context.object

        layout.prop(surface, "init_color_type", expand=False)
        if surface.init_color_type != 'NONE':
            layout.separator()

        # dissolve
        if surface.init_color_type == 'COLOR':
            layout.prop(surface, "init_color")

        elif surface.init_color_type == 'TEXTURE':
            layout.prop(surface, "init_texture")
            layout.prop_search(surface, "init_layername", ob.data, "uv_textures", text="UV Map")

        elif surface.init_color_type == 'VERTEX_COLOR':
            layout.prop_search(surface, "init_layername", ob.data, "vertex_colors", text="Color Layer")


class PHYSICS_PT_dp_effects(PhysicButtonsPanel, Panel):
    bl_label = "Dynamic Paint Effects"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        md = context.dynamic_paint
        rd = context.scene.render
        ob = context.object
        indx = ob.modifier_active_index
        try:
            mod = ob.modifiers[indx]
        except IndexError:
            return False             
        if not (md and md.ui_type == 'CANVAS' and md.canvas_settings):
            return False
        surface = context.dynamic_paint.canvas_settings.canvas_surfaces.active
        return (mod.type == 'DYNAMIC_PAINT') and (surface and surface.surface_type == 'PAINT') and (not rd.use_game_engine)

    def draw(self, context):
        layout = self.layout

        canvas = context.dynamic_paint.canvas_settings
        surface = canvas.canvas_surfaces.active

        layout.prop(surface, "effect_ui", expand=True)

        if surface.effect_ui == 'SPREAD':
            layout.prop(surface, "use_spread")

            row = layout.row()
            row.active = surface.use_spread
            row.prop(surface, "spread_speed")
            row.prop(surface, "color_spread_speed")

        elif surface.effect_ui == 'DRIP':
            layout.prop(surface, "use_drip")

            col = layout.column()
            col.active = surface.use_drip
            effector_weights_ui(self, context, surface.effector_weights, 'DYNAMIC_PAINT')

            layout.label(text="Surface Movement:")
            row = layout.row()
            row.prop(surface, "drip_velocity", slider=True)
            row.prop(surface, "drip_acceleration", slider=True)

        elif surface.effect_ui == 'SHRINK':
            layout.prop(surface, "use_shrink")

            row = layout.row()
            row.active = surface.use_shrink
            row.prop(surface, "shrink_speed")


class PHYSICS_PT_dp_cache(PhysicButtonsPanel, Panel):
    bl_label = "Dynamic Paint Cache"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        md = context.dynamic_paint
        rd = context.scene.render
        ob = context.object
        indx = ob.modifier_active_index
        try:
            mod = ob.modifiers[indx]
        except IndexError:
            return False                 
        return (md and 
                mod.type == 'DYNAMIC_PAINT' and
                md.ui_type == 'CANVAS' and
                md.canvas_settings and
                md.canvas_settings.canvas_surfaces.active and
                md.canvas_settings.canvas_surfaces.active.is_cache_user and
                (not rd.use_game_engine))

    def draw(self, context):
        surface = context.dynamic_paint.canvas_settings.canvas_surfaces.active
        cache = surface.point_cache

        point_cache_ui(self, context, cache, (cache.is_baked is False), 'DYNAMIC_PAINT')


class PHYSICS_PT_dp_brush_source(PhysicButtonsPanel, Panel):
    bl_label = "Dynamic Paint Source"

    @classmethod
    def poll(cls, context):
        md = context.dynamic_paint
        rd = context.scene.render
        ob = context.object
        indx = ob.modifier_active_index
        try:
            mod = ob.modifiers[indx]
        except IndexError:
            return False                 
        return md and (mod.type == 'DYNAMIC_PAINT')and md.ui_type == 'BRUSH' and md.brush_settings and (not rd.use_game_engine)

    def draw(self, context):
        layout = self.layout

        brush = context.dynamic_paint.brush_settings
        ob = context.object

        split = layout.split()
        col = split.column()
        col.prop(brush, "paint_source")

        if brush.paint_source == 'PARTICLE_SYSTEM':
            col.prop_search(brush, "particle_system", ob, "particle_systems", text="")
            if brush.particle_system:
                col.label(text="Particle effect:")
                sub = col.column()
                sub.active = not brush.use_particle_radius
                sub.prop(brush, "solid_radius", text="Solid Radius")
                col.prop(brush, "use_particle_radius", text="Use Particle's Radius")
                col.prop(brush, "smooth_radius", text="Smooth radius")

        if brush.paint_source in {'DISTANCE', 'VOLUME_DISTANCE', 'POINT'}:
            col.prop(brush, "paint_distance", text="Paint Distance")
            split = layout.row().split(percentage=0.4)
            sub = split.column()
            if brush.paint_source in {'DISTANCE', 'VOLUME_DISTANCE'}:
                sub.prop(brush, "use_proximity_project")
            if brush.paint_source == 'VOLUME_DISTANCE':
                sub.prop(brush, "invert_proximity")
                sub.prop(brush, "use_negative_volume")

            sub = split.column()
            if brush.paint_source in {'DISTANCE', 'VOLUME_DISTANCE'}:
                column = sub.column()
                column.active = brush.use_proximity_project
                column.prop(brush, "ray_direction")
            sub.prop(brush, "proximity_falloff")
            if brush.proximity_falloff == 'RAMP':
                col = layout.row().column()
                col.separator()
                col.prop(brush, "use_proximity_ramp_alpha", text="Only Use Alpha")
                col.template_color_ramp(brush, "paint_ramp", expand=True)


class PHYSICS_PT_dp_brush_velocity(PhysicButtonsPanel, Panel):
    bl_label = "Dynamic Paint Velocity"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        md = context.dynamic_paint
        rd = context.scene.render
        ob = context.object
        indx = ob.modifier_active_index
        try:
            mod = ob.modifiers[indx]
        except IndexError:
            return False                 
        return md and mod.type == 'DYNAMIC_PAINT' and md.ui_type == 'BRUSH' and md.brush_settings and (not rd.use_game_engine)

    def draw(self, context):
        layout = self.layout

        brush = context.dynamic_paint.brush_settings

        split = layout.split()

        col = split.column()
        col.prop(brush, "use_velocity_alpha")
        col.prop(brush, "use_velocity_color")

        split.prop(brush, "use_velocity_depth")

        col = layout.column()
        col.active = (brush.use_velocity_alpha or brush.use_velocity_color or brush.use_velocity_depth)
        col.prop(brush, "velocity_max")
        col.template_color_ramp(brush, "velocity_ramp", expand=True)
        layout.separator()

        row = layout.row()
        row.prop(brush, "use_smudge")
        sub = row.row()
        sub.active = brush.use_smudge
        sub.prop(brush, "smudge_strength")


class PHYSICS_PT_dp_brush_wave(PhysicButtonsPanel, Panel):
    bl_label = "Dynamic Paint Waves"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        md = context.dynamic_paint
        rd = context.scene.render
        ob = context.object
        indx = ob.modifier_active_index
        try:
            mod = ob.modifiers[indx]
        except IndexError:
            return False                 
        return md and mod.type == 'DYNAMIC_PAINT' and md.ui_type == 'BRUSH' and md.brush_settings and (not rd.use_game_engine)

    def draw(self, context):
        layout = self.layout

        brush = context.dynamic_paint.brush_settings

        layout.prop(brush, "wave_type")
        if brush.wave_type != 'REFLECT':
            row = layout.row()
            row.prop(brush, "wave_factor")
            row.prop(brush, "wave_clamp")

######### Softbody modifier
def softbody_panel_enabled(md):
    return (md.point_cache.is_baked is False)


class PhysicButtonsPanel():
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "modifier"

    @classmethod
    def poll(cls, context):
        ob = context.object
        rd = context.scene.render
        indx = ob.modifier_active_index
        try:
            mod = ob.modifiers[indx]
        except IndexError:
            return False        
        return (ob and (mod.type == 'SOFT_BODY' or ob.type == 'LATTICE'or ob.type == 'CURVE')) and (not rd.use_game_engine) and (context.soft_body)


class PHYSICS_PT_softbody(PhysicButtonsPanel, Panel):
    bl_label = "Soft Body"

    def draw(self, context):
        layout = self.layout

        md = context.soft_body
        ob = context.object

        softbody = md.settings

        # General
        split = layout.split()
        split.enabled = softbody_panel_enabled(md)

        col = split.column()
        col.label(text="Object:")
        col.prop(softbody, "friction")
        col.prop(softbody, "mass")
        col.prop_search(softbody, "vertex_group_mass", ob, "vertex_groups", text="Mass")

        col = split.column()
        col.label(text="Simulation:")
        col.prop(softbody, "speed")


class PHYSICS_PT_softbody_cache(PhysicButtonsPanel, Panel):
    bl_label = "Soft Body Cache"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        md = context.soft_body
        point_cache_ui(self, context, md.point_cache, softbody_panel_enabled(md), 'SOFTBODY')


class PHYSICS_PT_softbody_goal(PhysicButtonsPanel, Panel):
    bl_label = "Soft Body Goal"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        softbody = context.soft_body.settings

        self.layout.active = softbody_panel_enabled(context.soft_body)
        self.layout.prop(softbody, "use_goal", text="")

    def draw(self, context):
        layout = self.layout

        md = context.soft_body
        softbody = md.settings
        ob = context.object

        layout.active = softbody.use_goal and softbody_panel_enabled(md)

        split = layout.split()

        # Goal
        split = layout.split()

        col = split.column()
        col.label(text="Goal Strengths:")
        col.prop(softbody, "goal_default", text="Default")
        sub = col.column(align=True)
        sub.prop(softbody, "goal_min", text="Minimum")
        sub.prop(softbody, "goal_max", text="Maximum")

        col = split.column()
        col.label(text="Goal Settings:")
        col.prop(softbody, "goal_spring", text="Stiffness")
        col.prop(softbody, "goal_friction", text="Damping")

        layout.prop_search(softbody, "vertex_group_goal", ob, "vertex_groups", text="Vertex Group")


class PHYSICS_PT_softbody_edge(PhysicButtonsPanel, Panel):
    bl_label = "Soft Body Edges"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        softbody = context.soft_body.settings

        self.layout.active = softbody_panel_enabled(context.soft_body)
        self.layout.prop(softbody, "use_edges", text="")

    def draw(self, context):
        layout = self.layout

        md = context.soft_body
        softbody = md.settings
        ob = context.object

        layout.active = softbody.use_edges and softbody_panel_enabled(md)

        split = layout.split()

        col = split.column()
        col.label(text="Springs:")
        col.prop(softbody, "pull")
        col.prop(softbody, "push")
        col.prop(softbody, "damping")
        col.prop(softbody, "plastic")
        col.prop(softbody, "bend")
        col.prop(softbody, "spring_length", text="Length")
        col.prop_search(softbody, "vertex_group_spring", ob, "vertex_groups", text="Springs")

        col = split.column()
        col.prop(softbody, "use_stiff_quads")
        sub = col.column()
        sub.active = softbody.use_stiff_quads
        sub.prop(softbody, "shear")

        col.label(text="Aerodynamics:")
        col.row().prop(softbody, "aerodynamics_type", expand=True)
        col.prop(softbody, "aero", text="Factor")

        #sub = col.column()
        #sub.enabled = softbody.aero > 0

        col.label(text="Collision:")
        col.prop(softbody, "use_edge_collision", text="Edge")
        col.prop(softbody, "use_face_collision", text="Face")


class PHYSICS_PT_softbody_collision(PhysicButtonsPanel, Panel):
    bl_label = "Soft Body Self Collision"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        softbody = context.soft_body.settings

        self.layout.active = softbody_panel_enabled(context.soft_body)
        self.layout.prop(softbody, "use_self_collision", text="")

    def draw(self, context):
        layout = self.layout

        md = context.soft_body
        softbody = md.settings

        layout.active = softbody.use_self_collision and softbody_panel_enabled(md)

        layout.label(text="Collision Ball Size Calculation:")
        layout.prop(softbody, "collision_type", expand=True)

        col = layout.column(align=True)
        col.label(text="Ball:")
        col.prop(softbody, "ball_size", text="Size")
        col.prop(softbody, "ball_stiff", text="Stiffness")
        col.prop(softbody, "ball_damp", text="Dampening")


class PHYSICS_PT_softbody_solver(PhysicButtonsPanel, Panel):
    bl_label = "Soft Body Solver"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        md = context.soft_body
        softbody = md.settings

        layout.active = softbody_panel_enabled(md)

        # Solver
        split = layout.split()

        col = split.column(align=True)
        col.label(text="Step Size:")
        col.prop(softbody, "step_min")
        col.prop(softbody, "step_max")
        col.prop(softbody, "use_auto_step", text="Auto-Step")

        col = split.column()
        col.prop(softbody, "error_threshold")
        col.label(text="Helpers:")
        col.prop(softbody, "choke")
        col.prop(softbody, "fuzzy")

        layout.label(text="Diagnostics:")
        layout.prop(softbody, "use_diagnose")
        layout.prop(softbody, "use_estimate_matrix")


class PHYSICS_PT_softbody_field_weights(PhysicButtonsPanel, Panel):
    bl_label = "Soft Body Field Weights"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        md = context.soft_body
        softbody = md.settings

        effector_weights_ui(self, context, softbody.effector_weights, 'SOFTBODY')
        
 ######## Fluid Modifier
class FLUID_MT_presets(Menu):
    bl_label = "Fluid Presets"
    preset_subdir = "fluid"
    preset_operator = "script.execute_preset"
    draw = Menu.draw_preset


class PhysicButtonsPanel():
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "modifier"

    @classmethod
    def poll(cls, context):
        ob = context.object
        rd = context.scene.render
        indx = ob.modifier_active_index
        try:
            mod = ob.modifiers[indx]
        except IndexError:
            return False          
        return (ob and mod.type == 'FLUID_SIMULATION') and (not rd.use_game_engine) and (context.fluid)


class PHYSICS_PT_fluid(PhysicButtonsPanel, Panel):
    bl_label = "Fluid"

    def draw(self, context):
        layout = self.layout

        md = context.fluid
        fluid = md.settings

        col = layout.column()
        if not bpy.app.build_options.mod_fluid:
            col.label("Built without fluids")
            return

        col.prop(fluid, "type")
        if fluid.type not in {'NONE', 'DOMAIN', 'PARTICLE', 'FLUID', 'OBSTACLE'}:
            col.prop(fluid, "use")

        layout = layout.column()
        if fluid.type not in {'NONE', 'DOMAIN', 'PARTICLE', 'FLUID', 'OBSTACLE'}:
            layout.active = fluid.use

        if fluid.type == 'DOMAIN':
            # odd formatting here so translation script can extract string
            layout.operator("fluid.bake", text=iface_("Bake (Req. Memory: %s)") % fluid.memory_estimate,
                            translate=False, icon='MOD_FLUIDSIM')

            if bpy.app.build_options.openmp:
                layout.prop(fluid, "threads", text="Simulation Threads")

            split = layout.split()

            col = split.column()
            col.label(text="Resolution:")
            col.prop(fluid, "resolution", text="Final")
            col.label(text="Render Display:")
            col.prop(fluid, "render_display_mode", text="")

            col = split.column()
            col.label()
            col.prop(fluid, "preview_resolution", text="Preview")
            col.label(text="Viewport Display:")
            col.prop(fluid, "viewport_display_mode", text="")

            split = layout.split()

            col = split.column()
            col.label(text="Time:")
            sub = col.column(align=True)
            sub.prop(fluid, "start_time", text="Start")
            sub.prop(fluid, "end_time", text="End")
            col.prop(fluid, "simulation_rate", text="Speed")

            col = split.column()
            col.label()
            sub = col.column(align=True)
            sub.prop(fluid, "use_speed_vectors")
            sub.prop(fluid, "use_reverse_frames")
            col.prop(fluid, "frame_offset", text="Offset")

            layout.prop(fluid, "filepath", text="")

        elif fluid.type == 'FLUID':
            split = layout.split()

            col = split.column()
            col.label(text="Volume Initialization:")
            col.prop(fluid, "volume_initialization", text="")
            col.prop(fluid, "use_animated_mesh")

            col = split.column()
            col.label(text="Initial Velocity:")
            col.prop(fluid, "initial_velocity", text="")

        elif fluid.type == 'OBSTACLE':
            split = layout.split()

            col = split.column()
            col.label(text="Volume Initialization:")
            col.prop(fluid, "volume_initialization", text="")
            col.prop(fluid, "use_animated_mesh")

            col = split.column()
            subsplit = col.split()
            subcol = subsplit.column()
            if fluid.use_animated_mesh:
                subcol.enabled = False
            subcol.label(text="Slip Type:")
            subcol.prop(fluid, "slip_type", text="")
            if fluid.slip_type == 'PARTIALSLIP':
                subcol.prop(fluid, "partial_slip_factor", slider=True, text="Amount")

            col.label(text="Impact:")
            col.prop(fluid, "impact_factor", text="Factor")

        elif fluid.type == 'INFLOW':
            split = layout.split()

            col = split.column()
            col.label(text="Volume Initialization:")
            col.prop(fluid, "volume_initialization", text="")
            col.prop(fluid, "use_animated_mesh")
            row = col.row()
            row.active = not fluid.use_animated_mesh
            row.prop(fluid, "use_local_coords")

            col = split.column()
            col.label(text="Inflow Velocity:")
            col.prop(fluid, "inflow_velocity", text="")

        elif fluid.type == 'OUTFLOW':
            col = layout.column()
            col.label(text="Volume Initialization:")
            col.prop(fluid, "volume_initialization", text="")
            col.prop(fluid, "use_animated_mesh")

        elif fluid.type == 'PARTICLE':
            split = layout.split()

            col = split.column()
            col.label(text="Influence:")
            col.prop(fluid, "particle_influence", text="Size")
            col.prop(fluid, "alpha_influence", text="Alpha")

            col = split.column()
            col.label(text="Type:")
            col.prop(fluid, "use_drops")
            col.prop(fluid, "use_floats")
            col.prop(fluid, "show_tracer")

            layout.prop(fluid, "filepath", text="")

        elif fluid.type == 'CONTROL':
            split = layout.split()

            col = split.column()
            col.label(text="")
            col.prop(fluid, "quality", slider=True)
            col.prop(fluid, "use_reverse_frames")

            col = split.column()
            col.label(text="Time:")
            sub = col.column(align=True)
            sub.prop(fluid, "start_time", text="Start")
            sub.prop(fluid, "end_time", text="End")

            split = layout.split()

            col = split.column()
            col.label(text="Attraction Force:")
            sub = col.column(align=True)
            sub.prop(fluid, "attraction_strength", text="Strength")
            sub.prop(fluid, "attraction_radius", text="Radius")

            col = split.column()
            col.label(text="Velocity Force:")
            sub = col.column(align=True)
            sub.prop(fluid, "velocity_strength", text="Strength")
            sub.prop(fluid, "velocity_radius", text="Radius")


class PHYSICS_PT_domain_gravity(PhysicButtonsPanel, Panel):
    bl_label = "Fluid World"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        md = context.fluid
        rd = context.scene.render
        ob = context.object
        indx = ob.modifier_active_index
        try:
            mod = ob.modifiers[indx]
        except IndexError:
            return False          
        return md and md.settings and (md.settings.type == 'DOMAIN') and (mod.type == "FLUID_SIMULATION") and (not rd.use_game_engine)

    def draw(self, context):
        layout = self.layout

        fluid = context.fluid.settings
        scene = context.scene

        split = layout.split()

        col = split.column()
        if scene.use_gravity:
            col.label(text="Use Scene Gravity", icon='SCENE_DATA')
            sub = col.column()
            sub.enabled = False
            sub.prop(fluid, "gravity", text="")
        else:
            col.label(text="Gravity:")
            col.prop(fluid, "gravity", text="")

        if scene.unit_settings.system != 'NONE':
            col.label(text="Use Scene Size Units", icon='SCENE_DATA')
            sub = col.column()
            sub.enabled = False
            sub.prop(fluid, "simulation_scale", text="Meters")
        else:
            col.label(text="Real World Size:")
            col.prop(fluid, "simulation_scale", text="Meters")

        col = split.column()
        col.label(text="Viscosity Presets:")
        sub = col.row(align=True)
        sub.menu("FLUID_MT_presets", text=bpy.types.FLUID_MT_presets.bl_label)
        sub.operator("fluid.preset_add", text="", icon='ZOOMIN')
        sub.operator("fluid.preset_add", text="", icon='ZOOMOUT').remove_active = True

        sub = col.column(align=True)
        sub.prop(fluid, "viscosity_base", text="Base")
        sub.prop(fluid, "viscosity_exponent", text="Exponent", slider=True)

        col.label(text="Optimization:")
        col.prop(fluid, "grid_levels", slider=True)
        col.prop(fluid, "compressibility", slider=True)


class PHYSICS_PT_domain_boundary(PhysicButtonsPanel, Panel):
    bl_label = "Fluid Boundary"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        md = context.fluid
        rd = context.scene.render
        ob = context.object
        indx = ob.modifier_active_index
        try:
            mod = ob.modifiers[indx]
        except IndexError:
            return False         
        return md and md.settings and (md.settings.type == 'DOMAIN') and (mod.type == 'FLUID_SIMULATION') and (not rd.use_game_engine)

    def draw(self, context):
        layout = self.layout

        fluid = context.fluid.settings

        split = layout.split()

        col = split.column()
        col.label(text="Slip Type:")
        col.prop(fluid, "slip_type", text="")
        if fluid.slip_type == 'PARTIALSLIP':
            col.prop(fluid, "partial_slip_factor", slider=True, text="Amount")
        col.prop(fluid, "use_surface_noobs")

        col = split.column()
        col.label(text="Surface:")
        col.prop(fluid, "surface_smooth", text="Smoothing")
        col.prop(fluid, "surface_subdivisions", text="Subdivisions")


class PHYSICS_PT_domain_particles(PhysicButtonsPanel, Panel):
    bl_label = "Fluid Particles"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        md = context.fluid
        rd = context.scene.render
        ob = context.object
        indx = ob.modifier_active_index
        try:
            mod = ob.modifiers[indx]
        except IndexError:
            return False         
        return md and md.settings and (md.settings.type == 'DOMAIN') and (mod.type == 'FLUID_SIMULATION') and (not rd.use_game_engine)

    def draw(self, context):
        layout = self.layout

        fluid = context.fluid.settings

        row = layout.row()
        row.prop(fluid, "tracer_particles", text="Tracer")
        row.prop(fluid, "generate_particles", text="Generate")
        
 ######### Smoke Modifier
class PhysicButtonsPanel():
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "modifier"

    @classmethod
    def poll(cls, context):
        ob = context.object
        rd = context.scene.render
        indx = ob.modifier_active_index
        try:
            mod = ob.modifiers[indx]
        except IndexError:
            return False        
        return (ob and mod.type == 'SMOKE') and (not rd.use_game_engine) and (context.smoke)
    



class PHYSICS_PT_smoke(PhysicButtonsPanel, Panel):
    bl_label = "Smoke"

    def draw(self, context):
        layout = self.layout

        md = context.smoke
        ob = context.object

        layout.prop(md, "smoke_type", expand=True)

        if md.smoke_type == 'DOMAIN':
            domain = md.domain_settings

            split = layout.split()

            split.enabled = not domain.point_cache.is_baked

            col = split.column()
            col.label(text="Resolution:")
            col.prop(domain, "resolution_max", text="Divisions")
            col.label(text="Time:")
            col.prop(domain, "time_scale", text="Scale")
            col.label(text="Border Collisions:")
            col.prop(domain, "collision_extents", text="")

            col = split.column()
            col.label(text="Behavior:")
            col.prop(domain, "alpha")
            col.prop(domain, "beta", text="Temp. Diff.")
            col.prop(domain, "vorticity")
            col.prop(domain, "use_dissolve_smoke", text="Dissolve")
            sub = col.column()
            sub.active = domain.use_dissolve_smoke
            sub.prop(domain, "dissolve_speed", text="Time")
            sub.prop(domain, "use_dissolve_smoke_log", text="Slow")

        elif md.smoke_type == 'FLOW':

            flow = md.flow_settings

            layout.prop(flow, "smoke_flow_type", expand=False)

            if flow.smoke_flow_type != "OUTFLOW":
                split = layout.split()
                col = split.column()
                col.label(text="Flow Source:")
                col.prop(flow, "smoke_flow_source", expand=False, text="")
                if flow.smoke_flow_source == "PARTICLES":
                    col.label(text="Particle System:")
                    col.prop_search(flow, "particle_system", ob, "particle_systems", text="")
                    col.prop(flow, "use_particle_size", text="Set Size")
                    sub = col.column()
                    sub.active = flow.use_particle_size
                    sub.prop(flow, "particle_size")
                else:
                    col.prop(flow, "surface_distance")
                    col.prop(flow, "volume_density")

                sub = col.column(align=True)
                sub.prop(flow, "use_initial_velocity")

                sub = sub.column()
                sub.active = flow.use_initial_velocity
                sub.prop(flow, "velocity_factor")
                if flow.smoke_flow_source == "MESH":
                    sub.prop(flow, "velocity_normal")
                    #sub.prop(flow, "velocity_random")

                sub = split.column()
                sub.label(text="Initial Values:")
                sub.prop(flow, "use_absolute")
                if flow.smoke_flow_type in {'SMOKE', 'BOTH'}:
                    sub.prop(flow, "density")
                    sub.prop(flow, "temperature")
                    sub.prop(flow, "smoke_color")
                if flow.smoke_flow_type in {'FIRE', 'BOTH'}:
                    sub.prop(flow, "fuel_amount")
                sub.label(text="Sampling:")
                sub.prop(flow, "subframes")

        elif md.smoke_type == 'COLLISION':
            coll = md.coll_settings

            split = layout.split()

            col = split.column()
            col.prop(coll, "collision_type")


class PHYSICS_PT_smoke_flow_advanced(PhysicButtonsPanel, Panel):
    bl_label = "Smoke Flow Advanced"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        md = context.smoke
        ob = context.object
        indx = ob.modifier_active_index
        try:
            mod = ob.modifiers[indx]
        except IndexError:
            return False            
        return md and (mod.type == 'SMOKE') and (md.smoke_type == 'FLOW') and (md.flow_settings.smoke_flow_source == "MESH")

    def draw(self, context):
        layout = self.layout
        ob = context.object
        flow = context.smoke.flow_settings

        split = layout.split()
        col = split.column()

        col.prop(flow, "use_texture")
        sub = col.column()
        sub.active = flow.use_texture
        sub.prop(flow, "noise_texture", text="")
        sub.label(text="Mapping:")
        sub.prop(flow, "texture_map_type", expand=False, text="")
        if flow.texture_map_type == "UV":
            sub.prop_search(flow, "uv_layer", ob.data, "uv_textures", text="")
        if flow.texture_map_type == "AUTO":
            sub.prop(flow, "texture_size")
        sub.prop(flow, "texture_offset")

        col = split.column()
        col.label(text="Vertex Group:")
        col.prop_search(flow, "density_vertex_group", ob, "vertex_groups", text="")


class PHYSICS_PT_smoke_fire(PhysicButtonsPanel, Panel):
    bl_label = "Smoke Flames"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        md = context.smoke
        ob = context.object
        indx = ob.modifier_active_index
        try:
            mod = ob.modifiers[indx]
        except IndexError:
            return False            
        return md and (mod.type == 'SMOKE') and (md.smoke_type == 'DOMAIN')

    def draw(self, context):
        layout = self.layout
        domain = context.smoke.domain_settings

        split = layout.split()
        split.enabled = not domain.point_cache.is_baked

        col = split.column(align=True)
        col.label(text="Reaction:")
        col.prop(domain, "burning_rate")
        col.prop(domain, "flame_smoke")
        col.prop(domain, "flame_vorticity")

        col = split.column(align=True)
        col.label(text="Temperatures:")
        col.prop(domain, "flame_ignition")
        col.prop(domain, "flame_max_temp")
        col.prop(domain, "flame_smoke_color")


class PHYSICS_PT_smoke_adaptive_domain(PhysicButtonsPanel, Panel):
    bl_label = "Smoke Adaptive Domain"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        md = context.smoke
        ob = context.object
        indx = ob.modifier_active_index
        try:
            mod = ob.modifiers[indx]
        except IndexError:
            return False            
        return md and (md.smoke_type == 'DOMAIN') and (mod.type == 'SMOKE')

    def draw_header(self, context):
        md = context.smoke.domain_settings

        self.layout.prop(md, "use_adaptive_domain", text="")

    def draw(self, context):
        layout = self.layout

        domain = context.smoke.domain_settings
        layout.active = domain.use_adaptive_domain

        split = layout.split()
        split.enabled = (not domain.point_cache.is_baked)

        col = split.column(align=True)
        col.label(text="Resolution:")
        col.prop(domain, "additional_res")
        col.prop(domain, "adapt_margin")

        col = split.column(align=True)
        col.label(text="Advanced:")
        col.prop(domain, "adapt_threshold")


class PHYSICS_PT_smoke_highres(PhysicButtonsPanel, Panel):
    bl_label = "Smoke High Resolution"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        md = context.smoke
        rd = context.scene.render
        ob = context.object
        indx = ob.modifier_active_index
        try:
            mod = ob.modifiers[indx]
        except IndexError:
            return False            
        return md and (mod.type == 'SMOKE') and (md.smoke_type == 'DOMAIN') and (not rd.use_game_engine) 

    def draw_header(self, context):
        md = context.smoke.domain_settings

        self.layout.prop(md, "use_high_resolution", text="")

    def draw(self, context):
        layout = self.layout

        md = context.smoke.domain_settings

        layout.active = md.use_high_resolution

        split = layout.split()
        split.enabled = not md.point_cache.is_baked

        col = split.column()
        col.label(text="Resolution:")
        col.prop(md, "amplify", text="Divisions")
        col.label(text="Flow Sampling:")
        col.row().prop(md, "highres_sampling", text="")

        col = split.column()
        col.label(text="Noise Method:")
        col.row().prop(md, "noise_type", text="")
        col.prop(md, "strength")

        layout.prop(md, "show_high_resolution")


class PHYSICS_PT_smoke_groups(PhysicButtonsPanel, Panel):
    bl_label = "Smoke Groups"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        md = context.smoke
        rd = context.scene.render
        ob = context.object
        indx = ob.modifier_active_index
        try:
            mod = ob.modifiers[indx]
        except IndexError:
            return False            
        return md and (mod.type == 'SMOKE') and (md.smoke_type == 'DOMAIN') and (not rd.use_game_engine)

    def draw(self, context):
        layout = self.layout
        domain = context.smoke.domain_settings

        split = layout.split()

        col = split.column()
        col.label(text="Flow Group:")
        col.prop(domain, "fluid_group", text="")

        #col.label(text="Effector Group:")
        #col.prop(domain, "effector_group", text="")

        col = split.column()
        col.label(text="Collision Group:")
        col.prop(domain, "collision_group", text="")


class PHYSICS_PT_smoke_cache(PhysicButtonsPanel, Panel):
    bl_label = "Smoke Cache"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        md = context.smoke
        rd = context.scene.render
        ob = context.object
        indx = ob.modifier_active_index
        try:
            mod = ob.modifiers[indx]
        except IndexError:
            return False            
        return md and (mod.type == 'SMOKE') and (md.smoke_type == 'DOMAIN') and (not rd.use_game_engine)

    def draw(self, context):
        layout = self.layout

        md = context.smoke.domain_settings
        cache = md.point_cache

        layout.label(text="Compression:")
        layout.prop(md, "point_cache_compress_type", expand=True)

        point_cache_ui(self, context, cache, (cache.is_baked is False), 'SMOKE')


class PHYSICS_PT_smoke_field_weights(PhysicButtonsPanel, Panel):
    bl_label = "Smoke Field Weights"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        md = context.smoke
        rd = context.scene.render
        ob = context.object
        indx = ob.modifier_active_index
        try:
            mod = ob.modifiers[indx]
        except IndexError:
            return False            
        return md and (mod.type == 'SMOKE') and (md.smoke_type == 'DOMAIN') and (not rd.use_game_engine)

    def draw(self, context):
        domain = context.smoke.domain_settings
        effector_weights_ui(self, context, domain.effector_weights, 'SMOKE')    



def register():
    bpy.utils.register_module(__name__)
    bpy.types.Object.modifier_active_index = bpy.props.IntProperty()


def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Object.modifier_active_index


if __name__ == "__main__":
    register()

