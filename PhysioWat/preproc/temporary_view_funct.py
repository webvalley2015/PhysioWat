

def select_experiment(request):
    if request.method == 'POST':
        exp_name = request.POST.get('exp_name')
        password = request.POST.get('password')
        err_log = False
        for i in getExperimentsList():
            if exp_name == i[0] and password == i[1]:
                err_log = True
        if err_log:
            return HttpResponseRedirect('/preproc/recording')
        else:
            messages.error(request, 'Error wrong password')
    else:
        name_list = getExperimentsNames()
        context = {'name_list':name_list}
        return render(request, 'preproc/experiments.html', context)
