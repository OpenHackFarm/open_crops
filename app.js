var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};

// https://stackoverflow.com/questions/736513/how-do-i-parse-a-url-into-hostname-and-path-in-javascript
function getLocation(href) {
    var match = href.match(/^(https?\:)\/\/(([^:\/?#]*)(?:\:([0-9]+))?)([\/]{0,1}[^?#]*)(\?[^#]*|)(#.*|)$/);
    return match && {
        href: href,
        protocol: match[1],
        host: match[2],
        hostname: match[3],
        port: match[4],
        pathname: match[5],
        search: match[6],
        hash: match[7],
        root: match[1] + '//' + match[2] + '/'
    }
}

function precisionRound(number, precision) {
    var factor = Math.pow(10, precision);
    return Math.round(number * factor) / factor;
}

var UploadCrop = {
    findByOpenCropId: function(id) {
        crops = [];

        $.ajax({
            url: 'https://api.airtable.com/v0/appSHD6QX03beYde1/open_crop_upload?filterByFormula={open_crop_binding}="' + id + '"',
            headers: { 'Authorization': 'Bearer key5cOGuWwOqmI1DV' },
            type: 'get',
            async: false,
            success:function(data){ crops = data['records']; },
            error:function(jqXHR, textStatus, errorThrown) { }
        });

        return crops;
    },
};

var OpenCrop = {
    set_cover: function(id, url) {
        if(confirm('Set cover photo?')) {
            $.ajax({
                url: 'https://api.airtable.com/v0/appSHD6QX03beYde1/open_crop/' + id,
                headers: { 'Authorization': 'Bearer key5cOGuWwOqmI1DV',
                    'Content-Type' : 'application/json',
                },
                type: 'PATCH',
                data: JSON.stringify({ "fields": {"cover": url} }),
                async: false,
                success:function(data){
                    alert('Success!');
                    location.reload(true);
                },
                error:function(jqXHR, textStatus, errorThrown) {
                    alert('Error!');
                }
            });
        }
    }
};

function get_opencrops() {
    crops = [];

    $.ajax({
        // url: "https://api.airtable.com/v0/appSHD6QX03beYde1/open_crop?sortField=family",
        url: "https://api.airtable.com/v0/appSHD6QX03beYde1/open_crop?sortField=id",
        headers: { 'Authorization': 'Bearer key5cOGuWwOqmI1DV' },
        type: 'get',
        async: false,
        success:function(data){
            crops = data['records'];
        },
        error:function(jqXHR, textStatus, errorThrown) {
            //alert(jqXHR.responseText);
            //alert(jqXHR.status);
            //alert(jqXHR.readyState);
            //alert(jqXHR.statusText);
            /*弹出其他两个参数的信息*/
            //alert(textStatus);
            //alert(errorThrown);
        }
    });

    return crops;
}

function get_opencrop(id) {
    $.ajax({
        url: "https://api.airtable.com/v0/appSHD6QX03beYde1/open_crop/" + id,
        headers: { 'Authorization': 'Bearer key5cOGuWwOqmI1DV' },
        type: 'get',
        success:function(crop){
            console.log(crop);

            data = [];
            data['id'] = crop['id'];
            data['AMIS'] = crop['fields']['AMIS'];
            data['common_names_zh'] = crop['fields']['common_names_zh'];
            data['common_names'] = crop['fields']['common_names'];
            data['binomial_name'] = crop['fields']['binomial_name']?crop['fields']['binomial_name']:crop['id'];
            if(crop['fields']['cover']){
                parse_url = getLocation(crop['fields']['cover']);
                new_url = parse_url['root'] + '350x350' + parse_url['pathname'];
                data['cover'] = new_url;
            } else {
                data['cover'] = '/No_Cover.jpg';
            }
            data['family'] = (crop['fields']['family'] ? '<a href="index.html?family=' + crop['fields']['family'] + '">' + crop['fields']['family'] + '</a>' + ' ' : '') + (crop['fields']['family_zh']?crop['fields']['family_zh']:'');
            data['genus'] = (crop['fields']['genus']?crop['fields']['genus'] + ' ':'') + (crop['fields']['genus_zh']?crop['fields']['genus_zh']:'');
            data['species'] = (crop['fields']['species']?crop['fields']['species'] + ' ':'') + (crop['fields']['species_zh']?crop['fields']['species_zh']:'');
            data['variety'] = (crop['fields']['variety']?crop['fields']['variety'] + ' ':'') + (crop['fields']['variety_zh']?crop['fields']['variety_zh']:'');
            data['origin'] = crop['fields']['origin'];
            data['invasive'] = (crop['fields']['invasive'] == 'Y') ? '具有入侵性' : '';
            data['propagate'] = crop['fields']['propagate'];
            data['row_spacing'] = crop['fields']['row_spacing'];
            habit = '';
            if(crop['fields']['habit'] == '草本') {
                habit += '<div class="iconbar-icon niche-icon niche-icon-shrub" title="草本">Shrub</div>';
            } else if(crop['fields']['habit'] == '草質藤本') {
                habit += '<div class="iconbar-icon niche-icon niche-icon-climber" title="草質藤本">Climber</div>';
            } else if(crop['fields']['habit'] == '喬木') {
                habit += '<div class="iconbar-icon niche-icon niche-icon-canopy" title="喬木">Canopy</div>';
            } else if(crop['fields']['habit'] == '灌木') {
                habit += '<div class="iconbar-icon niche-icon niche-icon-canopy" title="灌木">Canopy</div>';
            }
            if(crop['fields']['ground_cover'] == 'Y') {
                habit += '<div class="iconbar-icon niche-icon niche-icon-soil_surface" title="覆地">Soil surface</div>';
            }
            if(crop['fields']['aquatic'] == 'Y') {
                habit += '<div class="iconbar-icon water-icon water-icon-aquatic" title="水生"></div>';
            }
            data['icons'] = habit;

            render_detail(data);
        },
        error:function(jqXHR, textStatus, errorThrown) {
            //alert(jqXHR.responseText);
            //alert(jqXHR.status);
            //alert(jqXHR.readyState);
            //alert(jqXHR.statusText);
            /*弹出其他两个参数的信息*/
            //alert(textStatus);
            //alert(errorThrown);
        }
    });
}


function search_unique_opencrop(name) {
    data = null;

    $.ajax({
        url: 'https://api.airtable.com/v0/appSHD6QX03beYde1/open_crop?filterByFormula=(FIND("' + name + '",{common_names_zh}))',
        headers: { 'Authorization': 'Bearer key5cOGuWwOqmI1DV' },
        type: 'get',
        async: false,
        success:function(crop){
            if(crop['records'].length == 1){
                crop_list = crop['records'][0]['fields']['common_names_zh'].split(',');

                if(crop_list.indexOf(name) > -1){
                     data = crop['records'][0];
                }
            }
        },
        error:function(jqXHR, textStatus, errorThrown) {
        }
    });

    return data;
}

function binding_opencrop(upload_id, opencrop_id) {
    ret = false;

    $.ajax({
        url: 'https://api.airtable.com/v0/appSHD6QX03beYde1/open_crop_upload/' + upload_id,
        headers: { 'Authorization': 'Bearer key5cOGuWwOqmI1DV',
            'Content-Type' : 'application/json',
        },
        type: 'PATCH',
        data: JSON.stringify({ "fields": {"open_crop_binding": opencrop_id} }),
        async: false,
        success:function(data){
            // console.log('Success!');
            ret =  true;
        },
        error:function(jqXHR, textStatus, errorThrown) {
            // console.log('Error!');

            /*弹出jqXHR对象的信息*/
            //alert(jqXHR.responseText);
            //alert(jqXHR.status);
            //alert(jqXHR.readyState);
            //alert(jqXHR.statusText);
            /*弹出其他两个参数的信息*/
            //alert(textStatus);
            //alert(errorThrown);
        }
    });

    return ret;
}

function append_opencrop_common_name(id, name) {
    ret = false;

    // get crop
    crop = null;
    $.ajax({
        url: "https://api.airtable.com/v0/appSHD6QX03beYde1/open_crop/" + id,
        headers: { 'Authorization': 'Bearer key5cOGuWwOqmI1DV' },
        type: 'get',
        async: false,
        success:function(data){
            console.log(data);

            crop = data;
        },
        error:function(jqXHR, textStatus, errorThrown) {
            ret = false;
        }
    });

    if(crop) {
        names = crop['fields']['common_names_zh'];
        name_list = names.split(',');

        // if name not in common_names_zh
        if(names.indexOf(name) == -1) {
            names += ', ' + name;

            // update names
            $.ajax({
                url: 'https://api.airtable.com/v0/appSHD6QX03beYde1/open_crop/' + id,
                headers: { 'Authorization': 'Bearer key5cOGuWwOqmI1DV',
                    'Content-Type' : 'application/json',
                },
                type: 'PATCH',
                data: JSON.stringify({ "fields": {"common_names_zh": names} }),
                async: false,
                success:function(data){
                    ret = true;
                },
                error:function(jqXHR, textStatus, errorThrown) {
                    ret = false;
                }
            });
        } else {
            ret = true;
        }
    }

    return ret;
}

function render(mustache, data, id) {
    $.get(mustache, function(template) {
        var html = Mustache.to_html(template, data);
        $(id).html(html);
    });
}

function render_detail(data) {
    render('templates/detail.header.mustache', data, '#header');
    render('templates/detail.heading.mustache', data, '#heading');
    render('templates/detail.picture.mustache', data, '#picture');
    render('templates/detail.information.mustache', data, '#information');
}

function get_template(path) {
    template = '';

    $.ajax({
        url: path,
        async: false,
        success: function(t){ template = t; }
    });

    return template;
}

function count_temperature(temperatures) {
    data = {};
    data['hot_count'] = 0;
    data['warm_count'] = 0;
    data['cool_count'] = 0;
    data['cold_count'] = 0;
    total_temperatue = 0;

    total_count = temperatures.length;
    data['max_temperature'] = total_count ? Math.max.apply(Math, temperatures) : '-';
    data['min_temperature'] = total_count ? Math.min.apply(Math, temperatures) : '-';

    $.each(temperatures, function(index, value) {
        total_temperatue += value;
        if(value<10) {
            data['cold_count']++;
        } else if(value>=10 && value<20) {
            data['cool_count']++;
        } else if(value>=20 && value<30) {
            data['warm_count']++;
        } else if(value>=30) {
            data['hot_count']++;
        }
    });

    data['hot_percent'] = total_count ? data['hot_count'] / total_count * 100 : 0;
    data['warm_percent'] = total_count ? data['warm_count'] / total_count * 100 : 0;
    data['cool_percent'] = total_count ? data['cool_count'] / total_count * 100 : 0;
    data['cold_percent'] = total_count ? data['cold_count'] / total_count * 100 : 0;

    data['avg_temperature'] = total_count ? precisionRound(total_temperatue / total_count, 2) : '-';

    return data;
}
