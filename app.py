from shiny import ui, render, App
import seaborn as sns
import pandas as pd
import statsmodels.formula.api as smf
from shiny import reactive 

df = pd.read_csv('holistic_health_lifestyle_dataset.csv')

f = 'Overall_Health_Score ~ Sleep_Hours + Alcohol + Stress_Level + Mindfulness + Hydration + Physical_Activity + Smoking '
model = smf.ols(formula=f, data=df).fit()

band_ranges = (
    df.groupby("Health_Status")["Overall_Health_Score"].agg(["min", "max"])
)


app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_slider(
        "Sleep_Hours",
        "How many hours of sleep do you get normally?",
        min=0, max=10, value=5),
        ui.input_slider(
        "Mindfulness",
        "How many minutes of mindfulness do you practice a day?",
        min=0, max=60, value=30),
        ui.input_slider(
        "Hydration" ,
        "How many litres of water do you drink a day?",
        min=0.5, max=5, value=1),
        ui.input_slider(
        "Stress_Level" ,
        "How would you rate your stress levels out of 10 (10 being the highest)?",
        min=0, max=10, value=1),
        ui.input_slider( 
        "Physical_Activity",
        "How many minutes of exercise do you do a day?",
        min=0 , max= 120, value= 10),
        ui.input_slider(
        "Alcohol",
        "How many units of alcohol do you drink in a week?",
        min = 0, max = 20, value = 5),
        ui.input_slider(
        "Smoking", 
        "How many cigarettes do you smoke a day?",
        min = 0, max= 30, value = 1),
    ),
    ui.h1("What is Your Health Score"),
    ui.layout_columns(
        ui.card(
            ui.card_header("Distribution of Health Scores"),
            ui.output_plot("plot"),
            ui.card_header("Your Health Score"),
            ui.output_text_verbatim("value"),
        ),
    
    ui.input_slider("n", "Number of bins", 2, 100, 20), 
))


def server(input, output, session):

    user_score = reactive.Value(None)

    def categorize_score(score):
    row = band_ranges[(band_ranges["min"] <= score) & (band_ranges["max"] >= score)]
    if len(row) == 1:
        return row.index[0]
    else:
        return "Unknown"

    
    @output
    @render.plot(alt="Where does your health score fall on others health scores?")  
    def plot():  
        ax = sns.histplot(data= df, x="Overall_Health_Score", bins=input.n())  
        ax.set_title("Health Score Distribution")
        ax.set_xlabel("Health Score")
        ax.set_ylabel("Count")
        
        out_of_sample_data = pd.DataFrame([{
        'Sleep_Hours': input.Sleep_Hours(), 
        'Alcohol': input.Alcohol(),
        'Mindfulness': input.Mindfulness(),
        'Hydration' : input.Hydration(), 
        'Physical_Activity' : input.Physical_Activity(),
        'Smoking': input.Smoking(),
        'Stress_Level': input.Stress_Level()}])
        user_hs = model.predict(out_of_sample_data)
        user_score.set(user_hs[0])
        ax.axvline(user_hs[0], color= 'red')
        return ax  
    
    @output
    @render.text
    def value():
        score = user_score.get()

        if score is None:
            score_text = "Score not calculated yet."
        else:
            score_text = f"Predicted Health Score: {score:.2f}"

        return (
            f"Sleep: {input.Sleep_Hours()}, "
            f"Mindfulness: {input.Mindfulness()}, "
            f"Hydration: {input.Hydration()}, "
            f"Stress: {input.Stress_Level()}, "
            f"Exercise: {input.Physical_Activity()}, "
            f"Alcohol: {input.Alcohol()}, "
            f"Smoking: {input.Smoking()}\n\n"
            f"{score_text}"
        )
 

#App
app = App(app_ui, server)
