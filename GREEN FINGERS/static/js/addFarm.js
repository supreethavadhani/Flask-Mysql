$(function(){
	$('#btnAddFarm').click(function(){

		$.ajax({
			url: '/addFarm',
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
