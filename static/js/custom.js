$(document).ready(function(){
	// Product Variation
	$(".size_section").hide();

	// Show size according to selected color
	$(".choose-color").on('click',function(){
		$(".choose-color").removeClass('customfocuscolor');
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

// // $(".choose-color").change(function() {
// // 	var attr_size = $(this).find("option:selected").data("variation-id-1") //get attr value
// // 	//hide all div inside buttons
// // 	$("#buttons div").hide()
// // 	//show only divs where match found
// // 	$("#buttons input[data-variation-id-2=" + attr_size + "]").closest('div').show()
  
// //   });
// //   $("select[name=size]").trigger('change')
  

// $(".choose-color").on('click',function(){
// 	$(".choose-size").removeClass('active');
// 	$(".choose-color").removeClass('focused');
// 	$(this).addClass('focused');

// 	var _color=$(this).attr('data-color');

// 	$(".choose-size").hide();
// 	$(".color"+_color).show();
// 	$(".color"+_color).first().addClass('active');