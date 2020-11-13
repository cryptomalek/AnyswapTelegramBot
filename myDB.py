#!/usr/bin/python
import psycopg2
import util
from config import config


def formatPercent(percentage: int, precision=2) -> str:
    if percentage is None:
        return '-'
    return "{:.{}f}%".format(percentage * 100, precision)


def pad(s: str, dirc='^') -> str:
    return f'{s:{dirc}8}'


class APYRecord:
    def __init__(self, name, any_rewards, trading_rewards, total_rewards):
        self.name = name
        self.any_rewards = any_rewards
        self.trading_rewards = trading_rewards
        self.total_rewards = total_rewards
        return

    def __str__(self):
        return f'{util.build_href("pair", self.name, self.name)}: {formatPercent(self.total_rewards)} ({formatPercent(self.any_rewards)} ANY + {formatPercent(self.trading_rewards)} Fees)'


class ILRecord:
    def __init__(self, period, il):
        self.period = period
        self.il = il
        return

    def __str__(self):
        return pad(self.period, '<') + ':' + pad(formatPercent(self.il, 3))


class NetRecord:
    def __init__(self, period, net):
        self.period = period
        self.net = net
        return

    def __str__(self):
        return pad(self.period, '<') + ':' + pad(formatPercent(self.net, 3))


class VOLRecord2:
    def __init__(self, name, vol):
        self.name = name
        self.vol = vol if vol is not None else 0
        return

    def __str__(self):
        return self.name.ljust(10) + f'${self.vol:,.0f}'


class TVLRecord:
    def __init__(self, name, tvl, price):
        self.token = name
        self.tvl = tvl
        self.price = price
        return

    def __str__(self):
        if self.tvl < 1000:
            formatted_tvl = str(f'{self.tvl:.2f}').ljust(10)
        else:
            formatted_tvl = str(f'{self.tvl:,.0f}').ljust(10)
        return formatted_tvl + f' {util.build_href("token", self.token, self.token)}'


def getVOLCALC(lp=''):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        if lp == '':
            sql = f'SELECT lp, vol FROM vol_all;'
        else:
            sql = f'SELECT "period", vol FROM vol_lp WHERE lp = \'{lp}\';'
        cur.execute(sql)
        rows = cur.fetchall()
        result = []
        for row in rows:
            rec = VOLRecord2(row[0], row[1])
            result.append(rec)
        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def getIL(lp):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        sql = f'SELECT period, il FROM il_lp WHERE lp = \'{lp}\' ORDER BY day;'
        cur.execute(sql)
        rows = cur.fetchall()
        result = []
        for row in rows:
            rec = ILRecord(row[0], row[1])
            result.append(rec)
        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def getNet(lp):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        sql = f'SELECT period, net FROM net_lp WHERE lp = \'{lp}\' ORDER BY day;'
        cur.execute(sql)
        rows = cur.fetchall()
        result = []
        for row in rows:
            rec = NetRecord(row[0], row[1])
            result.append(rec)
        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def getAPY(lp='', top=500):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        if lp == '':
            sql = f'SELECT name, "any", trading, total FROM apy_all limit {top};'
        else:
            sql = f'SELECT description, "any", trading, total FROM apy_lp WHERE name = \'{lp}\' ORDER BY day;'
        cur.execute(sql)
        rows = cur.fetchall()
        result = []
        for row in rows:
            rec = APYRecord(row[0], row[1], row[2], row[3])
            result.append(rec)
        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def getTVLall():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(
            f'SELECT token, tvl, price FROM tvl_all;')
        rows = cur.fetchall()
        result = []
        for row in rows:
            rec = TVLRecord(row[0], row[1], row[2])
            result.append(rec)
        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return []
    finally:
        if conn is not None:
            conn.close()


def isValidLP(lp: str) -> bool:
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(
            f"SELECT 1 FROM public.token t WHERE t.name = '{lp}'")
        rows = cur.fetchall()
        result = (len(rows) > 0)
        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
