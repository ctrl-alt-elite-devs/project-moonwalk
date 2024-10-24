from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def googleCalendar(request):
    iframe_code = '''
    <iframe
        src="https://calendar.google.com/calendar/embed?height=600&wkst=1&ctz=America%2FLos_Angeles&bgcolor=%239E69AF&src=YzI0ZTliYzcwNDhkMzg0NDczMmM2NTY5NzljODY4MDgzNjZlOWI1MGVhZGM2ZmUxNTBjODY2OWE3YTYxMjRkMUBncm91cC5jYWxlbmRhci5nb29nbGUuY29t&color=%23B39DDB"
        style="border:solid 1px #777"
        width="500"
        height="800"
        frameborder="0"
        scrolling="no">
    </iframe>
    '''
    return render(request, 'googleCalendar.html', {'iframe_code': iframe_code})
