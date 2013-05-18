// ------------------------------------------------------------------ 
function vote_onItem_03(elem, object_id, content_type, ajaxProcessingUrl, currentVote, thisVote, vote_1, vote_2, vote_3) {
//    debugger; 

    var divParent   = $(elem).parent();
    var upChild     = divParent.children().filter("div:first"); 
    var downChild   = divParent.children().filter("div:last");
    var middleChild = divParent.children().filter("div:eq(1)");
    
//    console.log("vote_1 = " + vote_1)
//    console.log("vote_2 = " + vote_2)
//    console.log("vote_3 = " + vote_3)
    
    if  (thisVote == 'up') {
        if (upChild.attr("class") == "arrow upmod") {
            upChild.attr("class", "arrow up");
            middleChild.html(vote_2);            
        }
        else {
            upChild.attr("class", "arrow upmod");
            middleChild.html(vote_1);            
        }

        downChild.attr("class", "arrow down");   
    }
    else {
        upChild.attr("class", "arrow up");   

        if (downChild.attr("class") == "arrow downmod") {
            downChild.attr("class", "arrow down");
            middleChild.html(vote_2);            
        }
        else {
            downChild.attr("class", "arrow downmod");
            middleChild.html(vote_3);            
        }
    }

    // Assemble dataDict
    var dataDict = {};
    dataDict['object_id']       = object_id;
    dataDict['content_type']    = content_type;

    // Post data dict to processing url
	$.post(
			ajaxProcessingUrl,	        		// url:      The URL of the page to load.
			dataDict                            // data:     Key/value pairs that will be sent to the server.                       (optional)
	);    
    
	return false;
};

// ------------------------------------------------------------------ 
function toggle_subscription_03(elem, object_id, content_type, ajaxProcessingUrl) {
    // Toggle text
    if ($(elem).html() == "Subscribe") {
        $(elem).html("Un-Subscribe");
    }  
    else {
        $(elem).html("Subscribe");
    };

    // Assemble dataDict
    var dataDict = {};
    dataDict['object_id']    = object_id;
    dataDict['content_type'] = content_type;

    // Post data dict to processing url
	$.post(
			ajaxProcessingUrl,	        		// url:      The URL of the page to load.
			dataDict                            // data:     Key/value pairs that will be sent to the server.                       (optional)
	);    
    
	return false;
};

// ------------------------------------------------------------------ 
function toggle_03(elem, key, callback) {
	var self = $(elem).parent().andSelf().filter("." + key);
	var sibling = self.toggleClass("inactive").siblings().toggleClass("inactive").get(0);
	if(callback) callback(elem);
	return false;
};

// ------------------------------------------------------------------ 
function extract_thread_id(ff_name) {
    var split1 = ff_name.split(":");
    var split2 = split1[1].split("-",1);
    return split2;
};

// ------------------------------------------------------------------ 
function cancel_edit_05(elem) {
	// Find parent span with id=formSpan
	var formSpan 	= $(elem).parents("span[id=formSpan]");
	var spanParent 	= formSpan.parent();
	var divParent 	= spanParent.parent();
	
	// hide input form
	if (formSpan.hasClass("inactive") == false){
		formSpan.addClass("inactive");
	}
	
	// show all links from spanParent 
	spanParent.children().filter("a").show();
	spanParent.children().filter(".hackCancel").hide();   // temp hack to undisplay cancel link
	
	// show all .hide-for-edit class elements from divParent 
	divParent.children().filter(".hide-for-edit").show();
	
	// hide cancel button 
	formSpan.find("button[name=cancel]").hide().end();
	
	// Find and remove text from  textarea input form field 
	//formSpan.find("textarea").attr("value", "");  
	
	// Find the hiddenWasEdited hidden form field and set its value back to 0
	var hiddenWasEdited = $("input:hidden:last", formSpan);
	hiddenWasEdited.attr("value",0);
};

