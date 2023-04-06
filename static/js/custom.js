$(document).ready(function(){
	// Product Variation
	$(".size_section").hide();

	// Show size according to selected color
	$(".choose-color").on('click',function(){
		$(".choose-color").removeClass('customfocuscolor');
		$(".choose-color").removeClass('focus');
		$(".size_section").show();
		
		$(this).addClass('customfocuscolor');
		$(this).addClass('focus');

		var _color=$(this).attr('data-color');

		$(".choose-size").hide();
		$(".color"+_color).show();
	});

	$(".choose-size").on('click',function(){
		$(".choose-size").removeClass('customfocussize')
			
		$(this).addClass('customfocussize');
	
		var _size=$(this).attr('data-size');
	});
	// End
});

function storeColor(id_product_color) {
	var color = id_product_color.getAttribute('data-color-name'); 
	$('#js_data_input').val(color)
	console.log(color);
}

function storeSize(id_product_size) {
	var size = id_product_size.getAttribute('value'); 
	$('#js_data_input2').val(size)
	console.log(size);
}