# Bot Swords

## Description

Bot Swords is a Telegram bot developed as part of the international CREATIVE SOCIETY project. The bot is designed to replace stop words in video titles. The CREATIVE SOCIETY project unites people from more than 180 countries on a voluntary basis to transition from a consumerist societal format to a new, creative one where human life is the highest value.

## Key Features

- Stop-word replacement in titles
- Configurable through command line arguments
- Easily deployable

## Environment Variables

### Setting Environment Variables on macOS or Linux

To configure the required environment variables, follow these steps:

1. Open your shell's profile file in a text editor. For Bash, use:

    ```bash
    nano ~/.bashrc
    ```

   For Zsh, use:

    ```bash
    nano ~/.zshrc
    ```

2. Add the following line at the end of the file:

    ```bash
    export TELEGRAM_TOKEN_SWORDS=your_token_here
    ```

3. Save the file and close the editor.

4. To apply the changes, run:

    ```bash
    source ~/.bashrc  # For Bash
    ```

   Or:

    ```bash
    source ~/.zshrc  # For Zsh
    ```

To verify the value of the `TELEGRAM_TOKEN_SWORDS` variable, use:

```bash
echo $TELEGRAM_TOKEN_SWORDS
```

### Setting Environment Variables on Windows

To set environment variables on Windows, make the following changes to the `start_swords.bat` file:

Uncomment the line `@REM set TELEGRAM_TOKEN_SWORDS='XXX:YYY'` and insert your Telegram bot token. The line should look like this:

```batch
set TELEGRAM_TOKEN_SWORDS=1234567890:ABCDEFabcdef
```

## Dependencies

### macOS, Windows, Linux

To run this project on macOS, Windows or Linux you'll need to install the following Python libraries:

```bash
pip install aiogram asyncio argparse langdetect psutil pynvml SQLAlchemy chardet
```

Note: Some modules (`io`, `logging`, `os`, `sys`, `time`, `typing`) are Python built-ins and don't require installation.

## Usage

### macOS, Linux

#### Default Startup

```bash
python start_swords.py
```

### Customized Startup

```bash
python start_swords.py -fs swords -ns swords_EN.txt -lf logs.md -ll info
```

### Windows

```bash
start_swords.bat
```

## Examples

(TO-DO: Add examples demonstrating the bot's features)

## License

This project is licensed under the MIT License.

## Support

For more information or questions, please feel free to reach out:

- **Contact Person**: Arthur
- **Email**: [kongotoken@gmail.com](mailto:kongotoken@gmail.com)
