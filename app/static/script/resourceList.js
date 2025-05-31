class ResourceManager {
  constructor(resources, resourceTypes, containerSelector) {
    this.resources = resources;
    this.resourceTypes = resourceTypes;
    this.container = document.querySelector(containerSelector);
    this.activeType = null; // Default to "All"

    this.init();
  }

  init() {
    this.renderTabs();
    this.renderResources();
    this.addEventListeners();
  }

  renderTabs() {
    const tabContainer = document.createElement("div");
    tabContainer.className = "resource-tabs col-sm-12";

    this.resourceTypes.forEach(type => {
      const button = document.createElement("button");
      button.classList.add("tab-button");
      button.dataset.type = type.key === null ? "null" : type.key;
      button.textContent = type.value;

      if (type.key === null) {
        button.classList.add("active");
      }

      tabContainer.appendChild(button);
    });

    this.container.appendChild(tabContainer);
  }

  renderResources() {
  // Remove old list if it exists
  const oldList = this.container.querySelector(".resource-list");
  if (oldList) oldList.remove();

  const list = document.createElement("div");
  list.className = "resource-list";

  const filtered = this.getFilteredResources();

  if (filtered.length === 0) {
    const emptyMessage = document.createElement("p");
    emptyMessage.classList.add("empty-message");
    emptyMessage.textContent = "No resources found in this category.";
    list.appendChild(emptyMessage);
  } else {
    filtered.forEach(resource => {
      const card = document.createElement("a");
      card.className = "resource-card col-sm-4";

      if (["eBook"].includes(resource.resourceType)) {
        // Downloadable: gated or direct file
        card.href = resource.gateUrl || `/resources/${resource.slug}`;
        card.target = resource.gateUrl ? "_blank": "_self";

      } else if (["blog", "webinar"].includes(resource.resourceType)) {
        // Navigable resource (blog post or webinar page)
        // link.textContent = "Read More";
        card.href = resource.gateUrl || `/resources/${resource.slug}`;

      } else {
        // Unknown type fallback
        // link.textContent = "View Resource";
        card.href = "#";
      }


      const title = document.createElement("h3");
      title.className = "heading-4"
      title.textContent = resource.title;

      const badge = document.createElement("span");
      badge.classList.add("resource-badge");
      badge.textContent = resource.resourceType.charAt(0).toUpperCase() + resource.resourceType.slice(1);

      const summary = document.createElement("p");
      summary.className = "mt-2"
      summary.textContent = resource.summary;

      const link = document.createElement("a");
      link.classList.add("resource-cta");

      const thumbnail = document.createElement("div");
      thumbnail.className = "thumbnail-wrap"
      const thumbnailImage = document.createElement("img")
      thumbnailImage.setAttribute("src", resource.thumbnail.url)
      thumbnail.appendChild(thumbnailImage)
      thumbnail.appendChild(badge)

      if (["eBook"].includes(resource.resourceType)) {
        // Downloadable: gated or direct file
        link.textContent = "Get Resource";
        // link.href = resource.gateUrl || (resource.file?.url ?? "#");

      } else if (["blog", "webinar"].includes(resource.resourceType)) {
        // Navigable resource (blog post or webinar page)
        link.textContent = "Read More";
        link.href = resource.gateUrl || `/resources/${resource.slug}`;

      } else {
        // Unknown type fallback
        link.textContent = "View Resource";
        link.href = "#";
      }

      card.appendChild(thumbnail);

      card.appendChild(title);
      card.appendChild(link);
      list.appendChild(card);
    });
  }

  this.container.appendChild(list);
}

  getFilteredResources() {
    if (!this.activeType) return this.resources;
    return this.resources.filter(res =>
      (res.resourceType || "").toLowerCase() === (this.activeType || "").toLowerCase()
    );
  }

  addEventListeners() {
    this.container.addEventListener("click", (e) => {
      if (e.target.matches(".tab-button")) {
        const selected = e.target.dataset.type;
        this.activeType = selected === "null" ? null : selected;

        // Toggle active tab class
        this.container.querySelectorAll(".tab-button").forEach(btn => {
          btn.classList.remove("active");
        });
        e.target.classList.add("active");

        this.renderResources();
      }
    });
  }
}
