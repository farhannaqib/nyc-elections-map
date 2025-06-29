mapboxgl.accessToken = ACCESS_TOKEN;
var map = new mapboxgl.Map({
    container: 'map', // container ID
    style: 'mapbox://styles/farhannaqib/cmcdy3hd6002s01s78lkd2jiv', // style URL
    center: [-74, 40.70], // starting position [lng, lat]
    zoom: 9.5, // starting zoom
    maxZoom: 17,
    minZoom: 8,
});

map.on("load", () => {
    map.addLayer(
        {
            id: "nyc_mayor_elections_outline",
            type: "line",
            source: {
                type: "geojson",
                data: "data/boroughs.geojson",
            },
            maxzoom: 9,
            paint: {
                "line-color": "#ffffff",
                "line-width": 0.5,
            },
        },
        "waterway-label"
    );
    map.addLayer(
        {
            id: "nyc_mayor_elections",
            type: "fill",
            source: {
                type: "geojson",
                data: "data/boroughs.geojson",
            },
            maxzoom: 9,
            paint: {
                "fill-color": [
                    "match",
                    ["get", "Winner"],
                    "Andrew M. Cuomo", "#15467c",
                    "Zohran Kwame Mamdani", "#ffaa03",
                    "Brad Lander", "#078207",
                    "#ffffff",
                ],
                "fill-outline-color": "#ffffff",
                "fill-opacity": [
                    "step",
                    ["get", "WinnerPrc"],
                    0.3,
                    0.05,
                    0.5,
                    0.10,
                    0.7,
                    0.2,
                    0.9,
                ],
            },
        },
        "nyc_mayor_elections_outline"
    );
    map.addLayer(
        {
            id: "ad_elections_outline",
            type: "line",
            source: {
                type: "geojson",
                data: "data/ad.geojson",
            },
            minzoom: 9,
            maxzoom: 9.5,
            paint: {
                "line-color": "#ffffff",
                "line-width": 0.25,
            },
        },
        "nyc_mayor_elections"
    );
    map.addLayer(
        {
            id: "ad_elections",
            type: "fill",
            source: {
                type: "geojson",
                data: "data/ad.geojson",
            },
            minzoom: 9,
            maxzoom: 9.5,
            paint: {
                "fill-color": [
                    "match",
                    ["get", "Winner"],
                    "Andrew M. Cuomo", "#15467c",
                    "Zohran Kwame Mamdani", "#ffaa03",
                    "Brad Lander", "#078207",
                    "#ffffff",
                ],
                "fill-outline-color": "#ffffff",
                "fill-opacity": [
                    "step",
                    ["get", "WinnerPrc"],
                    0.3,
                    0.05,
                    0.5,
                    0.10,
                    0.7,
                    0.6,
                    0.9,
                ],
            },
        },
        "ad_elections_outline"
    );
    map.addLayer(
        {
            id: "ed_elections_outline",
            type: "line",
            source: {
                type: "geojson",
                data: "data/ed.geojson",
            },
            minzoom: 9.5,
            paint: {
                "line-color": "#ffffff",
                "line-width": 0.1,
            },
        },
        "ad_elections"
    );
    map.addLayer(
        {
            id: "ed_elections",
            type: "fill",
            source: {
                type: "geojson",
                data: "data/ed.geojson",
            },
            minzoom: 9.5,
            paint: {
                "fill-color": [
                    "match",
                    ["get", "Winner"],
                    "Andrew M. Cuomo", "#15467c",
                    "Zohran Kwame Mamdani", "#ffaa03",
                    "Brad Lander", "#078207",
                    "#ffffff",
                ],
                "fill-outline-color": "#ffffff",
                "fill-opacity": [
                    "step",
                    ["get", "WinnerPrc"],
                    0.3,
                    0.05,
                    0.5,
                    0.10,
                    0.7,
                    0.6,
                    0.9,
                ],
            },
        },
        "ed_elections_outline"
    );
});