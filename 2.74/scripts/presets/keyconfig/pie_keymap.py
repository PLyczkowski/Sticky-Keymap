import bpy
import os

def kmi_props_setattr(kmi_props, attr, value):
    try:
        setattr(kmi_props, attr, value)
    except AttributeError:
        print("Warning: property '%s' not found in keymap item '%s'" %
              (attr, kmi_props.__class__.__name__))
    except Exception as e:
        print("Warning: %r" % e)

wm = bpy.context.window_manager
kc = wm.keyconfigs.new(os.path.splitext(os.path.basename(__file__))[0])

# Map Object Mode
km = kc.keymaps.new('Object Mode', space_type='EMPTY', region_type='WINDOW', modal=False)

kmi = km.keymap_items.new('wm.context_cycle_enum', 'O', 'PRESS', shift=True)
kmi_props_setattr(kmi.properties, 'data_path', 'tool_settings.proportional_edit_falloff')
kmi = km.keymap_items.new('wm.context_toggle', 'O', 'PRESS')
kmi_props_setattr(kmi.properties, 'data_path', 'tool_settings.use_proportional_edit_objects')
kmi = km.keymap_items.new('view3d.game_start', 'P', 'PRESS')
kmi = km.keymap_items.new('object.select_all', 'A', 'CLICK', ctrl=True)
kmi_props_setattr(kmi.properties, 'action', 'SELECT')
kmi = km.keymap_items.new('object.select_all', 'I', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'action', 'INVERT')
kmi = km.keymap_items.new('object.select_linked', 'L', 'PRESS', shift=True)
kmi = km.keymap_items.new('object.select_grouped', 'G', 'PRESS', shift=True)
kmi = km.keymap_items.new('object.select_mirror', 'M', 'PRESS', shift=True, ctrl=True)
kmi = km.keymap_items.new('object.select_hierarchy', 'LEFT_BRACKET', 'PRESS')
kmi_props_setattr(kmi.properties, 'direction', 'PARENT')
kmi_props_setattr(kmi.properties, 'extend', False)
kmi = km.keymap_items.new('object.select_hierarchy', 'LEFT_BRACKET', 'PRESS', shift=True)
kmi_props_setattr(kmi.properties, 'direction', 'PARENT')
kmi_props_setattr(kmi.properties, 'extend', True)
kmi = km.keymap_items.new('object.select_hierarchy', 'RIGHT_BRACKET', 'PRESS')
kmi_props_setattr(kmi.properties, 'direction', 'CHILD')
kmi_props_setattr(kmi.properties, 'extend', False)
kmi = km.keymap_items.new('object.select_hierarchy', 'RIGHT_BRACKET', 'PRESS', shift=True)
kmi_props_setattr(kmi.properties, 'direction', 'CHILD')
kmi_props_setattr(kmi.properties, 'extend', True)
kmi = km.keymap_items.new('object.parent_set', 'P', 'PRESS', ctrl=True)
kmi = km.keymap_items.new('object.parent_no_inverse_set', 'P', 'PRESS', shift=True, ctrl=True)
kmi = km.keymap_items.new('object.parent_clear', 'P', 'PRESS', alt=True)
kmi = km.keymap_items.new('object.track_set', 'T', 'PRESS', ctrl=True)
kmi = km.keymap_items.new('object.track_clear', 'T', 'PRESS', alt=True)
kmi = km.keymap_items.new('object.constraint_add_with_targets', 'C', 'PRESS', shift=True, ctrl=True)
kmi = km.keymap_items.new('object.constraints_clear', 'C', 'PRESS', ctrl=True, alt=True)
kmi = km.keymap_items.new('object.location_clear', 'G', 'PRESS', alt=True)
kmi = km.keymap_items.new('object.rotation_clear', 'R', 'PRESS', alt=True)
kmi = km.keymap_items.new('object.scale_clear', 'S', 'PRESS', alt=True)
kmi = km.keymap_items.new('object.origin_clear', 'O', 'PRESS', alt=True)
kmi = km.keymap_items.new('object.hide_view_clear', 'H', 'PRESS', alt=True)
kmi = km.keymap_items.new('object.hide_view_set', 'H', 'PRESS')
kmi_props_setattr(kmi.properties, 'unselected', False)
kmi = km.keymap_items.new('object.hide_view_set', 'H', 'PRESS', shift=True)
kmi_props_setattr(kmi.properties, 'unselected', True)
kmi = km.keymap_items.new('object.hide_render_clear', 'H', 'PRESS', ctrl=True, alt=True)
kmi = km.keymap_items.new('object.hide_render_set', 'H', 'PRESS', ctrl=True)
kmi = km.keymap_items.new('object.move_to_layer', 'M', 'PRESS')
kmi = km.keymap_items.new('object.delete', 'X', 'PRESS')
kmi_props_setattr(kmi.properties, 'use_global', False)
kmi = km.keymap_items.new('object.delete', 'X', 'PRESS', shift=True)
kmi_props_setattr(kmi.properties, 'use_global', True)
kmi = km.keymap_items.new('object.delete', 'DEL', 'PRESS')
kmi_props_setattr(kmi.properties, 'use_global', False)
kmi = km.keymap_items.new('object.delete', 'DEL', 'PRESS', shift=True)
kmi_props_setattr(kmi.properties, 'use_global', True)
kmi = km.keymap_items.new('wm.call_menu', 'F', 'PRESS')
kmi_props_setattr(kmi.properties, 'name', 'INFO_MT_add')
kmi = km.keymap_items.new('object.duplicates_make_real', 'A', 'PRESS', shift=True, ctrl=True)
kmi = km.keymap_items.new('wm.call_menu', 'A', 'PRESS', alt=True)
kmi_props_setattr(kmi.properties, 'name', 'VIEW3D_MT_object_apply')
kmi = km.keymap_items.new('wm.call_menu', 'U', 'PRESS')
kmi_props_setattr(kmi.properties, 'name', 'VIEW3D_MT_make_single_user')
kmi = km.keymap_items.new('wm.call_menu', 'L', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'name', 'VIEW3D_MT_make_links')
kmi = km.keymap_items.new('object.duplicate_move', 'D', 'PRESS', shift=True)
kmi = km.keymap_items.new('object.duplicate_move_linked', 'D', 'PRESS', alt=True)
kmi = km.keymap_items.new('object.join', 'J', 'PRESS', ctrl=True)
kmi = km.keymap_items.new('object.convert', 'C', 'PRESS', alt=True)
kmi = km.keymap_items.new('object.proxy_make', 'P', 'PRESS', ctrl=True, alt=True)
kmi = km.keymap_items.new('object.make_local', 'L', 'PRESS')
kmi = km.keymap_items.new('anim.keyframe_insert_menu', 'I', 'PRESS')
kmi = km.keymap_items.new('anim.keyframe_delete_v3d', 'I', 'PRESS', alt=True)
kmi = km.keymap_items.new('anim.keying_set_active_set', 'I', 'PRESS', shift=True, ctrl=True, alt=True)
kmi = km.keymap_items.new('group.create', 'G', 'PRESS', ctrl=True)
kmi = km.keymap_items.new('group.objects_remove', 'G', 'PRESS', ctrl=True, alt=True)
kmi = km.keymap_items.new('group.objects_remove_all', 'G', 'PRESS', shift=True, ctrl=True, alt=True)
kmi = km.keymap_items.new('group.objects_add_active', 'G', 'PRESS', shift=True, ctrl=True)
kmi = km.keymap_items.new('group.objects_remove_active', 'G', 'PRESS', shift=True, alt=True)
kmi = km.keymap_items.new('wm.call_menu', 'W', 'PRESS')
kmi_props_setattr(kmi.properties, 'name', 'VIEW3D_MT_object_specials')
kmi.active = False
kmi = km.keymap_items.new('object.data_transfer', 'T', 'PRESS', shift=True, ctrl=True)
kmi = km.keymap_items.new('object.subdivision_set', 'ZERO', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'level', 0)
kmi = km.keymap_items.new('object.subdivision_set', 'ONE', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'level', 1)
kmi = km.keymap_items.new('object.subdivision_set', 'TWO', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'level', 2)
kmi = km.keymap_items.new('object.subdivision_set', 'THREE', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'level', 3)
kmi = km.keymap_items.new('object.subdivision_set', 'FOUR', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'level', 4)
kmi = km.keymap_items.new('object.subdivision_set', 'FIVE', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'level', 5)
kmi = km.keymap_items.new('view3d.manipulator', 'SELECTMOUSE', 'PRESS')
kmi_props_setattr(kmi.properties, 'release_confirm', True)

