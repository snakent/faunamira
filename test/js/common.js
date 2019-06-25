// initialize tabs
$(document).ready(function(){
	$('ul.tabs.autorization').tabs({
		// swipeable: true,	
	});
});
// initialize select
$(document).ready(function() {
	$('select').material_select();
});
// initialize textarea
$(document).ready(function(){
	$('#textarea').trigger('autoresize');
});
// Initialize collapse button
  $(".button-collapse").sideNav()

$(function(){
  $('.crsl-items-people').carousel({
    visible: 4,
    itemMinWidth: 150,
    itemEqualHeight: 150,
    itemMargin: 0,
  });
  
  $("a[href=#]").on('click', function(e) {
    e.preventDefault();
  });
});

$(function(){
  $('.crsl-items-1').carousel({
    visible: 4,
    itemMinWidth: 150,
    itemEqualHeight: 150,
    itemMargin: 0,
  });
  
  $("a[href=#]").on('click', function(e) {
    e.preventDefault();
  });
});

// post slider
$(function(){
  $('.crsl-items').carousel({
    visible: 4,
    itemMinWidth: 150,
    itemEqualHeight: 150,
    itemMargin: 15,
  });
  
  $("a[href=#]").on('click', function(e) {
    e.preventDefault();
  });
});

// initialize grid random
// function getRandomSize(min, max) {
//   return Math.round(Math.random() * (max - min) + min);
// }

// var allImages = "";

// for (var i = 0; i < 25; i++) {
//   var width = getRandomSize(200, 400);
//   var height =  getRandomSize(200, 400);
//   allImages += '<img src="http://lorempixel.com/'+width+'/'+height+'/people" alt="">';
// <img src="http://lorempixel.com/200/200/people" class="responsive-img-height" alt="">
// }

// $('#photos').append(allImages);

// initialize freewall
$(document).ready(function () {
	$(function() {
		var wall = new Freewall("#freewall");
		if ($(window).width() < 1025) { 
			wall.reset({
			selector: '.level1',
			cellW: 100,
			cellH: 80,
			fixSize: 0,
			gutterX: 0,
			gutterY: 0,
			onResize: function() {
				wall.fitZone();
			}
		});
		} else {
			wall.reset({
			selector: '.level1',
			cellW: 70,
			cellH: 60,
			fixSize: 0,
			gutterX: 0,
			gutterY: 0,
			onResize: function() {
				wall.fitZone();
			}
		});
		}
		wall.fitZone();
		$(window).trigger("resize");
	});
});

$(document).ready(function () {
	$(function() {
		var wall = new Freewall("#freewall1");
		if ($(window).width() < 1025) { 
			wall.reset({
			selector: '.level1',
			cellW: 100,
			cellH: 80,
			fixSize: 0,
			gutterX: 0,
			gutterY: 0,
			onResize: function() {
				wall.fitZone();
			}
		});
		} else if ($(window).width() < 1367) {
			wall.reset({
			selector: '.level1',
			cellW: 80,
			cellH: 60,
			fixSize: 0,
			gutterX: 0,
			gutterY: 0,
			onResize: function() {
				wall.fitZone();
			}
		});
		} else {
			wall.reset({
			selector: '.level1',
			cellW: 100,
			cellH: 100,
			fixSize: 0,
			gutterX: 0,
			gutterY: 0,
			onResize: function() {
				wall.fitZone();
			}
		});
		}
		wall.fitZone();
		$(window).trigger("resize");
	});
});