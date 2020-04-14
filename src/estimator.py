def estimator(data):
  # Append regional data to input
  regionData = dict()
  regionData['name'] = 'Africa'
  regionData['avgAge'] = 19.7
  regionData['avgDailyIncomeInUSD'] = 5
  regionData['avgDailyIncomePopulation'] = 0.71

  data['region'] = regionData
 
  #setup input parameters
  period_type = str(data['period_type'])
  timeToElapse = int(data['timeToElapse'])
  reportedCases = int(data['reportedCases'])
  population = int(data['population'])
  totalHospitalBeds = int(data['totalHospitalBeds'])

  avgDailyIncomeInUSD = data['region']['avgDailyIncomeInUSD']
  avgDailyIncomePopulation = data['region']['avgDailyIncomePopulation']

  
  # setup output parameters
  impact = severImpact = dict()
  
  # estimates duration in days
  if periodType == 'months':
    noOfDays = timeToElapse*30
  elif periodType == 'weeks':
    noOfDays = timeToElapse*7
  else:
    noOfDays = timeToElapse

  impact['currentlyInfected'] = reportedCases*10
  severImpact['currentlyInfected'] = reportedCases*50

  # factor for number of infected people in a given day
  factor = int(noOfDays/3)

  impact['infectionsByRequestedTime'] = int(impact['currentlyInfected']*pow(2, factor))
  severImpact['infectionsByRequestedTime'] = int(severImpact['currentlyInfected']*pow(2, factor))

  # estimated number of severe positive cases
  impact['severeCasesByRequestedTime'] = int(0.15*impact['infectionsByRequestedTime'])
  severImpact['severeCasesByRequestedTime'] = int(0.15*severImpact['infectionsByRequestedTime'])

  # estimated number of available hospital beds for severe COVID-19 positive patients.
  impact['hospitalBedsByRequestedTime'] = totalHospitalBeds - impact['severeCasesByRequestedTime']
  severImpact['hospitalBedsByRequestedTime'] = totalHospitalBeds - severImpact['severeCasesByRequestedTime']

  # estimated number of severe positive cases that will require ICU care.
  impact['casesForICUByRequestedTime'] = int(0.05*impact['infectionsByRequestedTime'])
  severImpact['casesForICUByRequestedTime'] = int(0.05*severImpact['infectionsByRequestedTime'])

  # estimated number of severe positive cases that will require ventilators.
  impact['casesForVentilatorsByRequestedTime'] = int(0.02*impact['infectionsByRequestedTime'])
  severImpact['casesForVentilatorsByRequestedTime'] = int(0.02*severImpact['infectionsByRequestedTime'])

  # compute the average daily for specified period
  impact['dollarsInFlight'] = int((impact['infectionsByRequestedTime']*avgDailyIncomePopulation*avgDailyIncomeInUSD)/noOfDays)
  severImpact['dollarsInFlight'] = int((severImpact['infectionsByRequestedTime']*avgDailyIncomePopulation*avgDailyIncomeInUSD)/noOfDays)

  # Output data
  data = {
    'data': data,
    'impact': impact,
    'severImpact': severImpact
  }

  return data
