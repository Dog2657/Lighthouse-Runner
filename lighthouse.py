import subprocess
import platform
import sys 
import re
import os

urlPattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

def runCommand(*args, errorMessage: str = ''):
    try:
        subprocess.run(args=args, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"{errorMessage}: {e}")

def check_npm_package_installation(package_name):
    try:
        result = subprocess.run(['npm', 'list', '-g'], capture_output=True, text=True)
        if package_name in result.stdout:
            return True
        else:
            return False
    except FileNotFoundError:
        raise RuntimeError("npm command not found. Make sure Node.js and npm are installed.")
    
def hasArg(arg: str):
    return any(item.lower() == f'--{arg}' for item in sys.argv[1:])

def detect_os():
    os_name = platform.system()
    if os_name == "Darwin":
        return "macOS"
    elif os_name == "Windows":
        return "Windows"
    elif os_name == "Linux":
        return "Linux"
    else:
        return "Unknown"

forceCommand = ''
match detect_os():
    case "macOS":
        forceCommand = 'sudo'
        
    case "Linux":
        forceCommand = 'sudo'
   
def log(message: str):
    print('\n')
    print(message)

urls = [url for item in sys.argv[1:] for url in re.findall(urlPattern, item)]

if(not check_npm_package_installation('lighthouse')):
    log("Installing google lighthouse by npm:")
    runCommand(forceCommand, 'npm', 'install', '-g', 'lighthouse')

log('Running lighthouse:')
runCommand('lighthouse', '--view', '--output-path=./lighthouse.html', urls[0])

if(hasArg('delete')):
    log('Clearing lighthouse.html:')
    os.remove("lighthouse.html") 
