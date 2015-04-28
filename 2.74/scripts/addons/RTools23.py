bl_info = {
    'name': "RTools",
    'author': "PLyczkowski",
    'version': (1, 0, 0),
    'blender': (2, 6, 0),
    'api': 41270,
    'location': "View3D > Toolbar",
    'warning': "",
    'description': "Tools to aid modelling.",
    'wiki_url': "",
    'tracker_url': "",
    'category': 'Mesh'}

import bpy,bmesh

# OPERATOR RCURSOR_TO_X

class rcursor_to_x(bpy.types.Operator):
    bl_idname = "object.rcursor_to_x"
    bl_label = "Cursor to X"
    bl_description = "Snap cursor to X Axis."
    bl_register = True
    bl_undo = True

    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        
        bpy.context.space_data.cursor_location[0] = 0
        
        return {'FINISHED'}

# OPERATOR ADD MIRRORPLANE

def raddmirrorplane_context(context):
    
    bpy.ops.view3d.layers(nr=1)
    
    bpy.ops.mesh.primitive_plane_add(view_align=False, enter_editmode=False, location=(0, 0, 0), rotation=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    
    bpy.ops.object.editmode_toggle()
    
    bpy.ops.transform.translate(value=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, snap=False, snap_target='CLOSEST', snap_point=(0, 0, 0), snap_align=False, snap_normal=(0, 0, 0), texture_space=False, release_confirm=True)
    
    bpy.ops.transform.translate(value=(0, 0, 2), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, snap=False, snap_target='CLOSEST', snap_point=(0, 0, 0), snap_align=False, snap_normal=(0, 0, 0), texture_space=False, release_confirm=True)
    
    bpy.ops.object.editmode_toggle()
    
    bpy.ops.object.modifier_add(type='MIRROR')
    
    bpy.ops.object.shade_smooth()


class RAddMirrorPlane(bpy.types.Operator):
    '''Tooltip'''
    bl_description = "Adds a plane with mirror modifier to the scene."
    bl_idname = "object.raddmirrorplane"
    bl_label = "RAddMirrorPlane"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        raddmirrorplane_context(context)
        return {'FINISHED'}
    
# OPERATOR SETUP MIRROR RETOPO

def rsetup_mirror_retopo_context(context):
    
    bpy.ops.view3d.layers(nr=1)
    
    bpy.ops.mesh.primitive_plane_add(view_align=False, enter_editmode=False, location=(0, 0, 0), rotation=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    
    bpy.context.object.show_x_ray = True
    
    bpy.ops.object.editmode_toggle()
    
    bpy.ops.transform.translate(value=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, snap=False, snap_target='CLOSEST', snap_point=(0, 0, 0), snap_align=False, snap_normal=(0, 0, 0), texture_space=False, release_confirm=True)
    
    bpy.ops.transform.translate(value=(0, 0, 2), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, snap=False, snap_target='CLOSEST', snap_point=(0, 0, 0), snap_align=False, snap_normal=(0, 0, 0), texture_space=False, release_confirm=True)
    
    bpy.ops.object.editmode_toggle()
    
    bpy.ops.object.modifier_add(type='MIRROR')
    
    bpy.ops.object.shade_smooth()
    
    
    bpy.context.scene.tool_settings.use_snap = True
    bpy.context.scene.tool_settings.snap_element = 'FACE'
    bpy.context.scene.tool_settings.use_snap_project = True
    
    

class RSetupMirrorRetopo(bpy.types.Operator):
    '''Tooltip'''
    bl_description = "Adds a mirror plane, and turns on retopo related settings."
    bl_idname = "object.rsetup_mirror_retopo"
    bl_label = "RSetupMirrorRetopo"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        rsetup_mirror_retopo_context(context)
        return {'FINISHED'}
    
#SETUP RETOPO

def rsetup_retopo_context(context):
    
    bpy.context.scene.tool_settings.use_snap = True
    bpy.context.scene.tool_settings.snap_element = 'FACE'
    bpy.context.scene.tool_settings.use_snap_project = True

class RSetupRetopo(bpy.types.Operator):
    '''Tooltip'''
    bl_description = "Turn on retopo related settings."
    bl_idname = "object.rsetup_retopo"
    bl_label = "RSetupRetopo"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        rsetup_retopo_context(context)
        return {'FINISHED'}

#DISABLE RETOPO

def rdisable_retopo_context(context):
    
    bpy.context.scene.tool_settings.use_snap = False

class RDisableRetopo(bpy.types.Operator):
    '''Tooltip'''
    bl_description = "Turn off retopo related settings."
    bl_idname = "object.rdisable_retopo"
    bl_label = "RDisableRetopo"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        rdisable_retopo_context(context)
        return {'FINISHED'}
    
#APPLY MODIFIERS by Oscurart
    
class oscApplyModifiers (bpy.types.Operator):
    bl_idname = "object.modifiers_apply_osc"
    bl_label = "Apply modifiers" 
    bl_options =  {"REGISTER","UNDO"}
    def execute(self,context):
        for objeto in bpy.context.selected_objects:
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.scene.objects.active=objeto
            objeto.select=True            
            bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=True, obdata=True, material=False, texture=False, animation=False)
            for modificador in objeto.modifiers:
                print(modificador.type)
                # SUBSURF
                if modificador.type == 'SUBSURF':
                    if modificador.levels > 0:
                        bpy.ops.object.modifier_apply(apply_as="DATA",modifier=modificador.name)
                    else:
                        bpy.ops.object.modifier_remove(modifier=modificador.name)          
                # MESH DEFORM
                if modificador.type == 'MESH_DEFORM':
                    if modificador.object != None:
                        bpy.ops.object.modifier_apply(apply_as="DATA",modifier=modificador.name)
                    else:
                        bpy.ops.object.modifier_remove(modifier=modificador.name)      
                # ARRAY 
                if modificador.type == 'ARRAY':
                    bpy.ops.object.modifier_apply(apply_as="DATA",modifier=modificador.name)
                # BEVEL 
                if modificador.type == 'BEVEL':
                    bpy.ops.object.modifier_apply(apply_as="DATA",modifier=modificador.name) 
                # BOOLEAN
                if modificador.type == 'BOOLEAN':
                    if modificador.object != None:
                        bpy.ops.object.modifier_apply(apply_as="DATA",modifier=modificador.name)
                    else:
                        bpy.ops.object.modifier_remove(modifier=modificador.name)                      
                # BUILD
                if modificador.type == 'BUILD':
                    bpy.ops.object.modifier_apply(apply_as="DATA",modifier=modificador.name)            
                # DECIMATE
                if modificador.type == 'DECIMATE':
                    bpy.ops.object.modifier_apply(apply_as="DATA",modifier=modificador.name) 
                # EDGE SPLIT
                if modificador.type == 'EDGE_SPLIT':
                    bpy.ops.object.modifier_apply(apply_as="DATA",modifier=modificador.name)             
                # MASK
                if modificador.type == 'MASK':
                    bpy.ops.object.modifier_apply(apply_as="DATA",modifier=modificador.name)              
                # MIRROR
                if modificador.type == 'MIRROR':
                    bpy.ops.object.modifier_apply(apply_as="DATA",modifier=modificador.name) 
                # MULTIRESOLUTION
                if modificador.type == 'MULTIRES':
                    bpy.ops.object.modifier_apply(apply_as="DATA",modifier=modificador.name)
                # SCREW
                if modificador.type == 'SCREW':
                    bpy.ops.object.modifier_apply(apply_as="DATA",modifier=modificador.name)
                # SOLIDIFY
                if modificador.type == 'SOLIDIFY':
                    bpy.ops.object.modifier_apply(apply_as="DATA",modifier=modificador.name)     
                # UV_PROJECT
                if modificador.type == 'UV_PROJECT':
                    bpy.ops.object.modifier_apply(apply_as="DATA",modifier=modificador.name)              
                # ARMATURE
                if modificador.type == 'ARMATURE':
                    if modificador.object != None:
                        bpy.ops.object.modifier_apply(apply_as="DATA",modifier=modificador.name)
                    else:
                        bpy.ops.object.modifier_remove(modifier=modificador.name) 
                # CAST
                if modificador.type == 'CAST':
                    bpy.ops.object.modifier_apply(apply_as="DATA",modifier=modificador.name) 
                # CURVE
                if modificador.type == 'CURVE':
                    if modificador.object != None:
                        bpy.ops.object.modifier_apply(apply_as="DATA",modifier=modificador.name)
                    else:
                        bpy.ops.object.modifier_remove(modifier=modificador.name)                              
                # DISPLACE
                if modificador.type == 'DISPLACE':
                    if modificador.texture != None:
                        bpy.ops.object.modifier_apply(apply_as="DATA",modifier=modificador.name)
                    else:
                        bpy.ops.object.modifier_remove(modifier=modificador.name)                  
                # HOOK
                if modificador.type == 'HOOK':
                    if modificador.object != None:
                        bpy.ops.object.modifier_apply(apply_as="DATA",modifier=modificador.name)
                    else:
                        bpy.ops.object.modifier_remove(modifier=modificador.name)                   
                # LATTICE
                if modificador.type == 'LATTICE':
                    if modificador.object != None:
                        bpy.ops.object.modifier_apply(apply_as="DATA",modifier=modificador.name)
                    else:
                        bpy.ops.object.modifier_remove(modifier=modificador.name)                
                # SHRINK WRAP
                if modificador.type == 'SHRINKWRAP':
                    if modificador.target != None:
                        bpy.ops.object.modifier_apply(apply_as="DATA",modifier=modificador.name)
                    else:
                        bpy.ops.object.modifier_remove(modifier=modificador.name)                  
                # SIMPLE DEFORM
                if modificador.type == 'SIMPLE_DEFORM':
                    bpy.ops.object.modifier_apply(apply_as="DATA",modifier=modificador.name)                
                # SMOOTH
                if modificador.type == 'SMOOTH':
                    bpy.ops.object.modifier_apply(apply_as="DATA",modifier=modificador.name)                  
                # WARP
                if modificador.type == 'WARP':
                    if modificador.object_from != None:
                        if modificador.object_to != None:
                            bpy.ops.object.modifier_apply(apply_as="DATA",modifier=modificador.name)
                    else:
                        bpy.ops.object.modifier_remove(modifier=modificador.name)                 
                # WAVE
                if modificador.type == 'WAVE':
                    bpy.ops.object.modifier_apply(apply_as="DATA",modifier=modificador.name) 
        return{"FINISHED"}

# OPERATOR MIRRORX OBJECT

def mirrorx_object_content(context):
    
    storePivot = context.space_data.pivot_point
    storeObject = bpy.context.active_object
    
    storeCursorX = context.space_data.cursor_location.x
    storeCursorY = context.space_data.cursor_location.y
    storeCursorZ = context.space_data.cursor_location.z
    
    newObjectOriginX = -bpy.context.active_object.location[0]
    newObjectOriginY = bpy.context.active_object.location[1]
    newObjectOriginZ = bpy.context.active_object.location[2]
    
    bpy.ops.object.editmode_toggle()
    
    bpy.ops.view3d.snap_cursor_to_center()
    
    context.space_data.pivot_point = 'CURSOR'
    
    bpy.ops.mesh.select_all(action='SELECT')
    
    bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode": 1}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "texture_space":False, "release_confirm":False})
    
    bpy.ops.transform.mirror(constraint_axis=(True, False, False), constraint_orientation='GLOBAL', proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, release_confirm=False)
    
    bpy.ops.mesh.select_all(action='INVERT')
    
    bpy.ops.mesh.separate(type='SELECTED')
    
    bpy.ops.object.editmode_toggle()
    
    context.space_data.cursor_location.x = newObjectOriginX
    context.space_data.cursor_location.y = newObjectOriginY
    context.space_data.cursor_location.z = newObjectOriginZ
    
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    
    context.space_data.pivot_point = storePivot
    
    context.space_data.cursor_location.x = storeCursorX
    context.space_data.cursor_location.y = storeCursorY
    context.space_data.cursor_location.z = storeCursorZ
    
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    
#    storeObject.select = True
#    bpy.context.scene.objects.active = storeObject

class RMirrorX_Object(bpy.types.Operator):
    '''Tooltip'''
    bl_description = "Mirrors the selected object along the x axis."
    bl_idname = "object.rmirrorx_object"
    bl_label = "RMirror X"

    @classmethod
    def poll(cls, context):
        if  bpy.context.active_object is not None and bpy.context.active_object.type == 'MESH':
            return True
        else:
            return False

    def execute(self, context):
        mirrorx_object_content(context)
        return {'FINISHED'}


# OPERATOR MIRRORX

def mirrorx_content(context):
    
    storePivot = context.space_data.pivot_point
    
    storeCursorX = context.space_data.cursor_location.x
    storeCursorY = context.space_data.cursor_location.y
    storeCursorZ = context.space_data.cursor_location.z
    
    bpy.ops.view3d.snap_cursor_to_center()
    
    context.space_data.pivot_point = 'CURSOR'
    
    bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode":1}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "texture_space":False, "release_confirm":False})
    
    bpy.ops.transform.mirror(constraint_axis=(True, False, False), constraint_orientation='GLOBAL', proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, release_confirm=False)
    
    bpy.ops.mesh.flip_normals()
    
    context.space_data.pivot_point = storePivot
    
    context.space_data.cursor_location.x = storeCursorX
    context.space_data.cursor_location.y = storeCursorY
    context.space_data.cursor_location.z = storeCursorZ

class RMirrorX(bpy.types.Operator):
    '''Tooltip'''
    bl_description = "Mirrors the selected geometry along the x axis."
    bl_idname = "object.rmirrorx"
    bl_label = "RMirror X"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        mirrorx_content(context)
        return {'FINISHED'}

# OPERATOR TOX

def tox_content(context):
    
    storePivot = context.space_data.pivot_point
    
    storeCursorX = context.space_data.cursor_location.x
    storeCursorY = context.space_data.cursor_location.y
    storeCursorZ = context.space_data.cursor_location.z
    
    bpy.ops.view3d.snap_cursor_to_center()
    
    context.space_data.pivot_point = 'CURSOR'
    
    bpy.ops.transform.resize(value=(0, 1, 1), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, snap=False, snap_target='CLOSEST', snap_point=(0, 0, 0), snap_align=False, snap_normal=(0, 0, 0), texture_space=False, release_confirm=False)
    
    context.space_data.pivot_point = storePivot
    
    context.space_data.cursor_location.x = storeCursorX
    context.space_data.cursor_location.y = storeCursorY
    context.space_data.cursor_location.z = storeCursorZ

class RToX(bpy.types.Operator):
    '''Tooltip'''
    bl_description = "Sets the x position of the selected vertices to 0."
    bl_idname = "object.rtox"
    bl_label = "RTo X"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        tox_content(context)
        return {'FINISHED'}
    
# OPERATOR UNIFYSHADING

def unifyshading_content(context):
    
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.mesh.faces_shade_smooth()
    bpy.ops.mesh.select_all(action='DESELECT')

class RUnifyShading(bpy.types.Operator):
    '''Tooltip'''
    bl_description = "Recalculates normals and sets shading type to smooth on the whole mesh."
    bl_idname = "object.runifyshading"
    bl_label = "Unify Shading"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        unifyshading_content(context)
        return {'FINISHED'}

# OPERATOR REXPLODE

def rexplode_content(context):
    
    selected = context.selected_objects
    obj = context.active_object
    objects = bpy.data.objects

    bpy.ops.object.select_all(action='DESELECT')
    context.active_object.select = True

    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.editmode_toggle()
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

class RExplode(bpy.types.Operator):
    '''Tooltip'''
    bl_description = "Divides mesh by parts, sets origin at the center of each part."
    bl_idname = "object.rexplode"
    bl_label = "Explode Mesh"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        rexplode_content(context)
        return {'FINISHED'}
    
# OPERATOR RSETPIVOTBOUNDING

def rsetpivotbounding_content(context):
    
    context.space_data.pivot_point = 'BOUNDING_BOX_CENTER'

class Rsetpivotbounding(bpy.types.Operator):
    '''Tooltip'''
    bl_description = ""
    bl_idname = "object.rsetpivotbounding"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        rsetpivotbounding_content(context)
        return {'FINISHED'}
    
# OPERATOR RSETPIVOTCURSOR

def rsetpivotcursor_content(context):
    
    context.space_data.pivot_point = 'CURSOR'

class Rsetpivotcursor(bpy.types.Operator):
    '''Tooltip'''
    bl_description = ""
    bl_idname = "object.rsetpivotcursor"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        rsetpivotcursor_content(context)
        return {'FINISHED'}
    
# OPERATOR RSETPIVOTMEDIAN

def rsetpivotmedian_content(context):
    
    context.space_data.pivot_point = 'MEDIAN_POINT'

class Rsetpivotmedian(bpy.types.Operator):
    '''Tooltip'''
    bl_description = ""
    bl_idname = "object.rsetpivotmedian"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        rsetpivotmedian_content(context)
        return {'FINISHED'}
    
# OPERATOR RSETPIVOTACTIVE

def rsetpivotactive_content(context):
    
    context.space_data.pivot_point = 'ACTIVE_ELEMENT'

class Rsetpivotactive(bpy.types.Operator):
    '''Tooltip'''
    bl_description = ""
    bl_idname = "object.rsetpivotactive"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        rsetpivotactive_content(context)
        return {'FINISHED'}
    
# OPERATOR RSETPIVOTINDIVIDUAL

def rsetpivotindividual_content(context):
    
    context.space_data.pivot_point = 'INDIVIDUAL_ORIGINS'

class Rsetpivotindividual(bpy.types.Operator):
    '''Tooltip'''
    bl_description = ""
    bl_idname = "object.rsetpivotindividual"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        rsetpivotindividual_content(context)
        return {'FINISHED'}
    
# OPERATOR RSETSCULPTMODE

def rsetsculptmode_content(context):
    
    if context.active_object.type == 'MESH':
        bpy.ops.object.mode_set(mode='SCULPT', toggle=False)

class Rsetsculptmode(bpy.types.Operator):
    '''Tooltip'''
    bl_description = ""
    bl_idname = "object.rsetsculptmode"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        if  bpy.context.active_object is not None and bpy.context.active_object.type == 'MESH' and bpy.context.active_object.mode != 'SCULPT':
            return True
        else:
            return False

    def execute(self, context):
        rsetsculptmode_content(context)
        return {'FINISHED'}
    
# OPERATOR RSETOBJECTMODE

def rsetobjectmode_content(context):
    
    if context.active_object.type == 'MESH':
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

class Rsetobjectmode(bpy.types.Operator):
    '''Tooltip'''
    bl_description = ""
    bl_idname = "object.rsetobjectmode"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        if  bpy.context.active_object is not None and bpy.context.active_object.type == 'MESH' and bpy.context.active_object.mode != 'OBJECT':
            return True
        else:
            return False

    def execute(self, context):
        rsetobjectmode_content(context)
        return {'FINISHED'}
    
# OPERATOR RSETEDITMODE

def rseteditmode_content(context):
    
    if context.active_object.type == 'MESH':
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)

