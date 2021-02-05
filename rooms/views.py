from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from django.core.paginator import Paginator
from django.views.generic import View
from . import models
from . import forms


def all_rooms(request):
    page_number = request.GET.get("page", 1)
    room_lists = models.Room.objects.all().order_by("created_at")
    paginator = Paginator(room_lists, 10, 5)
    rooms = paginator.get_page(page_number)

    return render(request, "rooms/home.html", {"rooms": rooms})


def rooms_detail(request, pk):
    try:
        rooms = models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", {"rooms": rooms})
    except models.Room.DoesNotExist:
        raise Http404()


class SearchView(View):
    def get(self, request):
        country = request.GET.get("country")
        if country:
            form = forms.SearchForm(request.GET)

            if form.is_valid():

                city = form.cleaned_data.get("city")
                city = str.capitalize(city)
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                beds = form.cleaned_data.get("beds")
                bedrooms = form.cleaned_data.get("bedrooms")
                baths = form.cleaned_data.get("baths")
                guests = form.cleaned_data.get("guests")
                superhost = form.cleaned_data.get("superhost")
                instant = form.cleaned_data.get("instant")
                amenities = form.cleaned_data.get("amenity")
                facilities = form.cleaned_data.get("facility")
                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city
                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                for amenity in amenities:
                    filter_args["amenities"] = amenity
                for facility in facilities:
                    filter_args["facilities"] = facility

                if superhost:
                    filter_args["host__superhost"] = True
                if instant:
                    filter_args["instant_book"] = True
                rooms = models.Room.objects.filter(**filter_args)
                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms}
                )
        else:
            form = forms.SearchForm()
        return render(request, "rooms/search.html", {"form": form})
