function starting()
{
    //-----[Showing the form]-----
    var spoiler_button = document.getElementById("spoiler-button");
    var spoiler_container = document.getElementById("spoiler-container");

    spoiler_button.addEventListener("click", function() 
    {
        spoiler_button.style.visibility = "hidden";
        spoiler_container.style.visibility = "visible";
    }, false);
}
window.onload = starting;
