from telegram.ext import Updater, CommandHandler
from myTelegram import apy, mc, il, tvl, vol, net, undermaintenance, cyc


def loadTelegramAPI():
    with open('telegramapi.txt', 'r') as f:
        return f.read()


def main():
    updater = Updater(loadTelegramAPI(), use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('apy', apy))
    dp.add_handler(CommandHandler('tvl', tvl))
    dp.add_handler(CommandHandler('mc', mc))
    dp.add_handler(CommandHandler('il', il))
    dp.add_handler(CommandHandler('vol', vol))
    dp.add_handler(CommandHandler('net', net))
    dp.add_handler(CommandHandler('cyc', cyc))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
