import os

from cs50 import SQL
from flask import Flask, render_template, request

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///dogs.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    """Homepage"""
    return render_template("index.html")

@app.route("/survey", methods=["GET", "POST"])
def survey():
    """Survey page"""
    # User reached route via POST
    if request.method == "POST":
        survey_home = int(request.form.get("home"))
        survey_allergies = request.form.get("allergies")
        survey_kids = int(request.form.get("kids"))
        survey_shedding = int(request.form.get("shedding"))
        survey_drooling = int(request.form.get("drooling"))
        survey_grooming = int(request.form.get("grooming"))
        survey_experience = int(request.form.get("experience"))
        survey_train_time = int(request.form.get("train_time"))
        survey_walk_time = int(request.form.get("walk_time"))
        survey_activity = int(request.form.get("activity"))
        survey_reactivity = int(request.form.get("reactivity"))
        survey_patience1 = int(request.form.get("patience1"))
        survey_patience2 = int(request.form.get("patience2"))
        survey_patience = (survey_patience1 + survey_patience2)/2.0
        survey_time_alone = int(request.form.get("time_alone"))

        # Figure out apt. adaptability
        if survey_home >= 4:
            apt_ready = "can adapt to any size home"
        elif survey_home == 3:
            apt_ready = "needs some space to stretch their legs"
        elif survey_home <= 2:
            apt_ready = "not relevant"

        # Figure out kid friendliness
        if survey_kids <= 2:
            kid_friendly = "loves everyone"
        elif survey_kids == 3:
            kid_friendly = "likes a majority of kids"
        elif survey_kids == 4:
            kid_friendly = "indifferent"
        else:
            kid_friendly = "not relevant"

        # Figure out drooling
        if survey_drooling == 1:
            drooling = "little to none"
        elif survey_drooling == 2 or survey_drooling == 3:
            drooling = "some"
        else:
            drooling = "any amount"

        # Figure out shedding
        if survey_shedding == 1:
            shedding = "little to none"
        elif survey_shedding == 2 or survey_shedding == 3:
            shedding = "some"
        else:
            shedding = "any amount"

        # Figure out maintenance
        if survey_grooming <= 2:
            maintenance = "occasional brushing + grooming"
        elif survey_grooming == 3:
            maintenance = "weekly brushing + 4-6 groomings/year"
        else:
            maintenance = "daily brushing + 6-10 groomings/year"

        # Figure out trainability
        if (survey_experience == 3 and survey_train_time >= 3 and survey_patience > 2 and survey_reactivity == 1):
            trainability = "enjoys and needs multiple hours of daily mental stimulation"
            breed_trainability = 5
        elif (survey_experience == 3 and survey_train_time == 3 and survey_reactivity <= 2):
            trainability = "enjoy and needs multiple hours of daily mental stimulation"
            breed_trainability = 4
        elif (survey_experience == 2 and survey_train_time >= 2 and survey_patience >= 2 and survey_reactivity <= 2):
            trainability = "can learn basic cues, but not interested in much more"
            breed_trainability = 2
        elif (survey_experience == 2 and survey_train_time == 1 and survey_patience > 2 and survey_reactivity == 1):
            trainability = "teaching basic cues can be difficult"
            breed_trainability = 1
        else:
            trainability = "enjoys some daily mental stimulation"
            breed_trainability = 3

        # Figure out activity needs
        if (survey_experience == 3 and survey_activity == 4 and survey_walk_time == 4 and survey_time_alone == 1):
            activity = "requires several hours of daily physical activity"
            breed_activity = 5
        elif (survey_experience >= 2 and survey_activity >= 3 and survey_walk_time >= 3 and survey_time_alone == 1):
            activity = "requires several hours of daily physical activity"
            breed_activity = 4
        elif (survey_activity >= 2 and survey_walk_time >= 2 and survey_time_alone <= 2):
            activity = "requires 2-4 hours of daily physical activity"
            breed_activity = 3
        elif (survey_experience <= 2 and survey_activity == 2 and survey_walk_time == 2 and survey_time_alone <= 3):
            activity = "requires 1-2 hours of daily physical activity"
            breed_activity = 2
        else:
            activity = "requires under 1 hour of daily physical activity"
            breed_activity = 1

        # Figure out cases for no dog
        if survey_walk_time == 1 or survey_time_alone == 4 or survey_patience < 2 or survey_reactivity == 3 or survey_train_time == 1:
            return render_template("no_dog.html")

        # Query list of potential breeds from database based on hypoallergenic needs
        if survey_allergies == "Y":
            hypo = "yes"
            primary_breeds = db.execute("SELECT name FROM dogs WHERE apt_tolerant >= ? AND kid_friendly >= ? AND shedding <= ? AND drooling <= ? AND maintenance <= ? AND hypoallergenic = ? AND trainability <= ? AND activity <= ?",
            survey_home, survey_kids, (survey_shedding + 1), (survey_drooling + 1), (survey_grooming + 1), survey_allergies, breed_trainability, breed_activity)
            secondary_breeds = db.execute("SELECT name FROM dogs WHERE apt_tolerant >= ? AND kid_friendly >= ? AND shedding <= ? AND drooling <= ? AND maintenance <= ? AND hypoallergenic = ? AND trainability <= ? AND activity <= ?",
            survey_home, survey_kids, (survey_shedding + 2), (survey_drooling + 2), (survey_grooming + 2), survey_allergies, (breed_trainability + 1), (breed_activity + 1))

        else:
            hypo = "not necessarily"
            primary_breeds = db.execute("SELECT name FROM dogs WHERE apt_tolerant >= ? AND kid_friendly >= ? AND shedding <= ? AND drooling <= ? AND maintenance <= ? AND hypoallergenic = ? AND trainability <= ? AND activity <= ?",
            survey_home, survey_kids, (survey_shedding + 1), (survey_drooling + 1), (survey_grooming + 1), survey_allergies, breed_trainability, breed_activity)
            secondary_breeds = db.execute("SELECT name FROM dogs WHERE apt_tolerant >= ? AND kid_friendly >= ? AND shedding <= ? AND drooling <= ? AND maintenance <= ? AND hypoallergenic = ? AND trainability <= ? AND activity <= ?",
            survey_home, survey_kids, (survey_shedding + 2), (survey_drooling + 2), (survey_grooming + 2), survey_allergies, (breed_trainability + 1), (breed_activity + 1))

        # Take user to result
        return render_template("result.html", apt_ready=apt_ready, kid_friendly=kid_friendly, drooling=drooling, shedding=shedding,
         maintenance=maintenance, hypo=hypo, trainability=trainability, activity=activity, primary_breeds=primary_breeds, secondary_breeds=secondary_breeds)

    # User reached route via GET
    else:
        return render_template("survey.html")

