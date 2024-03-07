from flask import Flask, render_template, request, redirect, url_for
import re
from datetime import datetime

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/results', methods=['POST'])
def results():
    log_data = request.form['logData']
    time_threshold = int(request.form['timeThreshold'])

    # Добавьте отладочные утверждения здесь
    print("Log Data:", log_data)
    print("Time Threshold:", time_threshold)

    # Регулярные выражения
    url_pattern = r'https://samsara\.yandex-team\.ru/ticket/\d+'
    time_pattern = r'Выполнен с (\d{2}:\d{2}:\d{2} \d{2}-\d{2}-\d{4}) по (\d{2}:\d{2}:\d{2} \d{2}-\d{2}-\d{4})'

    # Поиск и обработка данных
    urls = re.findall(url_pattern, log_data)
    times = re.findall(time_pattern, log_data)

    results = []
    for url, (start_time_str, end_time_str) in zip(urls, times):
        start_time = datetime.strptime(start_time_str, '%H:%M:%S %d-%m-%Y')
        end_time = datetime.strptime(end_time_str, '%H:%M:%S %d-%m-%Y')
        time_diff = round((end_time - start_time).total_seconds() / 60)

        if time_diff >= time_threshold:
            results.append((url, time_diff))
    print(results)
    return render_template('results.html', results=results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
