import requests, time, math

api_token = '2003733580:AAH7tZzMCvsqM6OaMmUPdBf1qpi54IouMnU'
chat_id = "-4221805882"

api_url = 'https://api.telegram.org/bot' + api_token

def main():
  wallets = []
  while True:
    res = requests.get("https://toncenter.com/api/v3/jetton/transfers?direction=both&limit=128&offset=0&sort=desc")
    if res.status_code == 200:
      for tx in res.json()["jetton_transfers"]:
        wallet = tx["source"]
        if wallet not in wallets:
          res = requests.get("https://toncenter.com/api/v3/wallet?address=" + wallet)
          if res.status_code == 200:
            balance = int(res.json()["balance"])
            if balance > 5000000000 and balance < 1000000000000:
              res = requests.get("https://tonapi.io/v2/accounts/" + wallet + "/jettons?currencies=usd")
              if res.status_code == 200:
                try:
                  json = res.json()
                  t_worth = (balance / 1000000000) * 5.50
                  j_worth = 0
                  for j in json["balances"]:
                    j_worth += (int(j["balance"]) / math.pow(10, j["jetton"]["decimals"])) * j["price"]["prices"]["USD"]
                  worth = round(t_worth + j_worth, 2)
                  if worth > 125:
                    text = "`"+wallet+"`\n💰 $"+worth, "USD"
                    res = requests.get(api_url + '/sendMessage?parse_mode=html&disable_web_page_preview=true&chat_id=' + chat_id + '&text=' + text)
                    print("s", res.status_code, res.json())
                    # print("$" + str(round(worth, 2)), "USD :", wallet)
                except Exception as e:
                  print(e)
              else:
                print(res.status_code)
          elif res.status_code == 409:
            pass
          else:
            print(res.status_code)
          time.sleep(3)
        wallets.append(wallet)
    else:
      print(res.status_code)
    time.sleep(3)

if __name__ == "__main__":
  main()

