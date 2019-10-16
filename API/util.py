import compute_model
import numpy as np


# Household
# one hot country
country_format = ["France", "Germany", "Italy", "Spain", "UK"]
# one hot type of housing
type_of_housing_format = ["Detached", "Semi detached",
                          "Attached single family home", "Flat"]
# heating energy resource
heating_energy_source_format = ['Coal', 'Natural Gas', 'Heating oil',
                                'Wood', 'Vegetable oil', 'Peat', 'Charcoal',
                                'No heating', 'Electricity']

# Transport
# one hot car usage list
car_usage_list_format = [0, "Gasoline", "Diesel", "Hybrid", "Electric"]

# Lifestyle
# one hot preferred diet
preferred_diet_list_format = ["Meat in most meals", "Meat in some meals",
                         "Meat very rarely/just fish", "Vegetarian", "Vegan"]
# one hot local product
local_product_list_format = ["Always", "Sometimes", "I'm not considering this option"]
# one hot buy from company
buy_from_companies_list_format = ["Always", "Sometimes", "I'm not considering this option"]


def onehotEncoding(inp, form):
    """This function return a one hot encoded vectors for
    every options/multiple-choice inputs"""
    return [0 if i != inp else 1 for i in form]


def mergeInput(json_dict):
    """This function get input from API as json format
    and convert to model's input"""
    # input of Household part
    household_input_value = getJsonHouseholdValues(json_dict)
    household_input_vector = onehotEncoding_Household(household_input_value)

    # input of Transport part
    transport_input_value = getJsonTransportValues(json_dict)
    transport_input_vector = onehotEncoding_Transport(transport_input_value)

    # input of Lifestyle part
    lifestyle_input_value = getJsonLifestyleValues(json_dict)
    lifestyle_input_vector = onehotEncoding_Lifestyle(lifestyle_input_value)

    return household_input_vector + transport_input_vector + lifestyle_input_vector


def getJsonLifestyleValues(json_dict):
    """This function get json_dict as input and get only lifestyle
        variables to one-hot"""
    # Lifestyle
    # 1. About your Lifestyle
    preferred_diet = json_dict["lifestyle"].get("preferred_diet")
    local_product = json_dict["lifestyle"].get("local_product")
    buy_from_companies = json_dict["lifestyle"].get("buy_from_companies")
    eat_out = json_dict["lifestyle"].get("eat_out")  # how many time a week

    # 2. How do you handle waste
    food = json_dict["lifestyle"].get("food")
    paper = json_dict["lifestyle"].get("paper")
    tincan = json_dict["lifestyle"].get("tincan")
    plastic = json_dict["lifestyle"].get("plastic")
    glass = json_dict["lifestyle"].get("glass")

    return [preferred_diet, local_product, buy_from_companies, eat_out,
            food, paper, tincan, plastic, glass]


def getJsonTransportValues(json_dict):
    """This function get json_dict as input and get only transport
        variables to one-hot"""
    # Transport
    # 1. How do you get around
    intercity_train = json_dict["transport"].get("intercity_train")  # Intercity Train
    subway = json_dict["transport"].get("subway")  # Subway
    intercity_bus = json_dict["transport"].get("intercity_bus")  # Intercity Bus
    city_bus = json_dict["transport"].get("city_bus")  # City Bus
    tram = json_dict["transport"].get("tram")  # Tram
    bike_walk = json_dict["transport"].get("bike_walk")  # Bike/Walk

    car_usage_list = json_dict["transport"].get("car_usage_list")  # "Please select" by default
    annual_mileage = json_dict["transport"].get("annual_mileage")  # Annual mileage
    average_consumption = json_dict["transport"].get("average_consumption")  # Average Consumption

    # 2. Private flights per year for all household members
    flight_very_long = json_dict["transport"].get("flight_very_long")  # very long flight
    flight_long = json_dict["transport"].get("flight_long")  # long flight
    flight_medium = json_dict["transport"].get("flight_medium")  # medium flight
    flight_short = json_dict["transport"].get("flight_short")  # short flight

    return [intercity_train, subway, intercity_bus, city_bus, tram, bike_walk,
            car_usage_list, annual_mileage, average_consumption,
            flight_very_long, flight_long, flight_medium, flight_short]


