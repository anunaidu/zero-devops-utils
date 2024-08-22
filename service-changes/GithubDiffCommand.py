import subprocess
import os

class GithubDiffCommand:

    def __init__(self):
        print('GitHub Diff Command processing...')


    # find the difference of 2 version on a specific folder in git clone
    def git_diff_with_version_in_service_image(self, base_branch, current_branch, diff_folder):
        response = ''
        try:
            # Run the git diff command with the two versions and the specific folder
            result = subprocess.run(
                ['git', '-C', f'{os.path.expanduser("~")}/zero-deployment/', 'diff', base_branch, current_branch, '--',
                 diff_folder], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                print(f"Error: {result.stderr}")
            else:
                # Return the diff output
                response = result.stdout
        except Exception as e:
            print(f"Exception occurred: {str(e)}")

        return self.segregate_git_diff(response)

    def git_diff_with_version_in_service_folder(self, base_branch, current_branch, diff_folder):
        response = ''
        try:
            # Run the git diff command with the two versions and the specific folder
            result = subprocess.run(
                ['git', '-C', f'{os.path.expanduser("~")}/zero-deployment/', 'diff', '--name-status', base_branch, current_branch, '--',
                 diff_folder], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                print(f"Error: {result.stderr}")
            else:
                # Return the diff output
                response = result.stdout
        except Exception as e:
            print(f"Exception occurred: {str(e)}")

        return self.segregate_git_diff(response)

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