# Map Mesh
km = kc.keymaps.new('Mesh', space_type='EMPTY', region_type='WINDOW', modal=False)

kmi = km.keymap_items.new('mesh.loopcut_slide', 'R', 'PRESS', ctrl=True)
kmi = km.keymap_items.new('mesh.inset', 'I', 'PRESS')
kmi = km.keymap_items.new('mesh.poke', 'P', 'PRESS', alt=True)
kmi = km.keymap_items.new('mesh.bevel', 'B', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'vertex_only', False)
kmi = km.keymap_items.new('mesh.bevel', 'B', 'PRESS', shift=True, ctrl=True)
kmi_props_setattr(kmi.properties, 'vertex_only', True)
kmi = km.keymap_items.new('mesh.loop_select', 'SELECTMOUSE', 'PRESS', alt=True)
kmi_props_setattr(kmi.properties, 'extend', False)
kmi_props_setattr(kmi.properties, 'deselect', False)
kmi_props_setattr(kmi.properties, 'toggle', False)
kmi = km.keymap_items.new('mesh.loop_select', 'SELECTMOUSE', 'PRESS', shift=True, alt=True)
kmi_props_setattr(kmi.properties, 'extend', False)
kmi_props_setattr(kmi.properties, 'deselect', False)
kmi_props_setattr(kmi.properties, 'toggle', True)
kmi = km.keymap_items.new('mesh.edgering_select', 'SELECTMOUSE', 'PRESS', ctrl=True, alt=True)
kmi_props_setattr(kmi.properties, 'extend', False)
kmi_props_setattr(kmi.properties, 'deselect', False)
kmi_props_setattr(kmi.properties, 'toggle', False)
kmi = km.keymap_items.new('mesh.edgering_select', 'SELECTMOUSE', 'PRESS', shift=True, ctrl=True, alt=True)
kmi_props_setattr(kmi.properties, 'extend', False)
kmi_props_setattr(kmi.properties, 'deselect', False)
kmi_props_setattr(kmi.properties, 'toggle', True)
kmi = km.keymap_items.new('mesh.shortest_path_pick', 'SELECTMOUSE', 'PRESS', ctrl=True)
kmi.active = False
kmi = km.keymap_items.new('mesh.select_all', 'A', 'CLICK', ctrl=True)
kmi_props_setattr(kmi.properties, 'action', 'SELECT')
kmi = km.keymap_items.new('mesh.select_all', 'I', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'action', 'INVERT')
kmi = km.keymap_items.new('mesh.select_more', 'NUMPAD_PLUS', 'PRESS', ctrl=True)
kmi = km.keymap_items.new('mesh.select_less', 'NUMPAD_MINUS', 'PRESS', ctrl=True)
kmi = km.keymap_items.new('mesh.select_non_manifold', 'M', 'PRESS', shift=True, ctrl=True, alt=True)
kmi = km.keymap_items.new('mesh.select_linked', 'L', 'PRESS', ctrl=True)
kmi = km.keymap_items.new('mesh.select_linked_pick', 'SELECTMOUSE', 'DOUBLE_CLICK')
kmi_props_setattr(kmi.properties, 'deselect', False)
kmi = km.keymap_items.new('mesh.select_linked_pick', 'SELECTMOUSE', 'HOLD', ctrl=True)
kmi_props_setattr(kmi.properties, 'deselect', True)
kmi = km.keymap_items.new('mesh.faces_select_linked_flat', 'F', 'PRESS', shift=True, ctrl=True, alt=True)
kmi = km.keymap_items.new('wm.call_menu', 'G', 'PRESS', shift=True)
kmi_props_setattr(kmi.properties, 'name', 'VIEW3D_MT_edit_mesh_select_similar')
kmi = km.keymap_items.new('wm.call_menu', 'TAB', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'name', 'VIEW3D_MT_edit_mesh_select_mode')
kmi = km.keymap_items.new('mesh.hide', 'H', 'PRESS')
kmi_props_setattr(kmi.properties, 'unselected', False)
kmi = km.keymap_items.new('mesh.hide', 'H', 'PRESS', shift=True)
kmi_props_setattr(kmi.properties, 'unselected', True)
kmi = km.keymap_items.new('mesh.reveal', 'H', 'PRESS', alt=True)
kmi = km.keymap_items.new('mesh.normals_make_consistent', 'N', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'inside', False)
kmi = km.keymap_items.new('mesh.normals_make_consistent', 'N', 'PRESS', shift=True, ctrl=True)
kmi_props_setattr(kmi.properties, 'inside', True)
kmi = km.keymap_items.new('view3d.edit_mesh_extrude_move_normal', 'E', 'CLICK')
kmi = km.keymap_items.new('wm.call_menu', 'E', 'PRESS', alt=True)
kmi_props_setattr(kmi.properties, 'name', 'VIEW3D_MT_edit_mesh_extrude')
kmi = km.keymap_items.new('transform.edge_crease', 'E', 'PRESS', shift=True)
kmi = km.keymap_items.new('mesh.spin', 'R', 'PRESS', alt=True)
kmi = km.keymap_items.new('mesh.fill', 'F', 'PRESS', alt=True)
kmi = km.keymap_items.new('mesh.beautify_fill', 'F', 'PRESS', shift=True, alt=True)
kmi = km.keymap_items.new('mesh.quads_convert_to_tris', 'T', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'quad_method', 'BEAUTY')
kmi_props_setattr(kmi.properties, 'ngon_method', 'BEAUTY')
kmi = km.keymap_items.new('mesh.quads_convert_to_tris', 'T', 'PRESS', shift=True, ctrl=True)
kmi_props_setattr(kmi.properties, 'quad_method', 'FIXED')
kmi_props_setattr(kmi.properties, 'ngon_method', 'CLIP')
kmi = km.keymap_items.new('mesh.tris_convert_to_quads', 'J', 'PRESS', alt=True)
kmi = km.keymap_items.new('mesh.rip_move', 'V', 'PRESS')
kmi = km.keymap_items.new('mesh.rip_move_fill', 'V', 'PRESS', alt=True)
kmi = km.keymap_items.new('mesh.rip_edge_move', 'D', 'PRESS', alt=True)
kmi = km.keymap_items.new('mesh.merge', 'M', 'PRESS', alt=True)
kmi = km.keymap_items.new('transform.shrink_fatten', 'S', 'PRESS', alt=True)
kmi = km.keymap_items.new('mesh.edge_face_add', 'F', 'PRESS')
kmi = km.keymap_items.new('mesh.duplicate_move', 'D', 'PRESS', shift=True)
kmi = km.keymap_items.new('wm.call_menu', 'A', 'PRESS', shift=True)
kmi_props_setattr(kmi.properties, 'name', 'INFO_MT_mesh_add')
kmi = km.keymap_items.new('mesh.separate', 'P', 'PRESS')
kmi = km.keymap_items.new('mesh.split', 'Y', 'PRESS')
kmi = km.keymap_items.new('mesh.vert_connect_path', 'J', 'PRESS')
kmi = km.keymap_items.new('transform.vert_slide', 'V', 'PRESS', shift=True)
kmi = km.keymap_items.new('mesh.dupli_extrude_cursor', 'ACTIONMOUSE', 'CLICK', ctrl=True)
kmi_props_setattr(kmi.properties, 'rotate_source', True)
kmi = km.keymap_items.new('mesh.dupli_extrude_cursor', 'ACTIONMOUSE', 'PRESS', shift=True, ctrl=True)
kmi_props_setattr(kmi.properties, 'rotate_source', False)
kmi = km.keymap_items.new('wm.call_menu', 'X', 'PRESS')
kmi_props_setattr(kmi.properties, 'name', 'VIEW3D_MT_edit_mesh_delete')
kmi = km.keymap_items.new('wm.call_menu', 'DEL', 'PRESS')
kmi_props_setattr(kmi.properties, 'name', 'VIEW3D_MT_edit_mesh_delete')
kmi = km.keymap_items.new('mesh.dissolve_mode', 'X', 'PRESS', ctrl=True)
kmi = km.keymap_items.new('mesh.dissolve_mode', 'DEL', 'PRESS', ctrl=True)
kmi = km.keymap_items.new('mesh.knife_tool', 'C', 'CLICK')
kmi_props_setattr(kmi.properties, 'use_occlude_geometry', True)
kmi_props_setattr(kmi.properties, 'only_selected', False)
kmi = km.keymap_items.new('mesh.knife_tool', 'K', 'PRESS', shift=True)
kmi_props_setattr(kmi.properties, 'use_occlude_geometry', False)
kmi_props_setattr(kmi.properties, 'only_selected', True)
kmi = km.keymap_items.new('object.vertex_parent_set', 'P', 'PRESS', ctrl=True)
kmi = km.keymap_items.new('wm.call_menu', 'W', 'PRESS')
kmi_props_setattr(kmi.properties, 'name', 'VIEW3D_MT_edit_mesh_specials')
kmi.active = False
kmi = km.keymap_items.new('wm.call_menu', 'F', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'name', 'VIEW3D_MT_edit_mesh_faces')
kmi = km.keymap_items.new('wm.call_menu', 'E', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'name', 'VIEW3D_MT_edit_mesh_edges')
kmi = km.keymap_items.new('wm.call_menu', 'V', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'name', 'VIEW3D_MT_edit_mesh_vertices')
kmi = km.keymap_items.new('wm.call_menu', 'H', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'name', 'VIEW3D_MT_hook')
kmi = km.keymap_items.new('wm.call_menu', 'U', 'PRESS')
kmi_props_setattr(kmi.properties, 'name', 'VIEW3D_MT_uv_map')
kmi = km.keymap_items.new('wm.call_menu', 'G', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'name', 'VIEW3D_MT_vertex_group')
kmi = km.keymap_items.new('object.subdivision_set', 'ZERO', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'level', 0)
kmi = km.keymap_items.new('object.subdivision_set', 'ONE', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'level', 1)
kmi = km.keymap_items.new('object.subdivision_set', 'TWO', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'level', 2)
kmi = km.keymap_items.new('object.subdivision_set', 'THREE', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'level', 3)
kmi = km.keymap_items.new('object.subdivision_set', 'FOUR', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'level', 4)
kmi = km.keymap_items.new('object.subdivision_set', 'FIVE', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'level', 5)
kmi = km.keymap_items.new('wm.context_cycle_enum', 'O', 'PRESS', shift=True)
kmi_props_setattr(kmi.properties, 'data_path', 'tool_settings.proportional_edit_falloff')
kmi = km.keymap_items.new('wm.context_toggle_enum', 'O', 'PRESS')
kmi_props_setattr(kmi.properties, 'data_path', 'tool_settings.proportional_edit')
kmi_props_setattr(kmi.properties, 'value_1', 'DISABLED')
kmi_props_setattr(kmi.properties, 'value_2', 'ENABLED')
kmi = km.keymap_items.new('wm.context_toggle_enum', 'O', 'PRESS', alt=True)
kmi_props_setattr(kmi.properties, 'data_path', 'tool_settings.proportional_edit')
kmi_props_setattr(kmi.properties, 'value_1', 'DISABLED')
kmi_props_setattr(kmi.properties, 'value_2', 'CONNECTED')
kmi = km.keymap_items.new('view3d.manipulator', 'SELECTMOUSE', 'PRESS')
kmi_props_setattr(kmi.properties, 'release_confirm', True)
kmi = km.keymap_items.new('mesh.select_linked_pick', 'SELECTMOUSE', 'HOLD', shift=True)
kmi = km.keymap_items.new('mesh.select_mode', 'ONE', 'CLICK')
kmi = km.keymap_items.new('mesh.select_mode', 'TWO', 'CLICK')
kmi_props_setattr(kmi.properties, 'type', 'EDGE')
kmi = km.keymap_items.new('mesh.select_mode', 'THREE', 'CLICK')
kmi_props_setattr(kmi.properties, 'type', 'FACE')
kmi = km.keymap_items.new('mesh.select_mode', 'ONE', 'PRESS', shift=True)
kmi_props_setattr(kmi.properties, 'use_extend', True)
kmi_props_setattr(kmi.properties, 'use_expand', False)
kmi_props_setattr(kmi.properties, 'action', 'TOGGLE')
kmi = km.keymap_items.new('mesh.select_mode', 'TWO', 'PRESS', shift=True)
kmi_props_setattr(kmi.properties, 'use_extend', True)
kmi_props_setattr(kmi.properties, 'type', 'EDGE')
kmi_props_setattr(kmi.properties, 'action', 'TOGGLE')
kmi = km.keymap_items.new('mesh.select_mode', 'THREE', 'PRESS', shift=True)
kmi_props_setattr(kmi.properties, 'use_extend', True)
kmi_props_setattr(kmi.properties, 'type', 'FACE')
kmi_props_setattr(kmi.properties, 'action', 'TOGGLE')
kmi = km.keymap_items.new('wm.call_menu', 'ONE', 'DOUBLE_CLICK')
kmi_props_setattr(kmi.properties, 'name', 'VIEW3D_MT_edit_mesh_vertices')
kmi.active = False
kmi = km.keymap_items.new('wm.call_menu', 'TWO', 'DOUBLE_CLICK')
kmi_props_setattr(kmi.properties, 'name', 'VIEW3D_MT_edit_mesh_edges')
kmi.active = False
kmi = km.keymap_items.new('wm.call_menu', 'THREE', 'DOUBLE_CLICK')
kmi_props_setattr(kmi.properties, 'name', 'VIEW3D_MT_edit_mesh_faces')
kmi.active = False

