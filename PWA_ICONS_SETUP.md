# 🎨 PWA Icons Setup

Your app needs 2 PNG icons for installation. Here's how to create them:

## Option 1: Quick Online Tool (Easiest)

1. Go to [favicon.io](https://favicon.io)
2. Go to **"Generate from Text"**
3. Text: `AJ` (or your logo)
4. Font: Choose nice font (e.g., "Playfair Display")
5. Size: 512x512
6. Background: `#10b981` (green, matches theme)
7. Download
8. Generate from same tool with 192x192 size
9. Save both to `frontend/public/icons/`
   - `icon-192x192.png`
   - `icon-512x512.png`

## Option 2: Design Tool (Canva)

1. Go to [canva.com](https://canva.com)
2. Create **"Custom Size"** → 512x512px
3. Add text "AJ" or your logo
4. Use green color (#10b981)
5. Download as PNG
6. Resize to 192x192 using [pixlr.com](https://pixlr.com) or similar
7. Save both to `frontend/public/icons/`

## Option 3: AI Image Generation (High Quality)

Use any AI image tool (Midjourney, DALL-E, etc.):
- Prompt: "Minimalist letter 'AJ' logo, green (#10b981), flat design, PNG"
- Generate 512x512
- Resize to 192x192

## Folder Structure

After adding icons:
```
frontend/
├── public/
│   ├── icons/
│   │   ├── icon-192x192.png ← Required
│   │   └── icon-512x512.png ← Required
│   ├── manifest.json
│   └── sw.js
```

## Verify Icons

1. Icon exists at both sizes
2. Format is PNG
3. Background is transparent or solid green (#10b981)
4. Clear and recognizable at small size (192x192)

Once icons are in place, your PWA is fully installable! 🎉

## What If You Skip Icons?

The app still works! Just:
- "Add to Home Screen" might show a generic icon
- Android Chrome will show default icon
- iOS will show a blank screen icon

But functionality is 100% the same.

## Icon Sizes Explained

- **192x192** - Android home screen icons
- **512x512** - Splash screens, larger displays

Both are required for best experience across devices.

---

**Quick Summary:**
1. Create or download 512x512 PNG icon
2. Resize to 192x192 PNG
3. Save both to `frontend/public/icons/`
4. Done! ✅
