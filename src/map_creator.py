import folium
import pandas as pd

class Map:
    """
    Uma classe dedicada a criar e popular o mapa Folium com dados FWD.
    """
    def __init__(self, street_data, analysis_type, traffic_level):
        """
        Inicializa o criador do mapa com os dados e filtros necessários.
        """
        self.street_data = street_data
        self.analysis_type = analysis_type
        self.traffic_level = traffic_level
        self.m = None

    def _plot_map(self):
        """Método privado para criar o mapa base e centralizá-lo."""
        all_dfs = [df for df in self.street_data.values() if not df.empty]
        if all_dfs:
            all_lats = pd.concat([df['Latitude'] for df in all_dfs]).mean()
            all_longs = pd.concat([df['Longitude'] for df in all_dfs]).mean()
            center_coord = [all_lats, all_longs]
        else:
            center_coord = [-2.53, -44.30] 

        self.m = folium.Map(location=center_coord, zoom_start=17, tiles="CartoDB positron")
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri', name='Satélite', overlay=False, control=True
        ).add_to(self.m)

    def _plot_points(self):
        """Método privado para desenhar os pontos de dados no mapa."""
        if self.m is None: self._plot_map()
            
        analysis_to_column_map = {
            'D0': 'D1', 'RAIO': 'RAIO', 'SCI': 'SCI', 'BDI': 'BDI', 'BCI': 'BCI'
        }
        analysis_col = f'ANÁLISE_{self.analysis_type}_{self.traffic_level}'
        value_col_name = analysis_to_column_map.get(self.analysis_type, self.analysis_type)

        for lane_name, df in self.street_data.items():
            fg = folium.FeatureGroup(name=lane_name, show=True)
            for _, row in df.iterrows():
                if analysis_col in row and value_col_name in row:
                    color = "cyan" if row[analysis_col] == "Aprovado" else "red"
                    popup_text = f"<b>{self.analysis_type}</b>: {row[value_col_name]:.2f}<br><b>Status</b>: {row[analysis_col]}"
                    
                    folium.CircleMarker(
                        location=[row['Latitude'], row['Longitude']],
                        radius=6, color=color, fill=True, fill_color=color, fill_opacity=0.8,
                        popup=folium.Popup(popup_text, max_width=200)
                    ).add_to(fg)
            fg.add_to(self.m)
        
        folium.LayerControl().add_to(self.m)

    def plot(self):
        """Método público que orquestra a criação do mapa e o retorna."""
        self._plot_map()
        self._plot_points()
        return self.m