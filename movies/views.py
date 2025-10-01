from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .models import Movie, Review, HiddenMovie, Petition, PetitionVote


def index(request):
    """
    Main list of movies.
    If the user is authenticated, exclude movies they have hidden.
    Supports ?search= query param as in your original implementation.
    """
    search_term = request.GET.get('search')
    qs = Movie.objects.all()
    if search_term:
        qs = qs.filter(name__icontains=search_term)

    if request.user.is_authenticated:
        qs = qs.exclude(hiddenmovie__user=request.user)

    template_data = {
        'title': 'Movies',
        'movies': qs,
    }
    return render(request, 'movies/index.html', {'template_data': template_data})


def show(request, id):
    """
    Movie detail page. Adds `is_hidden` in template_data for the S–Z story.
    """
    movie = get_object_or_404(Movie, id=id)
    reviews = Review.objects.filter(movie=movie).order_by('-date')

    is_hidden = False
    if request.user.is_authenticated:
        is_hidden = HiddenMovie.objects.filter(user=request.user, movie=movie).exists()

    template_data = {
        'title': movie.name,
        'movie': movie,
        'reviews': reviews,
        'is_hidden': is_hidden,
    }
    return render(request, 'movies/show.html', {'template_data': template_data})


@login_required
def create_review(request, id):
    movie = get_object_or_404(Movie, id=id)
    if request.method == 'POST' and request.POST.get('comment', '').strip():
        Review.objects.create(
            movie=movie,
            user=request.user,
            comment=request.POST['comment'].strip(),
        )
        messages.success(request, 'Review added.')
    return redirect('movies.show', id=id)


@login_required
def edit_review(request, id, review_id):
    movie = get_object_or_404(Movie, id=id)
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'GET':
        template_data = {
            'title': 'Edit Review',
            'movie': movie,
            'review': review,
        }
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST.get('comment', '').strip():
        review.comment = request.POST['comment'].strip()
        review.save()
        messages.success(request, 'Review updated.')
    return redirect('movies.show', id=id)


@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    messages.success(request, 'Review deleted.')
    return redirect('movies.show', id=id)


# -------------------- S–Z user story: hide/un-hide movies --------------------

@login_required
def hide_toggle(request, id):
    """
    POST: toggle hidden state for a movie for the current user.
    Redirects back to the referring page (or the index).
    """
    movie = get_object_or_404(Movie, id=id)
    existing = HiddenMovie.objects.filter(user=request.user, movie=movie).first()
    if existing:
        existing.delete()
        messages.info(request, f'"{movie.name}" un-hidden.')
    else:
        HiddenMovie.objects.create(user=request.user, movie=movie)
        messages.info(request, f'"{movie.name}" hidden.')
    return redirect(request.META.get('HTTP_REFERER') or 'movies.index')


@login_required
def hidden_list(request):
    """
    A page showing all movies this user has hidden, with un-hide buttons.
    """
    movies = Movie.objects.filter(hiddenmovie__user=request.user).order_by('name')
    template_data = {
        'title': 'Hidden Movies',
        'movies': movies,
    }
    return render(request, 'movies/hidden_list.html', {'template_data': template_data})


@login_required
def petitions_list(request):
    if request.method == 'POST':
        title = (request.POST.get('title') or '').strip()
        reason = (request.POST.get('reason') or '').strip()
        if not title:
            messages.error(request, 'Please provide a title for your petition.')
        else:
            Petition.objects.create(
                title=title,
                reason=reason,
                requested_by=request.user,
            )
            messages.success(request, 'Petition created.')
            return redirect('movies.petitions_list')
    petitions = Petition.objects.annotate(yes_count=Count('votes')).order_by('-created_at')
    template_data = {
        'title': 'Petitions',
        'petitions': petitions,
    }
    return render(request, 'movies/petitions_list.html', {'template_data': template_data})

def petition_vote_yes(request, petition_id):
    petition = get_object_or_404(Petition, id=petition_id)
    _, created = PetitionVote.objects.get_or_create(petition=petition, user=request.user)
    if created:
        messages.success(request, 'Your vote has been recorded.')
    else:
        messages.info(request, 'You already voted Yes on this petition.')
    return redirect('movies.petitions_list')


def petition_edit(request, petition_id):
    petition = get_object_or_404(Petition, id=petition_id)
    if petition.requested_by != request.user:
        messages.error(request, 'You can only edit your own petition.')
        return redirect('movies.petitions_list')

    if request.method == 'GET':
        template_data = {
            'title': 'Edit Petition',
            'petition': petition,
        }
        return render(request, 'movies/edit_petition.html', {'template_data': template_data})

    # POST
    title = (request.POST.get('title') or '').strip()
    reason = (request.POST.get('reason') or '').strip()
    if not title:
        messages.error(request, 'Please provide a title.')
        return redirect('movies.petition_edit', petition_id=petition.id)

    petition.title = title
    petition.reason = reason
    petition.save()
    messages.success(request, 'Petition updated.')
    return redirect('movies.petitions_list')

def petition_delete(request, petition_id):
    petition = get_object_or_404(Petition, id=petition_id)
    if petition.requested_by != request.user:
        messages.error(request, 'You can only delete your own petition.')
        return redirect('movies.petitions_list')

    if request.method == 'POST':
        petition.delete()
        messages.success(request, 'Petition deleted.')
        return redirect('movies.petitions_list')

    return redirect('movies.petitions_list')