class Rseteditmode(bpy.types.Operator):
    '''Tooltip'''
    bl_description = ""
    bl_idname = "object.rseteditmode"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        if  bpy.context.active_object is not None and bpy.context.active_object.type == 'MESH' and bpy.context.active_object.mode != 'EDIT':
            return True
        else:
            return False

    def execute(self, context):
        rseteditmode_content(context)
        return {'FINISHED'}
    
# OPERATOR RSETTEXTUREMODE

def rsettexturemode_content(context):
    
    if context.active_object.type == 'MESH':
        bpy.ops.object.mode_set(mode='TEXTURE_PAINT', toggle=False)

class Rsettexturemode(bpy.types.Operator):
    '''Tooltip'''
    bl_description = ""
    bl_idname = "object.rsettexturemode"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        if  bpy.context.active_object is not None and bpy.context.active_object.type == 'MESH' and bpy.context.active_object.mode != 'TEXTURE_PAINT':
            return True
        else:
            return False

    def execute(self, context):
        rsettexturemode_content(context)
        return {'FINISHED'}

# OPERATOR CHECKTRICOUNT

def checkTricount_content(context):
    
    ob = bpy.context.active_object
    
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "texture_space":False, "release_confirm":False})
    
    bpy.ops.object.modifiers_apply_osc()
    
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    
    bpy.ops.mesh.select_all(action='SELECT')
    
    bpy.ops.mesh.quads_convert_to_tris(use_beauty=True)
    
    mesh = context.object.data
    
    bpy.types.Scene.rTriCount = bpy.props.IntProperty(name="RTriCount")
    
    bpy.data.scenes[0].rTriCount = mesh.total_face_sel
        
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    
    bpy.ops.object.delete(use_global=False)
    
    ob.select = True
    bpy.context.scene.objects.active = ob

