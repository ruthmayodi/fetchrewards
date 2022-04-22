from django.shortcuts import render
from django.db.models import Sum, Min
from .serializers import PointsSerializer, TotalPointsSerializer
from .models import Points
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from django.utils import timezone


class PointsViewSets(viewsets.ModelViewSet):

    '''default action data'''
    queryset = Points.objects.order_by('-timestamp')
    serializer_class = PointsSerializer

    @action(detail=False, methods=['post'])
    def spend(self, request):
        post_data = JSONParser().parse(request)
        response_data = []
        spend = post_data['points']
        totals = (
            Points.objects.values('payer')
            .annotate(total_points=Sum('points'), earliest_date=Min('timestamp'))
            .values('payer', 'total_points', 'earliest_date')
            .order_by('earliest_date')
        )
        all_points = 0
        for total in totals:
            all_points += total['total_points']
        import pdb
        if spend <= all_points:
            for total in totals:
                if total['total_points'] >= spend:
                    cur_time = timezone.now()
                    post_data = {
                        'payer': total['payer'],
                        'points': -abs(spend),
                        'timestamp': cur_time
                    }
                    response_data.append(
                            {
                                'payer': total['payer'],
                                'points': -abs(spend),
                            }
                        )
                    post_serializer = PointsSerializer(data=post_data)
                    # pdb.set_trace()
                    if post_serializer.is_valid():
                        post_serializer.save()
                        return JsonResponse(response_data, safe=False)
                    return Response({'status': 'Failure'})
                else:
                    if total['total_points'] > 0:
                        cur_time = timezone.now()
                        spend -= total['total_points']
                        post_data = {
                            'payer': total['payer'],
                            'points': -abs(total['total_points']),
                            'timestamp': cur_time
                        }
                        response_data.append(
                            {
                                'payer': total['payer'],
                                'points': -abs(total['total_points']),
                            }
                        )
                        post_serializer = PointsSerializer(data=post_data)
                        # pdb.set_trace()
                        if post_serializer.is_valid():
                            post_serializer.save()
                        else:
                            return Response({'status': 'Failure'})
            return JsonResponse(response_data, safe=False)
        else:
            return Response({'status': 'Not enough points'})

    def create(self, request):
        post_data = JSONParser().parse(request)
        print(post_data)
        points_serializer = PointsSerializer(data=post_data)
        if points_serializer.is_valid():
            points_serializer.save()
            return Response({'status': 'Success'})
        return Response({'status': 'Failure'})


class TotalPointsViewSets(viewsets.ModelViewSet):

    '''default action data'''
    queryset = (
        Points.objects.values('payer')
        .annotate(total_points=Sum('points'))
        .values('payer', 'total_points')
    )
    serializer_class = TotalPointsSerializer

