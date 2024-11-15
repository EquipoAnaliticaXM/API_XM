import requests
import logging
import pandas as pd
from dataclasses import dataclass
import datetime as dt
from itertools import repeat

DATASETID = ""
VARIABLE_INVENTORY_ID = "a5a6c4"
CATALOG_ID =  "e007fb"
REFERENCE_DATE = '1990-01-01'
DATE_FORMAT = "%Y-%m-%d"
TODAY = dt.datetime.strftime(dt.datetime.now(), DATE_FORMAT)
BASE_API_URL = "https://www.simem.co/backend-files/api/PublicData?startdate={}&enddate={}"

class _Validation:
    
    @staticmethod 
    def log_approve(variable):
        approve_message = f"Variable values validated: {variable}"
        logging.debug(approve_message)

    @staticmethod
    def filter(var_column : str, var_values: str | list) -> None | tuple[str,list]:
        if not var_column and not var_values:
            logging.info("No filter has been chosen.")
            return None
        if not var_column or not var_values:
            logging.info("Check that the column and values are both defined for the filter. No filter has been chosen")
            return None
        if not isinstance(var_column, str):
            raise TypeError("Column filter must be a string")
        if isinstance(var_values, str):
            var_values = [var_values]
        elif not isinstance(var_values, list):
            raise TypeError("Values filter must be a string or a list")
        var_filter = (var_column, var_values)
        _Validation.log_approve(var_filter)
        return var_filter
    
    @staticmethod
    def date(var_date) -> dt.datetime:
        if isinstance(var_date, dt.datetime):
            return var_date
        try:
            var_date = dt.datetime.strptime(var_date, DATE_FORMAT)
        except ValueError:
            raise ValueError("Incorrect date format, use YYYY-MM-DD")
        except TypeError:
            raise TypeError("Incorrect data, date must be a string, datetime.date or datetime.datetime type.")
        return var_date

    @staticmethod
    def datasetid(var_dataset_id: str):
        if not isinstance(var_dataset_id, str):
            raise TypeError("Incorrect data type for ID, must be a string")
        var_dataset_id = var_dataset_id.strip()
        if len(var_dataset_id) > 6:
            raise ValueError("Invalid dataset ID")
        if not var_dataset_id.isalnum():
            raise ValueError("Dataset ID must be alphanumeric")
        _Validation.log_approve(var_dataset_id)
        return var_dataset_id
    
    @staticmethod
    def catalog_type(cat_type: str):
        if not isinstance(cat_type, str):
            raise TypeError("Incorrect data type for catalog type, must be a string")
        cat_type = cat_type.lower()
        if cat_type not in ('datasets', 'variables'):
            raise ValueError("Wrong parameter registered. Write 'Datasets' or 'Variables'.")
        _Validation.log_approve(cat_type)
        return cat_type

        
