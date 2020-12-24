#!/usr/bin/python
import psycopg2
import util
from config import config


class APYRecord:
    def __init__(self, name, any_rewards, trading_rewards, total_rewards):
        self.name = name
        self.any_rewards = any_rewards
        self.trading_rewards = trading_rewards
        self.total_rewards = total_rewards
        return

    def __str__(self):
        return f'{util.build_href("pair", self.name, self.name.ljust(12))}: <code>{util.formatPercent(self.total_rewards)} ({util.formatPercent(self.any_rewards)} ANY +' \
               f' {util.formatPercent(self.trading_rewards)} Fees)</code>'


class ILRecord:
    def __init__(self, period, il):
        self.period = period
        self.il = il
        return

    def __str__(self):
        return util.pad(self.period, '<') + ':' + util.pad(util.formatPercent(self.il, 3))


class NetRecord:
    def __init__(self, period, net):
        self.period = period
        self.net = net
        return

    def __str__(self):
        return util.pad(self.period, '<') + ':' + util.pad(util.formatPercent(self.net, 3))


class VOLRecord2:
    def __init__(self, name, vol):
        self.name = name
        self.vol = vol if vol is not None else 0
        return

    def __str__(self):
        return util.build_href('pair', self.name, self.name.ljust(12)) + f'<code>${self.vol:,.0f}</code>'


class TVLRecord:
    def __init__(self, name, tvl, price):
        self.token = name
        self.tvl = float(tvl)
        self.price = float(price)
        self.usd = self.tvl * self.price
        self.index = 0
        return

    def __str__(self):
        formatted_index = str(str(self.index) + '.').ljust(4)
        formatted_tvl = util.formatnumber(self.tvl).ljust(12)
        formatted_token = util.build_href("token", self.token, self.token.ljust(6))
        return f'{formatted_index}{formatted_tvl}{formatted_token}{util.formatcurrency(self.usd)}'


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
            sql = f'SELECT name, "any", trading, total FROM apy_all limit {top} ;'
        else:
            # sql = f'SELECT description, "any", trading, total FROM apy_lp WHERE name = \'{lp}\' ORDER BY day;'
            sql = f'SELECT name, "any", trading, total FROM apy_all ' + f" WHERE UPPER(name) LIKE UPPER('%{lp}%');"
            print('sql statement: ' + sql)
        cur.execute(sql)
        rows = cur.fetchall()
        result = []
        for row in rows:
            rec = APYRecord(row[0], row[1], row[2], row[3])
            result.append(rec)
        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        util.error()
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
            f'SELECT token, tvl, price FROM tvl_all ORDER BY tvl*price DESC')
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


def getVol():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(
            f'SELECT lp, vol FROM daily_xvol;')
        rows = cur.fetchall()
        result = []
        for row in rows:
            rec = VOLRecord2(row[0], row[1])
            result.append(rec)
        cur.close()
        return result
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return []
    finally:
        if conn is not None:
            conn.close()
