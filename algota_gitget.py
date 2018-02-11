import os, requests, shlex, subprocess

os.chdir('/Users/dg/Desktop/algo')


url = "https://git.unl.edu/api/v3/projects?private_token=AEb_5yDVwLmAJumEctJf"
project_list = requests.get(url).json()

print(len(project_list))

for project in project_list:


    try:
        command = shlex.split(f'git clone {project["ssh_url_to_repo"]}')
        file = ['./' + project['owner']['name'].replace(' ', '_') + project['name']]
        subprocess.Popen(command + file)

    except Exception as e:
        print("Error on {file}")




