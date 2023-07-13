window.onload = function () {
    const tags_list = document.querySelectorAll('.balance');
    for (let tag_item of tags_list) {
        tag_item.innerHTML = numberWithCommas(tag_item.innerHTML)
    }
}

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
}