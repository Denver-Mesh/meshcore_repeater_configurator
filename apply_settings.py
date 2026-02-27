import asyncio

from meshcore_cli.meshcore_cli import setup_repeater_serial, process_repeater_line

baudrate = 115200
# serial_port = "/dev/ttyUSB0"
serial_port = "/dev/cu.usbmodem1101"
commands = [
    "set owner"
    "get prv.key"
]


async def main() -> None:
    ser = await setup_repeater_serial(port=serial_port, baudrate=baudrate)

    for command in commands:
        await process_repeater_line(ser=ser,
                                    cmd=command)

    ser.close()

    return


if __name__ == "__main__":
    asyncio.run(main())
