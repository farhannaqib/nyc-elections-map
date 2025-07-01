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

def redistribute(data, name, perc):
    data["Zohran Kwame Mamdani"] += round(perc[0] * data[name])
    data["Andrew M. Cuomo"] += round(perc[1] * data[name])
    data["Inactive"] += round(perc[2] * data[name])
    data[name] = 0

def run_rcv(data):
    data["Inactive"] = 0

    redistribute(data, "Brad Lander", [0.7, 0.2, 0.1])
    redistribute(data, "Adrienne E. Adams", [0.5, 0.2, 0.3])
    redistribute(data, "Scott M. Stringer", [0.4, 0.3, 0.3])
    redistribute(data, "Zellnor Myrie", [0.2, 0.4, 0.4])
    redistribute(data, "Whitney R. Tilson", [0.9, 0.0, 0.1])

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
        if row_data[0] != 'Total': # We can recalculate total later, this is to ignore ED
            row_data.remove(row_data[1]) # % of votes reported, i dont rlly care about this
        votes.append(row_data)

    raw_data_dict = dict(zip([i for i in range(len(votes))], votes))
    columns = candidates
    columns.insert(0, name)
    data = pd.DataFrame.from_dict(raw_data_dict, orient='index', columns=columns)
    total = data.sum(axis=1, numeric_only=True)
    data["Winner"] = np.where(data.max(axis=1, numeric_only=True) != 0, data.idxmax(axis=1, numeric_only=True), "None")
    data["Total"] = total
    run_rcv(data)

    top_2 = data[data.columns[1:-3]].apply(lambda row: row.nlargest(2).values, axis=1)
    data["WinnerPrc"] = (top_2.apply(lambda row: row[0] - row[1]) / data["Total"]).round(4)
    return data

def merge_with_geojson(data: pd.DataFrame, shapefile_path: str, merge_key: str, output_path: str):
    geo = gpd.read_file(shapefile_path).to_crs(epsg=4326)
    geo_data = geo.merge(data, on=merge_key)
    geo_data.to_file(output_path, driver='GeoJSON')

def create_borough_geojson(url: str):
    data = create_data(url, "BoroName")
    merge_with_geojson(data, "data/nybb_25b/nybb.dbf", "BoroName", "data/boroughs.geojson")

def create_ad_geojson(url: str):
    data = create_data(url, "AssemDist")
    merge_with_geojson(data, "data/nyad_25b/nyad.dbf", "AssemDist", "data/ad.geojson")

def create_ed_geojson():
    data = pd.DataFrame()
    for ad in range(23, 88):
        url = f"https://enr.boenyc.gov/CD26916AD{ad}0.html"
        data = pd.concat([data, create_data(url, "ElectDist", ad)])
        print(url)
    print(data)
    print(data.sum(axis=0, numeric_only=True))

    merge_with_geojson(data, "data/nyed_25b/nyed.dbf", "ElectDist", "data/ed.geojson")


borough_url = "https://enr.boenyc.gov/CD26916ADI0.html"
ad_url = "https://enr.boenyc.gov/CD26916AD0.html"


create_borough_geojson(borough_url)
create_ad_geojson(ad_url)
create_ed_geojson()