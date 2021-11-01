// manually adding the page in the search bar because previous search gave not only the query

let searchForm = document.getElementById("search_form");
let pageLink = document.getElementsByClassName("page-link");
if (searchForm) {
  for (let i = 0; pageLink.length > i; i++) {
    pageLink[i].addEventListener("click", function (e) {
      e.preventDefault();
      // get the data attribute
      let page = this.dataset.page;
      // This will append in the search bar i.e. ?page=django&page=2
      searchForm.innerHTML += `<input  value=${page} name="page" hidden/>`;
      searchForm.submit();
    });
  }
}

let tags = document.getElementsByClassName("project-tag");
for (let i = 0; i < tags.length; i++) {
  tags[i].addEventListener("click", (e) => {
    let tagId = e.target.dataset.tag;
    let projectId = e.target.dataset.project;
    fetch("http://127.0.0.1:8000/api/remove-tag/", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ project: projectId, tag: tagId }),
    })
      .then((response) => response.json)
      .then((data) => e.target.remove());
  });
}
