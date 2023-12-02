"""Code to get the following data: 

1. Walkability data for each state (at city level)

"""

import pandas as pd
import requests
from io import StringIO
from selenium import webdriver
from selenium.webdriver.common.by import By

# WALKABILITY DATA
list_us_abbv = (
    pd.read_html("https://www.ssa.gov/international/coc-docs/states.html")[0][1]
).to_list()

df_walk = pd.DataFrame()
for st in list_us_abbv:
    print(st)
    try:
        temp = pd.read_html(f"https://www.walkscore.com/{st}")[0]
        temp["State"] = st
        df_walk = pd.concat([temp, df_walk])
    except:
        pass

# excludes American Samoa (AS)
assert df_walk["State"].nunique() == 51
df_walk.drop(["Transit Score"], axis=1).to_csv("./data/walkability.csv")

# GET KFF data
data = pd.DataFrame()
start_y = 2002
end_y = 2022

cur_tf = {
    k: v
    for k, v in zip(
        list(range(start_y - start_y, (end_y - start_y) + 1)),
        list(range(start_y, end_y + 1))[::-1],
    )
}

def get_kff(url):
    driver = webdriver.Chrome()
    driver.get(url)
    content = driver.find_elements(By.CSS_SELECTOR, ".ag-root.ag-font-style.ag-no-scrolls")
    table = content[0].text.split('\n')

    k, v = [], []
    for idx, el in enumerate(table):
        if idx % 2 == 0:
            k.append(el)
        elif idx % 2 == 1:
            v.append(el)
    return k, v

for i in cur_tf.items():
    avg_monthly_url = f"https://www.kff.org/other/state-indicator/avg-monthly-snap-benefits/?currentTimeframe={i[0]}&print=true&sortModel=%7B%22colId%22:%22Location%22,%22sort%22:%22asc%22%7D"
    participation_url = f"https://www.kff.org/other/state-indicator/avg-monthly-participation/?currentTimeframe={i[0]}&print=true&sortModel=%7B%22colId%22:%22Location%22,%22sort%22:%22asc%22%7D"
    tot_benefits_url = f"https://www.kff.org/other/state-indicator/total-snap-program-benefits/?currentTimeframe={i[0]}&print=true&sortModel=%7B%22colId%22:%22Location%22,%22sort%22:%22asc%22%7D"
    
    avg_k, avg_v = get_kff(avg_monthly_url)
    part_k, part_v = get_kff(participation_url)
    tot_ben_k, tot_ben_v = get_kff(tot_benefits_url)

    data = pd.concat([data, pd.DataFrame({avg_k[0]: avg_k[1:], 
                                          avg_v[0]:avg_v[1:], 
                                          part_k[0]: part_k[1:], 
                                          part_v[0]:part_v[1:], 
                                          tot_ben_k[0]: tot_ben_k[1:], 
                                          tot_ben_v[0]:tot_ben_v[1:], 
                                          'year':i[1]})])

data.to_csv("./SNAO_data_raw.csv")