from skfuzzy import control as ctrl
import skfuzzy as fuzz
import numpy as np

class microwave_oven:

    degree_cooked = ctrl.Antecedent(np.arange(0, 101, 1), 'degree_cooked')
    type_cooked = ctrl.Antecedent(np.arange(0, 101, 1), 'type_cooked')
    cook_time = ctrl.Consequent(np.arange(0, 61, 1), 'cook_time')

    degree_names = ['Low', 'Medium', 'High']
    type_names = ['NonFat', 'Medium', 'Fat']

    #Outputing them into auto-membership functions
    degree_cooked.automf(names=degree_names)
    type_cooked.automf(names=type_names)

    # Cooking Time Universe
    cook_time['very_short'] = fuzz.trimf(cook_time.universe, [0, 8, 12])
    cook_time['short'] = fuzz.trimf(cook_time.universe, [8, 12, 20])
    cook_time['medium'] = fuzz.trimf(cook_time.universe, [12, 20, 40])
    cook_time['long'] = fuzz.trimf(cook_time.universe, [20, 40, 60])
    cook_time['VeryLong'] = fuzz.trimf(cook_time.universe, [40, 60, 60])

    # Rule Application
    rule1 = ctrl.Rule(degree_dirt['High'] | type_cook['Fat'], cook_time['VeryLong'])
    rule2 = ctrl.Rule(degree_dirt['Medium'] | type_cook['Fat'], cook_time['long'])
    rule3 = ctrl.Rule(degree_dirt['Low'] | type_cook['Fat'], cook_time['long'])
    rule4 = ctrl.Rule(degree_dirt['High'] | type_cook['Medium'], cook_time['long'])
    rule5 = ctrl.Rule(degree_dirt['Medium'] | type_cook['Medium'], cook_time['medium'])
    rule6 = ctrl.Rule(degree_dirt['Low'] | type_cook['Medium'], cook_time['medium'])
    rule7 = ctrl.Rule(degree_dirt['High'] | type_cook['NonFat'], cook_time['medium'])
    rule8 = ctrl.Rule(degree_dirt['Medium'] | type_cook['NonFat'], cook_time['short'])
    rule9 = ctrl.Rule(degree_dirt['Low'] | type_cook['NonFat'], cook_time['very_short'])

    # Cooking Control Simulation
    cooking_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
    cooking = ctrl.ControlSystemSimulation(cooking_ctrl)

def fuzzify_food(fuzz_type,fuzz_degree):

    microwave_oven.washing.input['type_cook'] = fuzz_type
    microwave_oven.washing.input['degree_cooked'] = fuzz_degree

    microwave_oven.washing.compute()

    microwave_oven.cook_time.view(sim=microwave_oven.cooking)

    return microwave_oven.cooking output['cook_time']

microwave_oven.cooking.compute()
    microwave_oven.cook_time.view(sim=microwave_oven.washing)
