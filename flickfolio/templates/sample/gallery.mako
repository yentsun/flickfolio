<%inherit file="layout.mako"/>
<%page cached="True" cache_timeout="86400" cache_type="file" cache_dir="cache" cache_key="gallery"/>
<%def name="title()">Дизайн-проект</%def>
% if gallery:
<div id="projects" class="gallery">
    <% i = 1 %>
	% for photoset in gallery:
        <div
            % if i%2 == 0:
            class="last"
            % endif
        >
    	    <a href="/photoset/${photoset.id}">
    		    <span style="background-image:url(${photoset.primary.medium})">
                </span>
                ${photoset.title}
	        </a>
        </div>
        <% i += 1 %>
	% endfor
</div>
% endif
<script type="text/javascript">
	var pageId = 4;
</script>