# Football Grass Telegram Bot


## Information 

- A Telegram bot built with Python using the `python-telegram-bot` library. 
- The bot provides information about number of your commit in telegram


## Demo

[Online Bot](https://t.me/footbalgrassbot)


## Screenshots 


![image](https://github.com/aliseyedi01/Portfolio-Telegram-Bot/assets/118107025/ca62063c-6db1-4b00-8c3a-d76f4661719d)


## Features

- **Commit** : Show number of today's commit and all commit from 2024
- **Streak** :  show continues day done commit for current and longest


## Technology Used

- **Python:** Programming language used for bot development.
- **python-telegram-bot:** Telegram Bot API wrapper for Python.
- **requests:** Library for making HTTP requests.
- **dotenv:** Library for loading environment variables from a .env file.



## Prerequisites

- Python 3.6 or later
- Telegram API token
- GitHub API token 

## Installation

1. Clone the repository:

    ```bash
    git https://github.com/aliseyedi01/Footbal_Grass_Bot.git
    cd your_repository
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file and add your Telegram API token:

    ```plaintext
    TOKEN_TEL=your_telegram_api_token
	TOKEN_GH=your_github_api_token
    ```

4. Run the bot:

    ```bash
    python main.py
    ```

## Usage

1. Start the bot by sending the `/report` command in the Telegram app.



## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.