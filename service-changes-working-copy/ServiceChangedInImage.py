import os
import csv
from datetime import datetime

class ServiceChangedInImage:
    def __init__(self,base_version,current_version):
        print('Processing the GitHub Difference to find Service Changed from Image...')
        self.base_version = base_version
        self.current_version = current_version
        # current working directory of python file
        self.currentDirectory = os.getcwd()
        # csv file path to store output of comparison
        self.csvFilePath = os.path.join(self.currentDirectory, f'service-changed-{datetime.now().strftime("%d-%m-%Y-%H-%M-%S")}.csv')

    def get_diff_service_name(self, list_git_diff_response):

        list_service_name = []

        for git_diff in list_git_diff_response:
            flag_image = False
            list_digest_data = []
            service_name = ''
            for diff in git_diff.split('\n'):
                # find the service name
                if 'diff --git' in diff:
                    flag_image = False
                    vDiff = diff.replace('diff --git', '').strip()
                    vDiff = (vDiff.split(' ') if (len(vDiff.split(' ')) > 0) else [])
                    vDiff = [x for x in vDiff if x.strip() != '']
                    flag_service = False
                    for key in vDiff[len(vDiff) -1].split('/'):
                        if flag_service:
                            service_name = key
                            break
                        if not flag_service and key == 'kubernetes-manifests':
                            flag_service = True

                    if service_name in list_service_name or service_name == '' :
                        # service name already present / service name not found wile parsing
                        # hence abort the current iteration
                        break
                else:
                    # process to validate the difference in digestd
                    #check only images tag to start comparison
                    if "images:" in diff or "image:" in diff:
                        flag_image = True
                        continue

                    if flag_image:
                        list_keys = ['digest:', 'name:', 'newName:']
                        diff = diff.strip('+- ')

                        temp_key = [x for x in list_keys if diff.startswith(x)]

                        if temp_key is not None and len(temp_key) > 0:
                            if 'digest:' in temp_key:
                                list_digest_data.append(diff)
                            else:
                                if len(list_digest_data) == 2 and len(set(list_digest_data)) == len(list_digest_data):
                                    list_service_name.append(service_name)
                                    break
                                list_digest_data = []

        if list_service_name is not None or list_service_name != '':
            print(f'Found {len(list_service_name)} service changed images in Github diff...')
            self.write_service_name_to_csv(list_service_name)
        else:
            print('Service changes in image not found...')

    def write_service_name_to_csv(self, list_service_name):
        print('Writing service changes image data to csv...')
        with open(self.csvFilePath, mode='w', newline="") as file:
            wr = csv.writer(file, delimiter=',')
            wr.writerow([f'Services Changed ({self.base_version} -> {self.current_version})'])
            for x in list_service_name:
                wr.writerow([x])
            file.close()
        print('Service changed data saved into csv file at location \n', self.csvFilePath)

