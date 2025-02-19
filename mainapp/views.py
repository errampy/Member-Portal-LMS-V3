from django.shortcuts import render,redirect

from mainapp.scripts import validate_refinance_form, validate_restructure_form
from .forms import *
from .api_call import *
from datetime import *
from django.http import JsonResponse
import json
import logging
from json import *
# baseurl = 'http://127.0.0.1:9000/'

# service_api_url = 'micro-service1/'
url='http://127.0.0.1:9000/micro-service1/'
# url='https://bblmsv2be.pythonanywhere.com/micro-service1/'

import json
from django.shortcuts import render

import json

import json
from django.shortcuts import render

def dashboard(request):
    id_number = request.session.get('id_number')  
    member = request.session.get('member')

    # Ensure loanapp is in session
    if 'loanapp' not in request.session or not request.session['loanapp']:
        if member and 'code' in member:
            code1 = member['code']
            dict1 = {
                "ms_id": "MS18023016",#create portal member
                "ms_payload": {"code": code1}
            }
            json_data = json.dumps(dict1)
            response1 = call_post_method_without_token(url, json_data)
            if response1.status_code == 200:
                response_data = json.loads(response1.content)
                loanapp = response_data[0] if response_data else None
                request.session['loanapp'] = loanapp
            else:
                loanapp = None
        else:
            loanapp = None
    else:
        loanapp = request.session['loanapp']

    # Your existing logic to process loanapp data
    desired_data = {
        "paid_count": 0,
        "pending_count": 0,
        "amount_paid": 0,
        "amount_pending": 0,
        "total_repayment": 0,
    }
    loan_amount = 0
    wallet_balance=0
    cashbook_balance=0

    if loanapp and 'application_id' in loanapp:
        code1 = loanapp['application_id']
        dict1 = {
            "ms_id": "MS18029242", #counts for dashboard member
            "ms_payload": {"code": code1}
        }
        json_data = json.dumps(dict1)
        try:
            response1 = call_post_method_without_token(url, json_data)
            data = json.loads(response1.content)
            print('response1',response1.content)
            wallet_balance = data.get("wallet_balance", 0)
            cashbook_balance =data.get("cashbook_balance", 0)
            if "loan_amount" in data:
                loan_amount = data["loan_amount"]
            if "applications_with_repayment_counts" in data and data["applications_with_repayment_counts"]:
                repayment_data = data["applications_with_repayment_counts"][0]
                desired_data = {
                    "loan_amount": loan_amount,
                    "paid_count": repayment_data.get("paid_count", 0),
                    "pending_count": repayment_data.get("pending_count", 0),
                    "amount_paid": repayment_data.get("amount_paid", 0),
                    "amount_pending": repayment_data.get("amount_pending", 0),
                    "total_repayment": repayment_data.get("paid_count", 0) + repayment_data.get("pending_count", 0),
                }
        except Exception as e:
            print(f"Error fetching loan data: {e}")

    return render(request, 'dashboard.html', {
        'id_number': id_number,
        'member': member,
        'desired_data': desired_data,
        'loan_amount': loan_amount,
        'wallet_balance':wallet_balance,
        'cashbook_balance':cashbook_balance
    })

def member_profile(request):
    id_number = request.session.get('id_number')  # Retrieve id_number from session
    member = request.session.get('member')
    return render(request,'member_profile.html',{'member':member}) 
     
def image_filescreate(cleaned_data):
    files = {}
    fields_to_remove = []

    # Identify and separate file fields
    for field_name, value in cleaned_data.items():
        if hasattr(value, 'read'):  # Check if it's a file-like object
            files[field_name] = (value.name, value, value.content_type)
            fields_to_remove.append(field_name)

    # Remove file fields from cleaned_data
    for field_name in fields_to_remove:
        cleaned_data.pop(field_name)
    # Return files and the modified cleaned_data
    return files,cleaned_data

from django.shortcuts import render, redirect
import json

def login(request):
    form = LoginForm()
    error_message = None  # Default error message

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            id_number = str(cleaned_data['id_number'])  
            request.session['id_number'] = id_number  

            dict1 = {
                "ms_id": "MS18021697", #view member single
                "ms_payload": {
                    "code": str(cleaned_data['id_number']),
                }
            }
            json_data = json.dumps(dict1)
            response1 = call_post_method_without_token(url, json_data)
            print('response1',response1)
            print('response1 json',response1.json)
            if response1.status_code == 200:
                response=response1.content
                print('response',response)
                response_data = json.loads(response)
                member = response_data[0].get('member')
                print('member',member)
                request.session['member'] = member
                return redirect('verify')  
            else:
                error_message = "Either you are not a registered member or your under approval process"

    return render(request, 'login1.html', {'form': form, 'error_message': error_message})

def register(request):
    form=RegisterForm()
    return render(request,'register.html',{'form':form}) 

def verify(request):
    return render(request,'verify.html') 

def basic(request):
    form=UserRegistrationForm()
    return render(request,'basic.html',{'form':form}) 


def download(request):
    return render(request,'download.html') 


import json

def account_entry(request):
    member = request.session.get('member')
    record_details = []  

    form = StatementForm()
    error_message = None  # Default error message

    if request.method == 'POST':
        form = StatementForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            id_number = str(cleaned_data['applicant_id'])  
            request.session['id_number'] = id_number  

            dict1 = {
                "ms_id": "MS18022681", #entry statement
                "ms_payload": {
                    "applicant_id": id_number,
                }
            }
            json_data = json.dumps(dict1)
            response1 = call_post_method_without_token(url, json_data)
            
            if response1.status_code == 200:
                # Properly decode the response
                record_details = json.loads(response1.content.decode('utf-8'))
                print('Parsed Response:', record_details)
            else:
                error_message = "Either you are not a registered member or you're under the approval process."

    context = {
        "form": form,
        "record_details": record_details,  # Now properly formatted
        "error_message": error_message,
    }  
    return render(request, 'account_entry.html', context)


def loan_statement(request):
    member = request.session.get('member')
    record_details = []  

    form = LoanStatementForm()
    error_message = None  # Default error message

    if request.method == 'POST':
        form = LoanStatementForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            applicant_id = str(cleaned_data['applicant_id'])  
            loan_id = str(cleaned_data['loan_id'])  

            dict1 = {
                "ms_id": "MS12024740",
                "ms_payload": {
                    "applicant_id": applicant_id,
                    'loan_id':loan_id
                }
            }
            json_data = json.dumps(dict1)
            response1 = call_post_method_without_token(url, json_data)
            
            if response1.status_code == 200:
                # Properly decode the response
                record_details = json.loads(response1.content.decode('utf-8'))
                print('Parsed Response:', record_details)
            else:
                error_message = "Either you are not a registered member or you're under the approval process."

    context = {
    "form": form,
    "record_details": record_details,  # Now properly formatted
    "error_message": error_message,
}  

    return render(request,'loan_statement.html',context) 


