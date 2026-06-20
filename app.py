from flask import Flask,render_template,request
import pandas as pd
import joblib
import json
from datetime import datetime

app=Flask(__name__)

modelo=joblib.load("modelo.pkl")

paises={

"México":0,
"Estados Unidos":1,
"Canadá":2,
"España":3,
"Rusia":4,
"Nigeria":5

}

@app.route("/",methods=["GET","POST"])

def inicio():

    resultado=""

    if request.method=="POST":

        cliente=request.form["cliente"]

        monto=float(request.form["monto"])

        pais=request.form["pais"]

        hora=int(request.form["hora"])

        transacciones=int(request.form["transacciones_dia"])

        datos=pd.DataFrame([{

            "monto":monto,

            "pais":paises[pais],

            "hora":hora,

            "transacciones_dia":transacciones

        }])

        pred=modelo.predict(datos)[0]

        if pred==1:

            resultado="🚨 POSIBLE FRAUDE"

        else:

            resultado="✅ TRANSACCIÓN SEGURA"

        with open("historial.json","r",encoding="utf8") as archivo:

            historial=json.load(archivo)

        historial.append({

            "fecha":datetime.now().strftime("%d/%m/%Y %H:%M:%S"),

            "cliente":cliente,

            "monto":monto,

            "pais":pais,

            "hora":hora,

            "transacciones":transacciones,

            "resultado":resultado

        })

        with open("historial.json","w",encoding="utf8") as archivo:

            json.dump(historial,archivo,indent=4,ensure_ascii=False)

    return render_template("index.html",resultado=resultado)

@app.route("/historial")

def historial():

    with open("historial.json","r",encoding="utf8") as archivo:

        datos=json.load(archivo)

    return render_template("historial.html",datos=datos)

if __name__=="__main__":

    app.run(debug=True)
