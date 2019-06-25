$(document).ready(function(){
  tinymce.init({ 
    selector:'.section-add-article textarea',
    plugins: 'print preview fullpage searchreplace autolink directionality visualblocks visualchars fullscreen image link media template codesample table charmap hr pagebreak nonbreaking anchor toc insertdatetime advlist lists textcolor wordcount  imagetools   contextmenu colorpicker textpattern help',
    toolbar1: 'formatselect | bold italic strikethrough forecolor backcolor | link | image | alignleft aligncenter alignright alignjustify  | numlist bullist outdent indent  | removeformat',
    image_advtab: true,
    language: 'ru' 
  });
	// initialize tabs
	$('ul.tabs.autorization').tabs({
		// swipeable: true,	
	});

	// initialize select
	if (window.innerWidth <= 992) {
		$('select').addClass('browser-default');
	} else {
		$('select').material_select();
	}

  $('.multiple-select input[type="checkbox"]').addClass('filled-in custom-checkbox-filter');

	// initialize textarea
	$('#textarea, .materialize-textarea').trigger('autoresize');

  $(window).load(function(){
    $('#id_article').removeAttr('required');
  });

  $.datepicker.setDefaults( $.datepicker.regional[ "ru" ] );
  $( function() {
    $( ".datepicker" ).datepicker();
  } );

  $("a[href='#']").on('click', function(e) {
    e.preventDefault();
  });

  $('.section-article .article img, .section-found-article .article img').addClass('responsive-img');

  $('.avatar_upload #avatar-clear_id').addClass('filled-in custom-checkbox-filter');
  $('.file-field .btn input').remove();
  $('.avatar_upload #id_avatar').appendTo('.file-field .btn');

  $('#id_avatar').dropify({
      messages: {
          default: 'Перетащите сюда или нажмите, чтобы загрузить изображение',
          replace: 'Перетащите сюда или нажмите, чтобы заменить изображение',
          remove:  'Очистить',
          error:   'Ошибка'
      },
      tpl: {
        clearButton: '<label for="avatar-clear_id" class="dropify-clear">{{ remove }}</label><input type="checkbox" name="avatar-clear" id="avatar-clear_id" />',
      }
  });

  $('#id_photo').dropify({
      messages: {
          default: 'Перетащите сюда или нажмите, чтобы загрузить изображение',
          replace: 'Перетащите сюда или нажмите, чтобы заменить изображение',
          remove:  'Очистить',
          error:   'Ошибка'
      },
      tpl: {
        clearButton: '<label for="photo-clear_id" class="dropify-clear">{{ remove }}</label><input type="checkbox" name="photo-clear" id="photo-clear_id" />',
      }
  });

  $('#id_image').dropify({
      messages: {
          default: 'Перетащите сюда или нажмите, чтобы загрузить изображение',
          replace: 'Перетащите сюда или нажмите, чтобы заменить изображение',
          remove:  'Очистить',
          error:   'Ошибка'
      },
      tpl: {
        clearButton: '<label for="image-clear_id" class="dropify-clear">{{ remove }}</label><input type="checkbox" name="image-clear" id="image-clear_id" />',
      }
  });

  $(window).on('scroll',function() {
    var doc = window.pageYOffset;
    if(doc > 300) {
        $(".up").removeClass("scale-out");
    } else {
        $(".up").addClass("scale-out");
    }
  });
  $(".up").on("click", function() {
    $("body, html").stop().animate({scrollTop:0}, 500, 'swing');
  });

  function checkingNumber(input) {
    input.value = input.value.replace(/[^\d]/g,'');
  };

  $('#id_age-from .custom-input-filter, #id_age-before .custom-input-filter').on('keyup', function(){
      checkingNumber(this);
  });

  $('.section-my-pets .custom-block-body .row.margin-bottom-0').slick({
    slidesToShow: 4,
    slidesToScroll: 1,
    infinite: false,
    dots: false,
    arrows: true,
    prevArrow: '<a href="#" class="previous"><i class="small material-icons">keyboard_arrow_left</i></a>', 
    nextArrow: '<a href="#" class="next"><i class="small material-icons">keyboard_arrow_right</i></a>',
    appendArrows: '.section-my-pets .navig',
    responsive: [
      {
        breakpoint: 650,
        settings: {
          slidesToShow: 3
        }
      },
      {
        breakpoint: 380,
        settings: {
          slidesToShow: 2
        }
      }
    ]
  });

  $('.section-most-popular .custom-block-body .row.margin-bottom-0').slick({
    slidesToShow: 4,
    slidesToScroll: 1,
    dots: false,
    arrows: true,
    prevArrow: '<a href="#" class="previous"><i class="small material-icons">keyboard_arrow_left</i></a>', 
    nextArrow: '<a href="#" class="next"><i class="small material-icons">keyboard_arrow_right</i></a>',
    appendArrows: '.section-most-popular .navig',
    responsive: [
      {
        breakpoint: 650,
        settings: {
          slidesToShow: 3
        }
      },
      {
        breakpoint: 380,
        settings: {
          slidesToShow: 2
        }
      }
    ]
  });

  $('.section-last-article .custom-block-body .row.margin-bottom-0').slick({
    slidesToShow: 4,
    slidesToScroll: 1,
    dots: false,
    arrows: true,
    prevArrow: '<a href="#" class="previous"><i class="small material-icons">keyboard_arrow_left</i></a>', 
    nextArrow: '<a href="#" class="next"><i class="small material-icons">keyboard_arrow_right</i></a>',
    appendArrows: '.section-last-article .navig',
    responsive: [
      {
        breakpoint: 650,
        settings: {
          slidesToShow: 3
        }
      },
      {
        breakpoint: 440,
        settings: {
          slidesToShow: 2
        }
      }
    ]
  });

  $('.section-most-popular-blog .custom-block-body .row.margin-bottom-0').slick({
    slidesToShow: 4,
    slidesToScroll: 1,
    dots: false,
    arrows: true,
    prevArrow: '<a href="#" class="previous"><i class="small material-icons">keyboard_arrow_left</i></a>', 
    nextArrow: '<a href="#" class="next"><i class="small material-icons">keyboard_arrow_right</i></a>',
    appendArrows: '.section-most-popular-blog .navig',
    responsive: [
      {
        breakpoint: 650,
        settings: {
          slidesToShow: 3
        }
      },
      {
        breakpoint: 440,
        settings: {
          slidesToShow: 2
        }
      }
    ]
  });

  $('.section-user-last-article .custom-block-body .row.margin-bottom-0').slick({
    slidesToShow: 4,
    slidesToScroll: 1,
    dots: false,
    arrows: true,
    prevArrow: '<a href="#" class="previous"><i class="small material-icons">keyboard_arrow_left</i></a>', 
    nextArrow: '<a href="#" class="next"><i class="small material-icons">keyboard_arrow_right</i></a>',
    appendArrows: '.section-user-last-article .navig',
    responsive: [
      {
        breakpoint: 650,
        settings: {
          slidesToShow: 3
        }
      },
      {
        breakpoint: 440,
        settings: {
          slidesToShow: 2
        }
      }
    ]
  });

  $('.section-user-animal-photo .block .user-photo-carousel').slick({
    slidesToShow: 4,
    slidesToScroll: 1,
    dots: false,
    arrows: true,
    prevArrow: '<a href="#" class="previous"><i class="medium material-icons">keyboard_arrow_left</i></a>', 
    nextArrow: '<a href="#" class="next"><i class="medium material-icons">keyboard_arrow_right</i></a>',
    appendArrows: '.section-user-animal-photo .row.margin-bottom-0',
    responsive: [
      {
        breakpoint: 650,
        settings: {
          slidesToShow: 3
        }
      },
      {
        breakpoint: 440,
        settings: {
          slidesToShow: 2
        }
      }
    ]
  });

  $('.section-animal-about-article .custom-block-body .row.margin-bottom-0').slick({
    slidesToShow: 4,
    slidesToScroll: 1,
    dots: false,
    arrows: true,
    prevArrow: '<a href="#" class="previous"><i class="small material-icons">keyboard_arrow_left</i></a>', 
    nextArrow: '<a href="#" class="next"><i class="small material-icons">keyboard_arrow_right</i></a>',
    appendArrows: '.section-animal-about-article .navig',
    responsive: [
      {
        breakpoint: 650,
        settings: {
          slidesToShow: 3
        }
      },
      {
        breakpoint: 440,
        settings: {
          slidesToShow: 2
        }
      }
    ]
  });

  $('.section-similar-profiles .custom-block-body .row.margin-bottom-0').slick({
    slidesToShow: 6,
    slidesToScroll: 1,
    dots: false,
    arrows: true,
    prevArrow: '<a href="#" class="previous"><i class="small material-icons">keyboard_arrow_left</i></a>', 
    nextArrow: '<a href="#" class="next"><i class="small material-icons">keyboard_arrow_right</i></a>',
    appendArrows: '.section-similar-profiles .navig',
    responsive: [
      {
        breakpoint: 650,
        settings: {
          slidesToShow: 4
        }
      },
      {
        breakpoint: 440,
        settings: {
          slidesToShow: 3
        }
      }
    ]
  });

  $(function () {

    $('#ri-grid').gridrotator({
        // number of rows
        rows: 4,
        // number of columns 
        columns: 8,
        w320: {
            rows: 3,
            columns: 3
        },
        interval : 10000,
        // nochange: [0],
        preventClick: false
    });

  });

  $(window).on("scroll", function() {
    var top = $(document).scrollTop();
    var width = $(document).innerWidth();
    var header_height = $('.mobile-menu').height() + 80;

    if(top > header_height && width <= 992) {
        $(".mobile-menu").addClass('fixed');
    } else {
        $(".mobile-menu").removeClass('fixed');
    }
  });

});
	// Initialize collapse button
  $(".button-collapse").sideNav();