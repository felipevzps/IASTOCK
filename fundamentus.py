import pandas as pd
import os 

#[Task 1]: Create dictonaires with each company dataframe's
'''
fundamentus = {
    "ABEV3": balanco_dre_abev3,
    "MGLU3": balanco_dre_muglu3,
                }
'''

companies = ["ABEV3", "AZUL4", "BTOW3", "B3SA3", "BBSE3", "BRML3", "BBDC4", "BRAP4", "BBAS3", "BRKM5", "BRFS3", "BPAC11", "CRFB3", "CCRO3", "CMIG4", "HGTX3", "CIEL3", "COGN3", "CPLE6", "CSAN3", "CPFE3", "CVCB3", "CYRE3", "ECOR3", "ELET6", "EMBR3", "ENBR3", "ENGI11", "ENEV3", "EGIE3", "EQTL3", "EZTC3", "FLRY3", "GGBR4", "GOAU4", "GOLL4", "NTCO3", "HAPV3", "HYPE3", "IGTA3", "GNDI3", "ITSA4", "ITUB4", "JBSS3", "JHSF3", "KLBN11", "RENT3", "LCAM3", "LAME4", "LREN3", "MGLU3", "MRFG3", "BEEF3", "MRVE3", "MULT3", "PCAR3", "PETR4", "BRDT3", "PRIO3", "QUAL3", "RADL3", "RAIL3", "SBSP3", "SANB11", "CSNA3", "SULA11", "SUZB3", "TAEE11", "VIVT3", "TIMS3", "TOTS3", "UGPA3", "USIM5", "VALE3", "VVAR3", "WEGE3", "YDUQ3"]

fundamentus = {}

files = os.listdir("balancos")

for file in files:
    ticker = file[-9:-4]
    if "11" in ticker:
        ticker = file[-10:-4]
    if ticker in companies:
        balanco = pd.read_excel(f'balancos/{file}', sheet_name=0)
        #first column = ticker
        balanco.iloc[0, 0] = ticker
        #header = line 1 - (0, [1], 2, ...)
        balanco.columns = balanco.iloc[0]
        balanco = balanco[1:]
        #Create header with the companie ticker
        balanco = balanco.set_index(ticker)

        dre = pd.read_excel(f'balancos/{file}', sheet_name=1)
        #first column = ticker
        dre.iloc[0, 0] = ticker
        #header = line 1 - (0, [1], 2, ...)
        dre.columns = dre.iloc[0]
        dre = dre[1:]
        #Create header with the companie ticker
        dre = dre.set_index(ticker)

        fundamentus[ticker] = balanco.append(dre)
        #print(fundamentus)

#[Task 2]: Get 'cotacoes' for each company
cotacoes_df = pd.read_csv("Cotacoes.xlsx - Sheet1.tsv", sep="\t")
cotacoes = {}

for company in cotacoes_df["Empresa"].unique():
    cotacoes[company] = cotacoes_df.loc[cotacoes_df["Empresa"] == company, :]
#print(cotacoes["ABEV3"])

for company in companies:
    if cotacoes[company].isnull().values.any():
        cotacoes.pop(company)

companies = list(cotacoes.keys())

#[Task 3]: Concatenate 'fundamentus' with 'cotacoes'
'''
TO DO:
'cotacoes': 
    - Move 'Date' to index

'fundamentus':
    - Change lines with columns
    - Change date to python datetime format
    - Concatenate 'fundamentus' wich 'Adj Close' column
'''

for company in fundamentus:
    table = fundamentus[company].T #transpose
    table.index = pd.to_datetime(table.index, format="%d/%m/%Y")
    cotacao_table = cotacoes[company].set_index("Date")
    cotacao_table = cotacao_table[["Adj Close"]]
    
    table = table.merge(cotacao_table, right_index=True, left_index=True)
    table.index.name = company
    fundamentus[company] = table

print(fundamentus["ABEV3"])