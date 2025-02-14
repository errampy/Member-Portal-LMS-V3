from django import forms

MEMBERSHIP_CHOICES = [
    ('individual', 'Individual'),
    ('partner', 'Partner'),
]

CITIZENSHIP_CHOICES = [
    ('kenyan', 'Kenyan Citizen'),
    ('non_kenyan', 'Non-Citizen'),
]

class RegisterForm(forms.Form):
    id_number = forms.CharField(
        max_length=50,
        label="ID Number",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your ID number'})
    )
    first_name = forms.CharField(
        max_length=100,
        label="First Name",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'})
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    phone_number = forms.CharField(
        max_length=15,
        label="Phone Number",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'})
    )
    membership = forms.ChoiceField(
        choices=MEMBERSHIP_CHOICES,
        label="Membership",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    citizenship = forms.ChoiceField(
        choices=CITIZENSHIP_CHOICES,
        label="Are you a Kenyan Citizen?",
        widget=forms.RadioSelect
    )
    agree_terms = forms.BooleanField(
        label="I agree to the terms and conditions",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


class UserRegistrationForm(forms.Form):
    # Personal Details
        category_type = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={"class": "form-control","readonly":"true"}))
        category_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={"class": "form-control","readonly":"true"}))
        category = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={"class": "form-control","readonly":"true"}))
        recrited_by = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={"class": "form-control","readonly":"true"}))
        relationship_officer = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={"class": "form-control","readonly":"true"}))
        department_code = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={"class": "form-control","readonly":"true"}))

        title =forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={"class": "form-control","readonly":"true"}))
        first_name = forms.CharField(
            max_length=50,
            label="First Name",
            # required=True,
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )
        middle_name = forms.CharField(
            max_length=50,
            label="Middle Name",
            required=False,
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )
        last_name = forms.CharField(
            max_length=50,
            label="Last Name",
            # required=True,
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )
        date_of_birth = forms.DateField(
            label="Date of Birth",
            widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            required=False,
        )
        age = forms.IntegerField(
            label="Age",
            required=False,
            widget=forms.NumberInput(attrs={'class': 'form-control'})
        )
        marital_status=forms.ChoiceField(
            choices=[('single', 'Single'), ('married', 'Married'), ('widowed', 'Widowed'), ('divorced', 'Divorced'), ('withheld', 'Withheld')],
            label="marital_status",
            # required=True,
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        kra_pin = forms.CharField(
            max_length=20,
            label="KRA PIN",
            # required=True,
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )
        nationality  = forms.ChoiceField(
            choices=[('Kenyan', 'Kenyan'), ('Non-Kenyan', 'Non-Kenyan')],
            label="nationality",
            required=False,
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        identification_type=forms.ChoiceField(
            choices=[('national id/alien id', 'National id/alien id'), ('passport', 'Passport'), ('birthcertificate', 'Birthcertificate'), ('birth notifications', 'Birth notifications')],
            label="Type of Resident",
            # required=True,
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        identification_no=forms.CharField(
            max_length=50,
            label="Identification Number",
            required=False,
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )
       
       
     
        marital_status = forms.ChoiceField(choices=[('single', 'Single'), ('married', 'Married'), ('widowed', 'Widowed'), ('divorced', 'Divorced'), ('withheld', 'Withheld')], required=False, widget=forms.Select(attrs={"class": "form-control"}))
        gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female'), ('Non-binary/gender diverse', 'Non-binary/gender diverse'), ('Self-Described', 'Self-described'), ('other', 'Other'), ('both', 'Both')], required=False, widget=forms.Select(attrs={"class": "form-control"}))
 
        county = forms.ChoiceField(required=False, widget=forms.Select(attrs={"class": "form-control"}))
        sub_county = forms.ChoiceField(required=False, widget=forms.Select(attrs={"class": "form-control"}))
        national_id = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
        customer_income = forms.FloatField(required=True, widget=forms.NumberInput(attrs={"class": "form-control"}))
        existing_liabilities = forms.FloatField(required=False,widget=forms.NumberInput(attrs={"class": "form-control"}))
        expiry_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date","class": "form-control"}))
        is_active = forms.BooleanField(required=False,widget=forms.CheckboxInput())
        protected_account = forms.BooleanField(required=False,widget=forms.CheckboxInput())
        marketing_texts = forms.BooleanField(required=False,widget=forms.CheckboxInput())
        e_statement = forms.BooleanField(required=False,widget=forms.CheckboxInput())

        # Choice Fields
        type_of_resident = forms.ChoiceField(
            choices=[('Rented', 'Rented'), ('owned', 'Owned')],
            label="Type of Resident",
            # required=True,
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        gender = forms.ChoiceField(
            choices=[('male', 'Male'), ('female', 'Female'), ('Non-binary/gender diverse', 'Non-binary/gender diverse'), ('Self-Described', 'Self-described'), ('other', 'Other'), ('both', 'Both')],
            label="Gender",
            # required=True,
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        employment_type = forms.ChoiceField(
            choices=[('Employed', 'Employed'), ('Unemployed', 'Unemployed'), ('Self_Employed', 'Self_employed'), ('Part_Time', 'Part_time'), ('Retired', 'Retired'), ('Student', 'Student'), ('Other', 'Other')],
            label="Employment Type",
            # required=True,
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        # employer = forms.CharField(
        #     max_length=100,
        #     label="Employer",
        #     required=False,
        #     widget=forms.TextInput(attrs={'class': 'form-control'})
        # )
        
        # station = forms.CharField(
        #     max_length=100,
        #     label="Station",
        #     # required=True,
        #     widget=forms.TextInput(attrs={'class': 'form-control'})
        # )
        # designation = forms.CharField(
        #     max_length=100,
        #     label="Designation",
        #     # required=True,
        #     widget=forms.TextInput(attrs={'class': 'form-control'})
        # )
        # payroll_no = forms.CharField(
        #     max_length=50,
        #     label="Payroll No",
        #     # required=True,
        #     widget=forms.TextInput(attrs={'class': 'form-control'})
        # )
        e_mail = forms.EmailField(
            label="Email",
            # required=True,
            widget=forms.EmailInput(attrs={'class': 'form-control'})
        )
        primary_phone_no = forms.CharField(
            max_length=15,
            label="Primary Phone No",
            # required=True,
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )
        mobile_transacting_no = forms.CharField(
            max_length=15,
            label="Mobile Transacting No",
            required=False,
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )
        alt_phone_no = forms.CharField(
            max_length=15,
            label="Alternative Phone No",
            required=False,
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )
        residential_town = forms.CharField(
            max_length=100,
            label="Residential Town",
            # required=True,
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )
        address = forms.CharField(
            max_length=200,
            label="Address",
            # required=True,
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )
        residential_estate = forms.CharField(
            max_length=100,
            label="Residential Estate",
            required=False,
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )
               
        # Beneficiary Details
        beneficiary_type = forms.ChoiceField(
            choices=[('Primary', 'Primary'), ('Secondary', 'Secondary')],
            label="Beneficiary Type",
            required=False,
            widget=forms.Select(attrs={'class': 'form-control'})
        )
    
        relation = forms.CharField(
            max_length=50,
            label="Relation",
            required=False,
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )
        beneficiary_phone_no = forms.CharField(
            max_length=15,
            label="Phone No",
            required=False,
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )
        beneficiary_full_name = forms.CharField(
            max_length=100,
            label="Full Name",
            required=False,
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )
        beneficiary_dob = forms.DateField(
            label="Date of Birth",
            widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            required=False,
        )
        beneficiary_id_no = forms.CharField(
            max_length=20,
            label="Identification No",
            required=False,
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )
      
        existing_liabilities=forms.IntegerField(
            label="existing liabilities",
            required=False,
            widget=forms.NumberInput(attrs={'class': 'form-control'})
        )
        # File Uploads
        passport_photo = forms.ImageField(
            label="Passport Photo",
            required=False,
            widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
        )
        identification_image = forms.ImageField(
            label="Identification Image",
            required=False,
            widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
        )
        atm = forms.BooleanField(
            label="ATM",
            required=False,
            widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
        )
        protected_account = forms.BooleanField(
            label="protected account",
            required=False,
            widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
        )
        mobile = forms.BooleanField(
            label="Mobile",
            required=False,
            widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
        )
        e_statement = forms.BooleanField(
            label="e_statement",
            required=False,
            widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
        )
        marketing_texts = forms.BooleanField(
            label="e_statement",
            required=False,
            widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
        )
        fosa = forms.BooleanField(
            label="FOSA",
            required=False,
            widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
        )
        
        # Required File Uploads
        signature = forms.ImageField(
            label="Signature (Type: jpg, png; size: 1MB)",
            required=False,
            widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
        )
        front_id = forms.ImageField(
            label="Front ID (Type: jpg, png; size: 1MB)",
            required=False,
            widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
        )
        back_id = forms.ImageField(
            label="Back ID (Type: jpg, png; size: 1MB)",
            required=False,
            widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
        )
        


class LoanDisbursementForm(forms.Form):
        member_id = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={"class": "form-control","readonly":"true"}))
        loantype = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={"class": "form-control","readonly":"true"}))
        collateral = forms.ChoiceField(choices=[],label='Collateral', required=False, widget=forms.Select(attrs={"class": "form-control"}))
        loan_amount = forms.FloatField(required=True, widget=forms.NumberInput(attrs={"class": "form-control"}))
        disbursement_type = forms.ChoiceField(choices=[('one_off', 'One_off'), ('trenches', 'Trenches')], required=True, widget=forms.Select(attrs={"class": "form-control"}))
        interest_rate = forms.FloatField(required=True, widget=forms.NumberInput(attrs={"class": "form-control","readonly":"true"}))
        tenure = forms.IntegerField(required=True,widget=forms.NumberInput(attrs={"class": "form-control"}))
        tenure_type = forms.ChoiceField(choices=[('days', 'Days'), ('weeks', 'Weeks'), ('months', 'Months'), ('years', 'Years')], required=True, widget=forms.Select(attrs={"class": "form-control"}))
        repayment_start_date = forms.DateField(required=True, widget=forms.DateInput(attrs={"type": "date","class": "form-control"}))
        loan_calculation_method = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={"class": "form-control","readonly":"true"}))
        repayment_schedule = forms.ChoiceField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('halfyearly', 'Halfyearly'), ('annually', 'Annually'), ('one_time', 'One_time')], required=True, widget=forms.Select(attrs={"class": "form-control"}))
        repayment_mode = forms.ChoiceField(choices=[('principal_only', 'Principal_only'), ('interest_only', 'Interest_only'), ('both', 'Both'), ('interest_first', 'Interest_first'), ('principal_end', 'Principal_end')], required=True, widget=forms.Select(attrs={"class": "form-control"}))
        interest_basics = forms.ChoiceField(choices=[('365', '365'), ('other', 'Other')], required=True, widget=forms.Select(attrs={"class": "form-control"}))
        loan_purpose = forms.CharField( required=True, widget=forms.Textarea(attrs={"class": "form-control"}))
        description = forms.CharField(required=True, widget=forms.Textarea(attrs={"class": "form-control"}))
        is_active = forms.BooleanField(required=False,widget=forms.CheckboxInput())

        # application_status = forms.ChoiceField(choices=[('Submitted', 'Submitted'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], required=False, widget=forms.Select(attrs={"class": "form-control"}))
        applied_at = forms.DateField(required=False,label='', widget=forms.DateInput(attrs={"type": "date","class": "form-control","hidden":"true"}))
        approved_at = forms.DateField(required=False,label='', widget=forms.DateInput(attrs={"type": "date","class": "form-control","hidden":"true"}))
        # rejected_reason = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control"}))
        # workflow_stats = forms.ChoiceField(choices=[('Submitted', 'Submitted'), ('Approved', 'Approved'), ('Borrower_Approved', 'Borrower_approved'), ('Lender_Approved', 'Lender_approved'), ('Borrower_and_Lender_Approved', 'Borrower_and_lender_approved'), ('Borrower_Rejected', 'Borrower_rejected'), ('Agreement_completed', 'Agreement_completed'), ('Agreement_dined', 'Agreement_dined'), ('Disbursment', 'Disbursment'), ('Processing', 'Processing'), ('Loan Closed', 'Loan closed')], required=False, widget=forms.Select(attrs={"class": "form-control"}))
        # is_eligible = forms.BooleanField(required=False,widget=forms.CheckboxInput())
        # eligible_rejection_reason = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control"}))
        checked_on = forms.DateTimeField(required=False,label='', widget=forms.DateTimeInput(attrs={"type": "datetime-local","class": "form-control","hidden":"true"}))
        # risk_score = forms.FloatField(required=False, widget=forms.NumberInput(attrs={"class": "form-control"}))
        # risk_factor = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control"}))
        # document_verified = forms.BooleanField(required=False,widget=forms.CheckboxInput())
        document_verified_datetime = forms.DateTimeField(required=False,label='', widget=forms.DateTimeInput(attrs={"type": "datetime-local","class": "form-control","hidden":"true"}))
        # principal_repayment = forms.DecimalField(
        #     max_digits=10,
        #     decimal_places=2,
        #     label="Principal Repayment",
        #     required=False,
        #     widget=forms.NumberInput(attrs={'class': 'form-control'})
        # )
        # interest_repayment = forms.DecimalField(
        #     max_digits=10,
        #     decimal_places=2,
        #     label="Interest Repayment",
        #     required=False,
        #     widget=forms.NumberInput(attrs={'class': 'form-control'})
        # )
        # total_repayment = forms.DecimalField(
        #     max_digits=10,
        #     decimal_places=2,
        #     label="Total Repayment",
        #     required=False,
        #     widget=forms.NumberInput(attrs={'class': 'form-control'})
        # )
        # id_no = forms.CharField(
        #     max_length=20,
        #     label="ID No",
        #     required=False,
        #     widget=forms.TextInput(attrs={'class': 'form-control'})
        # )
        # amount_to_be_guaranteed = forms.DecimalField(
        #     max_digits=10,
        #     decimal_places=2,
        #     label="Amount to be Guaranteed",
        #     required=False,
        #     widget=forms.NumberInput(attrs={'class': 'form-control'})
        # )


