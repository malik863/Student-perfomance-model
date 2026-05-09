from django.shortcuts import render

# Create your views here.

# views.py

from django.shortcuts import render  # used to render HTML pages
from .forms import StudentForm 
from .models import StudentResponse
import numpy as np      # import the form we created
import joblib                        # to load the ML model
import os                            # to handle file paths
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


# Load the model ONCE when server starts (important for performance)
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'xgb_model2.pkl')  
# get path of model file inside the app folder

model = joblib.load(MODEL_PATH)  
# load trained ML model from file


from django.contrib.auth.models import User
from django.shortcuts import render, redirect



from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def signup(request):

    error = ""

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check empty fields
        if not username or not password:
            error = "Please fill all fields"

        # Check existing username
        elif User.objects.filter(username=username).exists():
            error = "Username already exists"

        else:
            User.objects.create_user(
                username=username,
                password=password
            )

            return redirect("login")

    return render(request, "signup.html", {"error": error})


def login_view(request):

    error = ""

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            error = "Please fill all fields"

        else:
            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
                login(request, user)
                return redirect("home")

            else:
                error = "Invalid username or password"

    return render(request, "login.html", {"error": error})


def logout_view(request):
    logout(request)
    return redirect("login")

def home(request):
    return render(request, "home.html")

def form(request):
    ...
    return render(request, "form.html", {"form": form})
# ==============================
# MAPPINGS (same as training)
# ==============================

freq_exercise = { "Never":0,
                   "Rarely (1-2 times a week)":1,
                    "Sometimes (3-4 times a week)":2,
                    "Often (5-6 times a week)":3,
                    "Every day":4
                    }

freq_dev_caffi = {"Never" : 0,
                  "Rarely (1-2 times a week)" :1,
                  "Sometimes (3-4 times a week)":2,
                  "Often (5-6 times a week)":3, 
                  "Always":4
}

freq_difficulty_wake = { "Never":0,
                   "Rarely (1-2 times a week)":1,
                    "Sometimes (3-4 times a week)":2,
                    "Often (5-6 times a week)":3,
                    "Every night":4
                    }

feq_classes = {"Never":0,
               "Rarely (1-2 times a month)":1,
               "Sometimes (1-2 times a week)":2,
                "Often (3-4 times a week)":3,
                "Always":4
                }

concentration_freq = {"Never" :0,
                      "Rarely":1,
                      "Sometimes":2,
                      "Often" :3,
                      "Always":4
                      }



sleep_quality_order = {"Poor":0, "Average":1, "Good":2, "Very good":3}
stress_order = {"No stress":0, "Low stress":1, "High stress":2, "Extremely high stress":3}

performance_order = {    
    "Poor":0,
    "Average":1,
    "Good":2,
    "Excellent":3}



# ==============================
# VIEW
# ==============================

@login_required
def predict(request):
    if request.method == "POST":
        form = StudentForm(request.POST)   # ✅ use form

        if form.is_valid():                            # ✅ validate first
            

            # ✅ get cleaned data (NOT request.POST)
            sleep = form.cleaned_data["sleep_difficulty"]
            wake = form.cleaned_data["wake_up"]
            concentration = form.cleaned_data["concentration"]
            fatigue = form.cleaned_data["fatigue"]
            skip = form.cleaned_data["skip_classes"]
            caffeine = form.cleaned_data["caffeine"]
            exercise = form.cleaned_data["exercise"]
            sleep_quality = form.cleaned_data["sleep_quality"]
            stress = form.cleaned_data["stress"]
            performance = form.cleaned_data["academic_performance"]

            # ==============================
            # Convert using maps
            # ==============================
            data = [
                freq_difficulty_wake.get(sleep, 0),
                freq_difficulty_wake.get(wake, 0),
                concentration_freq.get(concentration, 0),
                concentration_freq.get(fatigue, 0),
                feq_classes.get(skip, 0),
                freq_dev_caffi.get(caffeine, 0),
                freq_exercise.get(exercise, 0),
                sleep_quality_order.get(sleep_quality, 0),
                stress_order.get(stress, 0),
            ]

            data = np.array([data])

            # ==============================
            # Prediction
            # ==============================
            prediction = model.predict(data)[0]

            StudentResponse.objects.create(

                user=request.user,
                anonymous_id=request.user.userprofile.anonymous_id,

                sleep_difficulty=freq_difficulty_wake.get(sleep, 0),
                wake_up=freq_difficulty_wake.get(wake, 0),
                concentration=concentration_freq.get(concentration, 0),
                fatigue=concentration_freq.get(fatigue, 0),
                skip_classes=feq_classes.get(skip, 0),
                caffeine=freq_dev_caffi.get(caffeine, 0),
                exercise=freq_exercise.get(exercise, 0),
                sleep_quality=sleep_quality_order.get(sleep_quality, 0),
                stress=stress_order.get(stress, 0),

                prediction=prediction,
                academic_performance=performance_order.get(performance,0)

                )

            if prediction == 1:
                result = "High Risk"
            else:
                result = "Low Risk"

            # ==============================
            # Recommendations
            # ==============================
            

            recommendations = []

            risk_score = 0

            # Stress
            if stress_order.get(stress, 0) >= 2:
                risk_score += 2
                recommendations.append({
                    "priority": "high",
                    "icon": "🧠",
                    "title": "Stress Management",
                    "desc": "Your stress level appears high. Consider relaxation techniques and better study scheduling."
                })

            # Exercise
            if freq_exercise.get(exercise, 0) <= 1:
                risk_score += 1
                recommendations.append({
                    "priority": "medium",
                    "icon": "🏃",
                    "title": "Physical Activity",
                    "desc": "Regular exercise may improve concentration and reduce stress."
                })

            # Attendance
            if feq_classes.get(skip, 0) >= 2:
                risk_score += 2
                recommendations.append({
                    "priority": "high",
                    "icon": "📚",
                    "title": "Class Attendance",
                    "desc": "Frequent absence can negatively affect academic performance."
                })

            # Overall advice
            if risk_score >= 4:
                recommendations.append({
                    "priority": "high",
                    "icon": "🚨",
                    "title": "Academic Attention",
                    "desc": "You may benefit from academic counseling or additional support."
                })

            # Positive case
            if not recommendations:
                recommendations.append({
                    "priority": "low",
                    "icon": "✅",
                    "title": "Healthy Habits",
                    "desc": "Your current habits appear balanced. Keep maintaining them."
                })

            # Sort recommendations
            recommendations.sort(
                key=lambda x: {"high": 1, "medium": 2, "low": 3}[x["priority"]]
            )



            return render(request, "result.html", {
                "result": result,
                "recommendations": recommendations
        
            })
        else:
            print(form.errors.as_json())

    else:
        form = StudentForm()

    # ✅ IMPORTANT: return form with errors if invalid
    return render(request, "form.html", {"form": form})
