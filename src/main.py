import datetime
import os
import smtplib
import time
from email.message import EmailMessage

import yfinance as yf
from pandas_datareader import data as pdr

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")


def run_notifier():
    ticker = "AAPL"

    email_msg = EmailMessage()
    email_msg["Subject"] = f"Stock Alert: {ticker}"
    email_msg["From"] = EMAIL_ADDRESS
    email_msg["To"] = EMAIL_ADDRESS
    yf.pdr_override()

    target_price = 120
    start = datetime.datetime(2020, 1, 1)

    while True:
        now = datetime.datetime.now()
        df = pdr.get_data_yahoo(ticker, start, now)
        current_price = df["Adj Close"][-1]
        print(f"[{now}] {ticker} => {current_price}")
        if current_price < target_price:
            email_msg.set_content(
                f"{ticker} is below the target price of {target_price}, now trading at {current_price}"
            )
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(email_msg)
                print(f"Email sent at {now}")
                break
        time.sleep(10)


if __name__ == "__main__":
    run_notifier()