class CheckTricount(bpy.types.Operator):
    '''Tooltip'''
    bl_description = "Check the tricount of the selected object"
    bl_idname = "object.checktricount"
    bl_label = "Check Tricount"

    @classmethod
    def poll(cls, context):
        if  bpy.context.active_object is not None and bpy.context.active_object.type == 'MESH':
            return True
        else:
            return False

    def execute(self, context):
        checkTricount_content(context)
        self.report({'INFO'}, "Tricount: %d" % (bpy.data.scenes[0].rTriCount))
        return {'FINISHED'}

# OPERATOR RSETORIENTATION

def rsetorientation_content(context):
         
     bpy.ops.transform.create_orientation(name="rOrientation", use=True, overwrite=True)
     space = context.space_data
     
     space.show_manipulator = True

class RSetOrientation(bpy.types.Operator):
    '''Tooltip'''
    bl_description = "Set custom manipulator orientation"
    bl_idname = "object.rsetorientation"
    bl_label = "RSetOrientation"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        rsetorientation_content(context)
        return {'FINISHED'}
    
# OPERATOR RFLATBOUNDARYSEAM

def rflatboundaryseam_content(context):
         
     bpy.ops.mesh.faces_select_linked_flat(sharpness=0.0174533)
     
     bpy.ops.mesh.region_to_loop()
     
     bpy.ops.mesh.mark_seam(clear=False)
     
     context.tool_settings.mesh_select_mode = (False, False, True)

