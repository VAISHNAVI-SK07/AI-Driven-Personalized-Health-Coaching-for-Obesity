# Simple AI Health Coach Logic
def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)

def get_recommendation(bmi):
    if bmi < 18.5:
        return "Underweight: Focus on nutrient-dense calorie intake."
    elif 18.5 <= bmi < 25:
        return "Normal weight: Maintain your current lifestyle!"
    elif 25 <= bmi < 30:
        return "Overweight: Increase daily steps and watch portion sizes."
    else:
        return "Obesity: Focus on a high-protein diet and 30 mins of daily walking."

# Testing the logic
user_weight = float(input("Enter your weight in kg: "))
user_height = float(input("Enter your height in cm: "))

bmi_result = calculate_bmi(user_weight, user_height)
plan = get_recommendation(bmi_result)

print(f"--- Your Results ---")
print(f"Your BMI is: {bmi_result}")
print(f"Coach Recommendation: {plan}")