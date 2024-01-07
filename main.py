import os
from datetime import datetime
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update
import logging
from github_fetcher import Fetcher , usernames_list

load_dotenv()

TOKEN_TEL = os.getenv("TOKEN_TEL")
BOT_USERNAME = '@footbalgrassbot'


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class MyBot:
    def __init__(self, token):
        self.app = Application.builder().token(token).build()

    def run(self):
        self.add_handlers()
        self.app.run_polling(timeout=10)

    def add_handlers(self):
        self.app.add_handler(CommandHandler('report', self.send_report))
        self.app.add_error_handler(self.error)


    async def send_report(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        fetcher = Fetcher(usernames_list)
        results = fetcher.fetch_contributions_for_users()
        sorted_results = sorted(results, key=lambda item: item['today_contribution'], reverse=True)

        current_date = datetime.utcnow().strftime("%Y - %m - %d")
        current_day = datetime.utcnow().strftime("%A")
        # result_url = "https://github1s.com/aliseyedi01"

        report_message = f"🧾 Report Contribution & Streak  \n\nData: {current_date}   Day: {current_day} \n\n"
        for result in sorted_results:
            emoji_prefix = "😉" if result['today_contribution'] > 0 else "😣"
            name_link = f"<a href='{result['github_link']}'>{result['name']}</a>"
            report_message += f"{emoji_prefix} {name_link}\n" \
                              f"Contribution:  Today: {result['today_contribution']},     Total: {result['total_contribution']}\n" \
                              f"Streak:             Current: {result['current_streak']} , Longest: {result['longest_streak']}\n" \
                              f"〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n"


        await update.message.reply_text(text=report_message,parse_mode="HTML")


    async def error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.error(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    logger.info('Starting bot...')
    my_bot = MyBot(TOKEN_TEL)
    my_bot.run()


