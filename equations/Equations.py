import json
from equations.constants import COUNTRIES, TYPES_OF_HOUSING, HEATING_ENERGY_SOURCES, FUEL_TYPES, PREFERED_DIET, LOCAL_PRODUCT, BUY_FROM_COMPANES
import zipfile

class Equations:
    
    def __init__(self):
        self.max_car = 4
        self.coeffs = {}
        with zipfile.ZipFile('./equations/metadataa.zip', 'r') as archive:
            with archive.open('metadataa', 'r') as file:
                self.coeffs = json.load(file)
            
    def get_results(cls, input_dicts):
        results = []
        for _dict in input_dicts:
            result = cls.get_result(_dict)
            results.append(result)
        return results
            
    def get_result(cls, input_dict):
        transport_offset = cls.transports_equation(input_dict)
        flights_offset = cls.flights_equation(input_dict)
        lifestyle_offset = cls.lifestyle_equation(input_dict)
        energy_offset = cls.energy_equation(input_dict)
        
        base_result = cls.base_equation(input_dict)
        base_total_annual = base_result['total_annual']
        base_country_average = base_result['country_average']
        base_world_average = base_result['world_average']
        
        total_annual = base_total_annual + transport_offset + flights_offset + lifestyle_offset + energy_offset
        
        return {'total_annual': total_annual,
                'country_average': base_country_average,
                'world_average': base_world_average}
    
    def get_root_key(cls, input_dict):
        nr_of_people = input_dict['household']['nr_of_people']
        country = input_dict['household']['country']
        type_of_housing = input_dict['household']['type_of_housing']
        heating_energy_source = input_dict['household']['heating_energy_source']
        preferred_diet = input_dict['lifestyle']['preferred_diet']
        local_product = input_dict['lifestyle']['local_product']
        buy_from_companies = input_dict['lifestyle']['buy_from_companies']
        
        key = str(COUNTRIES[country])
        key += ','
        key += nr_of_people
        key += ','
        key += str(TYPES_OF_HOUSING[type_of_housing])
        key += ','
        key += str(HEATING_ENERGY_SOURCES[heating_energy_source])
        key += ','
        key += str(PREFERED_DIET[preferred_diet])
        key += ','
        key += str(LOCAL_PRODUCT[local_product])
        key += ','
        key += str(BUY_FROM_COMPANES[buy_from_companies])
        return key
    
    def base_equation(cls, input_dict):
        root_key = cls.get_root_key(input_dict)
        size_of_housing = int(input_dict['household']['size_of_housing'])
        total_annual_25 = cls.coeffs[root_key + ',' + '25']['total_annual']
        total_annual_200 = cls.coeffs[root_key + ',' + '200']['total_annual']
        total_annual_500 = cls.coeffs[root_key + ',' + '500']['total_annual']
        total_annual_1000 = cls.coeffs[root_key + ',' + '1000']['total_annual']

        total_annual = 0
        if size_of_housing < 100:
            total_annual = total_annual_25 + (total_annual_200 - total_annual_25) / (200 - 25) * (size_of_housing - 25)
        elif size_of_housing < 200:
            total_annual = total_annual_200 - (total_annual_200 - total_annual_25) / (200 - 25) * (200 - size_of_housing)
        elif size_of_housing < 350:
            total_annual = total_annual_200 + (total_annual_500 - total_annual_200) / (500 - 200) * (size_of_housing - 200)
        elif size_of_housing < 500:
            total_annual = total_annual_500 - (total_annual_500 - total_annual_200) / (500 - 200) * (500 - size_of_housing)
        elif size_of_housing < 750:
            total_annual = total_annual_500 + (total_annual_1000 - total_annual_500) / (1000 - 500) * (size_of_housing - 500)
        else:
            total_annual = total_annual_1000 + (total_annual_1000 - total_annual_500) / (1000 - 500) * (1000 - size_of_housing)
        
        country_average = cls.coeffs[root_key + ',' + '25']['country_average']
        world_average = cls.coeffs[root_key + ',' + '25']['world_average']
        return {'total_annual': total_annual,
                'country_average': country_average,
                'world_average': world_average}
    
    def transports_equation(cls, input_dict):
        transport_annual = 0
        coeff = cls.coeffs['transports']
        # TransportViewModel.Intercity = 0.2652
        intercity_train_coeff = coeff['Intercity']
        intercity_train = intercity_train_coeff * int(input_dict['transport']['intercity_train'])
        transport_annual += intercity_train
        # TransportViewModel.Subway = 0.1014
        subway_coeff = coeff['Subway']
        subway = subway_coeff * int(input_dict['transport']['subway'])
        transport_annual += subway
        # TransportViewModel.Bus = 0.195
        intercity_bus_coeff = coeff['Bus']
        intercity_bus = intercity_bus_coeff * int(input_dict['transport']['intercity_bus'])
        transport_annual += intercity_bus
        # TransportViewModel.CityBus = 0.0718
        city_bus_coeff = coeff['CityBus']
        city_bus = city_bus_coeff * int(input_dict['transport']['city_bus'])
        transport_annual += city_bus
        # TransportViewModel.Tram = 0.0546
        tram_coeff = coeff['Tram']
        tram = tram_coeff * int(input_dict['transport']['tram'])
        transport_annual += tram
        # TransportViewModel.BikeWalk = ?
        bike_walk_annual = cls.bikewark_equation(input_dict)
        transport_annual += bike_walk_annual

        # car 0
        car_annual = cls.car_equation(input_dict)
        transport_annual += car_annual

        return transport_annual

    def flights_equation(cls, input_dict):
        flights_annual = 0
        coeff = cls.coeffs['transports']
        # TransportViewModel.VeryLongRangeFlight = 6.48
        flight_very_long_coeff = coeff['VeryLongRangeFlight']
        flight_very_long = flight_very_long_coeff * int(input_dict['transport']['flight_very_long'])
        flights_annual += flight_very_long
        # TransportViewModel.LongRangeFlight = 3.807
        flight_long_coeff = coeff['LongRangeFlight']
        flight_long = flight_long_coeff * int(input_dict['transport']['flight_long'])
        flights_annual += flight_long
        # TransportViewModel.MediumRangeFlight = 2.025
        flight_medium_coeff = coeff['MediumRangeFlight']
        flight_medium = flight_medium_coeff * int(input_dict['transport']['flight_medium'])
        flights_annual += flight_medium
        # TransportViewModel.ShortRangeFlight = 0.824
        flight_short_coeff = coeff['ShortRangeFlight']
        flight_short = flight_short_coeff * int(input_dict['transport']['flight_short'])
        flights_annual += flight_short

        return flights_annual

    def bikewark_equation(cls, input_dict):
        coeff = cls.coeffs['transports']
        nr_of_people = int(input_dict['household']['nr_of_people'])
        country = COUNTRIES[input_dict['household']['country']]
        bike_walk = int(input_dict['transport']['bike_walk'])

        bike_walk_annual = 0
        bike_walk_coeff = coeff["BikeWalk"][str(country)][str(nr_of_people)]
        if bike_walk < 16:
            bike_walk_annual += bike_walk_coeff * bike_walk
        else:
            bike_walk_annual += bike_walk_coeff * 15

        return bike_walk_annual

    def car_equation(cls, input_dict):
        coeff = cls.coeffs['transports']
        country = COUNTRIES[input_dict['household']['country']]
        # Have a car
        have_fuel_type_option = "fuel_type" in input_dict['transport']
        have_annual_mileage_field = "annual_mileage" in input_dict['transport']
        have_average_consomption_field = "average_consomption" in input_dict['transport']
        have_a_car = have_fuel_type_option and have_annual_mileage_field and have_average_consomption_field
        
        car_annual = 0
        if have_a_car:
            fuel_type = FUEL_TYPES[input_dict['transport']['fuel_type']]
            annual_mileage = int(input_dict['transport']['annual_mileage'])
            average_consomption = int(input_dict['transport']['average_consomption'])

            car_coeff = coeff["car"][str(country)][str(fuel_type)]
            fuel_consumption = annual_mileage * average_consomption / 100
            car_annual += fuel_consumption * car_coeff

        return car_annual
    
    def lifestyle_equation(cls, input_dict):
        nr_of_people = int(input_dict['household']['nr_of_people'])
        country = COUNTRIES[input_dict['household']['country']]
        coeff = cls.coeffs['lifestyle']
        lifestyle_annual = 0
        # "LifestyleViewModel.RecycleFood"
        lifestyle_annual += coeff['RecycleFood'][str(country)] * int(input_dict['lifestyle']['food'])
        # "LifestyleViewModel.RecyclePaper"
        lifestyle_annual += coeff['RecyclePaper'][str(country)] * int(input_dict['lifestyle']['paper'])
        # "LifestyleViewModel.RecycleTinCans"
        lifestyle_annual += coeff['RecycleTinCans'][str(country)] * int(input_dict['lifestyle']['tincan'])
        # "LifestyleViewModel.RecyclePlastic"
        lifestyle_annual += coeff['RecyclePlastic'][str(country)] * int(input_dict['lifestyle']['plastic'])
        # "LifestyleViewModel.RecycleGlass"
        lifestyle_annual += coeff['RecycleGlass'][str(country)] * int(input_dict['lifestyle']['glass'])
        # "LifestyleViewModel.MealsOut"
        eat_out = int(input_dict['lifestyle']['eat_out'])
        lifestyle_annual += coeff['MealsOut'] * eat_out * nr_of_people

        return lifestyle_annual
    
    def energy_equation(cls, input_dict):
        nr_of_people = int(input_dict['household']['nr_of_people'])
        country = COUNTRIES[input_dict['household']['country']]
        coeff = cls.coeffs['energy']
        energy_annual = 0
        clean_energy_source = int(input_dict['household']['clean_energy_source'])
        if "electricity_consumption" in input_dict['household']:
            electricity_consumption = int(input_dict['household']['electricity_consumption'])
            key = str(country) + str(nr_of_people)
            if electricity_consumption > 0:
                energy_annual += coeff['first_step'][key]
                not_clean_electricity_consumption = electricity_consumption * (100 - clean_energy_source) / 100
                energy_annual += coeff['energy'][str(country)] * not_clean_electricity_consumption
            else:
                if clean_energy_source > 0:
                    energy_annual += coeff['first_step'][key]
        else:
            for selection in cls.coeffs['energy_selection']:
                field = "HouseholdViewModel." + selection
                if form[field] == True:
                    not_know_0_key = str(country) + str(nr_of_people) + '.' + selection
                    not_know_0 = coeff['NotKnow_0'][not_know_0_key]
                    energy_annual += not_know_0 / 100 * (100 - CleanSource)
            
            # lightbulbs
            not_know_0_key = str(country) + str(nr_of_people) + '.' + "UsageLightbulbs"
            not_know_0 = coeff['NotKnow_0'][not_know_0_key]
            lightbulbs = input_dict['household']['lightbulbs']
            energy_annual += not_know_0 * lightbulbs * (100 - clean_energy_source) / 100
            # STAR
            not_know_0_key = str(country) + str(nr_of_people) + '.' + "UsageEnergyStar"
            not_know_0 = coeff['NotKnow_0'][not_know_0_key]
            star = input_dict['household']['STAR']
            energy_annual += not_know_0 * star * (100 - clean_energy_source) / 100
            # thermostat
            not_know_0_key = str(country) + str(nr_of_people) + '.' + "UsageThermostat"
            not_know_0 = coeff['NotKnow_0'][not_know_0_key]
            thermostat = input_dict['household']['thermostat']
            energy_annual += not_know_0 * thermostat * (100 - clean_energy_source) / 100
            # energy_saving_device
            not_know_0_key = str(country) + str(nr_of_people) + '.' + "UsageEnergySavingDevices"
            not_know_0 = coeff['NotKnow_0'][not_know_0_key]
            energy_saving_device = input_dict['household']['energy_saving_device']
            energy_annual += not_know_0 * energy_saving_device * (100 - clean_energy_source) / 100
            # solar_water_heater
            not_know_0_key = str(country) + str(nr_of_people) + '.' + "UsageSolarWaterHeater"
            not_know_0 = coeff['NotKnow_0'][not_know_0_key]
            solar_water_heater = input_dict['household']['solar_water_heater']
            energy_annual += not_know_0 * solar_water_heater * (100 - clean_energy_source) / 100
            
            not_know_100_key = str(country) + str(nr_of_people)
            not_know_100 = coeff['NotKnow_100'][not_know_100_key]
            energy_annual += not_know_100 * clean_energy_source / 100
 
        return energy_annual
