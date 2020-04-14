def estimator(data):
  # Append regional data to input
  regionData = dict()
  regionData['name'] = 'Africa'
  regionData['avgAge'] = 19.7
  regionData['avg_daily_income_in_usd'] = 5
  regionData['avg_daily_income_population'] = 0.71

  data['region'] = regionData
 
  #setup input parameters
  period_type = str(data['periodType'])
  time_to_elapse = int(data['timeToElapse'])
  reported_cases = int(data['reportedCases'])
  population = int(data['population'])
  total_hospital_beds = int(data['totalHospitalBeds'])

  avg_daily_income_in_usd = data['region']['avgDailyIncomeInUSD']
  avg_daily_income_population = data['region']['avgDailyIncomePopulation']

  
  # setup output parameters
  impact = severImpact = dict()
  
  # estimates duration in days
  if period_type == 'months':
    noOfDays = time_to_elapse*30
  elif period_type == 'weeks':
    noOfDays = time_to_elapse*7
  else:
    noOfDays = time_to_elapse

  impact['currentlyInfected'] = reported_cases*10
  severImpact['currentlyInfected'] = reported_cases*50

  # factor for number of infected people in a given day
  factor = int(noOfDays/3)

  impact['infectionsByRequestedTime'] = int(impact['currentlyInfected']*pow(2, factor))
  severImpact['infectionsByRequestedTime'] = int(severImpact['currentlyInfected']*pow(2, factor))

  # estimated number of severe positive cases
  impact['severeCasesByRequestedTime'] = int(0.15*impact['infectionsByRequestedTime'])
  severImpact['severeCasesByRequestedTime'] = int(0.15*severImpact['infectionsByRequestedTime'])

  # estimated number of available hospital beds for severe COVID-19 positive patients.
  impact['hospitalBedsByRequestedTime'] = total_hospital_beds - impact['severeCasesByRequestedTime']
  severImpact['hospitalBedsByRequestedTime'] = total_hospital_beds - severImpact['severeCasesByRequestedTime']

  # estimated number of severe positive cases that will require ICU care.
  impact['casesForICUByRequestedTime'] = int(0.05*impact['infectionsByRequestedTime'])
  severImpact['casesForICUByRequestedTime'] = int(0.05*severImpact['infectionsByRequestedTime'])

  # estimated number of severe positive cases that will require ventilators.
  impact['casesForVentilatorsByRequestedTime'] = int(0.02*impact['infectionsByRequestedTime'])
  severImpact['casesForVentilatorsByRequestedTime'] = int(0.02*severImpact['infectionsByRequestedTime'])

  # compute the average daily for specified period
  impact['dollarsInFlight'] = int((impact['infectionsByRequestedTime']*avg_daily_income_population*avg_daily_income_in_usd)/noOfDays)
  severImpact['dollarsInFlight'] = int((severImpact['infectionsByRequestedTime']*avg_daily_income_population*avg_daily_income_in_usd)/noOfDays)

  # Output data
  data = {
    'data': data,
    'impact': impact,
    'severImpact': severImpact
  }

  return data
