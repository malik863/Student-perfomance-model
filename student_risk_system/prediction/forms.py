# forms.py

from django import forms  # import Django forms system

# Define ordered categories
CAFFIENE = [ ("Never","Never"),
                  ("Rarely (1-2 times a week)","Rarely (1-2 times a week)"),
                  ("Sometimes (3-4 times a week)","Sometimes (3-4 times a week)"),
                  ("Often (5-6 times a week)","Often (5-6 times a week)"),
                  ("Always","Always")]



EXERCISE = {( "Never", "Never"),
                 ("Rarely (1-2 times a week)","Rarely (1-2 times a week)"),
                 ("Sometimes (3-4 times a week)","Sometimes (3-4 times a week)"),
                 ("Often (5-6 times a week)","Often (5-6 times a week)"),
                 ("Every day","Every day")}




DIFFICULTY = [("Never","Never"),
                        ("Rarely (1-2 times a week)","Rarely (1-2 times a week)"),
                        ("Sometimes (3-4 times a week)","Sometimes (3-4 times a week)"),
                        ("Often (5-6 times a week)","Often (5-6 times a week)"),
                        ("Every night","Every night") ]



CLASSES = [("Never","Never"),
               ("Rarely (1-2 times a month)","Rarely (1-2 times a month)"),
               ("Sometimes (1-2 times a week)","Sometimes (1-2 times a week)"),
               ("Often (3-4 times a week)","Often (3-4 times a week)"),
               ("Always","Always") ]



                

CONCENTRATION = [("Never","Never"),("Rarely","Rarely"),("Sometimes","Sometimes"),("Often","Often"),("Always","Always")]

 
                      
FREQUENCY_CHOICES = [
    ("Never", "Never"),
    ("Rarely (1-2 times a week)", "Rarely (1-2/week)"),
    ("Rarely (1-2 times a month)", "Rarely (1-2/month)"),
    ("Sometimes (3-4 times a week)", "Sometimes"),
    ("Often (5-6 times a week)", "Often"),
    ("Every night", "Every night"),
    ("Always", "Always"),
]

SLEEP_QUALITY_CHOICES = [
    ("Poor", "Poor"),
    ("Average", "Average"),
    ("Good", "Good"),
    ("Very good", "Very good"),
]

STRESS_CHOICES = [
    ("No stress", "No stress"),
    ("Low stress", "Low stress"),
    ("High stress", "High stress"),
    ("Extremely high stress", "Extremely high stress"),
]

PERFORMANCE_CHOICES = [
    ("Excellent", "Excellent"),
    ("Good", "Good"),
    ("Average", "Average"),
    ("Poor", "Poor"),
]

class StudentForm(forms.Form):
    sleep_difficulty = forms.ChoiceField(choices=DIFFICULTY)
    wake_up = forms.ChoiceField(choices=DIFFICULTY)
    concentration = forms.ChoiceField(choices=CONCENTRATION)
    fatigue = forms.ChoiceField(choices=CONCENTRATION)
    skip_classes = forms.ChoiceField(choices=CLASSES)
    caffeine = forms.ChoiceField(choices=CAFFIENE)
    exercise = forms.ChoiceField(choices=EXERCISE)
    sleep_quality = forms.ChoiceField(choices=SLEEP_QUALITY_CHOICES)
    stress = forms.ChoiceField(choices=STRESS_CHOICES)
    academic_performance = forms.ChoiceField(choices=PERFORMANCE_CHOICES , required=False)






