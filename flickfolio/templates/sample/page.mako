<%inherit file="layout.mako"/>
<%def name="title()">${page.title}</%def>
<h2>${title()}</h2>
<div>
	${page.body | n}
</div>
<script type="text/javascript">
	var pageId = ${page.menuId};
</script>