class RFlatBoundarySeam(bpy.types.Operator):
    '''Tooltip'''
    bl_description = "Sets seams on the boundary of the flat faces surrounding the selection."
    bl_idname = "object.rflatboundaryseam"
    bl_label = "RFlatBoundarySeam"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        rflatboundaryseam_content(context)
        return {'FINISHED'}
    
# OPERATOR RBOUNDARYSEAM

def rboundaryseam_content(context):
     
     bpy.ops.mesh.region_to_loop()
     
     bpy.ops.mesh.mark_seam(clear=False)
     
     context.tool_settings.mesh_select_mode = (False, False, True)

class RBoundarySeam(bpy.types.Operator):
    '''Tooltip'''
    bl_description = "Sets seams on the boundary of the selection."
    bl_idname = "object.rboundaryseam"
    bl_label = "RBoundarySeam"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        rboundaryseam_content(context)
        return {'FINISHED'}
    
# OPERATOR RFLATBOUNDARYSHARP

def rflatboundarysharp_content(context):
         
     bpy.ops.mesh.faces_select_linked_flat(sharpness=0.0174533)
     
     bpy.ops.mesh.region_to_loop()
     
     bpy.ops.mesh.mark_sharp(clear=False)
     
     context.tool_settings.mesh_select_mode = (False, False, True)

