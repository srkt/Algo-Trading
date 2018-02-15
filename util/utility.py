import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd

from technical.screener import EmaReversion, Bollinger, StochasticOscillator, Macd, Vwap, Rsi, Screener


def py_mail(SUBJECT, BODY, TO, FROM):
    """With this function we send out our html email"""

    if (TO is None or FROM is None):
        raise Exception('invalid To and From addresses')

    TO_LIST = TO.split(",")

    # Create message container - the correct MIME type is multipart/alternative here!
    MESSAGE = MIMEMultipart('alternative')
    MESSAGE['subject'] = SUBJECT
    MESSAGE['To'] = TO
    MESSAGE['From'] = FROM
    MESSAGE.preamble = """
Your mail reader does not support the report format.
Please visit us <a href="http://www.mysite.com">online</a>!"""

    # Record the MIME type text/html.
    HTML_BODY = MIMEText(BODY, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    MESSAGE.attach(HTML_BODY)

    # The actual sending of the e-mail
    server = smtplib.SMTP('smtp.gmail.com:587')

    # Print debugging output when testing
    # if __name__ == "__main__":
    #     server.set_debuglevel(1)

    # Credentials (if needed) for sending the mail


    server.starttls()
    server.login(FROM, password)
    server.sendmail(FROM, TO_LIST, MESSAGE.as_string())
    server.quit()


def send_mail(msg):
    fromaddr = 'mytrademailer@gmail.com'
    toaddrs = 'obsoleteattribute@gmail.com'
    username = 'mytrademailer@gmail.com'
    password = 'Tr@deMailer'
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username, password)
    part = MIMEText(msg, 'html')
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()


def RunScreener(df, close_column='close', volume_column='volume'):
    if not isinstance(df, pd.DataFrame):
        raise Exception('Dataframe expected')

    # create screener
    screener = Screener(df)

    # Stratagies
    emrev = EmaReversion(df, close_column, 12, 21)
    bb = Bollinger(df, close_column, 14)
    sco = StochasticOscillator(df, 14, name=close_column)
    mcd = Macd(df, close_column)
    vwap = Vwap(df, close_column, vol_col_name=volume_column)
    rsi = Rsi(df, name=close_column)

    # add to screener
    screener.add_strategy(emrev)
    screener.add_strategy(bb)
    screener.add_strategy(sco)
    screener.add_strategy(rsi)
    screener.add_strategy(mcd)
    screener.add_strategy(vwap)

    results = screener.run()

    result_list = []

    for result in results:
        output = {
            'strategy': result.strategy_name,
            'signal': result.buy_sell,
            'weight': result.weight
        }
        result_list.append(output)
        # print('Strategy : ' + result.strategy_name + ', signal : ' + result.buy_sell + ', weight: ' + str(
        #     result.weight))

    # print('Current price:' + str(df[close_column][-1]))
    return result_list
