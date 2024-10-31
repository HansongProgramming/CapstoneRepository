import bpy

class SimpleCustomPanel(bpy.types.Panel):
    """Creates a custom panel with a button in the 3D Viewport"""
    bl_label = "Custom Button Panel"
    bl_idname = "VIEW3D_PT_custom_panel"
    bl_space_type = 'VIEW_3D'        # Area to show panel (3D View)
    bl_region_type = 'UI'            # Panel region (Tool Shelf/Sidebar)
    bl_category = "Custom Tab"       # Sidebar Tab name

    def draw(self, context):
        layout = self.layout
        row = layout.row()  # Creates a row layout to hold UI elements

        # Add button
        row.operator("wm.custom_button_operator")  # Refers to the operator we define below


class CustomButtonOperator(bpy.types.Operator):
    """Custom button that prints a message in the console"""
    bl_idname = "wm.custom_button_operator"  # Unique ID for the button operator
    bl_label = "Click Me!"  # Text on the button

    def execute(self, context):
        self.report({'INFO'}, "Button Pressed!")  # Display message in status bar
        print("Custom button was pressed!")  # Print message to console
        return {'FINISHED'}

# Register classes
def register():
    bpy.utils.register_class(SimpleCustomPanel)
    bpy.utils.register_class(CustomButtonOperator)

def unregister():
    bpy.utils.unregister_class(SimpleCustomPanel)
    bpy.utils.unregister_class(CustomButtonOperator)

if __name__ == "__main__":
    register()
