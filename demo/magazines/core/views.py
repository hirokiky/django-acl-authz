from django.http import Http404
from django.db.models import ObjectDoesNotExist
from django.template.response import TemplateResponse
from keeper.views import keeper, login_required

from core.models import Magazine, Article


def my_team_factory(request):
    team = getattr(request.user, 'team', None)
    if not team:
        raise Http404
    return team


def my_subscription_factory(request):
    team = my_team_factory(request)
    try:
        sub = team.subscription
    except ObjectDoesNotExist:
        raise Http404
    return sub


@keeper('view', factory=my_team_factory)
def team_dashboard(request):
    pass


@keeper('manage', factory=my_team_factory)
def team_manage(request):
    pass


@keeper('manage', factory=my_team_factory)
def team_billing(request):
    pass


@keeper('managef', factory=my_subscription_factory)
def team_billing_resign(request):
    pass


@keeper('list_magazines',
        on_fail=login_required())
def dashboard(request):
    return TemplateResponse(request, 'core/dashboard.html')


@keeper('read',
        model=Magazine,
        mapper=lambda request, magazine_id: {'id': magazine_id})
def magazine_detail(request, magazine_id):
    pass


@keeper('read',
        model=Article,
        mapper=lambda request, magazine_id, article_id: {'id': article_id})
def article_detail(request, magazine_id, article_id):
    pass