# Map 3D View
km = kc.keymaps.new('3D View', space_type='VIEW_3D', region_type='WINDOW', modal=False)

kmi = km.keymap_items.new('view3d.cursor3d', 'RIGHTMOUSE', 'PRESS', alt=True)
kmi = km.keymap_items.new('wm.call_menu', 'ACTIONMOUSE', 'PRESS')
kmi_props_setattr(kmi.properties, 'name', 'VIEW3D_MT_rRMB')
kmi = km.keymap_items.new('view3d.cursor3d', 'RIGHTMOUSE', 'PRESS', ctrl=True)
kmi = km.keymap_items.new('view3d.rotate', 'MIDDLEMOUSE', 'PRESS')
kmi = km.keymap_items.new('view3d.move', 'MIDDLEMOUSE', 'PRESS', shift=True)
kmi = km.keymap_items.new('view3d.zoom', 'MIDDLEMOUSE', 'PRESS', ctrl=True)
kmi = km.keymap_items.new('view3d.dolly', 'MIDDLEMOUSE', 'PRESS', shift=True, ctrl=True)
kmi = km.keymap_items.new('view3d.view_selected', 'SPACE', 'PRESS')
kmi_props_setattr(kmi.properties, 'use_all_regions', True)
kmi = km.keymap_items.new('view3d.view_selected', 'NUMPAD_PERIOD', 'PRESS')
kmi_props_setattr(kmi.properties, 'use_all_regions', False)
kmi = km.keymap_items.new('view3d.view_lock_to_active', 'NUMPAD_PERIOD', 'PRESS', shift=True)
kmi = km.keymap_items.new('view3d.view_lock_clear', 'NUMPAD_PERIOD', 'PRESS', alt=True)
kmi = km.keymap_items.new('view3d.navigate', 'F', 'PRESS', shift=True)
kmi = km.keymap_items.new('view3d.smoothview', 'TIMER1', 'ANY', any=True)
kmi = km.keymap_items.new('view3d.rotate', 'TRACKPADPAN', 'ANY')
kmi = km.keymap_items.new('view3d.rotate', 'MOUSEROTATE', 'ANY')
kmi = km.keymap_items.new('view3d.move', 'TRACKPADPAN', 'ANY', shift=True)
kmi = km.keymap_items.new('view3d.zoom', 'TRACKPADZOOM', 'ANY')
kmi = km.keymap_items.new('view3d.zoom', 'TRACKPADPAN', 'ANY', ctrl=True)
kmi = km.keymap_items.new('view3d.zoom', 'NUMPAD_PLUS', 'PRESS')
kmi_props_setattr(kmi.properties, 'delta', 1)
kmi = km.keymap_items.new('view3d.zoom', 'NUMPAD_MINUS', 'PRESS')
kmi_props_setattr(kmi.properties, 'delta', -1)
kmi = km.keymap_items.new('view3d.zoom', 'EQUAL', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'delta', 1)
kmi = km.keymap_items.new('view3d.zoom', 'MINUS', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'delta', -1)
kmi = km.keymap_items.new('view3d.zoom', 'WHEELINMOUSE', 'PRESS')
kmi_props_setattr(kmi.properties, 'delta', 1)
kmi = km.keymap_items.new('view3d.zoom', 'WHEELOUTMOUSE', 'PRESS')
kmi_props_setattr(kmi.properties, 'delta', -1)
kmi = km.keymap_items.new('view3d.dolly', 'NUMPAD_PLUS', 'PRESS', shift=True)
kmi_props_setattr(kmi.properties, 'delta', 1)
kmi = km.keymap_items.new('view3d.dolly', 'NUMPAD_MINUS', 'PRESS', shift=True)
kmi_props_setattr(kmi.properties, 'delta', -1)
kmi = km.keymap_items.new('view3d.dolly', 'EQUAL', 'PRESS', shift=True, ctrl=True)
kmi_props_setattr(kmi.properties, 'delta', 1)
kmi = km.keymap_items.new('view3d.dolly', 'MINUS', 'PRESS', shift=True, ctrl=True)
kmi_props_setattr(kmi.properties, 'delta', -1)
kmi = km.keymap_items.new('view3d.zoom_camera_1_to_1', 'NUMPAD_ENTER', 'PRESS', shift=True)
kmi = km.keymap_items.new('view3d.view_center_camera', 'HOME', 'PRESS')
kmi = km.keymap_items.new('view3d.view_center_lock', 'HOME', 'PRESS')
kmi = km.keymap_items.new('view3d.view_center_cursor', 'HOME', 'PRESS', alt=True)
kmi = km.keymap_items.new('view3d.view_center_pick', 'F', 'PRESS', alt=True)
kmi = km.keymap_items.new('view3d.view_all', 'HOME', 'PRESS')
kmi_props_setattr(kmi.properties, 'center', False)
kmi = km.keymap_items.new('view3d.view_all', 'HOME', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'use_all_regions', True)
kmi_props_setattr(kmi.properties, 'center', False)
kmi = km.keymap_items.new('view3d.view_all', 'C', 'PRESS', shift=True)
kmi_props_setattr(kmi.properties, 'center', True)
kmi = km.keymap_items.new('view3d.viewnumpad', 'NUMPAD_0', 'PRESS')
kmi_props_setattr(kmi.properties, 'type', 'CAMERA')
kmi = km.keymap_items.new('view3d.viewnumpad', 'NUMPAD_1', 'PRESS')
kmi_props_setattr(kmi.properties, 'type', 'FRONT')
kmi = km.keymap_items.new('view3d.view_orbit', 'NUMPAD_2', 'PRESS')
kmi_props_setattr(kmi.properties, 'type', 'ORBITDOWN')
kmi = km.keymap_items.new('view3d.viewnumpad', 'NUMPAD_3', 'PRESS')
kmi_props_setattr(kmi.properties, 'type', 'RIGHT')
kmi = km.keymap_items.new('view3d.view_orbit', 'NUMPAD_4', 'PRESS')
kmi_props_setattr(kmi.properties, 'type', 'ORBITLEFT')
kmi = km.keymap_items.new('view3d.view_persportho', 'NUMPAD_5', 'PRESS')
kmi = km.keymap_items.new('view3d.view_orbit', 'NUMPAD_6', 'PRESS')
kmi_props_setattr(kmi.properties, 'type', 'ORBITRIGHT')
kmi = km.keymap_items.new('view3d.viewnumpad', 'NUMPAD_7', 'PRESS')
kmi_props_setattr(kmi.properties, 'type', 'TOP')
kmi = km.keymap_items.new('view3d.view_orbit', 'NUMPAD_8', 'PRESS')
kmi_props_setattr(kmi.properties, 'type', 'ORBITUP')
kmi = km.keymap_items.new('view3d.viewnumpad', 'NUMPAD_1', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'type', 'BACK')
kmi = km.keymap_items.new('view3d.viewnumpad', 'NUMPAD_3', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'type', 'LEFT')
kmi = km.keymap_items.new('view3d.viewnumpad', 'NUMPAD_7', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'type', 'BOTTOM')
kmi = km.keymap_items.new('view3d.view_pan', 'NUMPAD_2', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'type', 'PANDOWN')
kmi = km.keymap_items.new('view3d.view_pan', 'NUMPAD_4', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'type', 'PANLEFT')
kmi = km.keymap_items.new('view3d.view_pan', 'NUMPAD_6', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'type', 'PANRIGHT')
kmi = km.keymap_items.new('view3d.view_pan', 'NUMPAD_8', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'type', 'PANUP')
kmi = km.keymap_items.new('view3d.view_roll', 'NUMPAD_4', 'PRESS', shift=True)
kmi_props_setattr(kmi.properties, 'type', 'ROLLLEFT')
kmi = km.keymap_items.new('view3d.view_roll', 'NUMPAD_6', 'PRESS', shift=True)
kmi_props_setattr(kmi.properties, 'type', 'ROLLTRIGHT')
kmi = km.keymap_items.new('view3d.view_pan', 'WHEELUPMOUSE', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'type', 'PANRIGHT')
kmi = km.keymap_items.new('view3d.view_pan', 'WHEELDOWNMOUSE', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'type', 'PANLEFT')
kmi = km.keymap_items.new('view3d.view_pan', 'WHEELUPMOUSE', 'PRESS', shift=True)
kmi_props_setattr(kmi.properties, 'type', 'PANUP')
kmi = km.keymap_items.new('view3d.view_pan', 'WHEELDOWNMOUSE', 'PRESS', shift=True)
kmi_props_setattr(kmi.properties, 'type', 'PANDOWN')
kmi = km.keymap_items.new('view3d.view_orbit', 'WHEELUPMOUSE', 'PRESS', ctrl=True, alt=True)
kmi_props_setattr(kmi.properties, 'type', 'ORBITLEFT')
kmi = km.keymap_items.new('view3d.view_orbit', 'WHEELDOWNMOUSE', 'PRESS', ctrl=True, alt=True)
kmi_props_setattr(kmi.properties, 'type', 'ORBITRIGHT')
kmi = km.keymap_items.new('view3d.view_orbit', 'WHEELUPMOUSE', 'PRESS', shift=True, alt=True)
kmi_props_setattr(kmi.properties, 'type', 'ORBITUP')
kmi = km.keymap_items.new('view3d.view_orbit', 'WHEELDOWNMOUSE', 'PRESS', shift=True, alt=True)
kmi_props_setattr(kmi.properties, 'type', 'ORBITDOWN')
kmi = km.keymap_items.new('view3d.view_roll', 'WHEELUPMOUSE', 'PRESS', shift=True, ctrl=True)
kmi_props_setattr(kmi.properties, 'type', 'ROLLLEFT')
kmi = km.keymap_items.new('view3d.view_roll', 'WHEELDOWNMOUSE', 'PRESS', shift=True, ctrl=True)
kmi_props_setattr(kmi.properties, 'type', 'ROLLTRIGHT')
kmi = km.keymap_items.new('view3d.viewnumpad', 'NUMPAD_1', 'PRESS', shift=True)
kmi_props_setattr(kmi.properties, 'type', 'FRONT')
kmi_props_setattr(kmi.properties, 'align_active', True)
kmi = km.keymap_items.new('view3d.viewnumpad', 'NUMPAD_3', 'PRESS', shift=True)
kmi_props_setattr(kmi.properties, 'type', 'RIGHT')
kmi_props_setattr(kmi.properties, 'align_active', True)
kmi = km.keymap_items.new('view3d.viewnumpad', 'NUMPAD_7', 'PRESS', shift=True)
kmi_props_setattr(kmi.properties, 'type', 'TOP')
kmi_props_setattr(kmi.properties, 'align_active', True)
kmi = km.keymap_items.new('view3d.viewnumpad', 'NUMPAD_1', 'PRESS', shift=True, ctrl=True)
kmi_props_setattr(kmi.properties, 'type', 'BACK')
kmi_props_setattr(kmi.properties, 'align_active', True)
kmi = km.keymap_items.new('view3d.viewnumpad', 'NUMPAD_3', 'PRESS', shift=True, ctrl=True)
kmi_props_setattr(kmi.properties, 'type', 'LEFT')
kmi_props_setattr(kmi.properties, 'align_active', True)
kmi = km.keymap_items.new('view3d.viewnumpad', 'NUMPAD_7', 'PRESS', shift=True, ctrl=True)
kmi_props_setattr(kmi.properties, 'type', 'BOTTOM')
kmi_props_setattr(kmi.properties, 'align_active', True)
kmi = km.keymap_items.new('view3d.localview', 'NUMPAD_SLASH', 'PRESS')
kmi = km.keymap_items.new('view3d.ndof_orbit_zoom', 'NDOF_MOTION', 'ANY')
kmi = km.keymap_items.new('view3d.ndof_orbit', 'NDOF_MOTION', 'ANY', ctrl=True)
kmi = km.keymap_items.new('view3d.ndof_pan', 'NDOF_MOTION', 'ANY', shift=True)
kmi = km.keymap_items.new('view3d.ndof_all', 'NDOF_MOTION', 'ANY', shift=True, ctrl=True)
kmi = km.keymap_items.new('view3d.view_selected', 'NDOF_BUTTON_FIT', 'PRESS')
kmi_props_setattr(kmi.properties, 'use_all_regions', False)
kmi = km.keymap_items.new('view3d.view_roll', 'NDOF_BUTTON_ROLL_CCW', 'PRESS')
kmi_props_setattr(kmi.properties, 'angle', -1.5707963705062866)
kmi = km.keymap_items.new('view3d.view_roll', 'NDOF_BUTTON_ROLL_CW', 'PRESS')
kmi_props_setattr(kmi.properties, 'angle', 1.5707963705062866)
kmi = km.keymap_items.new('view3d.viewnumpad', 'NDOF_BUTTON_FRONT', 'PRESS')
kmi_props_setattr(kmi.properties, 'type', 'FRONT')
kmi = km.keymap_items.new('view3d.viewnumpad', 'NDOF_BUTTON_BACK', 'PRESS')
kmi_props_setattr(kmi.properties, 'type', 'BACK')
kmi = km.keymap_items.new('view3d.viewnumpad', 'NDOF_BUTTON_LEFT', 'PRESS')
kmi_props_setattr(kmi.properties, 'type', 'LEFT')
kmi = km.keymap_items.new('view3d.viewnumpad', 'NDOF_BUTTON_RIGHT', 'PRESS')
kmi_props_setattr(kmi.properties, 'type', 'RIGHT')
kmi = km.keymap_items.new('view3d.viewnumpad', 'NDOF_BUTTON_TOP', 'PRESS')
kmi_props_setattr(kmi.properties, 'type', 'TOP')
kmi = km.keymap_items.new('view3d.viewnumpad', 'NDOF_BUTTON_BOTTOM', 'PRESS')
kmi_props_setattr(kmi.properties, 'type', 'BOTTOM')
kmi = km.keymap_items.new('view3d.viewnumpad', 'NDOF_BUTTON_FRONT', 'PRESS', shift=True)
kmi_props_setattr(kmi.properties, 'type', 'FRONT')
kmi_props_setattr(kmi.properties, 'align_active', True)
kmi = km.keymap_items.new('view3d.viewnumpad', 'NDOF_BUTTON_RIGHT', 'PRESS', shift=True)
kmi_props_setattr(kmi.properties, 'type', 'RIGHT')
kmi_props_setattr(kmi.properties, 'align_active', True)
kmi = km.keymap_items.new('view3d.viewnumpad', 'NDOF_BUTTON_TOP', 'PRESS', shift=True)
kmi_props_setattr(kmi.properties, 'type', 'TOP')
kmi_props_setattr(kmi.properties, 'align_active', True)
kmi = km.keymap_items.new('view3d.select_or_deselect_all', 'SELECTMOUSE', 'PRESS')
kmi_props_setattr(kmi.properties, 'extend', False)
kmi_props_setattr(kmi.properties, 'toggle', False)
kmi_props_setattr(kmi.properties, 'deselect', False)
kmi_props_setattr(kmi.properties, 'center', False)
kmi_props_setattr(kmi.properties, 'enumerate', False)
kmi_props_setattr(kmi.properties, 'object', False)
kmi = km.keymap_items.new('view3d.select_or_deselect_all', 'SELECTMOUSE', 'PRESS', shift=True)
kmi_props_setattr(kmi.properties, 'extend', False)
kmi_props_setattr(kmi.properties, 'toggle', True)
kmi_props_setattr(kmi.properties, 'deselect', False)
kmi_props_setattr(kmi.properties, 'center', False)
kmi_props_setattr(kmi.properties, 'enumerate', False)
kmi_props_setattr(kmi.properties, 'object', False)
kmi = km.keymap_items.new('view3d.select_or_deselect_all', 'SELECTMOUSE', 'PRESS', ctrl=True)
kmi_props_setattr(kmi.properties, 'extend', False)
kmi_props_setattr(kmi.properties, 'toggle', False)
kmi_props_setattr(kmi.properties, 'deselect', True)
kmi_props_setattr(kmi.properties, 'center', False)
kmi_props_setattr(kmi.properties, 'enumerate', False)
kmi_props_setattr(kmi.properties, 'object', False)
kmi = km.keymap_items.new('view3d.select_or_deselect_all', 'SELECTMOUSE', 'PRESS', alt=True)
kmi_props_setattr(kmi.properties, 'extend', False)
kmi_props_setattr(kmi.properties, 'toggle', False)
kmi_props_setattr(kmi.properties, 'deselect', False)
kmi_props_setattr(kmi.properties, 'center', False)
kmi_props_setattr(kmi.properties, 'enumerate', True)
kmi_props_setattr(kmi.properties, 'object', False)
kmi = km.keymap_items.new('view3d.select_border', 'EVT_TWEAK_S', 'ANY')
kmi_props_setattr(kmi.properties, 'extend', False)
kmi = km.keymap_items.new('view3d.select_border', 'EVT_TWEAK_S', 'ANY', shift=True)
kmi = km.keymap_items.new('view3d.select_border', 'EVT_TWEAK_S', 'ANY', ctrl=True)
kmi_props_setattr(kmi.properties, 'extend', False)
kmi = km.keymap_items.new('view3d.view_center_pick', 'MIDDLEMOUSE', 'PRESS', alt=True)
kmi = km.keymap_items.new('transform.translate', 'D', 'CLICK')
kmi = km.keymap_items.new('transform.resize', 'S', 'CLICK')
kmi = km.keymap_items.new('transform.rotate', 'A', 'CLICK')
kmi = km.keymap_items.new('wm.context_toggle_enum', 'Z', 'CLICK')
kmi_props_setattr(kmi.properties, 'data_path', 'space_data.viewport_shade')
kmi_props_setattr(kmi.properties, 'value_1', 'SOLID')
kmi_props_setattr(kmi.properties, 'value_2', 'WIREFRAME')
kmi.active = False
kmi = km.keymap_items.new('wm.context_toggle', 'Z', 'CLICK')
kmi_props_setattr(kmi.properties, 'data_path', 'space_data.use_occlude_geometry')

