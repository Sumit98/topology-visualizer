function ValidateIPaddress(inputText)
 {
    console.log(inputText.value)
    var ipformat = /^(?:(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?:,? ?)){1,50}$/;
    if(inputText.value.match(ipformat))
    {
        document.ip_validation.ip_addr.focus();
        console.log(inputText.value)
        $(document.getElementById("loading")).show();
        return true;
    }
    else
    {
        alert("You have entered an invalid IP address!");
        document.ip_validation.ip_addr.focus();
        return false;
    }
 }