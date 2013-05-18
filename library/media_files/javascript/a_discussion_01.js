// --------------------------------------------------------
// The ready method 
$(function() {
});


// ------------------------------------------------------------------ 
function focusOnForm(elem) {
    var self = $(elem).parent().find('input:first').focus();
    //console.log(elem);
};


// ------------------------------------------------------------------ 
function toggle_sibling(elem, class, callback) {
    // Worked fine if all toggled siblings had the same parent                                                
    //$(elem).toggleClass("inactive");
    //var siblings = $(elem).siblings().filter("." + class).toggleClass("inactive");

    // Works better so that all toggled siblings can have the same grandparent
    var grandparent = $(elem).parent().parent().get(0);
    var allElementsThatToggle = $(grandparent).find("."+class).toggleClass("inactive");
    
    if(callback) callback(elem);
    return false;
};