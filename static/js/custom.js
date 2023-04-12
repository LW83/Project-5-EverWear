/// Tailored from CodeArtisanLab ///

$(document).ready(function(){
	$('#add_bag').attr('disabled',true);
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
		$('#add_bag').attr('disabled', false);
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

/// From CodeArtisanLab ///

// Product Review Save
$("#addForm").submit(function(e){
	$("#productReview").hide();

	$.ajax({
		data:$(this).serialize(),
		method:$(this).attr('method'),
		url:$(this).attr('action'),
		dataType:'json',
		success:function(res){
			if(res.bool==true){
				$(".ajaxRes").html('Data has been added.');
				$("#reset").trigger('click');
				// Hide Button
				$(".reviewBtn").hide();
				// End

				// create data for review
				var _html='<blockquote class="blockquote">';
				_html+='<small>'+res.data.review_text+'</small>';
				_html+='<footer class="blockquote-footer text-right">'+res.data.user;
				_html+='<cite title="Source Title">';
				for(var i=1; i<=res.data.review_rating; i++){
					_html+='<i class="fa fa-star text-white"></i>';
				}
				_html+='</cite>';
				_html+='</footer>';
				_html+='</blockquote>';
				_html+='</hr>';

				$(".no-data").hide();

				// Prepend Data
				$(".review-list").prepend(_html);

				// Hide Modal
				$("#productReview").hide();

			}
		}
	});
	e.preventDefault();
});
// End
