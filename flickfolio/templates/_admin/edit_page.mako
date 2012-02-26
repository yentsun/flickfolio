<%inherit file="admin.mako"/>
<%def name="title()">Редактирование страницы</%def>
<div>
	<form method="post" action="${save_url}">
		<fieldset>
			<label for="title">Заголовок <small>(нельзя менять)</small></label>
			<input id="title" disabled name="title" type="text" value="${page.title}">
			<label for="body">Текст страницы</label>
			<textarea id="body" name="body" rows="10" cols="30">${page.body}</textarea>
			<button class="save" type="submit">Сохранить</button>
		</fieldset>
	</form>
</div>
<%def name="js()">
	<script type="text/javascript" src="/static/admin/ckeditor/ckeditor.js"></script>
	<script type="text/javascript" src="/static/admin/ckeditor/adapters/jquery.js"></script>
	${parent.js()}
</%def>