$(function(){
	if ($('.admin textarea').length) {
		$('.admin textarea').ckeditor({
			toolbar_Full: [
				{ name: 'basicstyles', items : [ 'Bold','Italic','Underline','Strike','Subscript','Superscript','-','RemoveFormat' ] },
	 			{ name: 'clipboard',   items : [ 'Cut','Copy','Paste','PasteText','PasteFromWord','-','Undo','Redo' ] },
	 			{ name: 'paragraph',   items : [ 'NumberedList','BulletedList','-','Outdent','Indent','-','Blockquote','-','JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock','-','BidiLtr','BidiRtl' ] },
	 			{ name: 'links',       items : [ 'Link','Unlink','Anchor' ] },
	 			{ name: 'insert',      items : [ 'Image','Table' ] },
	 			{ name: 'misc',      items : [ 'Source' ] },
	 		],
	 	});
	}	
});