@dataclass
class ReadSIMEM:
    """
    Class to request dataset information and data to SIMEM using API

    Args: 
    var_dataset_id : str
        ID of the dataset to request data.
    var_start_date : str | dt.datetime 
        The starting date for the data slicing.
    var_end_date : str | dt.datetime 
        The ending date for the data slicing.
    var_column_destiny (Optional): str 
        The column name to apply the filter on.
    var_values (Optional): str | list 
        The values to filter the column by.
    
    Methods:
    set_datasetid(self, var_dataset_id) -> None:
        Sets the dataset ID for the request.

    set_dates(self, var_start_date: str | dt.datetime, var_end_date: str | dt.datetime) -> None:
        Sets the start and end dates for the dataset request.

    set_filter(self, var_column, var_values) -> None:
        Sets the filter for the dataset request.
        
    main(self, filter: bool = False) -> pd.DataFrame:
        Creates a .csv file with the dataset records for the given dates.
    """

    def __init__(self, var_dataset_id: str, var_start_date: str | dt.datetime, var_end_date: str| dt.datetime,
                 var_column_destiny: str = None, var_values: str | list = None):
        self.url_api: str = BASE_API_URL
        self.set_datasetid(var_dataset_id)
        self.set_dates(var_start_date, var_end_date)
        self.set_filter(var_column_destiny, var_values)
        self._set_dataset_data()

    def set_filter(self, var_column, var_values) -> None:
        """
        Sets the filter for the dataset request and the complement for the URL.
        If one of the 2 arguments are not given the filter won't set.
        
        Args:
        var_column : str
            The column name to apply the filter on.
        var_values : str | list
            The values to filter the column by.
        
        Returns:
        None
        """
        var_filter = _Validation.filter(var_column, var_values)
        if var_filter is None:
            var_filter = ''
            return
        values_string = ','.join(var_filter[1])
        self.__filter_values: tuple[str, list] =  var_filter
        self.__filter_url: str = f"&columnDestinyName={var_column}&values={values_string}"
        logging.info("Filter defined")

    def set_datasetid(self, var_dataset_id) -> None:
        """
        Sets the dataset ID for the request and complement the basic url for the defined dataset.
        
        Parameters:
        var_dataset_id : str
            The dataset ID to be set.
        
        Returns:
        None
        """
        var_dataset_id = _Validation.datasetid(var_dataset_id)
        self.__dataset_id: str = var_dataset_id.lower()
        self.url_api = self.url_api + f"&datasetId={var_dataset_id}"
        logging.info("ID defined")

    def set_dates(self, var_start_date: str | dt.datetime, 
                  var_end_date: str | dt.datetime) -> None:
        """
        Sets the start and end dates for the dataset request.
        
        Parameters:
        var_start_date : str | dt.datetime
            The start date for the dataset request.
        var_end_date : str | dt.datetime
            The end date for the dataset request.
        
        Returns:
        None
        """
        var_start_date = _Validation.date(var_start_date)
        var_end_date = _Validation.date(var_end_date)
        if var_start_date > var_end_date:
            logging.info("Dataset will be empty - Start date is bigger than end date")
        self.__start_date: dt.datetime = var_start_date
        self.__end_date: dt.datetime = var_end_date
        logging.info("Dates defined")
        
    def _set_dataset_data(self) -> None:
        """
        Internal method to set dataset information.
        Make a initial request to the API to extract and organize all the information 
        related to the required dataset.
        
        Returns:
        None
    
        """
        with requests.Session() as session:
            url = self.url_api.format(REFERENCE_DATE, REFERENCE_DATE)
            response = self._make_request(url, session)
            response["parameters"]["startDate"] = self.get_startdate()
            response["parameters"]["endDate"] = self.get_enddate()
            self.__dataset_info = response
            metadata = response["result"]["metadata"]
            self.__columns: pd.DataFrame = pd.DataFrame.from_dict(response["result"]["columns"])
            self.__date_filter: str = response["result"]["filterDate"]
            self.__metadata: pd.DataFrame = pd.DataFrame.from_records([metadata])
            self.__name: str = response["result"]["name"]
            self.__granularity: str = metadata["granularity"]
            self.__resolution: int = self.__check_date_resolution(self.__granularity)
            session.close()
        
    def main(self, filter:bool= False) -> pd.DataFrame:
        """
        Creates a .csv file with the information about the required dataset 
        in the given dates.
        
        Parameters:
        filter : bool
            Whether to apply the filter to the dataset request.
        
        Returns:
        pd.DataFrame
            A DataFrame containing the dataset records.
        """
        self.session = requests.Session()
        resolution: int = self.get_resolution()
        urls: list[str] = self.__create_urls(self.get_startdate(), self.get_enddate(), resolution, filter)
        records: list[list] = list(map(self._get_records, urls, repeat(self.session)))
        dataset_info: dict = self.__get_dataset_info()
        dataset: dict = self.__save_dataset(dataset_info, records)
        self.session.close()

        return pd.DataFrame.from_dict(dataset["result"]["records"])

    def _get_records(self, var_url: str, session) -> list:
        """
        Makes the request and returns a list of records from the dataset.
        
        Parameters:
        var_url : str
            The URL for the dataset request.
        session : requests.Session
            The session for making the request.
        
        Returns:
        list
            A list of records from the dataset.
        """
        response = self._make_request(var_url, session)
        records = response["result"]["records"]
        logging.info("Records saved: %d rows registered.", len(records))
        return records


    def __save_dataset(self, var_dataset_info: dict, records: list[list]):
        """
        Creates a deserialized JSON in a dictionary that includes the dataset info and 
        the records of the selected dates.
        
        Parameters:
        var_dataset_info : dict
            The dataset information.
        records : list[list]
            The list of records from the dataset.
        
        Returns:
        dict
            A dictionary containing the dataset info and records.
        """
        var_dataset_info["result"]["records"] = [item for sublist in records for item in sublist]
        logging.info("%s from %s to %s dataset saved.", self.get_datasetid(), self.get_startdate(), self.get_enddate())
        return var_dataset_info
    
    @staticmethod
    def _make_request(url: str, session: requests.Session) -> dict:
        """
        Makes the GET request to the URL inside a session and delivers a dictionary
        with the response.
        
        Parameters:
        url : str
            The URL for the dataset request.
        session : requests.Session
            The session for making the request.
        
        Returns:
        dict
            A dictionary containing the response in json encoded format.
        """
        response = session.get(url)
        logging.info("Response with status: %s", response.status_code)
        return response.json()

    @staticmethod
    def __check_date_resolution(granularity: str) -> int:
        """
        Checks if the date range given in the object is allowed in a request to the API.
        
        Parameters:
        granularity : str
            The granularity of the date range (e.g., 'Diaria', 'Horaria', 'Mensual', 'Semanal', 'Anual').
        
        Returns:
        int
            The maximum allowed date range in days.
        """
        if granularity in ['Diaria','Horaria']:
            resolution = 31
        elif granularity in ['Mensual','Semanal']:
            resolution = 731
        elif granularity == 'Anual':
            resolution = 1827
        else:
            resolution = 0
        
        return resolution

    @staticmethod
    def _generate_start_dates(start_date: dt.datetime, end_date: dt.datetime, resolution: int):
        """
        Generator to deliver a list of date ranges.
        
        Parameters:
        start_date : dt.datetime
            The start date of the range.
        end_date : dt.datetime
            The end date of the range.
        resolution : int
            The maximum allowed date range in days.
        
        Yields:
        str
            The start dates in the specified date range formatted as strings.
        """
        intervals = (end_date - start_date)/resolution

        for i in range(0, intervals.days + 1):
            yield (start_date + dt.timedelta(days=resolution)*i).strftime(DATE_FORMAT)
        yield (end_date.strftime(DATE_FORMAT))

    def __create_urls(self, start_date: str, end_date: str, resolution: int, filter: bool= False) -> list[str]:
        """
        Receive the limit dates and deliver the API URLs for the dataset id 
        and different date ranges based on resolution.
        
        Parameters:
        start_date : str
            The start date of the range in 'YYYY-MM-DD' format.
        end_date : str
            The end date of the range in 'YYYY-MM-DD' format.
        resolution : int
            The maximum allowed date range in days.
        filter : bool, optional
            Whether to apply the filter to the dataset request (default is False).
        
        Returns:
        list[str]
            A list of URLs for the dataset requests.
        """
        start_dates: list[str] = list(date for date in self._generate_start_dates(start_date, end_date, resolution))
        end_dates: list[str] = [(dt.datetime.strptime(date,'%Y-%m-%d') - dt.timedelta(days=1)).strftime('%Y-%m-%d') for date in start_dates]
        end_dates[-1] = start_dates[-1]
        start_dates.pop(-1)
        end_dates.pop(0)
        if filter:
            base_url = self.url_api + self.__filter_url
        else: 
            base_url = self.url_api
        urls: list[str] = list(map(base_url.format, start_dates, end_dates))
            
        logging.info("%s urls created.", self.get_datasetid())
        return urls

    def get_datasetid(self) -> str:
        """
        Returns the dataset ID.
        
        Returns:
        str
            The dataset ID.
        """
        return self.__dataset_id

    def get_startdate(self) -> str:
        """
        Returns the start date of the dataset object.
        
        Returns:
        str
            The start date in 'YYYY-MM-DD' format.
        """
        return self.__start_date

    def get_enddate(self) -> str:
        """
        Returns the end date of the dataset object.
        
        Returns:
        str
            The end date in 'YYYY-MM-DD' format.
        """
        return self.__end_date

    def get_filter_url(self) -> str | None:
        """
        Returns the filter URL complement for the dataset request.
        
        Returns:
        str
            The filter URL.
        """
        var_filter_url = getattr(self, "__filter_url", None)
        if var_filter_url is None:
            logging.info("No filter assigned.")
        return var_filter_url

    def get_filters(self) -> tuple | None:
        """
        Returns the filter values for the dataset request.
        
        Returns:
        tuple | str
            The filter values.
        """
        var_filter_values = getattr(self, "__filter_values", None)
        if var_filter_values is None:
            logging.info("No filter assigned.")  
        return var_filter_values  

    def get_resolution(self) -> int:
        """
        Returns the resolution of the dataset object.
        
        Returns:
        int
            The resolution in days.
        """
        return self.__resolution

    def get_granularity(self) -> str:
        """
        Returns the granularity of the dataset object.
        
        Returns:
        str
            The granularity (e.g., 'Diaria', 'Horaria', 'Mensual', 'Semanal', 'Anual').
        """
        return self.__granularity

    def get_metadata(self) -> dict:
        """
        Returns the metadata of the dataset.
        
        Returns:
        dict
            The metadata of the dataset.
        """
        return self.__metadata

    def get_columns(self) -> pd.DataFrame:
        """
        Returns the columns of the dataset.
        
        Returns:
        pd.DataFrame
            A DataFrame containing the columns of the dataset.
        """
        return self.__columns  

    def get_name(self) -> str:
        """
        Returns the name of the dataset.
        
        Returns:
        str
            The name of the dataset.
        """
        return self.__name
    
    def get_filter_column(self) -> str:
        """
        Retrieves the assigned column to filter the dates in SIMEM.

        Returns:
        str
            The current column filter.
        """
        return self.__date_filter

    def __get_dataset_info(self) -> dict:
        """
        Returns the dataset information.
        
        Returns:
        dict
            A dictionary containing the dataset information.
        """
        return self.__dataset_info


class CatalogSIMEM(ReadSIMEM):
    """
    Class to interact with the SIMEM catalogs.
    
    Args:
    catalog_type : str
        The type of catalog to extract from the webpage ('Datasets', 'Variables')

    Methods:
    get_data(self) -> pd.DataFrame:
        Retrieves the catalog data stored in the object.

    """
    
    def __init__(self, catalog_type: str):
        
        self.set_dates(REFERENCE_DATE, TODAY)
        self.url_api = BASE_API_URL
        
        catalog_type = _Validation.catalog_type(catalog_type)
        if catalog_type == 'datasets':
            self.set_datasetid(CATALOG_ID)
        elif catalog_type == 'variables':
            self.set_datasetid(VARIABLE_INVENTORY_ID)

        self._set_dataset_data()
        self.url_api = self.url_api.format(self.get_startdate(), self.get_enddate())
        with requests.Session() as session:
            datasets = super()._get_records(self.url_api, session)
            self.__data = pd.DataFrame.from_dict(datasets)
        logging.info("Catalog retrieved correctly.")

    def get_data(self) -> pd.DataFrame:
        """
        Retrieves the data stored in the object.

        Returns:
            pd.DataFrame: The data stored in the object.
        """
        return self.__data
