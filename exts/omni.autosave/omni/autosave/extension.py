import time
import carb
import omni.ext
import omni.usd
import omni.kit.app


COOLDOWN = 5.0


class AutoSaveExtension(omni.ext.IExt):
    def on_startup(self, ext_id):
        self._last_save = time.time()

        self._update_sub = (
            omni.kit.app.get_app()
            .get_update_event_stream()
            .create_subscription_to_pop(self._on_update)
        )

        carb.log_info("[AutoSave] Running")

    def on_shutdown(self):
        self._update_sub = None

    def _on_update(self, event):
        if time.time() - self._last_save < COOLDOWN:
            return

        ctx = omni.usd.get_context()
        stage = ctx.get_stage()
        if not stage or not ctx.get_stage_url():
            return

        root_layer = stage.GetRootLayer()
        if not root_layer.dirty:
            return

        ctx.save_stage()
        self._last_save = time.time()
        carb.log_info("[AutoSave] Saved")
