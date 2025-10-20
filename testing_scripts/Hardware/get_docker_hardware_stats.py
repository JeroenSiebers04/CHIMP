import subprocess

result = subprocess.run("docker stats --no-stream", capture_output=True, text=True)

output = result.stdout

print(output)