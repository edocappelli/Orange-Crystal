"""
Generates plots depending on set settings.
"""


class PlotGenerator(object):
    def __init__(self, list_settings):
        self._settings = self._cloneSettings(list_settings)
        self._setProxiedPlots(None)
        self._setSettingsAreDirty(True)

    def _cloneSettings(self, list_settings):
        for setting in list_settings:
            self._settings.append(setting.clone())

    def _setSettingsAreDirty(self, value):
        self._settings_are_dirty = value

    def _areSettingsDirty(self):
        return self._settings_are_dirty

    def _setProxiedPlots(self, plots):
        self._proxied_plots = plots

    def _proxiedPlots(self):
        return self._proxied_plots

    def _plots(self):
        raise Exception("Must override this method.")

    def plots(self):
        if self._areSettingsDirty():
            plots = self._plots()
            self._setProxiedPlots(plots)
            self._setSettingsAreDirty(False)

        return self._proxiedPlots()

    def setSetting(self, setting_name, value):
        setting = self._settingByName(setting_name)
        setting.setValue(value)
        self._setSettingsAreDirty(True)

    def _settingByName(self,setting_name):
        for setting in self._settings:
            if setting.isNamed(setting_name):
                return setting

        return None

    def settings(self):
        return self._cloneSettings(self._settings)