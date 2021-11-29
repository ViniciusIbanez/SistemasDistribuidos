

from helpers.secrets_helper import retrieve_secrets
from helpers.mongo import connect
import datetime;
import requests
from flask import Flask, jsonify
import json
import argparse
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from helpers.json_helper import load_json



class Analysis:

    def  __init__(self):
        self.credentials = retrieve_secrets(debug=True)
        self.mongo_connection = connect(self.credentials, 'analysis')
        self.model = load_json('./performance_analysis\model\Test_Scope')


    def run_test(self):
        config_object = self.model

        for i in range(0, config_object.get('iterations')):
            for config in config_object.get('config'):
                self.retrieve_and_persist_result(config)

    def retrieve_and_persist_result(self, config):
        url = self.credentials.get('API_URL')
        print(f'{url}/run_test')
        result  = requests.get(f'{url}/run_test', json=config)
        json_data = json.loads(result.text).get('body')
        json_data['timestamp'] = datetime.datetime.now().timestamp()
        print(json_data)
        self.mongo_connection.insert_one(json_data)
    
    def retrieve_arguments(self):
        parser = argparse.ArgumentParser(description='Retrives info to run analysis')
        parser.add_argument('--mode', type=str , help='mode') 
       
        args = parser.parse_args()

        return args

    def run_analysis(self):
        print(f'Extracting historic data from database')
        historic_data = self.mongo_connection.find({})
        print(f'Data extracted')
        data = []
        report_data = {}
        for record in historic_data:
            data.append(record)
            
        dataframe =  pd.DataFrame(data)

        
        raw_data =  (
            dataframe[['nodes', 'tweets_to_retrieve', 'duration_time']]
            .round(5)
            .sort_values("nodes", ascending=True)
            .groupby(['nodes', 'tweets_to_retrieve']))
        report_data['raw_data']= raw_data
        
        print('Raw Data:\n')
        raw_data.apply(print)
        print('\n\n\n')

        
        count_df =  self.retrieve_count(dataframe)
        report_data['count_df'] = count_df
        print('Countdf:\n')
        count_df.apply(print)
        print('\n\n\n')


        average_df, average_with_tweets = self.retrieve_average_duration(dataframe=dataframe)
        report_data['average']= average_df

        report_data['average_w_tweets']= average_with_tweets

        print('Average by tweets:\n')
        average_with_tweets.apply(print)
        print('\n\n\n')

        print('Average duration:\n')
        average_df.apply(print)
        print('\n\n\n')
      
        self.create_report(report_data)
        
    
    def retrieve_average_duration(self, dataframe):
        average_df = dataframe[['nodes', 'duration_time']].groupby(['nodes']).mean()
        average_df_w_tweets = dataframe[['nodes','tweets_to_retrieve','duration_time']].groupby(['nodes', 'tweets_to_retrieve']).mean()
        return average_df, average_df_w_tweets
    
    def retrieve_count(self, dataframe):
        count_df = dataframe.groupby(['nodes']).size().reset_index(name='count')
        print('count')
        count_df.apply(print)
        return count_df
    


    def create_report(self, report_data):
        base_path =f'{os.getcwd()}/performance_analysis/results'
        hash = datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        directory = f'{base_path}/{hash}'
        
        try:
            os.mkdir(directory)
        except Exception as e:
            print(e)

        for name, dataframe in report_data.items():
            fig = plt.figure(facecolor='w', edgecolor='k', figsize=(8,8))
            sns.heatmap(dataframe.head(),
                        #cmap=ListedColormap(['white']), 
                        #cmap='viridis',
                        xticklabels=True, 
                        yticklabels=True, 
                        linewidths=1, 
                        linecolor='black', 
                        annot=True)
            plt.savefig(f'{directory}/{name}.png')
            
if __name__ == '__main__':
    a = Analysis()
    mode = a.retrieve_arguments().mode
    if mode == 'extract':
        print(f'Starting the extract for the following config:\n{a.model}')
        a.run_test()
    elif mode ==  'analysis':
        print(f'Starting the analysis for the historic data')
        a.run_analysis()
    else:
        print(f'The folowwing mode [{mode}] is not valid !!')
    
    #a.run_analysis()


    
    
    
    
