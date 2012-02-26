<%inherit file="layout.mako"/>
<%page cached="True" cache_timeout="86400" cache_type="file" cache_dir="cache" cache_key="${photo.id}"/>
<%def name="title()">Фото ${photo.title}</%def>
<img src="${photo.original}" alt="${photo.title}">
<script type="text/javascript">
	var pageId = 4;
</script>
