from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def user_profile(request):
    user = request.user
    groups = user.groups.all()
    return render(request, 'your_template.html', {'user': user, 'groups': groups})