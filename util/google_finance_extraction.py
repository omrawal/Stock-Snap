from bs4 import BeautifulSoup
import requests
import json

google_quote_base_url = "https://www.google.com/finance/quote/"
company_symbol = "RELIANCE"  # # "ITC" "RAYMOND" "NIFTY_IT"
exchange_symbol = "NSE" #"INDEXNSE"  #
quote_lpt_class = "YMlKec fxKbKc"
description_class = "zzDege"
prev_close_class = "gyFHrc"
CURRENCY_SYMBOLS = {"$": "USD", "₹": "INR"}

google_quote_fetch_url = google_quote_base_url + f"{company_symbol}:{exchange_symbol}"

response = requests.get(google_quote_fetch_url)
soup = BeautifulSoup(response.text, "html.parser")
# with open ('RELIANCE.html','w+', encoding='utf-8') as file:
#     file.write(str(soup))
quote_ltp = ""
content = soup.find(class_=quote_lpt_class)
if content is not None:
    quote_ltp = content.text
print(quote_ltp)
# <div class="gyFHrc"><span data-is-tooltip-wrapper="true"><div aria-describedby="i14" class="mfs7Fc" data-tooltip-anchor-boundary-type="2" data-tooltip-x-position="2" jsaction="mouseenter:tfO1Yc; focus:AHmuwe; blur:O22p3e; mouseleave:JywGue; touchstart:p6p2H; touchend:yfqBxc;mlnRJb:fLiPzd;" jscontroller="e2jnoe">Previous close</div><div aria-hidden="true" class="EY8ABd-OWXEXe-TAWMXe" id="i14" role="tooltip">The last closing price</div></span><div class="P6K39c">₹2,086.20</div></div>
# <div class="gyFHrc"><span data-is-tooltip-wrapper="true"><div aria-describedby="i14" class="mfs7Fc" data-tooltip-anchor-boundary-type="2" data-tooltip-x-position="2" jsaction="mouseenter:tfO1Yc; focus:AHmuwe; blur:O22p3e; mouseleave:JywGue; touchstart:p6p2H; touchend:yfqBxc;mlnRJb:fLiPzd;" jscontroller="e2jnoe">Previous close</div><div aria-hidden="true" class="EY8ABd-OWXEXe-TAWMXe" id="i14" role="tooltip">The last closing price</div></span><div class="P6K39c">₹2,984.80</div></div>
previous_close_content = soup.find_all(class_=prev_close_class)[0]
previous_close_tag = BeautifulSoup(str(previous_close_content), "html.parser")
previous_close_value = previous_close_tag.find(class_="P6K39c")
print(previous_close_value)
print(previous_close_value.text)


def get_currency_and_symbol(value_string)->tuple:
    currency_symbol = value_string[0]
    if currency_symbol in CURRENCY_SYMBOLS:
        return (CURRENCY_SYMBOLS.get(currency_symbol,None),currency_symbol)
    else:
        return (None,None)

def get_ltp_string(soup,quote_lpt_class="YMlKec fxKbKc") -> str:
    ltp_content = soup.find(class_=quote_lpt_class)
    if ltp_content is not None:
        quote_ltp = ""
        quote_ltp = ltp_content.text.replace(",", "")
        currency_symbol = quote_ltp[0]
        # print(currency_symbol)
        return quote_ltp
    else:
        print("LTP content is None")
        return None

def get_previous_close_string(soup,prev_close_class="gyFHrc"):
    previous_close_content = soup.find_all(class_=prev_close_class)[0]
    if previous_close_content is not None:
        previous_close_tag = BeautifulSoup(str(previous_close_content), "html.parser")
        previous_close_value = previous_close_tag.find(class_="P6K39c").text.replace(",", "")
        return previous_close_value
    else:
        print("Previous close content is None")
        return None


def get_quotes_of_all_500_nse_companies():
    with open("../assets/nse_500_companies_symbols.json", "r") as symbols:
        company_symbol_list = json.load(symbols)

    for company_symbol in company_symbol_list:
        print("checking for company_symbol:", company_symbol)
        # try:
        google_quote_fetch_url = google_quote_base_url + f"{company_symbol}:{exchange_symbol}"
        response = requests.get(google_quote_fetch_url)
        soup = BeautifulSoup(response.text, "html.parser")
        print("Get ltp is ->",get_ltp_string(soup))
        quote_ltp = ""
        desc = ""
        currency = ""
        currency_symbol = ""
        percentage_change = ""
        change_amount = ""
        change_type = "UP"  # UP / DOWN

        ltp_content = soup.find(class_=quote_lpt_class)
        desc_content = soup.find(class_=description_class)
        if ltp_content is not None:
            quote_ltp_str_value = get_ltp_string(soup)
            ltp_currency,ltp_currency_symbol = get_currency_and_symbol(quote_ltp_str_value)
            print("LTP symbol ",ltp_currency,ltp_currency_symbol)
            if ltp_currency is not None or ltp_currency_symbol is not None:
                quote_ltp = quote_ltp_str_value[1:]
            
            previous_close_str_value = get_previous_close_string(soup)
            previous_close_currency,previous_close_currency_symbol = get_currency_and_symbol(previous_close_str_value)
            print("previous_close symbol ",previous_close_currency,previous_close_currency_symbol)
            if previous_close_currency is not None or previous_close_currency_symbol is not None:
                previous_close_value = previous_close_str_value[1:]

            change_amount = float(quote_ltp) - float(previous_close_value)

            percentage_change = (abs(float(quote_ltp) - float(previous_close_value)) * 100) / float(previous_close_value)
            if change_amount < 0:
                change_type = "DOWN"
        else:
            print("ltp_content is none",)

        if desc_content is not None:
            desc = desc_content.text

        # print("change_amount", change_amount)
        # print(quote_ltp)
        print({company_symbol: {'ltp': quote_ltp, 'desc': desc,"previous_close": previous_close_value,
                                "currency": ltp_currency, "percentage_change": str(percentage_change) + str("%"),
                                "change_amount": change_amount, "currency_symbol": currency_symbol,
                                "change_type": change_type}})
        # except Exception as e:
        #     print(f"Exception {e} occurred for company symbol {company_symbol}")

get_quotes_of_all_500_nse_companies()
