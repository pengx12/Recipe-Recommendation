import numpy as np
    #how to calculate macros per day: https://www.healthline.com/nutrition/how-to-count-macros#step-by-step
def Cal(height, weight, age, gender, fitness_goal, activity_level):
    # age = raw_input("Please insert your age( 3 < y <100 ):");
    # weight = raw_input("Please insert your weight(kg):");
    # height = raw_input("Please insert your height(cm):");  height should be count in [cm]
    # gender = raw_input("Please insert your gender(male/female):");
    # activity_level = raw_input("Please insert your activity level(Sedentary/LowActive/Active/VeryActvie/Extra_active):");
    Calories = 0

    if activity_level == 'Sedentary':
        PA = 1.2
    elif activity_level == 'LowActive':
        PA = 1.375
    elif activity_level == 'Active':
        PA = 1.55
    elif activity_level == 'High_active':
        PA = 1.725
    else:
        print ('unresolved activity level')

    if gender == 'male':
        if (age >= 20) and (age <= 60):
            Calories = PA * (10 * float(weight) + 6.25 * float(height) - 5 * float(age) + 5)
        else:
            print ('unresolved age value')
    elif gender == 'female':
        if (age >= 20) and (age <= 60):
            Calories = PA * (10 * float(weight) + 6.25 * float(height) - 5 * float(age) - 161)
        else:
            print ('unresolved age value')

    #weight factor for different fitness goals
    if fitness_goal == 'Lose Weight':
        Calories = Calories * 0.8
    elif fitness_goal == 'Keep Fit':
        Calories = Calories
    elif fitness_goal == 'Build Muscle':
        Calories = Calories * 1.2
    else:
        print('unresolved fitness_goal')

    return Calories


    #vitamins :https://health.gov/dietaryguidelines/2015-scientific-report/15-appendix-E3/e3-1-a4.asp
    #calories : Carb: 4 calories/g  Protein: 4 calories/g  Fat: 9 calories/g  Alcohol 7 calories/g
    #g_of_carb = g_of_protein = g_of_fat = 0
