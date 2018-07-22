from werkzeug.datastructures import ImmutableMultiDict
from flask import Flask, render_template, request, redirect, url_for
import subprocess
import time
import os

app = Flask(__name__)


@app.route('/')
def bottle_code():
    return render_template('index.html')


@app.route('/output', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        papa = ''
        result = request.form
        result = result.to_dict(flat=False)

        with open('tempfiles/code.py', 'w') as f:
            f.write(result['ditor'][0])
        with open('tempfiles/input.txt', 'w') as f:
            f.write(result['input'][0])

        try:
            proc = subprocess.check_output('cat tempfiles/input.txt | timeout 2.6s python3 tempfiles/code.py', timeout=2.5, stdin=subprocess.PIPE, shell=True, stderr=subprocess.STDOUT)
            papa = proc
            error = 0
        except subprocess.CalledProcessError as e:
            papa = e.output
            error = 1
        except subprocess.TimeoutExpired as e:
            papa = b'TimeLimitExceed: "Code takes more then 2.5 seconds to execute"'
            error = 1
        print('proc  = , papa = {}'.format(papa))
        papa = papa.decode('utf-8')

        return render_template("output.html", papa=papa, error=error)

    else:
        return redirect(url_for('bottle_code'))


if __name__ == '__main__':
    host, port, debug = '0.0.0.0', 5000, True
    app.run(host, port, debug, threaded=True)
