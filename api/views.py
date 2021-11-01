# from django.http import JsonResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ProjectSerializer
from projects.models import Project,Review, Tag
# @api_view is a wrapper which takes in http methods 
@api_view(['GET'])
def getRoutes(request):
    routes=[
        {'GET':'/api/projects'},
        {'GET':'/api/projects/id'},
        {'POST':'/api/projects/id/vote'},
        {'POST':'/api/users/token'},
        {'POST':'/api/users/token/refresh'},
    ]
    # without using rest framework
    # return JsonResponse(routes,safe=False)
    return Response(routes)

@api_view(['GET'])
def getProjects(reqeust):
    projects=Project.objects.all()
    # converting projects object into Json format and getting the data many=true means getting all the objects
    serializer=ProjectSerializer(projects,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProject(reqeust,pk):
    project=Project.objects.get(id=pk)
    # converting projects object into Json format and getting the data many=false means getting only one object
    serializer=ProjectSerializer(project,many=False)
    return Response(serializer.data)

# authenticating the api with simple jwt  for posting the votes using permisssion classes and is authenticated 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request,pk):
    project=Project.objects.get(id=pk)
    # gets the logged in user whose user is taken from the token or jwt
    user=request.user.profile
    # request.data is like request.POST but it hase other http servies also
    data=request.data
    # if there is already a review with the same user or creates the user using get_or_create
    review,created=Review.objects.get_or_create(
        owner=user,
        project=project

    )
    review.value=data['value']
    review.save()
    project.getVoteCount
    serializer=ProjectSerializer(project,many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
def removeTag(request):
    tagId=request.data['tag']
    projectId=request.data['project']

    project=Project.objects.get(id=projectId)
    tag=Tag.objects.get(id=tagId)
    project.tags.remove(tag)
    return Response('Tag was deleted')