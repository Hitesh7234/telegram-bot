from typing import Final
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

Token: Final = "7288132283:AAG2qgcGFXSeDAd265lUNH8rDm214x7otmY"
bot_username: Final = "@scrap_wiki_bot"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! How can I assist you today?")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You can ask me anything!")

# Handle Responses
def handle_response(text: str) -> str:
    if text:
        return wiki(text)
    return "Please provide a valid input."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f"User ({update.message.chat.id}) in {message_type}: \"{text}\"")
    if message_type == "group":
        if bot_username in text:
            new_text: str = text.replace(bot_username, "").strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    
    print("Bot:", response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

def wiki(text: str) -> str:
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    action = ActionChains(driver)
    
    try:
        driver.get(url=f"https://en.wikipedia.org/wiki/{text}")
        info = driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div[1]/p[2]')
        return info.text
    except Exception as e:
        return f"We can't find the term '{text}'. Please check if it's correct."
    finally:
        driver.quit()

if __name__ == '__main__':
    print("Starting Bot....")
    app = Application.builder().token(Token).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))

    # Message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Error handler
    app.add_error_handler(error)

    print("Polling.....")
    app.run_polling(poll_interval=3)
