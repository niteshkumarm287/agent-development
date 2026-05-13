# Testing the Chrome Extension

## Setup

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt

# Set environment variables
export GCP_PROJECT_ID="game-d8160"
export GCP_REGION="us-central1"

# Run locally for testing
uvicorn main:app --reload --port 8000
```

### 2. Update Extension for Local Testing
Edit `extension/popup.js` line 1:
```javascript
const BACKEND = "http://localhost:8000/";
```

Update `extension/manifest.json` line 18-20:
```json
"host_permissions": [
  "http://localhost:8000/*"
]
```

### 3. Load Extension in Chrome

1. Open Chrome and go to `chrome://extensions/`
2. Enable **Developer mode** (toggle in top-right)
3. Click **Load unpacked**
4. Select the `extension/` folder
5. Extension should appear in your toolbar

## Testing Steps

### Test 1: Basic Functionality
1. Navigate to any webpage (e.g., news article, blog post)
2. Click the extension icon in toolbar
3. Popup should appear with 3 mode buttons
4. Click "Summarize this page"
5. Should show spinner, then summary

### Test 2: Different Modes
1. Click extension icon
2. Select "Bullets" mode
3. Click "Summarize this page"
4. Should return bullet points
5. Try "ELI5" mode similarly

### Test 3: Error Handling
1. Navigate to empty page or very short page
2. Click extension → Summarize
3. Should show error message

## Debugging

### Check Extension Console
1. Right-click extension icon → "Inspect popup"
2. Console shows JavaScript errors
3. Network tab shows API calls

### Check Backend Logs
Terminal running uvicorn shows request logs and errors

### Common Issues

**CORS Error**: Backend CORS allows `chrome-extension://*` but NOT `http://localhost`. For local testing, update backend CORS:
```python
allow_origins=["*"]  # Temporarily for testing
```

**Backend Not Running**: Verify backend is accessible:
```bash
curl http://localhost:8000/health
```

**Extension Permissions**: Ensure manifest.json has correct host_permissions for your backend URL

**No Content Extracted**: Check if page has extractable text (some sites use iframes/shadow DOM)

## Production Testing

To test with deployed backend:
1. Revert `popup.js` BACKEND to production URL
2. Revert `manifest.json` host_permissions to production
3. Reload extension in `chrome://extensions/`
4. Test on various websites

## Quick Test Sites
- https://en.wikipedia.org/wiki/Artificial_intelligence
- https://news.ycombinator.com/
- https://github.com/about
