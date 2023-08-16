import random
import requests
import json
import torch

from chatbox.deep_learning_model import NeuralNet
from chatbox.nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('chatbox/intents.json', 'r') as f:
    intents = json.load(f)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

api_url = "https://api.data.gov/ed/collegescorecard/v1/schools/?school.operating=1&2020.student.size__range=1..&school.degrees_awarded.predominant__range=1..3&school.degrees_awarded.highest__range=2..4&api_key={{your_api_key}}"

def fetch_university_info():
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return data['results']
        else:
            print(f"Failed to fetch university data. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"An error occurred while fetching university data: {e}")
    
    return []

def format_dict_responses(response_data):
    def format_nested(data, level=0):
        indent = " " * (level * 2)
        formatted = ""

        for key, value in data.items():
            if isinstance(value, dict):
                formatted += f"{indent}{key} :\n"
                formatted += format_nested(value, level + 1)
            else:
                formatted += f"{indent}{key} - {value}\n"

        return formatted

    return format_nested(response_data)

def get_admission_requirements(university_data, sentence):
    for result in university_data:
        school_data = result.get('2020', {}).get('school', {})
        school_data = school_data.get('name').split()
        for name in school_data:
            if name in sentence:
                admissions_data = result.get('2020', {}).get('admissions', {})
                admission_requirements = {
                    'test_requirements': admissions_data.get('test_requiremetns'),
                    'admission_rate': admissions_data.get('admission_rate'),
                    'act_scores': admissions_data.get('act_scores'),
                    'sat_scores': admissions_data.get('sat_scores')
                }
                response = admission_requirements
                return response, name

def search_universities(university_data):
    all_schools = []
    for result in university_data:
        school_data = result.get('2020', {}).get('school', {})
        school_name = school_data.get('name')
        if school_name:
            all_schools.append(school_name)
        response = all_schools
    return response

def get_cost_requirements(university_data, sentence):
    for result in university_data:
        school_data = result.get('2020', {}).get('school', {})
        school_data = school_data.get('name').split()
        for name in school_data:
            if name in sentence:
                cost_data = result.get('2020', {}).get('cost', {})
                cost_requirements = {
                    'tuition': cost_data.get('tuition'),
                    'roomboard': cost_data.get('roomboard'),
                    'avg_net_price': cost_data.get('avg_net_price'),
                    'otherexpense': cost_data.get('otherexpense')
                }
                response = cost_requirements
                return response, name

def aid_information(university_data, sentence):
    for result in university_data:
        school_data = result.get('2020', {}).get('school', {})
        school_data = school_data.get('name').split()
        for name in school_data:
            if name in sentence:
                aid_data = result.get('2020', {}).get('aid', {})
                aid_info = {
                    'loan_principal': aid_data.get('loan_principal'),
                    'federal_loan_rate': aid_data.get('federal_loan_rate'),
                    'dependent_students': aid_data.get('dependent_students'),
                    'independent_students': aid_data.get('independent_students'),
                    'completers': aid_data.get('completers')
                }
                response = aid_info
                return response, name
    

def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    
    
    university_data = fetch_university_info()
    
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                if intent["tag"] == "search_universities":
                    universities = search_universities(university_data)
                    response = f"{random.choice(intent['responses'])}\n"
                    response += "\n".join([f"{i+1}. {university}" for i, university in enumerate(universities)])
                    return response

                elif intent["tag"] == "admission_requirements":
                    admission_requirements, school_name = get_admission_requirements(university_data, sentence)
                    response = f"{random.choice(intent['responses'])} {school_name}:\n"
                    response += format_dict_responses(admission_requirements)
                    return response
                
                elif intent["tag"] == "cost":
                    cost_requirements, school_name = get_cost_requirements(university_data, sentence)
                    response = f"{random.choice(intent['responses'])} {school_name}:\n"
                    response += format_dict_responses(cost_requirements)
                    return response
                
                elif intent["tag"] == "aid":
                    aid_info, school_name = aid_information(university_data, sentence)
                    response = f"{random.choice(intent['responses'])} {school_name}:\n"
                    response += format_dict_responses(aid_info)
                    return response
    
    return "I do not understand..."



# print("Let's chat! (type 'quit' to exit)")
# while True:
#     # sentence = "do you use credit cards?"
#     sentence = input("You: ")
#     if sentence == "quit":
#         break

#     resp = get_response(sentence)
#     print(resp)