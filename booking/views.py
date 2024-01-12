from django.shortcuts import render

# Create your views here.
# views.py

from rest_framework.views import APIView
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from account.models import ProfessionalProfile,Location,User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from booking.serializers import ProfessionalSearchSerializer
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

class UserSearchView(APIView):
    permission_classes=[IsAuthenticated]

    # def get(self, request):
    #     job_query = request.GET.get("job")
    #     user = request.user
    #     location_query = Location.objects.get(user=user)

    #     if not job_query and not location_query:
    #         return Response({'Msg': 'Provide at least one search parameter (job or location)'}, status=status.HTTP_400_BAD_REQUEST)

    #     search = Q()

    #     if job_query:
    #         search |= Q(professionalprofile__job__icontains=job_query)

    #     if location_query:
    #         search |= (
    #             Q(location__state__icontains=location_query) |
    #             Q(location__district__icontains=location_query) |
    #             Q(location__city__icontains=location_query)
    #         )

    #     search_results = User.objects.filter(search).exclude(is_professional = False).distinct()
    #     print(search_results)

    #     if search_results:
    #         serializer = ProfessionalSearchSerializer(search_results, many=True)
    #         return Response(serializer.data, status=status.HTTP_200_OK)

    #     return Response({'Msg': 'Users Not Found '}, status=status.HTTP_404_NOT_FOUND)
    def get(self, request):
        job_query = request.GET.get("job")
        location_query = request.GET.get("location")

        if not job_query and not location_query:
            return Response({'Msg': 'Provide at least one search parameter (job or location)'}, status=status.HTTP_400_BAD_REQUEST)

        search = Q()

        if job_query:
            search |= Q(professionalprofile__job__icontains=job_query)

        if location_query:
            # Extract values from the Location object if not null
            location = Location.objects.get(id=location_query)
            if location.coordinates is not None:
                location_search = (
                    Q(location__coordinates=location.coordinates) |
                    Q(location__country=location.country) |
                    Q(location__state=location.state) |
                    Q(location__district=location.district) |
                    Q(location__city=location.city)
                )
                search |= location_search

        print(location_query)

        search_results = User.objects.filter(search).distinct()

        if search_results:
            serializer = ProfessionalSearchSerializer(search_results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'Msg': 'Users Not Found '}, status=status.HTTP_404_NOT_FOUND)



    


