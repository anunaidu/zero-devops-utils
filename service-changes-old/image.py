import os
from datetime import datetime
import subprocess
import argparse
import csv


class ServiceChangeInImage:
    def __init__(self):
        # current working directory of python file
        self.currentDirectory = os.getcwd()
        # csv file path to store output of comparison
        self.csvFilePath = os.path.join(self.currentDirectory, f'service-changes-{datetime.now().strftime("%d-%m-%Y-%H-%M-%S")}.csv')


    # find the difference of 2 version on a specific folder in git clone
    def git_diff_with_version_in_service_folder(self, base_branch, current_branch, diff_folder):
        try:
            # Run the git diff command with the two versions and the specific folder
            result = subprocess.run(['git', '-C', f'{os.path.expanduser("~")}/zero-deployment/', 'diff', base_branch, current_branch, '--', diff_folder], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            #git_diff_command = ["git", "-C", "~/zero-deployment", "diff", f"{version_1}:{folder_to_diff}", f"{version_2}:{folder_to_diff}"]
			# Check for errors
            if result.returncode != 0:
                print(f"Error: {result.stderr}")
            else:
                # Return the diff output
                list_git_diff_response = self.segregate_git_diff(result.stdout)
                if list_git_diff_response is not None and len(list_git_diff_response) > 0:
                    list_service_name = self.get_diff_service_name(list_git_diff_response)
                    self.write_service_name_to_csv(list_service_name)
        except Exception as e:
            print(f"Exception occurred: {str(e)}")

    def test(self):
        file = open('Test.txt', 'r')
        response = file.read()
        file.close()
        list_git_diff_response = self.segregate_git_diff(response)
        if list_git_diff_response is not None and len(list_git_diff_response) > 0:
            list_service_name = self.get_diff_service_name(list_git_diff_response)
            self.write_service_name_to_csv(list_service_name)

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

        return list_service_name

    def write_service_name_to_csv(self, list_service_name):
        with open(self.csvFilePath, mode='w', newline="") as file:
            wr = csv.writer(file, delimiter=',')
            wr.writerow(['Service Changed'])
            for x in list_service_name:
                wr.writerow([x])
            file.close()
        print('Service changed data saved into csv file at location \n', self.csvFilePath)

    def segregate_git_diff(self, diff_response):
        list_git_diff_response = []
        if diff_response is not None or diff_response != '':
            # split the response with new line to segregate the data into list
            list_response = diff_response.split('\n')
            # variable to segregate the data from diff --git
            diff_git_data = ''
            # loop the response data to segregate based on the diff -git key
            for data in list_response:
                if 'diff --git' in data:
                    # add data to list if next diff --git keyword occurs
                    if diff_git_data != '':
                        list_git_diff_response.append(diff_git_data)
                    # reset when next diff --git keyword occurs
                    diff_git_data = ''

                # collect all the diff --git data into one string
                diff_git_data = (diff_git_data + '\n' + data).strip()

            # add data to list if last diff --git keyword occurs
            if diff_git_data != '':
                list_git_diff_response.append(diff_git_data)

        return list_git_diff_response

def read_inputs():
     vParser = argparse.ArgumentParser(description='Read input arguments')
     vParser.add_argument('-basebranch', '-bb', type=str, help='pass the base branch with version', required=True)
     vParser.add_argument('-currentbranch', '-cb', type=str, help='pass the current branch with version', required=True)
     vParser.add_argument('-difffolder', '-df', type=str, help='enter relative path of the git folder', required=True)

     vSubParsers = vParser.add_subparsers(title='Mandatory Sub Options', dest='process_type', help='Choose a sub option')

     image = vSubParsers.add_parser('image',help='List out the services that has changes in Image [Kustomization.yaml]')
     image.add_argument("-image", "-image", type=str, default=False)

     vSubParsers.required = True

     return vParser.parse_args()

# Defining main function
def main():

    vInputs = read_inputs()
    base_version = vInputs.basebranch
    current_version = vInputs.currentbranch
    diff_folder = vInputs.difffolder
    process_type = vInputs.process_type

    print(base_version, current_version, diff_folder, process_type)

    if process_type == 'image':
        ServiceChangeInImage().git_diff_with_version_in_service_folder(base_version, current_version, diff_folder)
    elif process_type == '':
        print('')
    else:
        print('')

# Using the special variable
# __name__
if __name__ == "__main__":
    main()
