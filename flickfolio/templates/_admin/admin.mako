<%inherit file="layout.mako"/>
<%def name="css()"><link rel="stylesheet" href="/static/admin/admin.css" type="text/css" media="screen"></%def>
<%def name="title()">${next.title()}</%def>
<h2>${title()}</h2>
% if request.session.peek_flash():
<div id="flash">
	<% flash = request.session.pop_flash() %>
	% for message in flash:
		${message | n}
	% endfor
</div>
% endif
<div class="admin">
	${next.body()}
</div>
<%def name="js()">
	<script type="text/javascript" src="/static/admin/admin.js"></script>
</%def>
