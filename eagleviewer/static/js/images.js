const myUpdating = new bootstrap.Modal('#updating', {});
const slide = document.getElementById('img_slide');
const grid = document.getElementById('img_grids');
const menu = document.getElementById("starcontextmenu");
const myModalAlternative = new bootstrap.Modal(menu, {backdrop:true});
const nextpanel = document.getElementById('img_next');
const updating = document.getElementById("updating");
const error = document.getElementById("errormessage");
const navbar = document.getElementById("navbar")

function oncontextmenu(e) {
    const star = document.querySelector(".carousel-item.active .img_star");
    if(star) {
        if(star.textContent && 5 >= star.textContent && star.textContent >= 0) {
            startext = '星' + star.textContent;
        }
        else {
            startext = '';
        }
        for(a of menu.querySelectorAll('li')) {
            a.classList.toggle('active', startext && a.textContent == startext);
        }
    }
    myModalAlternative.show();
}

function addStar(star) {
    const a = document.querySelector(".carousel-item.active");
    if(a && a.id.startsWith('img_')) {
        error.textContent = "";
        const id = a.id.substring('img_'.length);
        const obj = { star: star };
        const body = JSON.stringify(obj);
        const headers = {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        };
        url = URLBASE + '/eagle/update/' + id;
        fetch(url, {method: "POST", headers: headers, body: body}).then((res) => {
            return res.json();
        }).then((json) => {
            starElement = a.querySelector(".img_star");
            if(star) {
                starElement.textContent = star;
            }
        })
        .catch((err) => {
            error.textContent = err;
        });
    }
}

