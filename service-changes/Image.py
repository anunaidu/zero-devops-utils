import argparse
from GithubDiffCommand import GithubDiffCommand
from ServiceChangedInImage import ServiceChangedInImage


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
    base_version = vInputs.basebranch
    current_version = vInputs.currentbranch
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

        github_diff_command_class = GithubDiffCommand()

        for process_type in list_process_type:
            if process_type == 'image':
                diff_folder = ''
                list_git_diff_response = github_diff_command_class.git_diff_with_version_in_service_folder(base_version, current_version, diff_folder)
                if list_git_diff_response is not None and len(list_git_diff_response) > 0:
                    # Validate the kustomization.yaml changed service name
                    ServiceChangedInImage().get_diff_service_name(list_git_diff_response)
                else:
                    print(f'process type {process_type} has no github diff response to process')

            elif process_type == 'folder':
                diff_folder = ''
                list_git_diff_response = github_diff_command_class.git_diff_with_version_in_service_folder(base_version, current_version, diff_folder)
                if list_git_diff_response is not None and len(list_git_diff_response) > 0:
                    # Validate the kustomization.yaml changed service name
                    print('')
            elif process_type == 'count':
                print('')
            else:
                print('Invalid process type requested...')

    else:
        print('Missing mandatory input argument data...')
# Using the special variable
# __name__
if __name__ == "__main__":
    main()