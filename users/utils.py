from django.db.models import Q
from .models import Profile, Skills
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProfile(request, profiles, results):
    # get page no. from the frontend from the query selector at href i.e href="?page=2"
    page_no = request.GET.get('page')
    # display only 3 items in a page
    results = results
    # using paginator object passing the profiles or object to paginate with the no. of items to display
    paginator = Paginator(profiles, results)
    try:
        # displaying the page from the page no taken from the frontend and profiles will inherit other pagination method
        profiles = paginator.page(page_no)
    except PageNotAnInteger:
        # if page no is not passed in the frontend make it page no=1
        page_no = 1
        profiles = paginator.page(page_no)
    except EmptyPage:
        # if page no. is out of index or more than the given than display the last page from paginator.num_pages
        page_no = paginator.num_pages
        profiles = paginator.page(page_no)

    # creating rolling window in pagination such that more pages doesn't make it messy
    leftIndex = (int(page_no)-2)
    if leftIndex < 1:
        leftIndex = 1
    rightIndex = (int(page_no)+3)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages+1

    custom_range = range(leftIndex, rightIndex)
    return custom_range, profiles


def searchProfile(request):
    # search_query is initialised to empty string so that it doesn't concatinate with another search
    search_query = ""
    # get the search name from frontend
    if request.GET.get('search'):
        search_query = request.GET.get('search')
    skill = Skills.objects.filter(name__icontains=search_query)
    # accessing the skills from profile as it is child element of profile from one to many relation
    # distinct is used so duplicate values are not shown when searching for the skill from  profile
    profiles = Profile.objects.distinct().filter(Q(name__icontains=search_query) |
                                                 Q(short_intro__icontains=search_query) | Q(skills__in=skill))
    return profiles, search_query
