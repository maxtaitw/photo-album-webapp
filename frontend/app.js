const config = window.PHOTO_ALBUM_CONFIG || {};

const state = {
  lastQuery: ""
};

const elements = {
  connectionStatus: document.querySelector("#connectionStatus"),
  fileName: document.querySelector("#fileName"),
  labelsInput: document.querySelector("#labelsInput"),
  messageArea: document.querySelector("#messageArea"),
  photoInput: document.querySelector("#photoInput"),
  refreshButton: document.querySelector("#refreshButton"),
  resultCount: document.querySelector("#resultCount"),
  resultsGrid: document.querySelector("#resultsGrid"),
  resultsTitle: document.querySelector("#resultsTitle"),
  searchForm: document.querySelector("#searchForm"),
  searchInput: document.querySelector("#searchInput"),
  uploadForm: document.querySelector("#uploadForm")
};

function getApiBaseUrl() {
  return String(config.apiBaseUrl || "").replace(/\/+$/, "");
}

function getHeaders(extraHeaders = {}) {
  const headers = { ...extraHeaders };
  if (config.apiKey) {
    headers["x-api-key"] = config.apiKey;
  }
  return headers;
}

function showMessage(message, type = "info") {
  elements.messageArea.textContent = message;
  elements.messageArea.className = `message-area ${type}`;
  elements.messageArea.hidden = false;
}

function formatNetworkError(error, action) {
  if (error instanceof TypeError && /load failed|failed to fetch/i.test(error.message)) {
    return `${action} could not reach API Gateway. Check the API URL, API Gateway CORS/OPTIONS, and allowed headers for x-api-key and x-amz-meta-customLabels.`;
  }

  return error.message;
}

function clearMessage() {
  elements.messageArea.hidden = true;
  elements.messageArea.textContent = "";
}

function setBusy(isBusy) {
  for (const button of document.querySelectorAll("button")) {
    button.disabled = isBusy;
  }
}

function encodeObjectKey(key) {
  return String(key || "")
    .split("/")
    .map((part) => encodeURIComponent(part))
    .join("/");
}

function resolvePhotoUrl(photo) {
  if (photo.url) {
    return photo.url;
  }

  if (config.photoBaseUrl && photo.objectKey) {
    return `${String(config.photoBaseUrl).replace(/\/+$/, "")}/${encodeObjectKey(photo.objectKey)}`;
  }

  if (photo.bucket && photo.objectKey) {
    const region = config.region || "us-east-1";
    return `https://${photo.bucket}.s3.${region}.amazonaws.com/${encodeObjectKey(photo.objectKey)}`;
  }

  return "";
}

function normalizeResults(body) {
  if (Array.isArray(body)) {
    return body;
  }
  if (Array.isArray(body.results)) {
    return body.results;
  }
  return [];
}

function getPhotoName(photo) {
  return photo.objectKey || photo.url || "photo";
}

function renderResults(results) {
  elements.resultsGrid.replaceChildren();
  elements.resultCount.textContent = `${results.length} result${results.length === 1 ? "" : "s"}`;

  if (results.length === 0) {
    showMessage("No matching photos found.", "warn");
    return;
  }

  clearMessage();

  for (const photo of results) {
    const card = document.createElement("article");
    card.className = "photo-card";

    const frame = document.createElement("div");
    frame.className = "photo-frame";

    const photoUrl = resolvePhotoUrl(photo);
    if (photoUrl) {
      const image = document.createElement("img");
      image.src = photoUrl;
      image.alt = getPhotoName(photo);
      image.loading = "lazy";
      image.addEventListener("error", () => {
        frame.replaceChildren(createFallback("Image URL is not publicly readable."));
      }, { once: true });
      frame.append(image);
    } else {
      frame.append(createFallback("No image URL returned."));
    }

    const body = document.createElement("div");
    body.className = "photo-body";

    const name = document.createElement("div");
    name.className = "photo-name";
    name.textContent = getPhotoName(photo);

    const labels = document.createElement("ul");
    labels.className = "label-list";
    for (const label of photo.labels || []) {
      const item = document.createElement("li");
      item.textContent = label;
      labels.append(item);
    }

    body.append(name, labels);
    card.append(frame, body);
    elements.resultsGrid.append(card);
  }
}

