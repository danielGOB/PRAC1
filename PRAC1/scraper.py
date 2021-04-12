import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import timedelta, date
"""Vamos a importar las librerías necesarias para la realización de éste proyecto."""

class coronaWorldometersScrapper():

    def __init__(self):
        self.url = 'https://www.worldometers.info'
        self.subdomain = '/coronavirus/'
        self.colnames = []
        self.rows = []

#Esta función se encarga de descargar la página entera

    def _download_html(self,url):
        page = requests.get(url)
        return page

# Esta función extrae la cabecera de una tabla

    def _header_extractor(self,table):
        header = table.findAll('thead')[0]
        header_list = header.findAll('th')
        for i in header_list:
            self.colnames.append(i.getText())

# Esta función extrae las filas de información de la tabla

    def _rows_extractor(self,table):
        body = table.findAll('tbody')[0]
        body_list = body.findAll('tr')
        for i in body_list:
            row = []
            body_row = i.findAll('td')
            for j in body_row:
                row.append(j.getText().strip())
            self.rows.append(row)

# Esta función va a hacer un renaming de todas las cabeceras para hacerlas más legibles

    def _header_renaming(self,df):
        df = df.rename(columns={"#": "Nr.", "Country,Other": "Country",
                                "TotalCases": "Total Cases","NewCases": "New Cases",
                                "TotalDeaths": "Total Deaths", "NewDeaths": "New Deaths",
                                "TotalRecovered": "Total Recovered", "NewRecovered": "New Recovered",
                                "ActiveCases": "Active Cases", "Serious,Critical": "Serious/Critical",
                                "Tests/\n1M pop\n": "Test per 1M","Tot\xa0Cases/1M pop": "Total Cases per 1M",
                                "Deaths/1M pop": "Deaths per 1M", "TotalTests": "Total Tests",
                                "1 Caseevery X ppl": "1 Case every X ppl", "1 Deathevery X ppl": "1 Death every X ppl",
                                "1 Testevery X ppl": "1 Test every X ppl"}, errors="raise")
        return df

# Esta función recibe un dataframe y escribe la información en un csv en la carpeta donde ejecuta
#el código.

    def df_to_csv(self,outputFile,coronaDf):
        coronaDf.to_csv(outputFile, index=False, header=True)

# La función scrap es la función principal que va a realizar el proceso de extracción.

    def scrap(self):
        print(f"vamos a extraer datos de {self.url} para obtener información actual acerca del coronavirus")

        #primeramente vamos a descargar los datos de la pagina web

        html = self._download_html(self.url + self.subdomain)
        soup = BeautifulSoup(html.content, 'html.parser')

        #extraemos la primera tabla de las que contiene la página web

        soup_table = soup.findAll('table')[0]

        #extraemos las cabeceras de la tabla

        self._header_extractor(soup_table)

        #extraemos las lineas de información de la tabla

        self._rows_extractor(soup_table)

        #con la información rows y col_names vamos a proceder a crear un dataframe para poder trabajar con la información de manera más comoda

        coronaDf = pd.DataFrame(self.rows, columns=self.colnames)

        #Vamos a hacer modificaciones en la cabecera del dataframe para hacerlo más legible

        coronaDf = self._header_renaming(coronaDf)

        #Vamos a excluir los primeros 8 elementos del dataframe porque nos muestra información de los distintos continentes. Puesto que
        #para este estudio quiero sólo información de los paises, no los tendremos en cuenta.

        coronaDf = coronaDf.iloc[8:]

        return coronaDf