def getJsonHouseholdValues(json_dict):
    """This function get json_dict as input and get only household
    variables to one-hot"""
    # Householde
    # 1. About the household
    nr_of_people = json_dict["household"].get("nr_of_people")  # Number of people in the household
    country = json_dict["household"].get("country")  # Country of residence
    size_of_housing = json_dict["household"].get("size_of_housing")  # Size of housing (m2)
    type_of_housing = json_dict["household"].get("type_of_housing")  # Type of housing

    # Electricity consumption is 0 equals to "I don't know the KWh/month"
    # 2. Energy consumption
    electricity_consumption = json_dict["household"].get("electricity_consumption")  # electricity consumption
    clean_energy_source = json_dict["household"].get("clean_energy_source")  # clean energy source

    lightbulbs = json_dict["household"].get("lightbulbs")  # use energy efficient lightbulbs
    STAR = json_dict["household"].get("STAR")  # use ENERGY STAR appliances
    thermostat = json_dict["household"].get("thermostat")  # have a programmable/smart thermostat
    energy_saving_device = json_dict["household"].get("energy_saving_device")  # Energy-saving devices
    solar_water_heater = json_dict["household"].get("solar_water_heater")  # have a solar water heater

    heating_energy_source = json_dict["household"].get("heating_energy_source")  # Heating energy source
    return [nr_of_people, country, size_of_housing, type_of_housing,
            electricity_consumption, clean_energy_source,
            lightbulbs, STAR, thermostat, energy_saving_device, solar_water_heater,
            heating_energy_source]


def onehotEncoding_Lifestyle(input_data):
    """This function will pre-processing data and one-hot encoding it"""
    [preferred_diet, local_product, buy_from_companies, eat_out,
            food, paper, tincan, plastic, glass] = input_data

    # one hot preferred diet
    preferred_diet_list_vector = onehotEncoding(preferred_diet, preferred_diet_list_format)
    # one hot local product
    local_product_list_vector = onehotEncoding(local_product, local_product_list_format)
    # one hot buy from company
    buy_from_companies_list_vector = onehotEncoding(buy_from_companies, buy_from_companies_list_format)

    lifestyle_input_vector = preferred_diet_list_vector + local_product_list_vector + \
                             buy_from_companies_list_vector + [eat_out] + \
                             [food, paper, tincan, plastic, glass]

    # convert all value from json to int
    lifestyle_input_vector = [float(i) for i in lifestyle_input_vector]

    return lifestyle_input_vector


def onehotEncoding_Transport(input_data):
    """This function will pre-processing data and one-hot encoding it"""
    [intercity_train, subway, intercity_bus, city_bus, tram, bike_walk,
        car_usage_list, annual_mileage, average_consumption,
        flight_very_long, flight_long, flight_medium, flight_short] = input_data

    # one hot car usage list
    car_usage_list_vector = onehotEncoding(car_usage_list, car_usage_list_format)

    transport_input_vector = [intercity_train, subway, intercity_bus, city_bus, tram, bike_walk] + \
                             car_usage_list_vector + [annual_mileage, average_consumption] + \
                             [flight_very_long, flight_long, flight_medium, flight_short]

    # convert all value from json to int
    transport_input_vector = [float(i) for i in transport_input_vector]

    return transport_input_vector


def onehotEncoding_Household(input_data):
    """This function will pre-processing data and one-hot encoding it"""
    [nr_of_people, country, size_of_housing, type_of_housing,
        electricity_consumption, clean_energy_source,
        lightbulbs, STAR, thermostat, energy_saving_device, solar_water_heater,
        heating_energy_source] = input_data

    # one hot country code
    country_vector = onehotEncoding(country, country_format)
    # one hot type of housing
    type_of_housing_vector = onehotEncoding(type_of_housing, type_of_housing_format)
    # heating energy resources
    heating_energy_source_vector = onehotEncoding(heating_energy_source, heating_energy_source_format)

    household_input_vector = [nr_of_people] + country_vector + [size_of_housing] + type_of_housing_vector + \
                             [electricity_consumption, clean_energy_source] + \
                             [lightbulbs, STAR, thermostat, energy_saving_device, solar_water_heater] + \
                             heating_energy_source_vector

    # convert all value from json to int
    household_vector = [float(i) for i in household_input_vector]

    return household_vector


def calculateOutput(input):
    """This function calculate the output value via model"""
    X = np.reshape(input, (-1, 61))
    outp = compute_model.outp(X)
    return outp