def loanapplication(request):
    member = request.session.get('member')
    if not member:
        return render(request, 'loanapplication.html', {'loans': []})
    
    code1 = member.get('code')
    print('code', code1)
    
    dict1 = {
        "ms_id": "MS18029529", #view loanapplication single member
        "ms_payload": {
            "code": code1,
        }
    }
    json_data = json.dumps(dict1)
    
    response1 = call_post_method_without_token(url, json_data)
    print('response1', response1)
    
    response = response1.content
    print('response', response)
    
    response_data = json.loads(response)
    
    # Check if response contains data
    loanapp = response_data[0] if response_data else None
    print('loanapp', loanapp)
    
    request.session['loanapp'] = loanapp
    
    # Ensure that `loanapp` is wrapped in a list to loop through in the template
    return render(request, 'loanapplication.html', {'loans': [loanapp] if loanapp else []})

import json
from django.shortcuts import render
from .forms import LoanDisbursementForm  # Ensure this is imported

def applyloan(request):
    loan_types = []
    loan_types_data = []
    member = request.session.get('member')
    code1 = member['code']
    print('code', code1)

    if request.method == 'POST':
        form = LoanDisbursementForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            cleaned_data['member_id'] = code1
            print("Form data:", cleaned_data)  # To check the submitted data
            if cleaned_data['repayment_start_date'] is not None:           
                cleaned_data['repayment_start_date'] = cleaned_data['repayment_start_date'].strftime('%Y-%m-%d')
            print('data', cleaned_data['repayment_start_date'])
            
            if cleaned_data['applied_at'] is None:           
                cleaned_data['applied_at'] = datetime.now().strftime('%Y-%m-%d')
            if cleaned_data['approved_at'] is None:           
                cleaned_data['approved_at'] = datetime.now().strftime('%Y-%m-%d')
            if cleaned_data['checked_on'] is None:                
                cleaned_data['checked_on'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if cleaned_data['document_verified_datetime'] is None:                
                cleaned_data['document_verified_datetime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Simulating the API request for loan types
            loan_dict = {
                "ms_id": "MS5028967",
                'ms_payload': cleaned_data         
            }
            print('loan_dict', loan_dict)
            json_data = json.dumps(loan_dict)              

            print('url', url)
            response1 = call_post_method_without_token(url, json_data)

            print('response1', response1)
            return redirect('loanapplication')
            
        else:
            print("Form errors:", form.errors)  # To check any form validation errors

    else:
        form = LoanDisbursementForm()
        dict1 = {
            "ms_id": "MS5026390",
            "ms_payload": {}
        }
        json_data = json.dumps(dict1)
        response1 = call_post_method_without_token(url, json_data)

        if response1.status_code == 200:
            response_data = json.loads(response1.content)
            if response_data and response_data[0].get("obj"):
                loan_types = [
                    {
                        "code": loan["code"],
                        "loantype": loan["loantype"],
                    }
                    for loan in response_data[0]["obj"]
                ]

        dict2 = {
            "ms_id": "MS7018031",
            "ms_payload": {}
        }
        json_data = json.dumps(dict2)
        response2 = call_post_method_without_token(url, json_data)

        if response2.status_code == 200:
            response_data = json.loads(response2.content)
            if response_data and response_data[0].get("obj"):
                loan_types_data = [
                    {
                        "code": loan["code"],
                        "loantype": loan["loantype"],
                        "description": loan["description"],
                        "disbursement_beneficiary": loan["disbursement_beneficiary"],
                        "interest_rate": loan["interest_rate"],
                        "loan_calculation_method": loan["loan_calculation_method"],
                        "min_loan_terms": loan["min_loan_terms"],
                        "max_loan_terms": loan["max_loan_terms"],
                        "min_loan_amt": loan["min_loan_amt"],
                        "max_loan_amt": loan["max_loan_amt"],
                        "processing_fee": loan["processing_fee"],
                        "pre_payment_fee": loan["pre_payment_fee"],
                        "post_payment_fee": loan["post_payment_fee"],
                        "min_age": loan["min_age"],
                        "max_age": loan["max_age"],
                        "income": loan["income"],
                        "collateral_required": loan["collateral_required"],
                        "is_active": loan["is_active"],
                        "is_refinance": loan["is_refinance"],
                        "is_deactivate": loan["is_deactivate"],
                        "loantype_id": loan["loantype_id"],
                        "branch": loan["branch"]
                    }
                    for loan in response_data[0]["obj"]
                ]

    return render(request, 'applyloan1.html', {'form': form, 'loan_types': loan_types, 'loan_types_data': loan_types_data})


def basic1(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST,files = request.FILES)  # Bind form data
        if form.is_valid():  # Validate the form
            cleaned_data = form.cleaned_data
            if cleaned_data['date_of_birth'] is not None:           
                cleaned_data['date_of_birth'] = cleaned_data['date_of_birth'].strftime('%Y-%m-%d')
            print(cleaned_data)
            files, cleaned_data = image_filescreate(cleaned_data)

            dict2 = {
                "ms_id": "MS5022689",
                "ms_payload": cleaned_data if files else cleaned_data
                }

            json_data = json.dumps(dict2)              
  
            print('url',url)
            response1=call_post_method_without_token(url,json_data)

            print('response1',response1)
            return redirect('login')
        else:
            print(form.errors)  # Print errors if form is not valid
    else:
        form = UserRegistrationForm()  # Create an empty form if GET request
        category_dict = {
                "ms_id": "MS5024477",
                "ms_payload": {'branch_id':'2'}
            }
        json_data = json.dumps(category_dict)
        category = call_post_method_without_token(url, json_data)
        # print('category',category.content)
        if category.status_code == 200:
            category_data = json.loads(category.content)
            if category_data and category_data[0].get("obj"):
                category_datas = [
                    {
                        "code": loan["code"],
                        "category": loan["description"],
                    }
                    for loan in category_data[0]["obj"]
                ]   
        print('category_data',category_datas)

        category_type_dict = {
                "ms_id": "MS5025936",
                "ms_payload": {'branch_id':'2'}
            }
        json_data = json.dumps(category_type_dict)
        category_type = call_post_method_without_token(url, json_data)
        # print('category type',category_type.content)
        if category_type.status_code == 200:
            category_type_data = json.loads(category_type.content)
            if category_type_data and category_type_data[0].get("obj"):
                category_type_datas = [
                    {
                        "code": loan["code"],
                        "category": loan["description"],
                    }
                    for loan in category_type_data[0]["obj"]
                ]   
                print('category_type_data',category_type_datas)

        category_dict = {
                "ms_id": "MS5027597",
                "ms_payload": {'branch_id':'2'}
            }
        json_data = json.dumps(category_dict)
        member_category = call_post_method_without_token(url, json_data)
        print('member_category',member_category.content)
        if member_category.status_code == 200:
            member_category_data = json.loads(member_category.content)
            if member_category_data and member_category_data[0].get("obj"):
                member_category_data = [
                    {
                        "code": loan["code"],
                        "category": loan["description"],
                    }
                    for loan in member_category_data[0]["obj"]
                ]   
                print('member_category_data',member_category_data)

        officer_datas=[]
        officer_dict = {
                "ms_id": "MS5028323",
                "ms_payload": {'branch_id':'2'}
            }
        json_data = json.dumps(officer_dict)
        officer_dict = call_post_method_without_token(url, json_data)
        if officer_dict.status_code == 200:
            officer_data = json.loads(officer_dict.content)
            if officer_data and officer_data[0].get("obj"):
                officer_datas = [
                    {
                        "code": loan["code"],
                        "category": loan["first_name"],
                    }
                    for loan in officer_data[0]["obj"]
                ]   
                print('officer_data',officer_datas)
        department_datas=[]
        department_dict = {
                "ms_id": "MS5028243",
                "ms_payload": {'branch_id':'2'}
            }
        json_data = json.dumps(department_dict)
        department_dict = call_post_method_without_token(url, json_data)
        print('department_dict',department_dict)
        if department_dict.status_code == 200:
            department_data = json.loads(department_dict.content)
            if department_data and department_data[0].get("obj"):
                department_datas = [
                    {
                        "code": loan["code"],
                        "category": loan["description"],
                    }
                    for loan in department_data[0]["obj"]
                ]   
                print('department_data',department_datas)

        title_datas = []  # Initialize an empty list before the if condition
        title_dict = {
                "ms_id": "MS5025774",
                "ms_payload": {'branch_id':'2'}
            }
        json_data = json.dumps(title_dict)
        title_data = call_post_method_without_token(url, json_data)
        print('title_dict',title_data)
        if title_data.status_code == 200:
            title_data = json.loads(title_data.content)
            if title_data and title_data[0].get("obj"):
                title_datas = [
                    {
                        "code": loan["code"],
                        "category": loan["description"],
                    }
                    for loan in title_data[0]["obj"]
                ]   
                print('title_data',title_datas)

    return render(request, 'basic1.html',{'form': form,'category_data':category_datas,'category_type_datas':category_type_datas,
                                          'title_data':title_datas,
                  'member_category_data':member_category_data,'officer_data':officer_datas,'department_data':department_datas})

import requests

def call_external_api(ms_id, code, url):
    payload = {
        "ms_id": ms_id,
        "ms_payload": {"code": code}
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()  # Return parsed JSON
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return None

def call_external_api1(ms_id, payload, url):
    payload = {
        "ms_id": ms_id,
        "ms_payload": payload
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()  # Return parsed JSON
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return None
# def repayment_Schedule(request):
#     member = request.session.get('loanapp')
#     if not member or 'application_id' not in member:
#         return render(request, 'repayment.html', {'error_message': 'Loan application not submitted'})

#     code1 = member['application_id']
#     loan_status = member.get('application_status', 'repayment')  # Default to repayment

#     print('Code:', code1)
#     print('Loan Status:', loan_status)

#     # Determine API call based on loan status
#     ms_id = "MS27011625" if loan_status == "restructured" else "MS27015670"
#     schedules = call_external_api(ms_id, code1, url)

#     if not schedules:
#         error_message = "Failed to load repayment schedule" if loan_status == "repayment" else "Failed to load restructure schedule"
#         return render(request, 'repayment.html', {'error_message': error_message})

#     return render(request, 'repayment.html', {'schedules': schedules})

def repayment_Schedule(request):
    member = request.session.get('loanapp')
    if not member or 'application_id' not in member:
        return render(request, 'repayment.html', {'error_message': 'Loan application not submitted'})

    code1 = member['application_id']
    loan_status = member.get('application_status', None)  # Fetch loan status, default is None

    print('Code:', code1)
    print('Loan Status:', loan_status)

    # Determine ms_id based on loan status
    if loan_status == "Restructured": #view restructureschedule single member
        ms_id = "MS18025544"
    elif loan_status == "Cleared balance and moved for refinance":
        ms_id = "MS5025769"
    elif loan_status == "Approved":
        ms_id = "MS18026046"  #view repaymentschedule single member
    else:
        # Handle loans under disbursement or unknown statuses
        return render(request, 'repayment.html', {'error_message': 'Application is under disbursement process. Please check back later.'})

    schedules = call_external_api(ms_id, code1, url)

    if not schedules:
        error_message = f"Failed to load schedule for status: {loan_status}"
        return render(request, 'repayment.html', {'error_message': error_message})

    return render(request, 'repayment.html', {'schedules': schedules})

import json
from django.shortcuts import render, redirect
from .forms import Loancalculator

def loancalculator(request):
    if request.method == 'POST':
        form = Loancalculator(request.POST)
        print('form',form.is_valid())
        if form.is_valid():
            cleaned_data = form.cleaned_data
            cleaned_data['repayment_start_date'] = cleaned_data['repayment_start_date'].strftime('%Y-%m-%d')

            print('cleaned_data', cleaned_data)
            dict1 = {
                    "ms_id": "MS5024169",
                    "ms_payload":  cleaned_data,
                    
                }
            json_data = json.dumps(dict1)
            
            response1 = call_post_method_without_token(url, json_data)
            print('response1', response1.content)
            response2 = json.loads(response1.content.decode('utf-8'))  # This gives a list
            print('response2:', response2)

            # Ensure response2 is a list and has data
            if isinstance(response2, list) and len(response2) > 0:
                records = response2  # Assign the list directly
            else:
                records = []  # Default to an empty list

            # Calculate total payments and interest
            total_payments = sum(item.get('Installment', 0) for item in records)
            total_interest = sum(item.get('Interest', 0) for item in records)


            context = {'form': form, 'save': True, 'records': records, 'total_payments': total_payments, 'total_interest': total_interest}
            return render(request, 'loancalculator.html', context)

            return redirect('loancalculator')  # Change this to an appropriate view
        else:
            print(form.errors)
    else:
        form = Loancalculator()
        dict1 = {
            "ms_id": "MS5026390",
            "ms_payload": {}
        }
        json_data = json.dumps(dict1)
        response1 = call_post_method_without_token(url, json_data)

        loan_types = []  # Initialize as empty list to avoid reference errors
        if response1.status_code == 200:
            response_data = json.loads(response1.content)
            if response_data and response_data[0].get("obj"):
                loan_types = [
                    {
                        "code": loan["code"],
                        "loantype": loan["loantype"],
                    }
                    for loan in response_data[0]["obj"]
                ]
                print('loan_types', loan_types)
        
        return render(request, 'loancalculator.html', {'form': form, 'loan_types': loan_types})
    
    # Default return to prevent NoneType error
    return render(request, 'loancalculator.html', {'form': form})

def req(request):
    return render(request,'requests.html') 

def deposit(request):
    member = request.session.get('member')
    print('Member:', member)

    category_types = []
    amounts = []  # Store balances separately
    success_message = None

    # API Request to fetch category types and balances
    dict1 = {
        "ms_id": "MS18023100", #cashbook_accounts
        "ms_payload": {'member': member['code']}
    }
    json_data = json.dumps(dict1)
    
    response1 = call_post_method_without_token(url, json_data)
    print('Response:', response1.content)

    if response1.status_code == 200 and response1.content:
        response_data = json.loads(response1.content)
        category_types = [{"code": category["code"]} for category in response_data]
        amounts = [{"balance": category["total_balance"]} for category in response_data]
        print('Category Types:', category_types)
        print('Amounts:', amounts)


        transaction_types = []

        # API Request to fetch category types and balances
        dict1 = {
            "ms_id": "MS18022297", #view transactiontypemode member
            "ms_payload": {}
        }
        json_data = json.dumps(dict1)

        response1 = call_post_method_without_token(url, json_data)
        print('Response:', response1.content)

        if response1.status_code == 200 and response1.content:
            response_data = json.loads(response1.content)
            
            # Extract the transaction list from the first dictionary in the response
            if isinstance(response_data, list) and "obj" in response_data[0]:
                transaction_list = response_data[0]["obj"]

                # Extract the transaction codes
                transaction_types = [
                    {"code": transaction["code"], "name": transaction["name"]}
                    for transaction in transaction_list
]
            
    print('Transaction Types:', transaction_types)


    if request.method == 'POST':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                data = json.loads(request.body)
                cashbook_account = data.get('cashbook_account')
                amount = float(data.get('amount', 0))
                transaction_mode = data.get('transaction_mode')

                # Fetch available balance
                available_balance = 0
                for item in amounts:
                    if item["balance"] is not None:
                        available_balance = item["balance"]
                        break

                if amount > available_balance:
                    return JsonResponse({"success": False, "message": "Insufficient balance. Please enter a valid amount."}, status=400)

                dict1 = {
                    "ms_id": "MS18025557",#wallet_topup
                    "ms_payload": {
                        'member': member['code'],
                        'account': cashbook_account,
                        'amount': amount,
                        'transaction_mode': transaction_mode
                    }
                }
                json_data = json.dumps(dict1)

                response1 = call_post_method_without_token(url, json_data)

                return JsonResponse({
                    "success": True,
                    "message": f"Deposit of {amount} to your {cashbook_account} account has been successfully processed."
                })

            except json.JSONDecodeError:
                return JsonResponse({"success": False, "message": "Invalid JSON format."}, status=400)
        else:
            return JsonResponse({"success": False, "message": "Invalid request."}, status=400)

    return render(request, 'wallet.html', {'category_types': category_types, 'amounts': amounts, 'transaction_types': transaction_types})

def account(request):
    member = request.session.get('member')
    code1 = member['code']
    print('code', code1)
    if request.method =='POST':
        form=CustomerAccount(request.POST)
        if form.is_valid():
            cleaned_data=form.cleaned_data
            cleaned_data['customer']=code1
            print('cleaned_data',cleaned_data)
            dict2 = {
                "ms_id": "MS6013052",
                "ms_payload": cleaned_data 
                }

            json_data = json.dumps(dict2)              
  
            print('url',url)
            response1=call_post_method_without_token(url,json_data)

            print('response1',response1)
            return redirect('login')
            
    else:
        form=CustomerAccount()
    return render(request,'account.html',{'form':form}) 

def accounttransfer(request):
    return render(request,'accounttransfer.html') 

def bank(request):
    return render(request,'bank.html') 

def edit_req(request):
    return render(request,'edit_req.html') 

def next_of_kinn(request):
    title_datas = []  # Initialize the variable with an empty list to avoid UnboundLocalError
    member = request.session.get('member')
    code1 = member['code']

    if request.method == 'POST':
        form = NextOfKinn(request.POST, files=request.FILES)  # Bind form data
        if form.is_valid():  # Validate the form
            cleaned_data = form.cleaned_data
            cleaned_data['member']=code1
            if cleaned_data['date_of_birth'] is not None:
                cleaned_data['date_of_birth'] = cleaned_data['date_of_birth'].strftime('%Y-%m-%d')
            # print(cleaned_data)
            # del cleaned_data['passport_image']
            # del cleaned_data['identification_document']
            print(cleaned_data)

            # files, cleaned_data = image_filescreate(cleaned_data)
            files=request.FILES
            print('uploaded',request.FILES)
            dict2 = {
                "ms_id": "MS5024932",
                "ms_payload": cleaned_data if files else cleaned_data
            }

            json_data = json.dumps(dict2)
            print('url', url)
            response1 = call_post_method_without_token(url, json_data)
            # response1 = call_post_method_without_token_v2(url,data= dict2,files=files)

            print('response1', response1)
            print('response1', response1.json)
            return redirect('login')
        else:
            print(form.errors)  # Print errors if form is not valid
    else:
        form = NextOfKinn()
        title_dict = {
            "ms_id": "MS5021914",
            "ms_payload": {'branch_id': '2'}
        }
        json_data = json.dumps(title_dict)
        title_data = call_post_method_without_token(url, json_data)
        print('title_dict', title_data)
        if title_data.status_code == 200:
            title_data = json.loads(title_data.content)
            if title_data and title_data[0].get("obj"):
                title_datas = [
                    {
                        "code": loan["code"],
                        "category": loan["description"],
                    }
                    for loan in title_data[0]["obj"]
                ]
                print('title_data', title_datas)

    return render(request, 'nextofkinn.html', {'form': form, 'title_data': title_datas})

import json
from django.shortcuts import render

def next_of_kinn_list(request):
    member = request.session.get('member')
    if not member:
        return render(request, 'nextofkinlist.html', {'loan_list': None})

    code1 = member.get('code')
    print('code', code1)

    dict1 = {
        "ms_id": "MS5029549",
        "ms_payload": {
            "code": code1,
        }
    }
    json_data = json.dumps(dict1)

    response1 = call_post_method_without_token(url, json_data)
    print('response1', response1)

    response = response1.content
    print('response', response)

    response_data = json.loads(response)

    # Ensure response_data is a list
    loan_list = response_data if isinstance(response_data, list) else [response_data]
    print('loan_list', loan_list)

    request.session['loan_list'] = loan_list
    return render(request, 'nextofkinlist.html', {'loan_list': loan_list})
def subscriptions(request):
    title_datas = []  # Initialize the variable with an empty list to avoid UnboundLocalError
    member = request.session.get('member')
    code1 = member['code']

    if request.method == 'POST':
        form = Subscriptions(request.POST, files=request.FILES)  # Bind form data
        if form.is_valid():  # Validate the form
            cleaned_data = form.cleaned_data
            cleaned_data['member']=code1
            if cleaned_data['start_date'] is not None:
                cleaned_data['start_date'] = cleaned_data['start_date'].strftime('%Y-%m-%d')
            print(cleaned_data)

            dict2 = {
                "ms_id": "MS5025558",
                "ms_payload": cleaned_data
            }

            json_data = json.dumps(dict2)
            print('url', url)
            response1 = call_post_method_without_token(url, json_data)

            print('response1', response1.content)
            return redirect('subscriptions')
        else:
            print(form.errors)  # Print errors if form is not valid
    else:
        form = Subscriptions()
        title_dict = {
            "ms_id": "MS5021914",
            "ms_payload": {'branch_id': '2'}
        }
        json_data = json.dumps(title_dict)
        title_data = call_post_method_without_token(url, json_data)
        print('title_dict', title_data)
        if title_data.status_code == 200:
            title_data = json.loads(title_data.content)
            if title_data and title_data[0].get("obj"):
                title_datas = [
                    {
                        "code": loan["code"],
                        "category": loan["description"],
                    }
                    for loan in title_data[0]["obj"]
                ]
                print('title_data', title_datas)

    return render(request, 'subscriptions.html', {'form': form, 'title_data': title_datas})
import json
from django.shortcuts import render

def subscriptions_list(request):
    member = request.session.get('member')
    if not member:
        return render(request, 'subscription_list.html', {'subscriptions': None})

    code1 = member.get('code')
    print('code', code1)

    dict1 = {
        "ms_id": "MS5029554",
        "ms_payload": {
            "code": code1,
        }
    }
    json_data = json.dumps(dict1)

    response1 = call_post_method_without_token(url, json_data)
    print('response1', response1)

    response = response1.content
    print('response', response)

    response_data = json.loads(response)

    # Ensure response_data is a list
    subscriptions = response_data if isinstance(response_data, list) else [response_data]
    print('subscriptions', subscriptions)

    request.session['subscriptions'] = subscriptions
    return render(request, 'subscription_list.html', {'subscriptions': subscriptions})

def nominees(request):
    title_datas = []  # Initialize the variable with an empty list to avoid UnboundLocalError
    member = request.session.get('member')
    code1 = member['code']

    if request.method == 'POST':
        form = Nominee(request.POST, files=request.FILES)  # Bind form data
        if form.is_valid():  # Validate the form
            cleaned_data = form.cleaned_data
            cleaned_data['member']=code1
            if cleaned_data['date_of_birth'] is not None:
                cleaned_data['date_of_birth'] = cleaned_data['date_of_birth'].strftime('%Y-%m-%d')
            print(cleaned_data)
            
            files, cleaned_data = image_filescreate(cleaned_data, request.FILES.get('passport_image'))
            print("Uploaded Files:", request.FILES)

            dict2 = {
                "ms_id": "MS5024020",
                "ms_payload": cleaned_data if files else cleaned_data
            }

            json_data = json.dumps(dict2)
            print('url', url)
            response1 = call_post_method_without_token(url, json_data)

            print('response1', response1)
            return redirect('login')
        else:
            print(form.errors)  # Print errors if form is not valid
    else:
        form = Nominee()
        title_dict = {
            "ms_id": "MS5021914",
            "ms_payload": {'branch_id': '2'}
        }
        json_data = json.dumps(title_dict)
        title_data = call_post_method_without_token(url, json_data)
        print('title_dict', title_data)
        if title_data.status_code == 200:
            title_data = json.loads(title_data.content)
            if title_data and title_data[0].get("obj"):
                title_datas = [
                    {
                        "code": loan["code"],
                        "category": loan["description"],
                    }
                    for loan in title_data[0]["obj"]
                ]
                print('title_data', title_datas)

    return render(request, 'nominee.html', {'form': form, 'title_data': title_datas})

import json
from django.shortcuts import render

def nominees_list(request):
    member = request.session.get('member')
    if not member:
        return render(request, 'nominee_list.html', {'nominees': None})

    code1 = member.get('code')
    print('code', code1)

    dict1 = {
        "ms_id": "MS5027124",
        "ms_payload": {
            "code": code1,
        }
    }
    json_data = json.dumps(dict1)

    response1 = call_post_method_without_token(url, json_data)
    print('response1', response1)

    response = response1.content
    print('response', response)

    response_data = json.loads(response)

    # Ensure response_data is a list
    nominees = response_data if isinstance(response_data, list) else [response_data]
    print('nominees', nominees)

    request.session['nominees'] = nominees
    return render(request, 'nominee_list.html', {'nominees': nominees})

def get_tenure_details(request, loantype_id):
    print('code', loantype_id)
    
    dict1 = {
        "ms_id": "MS5025311",
        "ms_payload": {
            "loantype_id": loantype_id,
        }
    }
    json_data = json.dumps(dict1)
    
    response1 = call_post_method_without_token(url, json_data)
    print('response1', response1)
    
    response = response1.content
    print('response', response)
    
    data = json.loads(response)
    
    # Check if data is a list and process the first element
    if isinstance(data, list) and len(data) > 0:
        loan_details = data[0]  # Extract the first element
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid response data'}, status=400)

    return JsonResponse({
        'status': 'success',
        'interest_rate': loan_details.get('interest_rate'),
        'loan_calculation_method': loan_details.get('loan_calculation_method'),
        'min_loan_terms': loan_details.get('min_loan_terms'),
        'max_loan_terms': loan_details.get('max_loan_terms'),
        'min_loan_amt': loan_details.get('min_loan_amt'),
        'max_loan_amt': loan_details.get('max_loan_amt'),
    })
import json
from django.shortcuts import render

def account_list(request):
    member = request.session.get('member')
    if not member:
        return render(request, 'accountlist.html', {'accounts': None})

    code1 = member.get('code')
    print('code', code1)

    dict1 = {
        "ms_id": "MS19025309", #view accounts member
        "ms_payload": {
            "code": code1,
        }
    }
    json_data = json.dumps(dict1)
    response1 = call_post_method_without_token(url, json_data)
    print('response1', response1)
    response = response1.content
    print('response', response)
    response_data = json.loads(response)
    # Ensure response_data is a list
    accounts = response_data if isinstance(response_data, list) else [response_data]
    print('accounts', accounts)

    request.session['accounts'] = accounts
    return render(request, 'accountlist.html', {'accounts': accounts})
import json
from datetime import datetime

def payment_process(request, schedule_id, loan_application_id):
    print(f"Schedule ID: {schedule_id}, Loan Application ID: {loan_application_id}")

    member = request.session.get('loanapp')
    if not member or 'application_id' not in member:
        return render(request, 'repayment.html', {'error_message': 'Loan application not submitted'})

    code1 = member['application_id']
    loan_status = member.get('application_status', None)

    print('Code:', code1)
    print('Loan Status:', loan_status)

    # Define mapping for loan statuses to ms_id and payload
    loan_status_map = {
        "Restructured": {
            "ms_id": "MS18024461", #getting restructure schedule
            "payload": {"schedule_id": schedule_id, "app_id": loan_application_id}
        },
        "Cleared balance and moved for refinance": {
            "ms_id": "MS18025113", #getting refinance schedule1
            "payload": {"schedule_id": schedule_id, "app_id": loan_application_id}
        },
        "Approved": {
            "ms_id": "MS18025413", #getting schedule
            "payload": {"schedule_id": schedule_id, "app_id": loan_application_id}
        },
    }

    if loan_status not in loan_status_map:
        return render(request, 'payment_process.html', {'error_message': 'Application is under disbursement process. Please check back later.'})

    ms_id = loan_status_map[loan_status]["ms_id"]
    payload = loan_status_map[loan_status]["payload"]

    schedules = call_external_api1(ms_id, payload, url)

    if not schedules:
        return render(request, 'payment_process.html', {'error_message': f"Failed to load schedule for status: {loan_status}"})

    # Extract the first schedule from the response
    schedule_data = schedules[0]

    # Debugging: Print values
    print('Repayment Date:', schedule_data['repayment_date'])
    print('Paid Amount:', schedule_data['paid_amount'])
    print('Instalment Amount:', schedule_data['instalment_amount'])

    # Calculate the penalty and overdue days
    payable_amount, overdue_days = calculate_penalty(schedule_data['repayment_date'], schedule_data['paid_amount'], schedule_data['instalment_amount'])

    # Add the penalty amount and overdue days to the schedule data
    schedule_data['payable_penalty_amt'] = payable_amount
    schedule_data['overdue_days'] = overdue_days  

    payable_amount = round(payable_amount, 2)
    print('payable_amount:', payable_amount)

    # Add the interest amount (if any) to the payable amount
    interest_amount = schedule_data['interest_amount'] if schedule_data['interest_amount'] else 0
    schedule_data['payable_amount'] = payable_amount + schedule_data['instalment_amount'] + interest_amount
    installment=schedule_data['instalment_amount']
    total = round(schedule_data['payable_amount'], 2)
    print('Total payable amount:', total)

    if request.method == 'POST':
        print('loan_status',loan_status)
        if loan_status == "Restructured": #paid restructure schedule
            ms_id = "MS18029213"
            payload = {"schedule_id": schedule_id, "app_id": loan_application_id,'paid_amount':total,'installment':installment,'penalty':payable_amount,'interest_amount':interest_amount}
        elif loan_status == "Cleared balance and moved for refinance":
            ms_id = "MS5025007"
            payload = {'schedule_id':schedule_id,'app_id':loan_application_id,'paid_amount':total,'installment':installment,'penalty':payable_amount,'interest_amount':interest_amount}
        elif loan_status == "Approved": #paid schedule
            ms_id = "MS18022893"
            payload = {'schedule_id': schedule_id, 'app_id': loan_application_id, 'paid_amount': total,'installment':installment,'penalty':payable_amount,'interest_amount':interest_amount}
        else:
            return render(request, 'payment_process.html', {'error_message': 'Application is under disbursement process. Please check back later.'})

        # Call the external API for payment processing
        print('ms_id, payload, url',ms_id, payload, url)
        schedules = call_external_api1(ms_id, payload, url)
        return redirect('repayment_Schedule')
            # Optionally, set a success flag for the templat

    return render(request, 'payment_process.html', {
        'schedule': schedule_data,
        'payable_amount': total
    })

def calculate_penalty(repayment_date, paid_amount, instalment_amount, penalty_rate=0.05):
    """
    Calculates the penalty if the repayment date is overdue.
    penalty_rate is set to 5% by default.
    """
    current_date = datetime.now().date()
    repayment_date = datetime.strptime(repayment_date, "%Y-%m-%d").date()

    if current_date > repayment_date and paid_amount == 0.0:
        overdue_days = (current_date - repayment_date).days
        penalty_amount = instalment_amount * penalty_rate * overdue_days
        return round(penalty_amount, 2), overdue_days
    return 0.0, 0


def loan_refinance(request, member, loanapp, loan):
    print('member', member)
    print('loanapp', loanapp)
    print('loan', loan)

    dict1 = {
        "ms_id": "MS18021330", #view loanapplication single member
        "ms_payload": {
            "code": loanapp,
        }
    }
    json_data = json.dumps(dict1)
    response1 = call_post_method_without_token(url, json_data)
    loan_datas = json.loads(response1.content)
    loan_amount = loan_datas[0]["approved_amount"]
    loan_status = loan_datas[0]["loan_status"]

    dict1 = {
        "ms_id": "MS18029529",  #view loan single member
        "ms_payload": {
            "code": member,
        }
    }
    json_data = json.dumps(dict1)
    response1 = call_post_method_without_token(url, json_data)
    loan_data = json.loads(response1.content)
    loantype = loan_data[0]["loantype"]
    tenure_type = loan_data[0]["tenure_type"]
    tenure = loan_data[0]["tenure"]
    disbursement_type = loan_data[0]["disbursement_type"]
    repayment_schedule = loan_data[0]["repayment_schedule"]
    application_id = loan_data[0]["application_id"]

    dict1 = {
        "ms_id": "MS19029134",  #view loantype single member
        "ms_payload": {
            "code": loantype,
        }
    }
    json_data = json.dumps(dict1)
    response1 = call_post_method_without_token(url, json_data)
    loantype_data = json.loads(response1.content)
    min_terms = loantype_data[0]["min_loan_terms"]
    max_terms = loantype_data[0]["max_loan_terms"]
    max_loan_amt = loantype_data[0]["max_loan_amt"]
    min_loan_amt = loantype_data[0]["min_loan_amt"]
    loan_calculation_method = loantype_data[0]["loan_calculation_method"]
    interest_rate = loantype_data[0]["interest_rate"]
    is_refinance = loantype_data[0]["is_refinance"]
    print('loan_status',loan_status)

    form = RefinanceForm()
    if loan_status == 'Restructured':
        dict1 = {
            "ms_id": "MS5026036",
            "ms_payload": {
                "loanapp_id": loanapp,
                "branch_id": 2,
            }
        }
        json_data = json.dumps(dict1)
        response1 = call_post_method_without_token(url, json_data)
        restructured_details = json.loads(response1.content)
        dict1 = {
            "ms_id": "MS5026036",
            "ms_payload": {
                "loanapp_id": loanapp,
                "branch_id": 2,
            }
        }
        json_data = json.dumps(dict1)
        response1 = call_post_method_without_token(url, json_data)
        restructured_details = json.loads(response1.content)

    elif loan_status == 'Active_Loan':
        dict1 = {
            "ms_id": "MS18024804", #getting repayment schedules
            "ms_payload": {
                "loanapp_id": loanapp,
                "branch_id": 1,
            }
        }
        json_data = json.dumps(dict1)
        response1 = call_post_method_without_token(url, json_data)
        schedules = json.loads(response1.content)
        print('schedules',schedules)
        paid_amount=sum(item['paid_amount'] for item in schedules)
        total_due = sum(item['instalment_amount'] for item in schedules) - sum(item['paid_amount'] for item in schedules)
        eligibile = max_loan_amt - total_due
        print('total_due',total_due)
        print('eligibile',eligibile)
        if request.method == 'POST':
            form = RefinanceForm(request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                loan_amount = cleaned_data['loan_amount']
                new_amount = loan_amount - total_due
                tenure = cleaned_data['tenure']
                repayment_id = cleaned_data['repayment_id'].strftime('%Y-%m-%d')

                resp = validate_refinance_form(
                    max_loan_amt, min_loan_amt, loan_amount, tenure, repayment_id,
                    max_terms, min_terms, total_due, loan_status, is_refinance
                )

                if resp[0]:
                    dict1 = {
                        "ms_id": "MS18026790", #loan refinance member
                        "ms_payload": {
                            'new_tenure': tenure,
                            'new_amount': new_amount,
                            'loan_id': loan,
                            'loanapp_id': loanapp,
                            'approval_status': "Refinanced",
                            'repayment_start_date': repayment_id,
                            "branch_id": 2,
                        }
                    }
                    json_data = json.dumps(dict1)
                    call_post_method_without_token(url, json_data)
                    return redirect('loanapplication')

                else:
                    context = {
                        'form': form, 'member': member, 'tenure_type': tenure_type, 'tenure': tenure,
                        'disbursement_type': disbursement_type, 'repayment_schedule': repayment_schedule,
                        'application_id': application_id, 'min_terms': min_terms, 'max_terms': max_terms,
                        'max_loan_amt': max_loan_amt, 'min_loan_amt': min_loan_amt,
                        'loan_calculation_method': loan_calculation_method, 'interest_rate': interest_rate,
                        'loantype': loantype, 'error_message': resp[1],
                        'total_due': total_due, 'eligibile': eligibile, 'loan_amount': loan_amount,'paid_amount':paid_amount
                    }
                    return render(request, 'refinance.html', context)  # FIXED: Always return here

    context = {
        'form': form, 'member': member, 'tenure_type': tenure_type, 'tenure': tenure,
        'disbursement_type': disbursement_type, 'repayment_schedule': repayment_schedule,
        'application_id': application_id, 'min_terms': min_terms, 'max_terms': max_terms,
        'max_loan_amt': max_loan_amt, 'min_loan_amt': min_loan_amt,
        'loan_calculation_method': loan_calculation_method, 'interest_rate': interest_rate,
        'loantype': loantype, 'loan_amount': loan_amount,'paid_amount':paid_amount,
        'total_due': total_due, 'eligibile': eligibile, 'loan_amount': loan_amount

    }
    return render(request, 'refinance.html', context)  # Ensuring function always returns


def loan_restructure(request,member,loanapp,loan):
    print('member', member)
    print('loanapp', loanapp)
    print('loan', loan)

    dict1 = {
        "ms_id": "MS18021330", #view loanapplication single member
        "ms_payload": {
            "code": loanapp,
        }
    }
    json_data = json.dumps(dict1)
    response1 = call_post_method_without_token(url, json_data)
    loan_datas = json.loads(response1.content)
    loan_amount = loan_datas[0]["approved_amount"]
    loan_status = loan_datas[0]["loan_status"]
    loan_id = loan_datas[0]["code"]

    dict1 = {
        "ms_id": "MS18029529",  #view loan single member
        "ms_payload": {
            "code": member,
        }
    }
    json_data = json.dumps(dict1)
    response1 = call_post_method_without_token(url, json_data)
    loan_data = json.loads(response1.content)
    loantype = loan_data[0]["loantype"]
    tenure_type = loan_data[0]["tenure_type"]
    tenure = loan_data[0]["tenure"]
    disbursement_type = loan_data[0]["disbursement_type"]
    repayment_schedule = loan_data[0]["repayment_schedule"]
    application_id = loan_data[0]["application_id"]

    dict1 = {
        "ms_id": "MS19029134",  #view loantype single member
        "ms_payload": {
            "code": loantype,
        }
    }
    json_data = json.dumps(dict1)
    response1 = call_post_method_without_token(url, json_data)
    loantype_data = json.loads(response1.content)
    min_terms = loantype_data[0]["min_loan_terms"]
    max_terms = loantype_data[0]["max_loan_terms"]
    max_loan_amt = loantype_data[0]["max_loan_amt"]
    min_loan_amt = loantype_data[0]["min_loan_amt"]
    loan_calculation_method = loantype_data[0]["loan_calculation_method"]
    interest_rate = loantype_data[0]["interest_rate"]
    is_refinance = loantype_data[0]["is_refinance"]

    form = RestructureForm()
    dict1 = {
        "ms_id": "MS18024804", #getting repayment schedules
        "ms_payload": {
            "loanapp_id": loanapp,
            "branch_id": 1,
        }
    }
    json_data = json.dumps(dict1)
    response1 = call_post_method_without_token(url, json_data)
    schedules = json.loads(response1.content)
    total_schedule=len(schedules)
    dict1 = {
        "ms_id": "MS18021401", #getting next schedules
        "ms_payload": {
            "loanapp_id": loanapp,
            "branch_id": 1,
        }
    }
    json_data = json.dumps(dict1)
    response1 = call_post_method_without_token(url, json_data)
    next_schedule = json.loads(response1.content)
    print('next schedules',next_schedule)
    paid_installment=next_schedule[0]['total']
    pending_installment=total_schedule-paid_installment
    total_installment_amount = sum(item['instalment_amount'] for item in schedules)
    total_paid_amount = sum(item['paid_amount'] for item in schedules)
    total_due=sum(item['instalment_amount'] for item in schedules) -sum(item['paid_amount'] for item in schedules)

    print('total_due',total_due)
    if request.method == 'POST':
        form = RestructureForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            tenure = cleaned_data['tenure']
            repayment_id = cleaned_data['repayment_id'].strftime('%Y-%m-%d')

            resp = validate_restructure_form(tenure,max_terms,min_terms,loan_status)
            if resp[0]:
                
                dict1 = {
                    "ms_id": "MS18023943", #confirmed schedule
                    "ms_payload": {
                        'loan_id': loan_id,
                    }
                }
                json_data = json.dumps(dict1)
                response=call_post_method_without_token(url, json_data)
                response2=json.loads(response.content)
                dict1 = {
                    "ms_id": "MS19025484", #loan restructure member
                    "ms_payload": {
                        'new_tenure': tenure,
                        'loan_id': loan_id,
                        'new_amount':total_due,
                        'loanapp_id': loanapp,
                        'approval_status': "Restructured",
                        'repayment_start_date': repayment_id,
                        "branch_id": 1,
                    }
                }
                json_data = json.dumps(dict1)
                restructure_response=call_post_method_without_token(url, json_data)
                restructure_response1=json.loads(restructure_response.content)
                return redirect('loanapplication')

            else:
                context = {
                    'form': form, 'member': member, 'tenure_type': tenure_type, 'tenure': tenure,
                    'disbursement_type': disbursement_type, 'repayment_schedule': repayment_schedule,
                    'application_id': application_id, 'min_terms': min_terms, 'max_terms': max_terms,
                    'max_loan_amt': max_loan_amt, 'min_loan_amt': min_loan_amt,'paid_amount':total_installment_amount,
                    'loan_calculation_method': loan_calculation_method, 'interest_rate': interest_rate,
                    'loantype': loantype, 'error_message': resp[1],'paid_installment':paid_installment,
                    'pending_installment':pending_installment,
                    'total_due': total_due, 
                }
                return render(request, 'restructure.html', context)  

    context = {
        'form': form, 'member': member, 'tenure_type': tenure_type, 'tenure': tenure,
        'disbursement_type': disbursement_type, 'repayment_schedule': repayment_schedule,
        'application_id': application_id, 'min_terms': min_terms, 'max_terms': max_terms,
        'max_loan_amt': max_loan_amt, 'min_loan_amt': min_loan_amt,
        'loan_calculation_method': loan_calculation_method, 'interest_rate': interest_rate,
        'loantype': loantype, 'loan_amount': loan_amount,'paid_amount':total_installment_amount,
        'paid_installment':paid_installment,
                    'pending_installment':pending_installment,
        'total_due': total_due,  'loan_amount': loan_amount

    }
    return render(request,'restructure.html',context)



def loan_closure(request,member,loanapp,loan):
    print('member', member)
    print('loanapp', loanapp)
    print('loan', loan)

    dict1 = {
        "ms_id": "MS18021330", #view loanapplication single member
        "ms_payload": {
            "code": loanapp,
        }
    }

    json_data = json.dumps(dict1)
    response1 = call_post_method_without_token(url, json_data)
    loan_datas = json.loads(response1.content)
    loan_amount = loan_datas[0]["approved_amount"]
    loan_status = loan_datas[0]["loan_status"]
    loan_id = loan_datas[0]["code"]

    dict1 = {
        "ms_id": "MS18029529",  #view loan single member
        "ms_payload": {
            "code": member,
        }
    }
    json_data = json.dumps(dict1)
    response1 = call_post_method_without_token(url, json_data)
    loan_data = json.loads(response1.content)
    loantype = loan_data[0]["loantype"]
    tenure_type = loan_data[0]["tenure_type"]
    tenure = loan_data[0]["tenure"]
    disbursement_type = loan_data[0]["disbursement_type"]
    repayment_schedule = loan_data[0]["repayment_schedule"]
    application_id = loan_data[0]["application_id"]

    dict1 = {
        "ms_id": "MS19029134",  #view loantype single member
        "ms_payload": {
            "code": loantype,
        }
    }
    json_data = json.dumps(dict1)
    response1 = call_post_method_without_token(url, json_data)
    loantype_data = json.loads(response1.content)
    min_terms = loantype_data[0]["min_loan_terms"]
    max_terms = loantype_data[0]["max_loan_terms"]
    max_loan_amt = loantype_data[0]["max_loan_amt"]
    min_loan_amt = loantype_data[0]["min_loan_amt"]
    loan_calculation_method = loantype_data[0]["loan_calculation_method"]
    interest_rate = loantype_data[0]["interest_rate"]
    is_refinance = loantype_data[0]["is_refinance"]

    if loan_status=='Active_Loan':
        dict1 = {
            "ms_id": "MS18024804", #getting repayment schedules
            "ms_payload": {
                "loanapp_id": loanapp,
                "branch_id": 1,
            }
        }
        json_data = json.dumps(dict1)
        response1 = call_post_method_without_token(url, json_data)
        schedules = json.loads(response1.content)
        
        total_schedule=len(schedules)
        dict1 = {
            "ms_id": "MS18021401", #getting next schedules
            "ms_payload": {
                "loanapp_id": loanapp,
                "branch_id": 1,
            }
        }
        json_data = json.dumps(dict1)
        response1 = call_post_method_without_token(url, json_data)
        next_schedule = json.loads(response1.content)
        print('next schedules',next_schedule)
        paid_installment=next_schedule[0]['total']
        pending_installment=total_schedule-paid_installment
        total_installment_amount = sum(item['instalment_amount'] for item in schedules)
        total_paid_amount = sum(item['paid_amount'] for item in schedules)
        total_due=sum(item['instalment_amount'] for item in schedules) -sum(item['paid_amount'] for item in schedules)
        total_interest=sum(item['interest_amount'] for item in schedules) 
        total_penalty=sum(item['payable_penalty_amt'] for item in schedules) 
        print('total_due',total_due)
        print('total_interest',total_interest)
        print('total_penalty',total_penalty)
        loan_close=total_due+total_interest+total_penalty
        member = request.session.get('loanapp')
        if not member or 'application_id' not in member:
            return render(request, 'repayment.html', {'error_message': 'Loan application not submitted'})
    elif loan_status=='Restructured':
        dict1 = {
            "ms_id": "MS18024416", #getting repayment restructure schedules
            "ms_payload": {
                "loanapp_id": loanapp,
                "branch_id": 1,
            }
        }
        json_data = json.dumps(dict1)
        response1 = call_post_method_without_token(url, json_data)
        schedules = json.loads(response1.content)
        print('schedules',schedules)
        total_schedule=len(schedules)
        dict1 = {
            "ms_id": "MS18022741", #getting next restructure schedules member
            "ms_payload": {
                "loanapp_id": loanapp,
                "branch_id": 1,
            }
        }
        json_data = json.dumps(dict1)
        response1 = call_post_method_without_token(url, json_data)
        next_schedule = json.loads(response1.content)
        print('next schedules',next_schedule)
        paid_installment=next_schedule[0]['total']
        pending_installment=total_schedule-paid_installment
        total_installment_amount = sum(item['instalment_amount'] for item in schedules)
        total_paid_amount = sum(item['paid_amount'] for item in schedules)
        total_due=sum(item['instalment_amount'] for item in schedules) -sum(item['paid_amount'] for item in schedules)
        total_interest=sum(item['interest_amount'] for item in schedules) 
        total_penalty=sum(item['payable_penalty_amt'] for item in schedules) 
        print('total_due',total_due)
        print('total_interest',total_interest)
        print('total_penalty',total_penalty)
        loan_close=total_due+total_interest+total_penalty
        print('loan_close',loan_close)
        member = request.session.get('loanapp')
        if not member or 'application_id' not in member:
            return render(request, 'repayment.html', {'error_message': 'Loan application not submitted'})

    code1 = member['application_id']
    loan_status = member.get('application_status', None)  # Fetch loan status, default is None

    print('Code:', code1)
    print('Loan Status:', loan_status)

    # Determine ms_id based on loan status
    if loan_status == "Restructured": #view restructureschedule single member
        ms_id = "MS18025544"
    elif loan_status == "Cleared balance and moved for refinance":
        ms_id = "MS5025769"
    elif loan_status == "Approved":
        ms_id = "MS18026046"  #view repaymentschedule single member
    else:
        # Handle loans under disbursement or unknown statuses
        return render(request, 'loan_closure.html', {'error_message': 'Application is under disbursement process. Please check back later.'})

    schedules = call_external_api(ms_id, code1, url)

    if not schedules:
        error_message = f"Failed to load schedule for status: {loan_status}"
        return render(request, 'repayment.html', {'error_message': error_message})
    if request.method=='POST':
        dict1 = {
            "ms_id": "MS19029965", #loan closure
            "ms_payload": {
                "member": member,
                'app_id':loanapp,
                "branch_id": 1,
                "penalty":total_penalty,
                "interest":total_interest,
                "principal":total_installment_amount,
                "total":loan_close,
                # "processing_fee":processing_fee
            }
        }
        json_data = json.dumps(dict1)
        response1 = call_post_method_without_token(url, json_data)
        next_schedule = json.loads(response1.content)
        return redirect('loanapplication')
    context = {
         'member': member, 'tenure_type': tenure_type, 'tenure': tenure,
        'disbursement_type': disbursement_type, 'repayment_schedule': repayment_schedule,
        'application_id': application_id, 'min_terms': min_terms, 'max_terms': max_terms,
        'max_loan_amt': max_loan_amt, 'min_loan_amt': min_loan_amt,
        'loan_calculation_method': loan_calculation_method, 'interest_rate': interest_rate,
        'loantype': loantype, 'loan_amount': loan_amount,'paid_amount':total_installment_amount,
        'paid_installment':paid_installment,
                    'pending_installment':pending_installment,
        'total_due': total_due,  'loan_amount': loan_amount,'schedules': schedules,'loan_close':loan_close

    }
    return render(request, 'loan_closure.html', context)