class LoginForm(forms.Form):
    id_number = forms.CharField(
        max_length=50,
        label="Member Code",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your member code'})
    )
   

class NextOfKinn(forms.Form):
    member = forms.CharField(required=False, widget=forms.Select(attrs={"class": "form-control"}))
    relative_code = forms.CharField( max_length=50,required=False, widget=forms.Select(attrs={"class": "form-control"}))
    identification_type = forms.ChoiceField(choices=[('National ID/Alien ID', 'National id/alien id'), ('Passport', 'Passport'), ('Birth Certificate', 'Birth certificate'), ('Birth Notification', 'Birth notification')], required=True, widget=forms.Select(attrs={"class": "form-control"}))
    identification_no = forms.IntegerField(required=True,widget=forms.NumberInput(attrs={"class": "form-control"}))
    name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date","class": "form-control"}))
    phone_no = forms.IntegerField(required=False,widget=forms.NumberInput(attrs={"class": "form-control"}))
    passport_image = forms.FileField(required=False,widget=forms.ClearableFileInput(attrs={"class": "form-control-file"}))
    identification_document = forms.FileField(required=False,widget=forms.ClearableFileInput(attrs={"class": "form-control-file"}))

class Subscriptions(forms.Form):
    member = forms.CharField( max_length=50, required=False, widget=forms.Select(attrs={"class": "form-control"}))
    account_type = forms.CharField( max_length=50, required=False, widget=forms.Select(attrs={"class": "form-control"}))
    start_date = forms.DateField(required=True, widget=forms.DateInput(attrs={"type": "date","class": "form-control"}))
    amount = forms.FloatField(required=True, widget=forms.NumberInput(attrs={"class": "form-control"}))
    minimum_contribution = forms.FloatField(required=True, widget=forms.NumberInput(attrs={"class": "form-control"}))

