from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def run_executable():
    result = subprocess.Popen('python main.py', shell=True, stdout=subprocess.PIPE)
    output = result.stdout.read()
    return render_template('output.html', output=output)

if __name__ == '__main__':
    app.run()
