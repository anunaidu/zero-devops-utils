import os
import csv
from datetime import datetime


class UpdatedChangesInArgoCDPipeline:

    def __init__(self):
        self.argocd_folder_path = None
        self.kubernetes_folder_path = None
        self.zero_deployment_path = f'{os.path.expanduser("~")}/zero-deployment/'
        self.currentDirectory = os.getcwd()
        self.csvFilePath = os.path.join(self.currentDirectory, f'updated-service-{datetime.now().strftime("%d-%m-%Y-%H-%M-%S")}.csv')
        print('Updated service changes in ARGO CD pipeline process...')

    def get_folder_from_kubernetes_folder(self):
        list_kubernetes_folder_name = []
        for root, directories, files in os.walk(self.kubernetes_folder_path):
            list_kubernetes_folder_name = directories
            break

        return list_kubernetes_folder_name

    def get_files_from_argocd_folder(self):
        list_argocd_file_name = [file.replace('.jsonnet', '').strip() for file in os.listdir(self.argocd_folder_path) if file.strip().endswith('jsonnet')]
        return list_argocd_file_name

    def comparision_of_the_service_name(self, list_argocd_file_name, list_kubernetes_folder_name):

        len_kubernetes = len(list_kubernetes_folder_name)
        len_argocd = len(list_argocd_file_name)

        if len_kubernetes == len_argocd:
            print('ArgoCD services has matched...')
        elif len_kubernetes > len_argocd:
            list_argocd_missed_service = [service for service in list_kubernetes_folder_name if service not in list_argocd_file_name]
            print(f'ArgoCD has {len(list_argocd_missed_service)} service change(s)...')
            self.write_service_name_to_csv(list_argocd_missed_service)
        else:
            print('No changes in ArgoCD...')

    def write_service_name_to_csv(self, list_service_name):
        with open(self.csvFilePath, mode='w', newline="") as file:
            wr = csv.writer(file, delimiter=',')
            wr.writerow(['Updated service changed'])
            for x in list_service_name:
                wr.writerow([x])
            file.close()
        print('Updated service changed data saved into csv file at location \n', self.csvFilePath)

    def updated_changes_in_argocd_pipeline(self, argocd_folder_path, kubernetes_folder_path):
        self.argocd_folder_path = self.zero_deployment_path + argocd_folder_path
        self.kubernetes_folder_path = self.zero_deployment_path + kubernetes_folder_path
        list_kubernetes_folder_name = self.get_folder_from_kubernetes_folder()
        list_argocd_file_name = self.get_files_from_argocd_folder()
        self.comparision_of_the_service_name(list_argocd_file_name, list_kubernetes_folder_name)


