


// POPULATE TABLE WITH VEHICLE DATA

var sno;

function create_html_for_table_rows(data){        

    //var vehicles = data['vehicles'];
    for (const vehicles in data) {
        for (const vehicle in data[vehicles]) {        
            var row_html = "<tr class='table-row'>\
                                <th scope='row'>"+sno+"</th>\
                                <td>"+data[vehicles][vehicle]['id']+"</td>\
                                <td>"+data[vehicles][vehicle]['name']+"</td>\
                                <td>"+data[vehicles][vehicle]['price']+" lakh</td>\
                                <td>"+data[vehicles][vehicle]['launchDate']+"</td>\
                                <td>"+data[vehicles][vehicle]['vendor']['name']+"</td>\
                                <td>"+data[vehicles][vehicle]['category']['name']+"</td>\
                            </tr>";  
                        
            sno += 1;
            $(".table-body").append(row_html);
        }                
    }    
}

// get csrftoken from cookie

function get_cookie(name){
    let cookie_value = null;
    if (document.cookie && document.cookie !== ''){
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++){
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')){
                cookie_value = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookie_value;
}

// show hide offset setting 

function show_hide_offset_setting(txt){
    if (txt == "Offset"){
        $(".from").removeClass("hide");
    } else {
        if (!$(".from").hasClass("hide"))
            $(".from").addClass("hide");
    }
}

// generate specific pagination query

function get_pagination_filter(txt){
    var filter_val = $("#filter").val();
    var filter = "first: "+filter_val;
    if (txt == "Last")
        filter = "last: "+filter_val;
    else if (txt == "Offset")
        filter = "first: "+$("#offset").val()+ ", offset: "+filter_val; 
    return filter;
}

const csrftoken = get_cookie('csrftoken');

// fetch new data from server

function fetch_new_data(pagination_filter) {
    $(".table-body").empty();
    sno = 1;
    fetch('http://localhost:8000/custom_graphql', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({            
            query: `
                        {
                            vehicleByPagination(`+pagination_filter+`){
                                id
                                name
                                price
                                launchDate
                                vendor {
                                name
                                }
                                category {
                                name
                                }
                            }
                        }
                    `
        })  
    })
    .then(res => res.json())
    .then(data => {    
        console.log(data);
        create_html_for_table_rows(data)    
    });
}


// GET ALL VEHICLES

