function submit(){
    $("#submit-bt").html('<div class="lds-spinner"><div></div><div></div><div></div><div>' +
        '</div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>');
    var title = $("#title").val();
    var description = $("#description").val();
    var client = $("#client").val();
    var product_area = $("#product_area").val();
    var target_date = $("#target_date").val();
    var level = $("#priority").val();
    if(title !== ""){
        if(description !== ""){
            if(client !== ""){
                if(product_area !== ""){
                    if(target_date !== ""){
                        if(level > 0){
                            $.post('/request/new', {title:title, description:description, client:client,
                                product_area:product_area, target_date:target_date, level:level}, function (data) {
                                alert(data);
                                $("#submit-bt").html('SUBMIT');
                                if(data === "The feature request was submitted successfully"){
                                    Lobibox.notify('success', {
                                        showClass: 'fadeIn',
                                        hideClass: 'fadeOut',
                                        msg: data
                                    });
                                    $("#title").val('');
                                    $("#description").val('');
                                    $("#client").val('');
                                    $("#product_area").val('');
                                    $("#target_date").val('');
                                    $("#priority").val("")
                                }else{
                                    Lobibox.notify('error', {
                                        showClass: 'fadeIn',
                                        hideClass: 'fadeOut',
                                        msg: data
                                    });
                                }
                            });
                        }else{
                            $("#submit-bt").html('SUBMIT');
                            Lobibox.notify('error', {
                                showClass: 'fadeIn',
                                hideClass: 'fadeOut',
                                msg: "The Priority Level must be greater than zero."
                            });
                        }
                    }else{
                        $("#submit-bt").html('SUBMIT');
                        Lobibox.notify('error', {
                            showClass: 'fadeIn',
                            hideClass: 'fadeOut',
                            msg: "The Target Date must be specified."
                        });
                    }
                }else{
                    $("#submit-bt").html('SUBMIT');
                    Lobibox.notify('error', {
                        showClass: 'fadeIn',
                        hideClass: 'fadeOut',
                        msg: "A Product Area is required."
                    });
                }
            }else{
                $("#submit-bt").html('SUBMIT');
                Lobibox.notify('error', {
                    showClass: 'fadeIn',
                    hideClass: 'fadeOut',
                    msg: "You have to select a client out of the list of clients"
                });
            }
        }else{
            $("#submit-bt").html('SUBMIT');
            Lobibox.notify('error', {
                    showClass: 'fadeIn',
                    hideClass: 'fadeOut',
                    msg: "The Description field is required"
                });
    }
    }else{
        $("#submit-bt").html('SUBMIT');
      Lobibox.notify('error', {
                    showClass: 'fadeIn',
                    hideClass: 'fadeOut',
                    msg: "The Title field is required!"
                });
    }

}

function existing(){
window.location.assign('/requests');
}
