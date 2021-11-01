from django.db import models
import uuid
from users.models import Profile

# Create your models here.


class Project(models.Model):
    # .SET_NULL means if profile is deleted then project will stay

    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(
        null=True, blank=True, default='default.jpg')
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    # Creating Many to many database Relationship
    tags = models.ManyToManyField('Tag', blank=True)
    votes_total = models.IntegerField(default=0, null=True, blank=True)
    votes_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.title

    class Meta:
        # Sorting on the basis of creation ascending order, -cretated in descending order
        # ordering = ['created']
        # if votes_ratio in a project is low then another project then votes_total gets priority
        ordering = ['-votes_ratio','-votes_total','title']

    # if the image is deleted then give empty string    
    @property
    def imageURL(self):
        try:
            url=self.featured_image.url
        except:
            url=""
        return url

    @property
    def reviewers(self):
        #get all the reviewers from their owner id and make it array from flat=true 
        query_set=self.review_set.all().values_list('owner__id',flat=True)
        return query_set
    
    @property
    def getVoteCount(self):
        reviews=self.review_set.all()
        upVotes=reviews.filter(value='up').count()
        totalVotes=reviews.count()
        ratio=(upVotes/totalVotes)*100
        self.votes_total=totalVotes
        self.votes_ratio=ratio

        self.save()


class Review(models.Model):
    VOTE_TYPE = (('up', 'Up Vote'), ('down', 'Down Vote'))
    # .CASCADE means if profile is deleted then review also gets deleted
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True)
    # Creating One to many database relationship
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    class Meta:
        # A project cannot have two reviews from the same account
        unique_together=[['owner','project']]

    def __str__(self):
        return self.value
    
    


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name
