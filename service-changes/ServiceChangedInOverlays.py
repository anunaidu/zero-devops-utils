import os
import csv
from datetime import datetime


class ServiceChangedInOverlays:
    def __init__(self,base_version,current_version):
        print('Processing the GitHub Difference to find Service Added...')
        # current working directory of python file
        self.base_version = base_version
        self.current_version = current_version
        self.currentDirectory = os.getcwd()
        # csv file path to store output of comparison
        self.csvFilePath = os.path.join(self.currentDirectory, f'service-overlays-{datetime.now().strftime("%d-%m-%Y-%H-%M-%S")}.csv')

    def get_diff_service_name(self, list_git_diff_response):
        list_code_accept = ['A']
        list_git_diff_response = [x for x in list_git_diff_response if x.strip()[0].strip() in list_code_accept]
        list_git_diff_response = [x for x in list_git_diff_response if '/overlays/' in x]
        list_service_name = []

        for git_diff in list_git_diff_response:
            git_code = git_diff.strip()[0].strip()
            git_diff = git_diff.lstrip(git_code).strip()
            flag_service = False
            service_name = ''
            if git_code in list_code_accept:
                for key in git_diff.split('/'):
                    if flag_service:
                        service_name = key
                        break
                    if not flag_service and key == 'kubernetes-manifests':
                        flag_service = True

                if service_name != '' and service_name not in list_service_name:
                    # service name already present / service name not found wile parsing
                    list_service_name.append(service_name)

        if list_service_name is not None and len(list_service_name) > 0 :
            print(f'Found {len(list_service_name)} service added in Github diff...')
            self.write_service_name_to_csv(list_service_name)
        else:
            print('No data found for service added...')

    def write_service_name_to_csv(self, list_service_name):
        print('Writing service added data to csv...')
        with open(self.csvFilePath, mode='w', newline="") as file:
            wr = csv.writer(file, delimiter=',')
            wr.writerow([f'Service changed in Overlays ({self.base_version} -> {self.current_version})'])
            for x in list_service_name:
                wr.writerow([x])
            file.close()
        print('Service added data saved into csv file at location \n', self.csvFilePath)

