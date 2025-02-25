from flask import Flask, render_template, request, jsonify
import pickle
import joblib

app = Flask(__name__)
print("hello")


model = joblib.load('wilson_disease_model.pkl')



@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/do')
def do():
    return render_template("do.html")

@app.route('/portfolio')
def portfolio():
    return render_template("portfolio.html")

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        try:
            # Getting form data
            age = float(request.form.get('inputAge'))

            # Convert categorical variables to numerical values
            gender = 0 if request.form.get('inputGender').lower() == 'male' else 1
            kfr = 1 if request.form.get('inputKFR').lower() == 'yes' else 0
            psychiatric = 1 if request.form.get('inputPsychiatric').lower() == 'yes' else 0
            familyHis = 1 if request.form.get('inputFamilyHistory').lower() == 'yes' else 0
            aTB = 1 if request.form.get('inputGeneMutation').lower() == 'yes' else 0
            alcohol = 1 if request.form.get('inputAlcoholUse').lower() == 'yes' else 0

            socioeconomic_status_map = {'high': 2, 'medium': 1, 'low': 0}
            socioeconomic_status = socioeconomic_status_map.get(request.form.get('inputSocioeconomicStatus').lower(), 0)

            # Convert other numeric values
            cl = float(request.form.get('inputCeruloplasmin'))
            copperinblood = float(request.form.get('inputCopperBlood'))
            freecopper = float(request.form.get('inputFreeCopperBlood'))
            copperun = float(request.form.get('inputCopperUrine'))
            alt = float(request.form.get('inputALT'))
            ast = float(request.form.get('inputAST'))
            bili = float(request.form.get('inputTotalBilirubin'))
            albumin = float(request.form.get('inputAlbumin'))
            alp = float(request.form.get('inputALP'))
            time = float(request.form.get('inputProthrombin'))
            ggt = float(request.form.get('inputGGT'))
            neurological = float(request.form.get('inputNeurological'))
            cognitive = float(request.form.get('inputCognitive'))
            bmi = float(request.form.get('inputBMI'))

            # Create feature vector
            input_features = [[
                age, gender, cl, copperinblood, freecopper, copperun, alt, ast, bili, albumin, alp, 
                time, ggt, kfr, neurological, psychiatric, cognitive, familyHis, aTB, 
                socioeconomic_status, alcohol, bmi
            ]]

            

            # Make prediction
            prediction = model.predict(input_features)[0]

            # Debug: Print prediction
            print("Prediction:", prediction)

            # Return JSON response
            return jsonify({'prediction': int(prediction)})

        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'error': 'An error occurred during prediction. Please check your inputs.'}), 500



if __name__ == '__main__':
    app.run(debug=True)

