import pandas as pd
from pandas import DataFrame


def do_thing_with_csvs(resale_csv, carrier_csv):
    with open(resale_csv) as resale_plans, open(carrier_csv) as carrier_plans:
        # (1)
        # Datoteku sa svim povezanim podacima i poljima:
        # MDN, Resale Plan, Sprint Plan i SOCs.
        resale: DataFrame = pd.read_csv(resale_plans)
        carrier: DataFrame = pd.read_csv(carrier_plans)
        carrier_drop: DataFrame = carrier.dropna(axis=1)
        merged: DataFrame = resale.merge(carrier_drop, on='mdn')
        columns: list = ['mdn', 'resale_plan', 'sprint_plan', 'socs']
        merged.to_csv('output.csv', index=False, columns=columns)

        # (2)
        # Datoteku sa povezanim podacima i poljima:
        # MDN, Resale Plan, Sprint Plan i poljem 'LTE SOC'
        # cija vrijednost se postavlja  na vrijednost  'Y' ili 'N', ovisno da li
        # se u polju SOCs u ulaznoj datoteci nalazi vrijednost 'DSMLTESOC'.
        grouped_csv: DataFrame = resale.groupby(['resale_plan']).count()
        grouped_csv.to_csv('first_file.csv')

        # (3)
        # Datoteku sa razdiobom pretplatnika po resale planu
        # tj.koliko pretplatnika se nalazi na kojem resale planu.
        data: DataFrame = pd.read_csv('output.csv')
        data.dropna(inplace=True)
        data_dict: dict = data.to_dict()
        new_list: list = list(data_dict.values())
        socs_dict: dict = new_list[3]
        for k, v in socs_dict.items():
            if 'DSMLTESOC' in v:
                socs_dict[k]: str = 'Y'
            else:
                socs_dict[k]: str = 'N'

        df: DataFrame = pd.DataFrame(data_dict)
        df.to_csv('my_file.csv', index=False, header=True)


do_thing_with_csvs(resale_csv='resale-plans.csv', carrier_csv='carrier-plans.csv')