// ------------------------------------------------------------------ 
function reply_03(elem) {
	var self = $(elem).parent().find('textarea:first').focus();
	var content;
    var node;
    
    //alert("reply_03");
	
	// show cancel button 
	var spanParent 	= $(elem).parent();
	var formSpan 	= spanParent.find("span");
	formSpan.find("button[name=cancel]").show().end();

	// Find and remove text from  textarea input form field 
	//formSpan.find("textarea").attr("value", "");  
	//formSpan.find("textarea").data("");  
	//formSpan.find("textarea").html("blue");

    node = formSpan.find("textarea");
    content = node.html();
    if (content.length){
	       node.html("");  
    }
    content = node.attr("value");
    if (content.length){
	       node.attr("value", "");  
    }
};

// ------------------------------------------------------------------ 
function edit_03(elem) {
	var spanParent 	= $(elem).parent();
	var divParent 	= spanParent.parent();
	var formSpan 	= spanParent.find("span");

    //alert("edit_03");

	// display input form 
	if (formSpan.hasClass("inactive")) {
		formSpan.removeClass("inactive");
	}
	
	// hide all links from spanParent 
	spanParent.children().filter("a").hide();
	
	// hide all .hide-for-edit class elements from divParent 
	divParent.children().filter(".hide-for-edit").hide();
    
    // VERSION 2
    var thread_id = extract_thread_id(formSpan.find("textarea").attr("name"));
	formSpan.find("textarea").load('/thread/raw/'+thread_id+'/');
    formSpan.find("textarea").attr(formSpan.find("textarea").html());
	formSpan.find('textarea').focus();

	//alert("textarea attr =" + formSpan.find("textarea").attr("value"));  

    
    // show cancel button 
	formSpan.find("button[name=cancel]").show().end();
	
	// Find the hiddenWasEdited hidden form field and set its value to 1 to indicate an edit is occurring
	var hiddenWasEdited = $("input:hidden:last", formSpan);
	hiddenWasEdited.attr("value",1);
	
	return false;
};

// ------------------------------------------------------------------ 
function submit_reply_04(form) {
	var formSpan 	= $(form).parent();
	var spanParent 	= formSpan.parent();
	var divParent 	= spanParent.parent();
	
	// Find the hiddenWasEdited hidden form field and set its value to 1 to indicate an edit is occurring
	var hiddenWasEdited = $("input:hidden:last", formSpan);
	if (hiddenWasEdited.attr("value") == "1") {
		
        // Find and insert textarea input text into comment text unless no text was entered 
        var content_node = formSpan.find("textarea");
		var content = content_node.attr("value");
        if (content.length){
			
			// ----------------- submit results via ajax/javascript
			var dataDict = {};
			var ff_value = content_node.attr("value");
			var ff_name  = content_node.attr("name");
			dataDict[ff_name] = ff_value;

            // ----------------------
			// don't forget the hidden fields which are required.
			var requiredHiddenFields = formSpan.find("input[type=hidden]").get();
			for (x in requiredHiddenFields) { 
				var ff_value = requiredHiddenFields[x].value;
				var ff_name  = requiredHiddenFields[x].name;
				dataDict[ff_name] = ff_value;
			}	
			
			$.post(
					formSpan.find("form").attr("action")+"?xhr",			// url:      The URL of the page to load.
					dataDict                                                // data:     Key/value pairs that will be sent to the server.                       (optional)
			);   

            // Version 2:
            var thread_id = extract_thread_id(content_node.attr("name"));
            var node = divParent.children().filter(".blueContent");
            node.load('/thread/bbcode/'+thread_id+'/');
            node.attr("value", node.html());  
            //alert ("node.html = "+node.html());
			
            cancel_edit_05(form);
		};
		return false;
	}
	else {
		return true;
	}
}

// ------------------------------------------------------------------ 
function queue_definition(elem, definition) {
		
	$.post(
			'/definition/queue/'+definition+'/'
	);   
    
    var new_node_data = $.get('/definition/sidebar/');   

    $.get('/definition/sidebar/',
          {},
          function(data){
                         $(".definition-sidebar").html(data);
                         }
          );
          
	return true;
};

// ------------------------------------------------------------------ 
// The ready method 
$(function() {
});