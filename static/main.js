$(document).ready(function() {
    $('button.grid-item').click(function() {
        location.href = "/blog/" +  $(this).data("index") + "/" + $(this).data("slug");
    });
});