from django.shortcuts import render

from rest_framework import generics

from rest_framework.views import APIView

from notes.serializers import UserSerializer,TaskSerializer

from notes.models import User,Task

from notes.permissions import OwnerOnly

from rest_framework.response import Response

from rest_framework import authentication,permissions



class UserCreationView(generics.CreateAPIView):

    serializer_class = UserSerializer

    

    # def post(self, request, *args, **kwargs):
        
    #     serialzer_instance = UserSerializer(data=request.data)

    #     if serialzer_instance.is_valid():

    #         data = serialzer_instance.validated_data

    #         User.objects.create_user(**data)

    #         return Response(data=serialzer_instance.data)
        
    #     else:

    #         return Response(data=serialzer_instance.errors)


class TaskCreateListView(generics.ListCreateAPIView):

    serializer_class = TaskSerializer

    queryset=Task.objects.all()

    # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes = [authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]



    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    

    # def list(self, request, *args, **kwargs):
        
    #     qs=Task.objects.filter(owner=se)      
        
    #     return 



    # to change(override) ORM query
    def get_queryset(self):
        # return Task.objects.filter(owner=self.request.user)
    
        qs = Task.objects.filter(owner = self.request.user)

        if 'category' in self.request.query_params:

            category_value = self.request.query_params.get("category")

            qs=qs.filter(category = category_value)

        return qs



class RetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Task.objects.all()

    serializer_class = TaskSerializer

    # authentication_classes = [authentication.BasicAuthentication]
    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [OwnerOnly]



from django.db.models import Count

class TaskSummaryAPIView(APIView):

    # authentication_classes = [authentication.BasicAuthentication]
    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]


    def get(self,request,*args,**kwargs):

        qs = Task.objects.filter(owner = request.user)

        category_summary = qs.values('category').annotate(count=Count('category'))

        priority_summary = qs.values('priority').annotate(count=Count('priority'))

        status_summary = qs.values('status').annotate(count=Count('status'))

        task_count = qs.count()

        context = {
            "category_summary":category_summary,
            "priority_summary":priority_summary,
            "status_summary":status_summary,
            "total tasks":task_count
        }

        print("category !!!!!!!!!!!!!!!!",category_summary)

        return Response(data=context)
    

class CategoryListView(APIView):

    def get(self,request,*args,**kwargs):

        qs = Task.category_choices

        '''
        ["bussiness","bussiness"
        ],
        ["personal","personal"]
        '''

        st = {cat for tp in qs for cat in tp}

        return Response(data=st)
    

class PriorityListView(APIView):

    def get(self,request,*args,**kwargs):

        qs = Task.priority_choices

        '''
        ["bussiness","bussiness"
        ],
        ["personal","personal"]
        '''

        st = {cat for tp in qs for cat in tp}

        return Response(data=st)
    


