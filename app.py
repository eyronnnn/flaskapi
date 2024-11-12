from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # First page content

@app.route('/page1')
def page1():
    return render_template('secondpage.html')  # Second page content

@app.route('/get-file-input')
def get_file_input():
    return render_template('components/fileinput.html')

@app.route('/get-batchscanreminder')
def get_batchscanreminder():
    return render_template('components/batchscanreminder.html')

if __name__ == '__main__':
    app.run(debug=True)
