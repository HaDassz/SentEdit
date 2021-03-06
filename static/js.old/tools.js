$(function(){
  var hash = window.location.hash;
  hash && $('ul.nav a[href="' + hash + '"]').tab('show');

  $('.navbar-nav a').click(function (e) {
    $(this).tab('show');
    var scrollmem = $('body').scrollTop() || $('html').scrollTop();
    window.location.hash = this.hash;
    $('html,body').scrollTop(scrollmem);
  });
});

function trim(str)
{
	return str.replace(/^[\s,]+|[\s,]+$/gm,'');
}

function split(str)
{
	if(!str){
		return [];
	}else{
		return str.split(/[\s,]+/);
	}
}

function trim_and_split(str)
{
	return split(trim(str));
}

function collect_sentedit()
{
	var data={}
	data.text=$('#sentedit_input').val();
	data.wordseg=$("#wordseg").prop("checked");
	data.wordtab=$('input[name=wordtab]:checked').val();
    return data;
}


function request_sentedit()
{
	$('#sentedit_output').val('');
	var data=collect_sentedit();
	if(data.text.length==0){
		return;
	}
	console.log('SEND:');
	console.log(data);
	var data_str=JSON.stringify(data);
	var obj={
		contentType:"application/json",
		type: "POST",
		url: "/sentedit2/",
		dataType: 'json',
		data:data_str ,
		//timeout:3000,
		error: function(xhr){
			$('#sentedit_output').html("計算過程發生錯誤！");
			$('#sentedit_output').html(xhr.responseText);
		},
		success: function(response){
			var arr=[];
			for(var key in response.stats){
				arr.push(['level '+key, response.stats[key]])
			}
			console.log('RECEIVE:');
			console.log(response.output);	
			console.log(response.word_list);	
			console.log(arr);	
			drawChart(arr);
			$('#sentedit_output').html(response.output);
		}
	};
	$.ajax(obj);

}


