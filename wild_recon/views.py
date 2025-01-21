from .utils import SubdomainFinderBasic
from django.shortcuts import render
from django.http import JsonResponse


def subdomain_view(request):
    if request.method == 'POST':
        domain = request.POST.get('domain')
        if not domain:
            return JsonResponse({"error": "No domain provided"}, status=400)

        # Call SubdomainFinderBasic
        subdomains, error = SubdomainFinderBasic.find_subdomains(domain)

        if error:
            return JsonResponse({"error": error}, status=500)

        # Render the template with subdomains
        return render(request, 'basic.html', {
            "domain": domain,
            "subdomains": subdomains
        })

    # For GET requests, render the form template
    return render(request, 'basic.html')