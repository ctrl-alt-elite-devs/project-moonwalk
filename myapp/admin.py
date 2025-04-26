from os import path
from pyexpat.errors import messages
from uuid import uuid4
from django.contrib import admin

from .models import Category,Customer,Product,Order,OrderItem,Subscriber,Theme,Newsletter

from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.utils.safestring import mark_safe
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import path
from django.urls import reverse
from django.shortcuts import get_object_or_404

# Register your models here.
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Subscriber)
admin.site.register(Theme)


#Mix customer info and user info
class CustomerInline(admin.StackedInline):
    model = Customer


class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username", "first_name", "last_name", "email"]
    inlines = [CustomerInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price_at_purchase']
    can_delete = False

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'square_order_id', 'total_amount', 'status', 'created_at']
    inlines = [OrderItemInline]

def render_subscribers_with_checkboxes(subscribers):
    html = """
    <button type="button" onclick="selectAll()">Select All</button>
    <form id="subscriber-form">
        <ul style='list-style-type:none; padding-left: 0;'>
    """

    for i, sub in enumerate(subscribers[:50]):
        html += f"""
        <li>
            <label>
                <input type="checkbox" name="subscriber" value="{sub.email}" id="sub_{i}">
                {sub.email}
            </label>
        </li>
        """

    html += """
        </ul>
    </form>
    <script>
        function selectAll() {
            const checkboxes = document.querySelectorAll("input[name='subscriber']");
            checkboxes.forEach(cb => cb.checked = true);
        }
    </script>
    """

    return mark_safe(html)

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'send_button')
    readonly_fields = ['send_button','subscriber_list']
    
        
    def subscriber_list(self, obj):
        from .models import Subscriber
        return render_subscribers_with_checkboxes(Subscriber.objects.all())

    subscriber_list.short_description = "Subscribers"

    

    def send_button(self, obj):
        if obj.pk:
            url = reverse('admin:send_newsletter', kwargs={'newsletter_id': obj.id})
            return mark_safe(
                f'<a class="button" href="{url}" '
                f'style="padding: 6px 12px; background: #28a745; color: white; text-decoration: none; border-radius: 4px;">'
                'Send Newsletter</a>'
            )
        return "Save first to enable sending"
    send_button.short_description = "Send Newsletter"
    



    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:newsletter_id>/send/',
                self.admin_site.admin_view(self.send_newsletter_email),
                name='send_newsletter',
            ),
        ]
        return custom_urls + urls

    def send_newsletter_email(self, request, newsletter_id):
        newsletter = get_object_or_404(Newsletter, id=newsletter_id)
        subscribers = Subscriber.objects.all()

        for subscriber in subscribers:
            # ✅ Ensure they have a valid token
            if not subscriber.unsubscribe_token:
                subscriber.unsubscribe_token = uuid4()
                subscriber.save()

            unsubscribe_url = request.build_absolute_uri(
                reverse("unsubscribe", args=[subscriber.unsubscribe_token])
            )

            html_content = render_to_string("newsletter.html", {
                "subject": newsletter.title,
                "message": mark_safe(newsletter.description),
                "banner_url": newsletter.banner_image.url if newsletter.banner_image else None,
                "button_url": "http://localhost:8000",  # Or dynamic value
                "unsubscribe_url": unsubscribe_url,
            })

            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                subject=newsletter.title,
                body=text_content,
                from_email="projectmoonwalk01@gmail.com",
                to=[subscriber.email],
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

        self.message_user(request, f"✅ Newsletter '{newsletter.title}' sent to all subscribers.", messages.SUCCESS)
        return redirect("admin:myapp_newsletter_changelist")
    
#unregister and re-register (django thing)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Order, OrderAdmin)