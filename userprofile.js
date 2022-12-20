let ppanel = document.getElementById("posts_panel");
let username = window.location.pathname.slice(window.location.pathname.lastIndexOf('/')+1);


let user_x = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#6c757d" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-user-x"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="8.5" cy="7" r="4"></circle><line x1="18" y1="8" x2="23" y2="13"></line><line x1="23" y1="8" x2="18" y2="13"></line></svg>'
let user_plus = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#0d6efd" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-user-plus"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="8.5" cy="7" r="4"></circle><line x1="20" y1="8" x2="20" y2="14"></line><line x1="23" y1="11" x2="17" y2="11"></line></svg>'
let heart_0 = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ff0000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-heart"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>';
let heart_1 = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#6c757d" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-heart"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>';

function handleLike(event)
{
    console.log(event.type);
}

function postHeader(author, datetime)
{
    let elem = document.createElement('div');
    elem.className = "row justify-content-start d-flex align-items-center border-bottom border-secondary";
    let ch1 = document.createElement('div');
    ch1.style.width = 'fit-content';
    ch1.innerHTML = `<h6>${author}</h6><small class="text-secondary">${datetime}</small>`;
    elem.append(ch1);
    return elem;
}

function postBody(text, imageUrl)
{
    let elem = document.createElement('div');
    elem.className = "row";
    let elem_text = document.createElement('p');
    elem_text.innerText = text;
    let elem_image = document.createElement('img');
    elem_image.className='mx-auto';
    elem_image.style.maxHeight = '500px';
    elem_image.style.maxWidth = '500px';
    elem_image.src = imageUrl;
    elem.append(elem_text, elem_image);
    return elem;
}

function postFooter(likes, liked)
{
    let elem = document.createElement('div');
    elem.className = "row justify-content-between d-flex align-items-center border-top border-secondary";
    let like_button = document.createElement('button');
    like_button.className = "btn notliked";
    like_button.style.width = 'fit-content';
    like_button.onclick = handleLike;
    like_button.innerHTML = heart_0 + `${likes}`;
    elem.append(like_button);
    return elem;
}

(async () => {
    try
    {
        url = window.location.href.slice();
        const response = await fetch(
            url,
            {
                method: "POST",
                body: JSON.stringify({action: "getposts", username: username}),
                headers: {'Content-Type': 'application/json'}
            }
        );
        const post_array = await response.json();
        console.debug(post_array);

        for (let i = 0; i < post_array.length; i++)
        {
            tpost = document.createElement('div');
            tpost.nodeName = `post_${post_array[i]["post_id"]}`;
            tpost.className = "container-fluid border border-secondary rounded mt-2 bg-white";
            tpost.style.height = 'fit-content';
            tpost.append(
                postHeader(post_array[i]["author"], post_array[i]["datetime"]),
                postBody(post_array[i]["content"], window.location.origin + `/image/${post_array[i]["image_id"]}`),
                postFooter(post_array[i]["likes"], post_array[i]["isliked"])
            );
            ppanel.append(tpost);
        }

    }
    catch (error)
    {
        console.error("Caught error:", error)
    }
})();