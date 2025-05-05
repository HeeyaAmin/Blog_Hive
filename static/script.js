//// script.js
// Authors: Heeya Mineshkumar Amin and Shail Jayesh Patel
// Example function (modify to suit your setup)
document.getElementById("submit-button").addEventListener("click", function () {
  const blogContainer = document.getElementById("blogs-container");

  // Optionally clear previous content
  blogContainer.innerHTML = "";

  // Your logic to fetch/generate blogs, for now simulate one:
  const blogHTML = `
    <div class="col-md-4 mb-4 blog-card">
      <div class="card shadow-sm h-100">
        <img src="https://via.placeholder.com/400x200" class="card-img-top" alt="Blog Image">
        <div class="card-body">
          <h5 class="card-title">Blog Title</h5>
          <p class="card-text">Blog Description</p>
        </div>
      </div>
    </div>
  `;

  blogContainer.innerHTML += blogHTML;

  // Remove `d-none` and add animation
  blogContainer.classList.remove("d-none");
});

document.addEventListener("DOMContentLoaded", function () {
  const selectedKeywords = {};
  const modal = document.getElementById("adjectiveModal");
  const adjectiveBox = document.getElementById("adjective-options");
  const modalTitle = document.getElementById("modal-title");
  let currentKeyword = "";

  // Keyword click to open modal
  document.querySelectorAll(".keyword-button").forEach(button => {
    button.addEventListener("click", function () {
      const keyword = button.value;
      const isSelected = button.classList.contains("btn-primary");

      if (isSelected) {
        button.classList.remove("btn-primary");
        button.classList.add("btn-outline-primary");
        delete selectedKeywords[keyword];
        return;
      }

      currentKeyword = keyword;
      modalTitle.innerText = `Select adjectives for "${currentKeyword}"`;
      adjectiveBox.innerHTML = "";

      fetch(`/get_adjectives/${currentKeyword}`)
        .then(response => response.json())
        .then(adjectives => {
          adjectives.forEach(adj => {
            const label = document.createElement("label");
            label.classList.add("m-2");

            const checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.value = adj;
            checkbox.classList.add("form-check-input", "me-1");

            if (selectedKeywords[currentKeyword]?.includes(adj)) {
              checkbox.checked = true;
            }

            label.appendChild(checkbox);
            label.appendChild(document.createTextNode(adj));
            adjectiveBox.appendChild(label);
          });

          modal.classList.remove("d-none");
          document.body.classList.add("modal-open");
        });
    });
  });

  // Confirm adjectives
  document.getElementById("confirm-adjectives").addEventListener("click", () => {
    const selected = [];
    adjectiveBox.querySelectorAll("input:checked").forEach(cb => {
      selected.push(cb.value);
    });

    selectedKeywords[currentKeyword] = selected;

    // Highlight the selected keyword button
    document.querySelectorAll(".keyword-button").forEach(btn => {
      if (btn.value === currentKeyword) {
        btn.classList.remove("btn-outline-primary");
        btn.classList.add("btn-primary");
      }
    });

    modal.classList.add("d-none");
    document.body.classList.remove("modal-open");
  });

  // Cancel adjectives
  document.getElementById("cancel-adjectives").addEventListener("click", () => {
    modal.classList.add("d-none");
    document.body.classList.remove("modal-open");
  });

  // Generate blogs
  document.getElementById("submit-button").addEventListener("click", function () {
    const blogContainer = document.getElementById("blogs-container");
    blogContainer.innerHTML = "";
    blogContainer.classList.remove("d-none");

    if (Object.keys(selectedKeywords).length === 0) {
      alert("Please select at least one keyword and its adjectives!");
      return;
    }

    // Loading state
    this.classList.add("loading");

    fetch("/generate_blogs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ keyword_adjectives: selectedKeywords })
    })
      .then(response => response.json())
      .then(data => {
        this.classList.remove("loading");

        if (!data.matched_blogs || data.matched_blogs.length === 0) {
          blogContainer.innerHTML = '<p class="text-center">No blogs found for selected interests.</p>';
          return;
        }

        data.matched_blogs.forEach(blog => {
          const blogCard = `
            <div class="col-md-6 col-lg-4 mb-4 blog-card">
              <div class="card h-100 shadow-sm">
                <img src="/${blog.image_url}" class="card-img-top" alt="Blog Image">
                <div class="card-body">
                  <h5 class="card-title">${blog.title}</h5>
                  <p class="card-text">${blog.description}</p>
                  <button class="btn btn-outline-danger btn-sm favorite-btn"
                          data-title="${blog.title}"
                          data-description="${blog.description}"
                          data-image="${blog.image_url}">
                          ❤️ Favorite
                  </button>

                </div>
              </div>
            </div>`;
          blogContainer.innerHTML += blogCard;
        });

        attachFavoriteListeners();
      })
      .catch(error => {
        this.classList.remove("loading");
        console.error("Error:", error);
      });
  });

  // Attach listeners to favorite buttons
  function attachFavoriteListeners() {
    document.querySelectorAll(".favorite-btn").forEach(button => {
      button.addEventListener("click", function () {
        const blog = {
            title: this.getAttribute("data-title"),
            description: this.getAttribute("data-description"),
            image_url: this.getAttribute("data-image")
        };


        fetch("/favorite_blog", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(blog)
        })
          .then(res => res.json())
          .then(response => {
            if (response.status === "success") {
              this.innerText = "💖 Favorited";
              this.disabled = true;
            } else if (response.status === "already_favorited") {
              alert("This blog is already in your favorites!");
              this.innerText = "💖 Favorited";
              this.disabled = true;
            }
          })
          .catch(error => {
            console.error("Favorite error:", error);
          });
      });
    });
  }
});