class Nominee(forms.Form):
    member = forms.CharField(max_length=50,required=False, widget=forms.Select(attrs={"class": "form-control"}))
    relative_code = forms.CharField(max_length=50,required=False, widget=forms.Select(attrs={"class": "form-control"}))
    identification_type = forms.ChoiceField(choices=[('National ID/Alien ID', 'National id/alien id'), ('Passport', 'Passport'), ('Birth Certificate', 'Birth certificate'), ('Birth Notification', 'Birth notification')], required=True, widget=forms.Select(attrs={"class": "form-control"}))
    identification_no = forms.IntegerField(required=True,widget=forms.NumberInput(attrs={"class": "form-control"}))
    name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date","class": "form-control"}))
    phone_no = forms.IntegerField(required=False,widget=forms.NumberInput(attrs={"class": "form-control"}))
    passport_image = forms.FileField(required=False,widget=forms.ClearableFileInput(attrs={"class": "form-control-file"}))
    identification_document = forms.FileField(required=False,widget=forms.ClearableFileInput(attrs={"class": "form-control-file"}))


class Loancalculator(forms.Form):
    loantype = forms.CharField(required=False, widget=forms.Select(attrs={"class": "form-control"}))
    loan_amount = forms.FloatField(required=True, widget=forms.NumberInput(attrs={"class": "form-control"}))
    interest_rate = forms.FloatField(required=True, widget=forms.NumberInput(attrs={"class": "form-control"}))
    tenure = forms.IntegerField(required=True,widget=forms.NumberInput(attrs={"class": "form-control"}))
    tenure_type = forms.ChoiceField(choices=[('days', 'Days'), ('weeks', 'Weeks'), ('months', 'Months'), ('years', 'Years')], required=True, widget=forms.Select(attrs={"class": "form-control"}))
    repayment_schedule = forms.ChoiceField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('halfyearly', 'Halfyearly'), ('annually', 'Annually'), ('one_time', 'One_time')], required=True, widget=forms.Select(attrs={"class": "form-control"}))
    repayment_mode = forms.ChoiceField(choices=[('principal_only', 'Principal_only'), ('interest_only', 'Interest_only'), ('both', 'Both'), ('interest_first', 'Interest_first'), ('principal_end', 'Principal_end')], required=True, widget=forms.Select(attrs={"class": "form-control"}))
    interest_basics = forms.ChoiceField(choices=[('365', '365'), ('other', 'Other')], required=True, widget=forms.Select(attrs={"class": "form-control"}))
    loan_calculation_method = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    repayment_start_date = forms.DateField(required=True, widget=forms.DateInput(attrs={"type": "date","class": "form-control"}))

