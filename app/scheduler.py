import schedule
import time

from app.crypto import generate_crypto_alerts
from app.equities import generate_stock_alerts

crypto_duration = 0.1  # 15  # in minutes
stock_duration = 0.1  # 12 * 60  # in minutes

schedule.every(crypto_duration).minutes.do(generate_crypto_alerts)
schedule.every(stock_duration).minutes.do(generate_stock_alerts)

while True:
    schedule.run_pending()
    time.sleep((stock_duration if crypto_duration > stock_duration else crypto_duration) * 60)

# schedule.every(10).minutes.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).days.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
