from settings import *

{% allkeys URL as urls %}

urlpatterns = patterns('',
    {% for keyconfig in urls %}
        {% if keyconfig.app.keys.url_path %}
            {% appkey keyconfig.app url_path as url_path %}
            url(r'^{{ url_path }}/', include({{ keyconfig.value }})),
        {% else %}
            url(r'^{{ keyconfig.app.name }}/', include({{ keyconfig.value }})),
        {% endif %}
    {% endfor %}
)