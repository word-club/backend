from collections import OrderedDict

from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from comment.models import Comment
from helpers.filter import fetch_query, get_filter_range
from publication.models import Publication
from publication.serializers import PublicationSerializer
from helpers.validators import check_bool_query, check_sort_by_query
from share.models import Share
from vote.models import Vote


def get_publication_reactions(publication):
    up_votes = Vote.objects.filter(publication=publication, up=True).count()
    down_votes = Vote.objects.filter(publication=publication, up=False).count()
    shares = Share.objects.filter(publication=publication).count()
    comments = Comment.objects.filter(publication=publication).count()
    total = up_votes + down_votes + shares + comments

    return {
        "up_votes": up_votes,
        "down_votes": down_votes,
        "shares": shares,
        "comments": comments,
        "total": total,
    }


def get_publication_wrt_query(request):
    query_params = fetch_query(request)
    if query_params["all_time"]:
        return Publication.objects.filter(is_published=True), None

    filterset = OrderedDict()
    filter_range, err = get_filter_range(query_params)
    if err:
        return None, err
    if query_params["community"]:
        filterset["community"] = query_params["community"]
    filterset["published_at__range"] = filter_range
    filterset["is_published"] = True
    if query_params["search"]:
        filterset["title__contains"] = query_params["search"]
    return (
        Publication.objects.filter(**filterset),
        None,
    )


class PublicationFilter(APIView):
    pagination_class = PageNumberPagination

    @staticmethod
    def get(request):
        ascending_filter = check_bool_query(request.query_params.get("asc"))  # expects 1|0
        sort_by = check_sort_by_query(request.query_params.get("sort_by"))

        dataset = OrderedDict()
        publications, err = get_publication_wrt_query(request)
        if err:
            return Response({"detail": err}, status=status.HTTP_400_BAD_REQUEST)
        if publications and len(publications):
            for item in publications:
                reactions = get_publication_reactions(item)
                serializer = PublicationSerializer(
                    item, context={"user": request.user}, read_only=True
                )
                dataset[item.id] = OrderedDict()
                dataset[item.id]["popularity"] = reactions["total"]
                dataset[item.id]["support"] = reactions["up_votes"] + reactions["shares"]
                dataset[item.id]["discussions"] = reactions["comments"]
                dataset[item.id]["unix"] = int(item.published_at.strftime("%s"))
                dataset[item.id]["data"] = serializer.data
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
