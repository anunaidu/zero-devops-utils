import os
import csv
from datetime import datetime


class NewServiceAdded:

    def __init__(self, base_version, current_version):
        print('Processing the GitHub Difference to find Service Added...')
        # current working directory of python file
        self.base_version = base_version
        self.current_version = current_version
        self.currentDirectory = os.getcwd()
        # csv file path to store output of comparison
        self.csvFilePath = os.path.join(self.currentDirectory,
                                        f'new-service-added-{datetime.now().strftime("%d-%m-%Y-%H-%M-%S")}.csv')

    def write_service_name_to_csv(self, list_service_name):
        print('Writing service added data to csv...')
        with open(self.csvFilePath, mode='w', newline="") as file:
            wr = csv.writer(file, delimiter=',')
            wr.writerow([f'Service Added ({self.base_version} -> {self.current_version})'])
            for x in list_service_name:
                wr.writerow([x])
            file.close()
        print('Service added data saved into csv file at location \n', self.csvFilePath)
