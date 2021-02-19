import sys
import subprocess

# package list must follow the installation guide in README.md
package_list = ('itur==0.2.1', 'tqdm==4.56.0', 'pandas==1.2.1', 'pathos==0.2.7', 'astropy==4.2', 'pyqt5==5.15.2')

for package in package_list:
    # implement pip as a subprocess:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',package])

    # process output with an API in the subprocess module:
    reqs = subprocess.check_output([sys.executable, '-m', 'pip','freeze'])
    installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

    print(installed_packages)

print('Process Completed!!!')