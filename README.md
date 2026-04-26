# ColoradoMesh MeshCore Repeater Configurator

A Docker application that will automatically configure a connected MeshCore repeater using a supplied settings file.

*NOTE*: Due to OS-level permissions related to device access, this Docker application DOES NOT work on MacOS.

apply_settings.py can also be used right from the command-line with the necessary dependencies installed.

```
python -m apply_settings --settings-file-path .\coloradomesh_meshcore_repeater_config_XXX-YYYY-ZZZZZ-AA-BBBB.json --serial-port=COM14
```


