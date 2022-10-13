# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 11:05:46 2022

@author: 1040750676
"""

import requests
import json
import pandas as pd
import datetime as dt
import time 
# noinspection SpellCheckingInspection


class ReadDB(object):

    def __new__(cls):
        return super(ReadDB, cls).__new__(cls)
    
    
    def __init__(self):
        """This object was created to extract data from API XM"""   
        self.url = "http://servapibi.xm.com.co/{period_base}"
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
        connection = requests.post(f'http://servapibi.xm.com.co/Lists', json=request)
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
        if type(filtros)==list:
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
        
        if self.inventario_metricas.query("MetricId == '{}' and Entity == '{}'".format(coleccion, metrica)).Type.values == 'HourlyEntities':
            end = end_date
            condition = True
            aux = True
            data = None
            period_base = 'hourly'
            self.url = f'http://servapibi.xm.com.co/{period_base}'
            while condition:
                if (start_date - end_date).days < 30:
                    end = start_date + dt.timedelta(29)
                if end > end_date:
                    end = end_date
                self.request = {"MetricId": coleccion,
                                "StartDate": "{}".format(str(start_date)),
                                "EndDate": "{}".format(str(end)),
                                'Entity': metrica,
                                "Filter": self.filtros}

                self.connection = requests.post(self.url, json=self.request)

                data_json = json.loads(self.connection.content)

                temporal_data = pd.json_normalize(data_json['Items'], 'HourlyEntities', 'Date', sep='_')

                if data is None:
                    data = temporal_data.copy()
                else:
                    data = data.append(temporal_data, ignore_index=True)
                start_date = start_date + dt.timedelta(30)

                if end == end_date:
                    aux = False
                condition = ((end - start_date).days > 30 | (end - end_date).days != 0) | aux

        elif self.inventario_metricas.query("MetricId == '{}' and Entity == '{}'".format(coleccion, metrica)).Type.values == 'DailyEntities':
            end = end_date
            condition = True
            aux = True
            data = None
            period_base = 'daily'
            self.url = f'http://servapibi.xm.com.co/{period_base}'
            while condition:
                if (start_date - end_date).days < 30:
                    end = start_date + dt.timedelta(29)
                if end > end_date:
                    end = end_date

                self.request = {"MetricId": coleccion,
                                "StartDate": "{}".format(str(start_date)),
                                "EndDate": "{}".format(str(end)),
                                'Entity': metrica,
                                "Filter": self.filtros}
                self.connection = requests.post(self.url, json=self.request)
                data_json = json.loads(self.connection.content)
                temporal_data = pd.json_normalize(data_json['Items'], 'DailyEntities', 'Date', sep='_')
                if data is None:
                    data = temporal_data.copy()
                else:
                    data = data.append(temporal_data, ignore_index=True)

                start_date = start_date + dt.timedelta(30)
                if end == end_date:
                    aux = False
                condition = ((end - start_date).days > 29 | (end - end_date).days != 0) | aux
        
        elif self.inventario_metricas.query("MetricId == '{}' and Entity == '{}'".format(coleccion, metrica)).Type.values == 'MonthlyEntities':
            
            end = end_date
            condition = True
            aux = True
            data = None
            period_base = 'monthly'
            self.url = f'http://servapibi.xm.com.co/{period_base}'
            while condition:
                if (start_date - end_date).days < 732:
                    end = start_date + dt.timedelta(731)
                if end > end_date:
                    end = end_date

                self.request = {"MetricId": coleccion,
                                "StartDate": "{}".format(str(start_date)),
                                "EndDate": "{}".format(str(end)),
                                'Entity': metrica,
                                "Filter": self.filtros}
                self.connection = requests.post(self.url, json=self.request)
                data_json = json.loads(self.connection.content)
                temporal_data = pd.json_normalize(data_json['Items'], 'MonthlyEntities','Date', sep='_')
                if data is None:
                    data = temporal_data.copy()
                else:
                    data = data.append(temporal_data, ignore_index=True)

                start_date = start_date + dt.timedelta(732)
                if end == end_date:
                    aux = False
                condition = ((end - start_date).days > 731 | (end - end_date).days != 0) | aux

        elif self.inventario_metricas.query("MetricId == '{}' and Entity == '{}'".format(coleccion, metrica)).Type.values == 'AnnualEntities':
            
            end = end_date
            condition = True
            aux = True
            data = None
            period_base = 'annual'
            self.url = f'http://servapibi.xm.com.co/{period_base}'
            while condition:
                if (start_date - end_date).days < 366:
                    end = start_date + dt.timedelta(365)
                if end > end_date:
                    end = end_date

                self.request = {"MetricId": coleccion,
                                "StartDate": "{}".format(str(start_date)),
                                "EndDate": "{}".format(str(end)),
                                'Entity': metrica,
                                "Filter": self.filtros}
                self.connection = requests.post(self.url, json=self.request)
                data_json = json.loads(self.connection.content)
                temporal_data = pd.json_normalize(data_json['Items'], 'AnnualEntities', 'Code', sep='_')
                if data is None:
                    data = temporal_data.copy()
                else:
                    data = data.append(temporal_data, ignore_index=True)

                start_date = start_date + dt.timedelta(366)
                if end == end_date:
                    aux = False
                condition = ((end - start_date).days > 365 | (end - end_date).days != 0) | aux


        elif self.inventario_metricas.query("MetricId == '{}' and Entity == '{}'".format(coleccion, metrica)).Type.values == 'ListsEntities':
            period_base = 'lists'
            self.url = f'http://servapibi.xm.com.co/{period_base}'
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
    listado = consult.request_data("Gene", "Recurso", dt.date(2022, 10, 1), dt.date(2022, 10, 9))
    metricas = consult.get_collections()