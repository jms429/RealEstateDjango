from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from listings.choices import state_choices, price_choices, bedroom_choices

from .models import Listing

# Create your views here.

def index(request):
    #make sure you install pylint if your Listing in the import gives you an error
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    # we are adding pagination to listings view with a range of 3 
    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings' : paged_listings
    }
    return render(request, 'listings/listings.html', context)   

def listing(request, listing_id):
    #checks for listing page number if none throws 404
    listing = get_object_or_404(Listing, pk=listing_id)
    context = {
        'listing': listing
    }

    return render(request, 'listings/listing.html', context)

 #this is for the search function
def search(request):
   #orders down by
    queryset_list = Listing.objects.order_by('-list_date')

    #check for keywords in the description in the search function
    if 'keywords' in request.GET:
        #the 'keywords' in this get request searches the html for the name attribute to match
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)
    
    #check for city words (non case sensitive) in the city input field in the search function
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)

    #same for state
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)


    #the lte means less than or equal to
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

   #max price 
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)

    # #check for city words (non case sensitive) in the city input field in the search function
    # if 'state' in request.GET:
    #     state = request.GET['state']
    #     if keywords:
    #         queryset_list = queryset_list.filter(state__iexact=keywords)


    context = {    
        'state_choices': state_choices,
        'bedroom_choices' : bedroom_choices,
        'price_choices' : price_choices,
        'listings': queryset_list,
        #this is how we pass state to the next page
        'values' : request.GET
    }
    return render(request, 'listings/search.html', context)
