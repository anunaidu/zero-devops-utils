import argparse
from GitCommands import GitCommands
from ServiceChangedInImage import ServiceChangedInImage
from ServiceChangedInFolder import ServiceChangedInFolder
from UpdatedChangesInArgoCDPipeline import UpdatedChangesInArgoCDPipeline

def read_inputs():
     vParser = argparse.ArgumentParser(description='Read input arguments')
     vParser.add_argument('-basebranch', '-bb', type=str, help='pass the base branch with version', required=True)
     vParser.add_argument('-currentbranch', '-cb', type=str, help='pass the current branch with version', required=True)
     #vParser.add_argument('-difffolder', '-df', type=str, help='enter relative path of the git folder', required=True)
     vParser.add_argument("-processtype", "-t", type=str, help="Process Type - {image, folder, count, all}",
                          choices=['image', 'folder', 'count', 'all'], default='all')

     return vParser.parse_args()

# Defining main function
def main():

    vInputs = read_inputs()
    git_origin = 'origin/'
    base_version = git_origin + vInputs.basebranch
    current_version = git_origin + vInputs.currentbranch
    #diff_folder = vInputs.difffolder
    process_type = vInputs.processtype

    if base_version != '' and current_version != '' and process_type != '':

        print('Base Version : ', base_version, '\nCurrent Version : ' ,current_version,
              '\nProcess Type', process_type)
        list_process_type = []
        if process_type == 'all':
            list_process_type = ['image', 'folder', 'count', 'all']
        else:
            list_process_type = [process_type]

        print('Selected process type options to process : ', list_process_type)

        git_commands_class = GitCommands()

        for process_type in list_process_type:
            print(f'Processing the {process_type} option...')
            if process_type == 'image':
                diff_folder = 'kubernetes-manifests/*/*/*/kustomization.yaml'
                list_git_diff_response = git_commands_class.git_diff_with_version_in_service_image(base_version, current_version, diff_folder)
                if list_git_diff_response is not None and len(list_git_diff_response) > 0:
                    # Validate the kustomization.yaml changed service name
                    print(f'Github diff response has {len(list_git_diff_response)} data')
                    ServiceChangedInImage(base_version,current_version).get_diff_service_name(list_git_diff_response)
                else:
                    print(f'process type {process_type} has no github diff response to process')

            elif process_type == 'folder':
                diff_folder = 'kubernetes-manifests/'
                list_git_diff_response = git_commands_class.git_diff_with_version_in_service_folder(base_version, current_version, diff_folder)
                if list_git_diff_response is not None and len(list_git_diff_response) > 0:
                    # Validate the kustomization.yaml changed service name
                    list_git_diff_response = list_git_diff_response[0].split('\n')
                    print(f'Github diff response has {len(list_git_diff_response)} data')
                    ServiceChangedInFolder(base_version,current_version).get_diff_service_name(list_git_diff_response)
            elif process_type == 'count':
                argocd_pipeline_folder = 'argocd-pipelines/'
                kubernetes_manifests_folder = 'kubernetes-manifests/'
                if git_commands_class.checkout_branch(current_version.replace(git_origin, '')):
                    UpdatedChangesInArgoCDPipeline().updated_changes_in_argocd_pipeline(argocd_pipeline_folder, kubernetes_manifests_folder)
                print('Not implemented the count')
            else:
                print('Invalid process type requested...')

    else:
        print('Missing mandatory input argument data...')
# Using the special variable
# __name__
if __name__ == "__main__":
    main()