function createFallback(text) {
  const fallback = document.createElement("div");
  fallback.className = "photo-fallback";
  fallback.textContent = text;
  return fallback;
}

async function searchPhotos(query) {
  const apiBaseUrl = getApiBaseUrl();
  if (!apiBaseUrl || !config.apiKey) {
    showMessage("Create frontend/config.js with apiBaseUrl and apiKey before calling the API.", "error");
    return;
  }

  state.lastQuery = query;
  elements.resultsTitle.textContent = query ? `Results for "${query}"` : "Results";
  setBusy(true);
  clearMessage();

  try {
    const response = await fetch(`${apiBaseUrl}/search?q=${encodeURIComponent(query)}`, {
      headers: getHeaders()
    });
    const body = await response.json().catch(() => ({}));

    if (!response.ok) {
      throw new Error(body.message || `Search failed with HTTP ${response.status}`);
    }

    renderResults(normalizeResults(body));
  } catch (error) {
    showMessage(formatNetworkError(error, "Search"), "error");
  } finally {
    setBusy(false);
  }
}

function normalizeLabels(value) {
  return String(value || "")
    .split(",")
    .map((label) => label.trim())
    .filter(Boolean)
    .join(", ");
}

function buildObjectKey(file) {
  const safeName = file.name.replace(/[^A-Za-z0-9._-]/g, "-");
  return `${Date.now()}-${safeName}`;
}

async function uploadPhoto(file, labels) {
  const apiBaseUrl = getApiBaseUrl();
  if (!apiBaseUrl || !config.apiKey) {
    showMessage("Create frontend/config.js with apiBaseUrl and apiKey before uploading.", "error");
    return;
  }

  const objectKey = buildObjectKey(file);
  setBusy(true);
  clearMessage();

  try {
    const headers = getHeaders({
      "Content-Type": file.type || "application/octet-stream"
    });
    const normalizedLabels = normalizeLabels(labels);
    if (normalizedLabels) {
      headers["x-amz-meta-customLabels"] = normalizedLabels;
    }

    const response = await fetch(`${apiBaseUrl}/photos/${encodeObjectKey(objectKey)}`, {
      method: "PUT",
      headers,
      body: file
    });

    if (!response.ok) {
      const body = await response.text();
      throw new Error(body || `Upload failed with HTTP ${response.status}`);
    }

    elements.uploadForm.reset();
    elements.fileName.textContent = "Choose image";
    showMessage("Upload finished. Search by an automatic label or custom label after indexing completes.", "info");
  } catch (error) {
    showMessage(formatNetworkError(error, "Upload"), "error");
  } finally {
    setBusy(false);
  }
}

function updateConfigStatus() {
  const missing = [];
  if (!getApiBaseUrl()) {
    missing.push("apiBaseUrl");
  }
  if (!config.apiKey || config.apiKey === "PUT_YOUR_SHARED_API_KEY_HERE") {
    missing.push("apiKey");
  }

  if (missing.length > 0) {
    elements.connectionStatus.textContent = `Missing config: ${missing.join(", ")}`;
    return;
  }

  elements.connectionStatus.textContent = "Connected to deployed API";
}

elements.searchForm.addEventListener("submit", (event) => {
  event.preventDefault();
  searchPhotos(elements.searchInput.value.trim());
});

elements.uploadForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const file = elements.photoInput.files[0];
  if (!file) {
    showMessage("Choose an image before uploading.", "warn");
    return;
  }
  uploadPhoto(file, elements.labelsInput.value);
});

elements.photoInput.addEventListener("change", () => {
  const file = elements.photoInput.files[0];
  elements.fileName.textContent = file ? file.name : "Choose image";
});

elements.refreshButton.addEventListener("click", () => {
  searchPhotos(state.lastQuery || elements.searchInput.value.trim());
});

updateConfigStatus();
