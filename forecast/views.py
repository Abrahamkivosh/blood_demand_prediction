from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import generic
from .models import BloodType, BloodDemandPrediction, BloodType, BloodSupply, Location
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
from datetime import datetime, date
from .services.blood_demand_service import predict_blood_demand
from django.db import IntegrityError
from django.core.management import call_command
from django.db.models import Sum
from .services.location_service import get_location


class IndexView(View):
    template_name = "pages/index.html"

    def get(self, request):
        return render(request, self.template_name)

class LoginView(View):
    template_name = "auth/login.html"

    def get(self, request):
        # Render the login form
        # Get the entered email from the session, if it exists
        username = request.session.get("username")
        # Clear the username from the session to avoid pre-filling on subsequent login attempts
        request.session["username"] = ""
        return render(request, self.template_name, {"username": username})

    def post(self, request):
        # Process the login form submission
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            request.session["username"] = username
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("forecast:dashboard")
            else:
                messages.error(
                    request, "Invalid username or password", extra_tags="danger"
                )
                return redirect("forecast:login")
        except Exception as e:
            messages.error(request, "Invalid username or password", extra_tags="danger")
            return redirect("forecast:login")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("forecast:index")


class DashboardView(View):
    template_name = "pages/dashboard.html"
    data = {
        "title": "Dashboard",
        'blood_types_count': BloodType.objects.all().count(),
        'blood_demand_predictions_count': BloodDemandPrediction.objects.all().count(),
        'users_count': User.objects.all().count(),
        'latest_blood_demand_predictions': BloodDemandPrediction.objects.all().order_by('-date')[:5],
        'users': User.objects.all().order_by('-date_joined')[:5],

    }

    def get(self, request):
        return render(request, self.template_name, self.data)


class BloodTypeView(generic.ListView):
    template_name = "pages/bloodTypes.html"
    context_object_name = "bloodTypes"

    def get_queryset(self):
        return BloodType.objects.order_by("blood_type_name")


class BloodTypeAddView(View):
    template_name = "pages/bloodTypeAdd.html"

    def get(self, request):
        blood_type_name = request.session.get("blood_type_name")
        # Clear the blood_type_name from the session to avoid pre-filling on subsequent
        request.session["blood_type_name"] = ""
        return render(request, self.template_name, {"blood_type_name": blood_type_name})

    def post(self, request):
        blood_type_name = request.POST.get("blood_type_name")

        request.session["blood_type_name"] = blood_type_name

        # in blood_type_name ensure that the value is in   A+ , A- , B+ , B- , AB+ , AB- , O+ , O-
        if blood_type_name not in ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]:
            messages.error(request, "Invalid blood type name", extra_tags="danger")
            return redirect("forecast:blood-types-add")
        # Check if the blood type already exists
        if BloodType.objects.filter(blood_type_name=blood_type_name).exists():
            messages.error(request, "Blood type already exists", extra_tags="danger")
            return redirect("forecast:blood-types-add")

        description = request.POST.get("description")
        blood_type = BloodType(blood_type_name=blood_type_name, description=description)
        blood_type.save()
        # clear session
        request.session["blood_type_name"] = ""
        messages.success(request, "Blood type added successfully", extra_tags="success")
        return redirect("forecast:blood-types-list")


class BloodTypeUpdateView(View):
    template_name = "pages/bloodTypeEdit.html"

    def get(self, request, bloodTypeId):
        blood_type = get_object_or_404(BloodType, pk=bloodTypeId)

        return render(request, self.template_name, {"blood_type": blood_type})

    def post(self, request, bloodTypeId):
        blood_type = get_object_or_404(BloodType, pk=bloodTypeId)
        # update the blood type
        blood_type_name = request.POST.get("blood_type_name")
        description = request.POST.get("description")

        # in blood_type_name ensure that the value is in   A+ , A- , B+ , B- , AB+ , AB- , O+ , O-
        if blood_type_name not in ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]:
            messages.error(request, "Invalid blood type name", extra_tags="danger")
            return redirect("forecast:blood-types-edit", bloodTypeId=bloodTypeId)
        # Check if the blood type already exists and not the one be updated
        existing_blood_type = (
            BloodType.objects.filter(blood_type_name=blood_type_name)
            .exclude(pk=blood_type.id)
            .first()
        )
        if existing_blood_type is not None:
            messages.error(request, "Blood type already exists", extra_tags="danger")
            return redirect("forecast:blood-types-edit", bloodTypeId=bloodTypeId)

        blood_type.blood_type_name = blood_type_name
        blood_type.description = description
        blood_type.save()

        messages.success(
            request, "Blood type updated successfully", extra_tags="success"
        )
        return redirect("forecast:blood-types-list")


