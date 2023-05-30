import bpy
import os

def import_gazebo(filename):
    config = '<?xml version="1.0"?> \n <model>\n<name>*</name>\n<version>1.0</version>\n<sdf version="1.5">model.sdf</sdf>\n<author>\n<name>Skyrats</name>\n<email>guilhermesangabriel@gmail.com</email>\n</author>\n<description>\nmodel imported from blender.\n</description>\n</model>'
    model = '<?xml\nversion="1.0"\n?>\n<sdf\nversion="1.6">\n<model\nname="*">\n<static>true</static>\n<link\nname="link">\n<collision\nname="collision">\n<geometry>\n<mesh>\n<scale>1\n1\n1</scale>\n<uri>//*/meshes/*.dae</uri>\n</mesh>\n<surface>\n<friction>\n<ode>\n<mu>1.2</mu>\n<mu2>1.2</mu2>\n</ode>\n</friction>\n</surface>\n</geometry>\n</collision>\n<visual\nname="visual">\n<geometry>\n<mesh>\n<scale>1\n1\n1</scale>\n<uri>model://*/meshes/*.dae</uri>\n</mesh>\n</geometry>\n</visual>\n</link>\n</model>\n</sdf>'

    path = bpy.path.abspath('//') + "/" + filename
    path_meshes = path + "/meshes"
    try:
        os.makedirs(path_meshes)
        print(path_meshes)
    except OSError as error:
        print(error)  
        
    print(path_meshes + "/" + filename)
    
    bpy.ops.wm.collada_export(filepath = path_meshes + "/" + filename)
    #write to .dae file to correct non existance of ambient light setting
    with open(path_meshes + "/" + filename + ".dae", "r") as file:
        collada = file.read()
        collada = collada.replace("</diffuse>", '</diffuse>\n\t\t<ambient>\n\t\t<color sid="ambient">1 1 1 1</color>\n\t\t</ambient>')
        file.close()

    with open(path_meshes + "/" + filename + ".dae", "w") as file:
        file.write(collada)
        file.close()
    """
    #write to model.config and model.sdf
    with open("model.config", "r") as file:
        config = file.read()
        config = config.replace("*", filename)
        file.close()
    """  
    
    with open(path + "/model.config", "w") as file:
        config = config.replace("*", filename)
        file.write(config)
        file.close()
        
    with open(path + "/model.sdf", "w") as file:
        model = model.replace("*", filename)
        file.write(model)
        file.close()

class panel (bpy.types.Panel):
    bl_label = "Gazebo"
    bl_idname = "PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Gazebo"

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.label(text = "Import to gazebo using .dae format", icon='PACKAGE')
        row = layout.row()
        row.operator("wm.gazeboop")
        

class WM_OT_import_gazebo_op(bpy.types.Operator):
    bl_label = "Import to gazebo"
    bl_idname = "wm.gazeboop"
    
    filename:bpy.props.StringProperty(name= "Enter name:", default = "")
    
    def execute(self, context):
        
        import_gazebo(self.filename)
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

def register():
    bpy.utils.register_class(WM_OT_import_gazebo_op)
    bpy.utils.register_class(panel)
    
def unregister():
    bpy.utils.unregister_class(panel)
    bpy.utils.unregister_class(WM_OT_import_gazebo_op)
    
if __name__ == "__main__":
    register()
