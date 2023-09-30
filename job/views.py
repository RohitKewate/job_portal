from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_403_FORBIDDEN
from rest_framework.pagination import PageNumberPagination
from .models import Job
from django.db.models import Avg, Min,Max,Count
from .serializers import JobSerilizer
from .filters import JobsFilter
from rest_framework.permissions import IsAuthenticated
# Create your views here.

@api_view(['GET'])
def get_all_jobs(request):
    filterset = JobsFilter(request.GET,queryset=Job.objects.filter().order_by('id'))
    
    count = filterset.qs.count()
    #pagination
    
    responsePerPage = 3
    paginator = PageNumberPagination()
    paginator.page_size = responsePerPage

    queryset = paginator.paginate_queryset(filterset.qs, request)

    serializer = JobSerilizer(queryset, many=True)
    return Response({
        "count": count,
        "responsePerPage": responsePerPage,
        "jobs": serializer.data 
    })


@api_view(['GET'])
def get_job_by_id(request,pk):
    job = get_object_or_404(Job,id=pk)
    
    serializer = JobSerilizer(job, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_job(request):
    request.data['user'] = request.user

    data = request.data
    job = Job.objects.create(**data)   
    serializer = JobSerilizer(job, many=False) 
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_job(request,pk):
    job = get_object_or_404(Job,id=pk)

    if job.user != request.user:
        return Response({'message':"You can't update this job!"  },status=HTTP_403_FORBIDDEN)

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
@permission_classes([IsAuthenticated])
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