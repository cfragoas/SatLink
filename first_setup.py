import sys
import subprocess

# package list must follow the installation guide in README.md
package_list = ('itur', 'tqdm', 'pandas', 'pathos', 'astropy', 'pyqt5',
                'matplotlib')

for package in package_list:
    # implement pip as a subprocess:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',package])

    # process output with an API in the subprocess module:
    reqs = subprocess.check_output([sys.executable, '-m', 'pip','freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

    print(installed_packages)

print('Process Completed!!!')