class BloodTypeDeleteView(View):
    def post(self, request, bloodTypeId):
        blood_type = get_object_or_404(BloodType, pk=bloodTypeId)

        # Perform the delete operation
        blood_type.delete()

        messages.success(
            request, "Blood type deleted successfully", extra_tags="success"
        )
        return redirect("forecast:blood-types-list")


def bloodDemandPredictionIndex(request):
    blood_demands = BloodDemandPrediction.objects.all().order_by("-id")
    locations = Location.objects.all()
    template_name = "pages/bloodDemandPredictions.html"

    return render(request, template_name, {"blood_demands": blood_demands, 'locations': locations})


def bloodDemandPredictionStore(request):
    if request.method == "POST":
        try:
            locationId = request.POST.get("location_id")
            location = Location.objects.get(pk=locationId)

            age = request.POST.get("age")
            temperature = request.POST.get("temperature")
            gender = request.POST.get("gender")
            events = request.POST.get("events")
            date = request.POST.get("date")
            user = request.user
             # Count the number of blood types
            blood_types_count = BloodType.objects.all().count()
            if blood_types_count != 8:
                # run command to seed blood types
                call_command("seed_blood_types")
            # check if blood demand prediction for that day exists
            blood_demand_prediction = BloodDemandPrediction.objects.filter(
                location_id=locationId, date=date , age = age, gender = gender
            ).first()
            if blood_demand_prediction is not None:
                raise Exception("Blood Demand Prediction Already Exists For That Day")
            else:
                # loop the blood types and predict blood demand
                for blood_type in BloodType.objects.all():
                    blood_demand = predict_blood_demand(
                        blood_type=  blood_type.blood_type_name,
                        temperature=temperature,
                        age=age,
                        gender= gender,
                        population= location.population,
                        events= events
                    )
                    # save the blood demand prediction
                    blood_demand_prediction = BloodDemandPrediction(
                        blood_type=blood_type,location=location,temperature = temperature,age=age,
                        date=date, predicted_demand=blood_demand,user=user,gender = gender,events = events
                    )
                    blood_demand_prediction.save()
                responseMessage = {"status": True,"status_code":200, "message": "Successfully Created Blood Demand Prediction"}

        except  Exception as e:

            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print(e)
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            responseMessage = {"status": False,"status_code":400, "message": str(e)}
        
    return JsonResponse(responseMessage, status=responseMessage["status_code"], safe=False)
        

def usersIndex(request):
    template_name = "pages/usersList.html"
    users = User.objects.all().order_by('username')
    return render(request, template_name, {"users": users})

def usersCreate(request):
    template_name = "pages/usersAdd.html"
    return render(request, template_name)

def usersStore(request):
    if request.method == "POST":
        try:
            username = request.POST.get("username")
            password = "password"
            email = request.POST.get("email")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            is_staff = request.POST.get("is_staff") 
            if is_staff == "on":
                is_staff = True
            else:
                is_staff = False

            user = User.objects.create_user(username=username, password=password, email=email, 
                                            first_name=first_name, last_name=last_name, is_staff=is_staff)
            user.save()
            responseMessage = {"status": True,"status_code":200, "message": "Successfully Created User"}
        except IntegrityError as err:
            responseMessage = {"status": False,"status_code":400, "message": "Username or Email is already Used"}
        except  Exception as e:

            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print(e)
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            responseMessage = {"status": False,"status_code":400, "message": str(e)}
    else:
        responseMessage = {"status": False,"status_code":400, "message": "Invalid Method. Support POST"}

    return JsonResponse(responseMessage, status=responseMessage["status_code"], safe=False)

