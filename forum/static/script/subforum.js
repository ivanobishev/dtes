function starting()
{
    //-----[Modal]-----
    var modal = document.getElementById("modal");
    var modal_button = document.getElementById("modal-button");
    var cross = document.getElementById("cross");

    modal_button.addEventListener("click", function()
    {
        modal.style.display = "block";
    }, false);

    cross.addEventListener("click", function()
    {
        modal.style.display = "none";
    }, false);
    window.addEventListener("click", function(event)
    {
        if(event.target == modal)
        {
            modal.style.display = "none";
        }
    });

    //-----[Spoiler]-----
    var spoiler_button = document.getElementById("spoiler-button");
    var spoiler_container = document.getElementById("spoiler-container");
    var spoiler_styles = window.getComputedStyle(spoiler_container);

    spoiler_button.addEventListener("click", function()
    {
        if(spoiler_styles.visibility == "hidden")
        {
            spoiler_button.innerHTML = "Hide tags";
            spoiler_container.style.visibility = "visible";
        }
        else
        {
            spoiler_button.innerHTML = "Show tags";
            spoiler_container.style.visibility = "hidden";
        }
    }, false);
}
window.onload = starting;
