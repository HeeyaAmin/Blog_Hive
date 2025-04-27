// script.js
document.addEventListener("DOMContentLoaded", function() {
  const selectedKeywords = [];

  // Handle keyword button click
  document.querySelectorAll(".keyword-button").forEach(button => {
    button.addEventListener("click", function() {
      const value = button.value;
      if (selectedKeywords.includes(value)) {
        const index = selectedKeywords.indexOf(value);
        selectedKeywords.splice(index, 1);
        button.classList.remove('btn-primary');
        button.classList.add('btn-outline-primary');
      } else {
        selectedKeywords.push(value);
        button.classList.remove('btn-outline-primary');
        button.classList.add('btn-primary');
      }
    });
  });

  // Handle submit button click
  document.getElementById("submit-button").addEventListener("click", function() {
    if (selectedKeywords.length === 0) {
      alert("Please select at least one keyword!");
      return;
    }

    fetch("/generate_blogs", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ selected_keywords: selectedKeywords })
    })
    .then(response => response.json())
    .then(data => {
      const blogsContainer = document.getElementById("blogs-container");
      blogsContainer.innerHTML = '';

      if (data.matched_blogs.length === 0) {
        blogsContainer.innerHTML = '<p class="text-center">No blogs found for selected interests.</p>';
        return;
      }

      // Display matched blogs
      data.matched_blogs.forEach(blog => {
        const blogCard = `
          <div class="col-md-6 col-lg-4 mb-4">
            <div class="card h-100">
              <img src="/${blog.image_url}" class="card-img-top" alt="Blog Image">
              <div class="card-body">
                <h5 class="card-title">${blog.title}</h5>
                <p class="card-text">${blog.description}</p>
                <button class="btn btn-outline-warning save-button" data-blog-id="${blog.blog_id}">
                  Save to Favorites ⭐
                </button>
              </div>
            </div>
          </div>
        `;
        blogsContainer.innerHTML += blogCard;
      });

      // After adding blogs, attach event listeners for "Save to Favorites"
      setTimeout(() => {
        document.querySelectorAll(".save-button").forEach(button => {
          button.addEventListener("click", function() {
            const blogId = button.getAttribute('data-blog-id');

            fetch('/save_favorite', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({ blog_id: blogId })
            })
            .then(response => response.json())
            .then(data => {
              alert(data.message);
            })
            .catch(error => console.error("Error saving favorite:", error));
          });
        });
      }, 500);

    })
    .catch(error => console.error("Error fetching blogs:", error));
  });
});