def nutrition(height, weight, age, gender, fitness_goal, activity_level):
    real_age = age
    Calories = Cal(height, weight, age, gender, fitness_goal, activity_level)
    Calories = Calories / 3  # divide into three meals
    if fitness_goal == 'Lose Weight':
        # 45% protein 40% cab 15% fat
        prot_cal = Calories * 0.45
        cab_cal = Calories * 0.4 
        fat_cal = Calories * 0.15


    elif fitness_goal == 'Keep Fit':
        prot_cal = Calories * 0.4
        cab_cal = Calories * 0.4 
        fat_cal = Calories * 0.2
    elif fitness_goal == 'Build Muscle':
        prot_cal = Calories * 0.4
        cab_cal = Calories * 0.5
        fat_cal = Calories * 0.2

    prot_weight = prot_cal / 4
    cab_weight = cab_cal / 4
    fat_weight = fat_cal / 9 * 2.5
    Fiber_weight = prot_weight * 0.3

    Macronutrients = {'Protein,g':str(prot_weight), 'Protein,kcal': str(prot_cal), 'Carbonhydrate,g': str(cab_weight),
                              'Carbonhydrate,kcal': str(cab_cal), 'DietaryFiber,g': str(Fiber_weight), 'AddedSugars,kcal': '<10%',
                              'TotalFat,kcal': str(fat_weight), 'SaturatedFat,kcal': '<10%', 'LinoleicAcid,g': '7',
                              'LinolenicAcid,g': '0.7'}

    if gender == 'male':
        if real_age > 3 and real_age <= 8:
            Minerals = {'Calcium,mg': '700', 'Iron,mg': '7', 'Magnesium,mg': '80', 'Phosphorus,mg': '460',
                        'Potassium,mg': '3000', 'Sodium,mg': '1500', 'Zinc,mg': '3', 'Copper,mcg': '340',
                        'Manganese,mg': '1.2', 'Selenium,mcg': '20'}
            Vitamins = {'Vitamin A, mg RAE': '300', 'Vitamin E,mg AT': '6', 'Vitamin D, IU': '600', 'Vitamin C, mg': '15',
                        'Thiamin, mg': '0.5', 'Riboflavin, mg': '0.5', 'Niacin, mg': '6', 'Vitamin B6, mg': '0.5',
                        'Vitamin B12, mcg': '0.9', 'Choline, mg': '200', 'Vitamin K, mcg': '30', 'Folate, mcg DFE': '150'}
        elif real_age > 8 and real_age <= 13:
            Minerals = {'Calcium,mg': '1300', 'Iron,mg': '8', 'Magnesium,mg': '240', 'Phosphorus,mg': '1250',
                'Potassium,mg': '4500', 'Sodium,mg': '2200', 'Zinc,mg': '8', 'Copper,mcg': '700', 'Manganese,mg': '1.9',
                'Selenium,mcg': '40'}
            Vitamins = {'Vitamin A, mg RAE': '600', 'Vitamin E,mg AT': '11', 'Vitamin D, IU': '600', 'Vitamin C, mg': '45',
                'Thiamin, mg': '0.9', 'Riboflavin, mg': '0.9', 'Niacin, mg': '12', 'Vitamin B6, mg': '1',
                'Vitamin B12, mcg': '1.8', 'Choline, mg': '250', 'Vitamin K, mcg': '55', 'Folate, mcg DFE': '200'}
        elif real_age > 13 and real_age <= 18:
            Minerals = {'Calcium,mg': '1300', 'Iron,mg': '11', 'Magnesium,mg': '410', 'Phosphorus,mg': '1250',
                    'Potassium,mg': '4700', 'Sodium,mg': '2300', 'Zinc,mg': '11', 'Copper,mcg': '890', 'Manganese,mg': '2.2',
                    'Selenium,mcg': '55'}
            Vitamins = {'Vitamin A, mg RAE': '900', 'Vitamin E,mg AT': '15', 'Vitamin D, IU': '600', 'Vitamin C, mg': '75',
                    'Thiamin, mg': '1.2', 'Riboflavin, mg': '1.3', 'Niacin, mg': '16', 'Vitamin B6, mg': '1.3',
                     'Vitamin B12, mcg': '2.4', 'Choline, mg': '550', 'Vitamin K, mcg': '75', 'Folate, mcg DFE': '400'}
        elif real_age > 18 and real_age <= 30:
            Minerals = {'Calcium,mg': '1000', 'Iron,mg': '8', 'Magnesium,mg': '400', 'Phosphorus,mg': '700', 'Potassium,mg': '4700',
                        'Sodium,mg': '2300', 'Zinc,mg': '11', 'Copper,mcg': '900', 'Manganese,mg': '2.3', 'Selenium,mcg': '55'}
            Vitamins = {'Vitamin A, mg RAE': '900', 'Vitamin E,mg AT': '15', 'Vitamin D, IU': '600', 'Vitamin C, mg': '90',
                        'Thiamin, mg': '1.2', 'Riboflavin, mg': '1.3', 'Niacin, mg': '16', 'Vitamin B6, mg': '1.3',
                        'Vitamin B12, mcg': '2.4', 'Choline, mg': '550', 'Vitamin K, mcg': '120', 'Folate, mcg DFE': '400'}
        elif real_age > 30 and real_age <= 50:
             Minerals = {'Calcium,mg': '1000', 'Iron,mg': '8', 'Magnesium,mg': '420', 'Phosphorus,mg': '700', 'Potassium,mg': '4700',
                          'Sodium,mg': '2300', 'Zinc,mg': '11', 'Copper,mcg': '900', 'Manganese,mg': '2.3', 'Selenium,mcg': '55'}
             Vitamins = {'Vitamin A, mg RAE': '900', 'Vitamin E,mg AT': '15', 'Vitamin D, IU': '600', 'Vitamin C, mg': '90',
                         'Thiamin, mg': '1.2', 'Riboflavin, mg': '1.3', 'Niacin, mg': '16', 'Vitamin B6, mg': '1.3',
                         'Vitamin B12, mcg': '2.4', 'Choline, mg': '550', 'Vitamin K, mcg': '120', 'Folate, mcg DFE': '400'}
        elif real_age > 50:
             Minerals = {'Calcium,mg': '1000', 'Iron,mg': '8', 'Magnesium,mg': '420', 'Phosphorus,mg': '700', 'Potassium,mg': '4700',
                         'Sodium,mg': '2300', 'Zinc,mg': '11', 'Copper,mcg': '900', 'Manganese,mg': '2.3', 'Selenium,mcg': '55'}
             Vitamins = {'Vitamin A, mg RAE': '900', 'Vitamin E,mg AT': '15', 'Vitamin D, IU': '600', 'Vitamin C, mg': '90',
                         'Thiamin, mg': '1.2', 'Riboflavin, mg': '1.3', 'Niacin, mg': '16', 'Vitamin B6, mg': '1.7',
                         'Vitamin B12, mcg': '2.4', 'Choline, mg': '550', 'Vitamin K, mcg': '120', 'Folate, mcg DFE': '400'}
        else:
             print ('error')
    if gender == 'female':
        if real_age > 3 and real_age <= 8:
             Minerals = {'Calcium,mg': '1000', 'Iron,mg': '10', 'Magnesium,mg': '130', 'Phosphorus,mg': '500',
                         'Potassium,mg': '3800', 'Sodium,mg': '1900', 'Zinc,mg': '5', 'Copper,mcg': '440',
                         'Manganese,mg': '1.5', 'Selenium,mcg': '30'}
             Vitamins = {'Vitamin A, mg RAE': '400', 'Vitamin E,mg AT': '7', 'Vitamin D, IU': '600',
                         'Vitamin C, mg': '25', 'Thiamin, mg': '0.6', 'Riboflavin, mg': '0.6',
                         'Niacin, mg': '8', 'Vitamin B6, mg': '0.6', 'Vitamin B12, mcg': '1.2',
                         'Choline, mg': '250', 'Vitamin K, mcg': '55', 'Folate, mcg DFE': '200'}
        elif real_age > 8 and real_age <= 13:
             Minerals = {'Calcium,mg': '1300', 'Iron,mg': '8', 'Magnesium,mg': '240', 'Phosphorus,mg': '1250',
                         'Potassium,mg': '4500', 'Sodium,mg': '2200', 'Zinc,mg': '8', 'Copper,mcg': '700',
                         'Manganese,mg': '1.6', 'Selenium,mcg': '40'}
             Vitamins = {'Vitamin A, mg RAE': '600', 'Vitamin E,mg AT': '11', 'Vitamin D, IU': '600',
            'Vitamin C, mg': '45', 'Thiamin, mg': '0.9', 'Riboflavin, mg': '0.9',
            'Niacin, mg': '12', 'Vitamin B6, mg': '1', 'Vitamin B12, mcg': '1.8',
            'Choline, mg': '375', 'Vitamin K, mcg': '60', 'Folate, mcg DFE': '300'}
        elif real_age > 13 and real_age <= 18:
             Minerals = {'Calcium,mg': '1300', 'Iron,mg': '15', 'Magnesium,mg': '360', 'Phosphorus,mg': '1250',
                         'Potassium,mg': '4700', 'Sodium,mg': '2300', 'Zinc,mg': '9', 'Copper,mcg': '890',
                        'Manganese,mg': '1.6', 'Selenium,mcg': '55'}
             Vitamins = {'Vitamin A, mg RAE': '700', 'Vitamin E,mg AT': '15', 'Vitamin D, IU': '600',
                         'Vitamin C, mg': '65', 'Thiamin, mg': '1', 'Riboflavin, mg': '1',
                         'Niacin, mg': '14', 'Vitamin B6, mg': '1.2', 'Vitamin B12, mcg': '2.4',
                         'Choline, mg': '400', 'Vitamin K, mcg': '75', 'Folate, mcg DFE': '400'}
        elif real_age > 18 and real_age <= 30:
            Minerals = {'Calcium,mg': '1000', 'Iron,mg': '18', 'Magnesium,mg': '310', 'Phosphorus,mg': '700',
                        'Potassium,mg': '4700', 'Sodium,mg': '2300', 'Zinc,mg': '8', 'Copper,mcg': '900',
                        'Manganese,mg': '1.8', 'Selenium,mcg': '55'}
            Vitamins = {'Vitamin A, mg RAE': '700', 'Vitamin E,mg AT': '15', 'Vitamin D, IU': '600',
                        'Vitamin C, mg': '75', 'Thiamin, mg': '1.1', 'Riboflavin, mg': '1.1',
                        'Niacin, mg': '14', 'Vitamin B6, mg': '1.3', 'Vitamin B12, mcg': '2.4',
                        'Choline, mg': '425', 'Vitamin K, mcg': '90', 'Folate, mcg DFE': '400'}
        elif real_age > 30 and real_age <= 50:
            Minerals = {'Calcium,mg': '1000', 'Iron,mg': '8', 'Magnesium,mg': '320', 'Phosphorus,mg': '700',
                        'Potassium,mg': '4700', 'Sodium,mg': '2300', 'Zinc,mg': '8', 'Copper,mcg': '900',
                        'Manganese,mg': '1.8', 'Selenium,mcg': '55'}
            Vitamins = {'Vitamin A, mg RAE': '700', 'Vitamin E,mg AT': '15', 'Vitamin D, IU': '600',
                        'Vitamin C, mg': '75', 'Thiamin, mg': '1.1', 'Riboflavin, mg': '1.1',
                        'Niacin, mg': '14', 'Vitamin B6, mg': '1.3', 'Vitamin B12, mcg': '2.4',
                        'Choline, mg': '425', 'Vitamin K, mcg': '120', 'Folate, mcg DFE': '400'}
        elif real_age > 50:

            Minerals = {'Calcium,mg': '1200', 'Iron,mg': '8', 'Magnesium,mg': '320', 'Phosphorus,mg': '700',
                        'Potassium,mg': '4700', 'Sodium,mg': '2300', 'Zinc,mg': '8', 'Copper,mcg': '900',
                        'Manganese,mg': '1.8', 'Selenium,mcg': '55'}
            Vitamins = {'Vitamin A, mg RAE': '700', 'Vitamin E,mg AT': '15', 'Vitamin D, IU': '600',
                        'Vitamin C, mg': '75', 'Thiamin, mg': '1.1', 'Riboflavin, mg': '1.1',
                        'Niacin, mg': '14', 'Vitamin B6, mg': '1.5', 'Vitamin B12, mcg': '2.4',
                        'Choline, mg': '425', 'Vitamin K, mcg': '90', 'Folate, mcg DFE': '400'}
        else:
             print ('error')

    Calories = Calories * 3
    nutrition_list = [Calories, Macronutrients['Protein,g'],  
                      Macronutrients['Carbonhydrate,g'],Macronutrients['DietaryFiber,g'], 
                      Macronutrients['TotalFat,kcal'], Minerals['Calcium,mg'], 
                      Minerals['Iron,mg'], Minerals['Magnesium,mg'],
                      Minerals['Phosphorus,mg'], Minerals['Potassium,mg'], Minerals['Sodium,mg'], Minerals['Zinc,mg'],
                      Minerals['Manganese,mg'], Minerals['Selenium,mcg'], Vitamins['Vitamin A, mg RAE'], Vitamins['Vitamin E,mg AT'],
                      Vitamins['Vitamin C, mg'],  Vitamins['Riboflavin, mg'],
                      Vitamins['Niacin, mg'], Vitamins['Vitamin B6, mg'], Vitamins['Vitamin B12, mcg'], Vitamins['Choline, mg'],
                      Vitamins['Vitamin K, mcg'], Vitamins['Folate, mcg DFE']]
    for i in range(len(nutrition_list)):
        nutrition_list[i]=float(nutrition_list[i])
    #print (nutrition_list)

    return nutrition_list

#print(nutrition(175, 55, 24, 'female', 'Build Muscle', 'Active'))