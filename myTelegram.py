from telegram.ext.dispatcher import run_async
from datetime import datetime
import exchangeAPI
import myDB
import myWeb3
import threading
import util


def mc(update, context):
    try:
        circ = 100000000 - int(myWeb3.getCirc())
        anyprice = myWeb3.getPrice('ANY')
        message = '<code>'
        mc = int(circ * anyprice)
        message += 'Market cap'.ljust(12) + ': ' + f'${mc:,}'
        message += '\n' + 'ANY price'.ljust(12) + ': ' + f'${anyprice:.3f}'
        message += '\nCirc. supply'.ljust(12) + ': ' + str(f'{circ:,}') + ' ANY'
        message += '\n' + 'Tot. supply '.ljust(12) + ': ' + '100,000,000 ANY'
        # message += '\n' + 'Calc. CMC Rank'.ljust(12) + ': ' + str(CMC.getCMCRank(mc))
        message += '</code>'
    except Exception as error:
        message = str(error)
        util.error()
    printInfo('MC', message, update, context)
    tg_msg = context.bot.send_message(chat_id=update.effective_chat.id, text=message,
                                      parse_mode='HTML')
    deleteMsg(context.bot, tg_msg)
    return


def printInfo(command, msg, update, context):
    try:
        console = str(datetime.now()) + '\n'
        console += f'Command : /{command} {" ".join(context.args)}\n'
        console += f'Result : {msg}'
        user = update.message.from_user
        console += '\nYou talk with user {}, his user ID: {} and his name: {} {}'.format(user['username'], user['id'], user['first_name'], user['last_name']) + '\n'
        console += '=' * 30
        print(console)
        util.log(console)
    except Exception as error:
        util.error()
        print(error)
    return


def apy_all(top=500):
    msg = '<b>APY over the last 24 hours</b>\n'
    records = myDB.getAPY('', top)
    if len(records) == 0:
        return 'Unable to load data'
    ANY_distributed = True
    i = 0
    for rec in records:
        i += 1
        msg += str(i) + '.' + str(rec) + '\n'
        if rec.any_rewards == 0:
            ANY_distributed = False
    msg += ''
    if not ANY_distributed:
        msg += '<em>* Some ANY rewards are not distributed yet.</em>\n'
    msg += f'\n<em>check {util.build_href("","","AnySwapInfo")} for detailed stats and APY</em>'
    return msg


def apy_lp(lp):
    if myDB.isValidLP(lp):
        msg = f'<b>APY for {lp} pool</b>\n<code>'
        records = myDB.getAPY(lp, 0)
        if len(records) == 0:
            return 'Unable to load data'
        ANY_distributed = True
        for rec in records:
            if rec.any_rewards is not None:
                if rec.any_rewards == 0:
                    ANY_distributed = False
                msg += str(rec) + '\n'
        msg += '</code>'
        if not ANY_distributed:
            msg += '<em>* Some ANY rewards are not distributed yet.</em>'
        return msg
    else:
        return f"'{lp}' pool is not found"


def vol_all(arg='TOP'):
    msg = '<b>Trading Volume over the last 24 hours</b>\n'
    if arg == 'CALC':
        records = myDB.getVOLCALC()
    else:
        records = exchangeAPI.getVOL()
    if len(records) == 0:
        return 'Unable to load data'
    total_volume = 0
    others_volume = 0
    for rec in records:
        if rec.vol < 5000:
            others_volume += rec.vol
        if arg == 'ALL' or (arg == 'TOP' and rec.vol > 5000) or arg == 'CALC':
            msg += str(rec) + '\n'
        total_volume += rec.vol
    if arg == 'TOP':
        msg += 'Others'.ljust(10) + f'${others_volume:,.0f}\n'
    msg += '=' * 20 + '\n'
    msg += 'Total'.ljust(10) + f'${total_volume:,.0f}'
    msg += ''
    if arg == 'CALC':
        msg += '\n<em>* Volume information is approximate.</em>'
    return msg


def vol_lp(lp):
    # NOT USED
    if myDB.isValidLP(lp):
        msg = f'<b>Trading Volume for {lp} pool</b>\n<code>'
        records = exchangeAPI.getVOL()
        if len(records) == 0:
            return 'Unable to load data'
        for rec in records:
            if rec.vol is not None:
                msg += str(rec) + '\n'
        msg += '</code><em>* Volume information is approximate.</em>'
        return msg
    else:
        return f"'{lp}' pool is not found"


def il_lp(lp):
    if myDB.isValidLP(lp):
        msg = f'<b>Impermanent Loss for {lp} pool</b>\n<code>'
        records = myDB.getIL(lp)
        if len(records) == 0:
            return 'Data not found.'
        for rec in records:
            if rec.il is not None:
                msg += str(rec) + '\n'
        msg += '</code>'
        return msg
    else:
        return f"'{lp}' pool is not found"


