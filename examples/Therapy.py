import os
import sys
import pyDMNrules

filename = 'Therapy.json'

if __name__ == '__main__':

    fileext = os.path.splitext(filename)[1]
    filePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)
    dmnRules = pyDMNrules.DMN()
    if fileext.lower() == '.xlsx':
        status = dmnRules.load(filePath)
    elif fileext.lower() == '.json':
        status = dmnRules.loadJson(filePath)
    else:
        print('Invalid file extension')
        sys.exit(0)
    if 'errors' in status:
        print(filename, 'has errors', status['errors'])
        sys.exit(0)
    else:
        print(filename, 'loaded')

    data = {}
    data['Patient Age'] = 56
    data['Patient Allergies'] = ['Penicillin', 'Streptomycin']
    data['Patient Creatinine Level'] = 2.0
    data['Patient Weight'] = 78
    data['Patient Active Medication'] = 'Coumadin'
    data['Encounter Diagnosis'] = 'Acute Sinusitis'
    print('Testing',repr(data))
    (status, newData) = dmnRules.decide(data)
    print('Decisions')
    for result in newData:
        print(repr(result))
        print()
    if 'errors' in status:
        print('With errors', status['errors'])
    print()

    if fileext.lower() == '.xlsx':
        (testStatus, results) = dmnRules.test()
    elif fileext.lower() == '.json':
        testFilePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'TherapyTest.json')
        (testStatus, results) = dmnRules.testJson(testFilePath)
    else:
        print('Invalid file extension')
        sys.exit(0)

    for test in range(len(results)):
        if 'Mismatches' not in results[test]:
            print('Test ID', results[test]['Test ID'], 'passed')
        else:
            print('Test ID', results[test]['Test ID'], 'failed')
            for failure in range(len(results[test]['Mismatches'])):
                print(results[test]['Mismatches'][failure])
            if 'TestAnnotations' in results[test]:
                print(results[test]['TestAnnotations'])
            if 'DataAnnotations' in results[test]:
                print(results[test]['DataAnnotations'])
            print(results[test]['data'])
            print(results[test]['newData'])
    if len(testStatus) > 0:
        print('with errors', repr(testStatus))
        sys.exit(0)

    print('Decisions (results)', results)
    print()
    print('Keys in a results list entry')
    print(results[-1].keys())
    for key in results[-1].keys():
        if isinstance(results[-1][key], dict):
            print('\t', "Keys in key '{!s}'".format(key), results[-1][key].keys())
            for subKey in results[-1][key].keys():
                if isinstance(results[-1][key][subKey], dict):
                    print('\t\t', "Keys in subKey '{!s}'".format(subKey), results[-1][key][subKey].keys())
    sys.exit(1)
