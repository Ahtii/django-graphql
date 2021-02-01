


// POPULATE TABLE WITH VEHICLE DATA

var sno;

function create_html_for_table_rows(data){        

    //var vehicles = data['vehicles'];
   // for (const vehicles in data) {
        console.log(data);
        for (const vehicle in data) {        
            var row_html = "<tr class='table-row'>\
                                <th scope='row'>"+sno+"</th>\
                                <td>"+data[vehicle]['id']+"</td>\
                                <td>"+data[vehicle]['name']+"</td>\
                                <td>"+data[vehicle]['price']+" lakh</td>\
                                <td>"+data[vehicle]['launchDate']+"</td>\
                                <td>"+data[vehicle]['vendor']['name']+"</td>\
                                <td>"+data[vehicle]['category']['name']+"</td>\
                            </tr>";  
                        
            sno += 1;
            $(".table-body").append(row_html);
        }                        
    //}    
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

var offset = 0, limit = $("#limit").val();
var has_next_page, has_prev_page, num_of_pages;

// pagination filter

function get_pagination_filter(){
    var offset_val = $("#offset").val();
    limit = $("#limit").val();
    var filter = "offset: "+offset+", limit: "+limit;
    console.log(filter);
    return filter;
}


const csrftoken = get_cookie('csrftoken');

// fetch new data from server

function fetch_new_data() {  
    $(".table-body").empty();  
    sno = 1;
    var filter = get_pagination_filter();
    fetch('http://localhost:8000/custom_graphql', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({            
            query: `
                        {
                            vehicleByOffsetPaginator(`+filter+`){
                                vehicles {
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
                                hasNext
                                hasPrev
                                totalPages
                            }
                        }
                    `
        })  
    })
    .then(res => res.json())
    .then(data => {                     
        create_html_for_table_rows(data['vehicleByOffsetPaginator']["vehicles"])
        has_next_page = data['vehicleByOffsetPaginator']["hasNext"];
        has_prev_page = data['vehicleByOffsetPaginator']["hasPrev"];
        num_of_pages = data['vehicleByOffsetPaginator']["totalPages"];
    });
}


var cursor_offset = 0, cursor_limit = $("#cursor-limit").val();
var cursor_has_next_page, cursor_has_prev_page, cursor_num_of_pages;

// pagination filter

function cursor_get_pagination_filter(){
    cursor_limit = $("#cursor-limit").val();
    var filter = "offset: "+cursor_offset+", limit: "+cursor_limit;
    return filter;
}

// fetch new data from server

function fetch_cursor_data() {  
    $(".cursor-table-body").empty();  
    sno = 1;
    var filter = cursor_get_pagination_filter();
    fetch('http://localhost:8000/custom_graphql', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify({            
            query: `
                        {
                            vehicleByCursorPaginator(`+filter+`){
                                vehicles {
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
                                hasNext
                                hasPrev
                                totalPages
                            }
                        }
                    `
        })  
    })
    .then(res => res.json())
    .then(data => {                     
        create_html_for_table_rows(data['vehicleByOffsetPaginator']["vehicles"])
        has_next_page = data['vehicleByOffsetPaginator']["hasNext"];
        has_prev_page = data['vehicleByOffsetPaginator']["hasPrev"];
        num_of_pages = data['vehicleByOffsetPaginator']["totalPages"];
    });
}



// GET ALL VEHICLES

$(document).ready(function(){  
        
    fetch_new_data();        

    $("#next").on("click", function(){
        if (has_next_page){
            if (offset == 0)
                offset = limit;
            else
                offset = parseInt(offset) + parseInt(limit);                       
            fetch_new_data();
        }    
    });    

    $("#prev").on("click", function(){
        if (has_prev_page){
            offset = offset - $("#limit").val();                        
            fetch_new_data();
        }           
    });

    $("#limit, #offset").on("change", function(){
        fetch_new_data();        
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