class RFlatBoundarySharp(bpy.types.Operator):
    '''Tooltip'''
    bl_description = "Sets sharp edges on the boundary of the flat faces surrounding the selection."
    bl_idname = "object.rflatboundarysharp"
    bl_label = "RFlatBoundarySharp"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        rflatboundarysharp_content(context)
        return {'FINISHED'}
    
# OPERATOR RBOUNDARYSHARP

def rboundarysharp_content(context):
     
     bpy.ops.mesh.region_to_loop()
     
     bpy.ops.mesh.mark_sharp(clear=False)
     
     context.tool_settings.mesh_select_mode = (False, False, True)

class RBoundarySharp(bpy.types.Operator):
    '''Tooltip'''
    bl_description = "Sets sharp edges on the boundary of the selection."
    bl_idname = "object.rboundarysharp"
    bl_label = "RBoundarySharp"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        rboundarysharp_content(context)
        return {'FINISHED'}
    
# OPERATOR RTOGGLELOCALEDTI

def rtogglelocaledit_content(context):
    
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    
    bpy.ops.view3d.localview()
    
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    

class RToggleLocalEdit(bpy.types.Operator):
    '''Tooltip'''
    bl_description = "View Global/Local"
    bl_idname = "object.rtogglelocaledit"
    bl_label = "RToggleLocalEdit"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        rtogglelocaledit_content(context)
        return {'FINISHED'}
    