$(document).ready(function(){  
        
    
    // first item selected

    $(".pagination-btn").text("First");

    // select particular pagination

    var pagination_filter = "first: "+$("#filter").val();

    $(".pagination-menu .dropdown-item").on("click", function(){
        var txt = $(this).text();
        show_hide_offset_setting(txt);
        pagination_filter = get_pagination_filter(txt);
        $(".pagination-btn").text(txt);
        fetch_new_data(pagination_filter);
    });    
    
    fetch_new_data(pagination_filter);

    $("#filter, #offset").on("change", function(){
        var txt = $(".pagination-btn").text();
        pagination_filter = get_pagination_filter(txt);        
        fetch_new_data(pagination_filter);        
    });    

    // fetch('http://localhost:8000/custom_graphql', {
    //     method: 'POST',
    //     headers: {
    //         "Content-Type": "application/json",
    //         "X-CSRFToken": csrftoken
    //     },
    //     body: JSON.stringify({            
    //         query: "\
    //             query {\
    //                 vehicles{\
    //                     id\
    //                     name\
    //                     price\
    //                     launchDate\
    //                     vendor {\
    //                         name\
    //                     }\
    //                     category {\
    //                         name\
    //                     }\
    //                 }\
    //             }\
    //         "
    //     })  
    // })
    // .then(res => res.json())
    // .then(data => {    
    //     console.log(data);
    //     create_html_for_table_rows(data)    
    // })
    // // after new data is avialible  
    // fetch('http://localhost:8000/custom_graphql', {
    //     method: 'POST',
    //     headers: {
    //         "Content-Type": "application/json",
    //         "X-CSRFToken": csrftoken
    //     },
    //     body: JSON.stringify({
    //         query: "\
    //             subscription {\
    //                 vendorUpdated {\
    //                     id\
    //                     name\
    //                 }\
    //             }\
    //         "
    //     })  
    // })
    // .then(res => res.json())
    // .then(data => {    
    //     //create_html_for_table_rows(data)    
    //     console.log(data);
    // })  
    
    // on click of more button
    $(".more-btn").on("click", function(){
        $(".more-menu").toggle();
    });

    // on click of add vendor
    $("#add-vendor").click(function(){
        $(".more-menu").toggle();
        $("#vendor-modal").modal("show");
    });

    // on click of add category
    $("#add-category").click(function(){
        $(".more-menu").toggle();
        $("#category-modal").modal("show");
    });

    // on click of add vehicle
    $("#add-vehicle").click(function(){
        $(".more-menu").toggle();
        $("#vehicle-modal").modal("show");
    });

    // on vendor form submit 
    $("#vendor-form").submit(function(e){
        e.preventDefault();        
        var value = $("#vendor-input").val();
        console.log(value);
        if (value){
            fetch("http://localhost:8000/custom_graphql", {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": $('#vendor-form input[name=csrfmiddlewaretoken]').val()
                },
                body: JSON.stringify(
                    {
                        query: "\
                            mutation addVendor($name: String!){\
                                addVendor(name: $name){\
                                    vendor {\
                                        id\
                                        name\
                                    }\
                                }\
                            }\
                        ",
                        variables: {"name": value}
                    }
                )  
            })
            .then(res => res.json())
            .then(data => {    
                console.log("got saved :)");                
                if (data == null)
                    alert("Error occured!");                
                else {
                    $("#vendor-modal .close").trigger("click");
                }    
            })             
        }
    });

    // on category form submit 
    $("#category-form").submit(function(e){
        e.preventDefault();        
        var value = $("#category-input").val();
        console.log(value);
        if (value){
            fetch("http://localhost:8000/custom_graphql", {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": $('#category-form input[name=csrfmiddlewaretoken]').val()
                },
                body: JSON.stringify(
                    {
                        query: "\
                            mutation addCategory($name: String!){\
                                addCategory(name: $name){\
                                    category {\
                                        id\
                                        name\
                                    }\
                                }\
                            }\
                        ",
                        variables: {"name": value}
                    }
                )  
            })
            .then(res => res.json())
            .then(data => {    
                console.log("got saved :)");                
                if (data == null)
                    alert("Error occured!");                
                else {
                    $("#category-modal .close").trigger("click");
                }    
            })             
        }
    });

    // on vehicle form submit 
    $("#vehicle-form").submit(function(e){
        e.preventDefault();   
        var inputs = {
            name: $("#vehicle-name-input").val(),
            price: $("#vehicle-price-input").val(),
            date: $("#vehicle-date-input").val(),
            vendor: $("#vehicle-vendor-input").val(),
            category: $("#vehicle-category-input").val()
        }     
        if (inputs['name'] || inputs['price'] || inputs['date'] || inputs['vendor'] || inputs['category']){
            fetch("http://localhost:8000/custom_graphql", {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": $('#category-form input[name=csrfmiddlewaretoken]').val()
                },
                body: JSON.stringify(
                    {
                        query: "\
                            mutation addVehicle($name: String!, $price: Decimal!, $launchDate: Date!, $vendor: String!, $category: String!){\
                                addVehicle(name: $name, price: $price, launchDate: $launchDate, vendor: $vendor, category: $category){\
                                        vehicle {\
                                            id\
                                            name\
                                            price\
                                            launchDate\
                                            vendor {\
                                                name\
                                            }\
                                            category {\
                                                name\
                                            }\
                                        }\
                                }\
                            }\
                        ",
                        variables: {
                            "name": inputs['name'],
                            "price": inputs['price'],
                            "launchDate": inputs['date'],
                            "vendor": inputs['vendor'],
                            "category": inputs['category']
                        }
                    }
                )  
            })
            .then(res => res.json())
            .then(data => {                                   
                if (data == null)
                    alert("Error occured!");                
                else {
                    var row_html = "<tr class='table-row'>\
                            <th scope='row'>"+sno+"</th>\
                            <td>"+data['addVehicle']['vehicle']['id']+"</td>\
                            <td>"+data['addVehicle']['vehicle']['name']+"</td>\
                            <td>"+data['addVehicle']['vehicle']['price']+" lakh</td>\
                            <td>"+data['addVehicle']['vehicle']['launchDate']+"</td>\
                            <td>"+data['addVehicle']['vehicle']['vendor']['name']+"</td>\
                            <td>"+data['addVehicle']['vehicle']['category']['name']+"</td>\
                        </tr>";  
                    
                    sno += 1;
                    $(".table-body").append(row_html);
                    $("#vehicle-modal .close").trigger("click");
                }    
            })             
        }
    });
});
