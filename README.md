# Osmium Bot

## About the project
This is a fully custom multi-function Discord bot written in Python.

## Installation
1. (Optional) Setup a virtual environment
    ```
    virtualenv venv
    ```
2. Install dependencies
    ```
    pip install -r requirements.txt
    ```
3. Rename `config_original.py` to `config.py`

4. Configure the bot by editing `config.py`. You need to at least add you own bot token. If you want to edit which modules are loaded, you need to do so in `bot.py`.

5. Run `bot.py`

### Dependencies
- [py-cord](https://github.com/Pycord-Development/pycord)
- [mcstatus](https://github.com/py-mine/mcstatus)
- [mojang](https://github.com/summer/mojang)
- [rcon](https://github.com/conqp/rcon)

## License

Distributed under the MIT License. See `LICENCE` for more information.