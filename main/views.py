from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import update_session_auth_hash, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import cache_control

from . import forms
from . import models
from . import review_criteria
from . import polls

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_view(request):
    if request.user.is_authenticated:
        return redirect('main:home')
    
    if request.method == 'POST':
        form = forms.CustomAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user, backend='main.backends.EmailBackend')
                return redirect('main:home')
    else:
        form = forms.CustomAuthenticationForm()

    return render(request,"main/login.html", { 'form':form, })

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signup_view(request):
    if request.user.is_authenticated:   
        return redirect('main:home')

    if request.method == 'POST':
        form = forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            user_data = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email'],
                # 'contact_number': form.cleaned_data['contact_number'],
                'password1': form.cleaned_data['password1'],
                'password2': form.cleaned_data['password2'],
            }
            request.session['user_data'] = user_data
            form.send_otp_email(request)
            return redirect('main:verify')  
    else:
        form = forms.CustomUserCreationForm()

    return render(request, 'main/signup.html', { 'form':form, })

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def verify_view(request):
    if request.user.is_authenticated:
        return redirect('main:home')

    user_data = request.session.get('user_data')
    if not user_data:
        return redirect('main:signup')

    if request.method == 'POST':
        form = forms.OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            if str(request.session.get('otp')) == str(otp):
                # contact_number = user_data['contact_number']

                user_data['password'] = user_data['password1']
                user_data['username']=str(user_data['first_name']+'-'+user_data['last_name']+'-'+timezone.now().strftime('%Y%m%d%H%M%S')).lower()
                del user_data['password1']
                del user_data['password2']
                # del user_data['contact_number']

                user = User.objects.create_user(**user_data)
                # user_profile = models.UserProfile.objects.create(user=user, contact_number=contact_number)
                user_profile = models.UserProfile.objects.create(user=user)
                poll = models.Poll.objects.create(username=user.username)

                user.save()

                del request.session['user_data']
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('main:home')
            else:
                form.add_error('otp', 'Wrong OTP!')
    else:
        form = forms.OTPVerificationForm()

    return render(request, 'main/verify.html', { 'form':form, })


@login_required
def home_view(request):
    user = request.user
    reviews = models.Review.objects.all()
    rec_reviews = reviews.filter(to_user=user.username)
    giv_reviews = reviews.filter(from_user=user.username)

    processed_giv_reviews = []
    for review in giv_reviews:
        processed_giv_reviews.append({
            'review': review,
            'has_upvoted': review.has_upvoted(user),
            'has_downvoted': review.has_downvoted(user), 
        })

    processed_rec_reviews = []
    for review in rec_reviews:
        processed_rec_reviews.append({
            'review': review,
            'has_upvoted': review.has_upvoted(user),
            'has_downvoted': review.has_downvoted(user), 
        })

    # poll
    poll = models.Poll.objects.get(username=user.username)
    has_voted = { question_num: {option['option_num']: poll.has_voted(f'q{question_num}', f'o{option["option_num"]}', user.username)
                    for option in polls.question_option_dict[question_num]['options']}
                    for question_num in polls.question_option_dict.keys() }
    has_voted_question = { question_num: poll.has_voted_question(f'q{question_num}', user.username) for question_num in polls.question_option_dict.keys() }
    vote_percentages = { question_num: {option['option_num']: poll.get_percentage(f'q{question_num}', f'o{option["option_num"]}')
                    for option in polls.question_option_dict[question_num]['options']}
                    for question_num in polls.question_option_dict.keys() }
    
    total_votes = { question_num: poll.get_total_votes(f'q{question_num}') for question_num in polls.question_option_dict.keys() }

    return render(request, 'main/home.html',
        {
            'user': user,
            'reviews':reviews,
            'rec_reviews': rec_reviews,
            'giv_reviews': giv_reviews,
            'processed_rec_reviews':processed_rec_reviews,
            'processed_giv_reviews':processed_giv_reviews,

            'problem_solving': review_criteria.problem_solving,
            'communication': review_criteria.communication,
            'sociability': review_criteria.sociability,

            'poll': poll,
            'username': user.username,
            'questions': polls.question_option_dict.keys(),
            'question_option_dict': polls.question_option_dict,
            'poll_dict': polls.poll_dict,
            'has_voted': has_voted,
            'has_voted_question': has_voted_question,
            'vote_percentages': vote_percentages,
            'total_votes': total_votes,
        }
    )


@login_required
def vote_view(request):
    user = request.user

    if request.method == 'POST':
        if 'action' in request.POST:
            review_id = request.POST.get('review_id')
            action = request.POST.get('action')
            review = models.Review.objects.get(id=review_id)

            if action == 'upvote':
                review.upvote(user)
            elif action == 'downvote':
                review.downvote(user)
            review.save()

            response_data = {
                'success':True,
                'review_id': review_id,
                'upvotes_count': review.get_upvotes_count(),
                'downvotes_count': review.get_downvotes_count(),
                'has_upvoted': review.has_upvoted(user),
                'has_downvoted': review.has_downvoted(user),
            }

        return JsonResponse(response_data)
    
    return JsonResponse({'success':False, })


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('main:login')
    