def net_lp(lp):
    if myDB.isValidLP(lp):
        msg = f'<b>Net Growth for {lp} pool</b>\n<code>'
        records = myDB.getNet(lp)
        if len(records) == 0:
            return 'Data not found.'
        for rec in records:
            if rec.net:
                msg += str(rec) + '\n'
        msg += '</code>'
        return msg
    else:
        return f"'{lp}' pool is not found"


@run_async
def apy(update, context):
    try:
        msg = ''
        if len(context.args) == 0:
            arg = "TOP"
        else:
            arg = ''.join(context.args).upper()
        if arg.upper() == 'ALL' or arg.upper() == 'A':
            msg = apy_all()
        elif arg == 'TOP':
            msg = apy_all(6)
        else:
            lp = args_to_lp(context.args)
            if lp == '':
                msg = f'Invalid command "{" ".join(context.args)}"'
            else:
                msg = apy_lp(lp)
    except Exception as error:
        util.error()
        msg = str(error)
    printInfo('APY', msg, update, context)
    message = context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='HTML')
    deleteMsg(context.bot, message)
    return


@run_async
def vol(update, context):
    try:
        msg = ''
        if len(context.args) == 0:
            arg = "TOP"
        else:
            arg = ''.join(context.args).upper()

        if arg.upper() == 'ALL' or arg.upper() == 'TOP' or arg.upper() == 'CALC':
            msg = vol_all(arg.upper())
        else:
            lp = args_to_lp(context.args)
            if lp == '':
                msg = f'Invalid parameters "{" ".join(context.args)}"'
            else:
                msg = vol_lp(lp)
    except Exception as error:
        util.error()
        msg = str(error)
    printInfo('VOL', msg, update, context)
    message = context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='HTML')
    deleteMsg(context.bot, message)
    return


@run_async
def tvl(update, context):
    try:
        msg = tvl_all()
    except Exception as error:
        util.error()
        msg = str(error)
    printInfo('TVL', msg, update, context)
    tg_msg = context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='HTML')
    deleteMsg(context.bot, tg_msg)
    return


@run_async
def undermaintenance(update, context):
    tg_msg = context.bot.send_message(chat_id=update.effective_chat.id, text="Under maintenance", parse_mode='HTML')
    deleteMsg(context.bot, tg_msg)
    return


def args_to_lp(args):
    lp = ''.join(args).upper().replace('-', '')
    if 'FSN' in lp:
        coin1 = 'FSN'
        lp = lp.replace('AUSDT', 'USDT').replace('AETH', 'ETH').replace('ABTC', 'BTC').replace('AUNI', 'UNI')
    elif 'BNB' in lp:
        coin1 = 'BNB'
    else:
        return ''
    coin2 = lp.replace(coin1, '')
    return f'{coin1}-{coin2}'


@run_async
def il(update, context):
    try:
        msg = ''
        if len(context.args) == 0:
            msg = 'Please specify a pool'
        else:
            lp = args_to_lp(context.args)
            if lp == '':
                msg = f'Invalid parameters "{" ".join(context.args)}"\nPlease specify a valid pool.'
            else:
                msg = il_lp(lp)
    except Exception as error:
        util.error()
        msg = str(error)
    printInfo('IL', msg, update, context)
    message = context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='HTML')
    deleteMsg(context.bot, message)
    return


def tvl_all():
    msg = '<b>Total Value Locked (TVL) on Anyswap</b>\n'
    records = myDB.getTVLall()
    if len(records) == 0:
        return 'Unable to load data'
    total_tvl = 0.0
    i = 0
    others_tvl = 0
    for rec in records:
        i += 1
        total_tvl += float(rec.price) * float(rec.tvl)
        if i <= 6:
            msg += str(rec) + '\n'
        else:
            others_tvl += float(rec.price) * float(rec.tvl)
    if others_tvl > 0:
        msg += str(f'${others_tvl:,.0f}').ljust(10) + ' Others\n'
    msg += '=' * 17 + '\n'
    msg += str(f'${total_tvl:,.0f}').ljust(10) + ' Total'
    msg += ''
    return msg


def deleteMsg(bot, message):
    try:
        if message.chat.type == 'private' or message.chat.type == 'group':
            return
        timer = threading.Timer(600.0, deleteMsgTimer, [bot, message])
        timer.start()
    except Exception as error:
        print(error)
    return


def deleteMsgTimer(bot, message):
    try:
        bot.delete_message(chat_id=message.chat_id,
                           message_id=message.message_id)
    except Exception as error:
        print(error)


@run_async
def net(update, context):
    try:
        msg = ''
        if len(context.args) == 0:
            msg = 'Please specify a pool'
        else:
            lp = args_to_lp(context.args)
            if lp == '':
                msg = f'Invalid parameters "{" ".join(context.args)}"\nPlease specify a valid pool.'
            else:
                msg = net_lp(lp)
    except Exception as error:
        util.error()
        msg = str(error)
    printInfo('NET', msg, update, context)
    message = context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='HTML')
    deleteMsg(context.bot, message)
    return
