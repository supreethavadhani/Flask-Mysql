$(function(){
	$('#btnAddSector').click(function(){

		$.ajax({
			url: '/addSector',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});
