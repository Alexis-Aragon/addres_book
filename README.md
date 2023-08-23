# Libreta de Contactos - Project

Para correr la libreta desde la terminal
necesitará instalar los siguientes módulos

```sh
pip3 install customtkinter
pip3 install appdirs

```
o use 
```sh
pip3 install -r requirements.txt
```
Después puede ejecutar el archivo con
```sh
python3 libreta_clientes.py
```

También puede usar pyinstaller para crear un ejecutable

En linux mint puede usar
```sh
pyinstaller --onefile -n "Libreta" --add-data "libreta.png:." libreta_clientes.py
```

En windows puede usar
```sh
pyinstaller --onefile -n "Libreta" --add-data "libreta.ico;." libreta_clientes.py
```