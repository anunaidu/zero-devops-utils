import subprocess
import os

class GithubDiffCommand:

    def __init__(self):
        print('GitHub Diff Command processing...')

    # find the difference of 2 version on a specific folder in git clone
    def git_diff_with_version_in_service_folder(self, base_branch, current_branch, diff_folder):
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

        return response