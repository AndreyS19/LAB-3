from flask import Flask, render_template, request,url_for
import math
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('openwindow.html')


@app.route('/solve', methods=['POST'])
def input():
    try:
        a = float(convert(request.form['a']))
        b = float(convert(request.form['b']))
        c = float(convert(request.form['c']))
        print(a,b,c)
        return solve(a,b,c)
    except:
        result='This is not quadratic equation!'
        return render_template('answerwindow.html',result=result)
def solve(a,b,c):
    s='x^2'
    m='x'
    f=''
    s = reverseconvert(a) + s
    m = trytoсonvert(m,b)
    f = trytoсonvert(f,c)
    equation=s+m+f
    d = math.pow(b, 2) - 4 * a * c
    if d < 0:
        realpart=-b/(2*a)
        complexpart=(math.sqrt(-d))/(2*a)
        x1="x1="+reverseconvert(complex(realpart,complexpart))
        x2="x2="+reverseconvert(complex(realpart,-complexpart))
        result="Complex solution!"

        return render_template('answerwindow.html',x1=x1,x2=x2,result=result,equation=equation)
    elif d == 0:
        x1 = -b / (2 * a)
        result = "One solution!"
        x1 = "x=" + reverseconvert(x1)
        return render_template('answerwindow.html', x1=x1,result=result,equation=equation)
    else:
        x1 ="x1="+reverseconvert((-b + math.sqrt(d)) / (2 * a))
        x2 ="x2="+reverseconvert((-b - math.sqrt(d)) / (2 * a))
        result = "Two solutions!"
        return render_template('answerwindow.html', x1=x1, x2=x2,result=result,equation=equation)
def convert(a):
    return str(a).replace(',', '.')
def reverseconvert(a):
    return str(a).replace('.', ',')
def trytoсonvert(a,elem):
    if elem==0.0:
        a = ''
        return a
    elif elem<0.0:
        a=reverseconvert(elem)+a
        return a
    elif elem>0.0:
        a = '+' + reverseconvert(elem)+a
        return a


def appstart():
    app.run(debug=True)