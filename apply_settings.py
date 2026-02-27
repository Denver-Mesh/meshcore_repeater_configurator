import asyncio
from argparse import ArgumentParser, Namespace

from denvermesh.meshcore.models.general.repeater_settings import RepeaterSettings
from meshcore_cli.meshcore_cli import setup_repeater_serial, process_repeater_line

BAUDRATE = 115200
SETTINGS_FILE_PATH = "/settings.json"  # Mount this volume via Docker
SERIAL_PORT = "/dev/cu.usbmodem1101"  # Mount this device via Docker


def _parse_settings_file(file_path: str) -> RepeaterSettings:
    """
    Parse the settings file and return a RepeaterSettings object.
    :param file_path: The path to the settings file (e.g. "/settings.json").
    :type file_path: str
    :return: A RepeaterSettings object containing the settings from the file.
    :rtype: RepeaterSettings
    """
    import json
    with open(file_path, 'r') as f:
        settings: dict = json.load(f)

    return RepeaterSettings(**settings)


async def _process_commands(ser, commands: list[str]) -> None:
    for command in commands:
        if not command:  # Skip missing commands
            continue
        await process_repeater_line(ser=ser,
                                    cmd=command)
        await asyncio.sleep(1)  # Sleep between commands to ensure they are processed


async def main(_args: Namespace) -> None:
    _baudrate = args.baudrate
    _settings_file_path = args.settings_file_path

    repeater_settings = _parse_settings_file(file_path=_settings_file_path)

    ser = await setup_repeater_serial(port=SERIAL_PORT, baudrate=_baudrate)
    commands = [
        'erase',
        repeater_settings.set_private_key_command,
        repeater_settings.set_name_command,
        repeater_settings.set_owner_info_command,
        *(repeater_settings.add_region_commands or []),
        repeater_settings.add_home_region_command,
        repeater_settings.save_regions_commands,
        repeater_settings.set_txdelay_command,
        repeater_settings.set_direct_txdelay_command,
        repeater_settings.set_rxdelay_command,
        repeater_settings.set_advert_interval_command,
        repeater_settings.set_flood_advert_interval_command,
        repeater_settings.set_guest_password_command,
    ]
    await _process_commands(ser=ser, commands=commands)
    ser.close()

    print("PLEASE REBOOT YOUR REPEATER NOW.")

    return


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Apply MeshCore repeater settings to a connected repeater via serial connection.")
    parser.add_argument("--baudrate",
                        type=int,
                        default=BAUDRATE,
                        help=f"Baud rate for the serial connection (default: {BAUDRATE})")
    parser.add_argument("--settings-file-path",
                        type=str,
                        default=SETTINGS_FILE_PATH,
                        help=f"Path to the settings file (default: {SETTINGS_FILE_PATH})")

    args = parser.parse_args()

    asyncio.run(main(_args=args))
