#### Failed to load libPySidePlugin.so in QT Designer

QT Designer shows message: `Cannot load library /usr/lib/qt6/plugins/designer/libPySidePlugin.so: (/usr/lib/qt6/plugins/designer/libPySidePlugin.so: undefined symbol: "PyImport_AddModule")` on Help -> About Plugins.

Solution: `sudo patchelf --add-needed libpython3.10.so /usr/lib/qt6/plugins/designer/libPySidePlugin.so`