@login_required
def update_image_view(request):
    try:
        profile = request.user.userprofile
    except ObjectDoesNotExist:
        profile = models.UserProfile(user=request.user)

    if request.method == 'POST':
        form = forms.ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('main:home')
        else:
            print(form.errors)
    else:
        form = forms.ProfileForm(instance=profile)

    return render(request, 'main/update_image.html', { 'form':form, })


@login_required
def update_details_view(request):
    try:
        profile = request.user.userprofile
    except ObjectDoesNotExist:
        profile = models.UserProfile(user=request.user)

    if request.method == 'POST':
        form = forms.ProfileDetailsForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save(request.user)
            return redirect('main:home')
        else:
            print(form.errors)
    else:
        form = forms.ProfileDetailsForm(user=request.user)

    return render(request, 'main/update_details.html', { 'form':form, })
    

@login_required
def update_bio_view(request):
    try:
        profile = request.user.userprofile
    except ObjectDoesNotExist:
        profile = models.UserProfile(user=request.user)

    if request.method == 'POST':
        form = forms.BioForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save(request.user)
            return redirect('main:home')
        else:
            print(form.errors)
    else:
        form = forms.BioForm(user=request.user)

    return render(request, 'main/update_bio.html', { 'form':form, })


@login_required
def user_view(request, username):
    if request.user.username == username:
        return redirect('main:home')
    
    else:
        user = User.objects.get(username=username)
        reviews = models.Review.objects.all()
        rec_reviews = reviews.filter(to_user=username)
        giv_reviews = reviews.filter(anonymous_from=username)
        
        current_user = request.user

        curr_user_rec_review = rec_reviews.filter(from_user=current_user).first()
        curr_user_giv_review = giv_reviews.filter(to_user=current_user).first()
        rec_reviews = rec_reviews.exclude(from_user=current_user)
        giv_reviews = giv_reviews.exclude(to_user=current_user)

        processed_giv_reviews = []
        if curr_user_giv_review is not None:
            processed_giv_reviews.append({
                'review': curr_user_giv_review,
                'has_upvoted': curr_user_giv_review.has_upvoted(current_user),
                'has_downvoted': curr_user_giv_review.has_downvoted(current_user),
            })
        for review in giv_reviews:
            processed_giv_reviews.append({
                'review': review,
                'has_upvoted': review.has_upvoted(current_user),
                'has_downvoted': review.has_downvoted(current_user), 
            })

        processed_rec_reviews = []
        if curr_user_rec_review is not None:
            processed_rec_reviews.append({
                'review': curr_user_rec_review,
                'has_upvoted': curr_user_rec_review.has_upvoted(current_user),
                'has_downvoted': curr_user_rec_review.has_downvoted(current_user),
            })
        for review in rec_reviews:
            processed_rec_reviews.append({
                'review': review,
                'has_upvoted': review.has_upvoted(current_user),
                'has_downvoted': review.has_downvoted(current_user), 
            })

        existing_review = reviews.filter(to_user=username, from_user=request.user.username).first()

        if request.method == 'POST':
            if 'action' not in request.POST:
                reviewform = forms.ReviewForm(request.POST, instance=existing_review)
                if reviewform.is_valid():
                    review = reviewform.save(commit=False)
                    review.to_user = username
                    if reviewform.cleaned_data['is_anonymous']:
                        review.anonymous_from = 'Anonymous'
                    else:
                        review.anonymous_from = request.user.username
                    review.from_user = request.user.username
                    review.save()
                    return redirect('main:user', username=username)
                else:
                    reviewform = forms.ReviewForm(instance=existing_review)
        else:
            reviewform = forms.ReviewForm(instance=existing_review)

        # poll
        poll = models.Poll.objects.get(username=username)
        has_voted = { question_num: {option['option_num']: poll.has_voted(f'q{question_num}', f'o{option["option_num"]}', request.user.username)
                        for option in polls.question_option_dict[question_num]['options']}
                        for question_num in polls.question_option_dict.keys() }
        has_voted_question = { question_num: poll.has_voted_question(f'q{question_num}', request.user.username) for question_num in polls.question_option_dict.keys() }
        vote_percentages = { question_num: {option['option_num']: poll.get_percentage(f'q{question_num}', f'o{option["option_num"]}')
                        for option in polls.question_option_dict[question_num]['options']}
                        for question_num in polls.question_option_dict.keys() }
        
        total_votes = { question_num: poll.get_total_votes(f'q{question_num}') for question_num in polls.question_option_dict.keys() }

        return render(request, 'main/user.html',
            {
                'user':user,
                'reviewform':reviewform if not existing_review else None,
                'reviews':reviews,
                'rec_reviews':rec_reviews,
                'giv_reviews':giv_reviews,
                'processed_rec_reviews':processed_rec_reviews,
                'processed_giv_reviews':processed_giv_reviews,
                'existing_review':existing_review,

                'problem_solving': review_criteria.problem_solving,
                'communication': review_criteria.communication,
                'sociability': review_criteria.sociability,

                'poll': poll,
                'username': username,
                'questions': polls.question_option_dict.keys(),
                'question_option_dict': polls.question_option_dict,
                'poll_dict': polls.poll_dict,
                'has_voted': has_voted,
                'has_voted_question': has_voted_question,
                'vote_percentages': vote_percentages,
                'total_votes': total_votes,
            }
        )