class UserUpdateView(View):
    template_name = "pages/userEdit.html"

    def get(self, request, username):
        user = get_object_or_404(User, username=username)

        return render(request, self.template_name, {"user": user})

    def post(self, request, username):
        try:
            user = get_object_or_404(User, username=username)
            # update the blood type
            username = request.POST.get("username")
            email = request.POST.get("email")
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            is_staff = int(request.POST.get("is_staff"))  
            if  is_staff == 1 :
                is_staff = True
            else:
                is_staff = False

            user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.is_staff = is_staff
            user.save()
        except IntegrityError as err:
            responseMessage = {"status": False,"status_code":400, "message": "Username or Email is already Used"}
            return JsonResponse(responseMessage, status=responseMessage["status_code"], safe=False)
        except  Exception as e:
                
                print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                print(e)
                print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                responseMessage = {"status": False,"status_code":400, "message": str(e)}
                return JsonResponse(responseMessage, status=responseMessage["status_code"], safe=False)

        responseMessage = {"status": True,"status_code":200, "message": "Successfully Updated User"}
        return JsonResponse(responseMessage, status=responseMessage["status_code"], safe=False)
    

class BloodSupplyView(View):
    template_name = "pages/bloodSupplies.html"
   
    data = {
        "title": "Blood Supply",
        'blood_supplies': BloodSupply.objects.all().order_by('-id'),
    }

    def get(self, request):
        return render(request, self.template_name, self.data)
    

class BloodSupplyAddView(View):
    template_name = "pages/bloodSupplyAdd.html"
    current_date = date.today()
    data = {
        "title": "Blood Supply",
        'blood_types': BloodType.objects.all().order_by('blood_type_name'),
        'today': date.today(),
        'predictions_count' : BloodDemandPrediction.objects.count(),
        'cities' : Location.objects.all()

    }

    def get(self, request):
        # check list in cities is greater than 0 if so redirect to blood-predictions-list url
        if (self.data['predictions_count'] < 1):
            messages.error(request, "Do Blood Predictions Before You Add Blood Into Blood Bank ", extra_tags="danger" )
            return redirect("forecast:blood-predictions-list")
            
        return render(request, self.template_name, self.data)

    def post(self, request):
        try:
            blood_type_id = request.POST.get("blood_type")
            location_name = request.POST.get("location")
            search_date = request.POST.get("date")
            blood_quantity = float( request.POST.get("quantity"))
            user = request.user

            blood_demand_prediction = BloodDemandPrediction.objects.filter (blood_type_id=blood_type_id, date=search_date).first()
            if blood_demand_prediction is not None:
                # sum already  existing blood supply for that day
                sm= BloodSupply.objects.filter(blood_type_id=blood_type_id, date=search_date).aggregate(Sum('blood_quantity'))
                blood_supply_sum = sm.get('blood_quantity__sum')
                if blood_supply_sum is None:
                    blood_supply_sum = 0

                new_quantity_existing = float( blood_supply_sum)  + float( blood_quantity)
                predicted_demand = blood_demand_prediction.predicted_demand
                if predicted_demand  < new_quantity_existing:
                    responseMessage = {"status": False,"status_code":400, "message": "Blood Supply Quantity is Greater Than Predicted Blood Demand of {0}".format(predicted_demand)  }
                    return JsonResponse(responseMessage, status=responseMessage["status_code"], safe=False)
                

                blood_supply = BloodSupply(blood_type_id=blood_type_id, date=search_date, blood_quantity=blood_quantity, user=user, blood_demand_prediction=blood_demand_prediction)
                blood_supply.save()
                messages.success(request, "Successfully Added Blood Supply", extra_tags="success" )
                responseMessage = {"status": True,"status_code":200, "message": "Successfully Added Blood Supply"}
            else:
                responseMessage = {"status": False,"status_code":400, "message": "No Blood Demand For That Day"}
        except  Exception as e:
                
                print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                print(e)
                print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                responseMessage = {"status": False,"status_code":400, "message": str(e)}
                return JsonResponse(responseMessage, status=responseMessage["status_code"], safe=False)

        return JsonResponse(responseMessage, status=responseMessage["status_code"], safe=False)

