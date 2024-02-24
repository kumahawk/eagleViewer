function flipScreenMode(id = null) {
    const slide = document.getElementById('img_slide');
    const grid = document.getElementById('img_grids');
    const tocarousel = !slide.classList.contains('carousel');
    if(! id) {
        if(tocarousel) {
            let a = document.activeElement;
            while(a) {
                if(a.id.startsWith('img_')) {
                    id = a.id.substr('img_'.length);
                    break;
                }
                a = a.parent;
            }
        }
        else {
            let a = document.querySelector(".carousel-item.active");
            if(a && a.id.startsWith('img_')) {
                id = a.id.substr('img_'.length);
            }
        }
    }
    var selected = document.getElementById('img_'+id);
    if(! selected) {
        if(grid.children.length > 0) {
            selected = grid.children[0];
        }
    }
    for(const e of grid.children) {
        const i = e.querySelector('img');
        if(i) {
            if(tocarousel) {
                if(i.hasAttribute('width')) {
                    i.setAttribute('data-twidth', i.getAttribute('width'));
                    i.removeAttribute('width');
                }
                if(i.hasAttribute('height')) {
                    i.setAttribute('data-theight', i.getAttribute('height'));
                    i.removeAttribute('height');
                }
                if(i.hasAttribute('data-rsrc')) {
                    i.setAttribute('data-tsrc', i.getAttribute('src'));
                    i.setAttribute('src', i.getAttribute('data-rsrc'));
                    i.removeAttribute('data-rsrc');
                }
            }
            else {
                if(i.hasAttribute('data-twidth')) {
                    i.setAttribute('width', i.getAttribute('data-twidth'));
                    i.removeAttribute('data-twidth');
                }
                if(i.hasAttribute('data-theight')) {
                    i.setAttribute('height', i.getAttribute('data-theight'));
                    i.removeAttribute('data-theight');
                }
                if(i.hasAttribute('data-tsrc')) {
                    i.setAttribute('data-rsrc', i.getAttribute('src'));
                    i.setAttribute('src', i.getAttribute('data-tsrc'));
                    i.removeAttribute('data-tsrc');
                }
            }
        }
        if(e == selected) {
            if(tocarousel) {
                e.classList.toggle('active', true);
            }
            else {
                e.focus();
            }
        }
        else {
            e.classList.toggle('active', false);
        }
        e.classList.toggle('col', !tocarousel);
        e.classList.toggle('carousel-item', tocarousel);
    }
    grid.classList.toggle('row', !tocarousel);
    grid.classList.toggle('row-cols-auto', !tocarousel);
    grid.classList.toggle('carousel-inner', tocarousel);
    slide.classList.toggle('carousel', tocarousel);
    slide.classList.toggle('slide', tocarousel);
    if(selected) {
        selected.scrollIntoView({block: 'start', behavior: 'instant'});
    }
}

const templ = Handlebars.compile(
`<div id="img_{{id}}" class="col" tabindex="1">
    <div class="row bg-secondary-subtle">
        <div class="column col-lg-9 text-center">
            <a onclick='flipScreenMode("{{id}}");'><img class="img-thumbnail" src="/images/{{id}}/{{thumbname}}" width="{{thumbwidth}}px" height="{{thumbheight}}px"
                 {{#if noThumbnail}}data-rsrc="/images/{{id}}/{{name}}.{{ext}}"{{/if}}></a>
        </div>
        <div class="column side col-lg-3 img_info">
            <div class="img_folders list-group">
                {{#each folders}}
                <div class="list-group-item list-group-item-info">{{this}}</div>
                {{/each}}
            </div>
            <div class="img_tags list-group">
                {{#each tags}}
                <div class="list-group-item list-group-item-secondary">{{this}}</div>
                {{/each}}
            </div>
            <div class="img_annotation bg-primary text-wrap">
                {{annotation}}
            </div>
        </div>
    </div>
</div>`);

function fillnext() {
    let e = document.getElementById('img_next');
    num = e.parentNode.children.length;
    fetch("/eagle/fetch/" + (num-1) + location.search)
    .then(function(res){
        return res.json();
    })
    .then(function(json) {
        for(i of json.images) {
            e.insertAdjacentHTML('beforebegin', templ(i));
        }
    })
}