function flipScreenMode(id = null) {
    const tocarousel = !slide.classList.contains('carousel');
    if(! id) {
        if(tocarousel) {
            let a = document.activeElement;
            while(a) {
                if(a.id.startsWith('img_')) {
                    id = a.id.substring('img_'.length);
                    break;
                }
                a = a.parent;
            }
        }
        else {
            let a = document.querySelector(".carousel-item.active");
            if(a && a.id.startsWith('img_')) {
                id = a.id.substring('img_'.length);
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
    navbar.classList.toggle('hidden', tocarousel)
    if(selected) {
        selected.scrollIntoView({block: 'start', behavior: 'instant'});
    }
}

function onimageclick(e, id) {
    const iscarousel = slide.classList.contains('carousel');
    if(iscarousel) {
        oncontextmenu(e);
    }
    else {
        flipScreenMode(id);        
    }
}

const templ = Handlebars.compile(
`<div id="img_{{id}}" class="col" tabindex="1">
    <a onclick='onimageclick(event, "{{id}}");'>
    <img class="img-thumbnail" src="{{URLBASE}}/images/{{id}}/{{thumbname}}" width="{{thumbwidth}}px" height="{{thumbheight}}px"
    {{#if noThumbnail }}data-rsrc="{{URLBASE}}/images/{{id}}/{{name}}.{{ext}}"{{/if}}>
    </a>
    <div class="img_infos">
    <div class="img_star badge bg-dark">{{#if star}}{{star}}{{/if}}</div>
    <div class="img_folders">
    {{#each folders}}<div class="img_folder badge bg-info">{{this}}</div>{{/each}}
    </div>
    <div class="img_tags">
    {{#each tags}}<div class="img_tag badge bg-secondary">{{this}}</div>{{/each}}
    </div>
    <div class="img_annotation bg-primary text-wrap">{{annotation}}</div>
    </div>
    <div class="row bg-secondary-subtle">
</div>`);

function fillnext() {
    const p = nextpanel.previousElementSibling;
    const iscarousel = slide.classList.contains('carousel');
    if(p && p.id.startsWith('img_')) {
        let id = p.id.substring('img_'.length);
        url = URLBASE + "/eagle/fetch/" + id + location.search;
    }
    else {
        url = URLBASE + "/eagle/fetch" + location.search;
    }
    error.textContent = "";
    fetch(url)
    .then((res) => {
        return res.json();
    })
    .then((json) => {
        for(i of json.images) {
            i.URLBASE = URLBASE;
            nextpanel.insertAdjacentHTML('beforebegin', templ(i));
            const f = nextpanel.previousElementSibling;
            if(iscarousel) {
                const g = f.querySelector('img');
                if(g) {
                    if(g.hasAttribute('width')) {
                        g.setAttribute('data-twidth', g.getAttribute('width'));
                        g.removeAttribute('width');
                    }
                    if(g.hasAttribute('height')) {
                        g.setAttribute('data-theight', g.getAttribute('height'));
                        g.removeAttribute('height');
                    }
                    if(g.hasAttribute('data-rsrc')) {
                        g.setAttribute('data-tsrc', g.getAttribute('src'));
                        g.setAttribute('src', g.getAttribute('data-rsrc'));
                        g.removeAttribute('data-rsrc');
                    }
                }
                f.classList.toggle('col', false);
                f.classList.toggle('carousel-item', true);
            }
        }
        nextpanel.classList.toggle('disabled', json.finish);
        if(iscarousel && nextpanel && p && p.nextElementSibling) {
            nextpanel.classList.toggle('active', false);
            if(p.nextElementSibling != nextpanel) {
                p.nextElementSibling.classList.toggle('active', true);
            }
            else {
                p.classList.toggle('active', true);
            }
        }
    })
    .catch((err) => {
        error.textContent = err;
    });
}
function resumeserver() {
    url = "http://qnap2.arimoto.biz:48880/qwol/WOL_script.php?time_string=+3 seconds&mac_address=00:d8:61:d8:16:50&secureon=&addr=192.168.3.0&cidr=24&port=9&store=No&submit=Send request";
    fetch(url,{mode: 'no-cors'});
}

function updateprogress(json) {
    progress = updating.querySelector(".progress");
    button = updating.querySelector("button");
    progressbar = updating.querySelector(".progress-bar");
    message = updating.querySelector(".alert");
    progress.setAttribute("aria-valuenow", json.progress);
    if(json.fullgage > 0) {
        fullgage = json.fullgage;
        progress.setAttribute("aria-valuemax", json.fullgage);
    }
    else {
        fullgage = 100;
    }
    progress = (json.progress * 100 / fullgage).toFixed(1) + "%";
    progressbar.style.width = progress;
    progressbar.textContent = progress;
    message.textContent = json.error;
    if(! json.running) {
        if(json.error == "") {
            message.textContent = "更新完了。処理:" + json.processed + "件。時間:" + json.elapsed;
        }
        button.textContent = "確認";
    }
    else {
        if(json.error == "") {
            message.textContent = "DB更新中..."
        }
        button.textContent = "中止";
    }
}

function endupdating() {
    progress = updating.querySelector(".progress");
    button = updating.querySelector("button");
    if(button.textContent == "中止") {
        fetch(URLBASE + "/eagle/updatedb/abort", {method: "POST"}).then((x) => {});
    }
    else {
        myUpdating.hide();
        progress.setAttribute("aria-valuenow", 0);
        progress.setAttribute("aria-valuemax", 100);
        button.textContent = "中止";    
    }
}

async function updatedb() {
    myUpdating.show();
    res = await fetch(URLBASE + "/eagle/updatedb/start", {method: "POST"});
    json = await res.json();
    updateprogress(json);
    while(json.running) {
        res = await fetch(URLBASE + "/eagle/updatedb/wait");
        json = await res.json();
        updateprogress(json);    
    }
}

function onvisible(entries, observer) {
    entries.forEach(entry => {
        if(entry.isIntersecting && entry.target.id == "img_next") {
            if(! nextpanel.classList.contains('disabled')) {
                setTimeout(() => { fillnext("") }, 500);
            }
        }
    });
}

function onload(event) {
    let options = {
      root: null,
      rootMargin: "0px",
      threshold: 0.95,
    };
    const observer = new IntersectionObserver(onvisible, options);
    observer.observe(nextpanel);
}

window.addEventListener("load", function(event) { this.onload(event); }, false);