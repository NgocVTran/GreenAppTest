import compute_model
import numpy as np


# one hot type of housing
type_of_housing_format = ["Attached single family home", "Detached",
                          "Flat", "Semi detached"]
# heating energy resource
heating_energy_source_format = ['Charcoal', 'Coal', 'Electricity',
                                'Heating oil', 'Natural Gas', 'No heating',
                                'Peat', 'Vegetable oil', 'Wood']


def getJsonValues(json_dict):
    """This function get json dict as input and turn it
    into variables to one-hot"""
    # Householde
    # 1. About the household
    nr_of_people = json_dict.get("nr_of_people")  # Number of people in the household
    country = json_dict.get("country")  # Country of residence
    size_of_housing = json_dict.get("size_of_housing")  # Size of housing (m2)
    type_of_housing = json_dict.get("type_of_housing")  # Type of housing

    # always assume that "I don't know the KWh/month"
    # 2. Energy consumption
    lightbulbs = json_dict.get("lightbulbs")  # use energy efficient lightbulbs
    STAR = json_dict.get("STAR")  # use ENERGY STAR appliances
    thermostat = json_dict.get("thermostat")  # have a programmable/smart thermostat
    energy_saving_device = json_dict.get("energy_saving_device")  # Energy-saving devices
    solar_water_heater = json_dict.get("solar_water_heater")  # have a solar water heater

    heating_energy_source = json_dict.get("heating_energy_source")  # Heating energy source

    return [nr_of_people, size_of_housing, type_of_housing,
            lightbulbs, STAR, thermostat, energy_saving_device, solar_water_heater,
            heating_energy_source]


def onehotEncoding(input_data):
    """This function will pre-processing data and one-hot encoding it"""
    [nr_of_people, size_of_housing, type_of_housing,
         lightbulbs, STAR, thermostat, energy_saving_device, solar_water_heater,
         heating_energy_source] = input_data

    pp_per_squared_meters = [nr_of_people, size_of_housing]

    # one hot type of housing
    type_of_housing_vector = [0 if i != type_of_housing else 1
                              for i in type_of_housing_format]
    # energy consumption
    energy_consumption_vector = [lightbulbs, STAR, thermostat,
                                 energy_saving_device, solar_water_heater]
    # heating energy resource
    heating_energy_source_vector = [0 if i != heating_energy_source else 1
                                    for i in heating_energy_source_format]

    inp_vector = pp_per_squared_meters + type_of_housing_vector + \
                 energy_consumption_vector + heating_energy_source_vector

    # convert all value from json to int
    int_vector = [int(i) for i in inp_vector]

    return int_vector


def calculateOutput(input):
    """This function calculate the output value via model"""
    X = np.reshape(input, (-1, 20))
    outp = compute_model.outp(X)
    return outp
