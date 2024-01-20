from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse 
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
import random
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from .forms import SignUpForm, OTPVerificationForm, PersonalDetailsForm
from .models import CustomUser ,UserPersonalDetails
# from spliterapp.models import Group
from django.contrib.auth.decorators import login_required

from django.contrib.auth.hashers import make_password

def Main(request):
    username= request.user
    return render(request, "index.html",{"username":username.username} )

# @login_required
# def Main(
#     request,
# ):
#     # group = Group.objects.get(id=group_id)
#     user = request.user  # Get the current user
#     user_groups = Group.objects.filter(members=user)

#     return render(request, "group/base.html", {"user_groups": user_groups})

def Login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(email)
        print(password)
        # Check if user with the provided email exists
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None:
            authenticated_user = authenticate(request, email=email, password=password)
            print(authenticated_user)
            if authenticated_user is not None:
                login(request, authenticated_user)
                messages.success(request, f"Welcome {authenticated_user.username}!")
                return redirect("Main")
            else:
                messages.error(request, "Invalid password. Please try again.")
        else:
            messages.error(request, "Invalid email or user does not exist.")
    
    return render(request, "register/signup.html", {"title": "Log in"})

def Signup(request):
    print("Signup")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():

            email = form.cleaned_data['email']
            number = form.cleaned_data['number']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            print("email", email, username)

        email = request.POST.get("email")
        number = request.POST.get("number")
        username = request.POST.get("username")
        password = request.POST.get("password1")
        # number = request.POST.get("number")
        print(email)
        print(number)

        # Generate a random OTP
        otp = random.randint(1000, 9999)

        # Create the email content
        htmly = get_template("register/gmail.html")
        context = {"username": username, "otp": otp}
        subject, from_email, to = "Welcome", "panchalvikas472@gmail.com", email
        html_content = htmly.render(context)
        print("context:-", context)
        msg = EmailMultiAlternatives(
            subject, "Your OTP is: {}".format(otp), from_email, [to]
        )
        print("massage", msg)
        msg.attach_alternative(html_content, "text/html")
        try:
        #     messages.success(
        #     request, "An OTP has been sent to your email. Please verify your email."
        # )
            msg.send()
        except Exception as e:
            print(f"Error sending email: {e}")
        # msg.send()

        # Store necessary information in the session for OTP verification
        request.session["signup_otp"] = otp
        request.session["signup_username"] = username
        request.session["signup_email"] = email
        request.session["signup_password"] = password
        request.session["signup_number"] = number


        return redirect("VerifyOTP")

    else:
        messages.error(request, "Please correct the errors below.")


    return render(
        request, "register/signup.html", { "title": "Register Here", }
    )


def VerifyOTP(request):
    username = request.session.get("signup_username")
    email = request.session.get("signup_email")
    number = request.session.get("signup_number")

    form = OTPVerificationForm(request.POST or None)

    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        stored_otp = request.session.get("signup_otp")

        if stored_otp and entered_otp == str(stored_otp):
            # Check if the user is already registered
            existing_user = CustomUser.objects.filter(email=email).first()

            if existing_user:
                messages.warning(request, "User already registered. Please log in.")
            else:
                # Complete the registration process and save the user
                user = CustomUser(username=username, email=email, number=number)
                user.password = make_password(request.session.get("signup_password"))
                user.save()

                # Authenticate and log in the user
                authenticated_user = authenticate(username=username, password=request.session.get("signup_password"))
                login(request, authenticated_user)

                messages.success(request, "Registration successful. You are now logged in.")

                # Redirect to the "user_details" page
                return redirect("user_details")

            # Clear session data
            for key in ["signup_otp", "signup_username", "signup_email", "signup_password", "signup_number"]:
                if key in request.session:
                    del request.session[key]

            return redirect("user_details")  # Redirect to your home page

        else:
            response_data = {
                'otp_valid': "invalid_otp",
            }
            return JsonResponse(response_data)

    return render(request, "register/signup.html", {"username": username, "form": form, "show_otp_slide": True})


def PersonalDetails(request):
    if request.method == "POST":
        # Process the personal details form submission
        aadhar_number = request.POST.get("aadhar_number")
        pan_number = request.POST.get("pan_number")
        print("aadhar_number", aadhar_number)

        # Save the personal details to the user model
        user = request.user  # Assuming the user is authenticated
        personal_details, created = UserPersonalDetails.objects.get_or_create(user=user)
        personal_details.aadhar_number = aadhar_number
        personal_details.pan_number = pan_number
        personal_details.save()

        return redirect("Main")  # Redirect to the "user_details" page

    # Render the personal details form
    return render(request, "register/signup.html")