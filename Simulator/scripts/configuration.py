import bpy

def customize_ui():
    # Hide unnecessary UI elements
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.show_gizmo = False
                    space.overlay.show_floor = False
                    space.overlay.show_axis_x = False
                    space.overlay.show_axis_y = False

    # Set up custom layout
    bpy.context.window.workspace.name = "Blood Simulation Workspace"

# Run the customization on startup
customize_ui()
