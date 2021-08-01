# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from tree.models import IndexTree
from tree.serializers import IndexTreeSerializer


class IndexTreeView(GenericAPIView):
    serializer_class = IndexTreeSerializer

    def find_children(self, obj):
        data = []
        for o in obj:
            temp = dict()
            qs = IndexTree.objects.filter(parent_id=o.id)
            temp['id'] = o.id
            temp['name'] = o.name
            temp['children'] = self.find_children(qs)
            data.append(temp)
        return data

    def get(self, request):
        tree = IndexTree.objects.filter(parent_id=None).first()  # 根节点
        children = IndexTree.objects.filter(parent_id=tree.id)  # 一级目录

        data = self.find_children(children)

        return Response({'id': tree.id, 'name': tree.name, 'children': data})
