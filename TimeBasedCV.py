
#Program that executes the rolling window train-val-test split 
import pandas as pd
import datetime
from datetime import datetime as dt
from dateutil.relativedelta import *

class TimeBasedCV(object):
    '''
    Parameters 
    ----------
    train_period: int
        number of time units to include in each train set
        default is 30
    test_period: int
        number of time units to include in each test set
        default is 7
    freq: string
        frequency of input parameters. possible values are: days, months, years, weeks, hours, minutes, seconds
        possible values designed to be used by dateutil.relativedelta class
        deafault is days
    '''
    
    
    def __init__(self, train_period=30, val_period=7, test_period=7, freq='days'):
        self.train_period = train_period
        self.val_period = val_period
        self.test_period = test_period
        self.freq = freq

        
        
    def split(self, data, first_split_date, second_split_date, date_column='DATE', gap=0):
        '''
        Generate indices to split data into training and test set
        
        Parameters 
        ----------
        data: pandas DataFrame
            your data, contain one column for the record date 
        validation_split_date: datetime.date()
            first date to perform the splitting on.
            if not provided will set to be the minimum date in the data after the first training set
        date_column: string, deafult='record_date'
            date of each record
        gap: int, default=0
            for cases the test set does not come right after the train set,
            *gap* days are left between train and test sets
        
        Returns 
        -------
        train_index ,test_index: 
            list of tuples (train index, test index) similar to sklearn model selection
        '''
        
        # check that date_column exist in the data:
        try:
            data[date_column]
        except:
            raise KeyError(date_column)
                    
        train_indices_list = []
        val_indices_list = []
        test_indices_list = []

       
        
        start_train = first_split_date - eval('relativedelta('+self.freq+'=self.train_period)')
        end_train = start_train + eval('relativedelta('+self.freq+'=self.train_period)')
        start_val = end_train + eval('relativedelta('+self.freq+'=gap)')
        end_val = start_val + eval('relativedelta('+self.freq+'=self.val_period)')
        start_test = end_val + eval('relativedelta('+self.freq+'=gap)')
        end_test = start_test + eval('relativedelta('+self.freq+'=self.test_period)')

        while end_test < data[date_column].max().date():
            # train indices:
            cur_train_indices = list(data[(data[date_column].dt.date>=start_train) & 
                                     (data[date_column].dt.date<end_train)].index)
            # validation indices:
            cur_val_indices = list(data[(data[date_column].dt.date>=start_val) & 
                                     (data[date_column].dt.date<end_val)].index)

            # test indices:
            cur_test_indices = list(data[(data[date_column].dt.date>=start_test) &
                                    (data[date_column].dt.date<end_test)].index)
            
            print("Train period:",start_train,"-" , end_train, ",val period:",start_val,"-" , end_val, ", Test period", start_test, "-", end_test,
                  "# train records", len(cur_train_indices),",# val records", len(cur_val_indices) , ", # test records", len(cur_test_indices))

            train_indices_list.append(cur_train_indices)
            val_indices_list.append(cur_val_indices)
            test_indices_list.append(cur_test_indices)

            # update dates:
            start_train = start_train + eval('relativedelta('+self.freq+'=self.val_period)')/2
            end_train = start_train + eval('relativedelta('+self.freq+'=self.train_period)')
            start_val = end_train + eval('relativedelta('+self.freq+'=gap)')
            end_val = start_val + eval('relativedelta('+self.freq+'=self.val_period)')            
            start_test = end_val + eval('relativedelta('+self.freq+'=gap)')
            end_test = start_test + eval('relativedelta('+self.freq+'=self.test_period)')

        # mimic sklearn output  
        index_output = [(train,val,test) for train,val,test in zip(train_indices_list,val_indices_list,test_indices_list)]

        self.n_splits = len(index_output)
        
        return index_output
    
    
    def get_n_splits(self):
        """Returns the number of splitting iterations in the cross-validator
        Returns
        -------
        n_splits : int
            Returns the number of splitting iterations in the cross-validator.
        """
        return self.n_splits 