class BloodSupplyUpdateView(View):
    template_name = "pages/bloodSupplyEdit.html"
    data = {
        "title": "Blood Supply",
        'blood_types': BloodType.objects.all().order_by('blood_type_name')

    }

    def get(self, request, bloodSupplyId):
        blood_supply = get_object_or_404(BloodSupply, pk=bloodSupplyId)
        return render(request, self.template_name, {"blood_supply": blood_supply, "blood_types": self.data["blood_types"]})

    def post(self, request, bloodSupplyId):
        try:
            blood_supply = get_object_or_404(BloodSupply, pk=bloodSupplyId)
            # update the blood type
            blood_type_id = request.POST.get("blood_type_id")
            blood_quantity = request.POST.get("blood_quantity")
            user_id = request.POST.get("user_id")
            blood_demand_prediction_id = request.POST.get("blood_demand_prediction_id")
            if blood_demand_prediction_id == "":
                blood_demand_prediction_id = None
            blood_supply.blood_type_id = blood_type_id
            blood_supply.blood_quantity = blood_quantity
            blood_supply.user_id = user_id
            blood_supply.blood_demand_prediction_id = blood_demand_prediction_id
            blood_supply.save()
        except  Exception as e:
                
                print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                print(e)
                print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                responseMessage = {"status": False,"status_code":400, "message": str(e)}
                return JsonResponse(responseMessage, status=responseMessage["status_code"], safe=False)

        responseMessage = {"status": True,"status_code":200, "message": "Successfully Updated Blood Supply"}
        return JsonResponse(responseMessage, status=responseMessage["status_code"], safe=False)
    
class BloodSupplyDeleteView(View):
    def post(self, request, bloodSupplyId):
        blood_supply = get_object_or_404(BloodSupply, pk=bloodSupplyId)

        # Perform the delete operation
        blood_supply.delete()

        messages.success(
            request, "Blood supply deleted successfully", extra_tags="success"
        )
        return redirect("forecast:blood-supplies-list")



class LocationView(View):
    template_name = "pages/locationsIndex.html"
    context_object_name = "locations"

    def get(self, request):
        return render(request, self.template_name, {"locations": Location.objects.all().order_by("name")})

    def post(self, request):
        location_name = request.POST.get("name")
        location_name = location_name.lower()
        # validate that location_name is not saved to DB
        try:
            if Location.objects.filter(name=location_name).exists():
                raise Exception("The Location Already Exists")
            else:
                # call location service
                response = get_location(location_name)
                print("=====================================")
                print(response)
                print("=====================================")
                if response :
                    post_params = {
                        "name": response.get("name"),
                        "population": response.get("population"),
                        "latitude": response.get("latitude"),
                        "longitude": response.get("longitude")
                       
                    }
                    print(post_params)
                
                    Location.objects.create(**post_params)
                    responseMessage = {"status": True,"status_code":200, "message": "Location Saved"}
                else:
                    raise Exception("Location Not Found")
            return JsonResponse(responseMessage, status=responseMessage["status_code"], safe=False) 
        except  Exception as e:
                    
                    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    print(e)
                    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    responseMessage = {"status": False,"status_code":400, "message": str(e)}
                    return JsonResponse(responseMessage, status=responseMessage["status_code"], safe=False)
        


class LocationDeleteView(View):
    def post(self, request, locationId):
        location = get_object_or_404(Location, pk=locationId)

        # Perform the delete operation
        location.delete()

        messages.success(
            request, "Location deleted successfully", extra_tags="success"
        )
        return redirect("forecast:locations-list")