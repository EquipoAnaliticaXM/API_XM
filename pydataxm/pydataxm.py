# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 11:05:46 2022

@author: 1040750676
"""

import requests
import json
import pandas as pd
import datetime as dt
#noinspection SpellCheckingInspection
from pydataxm.pydatasimem import *

import aiohttp # es para hacer peticiones asincronas
import asyncio # es para hacer peticiones asincronas	

class ReadDB(object):

    def __new__(cls):
        return super(ReadDB, cls).__new__(cls)
    
    
    def __init__(self):
        """This object was created to extract data from API XM"""   
        self.url = "https://servapibi.xm.com.co/{period_base}"
        self.connection = None
        self.request = ''
        self.inventario_metricas = self.all_variables()
        
        
    def all_variables(self):
        """This method allows the user to get all variables availables into the API XM.
        Args:
            None
        Returns: 
            Data Frame with all variables available into the API XM 
        """
        request = {"MetricId": 'ListadoMetricas'}
        connection = requests.post(f'https://servapibi.xm.com.co/Lists', json=request)
        data_json = json.loads(connection.content)
        df_variables = pd.json_normalize(data_json['Items'], 'ListEntities', 'Date', sep='_')
        df_variables.drop(columns=['Id', 'Date'], inplace=True)
        df_variables.columns = [x.replace('Values_', '') for x in df_variables.columns]
        return df_variables 
    
    
    def get_collections(self, coleccion=''):
        """ request public server data from XM by the API
        Args:
            coleccion: optional parameter, one of the set of variables availables at self.get_collections()
        Returns: 
            DataFrame with the raw Data
        """
        try:
            if coleccion == '':
                return self.inventario_metricas
            else:
                return self.inventario_metricas.query("MetricId == '{}'".format(coleccion))
        except:
            print('No existe la métrica {}'.format(coleccion))
            return pd.DataFrame()
    
    async def async_get_df(self, body, endpoint):
        """
            Realiza una solicitud HTTP POST asíncrona, obtiene la respuesta en formato JSON,
            la normaliza en un DataFrame de pandas y la devuelve.

            Args:
                body (dict): Un diccionario que contiene los datos que se enviarán en el cuerpo de la solicitud POST.
                endpoint (str): Una cadena que especifica el nombre del endpoint que se utilizará para normalizar los datos JSON en un DataFrame.

            Returns:
                pd.DataFrame: Un DataFrame de pandas que contiene los datos normalizados obtenidos de la respuesta JSON.
        """
        
        async with aiohttp.ClientSession() as session:            
               
            async with session.post(self.url, json=body, headers={'Connection':'close'}) as response:                    
                load = await response.json()
                dataframe = pd.json_normalize(load['Items'], endpoint, 'Date', sep='_')
                
        return dataframe
        
    async def run_async(self, list_bodies, endpoint):
        """
            Coordina la ejecución de múltiples tareas asíncronas que llaman a async_get_df.
            Recibe una lista de cuerpos de solicitudes, ejecuta todas las solicitudes en paralelo
            y concatena los resultados en un único DataFrame.

            Args:
                list_bodies (list): Una lista de diccionarios, donde cada diccionario contiene los datos que se enviarán en el cuerpo de una solicitud POST.
                endpoint (str): Una cadena que especifica el nombre del endpoint que se utilizará para normalizar los datos JSON en un DataFrame.

            Returns:
                pd.DataFrame: Un DataFrame de pandas que contiene los datos concatenados de todas las respuestas JSON normalizadas.
        """
         
        tasks = [self.async_get_df(body, endpoint) for body in list_bodies]
        result =  await asyncio.gather(*tasks)
        
        df = pd.concat(result)
        df.reset_index(drop=True, inplace=True) 
               
        return df            

    def request_data(self, coleccion, metrica, start_date, end_date, filtros=None):
        """ request public server data from XM by the API
        Args:
            coleccion: one of the set of variables availables at self.get_collections()
            metrica:one of this variables available in "ListadoMetricas", you have to enter MetricID
            start_date: start date consult data using YYYY-MM-DD format
            end_date: end date consult data using YYYY-MM-DD format
            filter: optional parameter, list of values to filter data
        Returns: 
            DataFrame with the raw Data
        """
        # self = cls()
        if type(filtros) == list:
            self.filtros = filtros
        elif filtros == None:
            self.filtros=[]
        else:
            print('Los filtros deben ingresarse como una lista de valores')
            self.filtros = list
            
        if coleccion not in self.inventario_metricas.MetricId.values:
            print('No existe la métrica {}'.format(coleccion))
            return pd.DataFrame()
        
        if metrica not in self.inventario_metricas.Entity.values:
            print('No existe la entidad {}'.format(metrica))
            return pd.DataFrame()
        
        # Generar periodos de inicio y fin de mes
        end_periods = pd.date_range(start_date, end_date, freq='M', inclusive = 'both')    
        if not  pd.Timestamp(end_date).is_month_end:
            end_periods = end_periods.append(pd.DatetimeIndex([end_date]))
        
        start_periods = end_periods.map(lambda x: x - pd.offsets.MonthBegin(1))        
        if not  pd.Timestamp(start_date).is_month_start:            
            start_periods.values[0] = pd.Timestamp(start_date)            
        
        # Crear lista de periodos    
        list_periods = list(zip(start_periods.astype(str), end_periods.astype(str)))
        
        period_dict = {
            'HourlyEntities': {'period_base': 'hourly', 'delta': 30, 'endpoint': 'HourlyEntities'},
            'DailyEntities': {'period_base': 'daily', 'delta': 30, 'endpoint': 'DailyEntities'},
            'MonthlyEntities': {'period_base': 'monthly', 'delta': 732, 'endpoint': 'MonthlyEntities'},
            'AnnualEntities': {'period_base': 'annual', 'delta': 366, 'endpoint': 'AnnualEntities'}
        }
        
        entity_type = self.inventario_metricas.query("MetricId == @coleccion and Entity == @metrica").Type.values[0]
        
        if entity_type in period_dict:             
            period_base = period_dict[entity_type]['period_base']
            endpoint = period_dict[entity_type]['endpoint']
            self.url = f'https://servapibi.xm.com.co/{period_base}'
            
            body_request = {
                    "MetricId": coleccion,
                    "StartDate": None,
                    "EndDate": None,
                    'Entity': metrica,
                    "Filter": self.filtros
            }
            
            list_bodies = []            
            for _start, _end in list_periods:
                temp_body = body_request.copy()
                temp_body['StartDate'] = _start
                temp_body['EndDate'] = _end
                list_bodies.append(temp_body)
          
            
            if __name__ == "__main__":
                data = asyncio.run(self.run_async(list_bodies, endpoint))
            else:
                loop = asyncio.get_event_loop()
                data = loop.run_until_complete(self.run_async(list_bodies, endpoint))
            

        elif self.inventario_metricas.query("MetricId == @coleccion and Entity == @metrica".format(coleccion, metrica)).Type.values == 'ListsEntities':
            period_base = 'lists'
            self.url = f'https://servapibi.xm.com.co/{period_base}'
            self.request = {'MetricId': coleccion,
                            'Entity': metrica}  
            self.connection = requests.post(self.url, json=self.request)
            data_json = json.loads(self.connection.content)
            data = pd.json_normalize(data_json['Items'], 'ListEntities','Date', sep='_')
        
        cols = data.columns
        for col in cols:
            data[col] = pd.to_numeric(data[col],errors='ignore')
        if ('Date' or 'date') in cols:
            data['Date'] = pd.to_datetime(data['Date'],errors='ignore', format= '%Y-%m-%d')
    
        return data

if __name__ == "__main__":
    
    consult = ReadDB()
    listado = consult.request_data("PrecBolsNaci", "Sistema", dt.date(2020, 10, 1), dt.date(2024, 11, 10))
    metricas = consult.get_collections()
