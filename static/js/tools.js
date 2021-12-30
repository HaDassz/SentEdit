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
	data.text=$('#sentedit_input').text();
	data.wordseg=$("#wordseg").prop("checked");
	data.wordtab=$('input[name=wordtab]:checked').val();
    data.corpus=$('input[name=corpus]:checked').val();
    data.limitWordLv=$('input[name=limit-word-level]:checked').val();
    data.topn=$('#topn').val();
    return data;
}

function request_sentedit()
{
	$('#sentedit_tag').val('');
	var data=collect_sentedit();
	if(data.text.length==0){
		return;
	}
	console.log('SEND:');
	console.log(data);
	var data_str=JSON.stringify(data);
	var obj={
		contentType:"application/json",
        beforeSend: function(){
            showDiv();
        },
        complete: function(){
            hiddenDiv();
            showBtn();
        },
		type: "POST",
		url: "/sentedit2/",
		dataType: 'json',
		data:data_str ,
		//timeout:3000,
		error: function(xhr){
			$('#sentedit_tag').html("計算過程發生錯誤！");
			$('#sentedit_tag').html(xhr.responseText);
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
			$('#sentedit_tag').html(response.output);
			$('#sentedit_word_list').html(response.word_list);
			$('#formSelectDiv').html(response.word_sim);
		}
	};
	$.ajax(obj);
}

function showDiv(){
    $('#loading').show();
}

function hiddenDiv(){
    $('#loading').hide();
}

function showBtn(){
    $('#scrShotBtn2').css('display', 'block');
    $('#scrShotBtn3').css('display', 'block');
    $('#scrShotBtn4').css('display', 'block');
}

/* ajaxComplete */
// $(document).ajaxComplete(
//     initformSelectDiv()
// )


