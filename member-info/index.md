---
layout: default
title: Important Info for Members
---
Before flying at the BSRCC field, please review the following information.

{% for item in site.data.member_info_links %}
[{{item.text}}]({{item.link}})
{% endfor %}
