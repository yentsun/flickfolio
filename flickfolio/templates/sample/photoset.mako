<%inherit file="layout.mako"/>
<%def name="title()">${photoset.title}</%def>
<h2 class="photoset">
    <a title="${photoset.previous.title}" href="/photoset/${photoset.previous.id}">&larr;</a>
    ${title()}
    <a title="${photoset.next.title}" href="/photoset/${photoset.next.id}">&rarr;</a>
</h2>
<div id="thumbs" class="gallery">
% for photo in photoset:
        <a id="th${photo.id}">
            <img src="${photo.square}" alt="${photo.title}">
        </a>
    % endfor
</div>
<div id="extended">
    <a href="${photoset.primary.big}">
        <img class="primary" id="ext${photoset.primary.id}" src="${photoset.primary.extended}" alt="заглавное фото">
    </a>
    % for photo in photoset:
        <a href="${photo.big}">
            <img id="ext${photo.id}" src="${photo.extended}" alt="фото ${photo.id}">
        </a>
    % endfor
</div>
<div id="description">
    ${photoset.description | n}
</div>
<script type="text/javascript">
	var pageId = 4;
</script>
<%def name="js()">
    <script type="text/javascript" src="/static/js/fancybox/jquery.fancybox-1.3.4.pack.js"></script>
    <script type="text/javascript" src="/static/js/fancybox/jquery.easing-1.3.pack.js"></script>
</%def>
<%def name="css()">
    <link rel="stylesheet" href="/static/js/fancybox/jquery.fancybox-1.3.4.css" type="text/css">
</%def>