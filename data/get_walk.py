"""Code to get walkability data for each state (at city level)"""

import pandas as pd

list_us_abbv = pd.read_html("https://www.ssa.gov/international/coc-docs/states.html")[0][1].to_list()

df_walk = pd.DataFrame()
for st in list_us_abbv:
    print(st)
    try:
        temp = pd.read_html(f'https://www.walkscore.com/{st}')[0]
        temp['State'] = st
        df_walk = pd.concat([temp, df_walk])
    except:
        pass

# excludes American Samoa (AS)
assert df_walk['State'].nunique() == 51 

df_walk.drop(['Transit Score'], axis=1).to_csv("./data/walkability.csv")