# OPERATOR RORIGINTOSELECTION

def rorigintoselection_content(context):
    
    bpy.ops.object.editmode_toggle()
    
    storeCursorX = context.space_data.cursor_location.x
    storeCursorY = context.space_data.cursor_location.y
    storeCursorZ = context.space_data.cursor_location.z
    
    bpy.ops.object.editmode_toggle()
    
    bpy.ops.view3d.snap_cursor_to_selected()
    
    bpy.ops.object.editmode_toggle()
    
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    
    context.space_data.cursor_location.x = storeCursorX
    context.space_data.cursor_location.y = storeCursorY
    context.space_data.cursor_location.z = storeCursorZ
    
    bpy.ops.object.editmode_toggle()

class ROriginToSelection(bpy.types.Operator):
    '''Tooltip'''
    bl_description = "Ser Origin to selection."
    bl_idname = "object.rorigintoselection"
    bl_label = "ROriginToSelection"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        rorigintoselection_content(context)
        return {'FINISHED'}

# OPERATOR TEST

def test_content(context):
     
    print('test')
    
    
    
    print('test end')

#    storePivot = context.space_data.pivot_point
#    storeObject = bpy.context.active_object
#    
#    storeCursorX = context.space_data.cursor_location.x
#    storeCursorY = context.space_data.cursor_location.y
#    storeCursorZ = context.space_data.cursor_location.z
#    
#    newObjectOriginX = -bpy.context.active_object.location[0]
#    newObjectOriginY = bpy.context.active_object.location[1]
#    newObjectOriginZ = bpy.context.active_object.location[2]
#    
#    bpy.ops.object.editmode_toggle()
#    
#    bpy.ops.view3d.snap_cursor_to_center()
#    
#    context.space_data.pivot_point = 'CURSOR'
#    
#    bpy.ops.mesh.select_all(action='SELECT')
#    
#    bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode": 1}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "texture_space":False, "release_confirm":False})
#    
#    bpy.ops.transform.mirror(constraint_axis=(True, False, False), constraint_orientation='GLOBAL', proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, release_confirm=False)
#    
#    bpy.ops.mesh.select_all(action='INVERT')
#    
#    bpy.ops.mesh.separate(type='SELECTED')
#    
#    bpy.ops.object.editmode_toggle()
#    
#    context.space_data.cursor_location.x = newObjectOriginX
#    context.space_data.cursor_location.y = newObjectOriginY
#    context.space_data.cursor_location.z = newObjectOriginZ
#    
#    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
#    
#    context.space_data.pivot_point = storePivot
#    
#    context.space_data.cursor_location.x = storeCursorX
#    context.space_data.cursor_location.y = storeCursorY
#    context.space_data.cursor_location.z = storeCursorZ
    

class Test(bpy.types.Operator):
    '''Tooltip'''
    bl_description = "Test"
    bl_idname = "object.test"
    bl_label = "Test"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        test_content(context)
        return {'FINISHED'}
    
# BUTTONS

class addButtonsInObjectMode(bpy.types.Panel):
    bl_idname = "rtools_objectmode"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Tools"

    bl_label = "RTools"
    bl_context = "objectmode"
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        subrow = row.row()
        subrow.scale_x = 1.15
        subrow.scale_y = 1.15
