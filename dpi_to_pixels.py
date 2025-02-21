bl_info = {
    "name": "Resolution from DPI and Size",
    "blender": (3, 0, 0),
    "category": "Render",
    "version": (1, 1),
    "author": "tolozine",
    "description": "基于毫米和分辨率, 设置渲染像素尺寸",
}

import bpy

# 更新分辨率函数（只有按钮调用）
def update_resolution(context):
    mm_to_inch = 25.4
    width_px = int((context.scene.width_mm / mm_to_inch) * context.scene.dpi)
    height_px = int((context.scene.height_mm / mm_to_inch) * context.scene.dpi)

    # 设置 Blender 渲染分辨率
    context.scene.render.resolution_x = width_px
    context.scene.render.resolution_y = height_px

# 操作类（点击按钮时更新分辨率）
class DPI_TO_PIXELS_OT_set_resolution(bpy.types.Operator):
    bl_idname = "render.set_resolution_from_dpi"
    bl_label = "Set Resolution from DPI and Size"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        update_resolution(context)
        self.report({'INFO'}, f"Resolution set to {context.scene.render.resolution_x}x{context.scene.render.resolution_y} pixels")
        return {'FINISHED'}

# UI 面板（放置在输出属性面板）
class DPI_TO_PIXELS_PT_panel(bpy.types.Panel):
    bl_label = "Set Resolution from DPI"
    bl_idname = "OUTPUT_PT_dpi_to_pixels"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"
    bl_parent_id = "RENDER_PT_format"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # 输入框（不自动更新）
        layout.prop(scene, "width_mm")
        layout.prop(scene, "height_mm")
        layout.prop(scene, "dpi")

        # 按钮（手动更新）
        layout.operator("render.set_resolution_from_dpi")

# 注册插件
def register():
    bpy.utils.register_class(DPI_TO_PIXELS_OT_set_resolution)
    bpy.utils.register_class(DPI_TO_PIXELS_PT_panel)

    # 定义 Scene 属性（无自动更新）
    bpy.types.Scene.width_mm = bpy.props.FloatProperty(default=210.0)
    bpy.types.Scene.height_mm = bpy.props.FloatProperty(default=297.0)
    bpy.types.Scene.dpi = bpy.props.IntProperty(default=300)

# 注销插件
def unregister():
    bpy.utils.unregister_class(DPI_TO_PIXELS_OT_set_resolution)
    bpy.utils.unregister_class(DPI_TO_PIXELS_PT_panel)

    del bpy.types.Scene.width_mm
    del bpy.types.Scene.height_mm
    del bpy.types.Scene.dpi

if __name__ == "__main__":
    register()
