<%inherit file="admin.mako"/>
<%def name="title()">Панель управления</%def>
% if pages:
<h3>Страницы</h3>
	<table class="list">
	% for page in pages:
		<tr>
			<td>
				<a title="Редактировать" href="/edit_page/${page.slug}">${page.title}</a>
			</td>
			<td>
				<span title="URL страницы">/${page.slug}</span>	
			</td>
		</tr>
	% endfor
	</table>
<h3>Персональная информация</h3>
    <table class="list">
        <tr>
            <td>Идентификатор flickr-пользователя</td>
            <td><code>${settings[0].value}</code></td>
        </tr>
        <tr>
            <td>API-ключ</td>
            <td><code>${settings[1].value}</code></td>
        </tr>
    </table>
% endif