#        subrow.operator("object.rsetobjectmode",text="",icon="OBJECT_DATAMODE")
#        subrow.operator("object.rseteditmode",text="",icon="EDITMODE_HLT")
#        subrow.operator("object.rsetsculptmode",text="",icon="SCULPTMODE_HLT")
#        subrow.operator("object.rsettexturemode",text="",icon="TPAINT_HLT")
        subrow.operator("object.rsetpivotcursor",text="",icon="CURSOR")
        subrow.operator("object.rsetpivotmedian",text="",icon="ROTATECENTER")
        subrow.operator("object.rsetpivotactive",text="",icon="ROTACTIVE")
        subrow.operator("object.rsetpivotindividual",text="",icon="ROTATECOLLECTION")
        
        row = layout.row()
        subrow = row.row()
        subrow.scale_x = 1.15
        subrow.scale_y = 1.15
        subrow.operator("view3d.viewnumpad",text="",icon="TRIA_DOWN").type='TOP'
        subrow.operator("view3d.viewnumpad",text="",icon="TRIA_RIGHT").type='LEFT'
        subrow.operator("view3d.viewnumpad",text="",icon="TRIA_LEFT").type='RIGHT'
        subrow.operator("view3d.viewnumpad",text="",icon="TRIA_UP").type='FRONT'
        subrow.operator("view3d.localview",text="",icon="RESTRICT_VIEW_OFF")
        
        row = layout.row()
        subrow = row.row()
        subrow.scale_x = 1.15
        subrow.scale_y = 1.15
        subrow.operator("mesh.primitive_cube_add",text="",icon="MESH_CUBE")
        subrow.operator("mesh.primitive_plane_add",text="",icon="MESH_PLANE")
        subrow.operator("mesh.primitive_uv_sphere_add",text="",icon="MESH_UVSPHERE")
        
        col = layout.column(align=True)
        
        col.operator("object.raddmirrorplane", text="Add Mirrored Plane")
        col.operator("object.rmirrorx_object", text="Mirror Along X")
        col.operator("object.rcursor_to_x", text="Cursor to X")

        col = layout.column(align=True)
        
        col.operator("object.rexplode", text="Explode Mesh")
        
        # col = layout.column(align=True)
        
        # col.operator("object.checktricount", text="Check Tricount")
        
        col = layout.column(align=True)
        
        col.operator("object.rsetup_mirror_retopo", text="Setup Mirrored Plane Retopo")
        col.operator("object.rsetup_retopo", text="Setup Retopo")
        col.operator("object.rdisable_retopo", text="Disable Retopo")
        
        col = layout.column(align=True)
        
        col.operator("object.test", text="Test")
        
class addButtonsInEditMode(bpy.types.Panel):
    bl_idname = "rtools_editmode"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Tools"

    bl_label = "RTools"
    bl_context = "mesh_edit"
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        subrow = row.row()
        subrow.scale_x = 1.15
        subrow.scale_y = 1.15
#        subrow.operator("object.rsetobjectmode",text="",icon="OBJECT_DATAMODE")
#        subrow.operator("object.rseteditmode",text="",icon="EDITMODE_HLT")
#        subrow.operator("object.rsetsculptmode",text="",icon="SCULPTMODE_HLT")
#        subrow.operator("object.rsettexturemode",text="",icon="TPAINT_HLT")
        subrow.operator("object.rsetpivotcursor",text="",icon="CURSOR")
        subrow.operator("object.rsetpivotmedian",text="",icon="ROTATECENTER")
        subrow.operator("object.rsetpivotactive",text="",icon="ROTACTIVE")
        subrow.operator("object.rsetpivotindividual",text="",icon="ROTATECOLLECTION")
        
        row = layout.row()
        subrow = row.row()
        subrow.scale_x = 1.15
        subrow.scale_y = 1.15
        subrow.operator("view3d.viewnumpad",text="",icon="TRIA_DOWN").type='TOP'
        subrow.operator("view3d.viewnumpad",text="",icon="TRIA_RIGHT").type='LEFT'
        subrow.operator("view3d.viewnumpad",text="",icon="TRIA_LEFT").type='RIGHT'
        subrow.operator("view3d.viewnumpad",text="",icon="TRIA_UP").type='FRONT'
        subrow.operator("object.rtogglelocaledit", text="", icon="RESTRICT_VIEW_OFF")
        
        col = layout.column(align=True)
        col.operator("object.rorigintoselection", text="Origin To Selection")
        
        col = layout.column(align=True)
        col.operator("object.rmirrorx", text="Mirror Along X")
        col.operator("object.rtox", text="Snap To X Axis")
        col.operator("object.rcursor_to_x", text="Cursor to X") 
        
        col = layout.column(align=True)
        col.operator("object.runifyshading", text="Unify Shading")
        col.operator("object.rsetorientation", text="Set Manipulator Orientation")
        
        col = layout.column(align=True)
        col.operator("object.rboundaryseam", text="Boundary Seam")
        col.operator("object.rflatboundaryseam", text="Flat Boundary Seam")
        
        col = layout.column(align=True)
        col.operator("object.rboundarysharp", text="Boundary Sharp")
        col.operator("object.rflatboundarysharp", text="Flat Boundary Sharp")
        
        col = layout.column(align=True)
        col.operator("mesh.loop_to_region", text="Loop To Region")
        col.operator("mesh.region_to_loop", text="Region To Loop")
        col.operator("mesh.select_axis")
        
        col = layout.column(align=True)
        
        col.operator("mesh.bridge_edge_loops", text="Bridge")
        
        col = layout.column(align=True)
        
        col.operator("object.test", text="Test")
        
