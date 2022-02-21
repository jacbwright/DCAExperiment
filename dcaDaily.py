"""
This script runs daily at 4PM CST. Tweets a real-time update of the DCA Experiment portfolio
on the @JacbWright Twitter account. Requires credentials for Twitter API and GCP.

Hosted: https://www.pythonanywhere.com/
Google Sheet: https://docs.google.com/spreadsheets/d/1k_xaCGcDtKTTZ1B9cjeUWxv3PxN5jLC1jSWFybYcvhc/edit?usp=sharing
"""
from oauth2client.service_account import ServiceAccountCredentials
from yahoo_fin import stock_info as yf
import gspread
import tweepy
import json

# Retrieve the credentials for accessing GCP
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
gcpCreds = ServiceAccountCredentials.from_json_keyfile_name("GCPCredentials.json", scope)
client = gspread.authorize(gcpCreds)

# Use GCP to retrieve the DCA portfolio Google Sheet
dcaSheet = client.open("DCA_Crypto_Tracker").sheet1
dcaData = dcaSheet.get_all_records()

# Retrieve the credentials for accessing the Twitter API
file = open('TwitterCredentials.json')
twitterCreds = json.load(file)
api_key = twitterCreds['api_key']
api_key_secret = twitterCreds['api_key_secret']
access_token = twitterCreds['access_token']
access_token_secret = twitterCreds['access_token_secret']

# Retrieve live BTC price, retrieve BTC portfolio, calculate gains
btcCurrent = float(yf.get_live_price("btc-usd"))
btcPurchase = float(dcaSheet.cell(10, 4).value[1:9])
btcShares = float(dcaSheet.cell(10, 3).value[1:9])
btcTotalCalc = btcShares * btcCurrent
btcGainCalc = btcTotalCalc - btcPurchase
btcPercentCalc = btcGainCalc / btcPurchase
btcTotal = "{:.2f}".format(btcTotalCalc)
btcGain = "{:.2f}".format(btcGainCalc)
btcPercent = "{:.2%}".format(btcPercentCalc)

# Retrieve live ETH price, retrieve ETH portfolio, calculate gains
ethCurrent = float(yf.get_live_price("eth-usd"))
ethPurchase = float(dcaSheet.cell(11, 4).value[1:9])
ethShares = float(dcaSheet.cell(11, 3).value[1:9])
ethTotalCalc = ethShares * ethCurrent
ethGainCalc = ethTotalCalc - ethPurchase
ethPercentCalc = ethGainCalc / ethPurchase
ethTotal = "{:.2f}".format(ethTotalCalc)
ethGain = "{:.2f}".format(ethGainCalc)
ethPercent = "{:.2%}".format(ethPercentCalc)

# Retrieve live ADA price, retrieve ADA portfolio, calculate gains
adaCurrent = float(yf.get_live_price("ada-usd"))
adaPurchase = float(dcaSheet.cell(12, 4).value[1:9])
adaShares = float(dcaSheet.cell(12, 3).value[:9])
adaTotalCalc = adaShares * adaCurrent
adaGainCalc = adaTotalCalc - adaPurchase
adaPercentCalc = adaGainCalc / adaPurchase
adaTotal = "{:.2f}".format(adaTotalCalc)
adaGain = "{:.2f}".format(adaGainCalc)
adaPercent = "{:.2%}".format(adaPercentCalc)

# Retrieve live MATIC price, retrieve MATIC portfolio, calculate gains
maticCurrent = float(yf.get_live_price("matic-usd"))
maticPurchase = float(dcaSheet.cell(13, 4).value[1:9])
maticShares = float(dcaSheet.cell(13, 3).value[:9])
maticTotalCalc = maticShares * maticCurrent
maticGainCalc = maticTotalCalc - maticPurchase
maticPercentCalc = maticGainCalc / maticPurchase
maticTotal = "{:.2f}".format(maticTotalCalc)
maticGain = "{:.2f}".format(maticGainCalc)
maticPercent = "{:.2%}".format(maticPercentCalc)

# Calculate total portfolio gains
totalTotalCalc = btcTotalCalc + ethTotalCalc + adaTotalCalc + maticTotalCalc
totalGainCalc = btcGainCalc + ethGainCalc + adaGainCalc + maticGainCalc
totalPercentCalc = totalGainCalc / (btcPurchase + ethPurchase + adaPurchase + maticPurchase)
totalTotal = "{:.2f}".format(totalTotalCalc)
totalGain = "{:.2f}".format(totalGainCalc)
totalPercent = "{:.2%}".format(totalPercentCalc)

# Retrieve DCA experiment details from Google sheet
dcaWeek = dcaSheet.cell(2, 8).value
dcaAmount = dcaSheet.cell(3, 8).value
dcaTotal = dcaSheet.cell(4, 8).value

# Determine which currency is the top performer
topCoinList = [btcGainCalc, ethGainCalc, adaGainCalc, maticGainCalc]
topCoinCalc = max(topCoinList)
if topCoinCalc == btcGainCalc:
    topCoin = "BTC"
if topCoinCalc == ethGainCalc:
    topCoin = "ETH"
if topCoinCalc == adaGainCalc:
    topCoin = "ADA"
if topCoinCalc == maticGainCalc:
    topCoin = "MATIC"

# Handle negative numbers for pretty formatting
negativeCheck = (totalGain, totalPercent, btcGain, btcPercent, ethGain, ethPercent, adaGain, adaPercent, maticGain, maticPercent)
negativeList = list(negativeCheck)
negativeListCounter = len(negativeCheck) - 1
while negativeListCounter != -1:
    if '-' not in negativeCheck[negativeListCounter]:
        negativeList[negativeListCounter] = "+" + negativeList[negativeListCounter]
    negativeListCounter -= 1

# Format tweet using the calculations above
tweet = ("DCA EXPERIMENT - WEEK " + dcaWeek +"\n"
         "$" + dcaTotal +" TOTAL / $" + dcaAmount +" PER COIN\n\n"
         "TOTAL: $" + totalTotal +" (" + negativeList[0] + " / " + negativeList[1] + ")\n"
         "$BTC $" + btcTotal +" (" + negativeList[2] + " / " + negativeList[3] + ")\n"
         "$ETH $" + ethTotal +" (" + negativeList[4] + " / " + negativeList[5] + ")\n"
         "$ADA $" + adaTotal +" (" + negativeList[6] + " / " + negativeList[7] + ")\n"
         "$MATIC $" + maticTotal +" (" + negativeList[8] + " / " + negativeList[9] + ")\n\n"
         "\U0001F451 $" + topCoin + "")

# Send tweet using the Twitter API
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
api.update_status(status=tweet)
