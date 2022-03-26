from collections import OrderedDict

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from comment.helper import get_comment_reactions
from comment.models import Comment
from comment.serializers import CommentSerializer
from helpers.filter import fetch_query, get_filter_range
from helpers.validators import check_bool_query, check_sort_by_query


def get_comments_wrt_query(request):
    query_params = fetch_query(request)
    if query_params["all_time"]:
        return Comment.objects.filter(reply__isnull=True), None
    pub_id = query_params["publication"]
    filter_range, err = get_filter_range(query_params)
    if err:
        return None, err
    filter_set = OrderedDict()
    filter_set["created_at__range"] = filter_range
    if query_params["search"]:
        filter_set["comment__contains"] = query_params["search"]
    else:
        filter_set["reply__isnull"] = True
    if pub_id:
        filter_set["publication"] = pub_id
    return Comment.objects.filter(**filter_set), None


class CommentFilter(APIView):
    @staticmethod
    def get(request):
        ascending_filter = check_bool_query(request.query_params.get("asc"))
        sort_by = check_sort_by_query(request.query_params.get("sort_by"))

        dataset = OrderedDict()
        comments, err = get_comments_wrt_query(request)
        if err:
            return Response({"detail": err}, status=status.HTTP_400_BAD_REQUEST)

        if comments and len(comments):
            for item in comments:
                comment_id = str(item.id)
                reactions = get_comment_reactions(item)
                serializer = CommentSerializer(item, context={"user": request.user}, read_only=True)
                dataset[comment_id] = OrderedDict()
                dataset[comment_id]["popularity"] = reactions["total"]
                dataset[comment_id]["support"] = reactions["up_votes"] + reactions["shares"]
                dataset[comment_id]["discussions"] = reactions["replies"]
                dataset[comment_id]["unix"] = int(item.created_at.strftime("%s"))
                dataset[comment_id]["data"] = serializer.data
            dataset = OrderedDict(
                sorted(
                    dataset.items(),
                    key=lambda x: x[1][sort_by],
                    reverse=not ascending_filter,
                )
            )
            return Response(
                {"count": len(dataset.keys()), "results": dataset},
                status=status.HTTP_200_OK,
            )
        return Response({"count": 0, "results": []}, status=status.HTTP_200_OK)