#class addButtonsInSculptMode(bpy.types.Panel):
#    bl_idname = "rtools_sculptmode"
#    bl_space_type = 'VIEW_3D'
#    bl_region_type = 'TOOLS'
#
#    bl_label = "RTools"
#    bl_context = "sculpt_mode"
#    
#    def draw(self, context):
#        layout = self.layout
#        
#        row = layout.row()
#        row.operator("object.rsetobjectmode",text="",icon="OBJECT_DATAMODE")
#        row.operator("object.rseteditmode",text="",icon="EDITMODE_HLT")
#        row.operator("object.rsetsculptmode",text="",icon="SCULPTMODE_HLT")
#        row.operator("object.rsettexturemode",text="",icon="TPAINT_HLT")
#        
#        row = layout.row()
#        subrow = row.row()
#        
#        subrow.operator("view3d.viewnumpad",text="",icon="TRIA_DOWN").type='TOP'
#        subrow.operator("view3d.viewnumpad",text="",icon="TRIA_RIGHT").type='LEFT'
#        subrow.operator("view3d.viewnumpad",text="",icon="TRIA_LEFT").type='RIGHT'
#        subrow.operator("view3d.viewnumpad",text="",icon="TRIA_UP").type='FRONT'
#        
#class addButtonsInArmatureEditMode(bpy.types.Panel):
#    bl_idname = "rtools_armatureeditmode"
#    bl_space_type = 'VIEW_3D'
#    bl_region_type = 'TOOLS'
#
#    bl_label = "RTools"
#    bl_context = "armature_edit"
#    
#    def draw(self, context):
#        layout = self.layout
#        
#        row = layout.row()
#        row.operator("object.rsetobjectmode",text="",icon="OBJECT_DATAMODE")
#        row.operator("object.rseteditmode",text="",icon="EDITMODE_HLT")
#        row.operator("object.rsetsculptmode",text="",icon="SCULPTMODE_HLT")
#        row.operator("object.rsettexturemode",text="",icon="TPAINT_HLT")
#        row.operator("object.rsetpivotcursor",text="",icon="CURSOR")
#        row.operator("object.rsetpivotmedian",text="",icon="ROTATECENTER")
#        
#        row = layout.row()
#        subrow = row.row()
#        subrow.operator("view3d.viewnumpad",text="",icon="TRIA_DOWN").type='TOP'
#        subrow.operator("view3d.viewnumpad",text="",icon="TRIA_RIGHT").type='LEFT'
#        subrow.operator("view3d.viewnumpad",text="",icon="TRIA_LEFT").type='RIGHT'
#        subrow.operator("view3d.viewnumpad",text="",icon="TRIA_UP").type='FRONT'
#        
#class addButtonsInArmaturePoseMode(bpy.types.Panel):
#    bl_idname = "rtools_armatureposemode"
#    bl_space_type = 'VIEW_3D'
#    bl_region_type = 'TOOLS'
#
#    bl_label = "RTools"
#    bl_context = "posemode"
#    
#    def draw(self, context):
#        layout = self.layout
#        
#        row = layout.row()
#        row.operator("object.rsetobjectmode",text="",icon="OBJECT_DATAMODE")
#        row.operator("object.rseteditmode",text="",icon="EDITMODE_HLT")
#        row.operator("object.rsetsculptmode",text="",icon="SCULPTMODE_HLT")
#        row.operator("object.rsettexturemode",text="",icon="TPAINT_HLT")
#        row.operator("object.rsetpivotcursor",text="",icon="CURSOR")
#        row.operator("object.rsetpivotmedian",text="",icon="ROTATECENTER")
#        
#        row = layout.row()
#        subrow = row.row()
#        subrow.operator("view3d.viewnumpad",text="",icon="TRIA_DOWN").type='TOP'
#        subrow.operator("view3d.viewnumpad",text="",icon="TRIA_RIGHT").type='LEFT'
#        subrow.operator("view3d.viewnumpad",text="",icon="TRIA_LEFT").type='RIGHT'
#        subrow.operator("view3d.viewnumpad",text="",icon="TRIA_UP").type='FRONT'
#        
#class addButtonsInTextureMode(bpy.types.Panel):
#    bl_idname = "rtools_texturemode"
#    bl_space_type = 'VIEW_3D'
#    bl_region_type = 'TOOLS'
#
#    bl_label = "RTools"
#    bl_context = "imagepaint"
#    
#    def draw(self, context):
#        layout = self.layout
#        
#        row = layout.row()
#        row.operator("object.rsetobjectmode",text="",icon="OBJECT_DATAMODE")
#        row.operator("object.rseteditmode",text="",icon="EDITMODE_HLT")
#        row.operator("object.rsetsculptmode",text="",icon="SCULPTMODE_HLT")
#        row.operator("object.rsettexturemode",text="",icon="TPAINT_HLT")
#        
#        row = layout.row()
#        subrow = row.row()
#        subrow.operator("view3d.viewnumpad",text="",icon="TRIA_DOWN").type='TOP'
#        subrow.operator("view3d.viewnumpad",text="",icon="TRIA_RIGHT").type='LEFT'
#        subrow.operator("view3d.viewnumpad",text="",icon="TRIA_LEFT").type='RIGHT'
#        subrow.operator("view3d.viewnumpad",text="",icon="TRIA_UP").type='FRONT'

# REGISTER UNREGISTER

def register():
    
    bpy.utils.register_module(__name__)

def unregister():
    
    bpy.utils.unregister_module(__name__)
    
if __name__ == "__main__":
    register()
