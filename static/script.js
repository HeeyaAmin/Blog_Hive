//// script.js
// Authors: Heeya Mineshkumar Amin and Shail Jayesh Patel


document.addEventListener("DOMContentLoaded", function() {
  const selectedKeywords = [];

  // --------------------------------------------
  // Written by Heeya Mineshkumar Amin
  // Handle keyword button click selection/deselection
  // --------------------------------------------
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

  // --------------------------------------------
  // Written by Shail Jayesh Patel
  // Handle Generate Blogs button click and fetch request
  // --------------------------------------------
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

      if (!data.matched_blogs || data.matched_blogs.length === 0) {
        blogsContainer.innerHTML = '<p class="text-center">No blogs found for selected interests.</p>';
        return;
      }

      // --------------------------------------------
      // Written by Shail Jayesh Patel
      // Dynamically generate blog cards
      // --------------------------------------------
      data.matched_blogs.forEach(blog => {
        const blogCard = `
          <div class="col-md-6 col-lg-4 mb-4">
            <div class="card h-100">
              <img src="/${blog.image_url}" class="card-img-top" alt="Blog Image">
              <div class="card-body">
                <h5 class="card-title">${blog.title}</h5>
                <p class="card-text">${blog.description}</p>
              </div>
            </div>
          </div>
        `;
        blogsContainer.innerHTML += blogCard;
      });
    })
    .catch(error => console.error("Error fetching blogs:", error));
  });

});
