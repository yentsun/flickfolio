<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
	<head>
<%def name="titlePrefix()">\
% if hasattr(self,'title'):
${self.title()} - \
%endif
</%def>
		<title>${titlePrefix()}</title>
		<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
  		<meta name="keywords" content="python web application">
  		<meta name="description" content="pyramid web application">
		<link rel="shortcut icon" href="/static/favicon.png">
		<link rel="stylesheet" href="/static/css/main.css" type="text/css" media="screen" charset="utf-8">
		% if hasattr(self,'css'):
		${self.css()}
		% endif
	</head>
	<%def name="bodyId()">general</%def>
	<body id="${next.bodyId()}">
		<div id="wrapper">
			<div id="header">
				Для использования сайта необходимо установить Flash!
  			</div>
			<div id="middle">
				${next.body()}
			</div>
  			<div id="footer">
				<a href="/page/about">О нас</a> |
				<a href="/portfolio">Портфолио</a> |
				<a href="/projects">Дизайн-проект</a> | 
				<a href="/page/contacts">Контакты</a> | 
				<a href="/page/partners">Наши партнеры</a> 
				<p>
					Все права защищены &copy; 2011. 
					При использовании материала, ссылка на сайт обязательна.
				</p>
  			</div>
		</div>
		<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.5.0/jquery.min.js"></script>
		<script type="text/javascript" src="/static/js/main.js"></script>
		% if hasattr(self,'js'):
		${self.js()}
		% endif
	</body>
</html>
