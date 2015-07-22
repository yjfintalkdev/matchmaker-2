
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render

from jobs.models import Job, Employer, Location
from likes.models import UserLike
from matches.models import Match, PositionMatch, EmployerMatch, LocationMatch
from questions.models import Question

from newsletter.forms import ContactForm, SignUpForm
from newsletter.models import SignUp

# Create your views here.
def home(request):
	if request.user.is_authenticated():

		#PositionMatch.objects.update_top_suggestions(request.user, 20)
		matches = Match.objects.get_matches_with_percent(request.user)[:6]
		positions = PositionMatch.objects.filter(user=request.user)[:6]

		if positions.count() > 0:
			positions[0].check_update(20) #20 matches total
		locations = LocationMatch.objects.filter(user=request.user)[:6]
		employers = EmployerMatch.objects.filter(user=request.user)[:6]
		mutual_likes = UserLike.objects.get_all_mutual_likes(request.user, 4)

		new_user = False
		if len(mutual_likes) == 0 or len(matches) == 0:
			new_user = True

		queryset = Question.objects.all().order_by('-timestamp') 
		context = {
			"queryset": queryset,
			"matches": matches,
			"positions": positions,
			"locations": locations,
			"employers": employers,
			"mutual_likes": mutual_likes,
			"new_user": new_user
		}
		return render(request, "dashboard/home.html", context)

	context = {
		
	}


	return render(request, "home.html", context)