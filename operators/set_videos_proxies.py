import os
import bpy


class SetVideosProxies(bpy.types.Operator):
    bl_idname = "power_sequencer.set_video_proxies"
    bl_label = "Set Videos Proxies"
    bl_description = "Set all video strips in the current scene as proxies and rebuild using Blender's proxy generation"
    bl_options = {"REGISTER"}

    use_custom_folder = bpy.props.BoolProperty(
        name="Custom proxy folder",
        description="Use a custom folder to store proxies",
        default=True)
    custom_folder_path = bpy.props.StringProperty(
        name="Custom proxy folder path",
        description="Store the generated proxies in a specific folder on your hard drive (absolute path)",
        default=r"D:\Program Files\Blender proxies")

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        sequencer = bpy.ops.sequencer

        selection = bpy.context.selected_sequences
        if not bpy.context.selected_sequences:
            self.report({"ERROR_INVALID_INPUT"}, "No movie sequences found")
            return {'CANCELLED'}

        prefs = context.user_preferences.addons[__package__].preferences

        for s in selection:
            if s.type not in ('MOVIE', 'IMAGE'):
                s.select = False

        sequencer.enable_proxies(proxy_25=prefs.proxy_25,
                                 proxy_50=prefs.proxy_50,
                                 proxy_75=prefs.proxy_75,
                                 proxy_100=prefs.proxy_100,
                                 override=False)
        if prefs.use_custom_folder and prefs.custom_folder_path:
            for s in bpy.context.selected_sequences:
                s.proxy.use_proxy_custom_directory = True
                blend_filename = bpy.path.basename(bpy.data.filepath)
                blend_filename = os.path.splitext(blend_filename)[0]
                s.proxy.directory = os.path.join(prefs.custom_folder_path, blend_filename)

        sequencer.rebuild_proxy({'dict': "override"}, 'INVOKE_DEFAULT')
        return {"FINISHED"}


class SettingsProxies(bpy.types.PropertyGroup):
    proxy_on_import = bpy.props.BoolProperty(
        name="Auto create proxy",
        description="Set and build videos strips as proxies on import for all strips",
        default=True)
    use_custom_folder = bpy.props.BoolProperty(
        name="Custom proxy folder",
        description="Use a custom folder to store proxies",
        default=True)
    custom_folder_path = bpy.props.StringProperty(
        name="Custom proxy folder path",
        description="Store the generated proxies in a specific folder on your hard drive (absolute path)",
        default=r"D:\Program Files\Blender proxies")
    proxy_25 = bpy.props.BoolProperty(name="Proxy at 25%", default=True)
    proxy_50 = bpy.props.BoolProperty(name="Proxy at 50%", default=False)
    proxy_75 = bpy.props.BoolProperty(name="Proxy at 75%", default=False)
    proxy_100 = bpy.props.BoolProperty(name="Proxy at 100%", default=False)
    proxy_quality = bpy.props.IntProperty(
        name="Proxy JPG quality",
        default=90, min=1, max=100)


# Panel for proxy options management
def proxy_menu(self, context):
    # prefs = context.user_preferences.addons['power_sequencer'].preferences
    power_sequencer_proxy = context.scene.power_sequencer_proxy

    layout = self.layout

    row = layout.row()
    row.separator()
    row = layout.row()
    row.prop(power_sequencer_proxy, 'proxy_on_import')

    # if prefs.proxy_on_import:
    row = layout.row(align=True)
    row.prop(power_sequencer_proxy, "proxy_25", toggle=True)
    row.prop(power_sequencer_proxy, "proxy_50", toggle=True)
    row.prop(power_sequencer_proxy, "proxy_75", toggle=True)
    row.prop(power_sequencer_proxy, "proxy_100", toggle=True)

    row = layout.row()
    row.prop(power_sequencer_proxy, "proxy_quality")
