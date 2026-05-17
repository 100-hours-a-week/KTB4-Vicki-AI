import subprocess

def get_staged_files():
    result = subprocess.run(
        ['git', 'diff', '--cached', '--name-only'], 
        stdout=subprocess.PIPE, 
        text=True
        )

    files = result.stdout.strip().split('\n')

    return [file for file in files if file]