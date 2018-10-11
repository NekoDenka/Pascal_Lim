import requests
from bs4 import BeautifulSoup
import pandas as pd

list_url = ["https://www.reuters.com/finance/stocks/financial-highlights/LVMH.PA",
            "https://www.reuters.com/finance/stocks/financial-highlights/AIR.PA",
            "https://www.reuters.com/finance/stocks/financial-highlights/DANO.PA"]

def get_all_data(list_url):
    df_quarter_sales = pd.DataFrame()
    df_dividend_yield = df_quarter_sales = pd.DataFrame()
    df_other_data = pd.DataFrame()
    for url in list_url:
        df_quarter_sales = df_quarter_sales.append(get_december_2018_quarter_sales(url))
        df_other_data = df_other_data.append(get_other_data(url))
        df_dividend_yield = df_dividend_yield.append(get_dividend_yield(url))
    print(df_quarter_sales.set_index('Company'))
    print(df_other_data.set_index('Company'))
    print(df_dividend_yield.set_index('Company'))

def _handle_request_result_and_build_soup(request_result):
    if request_result.status_code == 200:
        html_doc = request_result.content
        soup = BeautifulSoup(html_doc, "html.parser")
        return soup

def get_december_2018_quarter_sales(page_url):
    res = requests.get(page_url)
    soup = _handle_request_result_and_build_soup(res)
    temp = soup.find(text="SALES (in millions)")
    quarter_text = temp.parent.parent.findNext("tr").select("td.data")
    data = {}
    df = pd.DataFrame()
    titre = soup.select_one("div#sectionTitle h1").text
    data['Company'] = titre[:5]
    data['# of Estimates'] = quarter_text[0].string
    data['Mean Sales'] = quarter_text[1].string
    data["High Sales"] = quarter_text[2].string
    data["Low Sales"] = quarter_text[3].string
    data["1 Year Ago Sales"] = quarter_text[4].string.replace("--", "")
    df = df.append([data])
    return df

def get_other_data(page_url):
    res = requests.get(page_url)
    soup = _handle_request_result_and_build_soup(res)
    data = {}
    df = pd.DataFrame()
    titre = soup.select_one("div#sectionTitle h1").text
    stock_price = soup.find("span", {"class", "nasdaqChangeHeader"}).findNext('span').text
    stock_price_newformat = stock_price.strip("\n").strip("\t")
    change_percent = soup.find("span", {"class", "valueContentPercent"}).span.text
    change_percent_newformat = change_percent.strip("\n").strip("\t").strip(" ")[1:-8]
    temp = soup.find(text="% Shares Owned:")
    shares_owned = temp.parent.parent.findNext("td").text
    shares_owned_newformat = shares_owned[:-2]
    data['Company'] = titre[:5]
    data['Stock Price (Eur)'] = stock_price_newformat
    data['Change Stock Price (%)'] = change_percent_newformat
    data['Shares Owned (%)'] = shares_owned_newformat
    df = df.append([data])
    return df

def get_dividend_yield(page_url):
    res = requests.get(page_url)
    soup = _handle_request_result_and_build_soup(res)
    data = {}
    df = pd.DataFrame()
    titre = soup.select_one("div#sectionTitle h1").text
    temp = soup.find(text="Dividend Yield")
    data['Company'] = titre[:5]
    data['Dividend Yield Company'] = temp.findNext("td").text
    data['Dividend Yield industry'] = temp.findNext("td").findNext("td").text
    data["Dividend Yield sector"] = temp.findNext("td").findNext("td").findNext("td").text
    df = df.append([data])
    return df

get_all_data(list_url)