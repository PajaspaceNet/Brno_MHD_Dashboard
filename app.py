from flask import Flask, send_file, request
import pandas as pd
import folium
import matplotlib.pyplot as plt
import base64
from io import BytesIO

app = Flask(__name__)

# Načtení GTFS dat
stops = pd.read_csv("gtfs/stops.txt")
routes = pd.read_csv("gtfs/routes.txt")
trips = pd.read_csv("gtfs/trips.txt")
stop_times = pd.read_csv("gtfs/stop_times.txt")

# Vybrané linky
selected_lines = ['1', '44', '37', '26']
main_routes = routes[routes['route_short_name'].isin(selected_lines)]
trips_filtered = trips[trips['route_id'].isin(main_routes['route_id'])]
stop_times_filtered = stop_times[stop_times['trip_id'].isin(trips_filtered['trip_id'])]
stops_filtered = stops[stops['stop_id'].isin(stop_times_filtered['stop_id'])]

# Barevná paleta pro linky
colors = ['blue', 'red', 'green', 'orange']
line_map = {selected_lines[i]: colors[i] for i in range(len(selected_lines))}

# Spočítat počet spojů na každé zastávce pro normalizaci velikosti
stop_counts_list = []
for _, stop in stops_filtered.iterrows():
    trip_ids = stop_times_filtered[stop_times_filtered['stop_id']==stop['stop_id']]['trip_id']
    route_ids = trips_filtered[trips_filtered['trip_id'].isin(trip_ids)]['route_id'].unique()
    route_nums = main_routes[main_routes['route_id'].isin(route_ids)]['route_short_name'].values
    if len(route_nums) > 0:
        stop_counts_list.append(len(trip_ids))
    else:
        stop_counts_list.append(0)

min_radius = 4
max_radius = 12
min_count = min(stop_counts_list)
max_count = max(stop_counts_list)

@app.route("/")
def index():
    # Vytvoření mapy
    m = folium.Map(location=[49.1951, 16.6068], zoom_start=13)

    # Přidání zastávek s normalizovanou velikostí
    for idx, stop in stops_filtered.iterrows():
        trip_ids = stop_times_filtered[stop_times_filtered['stop_id']==stop['stop_id']]['trip_id']
        route_ids = trips_filtered[trips_filtered['trip_id'].isin(trip_ids)]['route_id'].unique()
        route_nums = main_routes[main_routes['route_id'].isin(route_ids)]['route_short_name'].values
        if len(route_nums) == 0:
            continue

        route_num = route_nums[0]
        stop_count = len(trip_ids)

        # Normalizovaný radius
        if max_count != min_count:
            radius = min_radius + (stop_count - min_count) / (max_count - min_count) * (max_radius - min_radius)
        else:
            radius = min_radius

        

        folium.CircleMarker(
            location=[stop['stop_lat'], stop['stop_lon']],
            radius=radius,
            color=color,
            fill=True,
            fill_opacity=0.8,
            popup=f"<b>{stop['stop_name']}</b><br>Linka {route_num}<br>Počet spojů: {stop_count}"
        ).add_to(m)

    # Graf top linek
    plt.figure(figsize=(5,3))
    main_routes['count'] = main_routes['route_id'].apply(
        lambda r: len(trips_filtered[trips_filtered['route_id']==r])
    )
    plt.bar(main_routes['route_short_name'], main_routes['count'],
            color=[line_map.get(str(x), 'black') for x in main_routes['route_short_name']])
    plt.title("Počet spojů vybraných linek")
    plt.xlabel("Linka")
    plt.ylabel("Počet spojů")

    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()
    img.seek(0)
    img_b64 = base64.b64encode(img.getvalue()).decode()

    html = f'<img src="data:image/png;base64,{img_b64}" width="400">'
    iframe = folium.IFrame(html, width=420, height=320)
    popup = folium.Popup(iframe, max_width=450)
    folium.Marker([49.2, 16.61], popup=popup, icon=folium.Icon(color='green', icon='info-sign')).add_to(m)

    m.save("mhd_brno_map.html")
    return send_file("mhd_brno_map.html")


@app.route("/stats")
def stats():
    line_filter = request.args.get("line")  # možnost filtrovat podle linky

    # Počet spojů na zastávce
    stop_counts = stop_times_filtered.groupby('stop_id')['trip_id'].count().reset_index()
    stop_counts = stop_counts.merge(stops[['stop_id','stop_name']], on='stop_id')
    stop_counts = stop_counts.rename(columns={'trip_id':'počet_spojů'})

    # Počet spojů na lince
    line_counts = trips_filtered.groupby('route_id')['trip_id'].count().reset_index()
    line_counts = line_counts.merge(routes[['route_id','route_short_name']], on='route_id')
    line_counts = line_counts.rename(columns={'trip_id':'počet_spojů'})

    if line_filter:
        # Filtrování zastávek jen pro vybranou linku
        filtered_route_ids = routes[routes['route_short_name']==line_filter]['route_id'].values
        filtered_trip_ids = trips[trips['route_id'].isin(filtered_route_ids)]['trip_id'].values
        stop_counts = stop_times[stop_times['trip_id'].isin(filtered_trip_ids)].groupby('stop_id')['trip_id'].count().reset_index()
        stop_counts = stop_counts.merge(stops[['stop_id','stop_name']], on='stop_id')
        stop_counts = stop_counts.rename(columns={'trip_id':'počet_spojů'})
        line_counts = line_counts[line_counts['route_short_name']==line_filter]

    # Top 5 zastávek
    top_stops = stop_counts.sort_values(by='počet_spojů', ascending=False).head(5)
    # Top 5 linek
    top_lines = line_counts.sort_values(by='počet_spojů', ascending=False).head(5)

    html = "<h2>Top zastávky podle počtu spojů</h2>"
    html += top_stops.to_html(index=False)
    html += "<h2>Top linky podle počtu spojů</h2>"
    html += top_lines.to_html(index=False)

    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
