def global_context(request):
    context = {}
    if request.user.is_authenticated:
        try:
            context['current_journaliste'] = request.user.journaliste
        except:
            context['current_journaliste'] = None
    return context
