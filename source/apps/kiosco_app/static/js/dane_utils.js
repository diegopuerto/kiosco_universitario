$(document).ready(function() {
    function localeTodayString(locale){
	var d = new Date();
	return d.toLocaleDateString(locale,{weekday: "long", day: "numeric",  month: "long", year: "numeric"});
    };
    // Update today dates on objects
    $(".today_display").text(localeTodayString("es-co"))
})
