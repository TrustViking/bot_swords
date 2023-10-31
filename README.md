# Bot Swords

## Description

Bot Swords is a Telegram bot developed as part of the international CREATIVE SOCIETY project. The bot is designed to replace stop words in video titles. The CREATIVE SOCIETY project unites people from more than 180 countries on a voluntary basis to transition from a consumerist societal format to a new, creative one where human life is the highest value.

## Key Features

- Stop-word replacement in titles
- Configurable through command line arguments
- Easily deployable

## Environment Variables

To set up the required environment variables, follow the steps below:

1. Open your shell's profile file in a text editor. For example, for Bash:

    ```bash
    nano ~/.bashrc
    ```

   Or for Zsh:

    ```bash
    nano ~/.zshrc
    ```

2. Add the following line at the end of the file:

    ```bash
    export TELEGRAM_TOKEN_SWORDS=your_token_here
    ```

3. Save the file and close the editor.

4. To apply the changes, run the following command:

    ```bash
    source ~/.bashrc  # For Bash
    ```

   Or:

    ```bash
    source ~/.zshrc  # For Zsh
    ```

To check the value of the `TELEGRAM_TOKEN_SWORDS` variable, you can use the following command:

```bash
echo $TELEGRAM_TOKEN_SWORDS
```

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
