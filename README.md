# Analisador Interativo de Ensaios FWD (Falling Weight Deflectometer)

Este projeto consiste em uma aplicação web interativa, desenvolvida com Python e Streamlit, para a visualização e análise de dados de ensaios de deflectometria (FWD) em pavimentos. A ferramenta permite que engenheiros e técnicos carreguem dados de ensaios, processem os índices deflectométricos e visualizem os resultados em um mapa interativo, facilitando a identificação de pontos críticos e a avaliação da condição estrutural de vias.

## Funcionalidades

* **Visualização Georreferenciada**: Plota os pontos de ensaio em um mapa interativo com opção de visualização por satélite.
* **Análise Dinâmica**: Permite filtrar os resultados por Nível de Tráfego (`N10^7`, `N10^6`) e por Tipo de Análise (`D0`, `RAIO`, `SCI`, `BDI`, `BCI`).
* **Controle por Faixas**: Oferece a funcionalidade de ligar e desligar a visualização de faixas específicas diretamente no mapa.
* **Processamento Automático**: A classe `FWD` realiza o pré-processamento dos dados, calcula os principais índices deflectométricos e avalia cada ponto com base em critérios pré-definidos ("Aprovado" / "Reprovado").
* **Interface Intuitiva**: Interface web construída com Streamlit, tornando a análise de dados acessível e rápida.

## Estrutura dos Dados de Entrada

Para o correto funcionamento do sistema, os arquivos de dados (em formato `.xlsx`) devem seguir uma estrutura específica de colunas e organização de diretórios.

### Formato das Colunas

O arquivo Excel de entrada deve conter as seguintes colunas:

| Coluna | Descrição |
| :--- | :--- |
| `KM` | Estaca ou quilometragem do ponto de ensaio. |
| `Target Load kN` | Carga alvo do ensaio em quilonewtons. |
| `Target Load (Kgf)`| Carga alvo do ensaio em quilograma-força. |
| `D1` - `D7` | Deflexão (em µm) medida pelos geofones de 1 a 7. |
| `Ar` | Temperatura do ar (°C) no momento do ensaio. |
| `Pav.` | Temperatura do pavimento (°C) no momento do ensaio. |
| `Latitude` | Coordenada geográfica de latitude do ponto. |
| `Longitude` | Coordenada geográfica de longitude do ponto. |
| `RAIO` | Raio de curvatura da bacia de deflexão. |
| `Data e Hora` | Data e hora em que o ensaio foi realizado. |

### Estrutura de Diretórios

O sistema espera que os arquivos Excel estejam organizados em uma pasta `EXCEL`, dentro de um diretório que nomeia a via em análise. A estrutura deve ser a seguinte:

```
[PASTA_RAIZ_DO_PROJETO]/
│
└─── FWD/
     │
     └─── [NOME_DA_AVENIDA_OU_RODOVIA]/
          │
          └─── EXCEL/
               │   1_..._PD_FX1.xlsx
               │   2_..._PE_FX1.xlsx
               │   ...
```

### Convenção de Nomes de Arquivo

Os nomes dos arquivos `.xlsx` devem conter, em seus últimos caracteres, a identificação da pista e da faixa, seguindo o padrão:

* **Pista**: `PD` (Pista Direita) ou `PE` (Pista Esquerda)
* **Faixa**: `FX` seguido do número da faixa (ex: `FX1`, `FX2`)

**Exemplo de nome de arquivo válido:**
`1 - [INFORMAÇÕES_DO_PROJETO]_FWD_PD_FX1.xlsx`

## Como Executar o Projeto

**1. Pré-requisitos**
* Python 3.8 ou superior

**2. Instalação das Dependências**
Clone este repositório e, no terminal, navegue até a pasta raiz do projeto e instale as bibliotecas necessárias:

```bash
pip install streamlit pandas numpy folium streamlit-folium openpyxl
```

**3. Execução da Aplicação**
Com as dependências instaladas, execute o seguinte comando no terminal:

```bash
streamlit run app.py
```

A aplicação será aberta automaticamente no seu navegador padrão.

## Autor

Este sistema foi desenvolvido por **Augusto Cesar Rodrigues Xavier**.

## Licença

Este projeto está licenciado sob os termos da **Licença MIT**. Veja o arquivo `LICENSE` para mais detalhes.