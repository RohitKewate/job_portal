from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from .models import Job
from django.db.models import Avg, Min,Max,Count
from .serializers import JobSerilizer
# Create your views here.

@api_view(['GET'])
def get_all_jobs(request):
    jobs = Job.objects.all()
    serializer = JobSerilizer(jobs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_job_by_id(request,pk):
    job = get_object_or_404(Job,id=pk)
    
    serializer = JobSerilizer(job, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def create_job(request):
    data = request.data
    job = Job.objects.create(**data)   
    serializer = JobSerilizer(job, many=False) 
    return Response(serializer.data)

@api_view(['PUT'])
def update_job(request,pk):
    job = get_object_or_404(Job,id=pk)
    
    job.title = request.data.get('title')
    job.description = request.data.get('description')
    job.email = request.data.get('email')
    job.address = request.data.get('address')
    job.jobType = request.data.get('jobType')
    job.education = request.data.get('education')
    job.industry = request.data.get('industry')
    job.experience = request.data.get('experience')
    job.salary = request.data.get('salary')
    job.positions = request.data.get('positions')
    job.company = request.data.get('company')

    job.save()
    serializer = JobSerilizer(job, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_job(request,pk):
    job = get_object_or_404(Job,id=pk)
    
    job.delete()
    
    return Response({'message':'Job is Deleted!' },status=HTTP_200_OK)


@api_view(['GET'])
def get_topic_stats(request,topic):
    args = {'title__icontains':topic}
    jobs = Job.objects.filter(**args)
    if len(jobs) == 0:
        return Response({'message':'No Data Found for {topic}!'.format(topic=topic) },)
    
    stats = jobs.aggregate(
        total_jobs = Count('title'),
        avg_positions = Avg('positions'),
        avg_salary=Avg('salary'),
        min_salary=Min('salary'),
        max_salary=Max('salary'),

    )

    return Response(stats)