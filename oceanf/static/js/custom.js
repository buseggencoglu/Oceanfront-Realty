$('input[name="dates"]').daterangepicker();
$('#id_name').inputmask({
    'regex': '([A-Za-z]* ?[A-Za-z]* [A-Za-z]*)'
});
$('#id_card_number').inputmask({
    'mask': '9999-9999-9999-9999',
    'placeholder': 'xxxx-xxxx-xxxx-xxxx'
});
$('#id_expire_date').inputmask({
    'mask': '99/99',
    'placeholder': 'MM/YY'
});
$('#id_ccr').inputmask({
    'mask': '999'
});

$('#id_plate').inputmask({
    'regex': '([0-9]{2})\ ([A-Z]{1,3})\ ([0-9]{2,4})',
});

$('#id_year').inputmask({
    'regex': '999'
});

$('.toast').toast({
    autohide: false
});
$('.toast').toast('show');

function notificationDeleted(id) {
    $.ajax({
        url: '/delete/notification/' + id,
        success: function () {
            $('#toast-' + id).toast('hide');
        }
    });
}

// to get current year
function getYear() {
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    document.querySelector("#displayYear").innerHTML = currentYear;
}

getYear();

// owl carousel

$('.owl-carousel').owlCarousel({
    loop: true,
    margin: 10,
    nav: true,
    autoplay: true,
    autoplayHoverPause: true,
    responsive: {
        0: {
            items: 1
        },
        600: {
            items: 3
        },
        1000: {
            items: 6
        }
    }
})