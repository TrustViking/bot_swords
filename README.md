# Bot Swords

## Description

Bot Swords is a Telegram bot developed as part of the international CREATIVE SOCIETY project. The bot is designed to replace stop words in video titles.
The CREATIVE SOCIETY project unites people from more than 180 countries on a voluntary basis to transition from a consumerist societal format to a new, creative one where human life is the highest value.

## Key Features

- Stop-word replacement in titles
- Configurable through command line arguments
- Easily deployable

## Environment Variables

The project requires the following environment variables:

- `TELEGRAM_TOKEN_SWORDS`: The token of the Telegram bot, obtained from @BotFather.

## Dependencies

### macOS

To run this project on macOS, you'll need to install the following Python libraries:

```bash
pip install aiogram asyncio argparse langdetect psutil pynvml SQLAlchemy chardet
```

### Windows

(Instructions for installing dependencies on Windows)

### Linux

(Instructions for installing dependencies on Linux)

Note: Some modules (`io`, `logging`, `os`, `sys`, `time`, `typing`) are Python built-ins and don't require installation.

## Usage

### Default Startup

```bash
python start_swords.py
```

### Customized Startup

```bash
python start_swords.py -fs swords -ns swords_EN.txt -lf logs.md -ll info
```

## Examples

(TO-DO: Add examples demonstrating the bot's features)

## License

This project is licensed under the MIT License.

## Support

For more information or questions, please feel free to reach out:

- **Contact Person**: Arthur
- **Email**: [kongotoken@gmail.com](mailto:kongotoken@gmail.com)