class CustomerAccount(forms.Form):
    customer = forms.CharField(max_length=20, required=False, widget=forms.Select(attrs={"class": "form-control"}))
    account_number = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    bank_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    branch_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    ifsc_code = forms.CharField(max_length=11, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    account_balance = forms.FloatField(required=True, widget=forms.NumberInput(attrs={"class": "form-control"}))
    account_status = forms.ChoiceField(choices=[('active', 'Active'), ('inactive', 'Inactive')], required=True, widget=forms.Select(attrs={"class": "form-control"}))


class StatementForm(forms.Form):
	applicant_id=forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))

class LoanStatementForm(forms.Form):
	applicant_id=forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))
	loan_id=forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))

class WalletTopUp(forms.Form):
    cashbook_account=forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))
    transaction_mode=forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))
    amount=forms.FloatField(required=True, widget=forms.NumberInput(attrs={"class": "form-control"}))

class RefinanceForm(forms.Form):
	loan_amount=forms.FloatField(
        required=True,
        label='Loan Amount',
        widget=forms.NumberInput(attrs={"class": "form-control","readony":"readonly"})
    )
	tenure=forms.IntegerField(
        required=True,
        label='Tenure',
        widget=forms.NumberInput(attrs={"class": "form-control","readony":"readonly"})
    )
	repayment_id= forms.DateField( required=False,label='repayment date', widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}))

