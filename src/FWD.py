# FWD.py
# Responsabilidade: Ler e processar os dados brutos do FWD.

import pandas as pd
import numpy as np
import os

class FWD:
    """
    Classe responsável pela leitura, processamento e avaliação
    dos dados de ensaios FWD a partir de arquivos Excel.
    """
    def __init__(self, path):
        self.path = path
        self.dict = {}
        self.conditionals = {
            "N10^7": {
                "D0": 50, "RAIO": 230, "SCI": 15, "BDI": 10, "BCI": 6
            },
            "N10^6":{
                "D0": 90, "RAIO": 110, "SCI": 30, "BDI": 15, "BCI": 10
            }
        }

    def _read(self):
        """Lê os arquivos .xlsx de uma estrutura de diretórios esperada."""
        list_path_files = os.listdir(self.path)
        fwd_files = {}
        for street in list_path_files:
            fwd_files[street] = {}
            excel_path = os.path.join(self.path, street, "EXCEL")
            if not os.path.exists(excel_path):
                continue
            
            # Filtra arquivos, ignorando os temporários do Excel
            excel_files = [f for f in os.listdir(excel_path) if f.endswith('.xlsx') and not f.startswith('~$')]

            for file in excel_files:
                street_side = "-".join(file.split(".")[0].split("_")[-2::])
                excel_file_path = os.path.join(excel_path, file)
                try:
                    fwd_files[street][street_side] = pd.read_excel(excel_file_path, engine='openpyxl')
                except Exception as e:
                    print(f"Alerta: Não foi possível ler o arquivo {excel_file_path}. Erro: {e}")
                    pass
            self.dict = fwd_files

    def _process_data(self):
        """Orquestra o processamento de cada DataFrame lido."""
        self._read()
        for key in self.dict.keys():
            for street_side, df in self.dict[key].items():
                if not df.empty:
                    self.dict[key][street_side] = self._process_dataframe(df)

    def _process_dataframe(self, df):
        """Aplica os cálculos dos índices deflectométricos ao DataFrame."""
        # Conversão de coordenadas
        df['Latitude'] = df['Latitude'].astype(str).str.replace(",",".")
        df['Longitude'] = df['Longitude'].astype(str).str.replace(",",".")
        df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
        df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
        df.dropna(subset=['Latitude', 'Longitude'], inplace=True)

        # Cálculo dos índices
        df['SCI'] = df['D1'] - df['D3']
        df['BDI'] = df['D3'] - df['D5']
        df['BCI'] = df['D5'] - df['D7']
        df['C'] = df['D1'] - df['D2']
        D30_D0 = np.divide(df['D3'], df['D1'])
        D60_D0 = np.divide(df['D5'], df['D1'])
        D90_D0 = np.divide(df['D7'], df['D1'])    
        Area_index = 15 * (1 + 2 * (D30_D0 + D60_D0 + D90_D0))
        df['AREA BACIA'] = Area_index
        return df

    def _evaluate_conditionals(self, df):
        """Adiciona colunas de 'Aprovado'/'Reprovado' com base nas condicionais."""
        for key, conditions in self.conditionals.items():
            df[f'ANÁLISE_RAIO_{key}'] = np.where(df['RAIO'] < conditions["RAIO"], "Reprovado", "Aprovado")
            df[f'ANÁLISE_D0_{key}'] = np.where(df['D1'] > conditions["D0"], "Reprovado", "Aprovado")
            df[f'ANÁLISE_SCI_{key}'] = np.where(df['SCI'] > conditions["SCI"], "Reprovado", "Aprovado")
            df[f'ANÁLISE_BDI_{key}'] = np.where(df['BDI'] > conditions["BDI"], "Reprovado", "Aprovado")
            df[f'ANÁLISE_BCI_{key}'] = np.where(df['BCI'] > conditions["BCI"], "Reprovado", "Aprovado")
        return df

    def _process_fwd_conditionals(self):
        """Orquestra a avaliação de cada DataFrame processado."""
        for street_name in self.dict.keys():
            for street_side in self.dict[street_name].keys():
                dataframe = self.dict[street_name][street_side]
                if not dataframe.empty:
                    self.dict[street_name][street_side] = self._evaluate_conditionals(dataframe)

    def process(self):
        """
        Método público principal para executar todo o pipeline de processamento.
        """
        self._process_data()
        self._process_fwd_conditionals()