@login_required
def search_view(request):
    query = request.GET.get('q')
    
    if not query:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if len(query.split()) > 1:
        first = query.split()[0]
        second = query.split()[1]
        users = User.objects.filter(
            first_name__icontains=first,
            last_name__icontains=second
        ).exclude(username=request.user.username).exclude(is_superuser=True)
    else:
        first = query.split()[0]
        users = User.objects.filter(
            Q(first_name__icontains=first) | Q(last_name__icontains=first)
        ).exclude(username=request.user.username).exclude(is_superuser=True)

    return render(request, 'main/search.html', { 'users': users, 'query': query, })


@login_required
def edit_view(request, review_id):
    try:
        review = models.Review.objects.get(id=review_id)
    except ObjectDoesNotExist:
        return redirect('main:home')
    
    if str(request.user.username) == str(review.from_user):
        if request.method == 'POST':
            
            if 'edit-review' in request.POST:
                form = forms.ReviewForm(request.POST, instance=review)
                
                if form.is_valid():
                    updated_review = form.save(commit=False)
                    if form.cleaned_data['is_anonymous']:
                        updated_review.anonymous_from = 'Anonymous'
                    else:
                        updated_review.anonymous_from = request.user.username
                    updated_review.save()
                    return redirect('main:user', username=str(review.to_user))
            
            else:
                form = forms.ReviewForm(instance=review)
                return render(request, 'main/edit.html',
                    {
                        'form':form, 'review_id':review_id, 'review':review, 'username':review.to_user,
                    }
                )
            
        else:
            form = forms.ReviewForm(instance=review)
            return render(request, 'main/edit.html', 
                {
                    'form':form, 'review_id':review_id, 'review':review, 'username':review.to_user, 
                }
            )
        
    return redirect('main:user', username=str(review.to_user))


@login_required
def delete_view(request, review_id):
    review = models.Review.objects.get(id=review_id)

    if str(request.user) == str(review.from_user):
        if request.method == 'POST':
            if 'delete-review' in request.POST:
                review.delete()
                return redirect('main:user', username=str(review.to_user))
            else:
                return render(request, 'main/delete.html', { 'review_id':review_id, 'username':review.to_user, })

        else:
            return render(request, 'main/delete.html', { 'review_id':review_id, 'username':review.to_user, })
    
    return redirect('main:user', username=str(review.to_user))


@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = forms.CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('main:home')
        else:
            print(form.errors)
    else:
        form = forms.CustomPasswordChangeForm(request.user)

    return render(request, 'main/password_change.html', { 'form':form, })


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@login_required
def public_private_view(request):
    if request.method == 'POST' and is_ajax(request):
        review_id = request.POST.get('review_id')
        skill = request.POST.get('skill')

        bool_val = False

        review = models.Review.objects.get(id=review_id)
        if skill == 'problem_solving':
            review.problem_solving_bool = not review.problem_solving_bool
            bool_val = review.problem_solving_bool
        elif skill == 'communication':
            review.communication_bool = not review.communication_bool
            bool_val = review.communication_bool
        elif skill == 'sociability':
            review.sociability_bool = not review.sociability_bool
            bool_val = review.sociability_bool

        review.save()
        
        return JsonResponse({ 'success':True, 'skill':skill, 'review_id':review_id, 'bool_val':bool_val, }, safe=False)
    
    return JsonResponse({ 'success':False, }, safe=False)

@login_required
def poll_view(request, username):
    poll = models.Poll.objects.get(username=username)
    if request.method == 'POST':
        question = request.POST.get('question')
        option = request.POST.get('option')
        user = request.user.username

        if question and option:
            poll.vote(question, option, user)
            has_voted = { f'{question}{option}': poll.has_voted(question, option, user) for option in polls.poll_dict[question] }
            has_voted_question = { f'{question}': poll.has_voted_question(question, user) for question in polls.poll_dict.keys() }
            ques_vote_percentages = { f'{question}{option}': poll.get_percentage(question, option) for option in polls.poll_dict[question] }
            ques_total_votes = { f'{question}': poll.get_total_votes(question) for question in polls.poll_dict.keys() }

            data = {
                'success':True,
                'question':question,
                'option':option,
                'user':user,
                'has_voted':has_voted,
                'has_voted_question': has_voted_question,
                'ques_vote_percentages': ques_vote_percentages,
                'ques_total_votes': ques_total_votes,
            }

            return JsonResponse(data, safe=False)

    return JsonResponse({'success': False})
