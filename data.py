import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import geopandas as gpd

def clean(cell_text: str, ad=-1):
    cell_text = cell_text.strip()
    if cell_text.isnumeric():
        cell_text = int(cell_text)
    elif cell_text == "New York":
        cell_text = "Manhattan"
    elif cell_text == "Kings":
        cell_text = "Brooklyn"
    elif cell_text == "Richmond":
        cell_text = "Staten Island"
    elif cell_text.startswith("AD"):
        cell_text = int(cell_text[-2:])
    elif cell_text.startswith("ED"):
        cell_text = 1000 * ad + int(cell_text[-2:])
    return cell_text    

def create_data(url: str, name: str, ad=-1) -> pd.DataFrame:
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.prettify())

    table = soup.find('table', class_='underline')
    rows = table.find_all('tr')
    candidates = [clean(cell.text, ad) for cell in rows[0].find_all('td') if cell.text != '\xa0'][0:12]
    rows.remove(rows[0]) # candidates
    rows.remove(rows[0]) # party affiliation
    votes = []
    for row in rows:
        row_data = [clean(cell.text, ad) for cell in row.find_all('td') if cell.text != '\xa0']
        if row_data[0] != 'Total':
            row_data.remove(row_data[1]) # % of votes reported, i dont rlly care about this
        votes.append(row_data)

    raw_data_dict = dict(zip([i for i in range(len(votes))], votes))
    columns = candidates
    columns.insert(0, name)
    data = pd.DataFrame.from_dict(raw_data_dict, orient='index', columns=columns)
    # data["Zohran Kwame Mamdani"] += (0.6 * data["Brad Lander"] + 0.5 * data["Adrienne E. Adams"])
    # data["Andrew M. Cuomo"] += (0.2 * data["Brad Lander"] + 0.2 * data["Adrienne E. Adams"] + data["Whitney R. Tilson"])
    # data["Brad Lander"] = 0
    # data["Adrienne E. Adams"] = 0
    # data["Whitney R. Tilson"] = 0
    data["Winner"] = np.where(data.max(axis=1, numeric_only=True) != 0, data.idxmax(axis=1, numeric_only=True), "None")
    data["Total"] = data.sum(axis=1, numeric_only=True)
    top_2 = data[data.columns[1:-2]].apply(lambda row: row.nlargest(2).values, axis=1)
    data["WinnerPrc"] = (top_2.apply(lambda row: row[0] - row[1]) / data["Total"]).round(4)
    return data

def create_borough_geojson(url: str):
    data = create_data(url, "BoroName")

    boroughs = gpd.read_file("nybb_25b/nybb.dbf")
    boroughs = boroughs.to_crs(epsg=4326)
    borough_data = boroughs.merge(data, on="BoroName")
    # print(borough_data)

    borough_data.to_file('data/boroughs.geojson', driver='GeoJSON')

def create_ad_geojson(url: str):
    data = create_data(url, "AssemDist")

    ad = gpd.read_file("nyad_25b/nyad.dbf")
    ad = ad.to_crs(epsg=4326)
    ad_data = ad.merge(data, on="AssemDist")
    # print(ad_data)

    ad_data.to_file('data/ad.geojson', driver='GeoJSON')

def create_ed_geojson():
    data = pd.DataFrame()
    for ad in range(23, 88):
        url = f"https://enr.boenyc.gov/CD26916AD{ad}0.html"
        data = pd.concat([data, create_data(url, "ElectDist", ad)])
        print(url)
    print(data)

    ed = gpd.read_file("nyed_25b/nyed.dbf")
    ed = ed.to_crs(epsg=4326)
    ed_data = ed.merge(data, on="ElectDist")
    print(ed_data)

    ed_data.to_file('data/ed.geojson', driver='GeoJSON')


borough_url = "https://enr.boenyc.gov/CD26916ADI0.html"
ad_url = "https://enr.boenyc.gov/CD26916AD0.html"


create_borough_geojson(borough_url)
create_ad_geojson(ad_url)
create_ed_geojson()