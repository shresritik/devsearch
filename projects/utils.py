from django.db.models import Q
from .models import Project, Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def searchProject(request):
    # search_query is initialised to empty string so that it doesn't concatinate with another search
    search_query = ""
    # get the search name from frontend
    if request.GET.get('search'):
        search_query = request.GET.get('search')
    tag = Tag.objects.filter(name__icontains=search_query)
    # accessing the tags from project as it is child element of project from many to many relation
    # distinct is used so duplicate values are not shown when searching for the tag from  project
    projects = Project.objects.distinct().filter(Q(title__icontains=search_query) |
                                                 Q(description__icontains=search_query) |
                                                 Q(owner__name__icontains=search_query) | Q(tags__in=tag))
    return projects, search_query


def paginateProject(request, projectList, results):
    # get page no. from the frontend from the query selector at href i.e href="?page=2"
    page_no = request.GET.get('page')
    # display only 3 items in a page
    results = results
    # using paginator object passing the projectList or object to paginate with the no. of items to display
    paginator = Paginator(projectList, results)
    try:
        # displaying the page from the page no taken from the frontend and projectList will inherit other pagination method
        projectList = paginator.page(page_no)
    except PageNotAnInteger:
        # if page no is not passed in the frontend make it page no=1
        page_no = 1
        projectList = paginator.page(page_no)
    except EmptyPage:
        # if page no. is out of index or more than the given than display the last page from paginator.num_pages
        page_no = paginator.num_pages
        projectList = paginator.page(page_no)

    # creating rolling window in pagination such that more pages doesn't make it messy
    leftIndex = (int(page_no)-2)
    if leftIndex < 1:
        leftIndex = 1
    rightIndex = (int(page_no)+3)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages+1

    custom_range = range(leftIndex, rightIndex)
    return custom_range, projectList