# Map Transform Modal Map
km = kc.keymaps.new('Transform Modal Map', space_type='EMPTY', region_type='WINDOW', modal=True)

kmi = km.keymap_items.new_modal('CANCEL', 'ESC', 'PRESS', any=True)
kmi = km.keymap_items.new_modal('CONFIRM', 'LEFTMOUSE', 'PRESS', any=True)
kmi = km.keymap_items.new_modal('CONFIRM', 'RET', 'PRESS', any=True)
kmi = km.keymap_items.new_modal('CONFIRM', 'NUMPAD_ENTER', 'PRESS', any=True)
kmi = km.keymap_items.new_modal('TRANSLATE', 'G', 'PRESS')
kmi = km.keymap_items.new_modal('ROTATE', 'R', 'PRESS')
kmi = km.keymap_items.new_modal('RESIZE', 'S', 'CLICK')
kmi = km.keymap_items.new_modal('SNAP_TOGGLE', 'TAB', 'PRESS', shift=True)
kmi = km.keymap_items.new_modal('SNAP_INV_ON', 'LEFT_CTRL', 'PRESS', any=True)
kmi = km.keymap_items.new_modal('SNAP_INV_OFF', 'LEFT_CTRL', 'RELEASE', any=True)
kmi = km.keymap_items.new_modal('SNAP_INV_ON', 'RIGHT_CTRL', 'PRESS', any=True)
kmi = km.keymap_items.new_modal('SNAP_INV_OFF', 'RIGHT_CTRL', 'RELEASE', any=True)
kmi = km.keymap_items.new_modal('ADD_SNAP', 'A', 'PRESS')
kmi = km.keymap_items.new_modal('REMOVE_SNAP', 'A', 'PRESS', alt=True)
kmi = km.keymap_items.new_modal('PROPORTIONAL_SIZE_UP', 'PAGE_UP', 'PRESS')
kmi = km.keymap_items.new_modal('PROPORTIONAL_SIZE_DOWN', 'PAGE_DOWN', 'PRESS')
kmi = km.keymap_items.new_modal('PROPORTIONAL_SIZE_UP', 'PAGE_UP', 'PRESS', shift=True)
kmi = km.keymap_items.new_modal('PROPORTIONAL_SIZE_DOWN', 'PAGE_DOWN', 'PRESS', shift=True)
kmi = km.keymap_items.new_modal('PROPORTIONAL_SIZE_UP', 'WHEELDOWNMOUSE', 'PRESS')
kmi = km.keymap_items.new_modal('PROPORTIONAL_SIZE_DOWN', 'WHEELUPMOUSE', 'PRESS')
kmi = km.keymap_items.new_modal('PROPORTIONAL_SIZE_UP', 'WHEELDOWNMOUSE', 'PRESS', shift=True)
kmi = km.keymap_items.new_modal('PROPORTIONAL_SIZE_DOWN', 'WHEELUPMOUSE', 'PRESS', shift=True)
kmi = km.keymap_items.new_modal('PROPORTIONAL_SIZE', 'TRACKPADPAN', 'ANY')
kmi = km.keymap_items.new_modal('EDGESLIDE_EDGE_NEXT', 'WHEELDOWNMOUSE', 'PRESS', alt=True)
kmi = km.keymap_items.new_modal('EDGESLIDE_PREV_NEXT', 'WHEELUPMOUSE', 'PRESS', alt=True)
kmi = km.keymap_items.new_modal('AUTOIK_CHAIN_LEN_UP', 'PAGE_UP', 'PRESS', shift=True)
kmi = km.keymap_items.new_modal('AUTOIK_CHAIN_LEN_DOWN', 'PAGE_DOWN', 'PRESS', shift=True)
kmi = km.keymap_items.new_modal('AUTOIK_CHAIN_LEN_UP', 'WHEELDOWNMOUSE', 'PRESS', shift=True)
kmi = km.keymap_items.new_modal('AUTOIK_CHAIN_LEN_DOWN', 'WHEELUPMOUSE', 'PRESS', shift=True)

# Map Gesture Border
km = kc.keymaps.new('Gesture Border', space_type='EMPTY', region_type='WINDOW', modal=True)

kmi = km.keymap_items.new_modal('CANCEL', 'ESC', 'PRESS', any=True)
kmi = km.keymap_items.new_modal('BEGIN', 'LEFTMOUSE', 'PRESS')
kmi = km.keymap_items.new_modal('SELECT', 'LEFTMOUSE', 'RELEASE')
kmi = km.keymap_items.new_modal('SELECT', 'LEFTMOUSE', 'RELEASE', shift=True)
kmi = km.keymap_items.new_modal('DESELECT', 'LEFTMOUSE', 'RELEASE', ctrl=True)
