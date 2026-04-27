# Frontend

Static photo album web application for Assignment 3.

## Local configuration

Copy the example config and add the shared API key:

```bash
cp frontend/config.example.js frontend/config.js
```

Edit `frontend/config.js`:

```js
window.PHOTO_ALBUM_CONFIG = {
  apiBaseUrl: "https://or7z11lo1g.execute-api.us-east-1.amazonaws.com/prod",
  apiKey: "your shared API key",
  region: "us-east-1",
  photoBaseUrl: ""
};
```

`frontend/config.js` is ignored by git because it contains the API key.

## Files to deploy

Upload these files to the frontend S3 static website bucket:

- `index.html`
- `styles.css`
- `app.js`
- `config.js`

The API key is visible to browser users after deployment. That is expected for this assignment API-key setup, but it should still not be committed to the repository.
