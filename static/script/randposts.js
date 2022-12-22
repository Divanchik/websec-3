let ppanel = document.getElementById("posts_panel");
let username = window.location.pathname.slice(
  window.location.pathname.lastIndexOf("/") + 1
);

let heart =
  '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-heart"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>';

async function handleLike(event)
{
    let btn = event.currentTarget;
    try
    {
        let pname = btn.parentElement.parentElement.getAttribute('name');
        let pnum = parseInt(pname.slice(pname.lastIndexOf('_')+1));
        console.debug(`Clicked like on post #${pnum}`);
        url = window.location.href.slice();
        const response = await fetch(
            url,
            {
                method: "POST",
                body: JSON.stringify({action: "like", postnum: pnum}),
                headers: {'Content-Type': 'application/json'}
            }
        );
        const data = await response.json();
        console.debug(data);
        if (data['success'])
        {
            btn.classList.toggle('liked');
            btn.classList.toggle('notliked');
            btn.innerHTML = heart + data['likes'].toString();
        }
        else
            console.error("Server error on 'like' fetch!");
    }
    catch (error)
    {
        console.error("Caught error:", error);
    }
}

async function handleComment(event)
{
    let btn = document.querySelector('form > div > button');
    let pnum = parseInt(btn.getAttribute('postnumber'));
    event.preventDefault();
    let txtarea = document.getElementById('comment_text');
    console.log('handleComment', pnum, txtarea);
    try
    {
        url = window.location.href.slice();
        const response = await fetch(
            url,
            {
                method: "POST",
                body: JSON.stringify({action: "newcomment", content: txtarea.value, postnum: pnum}),
                headers: {'Content-Type': 'application/json'}
            }
        );
        txtarea.value = "";
    }
    catch (error)
    {
        console.error("Caught error:", error);
    }
}

function postHeader(author, datetime) {
  // header div
  let elem = document.createElement("div");
  elem.className =
    "row justify-content-start d-flex align-items-center border-bottom border-secondary";
  // info div
  let info = document.createElement("div");
  info.style.width = "fit-content";
  info.innerHTML = `<a class="h6 link-dark" href="/user/${author}">${author}</a><small class="text-secondary">${datetime}</small>`;
  elem.append(info);
  return elem;
}

function postBody(text, imageUrl) {
  let elem = document.createElement("div");
  elem.className = "row";
  let elem_text = document.createElement("p");
  elem_text.innerText = text;
  elem.append(elem_text);
  if (imageUrl != "") {
    let elem_image = document.createElement("img");
    elem_image.className = "mx-auto";
    elem_image.style.height = "500px";
    elem_image.style.width = "100%";
    elem_image.style.objectFit = "scale-down";
    elem_image.src = imageUrl;
    elem.append(elem_image);
  }
  return elem;
}

function postFooter(likes, liked, pnum) {
  // footer div
  let elem = document.createElement("div");
  elem.className =
    "row justify-content-between d-flex align-items-center border-top border-secondary";
  // like button
  let like_button = document.createElement("button");
  like_button.classList.add("btn");
  if (liked)
  {
    like_button.classList.add("liked");
  }
  else
  {
    like_button.classList.add("notliked");
  }
  like_button.innerHTML = heart + `${likes}`;
  like_button.style.width = "fit-content";
  like_button.onclick = handleLike;
  elem.append(like_button);
  // comments button
  let comment_button = document.createElement("button");
  comment_button.className = "btn btn-outline-primary";
  comment_button.innerText = "View comments";
  comment_button.style.width = "150px";
  comment_button.setAttribute("data-bs-toggle", "modal");
  comment_button.setAttribute("data-bs-target", "#commentsModal");
  comment_button.setAttribute("data-bs-pnum", `${pnum}`);
  elem.append(comment_button);
  return elem;
}

function commentHeader(author, datetime)
{
    let elem = document.createElement('div');
    elem.className = "row justify-content-start d-flex align-items-center border-top border-secondary";
    elem.innerHTML = `<h6>${author}</h6><small class="text-secondary">${datetime}</small>`;
    return elem;
}

function commentBody(ctext)
{
    let elem = document.createElement('div');
    elem.className = "row border-bottom border-secondary";
    let elem_text = document.createElement('p');
    elem_text.innerText = ctext;
    elem.append(elem_text);
    return elem;
}

(async () => {
  try {
    // get random posts
    url = window.location.href.slice();
    const response = await fetch(url, {
      method: "POST",
      body: JSON.stringify({ action: "getposts" }),
      headers: { "Content-Type": "application/json" },
    });
    const post_array = await response.json();
    console.debug(post_array);

    // display posts
    for (let i = 0; i < post_array.length; i++) {
      tpost = document.createElement("div");
      tpost.setAttribute("name", `post_${post_array[i]["post_id"]}`);
      tpost.className =
        "container-fluid border border-secondary rounded mt-2 bg-white";
      tpost.style.height = "fit-content";
      tpost.append(
        postHeader(post_array[i]["author"], post_array[i]["datetime"]),
        postBody(
          post_array[i]["content"],
          window.location.origin + `/image/${post_array[i]["image_id"]}`
        ),
        postFooter(
          post_array[i]["likes"],
          post_array[i]["isliked"],
          post_array[i]["post_id"]
        )
      );
      ppanel.append(tpost);
    }

    // modal event
    let modal = document.getElementById("commentsModal");
    modal.addEventListener("show.bs.modal", async function (event) {
      let btn = event.relatedTarget;
      let pnum = parseInt(btn.getAttribute("data-bs-pnum"));
      let cbtn = modal.querySelector("form > div > button");
      cbtn.setAttribute("postnumber", `${pnum}`);
      try {
        // fetch comments
        url = window.location.href.slice();
        const response = await fetch(url, {
          method: "POST",
          body: JSON.stringify({ action: "getcomments", postnum: pnum }),
          headers: { "Content-Type": "application/json" },
        });
        const comment_array = await response.json();
        let mbody = document.querySelector("div.modal-body");
        mbody.innerHTML = "";
        console.log(comment_array, mbody);
        // display comments

        for (let i = 0; i < comment_array.length; i++) {
          tcom = document.createElement("div");
          tcom.append(
            commentHeader(comment_array[i]["author"], comment_array[i]["date"]),
            commentBody(comment_array[i]["content"])
          );
          mbody.append(tcom);
        }
      } catch (error) {
        console.error("Caught error:", error);
      }
    });
  } catch (error) {
    console.error("Caught error:", error);
  }
})();
